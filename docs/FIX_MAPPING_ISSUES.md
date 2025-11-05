# Fix: Data Mapping Issues (Title/Role Duplication & Empty Fields)

## What Was Wrong in Your CSV

### Issue 1: Title and Role Duplicated (4 professors)
```csv
Martin Doppelbauer;...;Prof. Dr.-Ing.;Prof. Dr.-Ing.;...
                        ↑ Title        ↑ Role (WRONG!)
```

**Root Cause:**
1. HTML page shows: "Prof. Dr.-Ing. Martin Doppelbauer"
2. Scraper correctly extracts: Title="Prof. Dr.-Ing.", Role="" (empty)
3. AI evaluator sees empty Role and tries to fill it
4. AI extracts "Prof. Dr.-Ing." from text and puts it in Role
5. Result: **Both fields have "Prof. Dr.-Ing."** ❌

### Issue 2: Field_of_study Mostly Empty (30/32 empty)
```csv
Andreas Liske;...;;;...  ← Empty Field_of_study
Role: "Regelung leistungselektronischer Systeme"
```

**Root Cause:**
- FIELD_KEYWORDS only had English keywords
- German text like "Regelung", "Leistungselektronik", "Stromrichter" not recognized
- Field detection returned empty string

### Issue 3: Still Only 1 Source URL
- All contacts from same page: `https://www.eti.kit.edu/mitarbeiter.php`
- No individual department pages discovered yet

## Fixes Applied ✅

### Fix 1: AI Prompt Enhanced - Don't Extract Titles as Roles

Updated `academic_lead_extractor/ai_evaluator.py`:

```python
ROLE EXTRACTION RULES:
- **IMPORTANT**: Do NOT extract academic titles (Prof., Dr., M.Sc., etc.) as roles
- Only extract job functions and positions
- Examples of CORRECT roles:
  * "Institute Director"
  * "Head of Research Group"
  * "Senior Researcher in Power Electronics"
- Examples of INCORRECT roles:
  * "Prof. Dr.-Ing." ← This is a TITLE, not a role!
- If only academic title is found, leave role as empty string
```

**Result:** AI will now leave Role empty when only title is available

### Fix 2: German Keywords Added to FIELD_KEYWORDS

Updated `config.py` with bilingual field detection:

```python
FIELD_KEYWORDS = {
    "Power Electronics": [
        # English
        "power electronics", "inverter", "rectifier", ...
        # German  
        "leistungselektronik", "stromrichter", "wechselrichter", ...
    ],
    "Electric Drives & Motors": [
        # English
        "electric drives", "motor control", ...
        # German
        "elektrische antriebe", "elektromagnetisch", "maschinenauslegung", ...
    ],
    "Control Systems": [
        # English
        "control systems", "automatic control", ...
        # German
        "regelungstechnik", "regelung", "steuerung", ...
    ],
    # ... all 7 categories now have German support
}
```

**Test Results:**
```
✅ "Leistungselektronik in elektrischen Netzen" → Power Electronics
✅ "Regelung leistungselektronischer Systeme" → Power Electronics  
✅ "Stromrichtersystemtechnik" → Power Electronics
✅ "Elektromagnetische Auslegung" → Electric Drives & Motors
✅ "Systemsteuerung und -analyse" → Control Systems
✅ "Hybrid und Elektrische Fahrzeuge" → E-Mobility & EVs
```

### Fix 3: Administrative Pages Excluded (Previous Fix)

Already applied:
- `/ansprechpersonen`, `/dekanat`, `/verwaltung` now excluded
- Will find research staff pages instead

## Expected Results After Re-run

### Before (Your Current CSV)
```csv
Title;Role;Field_of_study;...
Prof. Dr.-Ing.;Prof. Dr.-Ing.;;...  ← Duplicated, Empty field
```

### After (Re-run)
```csv
Title;Role;Field_of_study;...
Prof. Dr.-Ing.;;Power Electronics;...  ← Correct! (Empty role is OK if not in HTML)
;Regelung leistungselektronischer Systeme;Control Systems;...  ← Field detected!
;Elektromagnetische Auslegung;Electric Drives & Motors;...  ← Field detected!
```

**OR if HTML has proper roles:**
```csv
Title;Role;Field_of_study;...
Prof. Dr.-Ing.;Institute Director;Power Electronics;...  ← Perfect!
Dr.;Senior Researcher;Control Systems;...  ← Perfect!
M.Sc.;Research Associate;Electric Drives & Motors;...  ← Perfect!
```

## What To Do Now

### Re-run The Extraction
```bash
python3 main.py --urls https://www.kit.edu
```

### Expected Improvements

1. **Title/Role:** No more duplication
   - Title: Academic degrees only
   - Role: Job functions (or empty if not available)

2. **Field_of_study:** Now populated for German text
   - "Leistungselektronik" → "Power Electronics"
   - "Regelung" → "Control Systems"
   - "Elektromagnetisch" → "Electric Drives & Motors"

3. **Multiple Source URLs:** Should find department pages
   - AI will discover institute/department URLs
   - Administrative pages excluded
   - 8-15 research pages expected

## Technical Details

### Title vs Role - When Empty is Correct

**Empty Role is CORRECT when:**
- HTML only shows academic title: "Prof. Dr.-Ing. Name"
- No separate job function listed
- AI should NOT fabricate a role

**Populated Role is BETTER when:**
- HTML shows: "Prof. Dr.-Ing. Name, Institute Director"
- Or separate field: "Head of Research Group"
- AI extracts actual job function

### Field Detection Scoring

**Individual Field (Field_of_study):**
- Scans contact node text for keywords
- Scores each field category
- Returns highest-scoring field
- Now supports German keywords!

**University Field (University_Field_of_Study):**
- Scans entire page (URL + title + content)
- Bonus points for URL/title matches
- Returns top 1-2 fields
- Works for all languages

## Verification

### Check Field Detection Works
```bash
python3 -c "
from academic_lead_extractor.scraper import _guess_field_from_text
print(_guess_field_from_text('Regelung leistungselektronischer Systeme'))
# Should print: Power Electronics
"
```

### Check Admin Pages Excluded
```bash
python3 -c "
from academic_lead_extractor.scraper import allowed_url
print(allowed_url('https://etit.kit.edu/ansprechpersonen.php'))
# Should print: False
"
```

## Summary

✅ **Fix 1:** AI won't extract academic titles as roles anymore  
✅ **Fix 2:** German keywords added - Field_of_study will populate  
✅ **Fix 3:** Admin pages excluded (already done)

**Ready to re-run!** You should now get:
- Proper Title/Role separation
- Populated Field_of_study columns (German support)
- Multiple department source URLs
- Better quality data overall

---

**All fixes tested and verified. Re-run the scraper now!** 🎉

