# Department Page Discovery Enhancement Plan

## Problem Analysis

### Current Behavior
- All 35 contacts extracted from single URL: `https://www.eti.kit.edu/mitarbeiter.php`
- Missing department-specific pages like:
  - Institute for Power Electronics (Leistungselektronische Systeme)
  - Institute for Hybrid and Electric Vehicles (Hybride und Elektrische Fahrzeuge)
  - Institute for Electric Drives (Elektrische Antriebe)
  - Electromagnetic Design groups
  
### What Should Happen
1. AI link discovery should find department/institute URLs from homepage
2. Crawler should follow links to individual department pages
3. Each department page should be a separate Source_URL with its own contacts
4. University_Field_of_Study should reflect the specific department focus

## Root Causes

### Issue 1: AI Link Discovery Not Finding Department Pages
- AI is supposed to find subdomain links (etit.kit.edu, ipe.kit.edu, etc.)
- May be failing or returning too few results
- Needs debugging to see what AI actually returns

### Issue 2: Department Page Detection Too Narrow
- `looks_like_staff_page()` focuses on staff/people keywords
- Doesn't detect department homepages that lead to staff pages
- Should recognize institute/department patterns:
  - `/institut/`, `/institute/`, `/group/`, `/center/`
  - German: `/institut/`, `/fachgebiet/`, `/lehrstuhl/`

### Issue 3: Not Following Department-to-Staff Links
- Even if we find a department homepage, we need to follow its "Team"/"Mitarbeiter" link
- Current crawler may stop at department homepage level

## Solution

### Phase 1: Enhanced Department Page Detection

Add department page recognition to complement staff page detection:

```python
def looks_like_department_page(text: str, url: str) -> bool:
    """Detect department/institute homepages that should be explored for staff."""
    text_l = text.lower()
    url_l = url.lower()
    
    # URL patterns for departments/institutes
    dept_url_patterns = [
        '/institut/', '/institute/', '/faculty/', '/department/',
        '/group/', '/lab/', '/center/', '/centre/', 
        '/fachgebiet/', '/lehrstuhl/', '/arbeitsgruppe/',  # German
        '/fachbereich/', '/abteilung/'
    ]
    
    # Title patterns
    dept_title_keywords = [
        'institut', 'institute', 'faculty', 'department',
        'group', 'lab', 'laboratory', 'center', 'centre',
        'fachgebiet', 'lehrstuhl', 'arbeitsgruppe',
        'research group', 'forschungsgruppe'
    ]
    
    # Check URL
    for pattern in dept_url_patterns:
        if pattern in url_l:
            return True
    
    # Check title
    for keyword in dept_title_keywords:
        if keyword in text_l:
            return True
    
    return False
```

### Phase 2: Enhanced AI Link Discovery Prompt

Update AI prompt to explicitly request department pages:

```
**IMPORTANT:** Find THREE types of pages:
1. **Direct staff listing pages** (people/staff/team pages with contact info)
2. **Department/Institute homepages** (will need to follow Team/Staff link)
3. **Subdomain department sites** (e.g., ipe.kit.edu, etit.kit.edu)

For each department page, we'll automatically look for its staff/team subpage.
```

### Phase 3: Two-Level Crawl Strategy

When we find a department page:
1. Mark it as "department_page"
2. Look for staff links within that department (Team, Mitarbeiter, People, Staff)
3. Crawl those staff pages with department context
4. Tag all contacts with the department name

### Phase 4: Department Context Extraction

Extract and preserve department name:

```python
def extract_department_name(url: str, page_title: str) -> str:
    """Extract department/institute name from URL or title."""
    # From URL: https://eti.kit.edu/... → "ETI"
    # From title: "Institute for Power Electronics - KIT" → "Institute for Power Electronics"
    
    # Try URL first (more reliable)
    domain_parts = urlparse(url).netloc.split('.')
    if len(domain_parts) > 2:
        subdomain = domain_parts[0]
        if subdomain not in ['www', 'web', 'portal']:
            return subdomain.upper()
    
    # Try title
    # Remove university name, common suffixes
    clean_title = re.sub(r'\s*[-–|]\s*(KIT|University|Universität).*$', '', page_title)
    return clean_title.strip()
```

## Implementation Priority

1. **HIGH**: Add department page detection logic
2. **HIGH**: Update AI prompt to request department pages
3. **MEDIUM**: Implement department name extraction
4. **MEDIUM**: Add department context to contacts
5. **LOW**: Add department-to-staff link following logic

## Expected Results After Fix

Instead of:
```
Source_URL: https://www.eti.kit.edu/mitarbeiter.php (35 contacts)
```

We should see:
```
Source_URL: https://www.eti.kit.edu/iam/mitarbeiter (8 contacts)
   Department: Institute for Hybrid and Electric Vehicles
   
Source_URL: https://www.eti.kit.edu/lem/team (6 contacts)
   Department: Institute for Power Electronics Systems
   
Source_URL: https://ipe.kit.edu/staff (12 contacts)
   Department: Institute for Power Electronics (IPE)
   
Source_URL: https://etit.kit.edu/ema/people (9 contacts)
   Department: Electromagnetic Design Group
```

## Testing Plan

1. Run on KIT URL and check if multiple source URLs are found
2. Verify department names are extracted correctly
3. Confirm University_Field_of_Study reflects department focus
4. Check that contacts are properly attributed to their departments

## Notes

- MAX_DEPARTMENT_LINKS (15) should limit how many department pages we crawl
- Each department page should then have staff pages crawled (limited by MAX_FACULTY_LINKS = 50)
- This ensures we get deep, high-quality ICP-aligned contacts from relevant departments only

