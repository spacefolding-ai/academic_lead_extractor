# Quick Reference: Language Keywords Organization

## 📁 File Structure

### keywords_multilingual.py (ALL Language Data)
**Location:** `/keywords_multilingual.py`  
**Purpose:** Centralized multilingual keyword repository

```python
KEYWORDS_BY_LANGUAGE = {...}  # ICP detection (32 languages)
COUNTRY_LANGUAGE = {...}      # Country → Language mapping
FIELD_KEYWORDS = {...}        # Field classification (27+ languages)
```

### config.py (Configuration Only)
**Location:** `/config.py`  
**Purpose:** Application configuration and settings

```python
from keywords_multilingual import KEYWORDS_BY_LANGUAGE, COUNTRY_LANGUAGE, FIELD_KEYWORDS

KEYWORDS_INCLUDE = [...]       # English technical keywords
KEYWORDS_EXCLUDE = [...]       # Exclusion terms
UNIVERSAL_TECH_TERMS = [...]   # Language-agnostic acronyms
# ... other configuration ...
```

## 🔍 What's Where?

| What You Need | Where to Find It |
|---------------|------------------|
| Add new language for ICP detection | `keywords_multilingual.py` → `KEYWORDS_BY_LANGUAGE` |
| Add field classification keywords | `keywords_multilingual.py` → `FIELD_KEYWORDS` |
| Map country to language | `keywords_multilingual.py` → `COUNTRY_LANGUAGE` |
| Change script timeouts/limits | `config.py` → Script configuration section |
| Add English ICP keywords | `config.py` → `KEYWORDS_INCLUDE` |
| Add exclusion patterns | `config.py` → `KEYWORDS_EXCLUDE` / `EXCLUDE_URL_PATTERNS` |
| Add universal tech terms | `config.py` → `UNIVERSAL_TECH_TERMS` |

## ✏️ How to Add a New Language

### Example: Adding Japanese

**Step 1: Add ICP Keywords** (`keywords_multilingual.py`)
```python
KEYWORDS_BY_LANGUAGE = {
    # ... existing languages ...
    "Japanese": [
        "電力エレクトロニクス",  # power electronics
        "エネルギーシステム",      # energy systems
        "再生可能エネルギー",      # renewable energy
        # ... more keywords ...
    ]
}
```

**Step 2: Add Field Classification** (`keywords_multilingual.py`)
```python
FIELD_KEYWORDS = {
    "Power Electronics": [
        # ... existing languages ...
        # Japanese
        "電力エレクトロニクス", "インバータ", "整流器",
    ],
    "Energy Systems": [
        # ... existing languages ...
        # Japanese
        "エネルギーシステム", "スマートグリッド", "再生可能エネルギー",
    ],
    # ... other categories ...
}
```

**Step 3: Add Country Mapping** (`keywords_multilingual.py`)
```python
COUNTRY_LANGUAGE = {
    # ... existing countries ...
    "Japan": "Japanese",
}
```

## 📊 Current Coverage

| Category | Count | Location |
|----------|-------|----------|
| Languages Supported | 32 | `keywords_multilingual.py` |
| ICP Keywords | 2802 | `KEYWORDS_BY_LANGUAGE` |
| Field Categories | 7 | `FIELD_KEYWORDS` |
| Field Keywords | 693 | `FIELD_KEYWORDS` |
| Countries Mapped | 41 | `COUNTRY_LANGUAGE` |
| Universal Terms | 50 | `config.py` |

## 🎯 The 7 Field Categories

1. **Power Electronics** - Converters, inverters, rectifiers
2. **Electric Drives & Motors** - Motor control, PMSM, drives
3. **Energy Systems** - Smart grid, renewable energy, HVDC
4. **Battery & Storage** - BMS, lithium-ion, energy storage
5. **E-Mobility & EVs** - Electric vehicles, charging, powertrain
6. **Embedded & Real-Time** - Microcontrollers, HIL, firmware
7. **Control Systems** - MPC, robust control, automation

## ⚙️ Import Patterns

```python
# Recommended: Import from config.py
from config import FIELD_KEYWORDS, KEYWORDS_BY_LANGUAGE, COUNTRY_LANGUAGE

# Alternative: Import directly from keywords_multilingual.py
from keywords_multilingual import FIELD_KEYWORDS

# In scraper.py
from config import FIELD_KEYWORDS  # Works automatically!
```

## 📝 Maintenance Tips

✅ **Do:**
- Edit `keywords_multilingual.py` for any language additions
- Keep keywords lowercase for matching
- Add keywords to both ICP and field classification
- Test new languages with actual university pages

❌ **Don't:**
- Put language keywords in `config.py`
- Mix data and configuration
- Forget to add country mapping
- Add language-specific keywords to `UNIVERSAL_TECH_TERMS`

## 🔗 Related Documentation

- `COMPLETE_LANGUAGE_SUPPORT.md` - Full language support details
- `LANGUAGE_KEYWORDS_REORGANIZATION.md` - This reorganization explained
- `MULTI_LANGUAGE_SUPPORT.md` - How multilingual ICP works

---

**Last Updated:** November 5, 2025  
**Status:** ✅ Active
