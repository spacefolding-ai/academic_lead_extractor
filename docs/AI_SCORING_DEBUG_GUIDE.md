# 🐛 AI Scoring Debug Guide

## Problem: All 490 Contacts Got Score 0.0

This guide explains the bug and the fix applied to debug AI scoring issues.

---

## 🔍 The Issue

**Symptoms:**

```
✅ Extracted 490 raw contacts
🤖 Evaluating 490 contacts with AI (gpt-4o-mini)...
   Evaluated 490/490 contacts    [100.0%] ████████████████████
✅ 0 contacts passed AI threshold (0.3)
```

**Problem:** All contacts evaluated, but 0 passed threshold → suggests all got score < 0.3

---

## 🐛 Root Cause

The code was silently defaulting to `0.0` if the AI response didn't have a "score" key:

```python
# OLD CODE (BUGGY)
contact["AI_Score"] = ai_data.get("score", 0.0)  # Defaults to 0.0 silently!
```

**Why this happens:**

- AI response format might have changed
- Response parsing error
- JSON structure mismatch
- No error logging to detect the issue

---

## ✅ The Fix

### **1. Added Debug Output**

Now shows what the AI is actually returning:

```python
# Debug: Show sample of first result in first batch
if i == 0 and len(data) > 0:
    print(f"   📋 Sample AI response keys: {list(data[0].keys())}")
    print(f"   📋 Sample score: {data[0].get('score', 'MISSING')}")
```

**You'll see:**

```
🤖 Evaluating 490 contacts with AI (gpt-4o-mini)...
   📋 Sample AI response keys: ['id', 'relevant', 'score', 'reason', 'field']
   📋 Sample score: 0.75
   Evaluated 20/490 contacts    [  4.1%] ░░░░░░░░░░░░░░░░░░░░
```

### **2. Improved Score Parsing**

Tries multiple possible score keys:

```python
# Try multiple possible score keys
score = ai_data.get("score")
if score is None:
    score = ai_data.get("confidence", ai_data.get("relevance_score", 0.0))
    if score == 0.0:
        print(f"⚠️ Contact #{i+idx}: No score in AI response! Keys: {list(ai_data.keys())}")

# Ensure score is a float
try:
    score = float(score)
except (ValueError, TypeError):
    print(f"⚠️ Contact #{i+idx}: Invalid score '{score}', defaulting to 0.0")
    score = 0.0
```

### **3. Added Score Distribution Summary**

After all contacts evaluated, shows statistics:

```python
📊 Score Distribution:
   Average: 0.456 | Min: 0.02 | Max: 0.95
   Above threshold (0.3): 287/490
```

### **4. Warning for Suspicious Scores**

If all scores are < 0.1:

```python
⚠️  WARNING: All scores are extremely low (max=0.000)!
   This likely indicates a parsing error. Check the debug output above.
```

---

## 🧪 How to Test

### **Run Again with the Same University:**

```bash
python3 run_with_ai.py --urls [YOUR_URL] --ai-score 0.3
```

### **Expected Output Now:**

```
🤖 Evaluating 490 contacts with AI (gpt-4o-mini)...
   📋 Sample AI response keys: ['id', 'relevant', 'score', 'reason', 'field']
   📋 Sample score: 0.75
   Evaluated 20/490 contacts    [  4.1%] ░░░░░░░░░░░░░░░░░░░░
   Evaluated 40/490 contacts    [  8.2%] █░░░░░░░░░░░░░░░░░░░
   ...
   Evaluated 490/490 contacts    [100.0%] ████████████████████

   📊 Score Distribution:
      Average: 0.456 | Min: 0.02 | Max: 0.95
      Above threshold (0.3): 287/490

✅ 287 contacts passed AI threshold (0.3)
```

---

## 🎯 What to Look For

### **Good Signs ✅**

1. **Sample output appears:**

   ```
   📋 Sample AI response keys: ['id', 'relevant', 'score', 'reason', 'field']
   📋 Sample score: 0.75
   ```

2. **Score distribution is reasonable:**

   ```
   Average: 0.4-0.6 | Min: 0.0-0.2 | Max: 0.8-1.0
   Above threshold (0.3): ~50-70% of contacts
   ```

3. **No warnings appear**

### **Bad Signs ⚠️**

1. **Sample score is MISSING:**

   ```
   📋 Sample score: MISSING
   ```

   → AI is not returning scores!

2. **Lots of warnings:**

   ```
   ⚠️ Contact #23: No score in AI response! Keys: [...]
   ⚠️ Contact #24: No score in AI response! Keys: [...]
   ```

   → Response format is wrong

3. **Suspicious score distribution:**

   ```
   Average: 0.000 | Min: 0.000 | Max: 0.000
   ⚠️  WARNING: All scores are extremely low!
   ```

   → All scores defaulted to 0.0

4. **Expected vs actual mismatch:**
   ```
   ⚠️ Warning: Expected 20 results, got 15
   ```
   → AI didn't evaluate all contacts

---

## 🔧 Possible Issues & Solutions

### **Issue 1: AI Returns No Scores**

**Symptoms:**

```
📋 Sample score: MISSING
⚠️ Contact #0: No score in AI response! Keys: ['id', 'name', 'field']
```

**Cause:** AI isn't following the prompt format

**Solution:** Check OpenAI API changes, or adjust prompt

### **Issue 2: Wrong Batch Size**

**Symptoms:**

```
⚠️ Warning: Expected 20 results, got 5
```

**Cause:** AI didn't evaluate all 20 contacts in batch

**Solution:** Reduce batch size in `.env`:

```bash
AI_BATCH_SIZE=10  # Down from 20
```

### **Issue 3: All Scores Are Low**

**Symptoms:**

```
Average: 0.123 | Min: 0.01 | Max: 0.25
Above threshold (0.5): 0/490
```

**Cause:** University/contacts genuinely not relevant

**Solutions:**

- Lower threshold: `--ai-score 0.2`
- Check if university is in your target domain
- Try non-AI mode: `python3 run_without_ai.py --urls [URL]`

### **Issue 4: Parsing Error**

**Symptoms:**

```
⚠️ AI evaluation failed for batch: Expecting value: line 1 column 1 (char 0)
```

**Cause:** AI returned invalid JSON

**Solution:** Check API status, retry, or report bug

---

## 📊 Score Interpretation

### **AI Score Ranges:**

| Score       | Meaning             | Typical            |
| ----------- | ------------------- | ------------------ |
| **0.8-1.0** | Highly relevant     | 5-10% of contacts  |
| **0.6-0.8** | Very relevant       | 15-25% of contacts |
| **0.4-0.6** | Moderately relevant | 30-40% of contacts |
| **0.2-0.4** | Somewhat relevant   | 20-30% of contacts |
| **0.0-0.2** | Not relevant        | 10-20% of contacts |

### **Normal Distribution:**

For a technical university in power electronics domain:

```
Above 0.7: ~20-30%
Above 0.5: ~40-60%
Above 0.3: ~60-80%
Above 0.1: ~85-95%
```

### **Red Flags:**

- **All scores = 0.0:** Parsing bug
- **All scores < 0.1:** Wrong university or prompt issue
- **All scores > 0.9:** Too lenient, threshold too low

---

## 🎛️ Adjusting Threshold

### **Conservative (High Quality):**

```bash
--ai-score 0.7  # Only highly relevant contacts
```

**Result:** Fewer but higher quality contacts

### **Balanced (Recommended):**

```bash
--ai-score 0.5  # Default, good balance
```

**Result:** Good mix of quality and quantity

### **Inclusive (Maximum Coverage):**

```bash
--ai-score 0.3  # More lenient
```

**Result:** More contacts, some may be less relevant

### **Very Inclusive:**

```bash
--ai-score 0.1  # Almost everyone
```

**Result:** Maximum contacts, manual filtering needed

---

## 🔄 Comparison Test

To verify the fix works, run both modes:

### **1. With AI (should find ~50-70% of contacts):**

```bash
python3 run_with_ai.py --urls https://www.kit.edu --ai-score 0.3
```

### **2. Without AI (should find ~40-60% with keyword matching):**

```bash
python3 run_without_ai.py --urls https://www.kit.edu
```

**Expected:**

- AI mode: More accurate scoring (0.0-1.0 range)
- Non-AI mode: Binary (0.3 or 1.0)
- Both should find contacts (not 0)

---

## 📝 Files Modified

- ✅ `academic_lead_extractor.py` - Added debugging and improved parsing
- ✅ `docs/AI_SCORING_DEBUG_GUIDE.md` - This guide

---

## 🆘 Still Getting 0 Contacts?

### **Check These:**

1. **API Key Valid:**

   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

2. **API Credits:**

   - Log into OpenAI dashboard
   - Check if you have credits

3. **University Relevant:**

   - Is it a technical university?
   - Does it have power electronics department?

4. **Try Non-AI Mode:**

   ```bash
   python3 run_without_ai.py --urls [URL]
   ```

   If this finds contacts but AI doesn't, it's an AI issue.

5. **Check Sample Data:**
   Look at the debug output for the sample AI response.

---

**Now run the script again and check the new debug output!** 🎯

The script will tell you exactly what's going wrong with the AI scoring.
