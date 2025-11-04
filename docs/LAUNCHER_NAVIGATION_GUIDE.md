# 🎮 Interactive Launcher Navigation Guide

## New Feature: Step Back & Exit Options

The interactive launchers now support **going back** and **exiting** at any prompt!

---

## 🆕 What's New

### **1. Exit Option (0)**
Exit at any time from the main menu by pressing `0`

### **2. Go Back Option (b)**
Type `b` or `back` at any prompt to return to the previous step

### **3. Better Navigation**
- Clear menu with numbered options
- Colored output for better readability
- Loop back on invalid input
- Exit closes the terminal automatically

---

## 🎯 How to Navigate

### **Main Menu**

```
================================================================================
   ACADEMIC LEAD EXTRACTOR - WITHOUT AI
================================================================================

Options:
  1. Process ALL universities from universities.csv (default)
  2. Process SINGLE university URL
  3. Process MULTIPLE universities (space-separated URLs)
  4. Use CUSTOM CSV file
  0. EXIT

Enter your choice (1-4, 0 to exit) [default: 1]: _
```

**Actions:**
- Enter `1-4` → Choose your option
- Enter `0` → Exit immediately and close terminal
- Press Enter → Use default (option 1)

---

### **Depth Selection**

```
Exploration depth:
  1 = Shallow (fast, ~20-30 contacts per university)
  2 = Normal (balanced, ~35-60 contacts) [default]
  3 = Deep (thorough, ~60-100 contacts)

Enter depth (1-3) or 'b' to go back [default: 2]: _
```

**Actions:**
- Enter `1`, `2`, or `3` → Choose depth level
- Enter `b` or `back` → Return to main menu
- Press Enter → Use default (depth 2)

---

### **URL Input**

```
Enter university URL (or 'b' to go back): _
```

**Actions:**
- Enter a valid URL → Proceed with extraction
- Enter `b` or `back` → Return to main menu
- Empty input → Show error and ask again

---

### **Multiple URLs Input**

```
Enter URLs separated by spaces (or 'b' to go back):
URLs: _
```

**Actions:**
- Enter multiple URLs (space-separated) → Proceed with extraction
- Enter `b` or `back` → Return to main menu
- Empty input → Show error and ask again

---

### **CSV File Input**

```
Enter CSV filename (or 'b' to go back): _
```

**Actions:**
- Enter valid filename → Proceed with extraction
- Enter `b` or `back` → Return to main menu
- Empty input → Show error and ask again
- File not found → Show error and ask again

---

## 📝 Complete Navigation Flow

### **Example 1: Change Your Mind**

```
Step 1: Choose option 2 (Single URL)
Step 2: At depth selection, type 'b'
Result: Back to main menu ✅

Step 3: Choose option 3 (Multiple URLs)
Step 4: Continue with extraction ✅
```

### **Example 2: Quick Exit**

```
Step 1: Double-click launcher
Step 2: See main menu
Step 3: Type '0'
Result: Exits immediately and closes terminal ✅
```

### **Example 3: Correct Input Mistake**

```
Step 1: Choose option 2 (Single URL)
Step 2: Choose depth 3
Step 3: Start typing URL, realize it's wrong
Step 4: Type 'b' at URL prompt
Result: Back to main menu, can restart ✅
```

### **Example 4: With AI Launcher**

```
Step 1: Choose option 2 (Single URL)
Step 2: Enter AI score: 0.7
Step 3: At depth prompt, type 'b'
Result: Back to main menu (lose AI score, starts over) ✅
```

---

## 🎨 Visual Flow Diagram

```
┌─────────────────┐
│   Main Menu     │
│   (1-4, 0)      │
└────┬─────┬──────┘
     │     │
     │     └───→ 0: Exit (closes terminal)
     │
     ↓
┌─────────────────┐
│  Choose Option  │
│   1, 2, 3, 4    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  AI Score (AI)  │◄─── 'b' or 'back' returns to Main Menu
│  or Skip (no-AI)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Choose Depth   │◄─── 'b' or 'back' returns to Main Menu
│    1, 2, 3      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Enter Details  │◄─── 'b' or 'back' returns to Main Menu
│  (URL/CSV/etc)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Run Extraction │
└─────────────────┘
```

---

## 🆚 Before vs After

### **Before (Old Version):**
```
❌ Choose wrong option → Stuck, must run extraction or Ctrl+C
❌ Change mind → Ctrl+C and restart
❌ Exit → Close terminal window manually
```

### **After (New Version):**
```
✅ Choose wrong option → Type 'b' to go back
✅ Change mind → Type 'b' at any prompt
✅ Exit → Type '0' and terminal closes automatically
```

---

## 💡 Pro Tips

### **Tip 1: Preview Before Committing**
```
1. Start launcher
2. Choose option 1 (all universities)
3. See depth prompt → realize you want to test first
4. Type 'b' to go back
5. Choose option 2 (single URL) instead
```

### **Tip 2: Try Different Depths**
```
1. Choose option 2 (single URL)
2. Select depth 1
3. See extraction only gets 20 contacts
4. At next run, use depth 3
```

### **Tip 3: Quick Exit During Setup**
```
1. Start launcher by accident
2. At main menu, type '0'
3. Terminal closes immediately
```

### **Tip 4: Recover from Typos**
```
1. Choose option 2
2. Set depth 3
3. Start typing URL: "htps://..." (typo!)
4. Type 'b' to go back
5. Start over with correct URL
```

---

## 🎮 Keyboard Shortcuts Summary

| Input | Action | Available At |
|-------|--------|--------------|
| `0` | Exit and close terminal | Main menu only |
| `b` or `back` | Go back to main menu | All prompts (depth, URL, CSV, AI score) |
| `Enter` | Use default value | All prompts with defaults |
| `1-4` | Choose option | Main menu |
| `1-3` | Choose depth | Depth selection |

---

## 🔄 Loop Protection

The launchers now **loop on invalid input** instead of exiting:

```
Enter depth (1-3) or 'b' to go back [default: 2]: 5
Invalid input. Please enter 1, 2, 3, or 'b' to go back.

Enter depth (1-3) or 'b' to go back [default: 2]: _
```

**Old behavior:** Script would continue with invalid value or error out  
**New behavior:** Asks again until valid input ✅

---

## 🪟 Platform Differences

### **macOS/Linux (.command files)**
- Press `Ctrl+C` at any time to force quit (emergency only)
- Type `b` or `back` to navigate back (recommended)
- Type `0` at main menu to exit gracefully

### **Windows (.bat files)**
- Press `Ctrl+C` at any time to force quit (emergency only)
- Type `b` or `back` to navigate back (recommended)
- Type `0` at main menu to exit gracefully
- Case insensitive: `b`, `B`, `back`, `BACK` all work

---

## ⚠️ Important Notes

1. **Going back clears previous selections**
   - If you enter AI score 0.7 then go back, you'll need to enter it again
   - This is intentional to ensure you can change everything

2. **Main menu clears screen**
   - When returning to main menu, screen is cleared for better UX
   - Previous output is not visible

3. **Exit (0) closes terminal**
   - On both Windows and macOS, choosing 0 exits and closes the terminal
   - No "Press Enter to exit" prompt

4. **Extraction starts = No going back**
   - Once extraction begins, you can't go back
   - Use Ctrl+C to interrupt if needed

---

## 📊 Example Sessions

### **Session 1: Perfect Run**
```
1. Launch → Main menu
2. Type '2' → Single URL
3. Depth → Type '3' → Deep
4. URL → 'https://www.kit.edu'
5. ✅ Extraction runs with depth 3
```

### **Session 2: Changed Mind**
```
1. Launch → Main menu
2. Type '1' → All universities
3. Depth → Type 'b' → Back to main menu
4. Type '2' → Single URL instead
5. Depth → Type '2' → Normal
6. URL → 'https://www.kit.edu'
7. ✅ Extraction runs with single URL, depth 2
```

### **Session 3: Quick Exit**
```
1. Launch → Main menu
2. Type '0' → Exit
3. ✅ Terminal closes
```

### **Session 4: Multiple Backs**
```
1. Launch → Main menu
2. Type '2' → Single URL
3. Depth → Type '3' → Deep
4. URL → Type 'b' → Back to main menu
5. Type '2' → Single URL again
6. Depth → Type '1' → Shallow this time
7. URL → 'https://www.kit.edu'
8. ✅ Extraction runs with depth 1
```

---

## ✅ Summary

**New Navigation Options:**
- ✅ Type `0` at main menu to exit
- ✅ Type `b` or `back` to go back to main menu
- ✅ Loop on invalid input (no crashes)
- ✅ Clear error messages
- ✅ Better user experience

**Works on:**
- ✅ Windows (.bat launchers)
- ✅ macOS (.command launchers)
- ✅ Linux (.command launchers)

**Available in:**
- ✅ `run_without_ai_launcher.bat`
- ✅ `run_with_ai_launcher.bat`
- ✅ `run_without_ai_launcher.command`
- ✅ `run_with_ai_launcher.command`

---

**No more getting stuck in the launchers!** 🎉

Navigate freely with `b` to go back and `0` to exit!

