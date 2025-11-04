# Time and Cost Tracking

## Overview
The Academic Lead Extractor now tracks detailed timing information and AI token costs for complete transparency and cost optimization.

## Features Added

### 1. ⏱️ Time Tracking

#### Per-University Timing
- Tracks extraction time for each university
- Shows top 10 slowest universities
- Displays contacts extracted per university
- Helps identify performance bottlenecks

**Example Output:**
```
📊 Per-University Extraction Times:
   KIT (Karlsruhe)                         : 125.3s → 45 contacts
   ETH Zurich                              :  98.7s → 32 contacts
   TU Munich                               :  87.2s → 28 contacts
   ...
```

#### Total Pipeline Timing
- Scraping time (web crawling and extraction)
- AI evaluation time (OpenAI API calls)
- Total pipeline time
- Average time per university

### 2. 💰 Token Cost Tracking

#### Token Usage Metrics
- **Input tokens**: Tokens sent to AI (prompts + context)
- **Output tokens**: Tokens received from AI (responses)
- **Total tokens**: Sum of input + output
- **Cost per contact**: Helps optimize batch sizes

#### Pricing Information
Automatically tracks costs based on current OpenAI pricing:

**gpt-4o-mini** (Recommended - Fast & Affordable)
- Input: $0.150 per 1M tokens
- Output: $0.600 per 1M tokens

**gpt-4o** (Higher Quality)
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens

**Example Output:**
```
💰 AI TOKEN USAGE & COST:
   Input tokens:               125,430
   Output tokens:               18,765
   Total tokens:               144,195
   Estimated cost:             $0.0306 USD
   Model used:                 gpt-4o-mini
   Cost per contact:           $0.0010
```

## Configuration

### Pricing Updates
Update prices in `config.py` if OpenAI changes their pricing:

```python
AI_PRICING = {
    "gpt-4o-mini": {
        "input": 0.150,   # per 1M tokens
        "output": 0.600
    },
    "gpt-4o": {
        "input": 2.50,
        "output": 10.00
    }
}
```

## Final Summary Output

At the end of each extraction run, you'll see a comprehensive summary:

```
======================================================================
📈 EXTRACTION SUMMARY
======================================================================
🎯 Universities processed:     15
📧 Total contacts extracted:   342
✅ Contacts after filtering:   89

⏱️  TIMING BREAKDOWN:
   Scraping time:              245.3s (4.1min)
   AI evaluation time:         67.8s (1.1min)
   Total pipeline time:        313.1s (5.2min)
   Avg time per university:    16.4s

💰 AI TOKEN USAGE & COST:
   Input tokens:               125,430
   Output tokens:               18,765
   Total tokens:               144,195
   Estimated cost:             $0.0306 USD
   Model used:                 gpt-4o-mini
   Cost per contact:           $0.0010
======================================================================
```

## Cost Optimization Tips

### 1. Choose the Right Model
- **gpt-4o-mini**: 16x cheaper than gpt-4o, great for most use cases
- **gpt-4o**: Use only when you need maximum accuracy

### 2. Adjust Batch Size
Larger batches = fewer API calls but longer prompts:
```bash
# Smaller batches (more API calls, shorter prompts)
python3 main.py --urls https://example.edu --ai-batch-size 10

# Larger batches (fewer API calls, longer prompts)
python3 main.py --urls https://example.edu --ai-batch-size 30
```

### 3. Optimize Depth Settings
Fewer pages = lower costs:
```bash
# Shallow extraction (fast, lower cost)
python3 main.py --depth 1

# Deep extraction (thorough, higher cost)
python3 main.py --depth 3
```

## Technical Details

### Token Tracking Implementation
Token usage is captured from OpenAI API responses:
```python
if hasattr(response, 'usage') and response.usage:
    usage = response.usage
    input_tokens = getattr(usage, 'prompt_tokens', 0)
    output_tokens = getattr(usage, 'completion_tokens', 0)
    total_tokens = getattr(usage, 'total_tokens', input_tokens + output_tokens)
```

### Cost Calculation
```python
batch_cost = (input_tokens / 1_000_000 * pricing["input"]) + \
             (output_tokens / 1_000_000 * pricing["output"])
```

## Benefits

1. **Transparency**: Know exactly how long each university takes
2. **Cost Awareness**: Track real-time costs and optimize spending
3. **Performance Insights**: Identify slow universities/bottlenecks
4. **Budget Planning**: Estimate costs before large runs
5. **ROI Tracking**: Calculate cost per quality contact

## Example Use Cases

### Budget-Conscious Extraction
```bash
# Use cheapest model, shallow depth, small batches
python3 main.py \
  --ai-model gpt-4o-mini \
  --depth 1 \
  --ai-batch-size 15 \
  --urls https://example.edu
```

### Maximum Quality Extraction
```bash
# Use best model, deep exploration
python3 main.py \
  --ai-model gpt-4o \
  --depth 3 \
  --ai-batch-size 10 \
  --urls https://example.edu
```

### Cost Estimation
Run a test with 1-2 universities first to estimate costs for larger batches:
```bash
# Test run
python3 main.py --urls https://test.edu

# Check output for estimated cost
# Multiply by number of universities for total estimate
```

## Files Modified

- `config.py`: Added AI_PRICING, MAX_RETRIES, RETRY_DELAY
- `academic_lead_extractor/processor.py`: Added timing tracking and summary output
- `academic_lead_extractor/ai_evaluator.py`: Added token usage tracking and cost calculation
- `academic_lead_extractor/scraper.py`: Enhanced retry logic with timing

## Notes

- Costs are **estimates** based on official OpenAI pricing
- Actual costs may vary slightly due to tokenization differences
- Token counts include all AI operations (link discovery, filtering, evaluation)
- Timing includes all network operations and API calls

