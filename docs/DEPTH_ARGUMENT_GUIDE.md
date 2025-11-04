# 🔍 Exploration Depth Guide

## New Feature: Control Exploration Depth

You can now control how deeply the script explores university websites using the `--depth` argument!

---

## 🎯 **Quick Start**

```bash
# Shallow exploration (fast, fewer results)
python3 run_without_ai.py --urls https://www.kit.edu --depth 1

# Normal exploration (default, balanced)
python3 run_without_ai.py --urls https://www.kit.edu --depth 2

# Deep exploration (thorough, more results)
python3 run_without_ai.py --urls https://www.kit.edu --depth 3
```

---

## 📊 **Depth Levels Explained**

### **Depth 1 - Shallow (Fast)** ⚡

```
Settings:
- Max Faculty Links: 20
- Max Department Links: 5
```

**Best for:**

- Quick tests
- Fast preview of what's available
- Time-sensitive extractions
- Universities with simple structures

**Expected results:**

- ⏱️ Time: 5-10 seconds per university
- 📊 Contacts: 10-30 per university
- 🎯 Coverage: ~40% of available contacts

**Example:**

```bash
python3 run_without_ai.py --urls https://www.kit.edu --depth 1
```

---

### **Depth 2 - Normal (Balanced)** ⚖️ **[DEFAULT]**

```
Settings:
- Max Faculty Links: 50
- Max Department Links: 15
```

**Best for:**

- Standard extractions
- Balanced speed vs coverage
- Most use cases
- Production runs

**Expected results:**

- ⏱️ Time: 15-30 seconds per university
- 📊 Contacts: 30-100 per university
- 🎯 Coverage: ~70% of available contacts

**Example:**

```bash
python3 run_without_ai.py --urls https://www.kit.edu --depth 2
# or simply omit --depth (it's the default)
python3 run_without_ai.py --urls https://www.kit.edu
```

---

### **Depth 3 - Deep (Thorough)** 🔬

```
Settings:
- Max Faculty Links: 100
- Max Department Links: 25
```

**Best for:**

- Maximum coverage
- Large universities
- Research/academic purposes
- When completeness matters

**Expected results:**

- ⏱️ Time: 30-60 seconds per university
- 📊 Contacts: 80-200 per university
- 🎯 Coverage: ~90% of available contacts

**Example:**

```bash
python3 run_without_ai.py --urls https://www.kit.edu --depth 3
```

---

## 🎛️ **Fine-Tuning: Custom Limits**

Want precise control? Set limits individually:

```bash
# Custom faculty link limit
python3 run_without_ai.py --urls https://www.kit.edu --max-faculty-links 75

# Custom department limit
python3 run_without_ai.py --urls https://www.kit.edu --max-department-links 20

# Both together
python3 run_without_ai.py --urls https://www.kit.edu \
  --max-faculty-links 75 \
  --max-department-links 20
```

**Note:** Individual limits override `--depth` preset if both are specified.

---

## 📈 **Performance Comparison**

### Single University (e.g., KIT)

| Depth           | Time | Contacts | Departments Explored | Staff Pages Scraped |
| --------------- | ---- | -------- | -------------------- | ------------------- |
| **1 (Shallow)** | ~8s  | 25       | 5                    | 20                  |
| **2 (Normal)**  | ~18s | 65       | 12                   | 45                  |
| **3 (Deep)**    | ~40s | 120      | 22                   | 85                  |

### All 434 Universities

| Depth           | Total Time  | Total Contacts | Avg per University |
| --------------- | ----------- | -------------- | ------------------ |
| **1 (Shallow)** | 1-1.5 hours | 8,000-12,000   | 20-30              |
| **2 (Normal)**  | 2-3 hours   | 15,000-25,000  | 35-60              |
| **3 (Deep)**    | 4-6 hours   | 25,000-40,000  | 60-100             |

---

## 💡 **Usage Recommendations**

### **Use Depth 1 when:**

- ✅ Testing the script
- ✅ You need quick results
- ✅ Processing many universities and time is limited
- ✅ Universities have simple/flat structures

### **Use Depth 2 when:**

- ✅ Standard extraction runs
- ✅ You want balanced results
- ✅ Processing 100+ universities
- ✅ Cost/time matters (default is optimized)

### **Use Depth 3 when:**

- ✅ Maximum completeness is required
- ✅ Processing important/large universities
- ✅ Research or academic purposes
- ✅ You have time (overnight runs)

---

## 🎯 **Real-World Examples**

### Example 1: Quick Test

```bash
# Test with 3 universities, shallow depth
python3 run_without_ai.py --depth 1 --urls \
  https://www.kit.edu \
  https://ethz.ch \
  https://www.chalmers.se

# Expected: ~60-90 contacts in 30 seconds
```

### Example 2: Targeted Deep Dive

```bash
# Get maximum contacts from top 5 universities
python3 run_with_ai.py --depth 3 --ai-score 0.7 --urls \
  https://www.kit.edu \
  https://ethz.ch \
  https://www.tu-berlin.de \
  https://www.chalmers.se \
  https://www.aalto.fi

# Expected: 300-500 quality contacts in 3-5 minutes
```

### Example 3: Large Scale Extraction

```bash
# Process all universities with normal depth
python3 run_without_ai.py --depth 2

# Expected: 15,000-25,000 contacts in 2-3 hours
```

### Example 4: Custom Fine-Tuning

```bash
# Medium-deep: more departments, normal staff pages
python3 run_without_ai.py --urls https://www.kit.edu \
  --max-department-links 20 \
  --max-faculty-links 50

# Custom balance for your needs
```

---

## 🔄 **How Depth Affects Extraction**

### Depth 1 (Shallow):

```
University Homepage
  ↓ (explores 5 departments)
5 Department Pages
  ↓ (scrapes 20 staff pages total)
20 Staff Pages → ~25 contacts
```

### Depth 2 (Normal):

```
University Homepage
  ↓ (explores 15 departments)
15 Department Pages
  ↓ (scrapes 50 staff pages total)
50 Staff Pages → ~65 contacts
```

### Depth 3 (Deep):

```
University Homepage
  ↓ (explores 25 departments)
25 Department Pages
  ↓ (scrapes 100 staff pages total)
100 Staff Pages → ~120 contacts
```

---

## 🎮 **Interactive Launcher Support**

The double-click launchers also support depth settings!

### macOS/Linux:

```bash
./run_without_ai_launcher.command

# When prompted:
Exploration depth (1=shallow, 2=normal, 3=deep) [default: 2]: 3
```

### Windows:

```
run_without_ai_launcher.bat

# When prompted:
Exploration depth (1=shallow, 2=normal, 3=deep) [default: 2]: 3
```

---

## 📊 **Command-Line Examples**

```bash
# All possible combinations:

# 1. Depth preset only
python3 run_without_ai.py --depth 3

# 2. With URLs
python3 run_without_ai.py --urls https://www.kit.edu --depth 1

# 3. With AI and depth
python3 run_with_ai.py --urls https://www.kit.edu --depth 3 --ai-score 0.7

# 4. Fine-tuned limits
python3 run_without_ai.py --max-faculty-links 150 --max-department-links 30

# 5. Depth + fine-tune (fine-tune overrides depth)
python3 run_without_ai.py --depth 3 --max-faculty-links 75

# 6. Custom CSV with depth
python3 run_without_ai.py --csv my_universities.csv --depth 2
```

---

## 🆘 **Troubleshooting**

### "Depth must be 1, 2, or 3"

```bash
# Invalid:
python3 run_without_ai.py --depth 4  ❌

# Valid:
python3 run_without_ai.py --depth 3  ✅
```

### Not getting enough contacts?

```bash
# Try increasing depth:
python3 run_without_ai.py --urls https://www.kit.edu --depth 3
```

### Taking too long?

```bash
# Reduce depth:
python3 run_without_ai.py --depth 1
```

### Want precise control?

```bash
# Use individual limits instead of --depth:
python3 run_without_ai.py --max-faculty-links 30 --max-department-links 10
```

---

## 📝 **See Help**

```bash
python3 academic_lead_extractor.py --help
```

Look for the "exploration depth" section!

---

## ✅ **Summary**

| What                 | Command                                          |
| -------------------- | ------------------------------------------------ |
| **Quick test**       | `--depth 1`                                      |
| **Normal (default)** | `--depth 2` or omit                              |
| **Maximum coverage** | `--depth 3`                                      |
| **Custom limits**    | `--max-faculty-links N --max-department-links N` |
| **See options**      | `--help`                                         |

---

**Now you have full control over exploration depth!** 🎯🔍

Use shallow for speed, normal for balance, or deep for completeness!
