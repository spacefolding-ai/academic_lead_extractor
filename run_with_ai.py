#!/usr/bin/env python3
"""
Run Academic Lead Extractor WITH AI
=====================================
Quality scoring and filtering
Expected: 3,000-8,000 high-quality contacts
Cost: ~$10-15 in OpenAI API costs
Runtime: ~3-5 hours for 434 universities

Usage:
  python3 run_with_ai.py                                    # All universities from CSV
  python3 run_with_ai.py --urls https://www.kit.edu        # Single URL
  python3 run_with_ai.py --urls URL1 URL2 URL3             # Multiple URLs
  python3 run_with_ai.py --csv my_universities.csv         # Custom CSV
"""

import os
import sys

# Parse command-line arguments FIRST to count universities
import argparse
temp_parser = argparse.ArgumentParser(add_help=False)
temp_parser.add_argument('--urls', nargs='+')
temp_parser.add_argument('--csv', default='universities.csv')
temp_parser.add_argument('--ai-score', type=float)
temp_parser.add_argument('--ai-model', type=str, choices=['gpt-4o-mini', 'gpt-4o'])
temp_parser.add_argument('--depth', type=int, choices=[1, 2, 3])
temp_parser.add_argument('--max-faculty-links', type=int)
temp_parser.add_argument('--max-department-links', type=int)
temp_args, _ = temp_parser.parse_known_args()

# Count universities
university_count = 0
if temp_args.urls:
    university_count = len(temp_args.urls)
else:
    # Load from CSV
    import pandas as pd
    csv_file = temp_args.csv
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        if 'Website' in df.columns:
            university_count = df['Website'].notna().sum()

# Calculate dynamic estimates based on actual count
cost_min = max(0.02, university_count * 0.02)
cost_max = max(0.05, university_count * 0.035)
contacts_min = university_count * 7
contacts_max = university_count * 18
time_hours_min = max(0.1, university_count * 0.007)
time_hours_max = max(0.2, university_count * 0.012)

# Format cost nicely
if cost_max < 1:
    cost_str = f"${cost_min:.2f}-${cost_max:.2f}"
else:
    cost_str = f"${cost_min:.0f}-${cost_max:.0f}"

# Format time nicely
if time_hours_max < 1:
    time_str = f"{int(time_hours_min * 60)}-{int(time_hours_max * 60)} minutes"
else:
    time_str = f"{time_hours_min:.1f}-{time_hours_max:.1f} hours"

print("=" * 80)
print("🤖 ACADEMIC LEAD EXTRACTOR - WITH AI FILTERING")
print("=" * 80)
print()
print("Configuration:")
print("  ✅ AI Filtering: ENABLED (gpt-4o-mini)")
print("  ✅ Aggressive exploration: Enabled")
print("  ✅ Multi-language support: Enabled")
print("  ✅ Name extraction: Exact from webpage")
print("  ✅ AI relevance scoring: 0.0-1.0")
print("  ✅ AI field classification: Enabled")
print("  ✅ AI reasoning: Included")
print(f"  🎯 Universities to process: {university_count}")
print(f"  💰 Estimated cost: {cost_str} (OpenAI API)")
print(f"  📊 Expected contacts: {contacts_min:,}-{contacts_max:,} (high quality)")
print(f"  ⏱️  Estimated time: {time_str}")
print()

# Check for API key
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key or api_key == 'your-key-here':
    print("❌ ERROR: OPENAI_API_KEY not found or not set in .env file")
    print()
    print("Please add your OpenAI API key to the .env file:")
    print("  1. Open .env file")
    print("  2. Set: OPENAI_API_KEY=sk-your-actual-key-here")
    print()
    sys.exit(1)

print(f"  🔑 API Key: Found ({api_key[:20]}...)")

# Check for custom arguments
if len(sys.argv) > 1:
    print(f"  📋 Custom arguments: {' '.join(sys.argv[1:])}")

print()
print("=" * 80)
print()
print(f"⚠️  Note: This will use OpenAI API credits. Estimated cost: {cost_str}")
print("Press Ctrl+C now to cancel, or wait 5 seconds to continue...")
print()

import time
try:
    for i in range(5, 0, -1):
        print(f"Starting in {i}...", end='\r')
        time.sleep(1)
    print("Starting now!       ")
    print()
except KeyboardInterrupt:
    print("\n\n✋ Cancelled by user")
    sys.exit(0)

# Set environment variables BEFORE importing (module reads them at import time)
os.environ['USE_AI'] = 'true'
if temp_args.ai_score is not None:
    # Validate AI score threshold range
    if not 0.0 <= temp_args.ai_score <= 1.0:
        print(f"❌ Error: AI score threshold must be between 0.0 and 1.0 (got {temp_args.ai_score})")
        sys.exit(1)
    os.environ['AI_MIN_SCORE'] = str(temp_args.ai_score)
if temp_args.ai_model is not None:
    os.environ['AI_MODEL'] = temp_args.ai_model

# Import and run the main script
try:
    # Import and run main.py
    import main
    # Run main entry point (it will handle all argument parsing)
    main.main()
except KeyboardInterrupt:
    print("\n\n⚠️  Extraction interrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

