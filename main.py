#!/usr/bin/env python3
"""
Academic Lead Extractor - Main Entry Point
============================================
Extract academic contacts from university websites with AI-powered filtering.
"""

import os
import sys
import asyncio
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AI settings
USE_AI = os.getenv("USE_AI", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
# Validate AI_MODEL from environment - only allow gpt-4o-mini and gpt-4o
VALID_MODELS = ["gpt-4o-mini", "gpt-4o"]
if AI_MODEL not in VALID_MODELS:
    print(f"❌ Error: AI_MODEL in .env must be one of: {', '.join(VALID_MODELS)} (got {AI_MODEL})")
    print(f"   Please set AI_MODEL to either 'gpt-4o-mini' or 'gpt-4o'")
    sys.exit(1)
AI_BATCH_SIZE = int(os.getenv("AI_BATCH_SIZE", "20"))
AI_MIN_SCORE = float(os.getenv("AI_MIN_SCORE", "0.5"))
# Validate AI_MIN_SCORE from environment
if not 0.0 <= AI_MIN_SCORE <= 1.0:
    print(f"❌ Error: AI_MIN_SCORE in .env must be between 0.0 and 1.0 (got {AI_MIN_SCORE})")
    print("   Please set AI_MIN_SCORE to a value between 0.0 and 1.0")
    sys.exit(1)

if USE_AI and not OPENAI_API_KEY:
    print("⚠️  Warning: USE_AI=true but OPENAI_API_KEY not found in .env")
    print("    Continuing without AI filtering...")
    USE_AI = False

if USE_AI:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    print(f"✅ AI Filtering: ENABLED (Model: {AI_MODEL}, Min Score: {AI_MIN_SCORE})")
else:
    client = None
    print("ℹ️  AI Filtering: DISABLED (using keyword matching only)")

# Import config for depth settings
from config import MAX_FACULTY_LINKS, MAX_DEPARTMENT_LINKS
from academic_lead_extractor.processor import main as run_pipeline


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Academic Lead Extractor - Extract academic contacts from university websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all universities from universities.csv (default)
  python3 main.py
  
  # Process a single university URL
  python3 main.py --urls https://www.kit.edu
  
  # Process multiple universities
  python3 main.py --urls https://www.kit.edu https://www.eth.ch https://www.tu-berlin.de
  
  # Use custom CSV file
  python3 main.py --csv my_universities.csv
  
  # Set exploration depth
  python3 main.py --urls https://www.kit.edu --depth 3
  
  # Fine-tune limits
  python3 main.py --max-faculty-links 100 --max-department-links 25
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--urls',
        nargs='+',
        metavar='URL',
        help='One or more university website URLs to process (space-separated)'
    )
    group.add_argument(
        '--csv',
        metavar='FILE',
        default='universities.csv',
        help='Path to CSV file with universities (default: universities.csv)'
    )
    
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI filtering (same as setting USE_AI=false in .env)'
    )
    
    parser.add_argument(
        '--ai-score',
        type=float,
        metavar='SCORE',
        help='Minimum AI score threshold (must be 0.0-1.0, default: 0.5)'
    )
    
    parser.add_argument(
        '--ai-model',
        type=str,
        metavar='MODEL',
        choices=['gpt-4o-mini', 'gpt-4o'],
        help='AI model to use: gpt-4o-mini (fast, cost-efficient), gpt-4o (stronger understanding)'
    )
    
    # Exploration depth options
    depth_group = parser.add_argument_group('exploration depth')
    depth_group.add_argument(
        '--depth',
        type=int,
        choices=[1, 2, 3],
        metavar='LEVEL',
        help='Exploration depth: 1=shallow (fast), 2=normal (default), 3=deep (thorough)'
    )
    depth_group.add_argument(
        '--max-faculty-links',
        type=int,
        metavar='N',
        help='Max staff/people pages to scrape per university (default: 50)'
    )
    depth_group.add_argument(
        '--max-department-links',
        type=int,
        metavar='N',
        help='Max department/institute pages to explore per university (default: 15)'
    )
    
    return parser.parse_args()


def main():
    """Entry point for script execution."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Override AI settings if specified
    use_ai = USE_AI
    if args.no_ai:
        use_ai = False
        client_obj = None
    else:
        client_obj = client
    
    ai_min_score = AI_MIN_SCORE
    if args.ai_score is not None:
        ai_min_score = args.ai_score
        # Validate threshold range
        if not 0.0 <= ai_min_score <= 1.0:
            print(f"❌ Error: AI score threshold must be between 0.0 and 1.0 (got {ai_min_score})")
            sys.exit(1)
    
    # Validate default threshold from environment variable
    if not 0.0 <= ai_min_score <= 1.0:
        print(f"❌ Error: AI_MIN_SCORE in .env must be between 0.0 and 1.0 (got {ai_min_score})")
        sys.exit(1)
    
    # Set AI model
    ai_model = AI_MODEL
    if args.ai_model is not None:
        ai_model = args.ai_model
    
    # Final validation - ensure only allowed models are used
    if ai_model not in VALID_MODELS:
        print(f"❌ Error: AI model must be one of: {', '.join(VALID_MODELS)} (got {ai_model})")
        sys.exit(1)
    
    # Apply exploration depth settings
    from config import MAX_FACULTY_LINKS as CFG_MAX_FACULTY, MAX_DEPARTMENT_LINKS as CFG_MAX_DEPT
    max_faculty = CFG_MAX_FACULTY
    max_dept = CFG_MAX_DEPT
    
    if args.depth is not None:
        # Preset depth levels
        depth_presets = {
            1: {'max_faculty': 20, 'max_dept': 5, 'name': 'Shallow'},
            2: {'max_faculty': 50, 'max_dept': 15, 'name': 'Normal'},
            3: {'max_faculty': 100, 'max_dept': 25, 'name': 'Deep'}
        }
        preset = depth_presets[args.depth]
        max_faculty = preset['max_faculty']
        max_dept = preset['max_dept']
        print(f"🔍 Depth Level {args.depth} ({preset['name']}): "
              f"Faculty={preset['max_faculty']}, Departments={preset['max_dept']}")
    
    # Override with individual settings if specified
    if args.max_faculty_links is not None:
        max_faculty = args.max_faculty_links
        print(f"🔍 Max Faculty Links: {args.max_faculty_links}")
    
    if args.max_department_links is not None:
        max_dept = args.max_department_links
        print(f"🔍 Max Department Links: {args.max_department_links}")
    
    # Apply depth settings to config module
    import config
    config.MAX_FACULTY_LINKS = max_faculty
    config.MAX_DEPARTMENT_LINKS = max_dept
    
    # Prepare university list
    university_urls = None
    
    if args.urls:
        # Custom URLs provided
        university_urls = args.urls
        # Validate URLs
        for url in university_urls:
            if not url.startswith(('http://', 'https://')):
                print(f"❌ Error: Invalid URL '{url}' - must start with http:// or https://")
                sys.exit(1)
    elif args.csv != 'universities.csv' or not os.path.exists('universities.csv'):
        # Custom CSV file specified or default doesn't exist
        if not os.path.exists(args.csv):
            print(f"❌ Error: CSV file '{args.csv}' not found!")
            sys.exit(1)
        
        # Load from custom CSV
        import pandas as pd
        df = pd.read_csv(args.csv)
        required_columns = ['University', 'Website']
        if not all(col in df.columns for col in required_columns):
            print(f"❌ Error: CSV file must contain columns: {', '.join(required_columns)}")
            print(f"   Found columns: {', '.join(df.columns)}")
            sys.exit(1)
        
        # Extract URLs from custom CSV
        university_urls = [row.Website for _, row in df.iterrows() if pd.notna(row.Website)]
        if not university_urls:
            print(f"❌ Error: No valid URLs found in '{args.csv}'")
            sys.exit(1)
    
    # Run the main extraction
    asyncio.run(run_pipeline(
        university_urls=university_urls,
        use_ai=use_ai,
        client=client_obj,
        ai_model=ai_model,
        ai_batch_size=AI_BATCH_SIZE,
        ai_min_score=ai_min_score
    ))


if __name__ == "__main__":
    main()

