# Launcher Scripts - AI Profile Detection Prompt

## Overview
The launcher scripts now automatically ask users if they want to enable AI Profile Detection, making it easy to choose the right performance/accuracy balance.

## What Users Will See

### Step-by-Step Flow

When running `run_with_ai_launcher.command` (macOS) or `run_with_ai_launcher.bat` (Windows), users will see:

```
================================================================================
   ACADEMIC LEAD EXTRACTOR - WITH AI FILTERING
================================================================================

Options:
  1. Process ALL universities from universities.csv (default)
  2. Process SINGLE university URL
  3. Process MULTIPLE universities (space-separated URLs)
  4. Use CUSTOM CSV file
  0. EXIT

Enter your choice (1-4, 0 to exit) [default: 1]: 1

AI Model Selection:
  1. gpt-4o-mini - Fast + cost-efficient (filter 500-10,000 contacts) [default]
  2. gpt-4o - Stronger understanding, fewer false positives

Enter model (1-2) or 'b' to go back [default: 1]: 1

AI Score threshold (0.0-1.0) or 'b' to go back [default: 0.5]: 0.5

Exploration depth:
  1 = Shallow (fast, ~20-30 contacts per university)
  2 = Normal (balanced, ~35-60 contacts) [default]
  3 = Deep (thorough, ~60-100 contacts)

Enter depth (1-3) or 'b' to go back [default: 2]: 2

⚡ AI Profile Detection (Advanced):
  Uses AI to detect individual researcher profiles

  1. Disabled = FAST (60-80% faster, recommended) [default]
  2. Enabled  = SLOW (may catch edge cases, 4-6x slower)

💡 TIP: Keep disabled unless you need maximum completeness

Select option (1-2) or 'b' to go back [default: 1]: 1

Running with universities.csv...
```

## Default Behavior

### Most Common Choice (Recommended)
```
Select option (1-2): 1  <-- Just press Enter (default)
```
**Result**: ⚡ Fast extraction (60-80% faster)

### For Maximum Completeness
```
Select option (1-2): 2
⚠️  Warning: This will make extraction 4-6x slower!
```
**Result**: 🐌 Slow but thorough extraction

## Features

### User-Friendly Prompts
- ✅ Clear explanation of what it does
- ✅ Shows performance impact (60-80% faster)
- ✅ Recommends default (disabled)
- ✅ Warning if user enables it
- ✅ 'b' to go back option
- ✅ Default is "No" (fastest)

### Visual Indicators

**macOS/Linux** (`run_with_ai_launcher.command`):
- Yellow text for the section header
- Blue tip message
- Yellow warning if enabled

**Windows** (`run_with_ai_launcher.bat`):
- Yellow color for section header
- Yellow warning if enabled
- 2-second pause to show warning

## User Experience Flow

### Fast Extraction (Most Users)
1. Choose option (1-4)
2. Select AI model (default: gpt-4o-mini)
3. Set AI score (default: 0.5)
4. Choose depth (default: 2 - Normal)
5. **AI profile detection** → Press Enter for option 1 (Disabled)
6. ⚡ Fast extraction starts!

**Total time**: ~5 seconds to configure

### Thorough Extraction (Edge Cases)
1. Choose option (1-4)
2. Select AI model (maybe gpt-4o for max quality)
3. Set AI score (maybe 0.3 for wider net)
4. Choose depth (3 - Deep)
5. **AI profile detection** → Type '2' + Enter (Enabled)
6. See warning ⚠️
7. 🐌 Thorough extraction starts

**Total time**: ~10 seconds to configure

## Comparison Table

| Scenario | Profile Detection | Expected Speed | Best For |
|----------|------------------|----------------|----------|
| **Default** | Option 1 (Disabled) | 2-3 min/uni | Most universities |
| **Thorough** | Option 2 (Enabled) | 10-15 min/uni | Unusual page structures |
| **Quick Test** | Option 1 + Depth 1 | 1-2 min/uni | Testing/validation |
| **Maximum** | Option 2 + Depth 3 | 15-20 min/uni | Complete coverage needed |

## Examples of User Choices

### Example 1: Standard Production Run
```
Choice: 1 (process all)
Model: 1 (gpt-4o-mini)
Score: 0.5 (default)
Depth: 2 (normal)
Profile Detection: 1 (disabled) ✅ RECOMMENDED
```
**Result**: Fast, cost-efficient, excellent accuracy

### Example 2: Maximum Completeness
```
Choice: 2 (single URL)
Model: 2 (gpt-4o)
Score: 0.3 (lower threshold)
Depth: 3 (deep)
Profile Detection: 2 (enabled)
```
**Result**: Slowest but most thorough

### Example 3: Quick Test
```
Choice: 2 (single URL)
Model: 1 (gpt-4o-mini)
Score: 0.5 (default)
Depth: 1 (shallow)
Profile Detection: 1 (disabled)
```
**Result**: Fastest for testing

## Technical Details

### What Happens Behind the Scenes

**When Disabled (Default)**:
```bash
python3 run_with_ai.py --urls https://example.edu
# No --use-ai-profile-detection flag passed
```

**When Enabled**:
```bash
python3 run_with_ai.py --urls https://example.edu --use-ai-profile-detection
# Flag added to command
```

### Integration with Other Features

The AI profile detection prompt is part of the configuration flow:
1. ✅ AI Model Selection
2. ✅ AI Score Threshold
3. ✅ Exploration Depth
4. ✅ **AI Profile Detection** (NEW)
5. → Start extraction

All settings can be changed by typing 'b' to go back.

## Benefits

### For Users
- 🎯 **Clear choice**: Understand the trade-off before deciding
- ⚡ **Fast by default**: Most users get best performance
- 🔄 **Easy to change**: Can go back and modify
- 💡 **Informed decision**: Clear explanation and recommendation

### For Developers
- ✅ **No code changes needed**: Works with existing main.py
- ✅ **Backward compatible**: Old scripts still work
- ✅ **Consistent**: Same across macOS and Windows
- ✅ **Maintainable**: Easy to update messaging

## Summary

**The launcher scripts now intelligently guide users to:**
1. Choose the **fastest settings by default** (recommended)
2. **Understand the trade-offs** before enabling slow features
3. **Easily experiment** with different configurations
4. **Get warnings** when choosing slow options

**Result**: Better user experience, faster extractions, and informed decisions! 🚀

