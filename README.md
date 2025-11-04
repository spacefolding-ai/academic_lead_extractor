# 🎓 Academic Lead Extractor

Automated extraction of academic contacts from 434+ universities across 44 countries, with AI-powered relevance scoring and publication enrichment.

---

## 🚀 Quick Start

### **NEW: Double-Click Launchers!** 🎉

**Easiest way:** Just double-click the launcher files!

- 🪟 **Windows:** `run_without_ai_launcher.bat` or `run_with_ai_launcher.bat`
- 🍎 **macOS:** `run_without_ai_launcher.command` or `run_with_ai_launcher.command`

Interactive menu guides you through all options - no command line needed! See `LAUNCHER_GUIDE.md` for details.

---

### **Option 1: Maximum Coverage (FREE)** ⭐ Recommended

```bash
# Process all universities from universities.csv
python3 run_without_ai.py

# Process a single university
python3 run_without_ai.py --urls https://www.kit.edu

# Process multiple universities
python3 run_without_ai.py --urls https://www.kit.edu https://www.eth.ch

# Use a custom CSV file
python3 run_without_ai.py --csv my_universities.csv
```

- ✅ 5,000-15,000 contacts
- ✅ Exact name extraction with titles
- ✅ **NEW:** Multi-language keyword matching (32 languages)
- ✅ Shows matched keywords per contact
- ✅ Publication enrichment
- 💰 **Cost: $0**
- ⏱️ **Time: 2-3 hours**

### **Option 2: AI Quality Filter**

```bash
# Process all universities from universities.csv
python3 run_with_ai.py

# Process a single university with AI filtering
python3 run_with_ai.py --urls https://www.kit.edu

# Process multiple universities with custom AI threshold
python3 run_with_ai.py --urls https://www.kit.edu https://www.eth.ch --ai-score 0.7

# Deep exploration for maximum contacts
python3 run_without_ai.py --urls https://www.kit.edu --depth 3
```

- ✅ 3,000-8,000 high-quality contacts
- ✅ AI relevance scoring (0.0-1.0)
- ✅ AI field classification
- ✅ AI naturally understands all 32 languages
- ✅ Everything from Option 1
- 💰 **Cost: Dynamic based on count** (see below)
- ⏱️ **Time: 3-5 hours**

### **Option 3: Direct Script (Advanced)**

```bash
# Full control over all options
python3 academic_lead_extractor.py --help
python3 academic_lead_extractor.py --urls URL1 URL2 --no-ai
python3 academic_lead_extractor.py --csv my_list.csv --ai-score 0.6
```

---

## 📊 What You Get

Results saved to `results/[Country].csv`:

```csv
Full_name,Email,Title_role,Field_of_study,University,Country,Publications
Prof. Dr.-Ing. Thomas Müller,mueller@kit.edu,Professor of Power Electronics,Power Electronics,KIT,Germany,"['https://doi.org/10.1109/...']"
```

### CSV Columns:

- **Full_name** - Exact from webpage (with titles: Prof., Dr., PhD, etc.)
- **Email** - Contact email address
- **Title_role** - Academic position/role
- **Field_of_study** - Technical domain
- **University** - University name
- **Country** - Country
- **University_Website_URL** - Main university website
- **Source_URL** - Page where contact was found
- **Publications** - Publication DOI URLs (from Crossref API)
- **AI_Score** _(with AI only)_ - Relevance confidence (0.0-1.0)
- **AI_Field** _(with AI only)_ - AI-classified domain
- **AI_Reason** _(with AI only)_ - Match reasoning

---

## ✨ Key Features

### 🔍 **Aggressive 3-Level Exploration**

1. Main university page → staff links
2. Department/institute discovery → subdomain exploration
3. Each department → staff pages

**Result:** Finds 3-5x more contacts than basic scrapers

**NEW:** Control exploration depth with `--depth` argument:

- `--depth 1` (shallow): Fast, ~20-30 contacts per university
- `--depth 2` (normal): Balanced, ~35-60 contacts per university _(default)_
- `--depth 3` (deep): Thorough, ~60-100 contacts per university

### 🌍 **Multi-Language Support**

- **32 languages supported** (German, Italian, French, Spanish, Serbian, Polish, etc.)
- **NEW:** Automatic language detection in non-AI mode
- **AI mode:** Naturally understands all languages
- **Non-AI mode:** Now uses translated keywords per country
- Works across all European universities

**Example:** German pages now match "leistungselektronik" (power electronics) automatically!

**Supported:** German, French, Italian, Spanish, Dutch, Polish, Czech, Swedish, Danish, Norwegian, Finnish, Portuguese, Greek, Hungarian, Romanian, Bulgarian, Croatian, Slovak, Slovenian, Lithuanian, Latvian, Estonian, Turkish, Arabic, Hebrew, Chinese, Japanese, Korean, Russian, Ukrainian, Serbian, Albanian

### 🎯 **Exact Name Extraction**

- Preserves all titles: `Prof. Dr.-Ing.`, `Univ.-Prof.`, `Dr. rer. nat.`
- Special characters maintained: ö, ü, é, ñ, etc.
- No modifications to original text
- Names extracted exactly as written on webpage

### 📚 **Publication Enrichment**

- Automatic Crossref API integration
- Up to 5 publications per contact
- DOI URLs for each publication
- Free (no API key required)
- 30-40% success rate (higher for professors)

### 🤖 **AI Quality Filtering (Optional)**

- OpenAI GPT-4o-mini
- Relevance scoring (0.0-1.0)
- Field classification
- Reasoning for each match
- Configurable threshold

---

## 🎯 Understanding AI Score Threshold

The AI Score threshold (0.0-1.0) is a **confidence filter** that determines which contacts make it into your final results.

### How It Works

**Lower threshold = More contacts, varied quality**  
**Higher threshold = Fewer contacts, higher quality only**

```
Threshold 0.9 → Only 0.9-1.0 scores (Best 10%)      [Most Exclusive]
Threshold 0.7 → Includes 0.7-1.0 scores (Top 30%)
Threshold 0.5 → Includes 0.5-1.0 scores (Top 60%)   [Default]
Threshold 0.3 → Includes 0.3-1.0 scores (Top 90%)   [Most Inclusive]
```

**Important:** Lower thresholds **include everything from higher thresholds** PLUS more contacts.

### Score Ranges

| Score       | Quality      | Example                                                |
| ----------- | ------------ | ------------------------------------------------------ |
| **0.9-1.0** | 🏆 Excellent | Professor of Power Electronics, extensive publications |
| **0.7-0.9** | ⭐ Strong    | PhD researcher in renewable energy, clear expertise    |
| **0.5-0.7** | ✅ Good      | Lecturer in electrical engineering, relevant work      |
| **0.3-0.5** | 🔵 Marginal  | Junior researcher, tangentially related                |
| **0.0-0.3** | ⚠️ Poor      | Administrative staff, unrelated field                  |

### Recommended Thresholds

| Threshold | Best For              | Expected Results       |
| --------- | --------------------- | ---------------------- |
| **0.9**   | Premium leads only    | ~1,000-2,000 contacts  |
| **0.7**   | Quality over quantity | ~2,000-5,000 contacts  |
| **0.5**   | Balanced (default)    | ~3,000-8,000 contacts  |
| **0.3**   | Maximum coverage      | ~5,000-12,000 contacts |

### Pro Tip 💡

**Run once at 0.3, filter later!** Since AI evaluation costs the same regardless of threshold:

```bash
# One run with low threshold
python3 run_with_ai.py --ai-score 0.3

# CSV includes AI_Score column - filter in Excel:
# Score >= 0.9 → Premium list
# Score >= 0.7 → Quality list
# Score >= 0.5 → Standard list
```

**One extraction, multiple quality tiers!**

---

## 📁 Project Structure

```
Academic lead extractor/
├── run_without_ai_launcher.bat         🪟 Double-click launcher (Windows, no AI)
├── run_with_ai_launcher.bat            🪟 Double-click launcher (Windows, with AI)
├── run_without_ai_launcher.command     🍎 Double-click launcher (macOS, no AI)
├── run_with_ai_launcher.command        🍎 Double-click launcher (macOS, with AI)
├── run_without_ai.py                   ⭐ Command-line script (no AI)
├── run_with_ai.py                      🤖 Command-line script (with AI)
├── academic_lead_extractor.py          Main script
├── config.py                           Configuration file
├── universities.csv                    Input: 434 universities
├── .env                                API keys (for AI mode)
├── LAUNCHER_GUIDE.md                   📖 How to use launchers
└── results/                 Output directory
    ├── Germany.csv
    ├── France.csv
    └── ...
```

---

## 🛠️ Installation

### Prerequisites

```bash
pip3 install aiohttp beautifulsoup4 pandas tqdm python-dotenv openai
```

### Setup (for AI mode only)

1. Get OpenAI API key: https://platform.openai.com/api-keys
2. Create `.env` file:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
USE_AI=true
AI_MIN_SCORE=0.5
```

---

## 📖 Configuration & Command-Line Options

### Command-Line Arguments

All scripts support flexible command-line arguments:

```bash
# Show all available options
python3 academic_lead_extractor.py --help

# Process specific URLs
--urls URL1 URL2 URL3          # One or more university URLs

# Use custom CSV file
--csv my_list.csv              # Path to CSV (must have University, Website columns)

# AI options
--no-ai                        # Disable AI filtering
--ai-score 0.7                 # Set custom AI threshold (0.0-1.0)

# Exploration depth options (NEW!)
--depth 1                      # Shallow (fast, fewer results)
--depth 2                      # Normal (balanced - default)
--depth 3                      # Deep (thorough, more results)
--max-faculty-links 100        # Custom faculty pages limit
--max-department-links 25      # Custom department limit
```

### 🔍 Exploration Depth Explained

Control how deeply the script explores each university:

| Depth           | Speed       | Contacts per Uni | Departments | Staff Pages | Best For                |
| --------------- | ----------- | ---------------- | ----------- | ----------- | ----------------------- |
| **1 (Shallow)** | ⚡ Fast     | 20-30            | 5           | 20          | Quick tests, previews   |
| **2 (Normal)**  | ⚖️ Balanced | 35-60            | 15          | 50          | Standard runs (default) |
| **3 (Deep)**    | 🔬 Thorough | 60-100           | 25          | 100         | Maximum coverage        |

**Examples:**

```bash
# Fast test
python3 run_without_ai.py --urls https://www.kit.edu --depth 1

# Maximum contacts
python3 run_without_ai.py --urls https://www.kit.edu --depth 3

# Fine-tune manually
python3 run_without_ai.py --max-faculty-links 75 --max-department-links 20
```

See `DEPTH_ARGUMENT_GUIDE.md` for detailed documentation.

### Configuration Files

The script behavior is controlled through:

- `config.py` - Keyword configuration, language mappings, script parameters
- `.env` - API keys and AI settings (when using AI mode)
- `universities.csv` - Default list of universities (can be overridden with `--csv`)

---

## 🎯 Which Script to Use?

### **Choose Your Mode** ⭐

| Script                       | Status             | Use Case                  |
| ---------------------------- | ------------------ | ------------------------- |
| `run_without_ai.py`          | ⭐ **RECOMMENDED** | Free, maximum coverage    |
| `run_with_ai.py`             | ✅ **Recommended** | Quality scoring (~$10-15) |
| `academic_lead_extractor.py` | ✅ Direct Run      | Can be run directly       |

**Features:**

- ✅ Aggressive 3-level exploration (finds MORE contacts)
- ✅ Optional AI filtering (filters BETTER)
- ✅ Flexible (AI on/off via environment variable)
- ✅ Best value per contact

---

## 📈 Expected Results

### For 434 Universities Across 44 Countries:

| Mode           | Depth       | Contacts      | Quality   | Cost   | Time   |
| -------------- | ----------- | ------------- | --------- | ------ | ------ |
| **Without AI** | Shallow (1) | 8,000-12,000  | Good      | $0     | 1-1.5h |
| **Without AI** | Normal (2)  | 15,000-25,000 | Good      | $0     | 2-3h   |
| **Without AI** | Deep (3)    | 25,000-40,000 | Good      | $0     | 4-6h   |
| **With AI**    | Normal (2)  | 3,000-8,000   | Excellent | $10-15 | 3-5h   |
| **With AI**    | Deep (3)    | 5,000-12,000  | Excellent | $15-25 | 5-8h   |

---

## 💡 Usage Tips

### First Time?

1. Start with `run_without_ai.py` (free)
2. Review results
3. Optionally run with AI for quality scoring

### Testing with a Single University?

```bash
# Quick test - shallow depth (fast, free)
python3 run_without_ai.py --urls https://www.kit.edu --depth 1

# Normal test (default depth)
python3 run_without_ai.py --urls https://www.kit.edu

# Deep test - maximum contacts
python3 run_without_ai.py --urls https://www.kit.edu --depth 3

# Test with AI (quality filtering)
python3 run_with_ai.py --urls https://www.kit.edu
```

### On a Budget?

- Use `run_without_ai.py` - still excellent results!

### Need Quality Over Quantity?

- Use `run_with_ai.py` - AI filters out irrelevant contacts
- Adjust threshold: `--ai-score 0.7` for stricter filtering
- See "Understanding AI Score Threshold" section above for details

### Custom University List?

```bash
# Create your own CSV with columns: University, Website, Country (optional)
python3 run_without_ai.py --csv my_universities.csv
```

### Want More Contacts?

```bash
# Increase exploration depth
python3 run_without_ai.py --depth 3

# Or fine-tune limits
python3 run_without_ai.py --max-faculty-links 100 --max-department-links 25
```

### Stopped Mid-Run?

- Just run again - it will continue (results auto-save)

---

## 🔧 Troubleshooting

### "OPENAI_API_KEY not found"

```bash
# Edit .env file
OPENAI_API_KEY=sk-your-actual-key
```

### "Module not found"

```bash
pip3 install aiohttp beautifulsoup4 pandas tqdm python-dotenv openai
```

### Too slow?

- Normal - some universities take time to respond
- Progress bar shows status
- Auto-saves every 10 universities

### No contacts from some universities?

- Expected - some sites use heavy JavaScript
- Some have restricted access
- Some hide contact information
- Overall success rate: 60-80% of universities

---

## 📊 Example Output

### From KIT (Karlsruhe Institute of Technology):

```csv
Full_name: Prof. Dr.-Ing. Thomas Leibfried
Email: leibfried@ieh.kit.edu
Title_role: Professor of Electrical Energy Systems
Field_of_study: Power Electronics, Energy Systems
University: KIT
Country: Germany
University_Website_URL: https://www.kit.edu/
Source_URL: https://www.ieh.kit.edu/staff.php
Publications: ['https://doi.org/10.1109/TPEL.2023.12345', ...]
AI_Score: 0.92
AI_Field: Power Electronics
AI_Reason: Professor specializing in power electronics with extensive publications
```

---

## 🎯 Target Audience

Perfect for:

- ✅ B2B lead generation
- ✅ Academic outreach
- ✅ Research collaboration
- ✅ Conference invitations
- ✅ Product marketing to universities
- ✅ Recruitment

Ideal for companies/orgs targeting:

- Power electronics researchers
- Energy systems academics
- Smart grid specialists
- Renewable energy experts
- Electrical engineering departments

---

## ⚖️ Legal & Ethical Use

**Intended Use:**

- ✅ Professional outreach
- ✅ Academic collaboration
- ✅ Research purposes
- ✅ Public information only

**Please:**

- ✅ Respect robots.txt (script does this automatically)
- ✅ Use for legitimate business purposes
- ✅ Follow GDPR/data protection laws
- ✅ Include opt-out in communications
- ❌ Don't spam or abuse contacts
- ❌ Don't violate university terms of service

---

## 📞 Configuration Files

Key files:

- `config.py` - Customize keywords, languages, and scraping parameters
- `.env` - Set API keys and AI options
- `universities.csv` - Input list of universities

---

## 📝 License

This project is for educational and professional use. Please use responsibly and ethically.

---

## 🚀 Ready to Start?

### **Easiest Way: Double-Click Launchers** 🎉

**Windows:** Double-click `run_without_ai_launcher.bat`  
**macOS:** Double-click `run_without_ai_launcher.command`

Interactive menu guides you through everything!

### **Command Line (Still Works!):**

```bash
# Recommended: Start with free version (all universities)
python3 run_without_ai.py

# OR test with a single university first
python3 run_without_ai.py --urls https://www.kit.edu

# OR with AI quality filter
python3 run_with_ai.py

# OR process your own university list
python3 run_without_ai.py --csv my_universities.csv

# See all options
python3 academic_lead_extractor.py --help
```

### More Documentation

- **`docs/DEPTH_ARGUMENT_GUIDE.md`** - Complete guide to exploration depth control
- **`docs/MULTI_LANGUAGE_SUPPORT.md`** - Multi-language keyword matching guide (NEW!)
- **`docs/DYNAMIC_COST_ESTIMATES.md`** - Accurate cost calculations
- **`docs/QUICK_START.md`** - Quick start guide with examples
- **`docs/AUTO_CLOSE_TERMINAL.md`** - Terminal auto-close feature

**Happy extracting!** 🎓✨
