# Critical Bug Fix - Async Crawling Issue

## 🐛 The Bug
The crawler was visiting pages but not actually processing them, resulting in **0 contacts extracted**.

## 🔍 Root Cause
In `/academic_lead_extractor/scraper.py`, line 186:

```python
# BUG: Marking URL as visited BEFORE crawling
self.visited.add(full_url)
tasks.append(self._crawl_recursive(full_url, session, depth + 1))
```

When the recursive task ran, it immediately hit this check (line 143):
```python
if url in self.visited:
    return  # Already visited - skip!
```

So URLs were marked as "visited" but never actually processed!

## ✅ The Fix
Added a separate `queued` set to track URLs that are queued for crawling:

```python
# In __init__:
self.queued: Set[str] = set()

# When creating tasks:
if full_url in self.visited or full_url in self.queued:
    continue
self.queued.add(full_url)  # Mark as queued, not visited
tasks.append(self._crawl_recursive(full_url, session, depth + 1))
```

Now URLs are only marked as `visited` when actually processed (line 145), not when queued.

## 📊 Results After Fix

**Before:**
- Visited: 134 pages
- Staff pages found: 0
- Contacts extracted: 0

**After:**
- Visited: 201 pages  
- Staff pages found: 12 ✅
- Contacts extracted: 0 (see below)

## ⚠️  Remaining Issue: 0 Contacts Extracted

The crawler now correctly detects staff pages, but `extract_contacts_from_html()` isn't finding contacts. This is because:

1. **KIT uses directory pages** - Pages like "Spitzenforschende" (top researchers) are directories linking to individual profiles, not pages with direct contact info
2. **HTML structure mismatch** - German universities may use different HTML patterns than the CSS selectors expect
3. **Email obfuscation** - Contacts might be heavily obfuscated or behind JavaScript

## 🎯 Next Steps

To get actual contacts, we need to:

### Option 1: Increase Crawl Depth
These directory pages likely link to individual profile pages that DO have contacts. Increase depth:
```bash
python3 main.py --urls https://www.kit.edu --depth 3
```

### Option 2: Test with UK/US Universities
Try universities with simpler English pages:
```bash
python3 main.py --urls https://www.bristol.ac.uk
```

### Option 3: Improve Contact Extraction
The `extract_contacts_from_html()` function may need adjustments for:
- German HTML structures
- Different email formats
- JavaScript-rendered content

## Files Modified

1. `/Users/miroslavjugovic/Projects/Academic lead extractor/config.py`
   - Added multi-language STAFF_PAGE_KEYWORDS (44 keywords)
   - Set DEBUG = False

2. `/Users/miroslavjugovic/Projects/Academic lead extractor/academic_lead_extractor/scraper.py`
   - Added `self.queued` set
   - Fixed async task management
   - Improved debug output

## ✅ Verification

Run test:
```bash
python3 test_crawler.py
```

Should show:
- ✅ Multiple staff pages detected
- ✅ Staff keyword matches in URLs/titles
- URLs visited and properly processed

The core crawling infrastructure is now **working correctly**! 🎉

