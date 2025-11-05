# JSON Export Feature

**Date:** November 5, 2025  
**Status:** ✅ Implemented

## Overview

The Academic Lead Extractor now exports results in **both CSV and JSON formats**:
- **CSV**: Human-readable, Excel-compatible format (semicolon-separated)
- **JSON**: Machine-readable, structured format for APIs and programmatic access

## Features

### 📊 Dual Format Export

Every extraction now generates two files per country:
```
results/
├── Germany.csv          # Semicolon-separated CSV
├── Germany.json         # Structured JSON
├── Switzerland.csv
├── Switzerland.json
└── ...
```

### 📄 JSON Structure

The JSON file contains:
- **Metadata**: Country, extraction date, contact count
- **Structured contacts**: All fields properly typed
- **Publications array**: Preserved as list (not comma-separated string)
- **UTF-8 encoding**: Proper support for international characters

### Example JSON Output

```json
{
  "country": "Germany",
  "extraction_date": "2025-11-05 14:30:45",
  "total_contacts": 32,
  "contacts": [
    {
      "Full_name": "Prof. Dr.-Ing. Martin Doppelbauer",
      "Email": "martin.doppelbauer@kit.edu",
      "Title": "Prof. Dr.-Ing.",
      "Role": "Elektromagnetische Auslegung",
      "Field_of_study": "Power Electronics",
      "Country": "Germany",
      "University": "Karlsruhe Institute of Technology (KIT)",
      "University_Website_URL": "https://www.kit.edu/",
      "University_Field_of_Study": "Electrical Engineering, Energy Systems",
      "Source_URL": "https://www.eti.kit.edu/mitarbeiter.php",
      "AI_Field": "Power Electronics & Electrical Machines",
      "AI_Score": 1.0,
      "AI_Reason": "Professor with direct expertise in power electronics...",
      "Publications": [
        "https://doi.org/10.1109/ECCE.2023.10362123",
        "https://doi.org/10.1109/TIE.2022.3198259",
        "https://ieeexplore.ieee.org/document/9837563"
      ]
    },
    {
      "Full_name": "Herbert Hirsch",
      "Email": "herbert.hirsch@kit.edu",
      "Title": "",
      "Role": "Regelung leistungselektronischer Systeme",
      "Field_of_study": "Power Electronics",
      "Country": "Germany",
      "University": "Karlsruhe Institute of Technology (KIT)",
      "University_Website_URL": "https://www.kit.edu/",
      "University_Field_of_Study": "Electrical Engineering",
      "Source_URL": "https://www.eti.kit.edu/1461.php",
      "AI_Field": "Power Electronics Control Systems",
      "AI_Score": 0.95,
      "AI_Reason": "Researcher specializing in control of power electronics...",
      "Publications": []
    }
  ]
}
```

## Key Differences: CSV vs JSON

| Feature | CSV | JSON |
|---------|-----|------|
| **Publications** | Comma-separated string | Array of URLs |
| **Reading** | Excel, spreadsheet apps | Programming languages, APIs |
| **Structure** | Flat, tabular | Nested, typed |
| **Encoding** | UTF-8 (manual config) | UTF-8 (automatic) |
| **Empty values** | Empty string `""` | Empty string `""` or `[]` |
| **Metadata** | Header row only | Full metadata object |
| **Use case** | Manual review, CRM import | API integration, automation |

## Benefits

### 🚀 **API Integration**
```python
import json

# Load extraction results
with open('results/Germany.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access structured data
for contact in data['contacts']:
    print(f"{contact['Full_name']} - {contact['AI_Score']}")
    for pub in contact['Publications']:
        print(f"  📄 {pub}")
```

### 🔗 **Publications as Array**
```json
"Publications": [
  "https://doi.org/10.1109/ECCE.2023.10362123",
  "https://doi.org/10.1109/TIE.2022.3198259"
]
```
Instead of CSV string:
```csv
"https://doi.org/10.1109/ECCE.2023.10362123, https://doi.org/10.1109/TIE.2022.3198259"
```

### 🌍 **International Characters**
```json
{
  "Full_name": "François Müller",
  "Role": "Électronique de puissance",
  "University": "École Polytechnique Fédérale de Zürich"
}
```
Proper UTF-8 encoding ensures special characters are preserved.

### 📈 **Metadata Tracking**
```json
{
  "country": "Germany",
  "extraction_date": "2025-11-05 14:30:45",
  "total_contacts": 32,
  "contacts": [...]
}
```
Know exactly when data was extracted and how many contacts.

## Implementation Details

**File Modified:** `academic_lead_extractor/processor.py`

### Changes Made

1. **Added JSON import** (line 8)
   ```python
   import json
   ```

2. **Keep original contacts for JSON** (line 152)
   ```python
   original_contacts = [c.copy() for c in contacts]
   ```

3. **Smart deduplication for JSON** (lines 172-185)
   - Apply same deduplication logic as CSV
   - Keep highest AI_Score per email
   - Preserve Publications as list
   - Remove internal fields like `page_text`

4. **Save JSON file** (lines 207-215)
   ```python
   json_filename = os.path.join(output_dir, f"{country}.json")
   with open(json_filename, 'w', encoding='utf-8') as f:
       json.dump({
           "country": country,
           "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
           "total_contacts": len(json_contacts),
           "contacts": json_contacts
       }, f, indent=2, ensure_ascii=False)
   ```

5. **Updated output message** (lines 217-218)
   ```python
   print(f"✅ {country}: {len(df)} contacts → {csv_filename}")
   print(f"   📄 JSON: {json_filename}")
   ```

## Usage Examples

### Python Integration
```python
import json
import requests

# Load contacts
with open('results/Germany.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter high-quality leads
high_quality = [
    c for c in data['contacts'] 
    if c['AI_Score'] >= 0.9
]

# Send to CRM API
for contact in high_quality:
    response = requests.post('https://crm.example.com/api/leads', json=contact)
    print(f"Added {contact['Full_name']} to CRM")
```

### JavaScript/Node.js Integration
```javascript
const fs = require('fs');

// Load contacts
const data = JSON.parse(fs.readFileSync('results/Germany.json', 'utf8'));

// Group by university
const byUniversity = {};
for (const contact of data.contacts) {
  const uni = contact.University;
  if (!byUniversity[uni]) byUniversity[uni] = [];
  byUniversity[uni].push(contact);
}

console.log(`Found contacts at ${Object.keys(byUniversity).length} universities`);
```

### PowerShell/Automation
```powershell
# Load JSON
$data = Get-Content -Path "results\Germany.json" | ConvertFrom-Json

# Export high scorers to separate file
$topLeads = $data.contacts | Where-Object { $_.AI_Score -ge 0.9 }
$topLeads | ConvertTo-Json | Out-File "top_leads.json"

Write-Host "Exported $($topLeads.Count) top leads"
```

## Output Example

When you run the extractor, you'll see:

```
✅ Germany: 32 contacts → results/Germany.csv
   📄 JSON: results/Germany.json

🎉 TOTAL: 32 contacts across 1 countries
💾 Results saved to: results/
   📊 Format: CSV (semicolon-separated) + JSON (structured data)
```

## Data Consistency

Both CSV and JSON files contain the **same contacts** after deduplication:
- ✅ Same smart deduplication logic (highest AI_Score per email)
- ✅ Same contact list
- ✅ Same field values

**Only difference:**
- CSV: Publications as comma-separated string
- JSON: Publications as array + metadata wrapper

## File Naming Convention

Files are named by country:
- `Germany.csv` / `Germany.json`
- `Switzerland.csv` / `Switzerland.json`
- `Custom.csv` / `Custom.json` (if country unknown)

## Future Enhancements

Potential improvements for consideration:

1. **Combined JSON file**
   - Single `all_contacts.json` with all countries
   - Easier to load all data at once

2. **Summary JSON**
   - `extraction_summary.json` with statistics
   - Total contacts, AI costs, timing info

3. **Export formats**
   - XML export option
   - YAML export option
   - Excel .xlsx with multiple sheets

4. **Compression**
   - Optional gzip compression for large datasets
   - `Germany.json.gz` for bandwidth-efficient transfers

5. **Incremental updates**
   - Append to existing JSON instead of overwriting
   - Track changes over time

---

**Related Documentation:**
- `ENHANCED_ROLE_EXTRACTION.md` - Role extraction improvements
- `SMART_DEDUPLICATION.md` - Deduplication logic
- `COMPLETE_ENHANCEMENT_SUMMARY.md` - All features overview

