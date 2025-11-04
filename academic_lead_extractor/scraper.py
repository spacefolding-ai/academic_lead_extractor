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
    """Keep only links on same domain or subdomain as start URL."""
    try:
        base_domain = urlparse(base).netloc
        link_domain = urlparse(link).netloc
        
        # Extract root domain (e.g., kit.edu from www.kit.edu or iam.kit.edu)
        base_parts = base_domain.split('.')
        link_parts = link_domain.split('.')
        
        # Get root domain (last 2 parts: domain.tld)
        if len(base_parts) >= 2:
            base_root = '.'.join(base_parts[-2:])
        else:
            base_root = base_domain
            
        if len(link_parts) >= 2:
            link_root = '.'.join(link_parts[-2:])
        else:
            link_root = link_domain
        
        # Allow if same root domain (e.g., both end in kit.edu)
        return base_root == link_root
    except:
        return False


async def ai_filter_staff_page(url: str, title: str, html_snippet: str, client, ai_model: str) -> bool:
    """
    Use AI to determine if a page is a relevant staff/team directory for ICP (power electronics, energy systems).
    
    Args:
        url: The page URL
        title: Page title
        html_snippet: First ~2000 chars of page text for context
        client: OpenAI client
        ai_model: Model name (gpt-4o-mini or gpt-4o)
    
    Returns:
        True if page is ICP-relevant, False otherwise
    """
    if not client:
        return True  # Fallback: allow if AI unavailable
    
    import json
    import time
    
    # Build a compact prompt
    prompt = f"""You are an expert at identifying relevant academic departments and staff directories.

I need to determine if this webpage is relevant to our target domains:
- Power electronics & power systems
- Energy systems, storage & renewable energy
- Smart grids & grid integration
- Electrical engineering & electrical machines
- Mechatronics, robotics & embedded systems (control systems, automation, sensors)
- Battery systems, EVs & e-mobility
- Real-time simulation & hardware-in-the-loop

**Page Information:**
URL: {url}
Title: {title}
Content preview: {html_snippet[:2000]}

**Task:**
Determine if this page is:
1. A department/faculty/institute homepage for one of the target domains
2. A staff/team directory for researchers in these fields

Return JSON with:
- relevant (boolean): true if this page is ICP-relevant
- confidence (number 0.0-1.0): how confident you are
- reason (string): brief explanation

EXCLUDE:
- Law, medicine, architecture, business, humanities departments
- Chemistry, biology, pure mathematics (unless combined with engineering)
- Job postings, career pages, alumni pages
- Navigation/overview pages with just links (no actual staff info)
- Student organizations

INCLUDE:
- Faculty of Electrical Engineering (YES!)
- Institute for Power Electronics (YES!)
- Energy Systems Research Group (YES!)
- Mechatronics Department (YES! - includes control systems, sensors, automation)
- Robotics & Automation Institute (YES! - related to embedded systems)
- Team pages listing researchers with contact info

**Note:** Mechatronics, robotics, and automation are HIGHLY relevant because they involve:
- Embedded systems & real-time control
- Power electronics for motor drives
- Sensor technology & signal processing
- Industrial automation systems

Return ONLY valid JSON."""

    try:
        # Retry logic with exponential backoff
        max_retries = 3
        retry_delay = 30
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=ai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                break
            except Exception as api_error:
                error_msg = str(api_error)
                is_retryable = any(x in error_msg.lower() for x in ["rate", "limit", "500", "502", "503", "timeout"])
                
                if attempt < max_retries - 1 and is_retryable:
                    wait_time = retry_delay * (attempt + 1)
                    if DEBUG:
                        print(f"   ⚠️  AI filter error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    if DEBUG:
                        print(f"   ⚠️  AI filter failed: {error_msg}")
                    return True  # Fallback: allow if AI fails
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        is_relevant = result.get("relevant", False)
        confidence = result.get("confidence", 0.0)
        reason = result.get("reason", "")
        
        if DEBUG:
            status = "✅" if is_relevant else "❌"
            print(f"      {status} AI Filter: {title[:40]}... → {is_relevant} (conf: {confidence:.2f})")
            print(f"         Reason: {reason[:80]}")
        
        return is_relevant and confidence >= 0.5
        
    except Exception as e:
        if DEBUG:
            print(f"   ⚠️  AI filter exception: {e}")
        return True  # Fallback: allow if error


async def ai_find_staff_page_links(html: str, base_url: str, client, ai_model: str) -> list:
    """
    Use AI to discover staff/team page URLs from homepage HTML.
    
    Args:
        html: Homepage HTML content
        base_url: University homepage URL
        client: OpenAI client
        ai_model: Model name (gpt-4o-mini or gpt-4o)
    
    Returns:
        List of staff page URLs
    """
    if not client or not html:
        return []

    import json
    import time
    from selectolax.parser import HTMLParser
    from urllib.parse import urljoin
    
    tree = HTMLParser(html)
    
    # Extract all links from homepage
    links = []
    for a in tree.css("a"):
        href = a.attrs.get("href", "")
        if not href:
            continue
        
        full_url = urljoin(base_url, href)
        link_text = a.text(strip=True)
        
        # Skip obviously bad links
        if not is_same_domain(base_url, full_url):
            continue
        if not allowed_url(full_url):
            continue
        
        links.append({
            "url": full_url,
            "text": link_text,
            "href": href
        })
    
    # Prioritize subdomain links (department websites)
    subdomain_links = [l for l in links if urlparse(l["url"]).netloc != urlparse(base_url).netloc]
    main_domain_links = [l for l in links if urlparse(l["url"]).netloc == urlparse(base_url).netloc]
    
    # Show subdomain links first (more likely to be department pages)
    prioritized_links = subdomain_links[:100] + main_domain_links[:100]
    prioritized_links = prioritized_links[:150]  # Limit total to avoid token overflow
    
    if not prioritized_links:
        return []
    
    # Build prompt for AI with emphasis on subdomains
    prompt = f"""You are an expert at finding staff/team directory pages on university websites.

I need to identify which links from this university homepage lead to staff/team/people directories for ICP-relevant departments:
- Power electronics & power systems
- Energy systems, storage & renewable energy
- Electrical engineering & electrical machines
- Mechatronics, robotics & embedded systems
- Smart grids & battery systems

**Homepage:** {base_url}

**IMPORTANT:** Look especially for:
1. **Subdomain links** (e.g., etit.kit.edu, ipe.kit.edu, energy.kit.edu) - these are often department websites
2. Links containing: "institute", "faculty", "department", "center", "group"
3. Links to pages with staff/team/people listings

**Available Links (URL → Link Text):**
{chr(10).join([f'{i+1}. {link["url"]} → "{link["text"]}"' for i, link in enumerate(prioritized_links[:80])])}

**Task:**
Return a JSON object with a "staff_pages" array containing the URLs that are most likely to lead to or contain:
1. Staff/team directory pages (listing multiple people with contact info)
2. ICP-relevant department homepages (that will have staff links)
3. Research institute pages with team listings

**PRIORITIZE:**
- Subdomain URLs (iam.kit.edu, itep.kit.edu, energy.kit.edu, ipe.kit.edu, etc.)
- Institute/faculty pages (electrical engineering, energy, mechatronics)
- Direct staff directory links

**INCLUDE:**
- "Team", "Staff", "People", "Mitarbeiter", "Personnel", "Employees"
- "Institute", "Faculty", "Department", "Research Group"
- Energy-related institutes/centers
- Electrical engineering departments

**EXCLUDE:**
- Generic navigation pages
- Student pages, alumni directories
- Job postings, career pages
- Administrative support only
- Non-ICP departments (law, medicine, business, architecture, etc.)

Return ONLY valid JSON with format:
{{
  "staff_pages": [
    {{"url": "https://etit.kit.edu/", "reason": "Electrical Engineering faculty subdomain"}},
    {{"url": "https://energy.kit.edu/team", "reason": "Energy Center staff page"}},
    {{"url": "https://ipe.kit.edu/", "reason": "Power Electronics Institute subdomain"}}
  ]
}}

Return 5-20 most promising URLs (prioritize subdomains). If no good candidates found, return empty array."""

    try:
        # Retry logic
        max_retries = 3
        retry_delay = 30
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=ai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                break
            except Exception as api_error:
                error_msg = str(api_error)
                is_retryable = any(x in error_msg.lower() for x in ["rate", "limit", "500", "502", "503", "timeout"])
                
                if attempt < max_retries - 1 and is_retryable:
                    wait_time = retry_delay * (attempt + 1)
                    if DEBUG:
                        print(f"   ⚠️  AI link discovery error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    if DEBUG:
                        print(f"   ⚠️  AI link discovery failed: {error_msg}")
                    return []  # Fallback to keyword-based
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        staff_pages = result.get("staff_pages", [])
        
        # Extract URLs
        ai_urls = []
        for page in staff_pages:
            url = page.get("url", "")
            reason = page.get("reason", "")
            if url:
                ai_urls.append(url)
                if DEBUG:
                    print(f"      🤖 AI found: {url}")
                    print(f"         Reason: {reason}")
        
        if DEBUG and ai_urls:
            print(f"   🤖 AI discovered {len(ai_urls)} staff page link(s)")
        
        return ai_urls
        
    except Exception as e:
        if DEBUG:
            print(f"   ⚠️  AI link discovery exception: {e}")
        return []  # Fallback to keyword-based


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
    
    # Remove common spam-protection phrases
    email = re.sub(r'does-not-exist\.?', '', email, flags=re.IGNORECASE)
    email = re.sub(r'no-spam\.?', '', email, flags=re.IGNORECASE)
    email = re.sub(r'remove-this\.?', '', email, flags=re.IGNORECASE)

    # Apply standard obfuscation pattern replacements
    for pattern, repl in EMAIL_OBFUSCATION_PATTERNS.items():
        email = re.sub(pattern, repl, email, flags=re.IGNORECASE)

    # Special handling for KIT format: "firstname lastname @ domain tld"
    # Convert to "firstname.lastname@domain.tld"
    if "@" in email and email.count(" ") >= 2:
        parts = email.split("@")
        if len(parts) == 2:
            # Clean local part (before @): "firstname lastname" → "firstname.lastname"
            local = parts[0].strip()
            if " " in local and local.count(" ") == 1:
                local = local.replace(" ", ".")
            else:
                local = local.replace(" ", "")
            
            # Clean domain part (after @): "domain tld" → "domain.tld"
            domain = parts[1].strip()
            if " " in domain and domain.count(" ") == 1:
                domain = domain.replace(" ", ".")
            else:
                domain = domain.replace(" ", "")
            
            email = f"{local}@{domain}"
    else:
        # Standard case: just remove spaces
        email = email.replace(" ", "")
    
    # Clean up any remaining issues
    email = email.replace("..", ".")
    email = re.sub(r'^\.+|\.+$', '', email)  # Remove leading/trailing dots
    
    return email if "@" in email and "." in email.split("@")[-1] else ""


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
    def __init__(self, start_url: str, use_ai: bool = False, client=None, ai_model: str = "gpt-4o-mini"):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.queued: Set[str] = set()  # Track URLs queued for crawling
        self.found_pages: List[str] = []
        self.contacts: List[Dict] = []
        self.use_ai = use_ai
        self.client = client
        self.ai_model = ai_model
        self.ai_filtered_count = 0  # Track how many pages were filtered out by AI
        self.ai_discovered_urls: Set[str] = set()  # Track AI-discovered URLs

    async def crawl(self):
        """Main entry: start async crawl with queue."""
        connector = aiohttp.TCPConnector(limit=CONNECTIONS, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            await self._crawl_recursive(self.start_url, session, depth=0)
        
        # Print summary if AI was used
        if DEBUG and self.use_ai:
            ai_found_count = len(self.ai_discovered_urls)
            keyword_found_count = len(self.found_pages) - ai_found_count
            print(f"   📊 Discovery summary:")
            print(f"      🤖 AI discovered: {ai_found_count} staff pages")
            print(f"      📋 Keywords found: {keyword_found_count} additional pages")
            print(f"      ❌ AI filtered: {self.ai_filtered_count} non-ICP pages")
            print(f"      ✅ Total processed: {len(self.found_pages)} staff pages")
        
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

        # SPECIAL: At homepage level (depth=0), use AI to discover staff pages first
        if depth == 0 and self.use_ai and self.client:
            if DEBUG:
                print(f"   🤖 Using AI to discover staff page links...")
            
            ai_discovered_urls = await ai_find_staff_page_links(html, url, self.client, self.ai_model)
            
            if ai_discovered_urls:
                if DEBUG:
                    print(f"   ✅ AI found {len(ai_discovered_urls)} staff page link(s)")
                
                # Queue AI-discovered pages for crawling and track them
                for ai_url in ai_discovered_urls:
                    if ai_url not in self.visited and ai_url not in self.queued:
                        self.queued.add(ai_url)
                        self.ai_discovered_urls.add(ai_url)
            else:
                if DEBUG:
                    print(f"   ⚠️  AI found no staff pages, will use keyword discovery fallback")

        # Detect potential staff pages OR subdomain homepages
        is_staff_page = looks_like_staff_page(title, url)
        
        # Check if this is a subdomain homepage (e.g., iam.kit.edu, itep.kit.edu)
        # Only consider it a subdomain homepage if:
        # 1. It's at a shallow depth (0-2)
        # 2. It's a different subdomain from the start URL
        # 3. It's a shallow path (homepage-like)
        # 4. It's still part of the same root domain (kit.edu)
        url_domain = urlparse(url).netloc
        start_domain = urlparse(self.start_url).netloc
        
        # Extract root domains
        url_root = '.'.join(url_domain.split('.')[-2:]) if '.' in url_domain else url_domain
        start_root = '.'.join(start_domain.split('.')[-2:]) if '.' in start_domain else start_domain
        
        is_subdomain_homepage = (
            depth <= 2 and  # Only treat as homepage at shallow depths
            url_domain != start_domain and  # Different subdomain
            url_root == start_root and  # Same root domain (both kit.edu)
            url.count('/') <= 4 and  # Shallow path
            not any(x in url.lower() for x in ['karriere', 'job', 'student', 'alumni', 'news', 'press'])  # Exclude non-academic pages
        )
        
        if DEBUG and (is_subdomain_homepage or "mitarbeitende" in url.lower()):
            print(f"   🔍 Checking URL: {url}")
            print(f"      Title: {title[:60]}")
            print(f"      is_staff_page: {is_staff_page}, is_subdomain_homepage: {is_subdomain_homepage}")
        
        # Process if it's a staff page
        if is_staff_page:
            # Apply AI filter if enabled
            if self.use_ai and self.client:
                # Get page text preview for AI
                page_text_preview = _collect_page_text(tree)[:2000]
                is_icp_relevant = await ai_filter_staff_page(url, title, page_text_preview, self.client, self.ai_model)
                
                if not is_icp_relevant:
                    if DEBUG:
                        print(f"   ❌ AI filtered out: {url} (not ICP-relevant)")
                    self.ai_filtered_count += 1
                    return  # Skip this page - not ICP-relevant
            
            if DEBUG:
                print(f"   ✅ STAFF PAGE FOUND: {url}")
            self.found_pages.append(url)
            extracted = extract_contacts_from_html(html, url)
            self.contacts.extend(extracted)
            if DEBUG:
                print(f"      → Extracted {len(extracted)} contacts")
        elif is_subdomain_homepage and depth < MAX_CRAWL_DEPTH:
            # Subdomain homepage - continue exploring but don't extract contacts yet
            if DEBUG:
                print(f"   🏠 Subdomain homepage - will explore for staff pages: {url}")

        # Find further links and crawl them
        tasks = []
        
        # At depth 0, first crawl AI-discovered URLs
        if depth == 0 and self.use_ai:
            ai_queued = [u for u in self.queued if u not in self.visited]
            for ai_url in ai_queued:
                if ai_url not in self.visited:
                    tasks.append(self._crawl_recursive(ai_url, session, depth + 1))
            
            if DEBUG and ai_queued:
                print(f"   🤖 Queuing {len(ai_queued)} AI-discovered URLs for crawling")
        
        # Also crawl keyword-discovered links (fallback/supplement)
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
            ai_count = len(self.ai_discovered_urls) if self.use_ai else 0
            keyword_count = len(tasks) - ai_count
            if self.use_ai and ai_count > 0:
                print(f"   📋 Total URLs to crawl: {len(tasks)} (AI: {ai_count}, Keywords: {keyword_count})")
            else:
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
    
    # 2) Check for obfuscated emails in link text (KIT format)
    # Look for patterns like: "firstname lastname ∂ domain tld"
    for a in tree.css("a"):
        link_text = _text(a)
        # Check if contains obfuscation symbols
        if any(symbol in link_text for symbol in ['∂', '[at]', '(at)', ' at ']):
            # Extract just the email portion using regex patterns
            # Pattern: word(s) + obfuscation + word(s)
            email_patterns = [
                r'([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)\s*∂\s*([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)',
                r'([a-zA-Z.]+)\s*\[at\]\s*([a-zA-Z.]+)',
                r'([a-zA-Z.]+)\s*\(at\)\s*([a-zA-Z.]+)',
            ]
            for pattern in email_patterns:
                matches = re.findall(pattern, link_text, flags=re.IGNORECASE)
                for match in matches:
                    obfuscated = f"{match[0]} @ {match[1]}"
                    cleaned = clean_email(obfuscated)
                    if cleaned and '@' in cleaned:
                        found.add(cleaned)
    
    # 3) Check table cells for obfuscated emails (common in staff directories)
    for td in tree.css("td"):
        td_text = _text(td)
        # Check if contains obfuscation symbols - extract just the email portion
        if any(symbol in td_text for symbol in ['∂', '[at]', '(at)', ' at ']):
            # Use regex to extract just the email portion
            email_patterns = [
                r'([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)\s*∂\s*(?:does-not-exist\.)?\s*([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)',
                r'([a-zA-Z.]+)\s*\[at\]\s*([a-zA-Z.]+)',
                r'([a-zA-Z.]+)\s*\(at\)\s*([a-zA-Z.]+)',
            ]
            for pattern in email_patterns:
                matches = re.findall(pattern, td_text, flags=re.IGNORECASE)
                for match in matches:
                    obfuscated = f"{match[0]} @ {match[1]}"
                    cleaned = clean_email(obfuscated)
                    if cleaned and '@' in cleaned:
                        found.add(cleaned)

    # 4) Standard email regex patterns
    body_text = _text(tree.root)
    candidates = re.findall(EMAIL_REGEX, body_text, flags=re.I)
    for cand in candidates:
        cleaned = clean_email(cand)
        if cleaned:
            found.add(cleaned)
    
    # 5) Look for obfuscated patterns in full page text
    # Pattern: word(s) + obfuscation symbol + word(s)
    obfuscated_patterns = [
        r'([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s*∂\s*([a-zA-Z]+(?:\s+[a-zA-Z]+)?)',  # firstname lastname ∂ domain tld
        r'([a-zA-Z.]+)\s*\[at\]\s*([a-zA-Z.]+)',  # name [at] domain
        r'([a-zA-Z.]+)\s*\(at\)\s*([a-zA-Z.]+)',  # name (at) domain
    ]
    
    for pattern in obfuscated_patterns:
        matches = re.findall(pattern, body_text, flags=re.IGNORECASE)
        for match in matches:
            # Reconstruct email-like string and clean it
            obfuscated = f"{match[0]} @ {match[1]}"
            cleaned = clean_email(obfuscated)
            if cleaned and '@' in cleaned:
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
    """Extract title/role from node - looks for position, department, function."""
    # Look for labels like title/position/role
    for sel in TITLE_HINT_CLASSES:
        node = n.css_first(sel)
        if node:
            t = _text(node)
            if t and len(t) >= 3:
                return t
    
    # Check table cells - often contain position/function
    for td in n.css("td"):
        td_text = _text(td)
        # Look for role indicators
        role_indicators = ['professor', 'prof.', 'lecturer', 'researcher', 'head', 'director', 
                          'group lead', 'spokesperson', 'officer', 'contact person', 'leader',
                          'wissenschaftler', 'leiter', 'gruppenleiter', 'abteilungsleiter']
        if any(indicator in td_text.lower() for indicator in role_indicators):
            # Extract meaningful title (not just "Tel." or phone numbers)
            if not any(skip in td_text.lower() for skip in ['tel.', 'telefon', 'phone', 'fax', 'email']):
                if 10 < len(td_text) < 300 and not td_text.startswith('+'):
                    return td_text
    
    # Common small tags under name
    for sel in ["small", ".role", ".position", ".title", ".function", "em", "i", "p"]:
        node = n.css_first(sel)
        if node:
            t = _text(node)
            if t and len(t) >= 3 and len(t) < 200:
                return t
    
    # Check for text following the name in the same row/container
    node_text = _text(n)
    # Look for patterns like "Name, Title at Department"
    if ',' in node_text:
        parts = node_text.split(',', 1)
        if len(parts) > 1:
            potential_title = parts[1].strip()
            if 10 < len(potential_title) < 200:
                # Check if it looks like a title/role
                if any(indicator in potential_title.lower() for indicator in 
                      ['professor', 'prof', 'researcher', 'head', 'director', 'group', 'institute']):
                    return potential_title
    
    return ""


def _extract_academic_title(name: str) -> tuple:
    """
    Extract academic title from name and return (title, clean_name).
    Example: "Prof. Dr. John Smith" → ("Prof. Dr.", "John Smith")
    """
    if not name:
        return ("", name)
    
    # Academic title patterns (order matters - check longer patterns first)
    title_patterns = [
        r'^(Prof\.\s*Dr\.-Ing\.|Professor\s*Dr\.-Ing\.)\s+',
        r'^(Prof\.\s*Dr\.|Professor\s*Dr\.)\s+',
        r'^(Dr\.-Ing\.|Dr\.\s*Ing\.)\s+',
        r'^(Dr\.\s*rer\.\s*nat\.|Dr\.\s*rer\.nat\.)\s+',
        r'^(Dr\.\s*phil\.)\s+',
        r'^(Prof\.)\s+',
        r'^(Dr\.)\s+',
        r'^(Professor)\s+',
        r'^(PhD)\s+',
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            clean_name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
            return (title, clean_name)
    
    return ("", name)


def _split_title_and_role(title_role_str: str) -> tuple:
    """
    Split a title/role string into academic title and role/position.
    Example: "Prof. Dr., Head of Research Group" → ("Prof. Dr.", "Head of Research Group")
    """
    if not title_role_str:
        return ("", "")
    
    # Check if string starts with academic title
    title, remaining = _extract_academic_title(title_role_str)
    
    # Clean up remaining text (role)
    role = remaining.strip()
    if role.startswith(','):
        role = role[1:].strip()
    if role.startswith('-'):
        role = role[1:].strip()
    
    return (title, role)


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
    
    # Also check table rows (KIT and many German universities use tables)
    for tr in tree.css("tr"):
        tr_text = _text(tr)
        # Check if row contains obfuscated email or looks like a person entry
        has_email_indicator = any(symbol in tr_text for symbol in ['∂', '@', '[at]', '(at)'])
        has_name_like = re.search(r'\b[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)+\b', tr_text)
        if has_email_indicator and has_name_like:
            candidate_nodes.append(tr)

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
        
        # Also scan node text for obfuscated emails
        node_text = _text(node)
        
        # Check for obfuscated email patterns first - extract just email portion
        if any(symbol in node_text for symbol in ['∂', '[at]', '(at)', ' at ']):
            email_patterns = [
                r'([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)\s*∂\s*(?:does-not-exist\.)?\s*([a-zA-ZäöüÄÖÜß]+(?:\s+[a-zA-ZäöüÄÖÜß]+)?)',
                r'([a-zA-Z.]+)\s*\[at\]\s*([a-zA-Z.]+)',
                r'([a-zA-Z.]+)\s*\(at\)\s*([a-zA-Z.]+)',
            ]
            for pattern in email_patterns:
                matches = re.findall(pattern, node_text, flags=re.IGNORECASE)
                for match in matches:
                    obfuscated = f"{match[0]} @ {match[1]}"
                    cleaned = clean_email(obfuscated)
                    if cleaned and is_academic_email(cleaned):
                        if not any(e[0] == cleaned for e in emails_with_context):
                            emails_with_context.append((cleaned, ""))
        
        # Also check for standard email patterns
        for m in re.findall(EMAIL_REGEX, node_text, flags=re.I):
            cleaned = clean_email(m)
            if cleaned and is_academic_email(cleaned):  # Filter admin emails
                # Check if we already have this email from mailto links
                if not any(e[0] == cleaned for e in emails_with_context):
                    emails_with_context.append((cleaned, ""))

        # If no emails on card, we might still create a record and fill email later from page-level scan
        if not emails_with_context and (name or title):
            # Split title_role into academic title and role/position
            academic_title, role = _split_title_and_role(title) if title else ("", "")
            # Also extract academic title from name if present
            name_title, clean_name = _extract_academic_title(name) if name else ("", name)
            # Use academic title from name if title_role didn't have one
            if name_title and not academic_title:
                academic_title = name_title
                name = clean_name
            
            contacts.append({
                "Full_name": name or "",
                "Email": "",
                "Title": academic_title,
                "Role": role,
                "Field_of_study": _guess_field_from_text(node_text) or "",
                "page_text": node_text[:6000] if node_text else page_text[:6000],
                "source_url": page_url,
            })
        else:
            for em, local_name in emails_with_context:
                if em in per_node_emails:
                    continue
                per_node_emails.add(em)
                # Priority: 1) Local name from HTML, 2) Extract from email, 3) Node-level name as last resort
                final_name = local_name
                if not final_name:
                    # Try to extract from email (firstname.lastname@ format)
                    if "@" in em:
                        local_part = em.split("@")[0]
                        if "." in local_part and not local_part.startswith("."):
                            parts = local_part.split(".")
                            if len(parts) == 2 and len(parts[0]) > 1:
                                final_name = f"{parts[0].capitalize()} {parts[1].capitalize()}"
                            elif len(parts) == 2 and len(parts[0]) == 1:
                                final_name = f"{parts[0].upper()}. {parts[1].capitalize()}"
                # Only use node-level name if we still don't have anything
                if not final_name:
                    final_name = name
                
                # Split title_role into academic title and role/position
                academic_title, role = _split_title_and_role(title) if title else ("", "")
                # Also extract academic title from name if present
                name_title, clean_name = _extract_academic_title(final_name) if final_name else ("", final_name)
                # Use academic title from name if title_role didn't have one
                if name_title and not academic_title:
                    academic_title = name_title
                    final_name = clean_name

                contacts.append({
                    "Full_name": final_name or "",
                    "Email": em,
                    "Title": academic_title,
                    "Role": role,
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
                    title_str = title_m.group(0) if title_m else ""
                    
                    # Split title and role
                    academic_title, role = _split_title_and_role(title_str) if title_str else ("", "")
                    # Extract academic title from name if present
                    name_title, clean_name = _extract_academic_title(name) if name else ("", name)
                    if name_title and not academic_title:
                        academic_title = name_title
                        name = clean_name
                    
                    contacts.append({
                        "Full_name": name,
                        "Email": em,
                        "Title": academic_title,
                        "Role": role,
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
        # Create crawler with AI parameters and run
        crawler = StaffCrawler(url, use_ai=use_ai, client=client, ai_model=ai_model)
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