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
    FIELD_KEYWORDS,
    MAX_RETRIES,
    RETRY_DELAY
)

# ----------------------------------------
# GLOBAL SESSION LIMITS
# ----------------------------------------
CONNECTIONS = 5  # max concurrent HTTP requests (reduced to avoid server rejections)
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
2. A staff/team directory or search page listing researchers in these fields
3. A team/people page with contact information for relevant researchers

Return JSON with:
- relevant (boolean): true if this page is ICP-relevant
- confidence (number 0.0-1.0): how confident you are
- reason (string): brief explanation

EXCLUDE:
- Law, medicine, architecture, business, humanities departments
- Chemistry, biology, pure mathematics (unless combined with engineering)
- Job postings, career pages, alumni pages
- Student organizations
- General university overview pages with NO staff listings

INCLUDE (be generous!):
- Faculty of Electrical Engineering (YES!)
- Institute for Power Electronics (YES!)
- Energy Systems Research Group (YES!)
- Mechatronics Department (YES! - includes control systems, sensors, automation)
- Robotics & Automation Institute (YES! - related to embedded systems)
- Team pages listing researchers with contact info (YES!)
- Staff directories and search pages (YES! - these are exactly what we need)
- People/personnel pages for relevant departments (YES!)

**IMPORTANT:** Staff directories, people search pages, and team listing pages are EXACTLY what we need!
If the page appears to list or search for staff/researchers, mark it as relevant (YES!).

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


async def ai_detect_profile_page(url: str, title: str, html_snippet: str, client, ai_model: str) -> bool:
    """
    Use AI to determine if a page is an individual person's profile/bio page.
    
    Args:
        url: The page URL
        title: Page title
        html_snippet: First ~1500 chars of page text for context
        client: OpenAI client
        ai_model: Model name (gpt-4o-mini or gpt-4o)
    
    Returns:
        True if page is an individual profile, False otherwise
    """
    if not client:
        return False  # Fallback: don't assume it's a profile
    
    import json
    import time
    
    # Build a compact prompt
    prompt = f"""You are an expert at identifying individual academic profile pages.

**Page Information:**
URL: {url}
Title: {title}
Content preview: {html_snippet[:1500]}

**Task:**
Determine if this page is an INDIVIDUAL PERSON'S profile/bio page (not a department or list page).

An individual profile page typically contains:
- One person's name prominently displayed
- Personal contact information (email, phone, office)
- Biography or research interests for ONE person
- Publications or projects by ONE person
- Single person's photo
- Academic title/position for ONE person

NOT individual profiles:
- Staff directories listing multiple people
- Department/institute homepages
- Research group pages with multiple members
- Search pages or navigation pages
- Course pages or project pages

Return JSON with:
- is_profile (boolean): true if this is an INDIVIDUAL person's profile page
- confidence (number 0.0-1.0): how confident you are
- person_name (string): the person's name if detected, empty string otherwise
- reason (string): brief explanation

Be strict: only return true if it's clearly ONE person's profile page.

Return ONLY valid JSON."""

    try:
        # Retry logic with exponential backoff
        max_retries = 2  # Fewer retries for profile detection
        retry_delay = 30
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=ai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,  # Lower temperature for more consistent detection
                    response_format={"type": "json_object"}
                )
                break
            except Exception as api_error:
                error_msg = str(api_error)
                is_retryable = any(x in error_msg.lower() for x in ["rate", "limit", "500", "502", "503", "timeout"])
                
                if attempt < max_retries - 1 and is_retryable:
                    wait_time = retry_delay * (attempt + 1)
                    if DEBUG:
                        print(f"   ⚠️  AI profile detection error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    if DEBUG:
                        print(f"   ⚠️  AI profile detection failed: {error_msg}")
                    return False  # Fallback: don't assume it's a profile
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        is_profile = result.get("is_profile", False)
        confidence = result.get("confidence", 0.0)
        person_name = result.get("person_name", "")
        reason = result.get("reason", "")
        
        if DEBUG:
            status = "👤" if is_profile else "📋"
            print(f"      {status} AI Profile Detection: {title[:40]}... → {is_profile} (conf: {confidence:.2f})")
            if person_name:
                print(f"         Person: {person_name}")
            print(f"         Reason: {reason[:80]}")
        
        return is_profile and confidence >= 0.6  # Require 60% confidence for profile detection
        
    except Exception as e:
        if DEBUG:
            print(f"   ⚠️  AI profile detection exception: {e}")
        return False  # Fallback: don't assume it's a profile


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
    
    # Build prompt for AI with emphasis on subdomains and departments
    prompt = f"""You are an expert at finding department pages and staff directories on university websites.

I need to identify which links from this university homepage lead to ICP-relevant departments and their staff pages:

**TARGET DOMAINS (ICP):**
- Power electronics & power systems
- Energy systems, storage & renewable energy
- Electrical engineering & electrical machines
- Mechatronics, robotics & embedded systems (control, automation, sensors)
- Smart grids & battery systems

**Homepage:** {base_url}

**CRITICAL:** Find THREE types of pages:
1. **Direct staff listing pages** - Pages with "Team", "Staff", "People", "Mitarbeiter" containing contact listings
2. **Department/Institute homepages** - Main pages for institutes/departments (we'll automatically explore these for staff links)
3. **Subdomain department sites** - Subdomains like etit.kit.edu, ipe.kit.edu, energy.kit.edu

**PRIORITIZE (in order):**
1. Subdomain URLs for relevant departments (e.g., etit.kit.edu, ipe.kit.edu, iam.kit.edu, eti.kit.edu)
2. Institute/department URLs containing: /institut, /institute, /department, /faculty, /group, /lab, /center
3. Direct staff pages containing: /staff, /team, /people, /mitarbeiter, /personnel

**Available Links (URL → Link Text):**
{chr(10).join([f'{i+1}. {link["url"]} → "{link["text"]}"' for i, link in enumerate(prioritized_links[:80])])}

**INCLUDE these departments/institutes:**
- Electrical Engineering, Elektrotechnik, ETIT
- Power Electronics, Leistungselektronik
- Energy Systems, Energiesysteme
- Control Systems, Regelungstechnik
- Mechatronics, Robotics, Automation
- Smart Grid, Microgrids
- Battery Systems, Electric Vehicles

**EXCLUDE:**
- Law, medicine, business, architecture, humanities
- Pure mathematics, chemistry, biology (unless engineering-focused)
- Student/alumni/career pages
- Generic university admin pages
- Administrative contact pages (Ansprechpersonen, Dekanat, Verwaltung)
- Organizational/management pages (not research staff)

**Task:**
Return a JSON object with "staff_pages" array. Each entry should have:
- url: The full URL to explore
- reason: Brief explanation (mention if it's a department homepage vs direct staff page)

{{
  "staff_pages": [
    {{"url": "https://etit.kit.edu/", "reason": "Electrical Engineering faculty subdomain - will explore for staff"}},
    {{"url": "https://www.eti.kit.edu/", "reason": "Electrotechnical Institute - will explore for team pages"}},
    {{"url": "https://ipe.kit.edu/", "reason": "Power Electronics Institute subdomain"}},
    {{"url": "https://www.kit.edu/iam/", "reason": "Institute for Hybrid and Electric Vehicles"}},
    {{"url": "https://www.kit.edu/staff", "reason": "Direct staff directory page"}}
  ]
}}

Return 5-25 most promising URLs. Prioritize subdomains and institute pages over generic staff directories."""

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
    """Heuristic: detect staff/team/people directories AND individual profile pages."""
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
    
    # Generic detection of individual profile pages
    # These patterns work across different languages and university systems
    import re
    
    # Pattern 1: URL with ID/number + name
    # Examples: /421/john-smith, /staff/123/maria-garcia, /profile/456/mueller
    # Works for: English, German, Spanish, Serbian, etc.
    if re.search(r'/\d+/[\w-]+(?:-[\w-]+)*/?$', url_l, re.IGNORECASE):
        if DEBUG:
            print(f"   ✅ INDIVIDUAL PROFILE PAGE detected (number + name pattern): {url}")
        return True
    
    # Pattern 2: Profile/staff/people with single name
    # Examples: /profile/john-smith, /staff/maria-garcia, /people/hans-mueller, ~/username
    profile_url_keywords = [
        r'/profile/[\w-]+/?$', r'/staff/[\w-]+/?$', r'/people/[\w-]+/?$',
        r'/faculty/[\w-]+/?$', r'/researcher/[\w-]+/?$', r'/professor/[\w-]+/?$',
        r'/~[\w-]+/?$',  # Unix-style home directories
        r'/mitarbeiter/[\w-]+/?$', r'/personen/[\w-]+/?$',  # German
        r'/personnel/[\w-]+/?$', r'/chercheur/[\w-]+/?$',  # French
        r'/personale/[\w-]+/?$', r'/ricercatore/[\w-]+/?$',  # Italian
        r'/investigador/[\w-]+/?$', r'/profesor/[\w-]+/?$',  # Spanish
    ]
    for pattern in profile_url_keywords:
        if re.search(pattern, url_l, re.IGNORECASE):
            if DEBUG:
                print(f"   ✅ INDIVIDUAL PROFILE PAGE detected (profile URL pattern): {url}")
            return True
    
    # Pattern 3: Title starting with capitalized name followed by separator
    # Examples: "John Smith | MIT", "Dr. Maria Garcia - UNAM", "Prof. Hans Mueller, TUM"
    # Character ranges cover: Latin (English, German, French, Spanish, Italian), 
    # Cyrillic (Russian, Serbian, Bulgarian), Greek, and accented characters
    # Uppercase: A-Z, À-Ž, А-Я, Α-Ω (Latin, Latin Extended, Cyrillic, Greek)
    # Lowercase: a-z, à-ž, а-я, α-ω (Latin, Latin Extended, Cyrillic, Greek)
    title_name_patterns = [
        # With academic title prefix
        r'^(?:Prof\.?|Dr\.?|Professor|Doctor|Assoc\.?|Assistant)?\s*[A-ZÀ-ŽА-ЯΑ-Ω][a-zà-žа-яα-ω]+(?:\s+[A-ZÀ-ŽА-ЯΑ-Ω][a-zà-žа-яα-ω]+){1,3}\s*[|\-–—,]',
        # Without academic title
        r'^[A-ZÀ-ŽА-ЯΑ-Ω][a-zà-žа-яα-ω]+(?:\s+[A-ZÀ-ŽА-ЯΑ-Ω][a-zà-žа-яα-ω]+){1,3}\s*[|\-–—]',
    ]
    for pattern in title_name_patterns:
        if re.search(pattern, text, re.UNICODE):
            # Additional validation: title shouldn't be too long (profiles are usually short)
            if len(text) < 200:  # Profile titles are typically under 200 chars
                if DEBUG:
                    print(f"   ✅ INDIVIDUAL PROFILE PAGE detected (name in title): '{text[:80]}'")
                return True
    
    return False


def looks_like_department_page(text: str, url: str) -> bool:
    """
    Detect department/institute/research group homepages that should be explored for staff.
    These pages typically have their own staff/team pages that we need to discover.
    """
    text_l = text.lower()
    url_l = url.lower()
    
    # URL patterns for departments/institutes (multilingual)
    dept_url_patterns = [
        # English
        '/institut', '/institute', '/faculty', '/department', '/school',
        '/group', '/lab', '/laboratory', '/center', '/centre',
        # German
        '/fachgebiet', '/lehrstuhl', '/arbeitsgruppe', '/fachbereich', '/abteilung',
        # French
        '/laboratoire', '/équipe', '/département',
        # Italian  
        '/dipartimento', '/laboratorio',
        # Spanish
        '/departamento', '/grupo',
    ]
    
    # Title keywords (look for "Institute for X", "Department of Y", etc.)
    dept_title_keywords = [
        # English
        'institute for', 'institute of', 'faculty of', 'department of', 'school of',
        'research group', 'research center', 'research centre', 'laboratory',
        # German
        'institut für', 'institut für', 'lehrstuhl für', 'fachgebiet',
        'arbeitsgruppe', 'forschungsgruppe', 'fachbereich',
        # French
        'institut', 'laboratoire', 'département', 'équipe de recherche',
        # Italian
        'istituto', 'dipartimento', 'gruppo di ricerca',
        # Spanish
        'instituto', 'departamento', 'grupo de investigación',
    ]
    
    # Check URL - strong signal
    for pattern in dept_url_patterns:
        if pattern in url_l:
            # Exclude if it's already a staff page within department
            if not any(staff_kw in url_l for staff_kw in ['/staff', '/people', '/team', '/mitarbeiter', '/personnel']):
                if DEBUG:
                    print(f"   🏛️ DEPARTMENT PAGE detected (URL pattern): {url}")
                return True
    
    # Check title - moderate signal
    for keyword in dept_title_keywords:
        if keyword in text_l:
            # Additional validation: should be a homepage-like title
            if len(text) < 150:  # Department titles are usually concise
                if DEBUG:
                    print(f"   🏛️ DEPARTMENT PAGE detected (title keyword): '{text[:80]}'")
                return True
    
    return False


# ----------------------------------------
# ASYNC FETCH WITH RETRY + UA ROTATION
# ----------------------------------------

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch a page with retry + rotating User-Agent and exponential backoff."""
    headers = {"User-Agent": USER_AGENTS[hash(url) % len(USER_AGENTS)]}

    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True) as resp:
                if resp.status == 200 and resp.headers.get("content-type", "").startswith("text/html"):
                    html = await resp.text()
                    # Small delay after successful fetch to be polite to the server
                    await asyncio.sleep(0.3)
                    if DEBUG and attempt > 0:
                        print(f"   ✅ Fetch succeeded on attempt {attempt + 1}/{MAX_RETRIES} for {url[:80]}")
                    return html
                elif resp.status >= 500:
                    # Server error - worth retrying
                    if DEBUG:
                        print(f"   ⚠️  Server error {resp.status} (attempt {attempt + 1}/{MAX_RETRIES}): {url[:80]}")
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAY * (2 ** attempt)  # exponential backoff: 1s, 2s, 4s
                        await asyncio.sleep(delay)
                elif resp.status >= 400:
                    # Client error (404, 403, etc.) - no point retrying
                    if DEBUG:
                        print(f"   ⚠️  Client error {resp.status}, not retrying: {url[:80]}")
                    return ""
        except asyncio.TimeoutError:
            if DEBUG:
                print(f"   ⏱️  Timeout (attempt {attempt + 1}/{MAX_RETRIES}): {url[:80]}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # exponential backoff: 1s, 2s, 4s
                await asyncio.sleep(delay)
        except aiohttp.ClientError as e:
            if DEBUG:
                print(f"   ⚠️  Network error (attempt {attempt + 1}/{MAX_RETRIES}): {url[:80]} - {type(e).__name__}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # exponential backoff: 1s, 2s, 4s
                await asyncio.sleep(delay)
        except Exception as e:
            if DEBUG:
                print(f"   ⚠️  Unexpected error (attempt {attempt + 1}/{MAX_RETRIES}): {url[:80]} - {e}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # exponential backoff: 1s, 2s, 4s
                await asyncio.sleep(delay)

    if DEBUG:
        print(f"   ❌ Failed after {MAX_RETRIES} attempts: {url[:80]}")
    return ""  # failed after all retries


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
    def __init__(self, start_url: str, use_ai: bool = False, client=None, ai_model: str = "gpt-4o-mini", use_ai_profile_detection: bool = False):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.queued: Set[str] = set()  # Track URLs queued for crawling
        self.found_pages: List[str] = []
        self.contacts: List[Dict] = []
        self.use_ai = use_ai
        self.client = client
        self.ai_model = ai_model
        self.use_ai_profile_detection = use_ai_profile_detection  # Control AI profile detection
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

        # Detect potential staff pages, department pages, OR subdomain homepages
        is_staff_page = looks_like_staff_page(title, url)
        is_department_page = looks_like_department_page(title, url)
        
        # If not detected by regex but AI profile detection is enabled, check with AI
        # This is slower but more accurate for edge cases (disabled by default for performance)
        if not is_staff_page and self.use_ai_profile_detection and self.use_ai and self.client:
            page_text_preview = _collect_page_text(tree)[:1500]
            is_staff_page = await ai_detect_profile_page(url, title, page_text_preview, self.client, self.ai_model)
            if is_staff_page and DEBUG:
                print(f"   🤖 AI detected individual profile page (regex missed it)")
        
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
        
        if DEBUG and (is_subdomain_homepage or is_department_page or "mitarbeitende" in url.lower()):
            print(f"   🔍 Checking URL: {url}")
            print(f"      Title: {title[:60]}")
            print(f"      is_staff_page: {is_staff_page}, is_department_page: {is_department_page}, is_subdomain_homepage: {is_subdomain_homepage}")
        
        # Process if it's a staff page
        if is_staff_page:
            # Apply AI filter if enabled (BUT bypass for strong staff directory keywords)
            url_lower = url.lower()
            
            # Strong staff directory keywords that should NEVER be filtered out
            strong_staff_keywords = [
                'personensuche', 'people', 'staff', 'mitarbeiter', 'team',
                'faculty', 'researcher', 'professor', 'wissenschaftler',
                'employees', 'contacts', 'directory'
            ]
            is_strong_staff_page = any(kw in url_lower for kw in strong_staff_keywords)
            
            if self.use_ai and self.client and not is_strong_staff_page:
                # Get page text preview for AI
                page_text_preview = _collect_page_text(tree)[:2000]
                is_icp_relevant = await ai_filter_staff_page(url, title, page_text_preview, self.client, self.ai_model)
                
                if not is_icp_relevant:
                    if DEBUG:
                        print(f"   ❌ AI filtered out: {url} (not ICP-relevant)")
                    self.ai_filtered_count += 1
                    return  # Skip this page - not ICP-relevant
            elif is_strong_staff_page and DEBUG:
                print(f"   🎯 Strong staff keyword detected - bypassing AI filter")
            
            if DEBUG:
                print(f"   ✅ STAFF PAGE FOUND: {url}")
            self.found_pages.append(url)
            extracted = extract_contacts_from_html(html, url)
            self.contacts.extend(extracted)
            if DEBUG:
                print(f"      → Extracted {len(extracted)} contacts")
        elif is_department_page and depth < MAX_CRAWL_DEPTH:
            # Department/institute homepage - continue exploring for staff pages
            if DEBUG:
                print(f"   🏛️  DEPARTMENT PAGE - will explore for staff links: {url}")
            # Don't extract contacts here - wait for actual staff pages within department
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
        
        # Execute tasks in batches to avoid overwhelming the server
        # Even though CONNECTIONS limits concurrent HTTP requests, having too many
        # queued tasks can cause timeouts and memory issues
        if tasks:
            BATCH_SIZE = 5  # Reduced from 10 to 5 - smaller batches are gentler on servers
            for i in range(0, len(tasks), BATCH_SIZE):
                batch = tasks[i:i + BATCH_SIZE]
                await asyncio.gather(*batch, return_exceptions=True)
                # Longer delay between batches to be polite to the server
                # This gives the server time to recover between bursts
                if i + BATCH_SIZE < len(tasks):
                    await asyncio.sleep(2.0)  # Increased from 0.5s to 2s

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
    """
    Collect page text for AI evaluation, including hidden content (tabs, accordions, etc.).
    The selectolax .text() method extracts ALL text from HTML regardless of CSS visibility,
    so this captures content even if it's hidden via display:none, visibility:hidden, etc.
    """
    big_chunks = []
    
    # Priority 1: Main content areas
    for sel in ["main", "article", ".content", "#content", ".main-content"]:
        n = tree.css_first(sel)
        if n:
            t = _text(n)
            if t and len(t) > 300:
                big_chunks.append(t)
    
    # Priority 2: Tab content (often hidden initially but contains important info)
    # Common tab/accordion selectors across different frameworks
    tab_selectors = [
        ".tab-content", ".tabs", "[role='tabpanel']", ".tab-pane",  # Bootstrap, generic tabs
        ".accordion", ".collapse", "[data-toggle='collapse']",  # Accordions
        ".panel-body", ".panel-content",  # Panel layouts
        "[hidden]", ".hidden-content", ".toggle-content",  # Hidden sections
    ]
    for sel in tab_selectors:
        for node in tree.css(sel):
            t = _text(node)
            if t and len(t) > 200:  # Lower threshold for hidden content
                big_chunks.append(t)
    
    # Priority 3: Container and body (if we didn't get enough content)
    if len(" ".join(big_chunks)) < 1000:
        for sel in [".container", "body"]:
            n = tree.css_first(sel)
            if n:
                t = _text(n)
                if t and len(t) > 500:
                    big_chunks.append(t)
    
    # Fallback: Get everything from root
    if not big_chunks:
        big_chunks.append(_text(tree.root)[:10000])
    
    # Remove navigation and footer noise
    full_text = " ".join(big_chunks)
    
    # Filter out common navigation/footer patterns
    noise_patterns = [
        r'Cookie\s+(?:Policy|Notice|Settings)',
        r'Privacy\s+Policy',
        r'Terms\s+(?:of\s+)?(?:Service|Use)',
        r'Copyright\s+©',
        r'All\s+rights\s+reserved',
    ]
    for pattern in noise_patterns:
        full_text = re.sub(pattern, '', full_text, flags=re.IGNORECASE)
    
    # Normalize whitespace and limit length
    return re.sub(r"\s+", " ", full_text).strip()[:15000]  # Increased from 12000 to 15000


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
    Example: "Prof. Dr.-Ing., Researcher" → ("Prof. Dr.-Ing.", "Researcher")
    """
    if not name:
        return ("", name)
    
    # Academic title patterns (order matters - check longer patterns first)
    # Allow titles to be followed by space, comma, or end of string
    title_patterns = [
        r'^(Prof\.\s*Dr\.-Ing\.|Professor\s*Dr\.-Ing\.)(?:\s+|,\s*|$)',
        r'^(Prof\.\s*Dr\.|Professor\s*Dr\.)(?:\s+|,\s*|$)',
        r'^(Dr\.-Ing\.|Dr\.\s*Ing\.)(?:\s+|,\s*|$)',
        r'^(Dr\.\s*rer\.\s*nat\.|Dr\.\s*rer\.nat\.)(?:\s+|,\s*|$)',
        r'^(Dr\.\s*phil\.)(?:\s+|,\s*|$)',
        r'^(M\.Sc\.|M\.S\.|MSc)(?:\s+|,\s*|$)',
        r'^(B\.Sc\.|B\.S\.|BSc)(?:\s+|,\s*|$)',
        r'^(Dipl\.-Ing\.|Diplom-Ingenieur)(?:\s+|,\s*|$)',
        r'^(Prof\.)(?:\s+|,\s*|$)',
        r'^(Dr\.)(?:\s+|,\s*|$)',
        r'^(Professor)(?:\s+|,\s*|$)',
        r'^(PhD)(?:\s+|,\s*|$)',
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Remove the title and the separator (space or comma)
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
    """Detect field of study from text content using keyword matching."""
    txt_l = txt.lower()
    field_scores = {}
    
    # Count keyword matches for each field
    for field, kws in FIELD_KEYWORDS.items():
        score = 0
        for kw in kws:
            if kw in txt_l:
                score += 1
        if score > 0:
            field_scores[field] = score
    
    # Return field with highest score
    if field_scores:
        return max(field_scores.items(), key=lambda x: x[1])[0]
    return ""


def _detect_university_field(url: str, page_title: str, page_text: str) -> str:
    """
    Detect the primary field of study for a university department/institute
    based on URL, title, and page content.
    
    Returns a comma-separated string of detected fields (up to 2 primary fields).
    """
    combined_text = f"{url} {page_title} {page_text[:3000]}".lower()
    field_scores = {}
    
    # Score each field based on keyword frequency
    for field, kws in FIELD_KEYWORDS.items():
        score = 0
        for kw in kws:
            # Count occurrences (up to 5 per keyword to avoid over-weighting)
            count = min(combined_text.count(kw), 5)
            score += count
        
        # Bonus points for field keywords in URL or title (strong signals)
        url_lower = url.lower()
        title_lower = page_title.lower()
        for kw in kws[:5]:  # Check top 5 keywords per field
            if kw in url_lower:
                score += 10
            if kw in title_lower:
                score += 5
        
        if score > 0:
            field_scores[field] = score
    
    # Return top 2 fields if they have significant scores
    if not field_scores:
        return ""
    
    sorted_fields = sorted(field_scores.items(), key=lambda x: x[1], reverse=True)
    
    # If top field has score >= 2, it's confident (lowered threshold for better detection)
    # Higher scores indicate stronger confidence (e.g., keyword in URL/title = +10/+5 points)
    if sorted_fields[0][1] >= 2:
        # Include second field if it has at least 40% of top score
        if len(sorted_fields) > 1 and sorted_fields[1][1] >= sorted_fields[0][1] * 0.4:
            return f"{sorted_fields[0][0]}, {sorted_fields[1][0]}"
        return sorted_fields[0][0]
    
    return ""


def extract_contacts_from_html(html: str, page_url: str) -> List[Dict]:
    tree = HTMLParser(html)
    page_text = _collect_page_text(tree)
    page_title = (tree.css_first("title").text(strip=True) if tree.css_first("title") else "")
    
    # Detect university/department field of study from page content
    university_field = _detect_university_field(page_url, page_title, page_text)

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
                "University_Field_of_Study": university_field,
                "page_text": page_text[:10000],  # Always use full page context for AI
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
                    "University_Field_of_Study": university_field,
                    "page_text": page_text[:10000],  # Always use full page context for AI
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
                        "University_Field_of_Study": university_field,
                        "page_text": page_text[:10000],  # Always use full page context for AI
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
            # prefer record that has a non-empty title / role / field / longer page_text
            old = dedup[key]
            if len(_join_clean([c.get("Title", ""), c.get("Role", ""), c.get("Field_of_study", "")])) > \
               len(_join_clean([old.get("Title", ""), old.get("Role", ""), old.get("Field_of_study", "")])):
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
            "Title": c.get("Title", "") or "",  # Academic title (Prof., Dr., etc.)
            "Role": c.get("Role", "") or "",  # Position/function (Head of..., Researcher in..., etc.)
            "Field_of_study": c.get("Field_of_study", "") or "",  # Individual's field (keyword-based)
            "University_Field_of_Study": c.get("University_Field_of_Study", "") or "",  # Department/institute field
            "page_text": c.get("page_text", "") or "",
            "source_url": c.get("source_url", page_url),
        })

    return normalized


# ----------------------------------------
# UNIVERSITY PROCESSING WRAPPER
# ----------------------------------------

async def process_university(session, uni: dict, pbar=None, use_ai=False, client=None, ai_model="gpt-4o-mini", use_ai_profile_detection=False) -> List[Dict]:
    """
    Process a single university: crawl staff pages and extract contacts.
    
    Args:
        session: aiohttp ClientSession for HTTP requests
        uni: dict with keys 'country', 'name', 'url'
        pbar: optional progress bar (tqdm)
        use_ai: whether AI is enabled (for link discovery)
        client: OpenAI client (for AI-powered link discovery)
        ai_model: AI model name
        use_ai_profile_detection: whether to use AI for individual profile page detection (slower)
    
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
        crawler = StaffCrawler(url, use_ai=use_ai, client=client, ai_model=ai_model, use_ai_profile_detection=use_ai_profile_detection)
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