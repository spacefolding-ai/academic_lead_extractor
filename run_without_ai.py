#!/usr/bin/env python3
"""
Run Academic Lead Extractor WITHOUT AI
=====================================
Maximum coverage, $0 cost
Expected: 5,000-15,000 contacts
Runtime: ~2-3 hours for 434 universities

Usage:
  python3 run_without_ai.py                                    # All universities from CSV
  python3 run_without_ai.py --urls https://www.kit.edu        # Single URL
  python3 run_without_ai.py --urls URL1 URL2 URL3             # Multiple URLs
  python3 run_without_ai.py --csv my_universities.csv         # Custom CSV
"""

import os
import sys

print("=" * 80)
print("🚀 ACADEMIC LEAD EXTRACTOR - WITHOUT AI")
print("=" * 80)
print()
print("Configuration:")
print("  ✅ AI Filtering: DISABLED")
print("  ✅ Aggressive exploration: Enabled")
print("  ✅ Multi-language support: Enabled")
print("  ✅ Name extraction: Exact from webpage")
print("  💰 Cost: $0")
print("  📊 Expected contacts: 5,000-15,000")
print("  ⏱️  Estimated time: 2-3 hours")

# Check for custom arguments
if len(sys.argv) > 1:
    print(f"  📋 Custom arguments: {' '.join(sys.argv[1:])}")

print()
print("=" * 80)
print()

# Parse command-line arguments FIRST (before importing to set env vars)
# We need to do a minimal parse here to get ai_score before module import
import argparse
temp_parser = argparse.ArgumentParser(add_help=False)
temp_parser.add_argument('--ai-score', type=float)
temp_parser.add_argument('--no-ai', action='store_true')
temp_parser.add_argument('--depth', type=int, choices=[1, 2, 3])
temp_parser.add_argument('--max-faculty-links', type=int)
temp_parser.add_argument('--max-department-links', type=int)
temp_args, _ = temp_parser.parse_known_args()

# Set environment variables BEFORE importing (module reads them at import time)
os.environ['USE_AI'] = 'false' if temp_args.no_ai else 'false'  # Default to false for this script
if temp_args.ai_score is not None:
    # Validate AI score threshold range
    if not 0.0 <= temp_args.ai_score <= 1.0:
        print(f"❌ Error: AI score threshold must be between 0.0 and 1.0 (got {temp_args.ai_score})")
        sys.exit(1)
    os.environ['AI_MIN_SCORE'] = str(temp_args.ai_score)

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

