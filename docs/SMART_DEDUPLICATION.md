# Smart Email Deduplication

**Date:** November 5, 2025  
**Status:** ✅ Implemented

## Problem

When extracting contacts, the same person often appears on multiple pages with slightly different information:

```
Page 1: "Prof. Dr. Martin Doppelbauer" - Score: 0.9 - Role: "Head of Research Group"
Page 2: "Martin Doppelbauer"          - Score: 0.7 - Role: "Researcher"
Page 3: "M. Doppelbauer"              - Score: 0.6 - Role: ""
```

**Previous behavior:** Kept whichever appeared first (random quality)  
**Result:** 228 raw contacts → 176 passed AI → **32 saved** (144 duplicates removed)

## Solution: Smart Deduplication

### Implementation

**Location:** `academic_lead_extractor/processor.py` (lines 151-163)

```python
# Smart deduplication: Keep contact with highest AI_Score for each email
before_dedup = len(df)
if "AI_Score" in df.columns:
    # Sort by AI_Score descending, then deduplicate (keeps first = highest score)
    df = df.sort_values('AI_Score', ascending=False)
df = df.drop_duplicates(subset=["Email"], keep="first")
after_dedup = len(df)

# Report duplicates removed
if before_dedup > after_dedup:
    print(f"   📧 Removed {before_dedup - after_dedup} duplicate emails (kept highest AI scores)")
```

### How It Works

1. **Sort by AI_Score** (descending): Highest quality contacts come first
2. **Deduplicate by Email**: Keep first occurrence (= highest score)
3. **Report**: Show how many duplicates were removed

### Benefits

| Aspect | Before | After |
|--------|--------|-------|
| **Quality** | Random contact per email | Best contact per email |
| **Transparency** | Silent deduplication | Reports removed count |
| **Data loss** | Loses high-quality duplicates | Keeps highest AI scores |

### Example Output

```
✅ Custom: 32 contacts → results/Custom.csv
   📧 Removed 144 duplicate emails (kept highest AI scores)
```

### Real-World Example

**Input:** 3 variations of the same person

| Full_name | Email | AI_Score | Role |
|-----------|-------|----------|------|
| John Doe | john@kit.edu | 0.7 | Researcher |
| J. Doe | john@kit.edu | **0.9** | **Professor** |
| Prof. John Doe | john@kit.edu | 0.6 | *(empty)* |

**Previous:** Kept "John Doe" (0.7) - first in list  
**Now:** Keeps "J. Doe" (0.9) - highest AI score

## Impact

### Statistics from Real Run

```
228 raw contacts extracted
→ 176 passed AI threshold (≥0.5)
→ 32 unique emails saved
→ 144 duplicates removed (82% duplication rate!)
```

### Why So Many Duplicates?

Same person appears on:
- ✅ Main institute staff page
- ✅ Research group page
- ✅ Department overview
- ✅ Personal profile page
- ✅ Project team pages

Each extraction gets slightly different data quality.

## Deduplication Levels

The system has **two deduplication stages**:

### Stage 1: During Scraping
**Location:** `academic_lead_extractor/scraper.py` (`extract_contacts_from_html`)  
**Key:** `(Email, Full_name)` tuple  
**Purpose:** Merge exact same person from same page

### Stage 2: During Save ← **This is the smart one!**
**Location:** `academic_lead_extractor/processor.py`  
**Key:** `Email` only  
**Purpose:** Keep best record across all pages

## Code Changes

### Modified File
- `academic_lead_extractor/processor.py` (lines 151-163)

### Changes Made
1. ✅ Added `before_dedup` counter
2. ✅ Sort by `AI_Score` descending before dedup
3. ✅ Added `after_dedup` counter
4. ✅ Print report showing duplicates removed

### Testing
Verified with unit test showing correct behavior:
- Keeps highest AI_Score for each email ✅
- Reports duplicate count ✅
- Maintains data quality ✅

## Usage

No changes needed - this improvement is automatic!

When you run the extractor, you'll now see:
```bash
✅ Germany: 45 contacts → results/Germany.csv
   📧 Removed 123 duplicate emails (kept highest AI scores)
```

This tells you:
- How many unique contacts were saved
- How many duplicates were intelligently merged
- That the system kept the best version of each person

## Summary

**Before:** Random quality contact per email  
**After:** Best quality contact per email (highest AI score)  
**Visibility:** Silent → Reports duplicate count  
**Quality:** Improved data quality by keeping best records

---

**Related Documentation:**
- `AI_SCORING_DEBUG_GUIDE.md` - AI scoring implementation
- `COMPLETE_ENHANCEMENT_SUMMARY.md` - All improvements overview

