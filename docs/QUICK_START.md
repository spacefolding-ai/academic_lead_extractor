# 🚀 Quick Start Guide - Academic Lead Extractor

## ✅ The Scripts Are Now Fixed and Ready!

Both `run_without_ai.py` and `run_with_ai.py` now work correctly.

---

## 📝 How to Run (Choose One Method)

### **Method 1: Command Line (Easiest)**

```bash
# Navigate to the project directory
cd "/Users/miroslavjugovic/Projects/Academic lead extractor"

# Test with a single university (FREE, takes 2-5 minutes)
python3 run_without_ai.py --urls https://www.kit.edu

# OR run all universities (FREE, takes 2-3 hours)
python3 run_without_ai.py

# OR with AI filtering (requires OpenAI API key, $10-15)
python3 run_with_ai.py --urls https://www.kit.edu
```

### **Method 2: Double-Click Launchers (macOS)**

**Option A: From Finder**

1. Open Finder
2. Navigate to: `/Users/miroslavjugovic/Projects/Academic lead extractor`
3. Double-click: `run_without_ai_launcher.command`
4. Choose from the menu

**Option B: From Terminal**

```bash
# Make sure you include the leading slash!
/Users/miroslavjugovic/Projects/Academic\ lead\ extractor/run_without_ai_launcher.command
```

**Note:** If macOS says "cannot be opened because it is from an unidentified developer":

1. Right-click (or Ctrl+click) the `.command` file
2. Select "Open"
3. Click "Open" in the dialog

---

## 🎯 Recommended First Test

**Test with ONE university first (fast & free):**

```bash
cd "/Users/miroslavjugovic/Projects/Academic lead extractor"
python3 run_without_ai.py --urls https://www.kit.edu
```

**What you'll see:**

```
================================================================================
🚀 ACADEMIC LEAD EXTRACTOR - WITHOUT AI
================================================================================

Configuration:
  ✅ AI Filtering: DISABLED
  ✅ Aggressive exploration: Enabled
  ✅ Multi-language support: Enabled
  ✅ Name extraction: Exact from webpage
  💰 Cost: $0
  📊 Expected contacts: 5,000-15,000
  ⏱️  Estimated time: 2-3 hours
  📋 Custom arguments: --urls https://www.kit.edu

================================================================================

ℹ️  AI Filtering: DISABLED (using keyword matching only)

🎯 Processing 1 custom URL(s)
🔍 URLs: https://www.kit.edu
🔍 Exploration: Aggressive (subdomains + departments)

🔍 Scanning universities: 0%|          | 0/1 [00:00<?, ?it/s]
```

**Then after 2-5 minutes:**

- Check `results/Custom.csv` for results
- You should see 10-50 contacts from KIT

---

## 📊 All Available Commands

### **Without AI (Free)**

```bash
# All universities from universities.csv
python3 run_without_ai.py

# Single university
python3 run_without_ai.py --urls https://www.kit.edu

# Multiple universities
python3 run_without_ai.py --urls https://www.kit.edu https://ethz.ch https://www.tu-berlin.de

# Custom CSV file
python3 run_without_ai.py --csv my_universities.csv
```

### **With AI (Requires OpenAI API Key)**

```bash
# All universities with AI filtering
python3 run_with_ai.py

# Single university with AI
python3 run_with_ai.py --urls https://www.kit.edu

# Custom AI score threshold (0.0-1.0)
python3 run_with_ai.py --urls https://www.kit.edu --ai-score 0.8

# Custom CSV with AI
python3 run_with_ai.py --csv my_list.csv --ai-score 0.7
```

### **Get Help**

```bash
python3 academic_lead_extractor.py --help
```

---

## 🔧 If You Get Errors

### **"No such file or directory"**

Make sure you're in the right directory:

```bash
cd "/Users/miroslavjugovic/Projects/Academic lead extractor"
ls -la run_*.py  # Should show the scripts
```

### **"Module not found"**

Install dependencies:

```bash
pip3 install aiohttp beautifulsoup4 pandas tqdm python-dotenv openai
```

### **"OPENAI_API_KEY not found"** (only for run_with_ai.py)

Create a `.env` file:

```bash
cd "/Users/miroslavjugovic/Projects/Academic lead extractor"
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
echo "USE_AI=true" >> .env
```

---

## 📁 Where Results Are Saved

Results are saved in: `results/`

- **Default mode:** Results split by country (e.g., `Germany.csv`, `France.csv`)
- **Custom URLs:** Results saved in `Custom.csv`

**CSV Format:**

```csv
Full_name;Email;Title_role;AI_Field;AI_Score;AI_Reason;University;Country;...
Prof. Dr. John Smith;smith@kit.edu;Professor;Power Electronics;0.95;...
```

---

## ⏱️ Expected Processing Times

| Mode              | Universities | Time      | Contacts     | Cost   |
| ----------------- | ------------ | --------- | ------------ | ------ |
| **Single URL**    | 1            | 2-5 min   | 10-50        | $0     |
| **5 URLs**        | 5            | 10-20 min | 50-250       | $0     |
| **All (no AI)**   | 434          | 2-3 hours | 5,000-15,000 | $0     |
| **All (with AI)** | 434          | 3-5 hours | 3,000-8,000  | $10-15 |

---

## 💡 Pro Tips

1. **Always test first** - Run with one university before processing all 434
2. **Use Ctrl+C to stop** - You can interrupt anytime (results auto-save)
3. **Check results as you go** - Look in `results/` folder
4. **Run overnight** - Full extraction takes hours, start before bed
5. **Start without AI** - Get maximum coverage first, add AI later if needed

---

## 🎓 Example Workflow

```bash
# 1. Navigate to project
cd "/Users/miroslavjugovic/Projects/Academic lead extractor"

# 2. Test with one university (2-5 minutes)
python3 run_without_ai.py --urls https://www.kit.edu

# 3. Check results
cat ry/Custom.csv | head -5

# 4. If satisfied, run full extraction
python3 run_without_ai.py

# 5. Come back in 2-3 hours
# 6. Check resultsy/ folder for all CSVs
```

---

## ✅ Summary

| What You Want        | Command                                                |
| -------------------- | ------------------------------------------------------ |
| **Quick test**       | `python3 run_without_ai.py --urls https://www.kit.edu` |
| **All universities** | `python3 run_without_ai.py`                            |
| **With AI**          | `python3 run_with_ai.py`                               |
| **Get help**         | `python3 academic_lead_extractor.py --help`            |
| **Double-click**     | Open `run_without_ai_launcher.command` in Finder       |

---

**The scripts are fixed and ready to use!** 🚀

Start with: `python3 run_without_ai.py --urls https://www.kit.edu`
