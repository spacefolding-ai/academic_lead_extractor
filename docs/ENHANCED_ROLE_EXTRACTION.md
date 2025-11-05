# Enhanced AI Prompt for Role Extraction

**Date:** November 5, 2025  
**Status:** ✅ Implemented

## Problem

The AI was sometimes:
- Translating German roles to English (❌ "Elektromagnetische Auslegung" → "Electromagnetic Design")
- Extracting organization names as roles (❌ "Robert Bosch GmbH" as a role)
- Modifying or enhancing role descriptions instead of keeping them as-is
- Extracting academic titles as roles (❌ "Prof. Dr.-Ing." as a role)

## Solution

Enhanced the AI prompt in `ai_evaluator.py` to be explicit about:
1. **Extract EXACTLY as written** - No translation, no modification
2. **Keep original language** - German stays German, English stays English
3. **Organization names are NOT roles** - Company names go elsewhere
4. **Titles ≠ Roles** - Academic degrees are titles, not job functions

## Changes Made

**File Modified:** `academic_lead_extractor/ai_evaluator.py` (lines 167-220)

### Key Additions to AI Prompt

#### 1. Critical Instruction
```
**CRITICAL**: Extract role/position EXACTLY as it appears in the text
- DO NOT modify, translate, or enhance
- Copy the exact text from the website without changes
- Keep original language (German, English, etc.) - DO NOT translate
```

#### 2. Clear Examples

**✅ CORRECT extraction:**
- `"Elektromagnetische Auslegung"` (German, as written on page)
- `"Regelung leistungselektronischer Systeme"` (German, exact text)
- `"Head of Research Group, Institute of Applied Materials"` (English, exact text)
- `"Systemsteuerung und -analyse"` (German with hyphen, as written)

**❌ INCORRECT extraction:**
- `"Prof. Dr.-Ing."` ← This is a TITLE, not a role!
- `"Power Electronics"` ← Too generic, not a job function
- `"Electromagnetic Design"` ← DO NOT translate German text
- `"Robert Bosch GmbH"` ← This is an ORGANIZATION name, not a role
- `"Daimler AG"` ← This is an ORGANIZATION name, not a role

#### 3. Organization vs Role Distinction
```
ORGANIZATION vs ROLE:
- If text contains ONLY organization name (Bosch, Daimler, etc.): leave role EMPTY
- Organization names are NOT roles: "Robert Bosch GmbH" is not a role
- Company affiliations go elsewhere, not in role field
```

## Expected Impact

### Before Enhancement

| Contact | Title | Role (Before) | Issue |
|---------|-------|---------------|-------|
| Matthias Brodatzki | - | Elektromagnetische Auslegung | ✅ Correct (already German) |
| Herbert Hirsch | - | Electromagnetic Design | ❌ Translated from German |
| Bhaskar Chatterjee | - | Robert Bosch GmbH | ❌ Organization, not role |

### After Enhancement

| Contact | Title | Role (After) | Fix |
|---------|-------|-------------|-----|
| Matthias Brodatzki | - | Elektromagnetische Auslegung | ✅ Kept as-is |
| Herbert Hirsch | - | Elektromagnetische Auslegung | ✅ No translation |
| Bhaskar Chatterjee | - | *(empty)* | ✅ Organization removed |

## Benefits

1. **Data Authenticity** ✅
   - Roles appear exactly as on the source website
   - Original language preserved (important for international leads)
   - No information loss through translation

2. **Better Data Quality** ✅
   - Organization names correctly excluded from roles
   - Clear separation between titles and roles
   - More accurate job function extraction

3. **Consistency** ✅
   - All roles in same format as they appear on site
   - Multilingual roles properly maintained
   - Predictable extraction behavior

4. **CRM Integration** ✅
   - Real roles can be used for targeting
   - Organization affiliations not mixed with job functions
   - Authentic job titles for outreach

## Testing

To verify the improvement works, run extraction on a German university (like KIT) and check:

### Test Case 1: German Role Preservation
```
Source: "Elektromagnetische Auslegung"
Expected: "Elektromagnetische Auslegung" (no translation)
```

### Test Case 2: Organization Name Filtering
```
Source: Person works at "Robert Bosch GmbH"
Expected: Role = "" (empty, organization goes elsewhere)
```

### Test Case 3: Title vs Role
```
Source: "Prof. Dr.-Ing. Martin Doppelbauer"
Expected: Title = "Prof. Dr.-Ing.", Role = "" or actual job function
```

## Technical Details

### Prompt Structure
The enhanced prompt now has 3 key sections:

1. **ROLE EXTRACTION RULES** (9 bullet points)
   - Clear "DO" and "DON'T" instructions
   - Language preservation requirements
   - Organization name handling

2. **Examples of CORRECT extraction** (6 examples)
   - German examples with exact text
   - English examples with exact text
   - Mixed examples with group/institute names

3. **Examples of INCORRECT extraction** (6 examples)
   - Academic titles as roles
   - Translated German text
   - Organization names
   - Too generic terms

4. **ORGANIZATION vs ROLE** (3 rules)
   - Explicit organization name filtering
   - Clear instruction to leave role empty
   - Company affiliation handling

### Model Behavior
The AI (gpt-4o-mini or gpt-4o) now:
- Looks for exact role text in page content
- Preserves original language
- Filters out organization-only text
- Distinguishes titles from roles

## Future Improvements

Potential enhancements for consideration:

1. **Add more language examples**
   - French: "Responsable de recherche"
   - Italian: "Ricercatore"
   - Spanish: "Investigador"

2. **Add validation layer**
   - Detect if role was incorrectly translated
   - Flag suspicious organization names in role field
   - Warn if role looks like a title

3. **Organization field**
   - Extract organization to separate field
   - Useful for partner/external researcher tracking

4. **Role normalization (optional)**
   - Create normalized English version in separate field
   - Keep original + provide translation
   - Best of both worlds for CRM integration

## Usage

No changes needed from users! This improvement is automatic and will apply to all future extractions.

When you run the extractor, roles will now be extracted exactly as they appear on the website, preserving:
- ✅ Original language
- ✅ Exact phrasing
- ✅ Department/group names as written
- ✅ Authentic job functions

---

**Related Documentation:**
- `SMART_DEDUPLICATION.md` - Smart email deduplication
- `AI_SCORING_DEBUG_GUIDE.md` - AI scoring implementation
- `COMPLETE_ENHANCEMENT_SUMMARY.md` - All improvements overview

