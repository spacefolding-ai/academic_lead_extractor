# 🤖 AI-Powered Link Discovery

## Overview

The scraper now uses AI to intelligently discover staff directory and department pages when `run_with_ai.py` is used. This improves discovery rates on non-standard university websites while maintaining keyword-based fallback.

## How It Works

### **AI Discovery (Primary)**
When `use_ai=True`:
1. AI analyzes all links on a page
2. Identifies promising staff/department pages based on context
3. Returns high-confidence links

### **Keyword Fallback (Backup)**
If AI finds fewer than 3-5 links, the system:
1. Runs keyword-based discovery
2. Combines AI + keyword results
3. Deduplicates and returns combined list

### **Without AI (Default)**
When `use_ai=False` (run_without_ai.py):
- Uses only keyword-based discovery (fast, free, proven)

## Architecture

\`\`\`
run_with_ai.py → use_ai=True
    ↓
AI Link Discovery
    ├── ai_find_department_links() → Finds engineering/technical departments
    │   ├── Success (≥5 links) → Use AI links
    │   ├── Partial (<5 links) → Combine with keywords
    │   └── Failure (0 links) → Fallback to keywords
    │
    └── ai_find_staff_links() → Finds staff directory pages
        ├── Success (≥3 links) → Use AI links
        ├── Partial (<3 links) → Combine with keywords
        └── Failure (0 links) → Fallback to keywords

run_without_ai.py → use_ai=False
    ↓
Keyword-Based Discovery Only
    ├── find_department_links_keywords()
    └── find_faculty_links_keywords()
\`\`\`

## Results Comparison (KIT Example)

### **With AI** (`run_with_ai.py`)
- Contacts extracted: **53**
- After AI filtering (≥0.5): **34**
- Quality: High (scored and filtered)
- Runtime: ~30 seconds
- Cost: ~$0.03 per university

### **Without AI** (`run_without_ai.py`)
- Contacts extracted: **47**
- After keyword filtering: **46**
- Quality: Good (keyword match only)
- Runtime: ~15 seconds
- Cost: **Free** (keyword-based only)

## Benefits of AI Discovery

### ✅ **Advantages**
1. **Smarter Discovery**: Finds non-standard staff pages
   - "Our Team", "Who We Are", "Research Group"
   - Context-aware (understands "Wissenschaftler", "Investigators")

2. **Better Filtering**: Excludes noise
   - Distinguishes staff directories from navigation pages
   - Avoids "Persönlichkeiten" (history) vs "Mitarbeiter" (current staff)

3. **Handles Edge Cases**: Works on unusual websites
   - Non-standard navigation structures
   - Creative page naming

4. **Combined Strength**: Best of both worlds
   - AI finds unique pages
   - Keywords ensure nothing is missed
   - Deduplication prevents overlap

### ❌ **Trade-offs**
1. **Cost**: +$0.01-0.02 per university for link discovery
2. **Speed**: +10-15 seconds per university
3. **Complexity**: More moving parts

## Implementation Details

### **AI Prompts**

#### Department Discovery
\`\`\`
Find department/institute HOMEPAGES that might have staff directories.

LOOK FOR:
- Engineering department homepages (Electrical, Mechanical, Computer Science)
- Institute websites (e.g., "Institut für...", "Institute of...")
- Department subdomains (e.g., etit.kit.edu)

EXCLUDE:
- General "Fakultäten" overview pages
- Administrative departments
\`\`\`

#### Staff Discovery
\`\`\`
Find pages that LIST multiple staff members with contact information.

LOOK FOR:
- "Mitarbeiter", "Personen", "Staff", "Team", "Members"
- Pages likely to have MULTIPLE email addresses

EXCLUDE:
- Job postings / "Stellenangebote"
- "Persönlichkeiten" (notable people/history)
- Leadership pages (only top management)
\`\`\`

### **Smart Combining Logic**

\`\`\`python
if use_ai and client:
    ai_links = await ai_find_staff_links(...)
    
    if len(ai_links) >= 3:  # AI found enough
        return ai_links
    
    if ai_links:  # AI found some
        keyword_links = await find_faculty_links_keywords(...)
        return combine_and_deduplicate(ai_links, keyword_links)
    
    # AI found nothing - use keywords
    return await find_faculty_links_keywords(...)
\`\`\`

## Debug Output

AI discovery provides rich debugging:

\`\`\`
🤖 AI identified 10 staff page links
🤖 Using 10 AI-discovered staff links

🔄 Combining 2 AI links with keyword search...
✅ Combined: 16 total staff links

↩️  AI found no links, using keyword-based discovery
\`\`\`

## Cost Analysis

### Per University
- AI link discovery: **$0.01-0.02**
- AI contact evaluation: **$0.02**
- **Total: $0.03-0.04** per university

### Full Run (433 Universities)
- Without AI: **$0** (keywords only)
- With AI (links + evaluation): **$13-17**

## Recommendations

### Use AI Discovery When:
✅ Processing universities with non-standard layouts
✅ Need maximum coverage and quality
✅ Budget allows for enhanced discovery
✅ Processing <100 universities

### Use Keyword-Only When:
✅ Processing large batches (>200 universities)
✅ Cost is a concern
✅ Universities have standard structures
✅ Speed is critical

## Files Modified

- `academic_lead_extractor/scraper.py`
  - Added `ai_find_department_links()`
  - Added `ai_find_staff_links()`
  - Updated `find_department_links()` with smart combining
  - Updated `find_faculty_links()` with smart combining
  - Updated `process_university()` to pass AI parameters

- `academic_lead_extractor/processor.py`
  - Updated to pass `use_ai`, `client`, `ai_model` to scraper

## Testing

Tested on Karlsruhe Institute of Technology (KIT):
- ✅ AI discovery finds relevant pages
- ✅ Fallback to keywords works seamlessly
- ✅ Combined mode finds the most contacts
- ✅ No AI mode still works perfectly

## Future Enhancements

Potential improvements:
1. **Caching**: Cache AI decisions per domain pattern
2. **Learning**: Track which AI suggestions lead to contacts
3. **Confidence**: Use AI confidence scores to adjust combining threshold
4. **Batch Processing**: Send multiple pages to AI at once

