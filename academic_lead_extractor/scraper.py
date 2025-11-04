"""
Async University Staff Scraper v3
Mode: B (Auto-discover staff subpages only)
Author: Patched for Miki (2025)

✅ Features:
- Async crawling (aiohttp + asyncio)
- Auto-detects staff/people/team pages
- Extracts contacts (name, title, email, page URL, text)
- Handles obfuscated emails (∂, [at], (at), dot notation, etc.)
- Domain-restricted crawl (no external links)
- Depth-limited & page-limited (prevents infinite crawl)
- Passes extracted contacts to AI & enrichment pipeline
"""

import asyncio
import aiohttp
import re
from urllib.parse import urljoin, urlparse
from selectolax.parser import HTMLParser
from typing import List, Dict, Set
from config import (
    STAFF_PAGE_KEYWORDS,
    EXCLUDE_URL_PATTERNS,
    EMAIL_OBFUSCATION_PATTERNS,
    EXCLUDE_EMAIL_PATTERNS,
    MAX_PAGES_PER_DOMAIN,
    MAX_CRAWL_DEPTH,
    USER_AGENTS,
    DEBUG,
    EMAIL_REGEX,
    STAFF_CARD_SELECTORS,
    TITLE_HINT_CLASSES,
    FIELD_KEYWORDS
)

# ----------------------------------------
# GLOBAL SESSION LIMITS
# ----------------------------------------
CONNECTIONS = 20  # max concurrent HTTP requests
TIMEOUT = aiohttp.ClientTimeout(total=15)

# ----------------------------------------
# URL FILTERS
# ----------------------------------------

def is_same_domain(base: str, link: str) -> bool:
    """Keep only links on same domain as start URL."""
    try:
        return urlparse(base).netloc == urlparse(link).netloc
    except:
        return False


def allowed_url(url: str) -> bool:
    """Reject URLs matching excluded patterns (press, events, pdfs, etc.)"""
    if any(p.lower() in url.lower() for p in EXCLUDE_URL_PATTERNS):
        return False
    if url.endswith(".pdf") or url.endswith(".jpg") or url.endswith(".png"):
        return False
    return True


def looks_like_staff_page(text: str, url: str) -> bool:
    """Heuristic: detect staff/team/people directories before parsing full HTML."""
    text_l = text.lower()
    url_l = url.lower()

    # If title or URL contains staff keywords → strong signal
    for k in STAFF_PAGE_KEYWORDS:
        if k.lower() in url_l:
            if DEBUG:
                print(f"   ✅ STAFF KEYWORD MATCH in URL: '{k}' in {url}")
            return True
        if k.lower() in text_l:
            if DEBUG:
                print(f"   ✅ STAFF KEYWORD MATCH in TITLE: '{k}' in '{text[:80]}'")
            return True
    return False


# ----------------------------------------
# ASYNC FETCH WITH RETRY + UA ROTATION
# ----------------------------------------

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch a page with retry + rotating User-Agent."""
    headers = {"User-Agent": USER_AGENTS[hash(url) % len(USER_AGENTS)]}

    for attempt in range(3):
        try:
            async with session.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True) as resp:
                if resp.status == 200 and resp.headers.get("content-type", "").startswith("text/html"):
                    return await resp.text()
        except Exception as e:
            if DEBUG:
                print(f"   ⚠️ fetch failed ({attempt+1}/3) for {url}: {e}")
        await asyncio.sleep(0.7 * (attempt + 1))  # backoff

    return ""  # failed


# ----------------------------------------
# EMAIL FIXING / UNOBFUSCATION
# ----------------------------------------

def clean_email(raw: str) -> str:
    """Convert obfuscated emails to real email formats."""
    email = raw.strip()

    for pattern, repl in EMAIL_OBFUSCATION_PATTERNS.items():
        email = re.sub(pattern, repl, email, flags=re.IGNORECASE)

    # Remove double spaces, trailing dots
    email = email.replace(" ", "").replace("..", ".")
    return email if "@" in email else ""


def is_academic_email(email: str) -> bool:
    """Check if email looks like an academic researcher (not generic admin/office)."""
    if not email or "@" not in email:
        return False
    
    email_lower = email.lower()
    
    # Exclude generic admin/office emails (check if pattern appears anywhere in email)
    for pattern in EXCLUDE_EMAIL_PATTERNS:
        if pattern in email_lower:
            return False
    
    return True


# ----------------------------------------
# MAIN CRAWLER
# ----------------------------------------

class StaffCrawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.queued: Set[str] = set()  # Track URLs queued for crawling
        self.found_pages: List[str] = []
        self.contacts: List[Dict] = []

    async def crawl(self):
        """Main entry: start async crawl with queue."""
        connector = aiohttp.TCPConnector(limit=CONNECTIONS, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            await self._crawl_recursive(self.start_url, session, depth=0)
        return self.contacts

    async def _crawl_recursive(self, url: str, session, depth: int):
        """Depth-limited recursive crawler."""
        if depth > MAX_CRAWL_DEPTH:
            return
        if len(self.visited) > MAX_PAGES_PER_DOMAIN:
            return
        if url in self.visited:
            return
        self.visited.add(url)

        html = await fetch(session, url)
        if not html:
            if DEBUG and depth == 0:
                print(f"   ⚠️ Failed to fetch: {url}")
            return

        tree = HTMLParser(html)
        title = (tree.css_first("title").text(strip=True) if tree.css_first("title") else "")
        
        if DEBUG and depth == 0:
            print(f"   📄 [D{depth}] Checking: {url[:80]}... (title: {title[:40]}...)")

        # Detect potential staff pages
        is_staff_page = looks_like_staff_page(title, url)
        if DEBUG and "mitarbeitende" in url.lower():
            print(f"   🔍 Checking 'mitarbeitende' URL: {url}")
            print(f"      Title: {title}")
            print(f"      is_staff_page: {is_staff_page}")
        
        if is_staff_page:
            if DEBUG:
                print(f"   ✅ STAFF PAGE FOUND: {url}")
            self.found_pages.append(url)
            extracted = extract_contacts_from_html(html, url)
            self.contacts.extend(extracted)
            if DEBUG:
                print(f"      → Extracted {len(extracted)} contacts")

        # Find further links and crawl them
        tasks = []
        for link in tree.css("a"):
            href = link.attrs.get("href", "")
            if not href:
                continue

            full_url = urljoin(url, href)

            if not is_same_domain(self.start_url, full_url):
                continue
            if not allowed_url(full_url):
                continue
            if full_url in self.visited or full_url in self.queued:
                continue

            # Mark as queued to avoid duplicate tasks
            self.queued.add(full_url)
            tasks.append(self._crawl_recursive(full_url, session, depth + 1))
        
        if DEBUG and depth == 0:
            print(f"   📋 Found {len(tasks)} child URLs to crawl from homepage")
        
        # Wait for all child crawls to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

            # ----------------------------------------
# CONTACT EXTRACTION (HTML → structured contacts)
# ----------------------------------------

def _text(node) -> str:
    try:
        return node.text(separator=" ", strip=True)
    except Exception:
        return ""


def _join_clean(parts):
    return " ".join(p for p in (parts or []) if p).strip()


def _collect_page_text(tree: HTMLParser) -> str:
    # Collect a reasonable amount of page text for AI scoring/enrichment.
    # Skip nav/footer common sections if IDs/classes suggest so.
    big_chunks = []
    for sel in ["main", "article", ".content", "#content", ".container", "body"]:
        n = tree.css_first(sel)
        if n:
            t = _text(n)
            if t and len(t) > 600:
                big_chunks.append(t)
    if not big_chunks:
        big_chunks.append(_text(tree.root)[:8000])
    txt = " ".join(big_chunks)
    # Normalize whitespace
    return re.sub(r"\s+", " ", txt).strip()[:12000]


def _extract_emails_from_tree(tree: HTMLParser) -> List[str]:
    found = set()
    # 1) mailto links
    for a in tree.css("a[href]"):
        href = a.attrs.get("href", "")
        if href.startswith("mailto:"):
            raw = href.split("mailto:", 1)[1]
            cleaned = clean_email(raw)
            if cleaned:
                found.add(cleaned)

    # 2) inline text patterns (including obfuscations)
    body_text = _text(tree.root)
    # Normalize common obfuscations first (the regex-based clean_email will also run later)
    candidates = re.findall(EMAIL_REGEX, body_text, flags=re.I)
    for cand in candidates:
        cleaned = clean_email(cand)
        if cleaned:
            found.add(cleaned)

    return list(found)


def _looks_like_person_block(n: HTMLParser) -> bool:
    """
    Heuristic to identify a "person card" container.
    """
    classes = (n.attributes.get("class") or "").lower()
    role = (n.attributes.get("role") or "").lower()
    aria = (n.attributes.get("aria-label") or "").lower()
    idv = (n.attributes.get("id") or "").lower()

    signals = ["person", "people", "staff", "mitarbeiter", "team", "faculty", "researcher", "professor"]
    blob = " ".join([classes, role, aria, idv])
    return any(s in blob for s in signals)


def _guess_name_from_node(n: HTMLParser) -> str:
    # Try common tags (priority order)
    for sel in ["h1", "h2", "h3", "h4", ".name", ".staff-name", ".person-name", ".profile-name", 
                "[itemprop='name']", "strong", "b"]:
        node = n.css_first(sel)
        if node:
            txt = _text(node)
            # Name should be 2-6 words and look like a person name (not email/url)
            if 2 <= len(txt.split()) <= 6 and "@" not in txt and "." not in txt[:10]:
                return txt
    
    # Try link text (often person's name is a link)
    for a in n.css("a"):
        txt = _text(a)
        if 2 <= len(txt.split()) <= 6 and "@" not in txt:
            # Check if it looks like a name (starts with capital)
            if txt and txt[0].isupper():
                return txt
    
    # Fallback: first strong/b inside
    for node in n.css("strong, b"):
        txt = _text(node)
        if 2 <= len(txt.split()) <= 6 and "@" not in txt:
            return txt
    
    # Nothing obvious
    return ""


def _guess_title_from_node(n: HTMLParser) -> str:
    # Look for labels like title/position/role
    for sel in TITLE_HINT_CLASSES:
        node = n.css_first(sel)
        if node:
            t = _text(node)
            if t and len(t) >= 3:
                return t
    # Common small tags under name
    for sel in ["small", ".role", ".position", ".title", "em", "i", "p"]:
        node = n.css_first(sel)
        if node:
            t = _text(node)
            if t and len(t) >= 3 and len(t) < 200:
                return t
    return ""


def _guess_field_from_text(txt: str) -> str:
    txt_l = txt.lower()
    for field, kws in FIELD_KEYWORDS.items():
        for kw in kws:
            if kw in txt_l:
                return field
    return ""


def extract_contacts_from_html(html: str, page_url: str) -> List[Dict]:
    tree = HTMLParser(html)
    page_text = _collect_page_text(tree)

    contacts: List[Dict] = []

    # 1) Try structured "person cards" (common in KIT/DE sites)
    candidate_nodes = []
    for sel in STAFF_CARD_SELECTORS:
        candidate_nodes.extend(tree.css(sel))
    # Also add generic divs that look like person blocks (class/role heuristics)
    for div in tree.css("div"):
        if _looks_like_person_block(div):
            candidate_nodes.append(div)

    # Deduplicate nodes by id/ref
    seen_ids = set()
    person_nodes = []
    for n in candidate_nodes:
        key = id(n)
        if key not in seen_ids:
            seen_ids.add(key)
            person_nodes.append(n)

    # 2) Extract from person nodes
    per_node_emails = set()
    for node in person_nodes:
        name = _guess_name_from_node(node)
        title = _guess_title_from_node(node)

        # Emails in node scope - try to find each email's specific context
        emails_with_context = []
        for a in node.css("a[href]"):
            href = a.attrs.get("href", "")
            if href.startswith("mailto:"):
                cleaned = clean_email(href.split("mailto:", 1)[1])
                if cleaned and is_academic_email(cleaned):  # Filter admin emails
                    # Try to find name near this specific mailto link
                    local_name = ""
                    
                    # Strategy 1: Check link text itself (if it's a name, not the email)
                    link_text = _text(a).strip()
                    if link_text and "@" not in link_text and len(link_text.split()) >= 2:
                        local_name = link_text
                    
                    # Strategy 2: Check previous sibling (often: <span>Name</span><a>email</a>)
                    if not local_name and a.prev:
                        prev_text = _text(a.prev).strip()
                        if prev_text and "@" not in prev_text and len(prev_text.split()) >= 2:
                            local_name = prev_text
                    
                    # Strategy 3: Check parent text (e.g., <li>Name <a>email</a></li>)
                    if not local_name:
                        link_parent = a.parent
                        if link_parent:
                            parent_text = _text(link_parent).strip()
                            # Remove the email from parent text to avoid matching it
                            parent_text = parent_text.replace(cleaned, "").replace(href, "")
                            # Look for a name pattern (2-4 capitalized words)
                            name_match = re.search(r"([A-ZÄÖÜ][a-zäöüß\-']+(?:[\s,]+[A-ZÄÖÜ][a-zäöüß\-']+){1,3})", parent_text)
                            if name_match:
                                potential_name = name_match.group(1).strip(", ")
                                # Verify it looks like a person name (not too long, no numbers)
                                if len(potential_name.split()) <= 5 and not re.search(r'\d', potential_name):
                                    local_name = potential_name
                    
                    emails_with_context.append((cleaned, local_name))
        
        # Also scan node text for obfuscated emails (harder to get context)
        node_text = _text(node)
        for m in re.findall(EMAIL_REGEX, node_text, flags=re.I):
            cleaned = clean_email(m)
            if cleaned and is_academic_email(cleaned):  # Filter admin emails
                # Check if we already have this email from mailto links
                if not any(e[0] == cleaned for e in emails_with_context):
                    emails_with_context.append((cleaned, ""))

        # If no emails on card, we might still create a record and fill email later from page-level scan
        if not emails_with_context and (name or title):
            contacts.append({
                "Full_name": name or "",
                "Email": "",
                "Title_role": title or "",
                "Field_of_study": _guess_field_from_text(node_text) or "",
                "page_text": node_text[:6000] if node_text else page_text[:6000],
                "source_url": page_url,
            })
        else:
            for em, local_name in emails_with_context:
                if em in per_node_emails:
                    continue
                per_node_emails.add(em)
                # Prefer local name (found near the email) over node-level name
                final_name = local_name if local_name else name
                contacts.append({
                    "Full_name": final_name or "",
                    "Email": em,
                    "Title_role": title or "",
                    "Field_of_study": _guess_field_from_text(node_text) or "",
                    "page_text": node_text[:6000] if node_text else page_text[:6000],
                    "source_url": page_url,
                })

    # 3) If no person-cards detected, fall back to page-level email/name mining
    if not contacts:
        page_emails = _extract_emails_from_tree(tree)
        # Filter out generic admin emails
        page_emails = [em for em in page_emails if is_academic_email(em)]
        # Try to match nearby name/title snippets around emails (simple heuristic)
        if page_emails:
            # Pull short paragraphs/rows likely to contain profiles
            blocks = tree.css("p, li, tr, .row, .teaser, .card, .media, .grid, .list, .vcard")
            for em in page_emails:
                best_block = None
                best_score = -1
                for b in blocks[:400]:
                    t = _text(b)
                    if not t or em not in t:
                        continue
                    score = 0
                    if re.search(r"\bprof|research|lectur|wissenschaft|ingenieur|engineer|group|chair", t, re.I):
                        score += 2
                    if len(t) < 600:
                        score += 1
                    if score > best_score:
                        best_block, best_score = b, score

                if best_block is not None:
                    t = _text(best_block)
                    # crude name extraction: look for TitleCase multiword near email
                    name_m = re.search(r"([A-ZÄÖÜ][a-zäöüß]+(?:[-\s][A-ZÄÖÜ][a-zäöüß]+){1,3})", t)
                    name = name_m.group(1) if name_m else ""
                    # crude title extraction
                    title_m = re.search(r"(Professor|Prof\.|Dr\.|Lecturer|Research(?:er| Associate| Fellow)|Wissenschaft(?:ler|liche)|Ingenieur|Engineer|Head|Leader)[^.,\n]{0,120}", t, re.I)
                    title = title_m.group(0) if title_m else ""
                    contacts.append({
                        "Full_name": name,
                        "Email": em,
                        "Title_role": title,
                        "Field_of_study": _guess_field_from_text(t),
                        "page_text": t[:6000] if t else page_text[:6000],
                        "source_url": page_url,
                    })

    # 4) Final cleanup: de-dup by Email+Name, normalize blanks
    dedup = {}
    for c in contacts:
        # FALLBACK: If name is still missing after HTML extraction, try to extract from email
        # This only happens when the page doesn't contain the name in any detectable format
        if not c.get("Full_name") and c.get("Email"):
            email = c["Email"]
            if "@" in email:
                local_part = email.split("@")[0]
                # Check for firstname.lastname or f.lastname pattern
                if "." in local_part and not local_part.startswith("."):
                    parts = local_part.split(".")
                    # Handle firstname.lastname (2 parts)
                    if len(parts) == 2:
                        first = parts[0].capitalize()
                        last = parts[1].capitalize()
                        c["Full_name"] = f"{first} {last}"
                    # Handle f.lastname (initial + lastname)
                    elif len(parts) == 2 and len(parts[0]) == 1:
                        initial = parts[0].upper()
                        last = parts[1].capitalize()
                        c["Full_name"] = f"{initial}. {last}"
        
        key = (c.get("Email", "").lower(), (c.get("Full_name", "") or "").lower())
        if key in dedup:
            # prefer record that has a non-empty title / field / longer page_text
            old = dedup[key]
            if len(_join_clean([c.get("Title_role", ""), c.get("Field_of_study", "")])) > \
               len(_join_clean([old.get("Title_role", ""), old.get("Field_of_study", "")])):
                dedup[key] = c
            elif len(c.get("page_text", "")) > len(old.get("page_text", "")):
                dedup[key] = c
        else:
            dedup[key] = c

    # Ensure keys exist
    normalized = []
    for c in dedup.values():
        normalized.append({
            "Full_name": c.get("Full_name", "") or "",
            "Email": c.get("Email", "") or "",
            "Title_role": c.get("Title_role", "") or "",
            "Field_of_study": c.get("Field_of_study", "") or "",
            "page_text": c.get("page_text", "") or "",
            "source_url": c.get("source_url", page_url),
        })

    return normalized


# ----------------------------------------
# UNIVERSITY PROCESSING WRAPPER
# ----------------------------------------

async def process_university(session, uni: dict, pbar=None, use_ai=False, client=None, ai_model="gpt-4o-mini") -> List[Dict]:
    """
    Process a single university: crawl staff pages and extract contacts.
    
    Args:
        session: aiohttp ClientSession for HTTP requests
        uni: dict with keys 'country', 'name', 'url'
        pbar: optional progress bar (tqdm)
        use_ai: whether AI is enabled (for link discovery)
        client: OpenAI client (for AI-powered link discovery)
        ai_model: AI model name
    
    Returns:
        List of contact dictionaries with university metadata
    """
    university_name = uni.get("name", "Unknown")
    country = uni.get("country", "Unknown")
    url = uni.get("url", "")
    
    if not url:
        if pbar:
            pbar.update(1)
        return []
    
    try:
        # Create crawler and run
        crawler = StaffCrawler(url)
        contacts = await crawler.crawl()
        
        # Add university metadata to each contact
        for contact in contacts:
            contact["University"] = university_name
            contact["Country"] = country
            contact["University_Website_URL"] = url
        
        if DEBUG and contacts:
            print(f"   ✅ {university_name}: {len(contacts)} contacts from {len(crawler.found_pages)} staff pages")
        
    except Exception as e:
        if DEBUG:
            print(f"   ⚠️ {university_name}: Error during crawl: {e}")
        contacts = []
    
    if pbar:
        pbar.update(1)
    
    return contacts