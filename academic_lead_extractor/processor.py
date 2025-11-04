"""
Main pipeline for processing universities and extracting contacts.
"""

import asyncio
import os
import time
import pandas as pd
import aiohttp
from aiohttp import ClientSession
from tqdm import tqdm
from collections import defaultdict
from urllib.parse import urlparse

from config import UNI_PARALLEL, HEADERS
from academic_lead_extractor.scraper import process_university
from academic_lead_extractor.ai_evaluator import ai_evaluate_contacts
from academic_lead_extractor.enrichment import enrich_publications


async def main(university_urls=None, use_ai=True, client=None, ai_model="gpt-4o-mini",
               ai_batch_size=20, ai_min_score=0.5, use_ai_profile_detection=False):
    """Main pipeline for academic lead extraction."""
    # Validate AI score threshold
    if not 0.0 <= ai_min_score <= 1.0:
        raise ValueError(f"ai_min_score must be between 0.0 and 1.0, got {ai_min_score}")
    
    # Load universities from CSV or command-line arguments
    if university_urls:
        # Custom URLs provided via command line
        universities = []
        for idx, url in enumerate(university_urls, 1):
            # Try to extract university name from domain
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')
            uni_name = domain.split('.')[0].title() if domain else f"University_{idx}"
            
            universities.append({
                "country": "Custom",
                "name": uni_name,
                "url": url
            })
        
        print(f"\n🎯 Processing {len(universities)} custom URL(s)")
        print(f"🔍 URLs: {', '.join(university_urls[:3])}{'...' if len(university_urls) > 3 else ''}")
    else:
        # Load from universities.csv
        if not os.path.exists("universities.csv"):
            print("❌ Error: universities.csv not found!")
            print("   Please provide either:")
            print("   1. universities.csv file in current directory")
            print("   2. Custom URLs using --urls argument")
            return
        
        df = pd.read_csv("universities.csv")
        universities = [
            {"country": row.Country, "name": row.University, "url": row.Website}
            for _, row in df.iterrows() if pd.notna(row.Website)
        ]
        
        print(f"\n🎯 Loaded {len(universities)} universities from universities.csv")
    
    print(f"🔍 Exploration: Aggressive (subdomains + departments)")
    
    # STEP 1: Scrape all contacts (V2 logic)
    all_contacts = []
    university_times = {}  # Track time per university
    total_scraping_time = 0
    
    # Create session with proper SSL handling and connector
    connector = aiohttp.TCPConnector(ssl=False, limit=100)
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    scraping_start = time.time()
    
    async with ClientSession(connector=connector, headers=HEADERS, timeout=timeout) as session:
        with tqdm(total=len(universities), desc="🔍 Scanning universities") as pbar:
            for i in range(0, len(universities), UNI_PARALLEL):
                batch = universities[i:i + UNI_PARALLEL]
                # Track time for each university in batch
                batch_start = time.time()
                
                # Pass AI parameters for link discovery and profile detection
                tasks = [process_university(session, uni, pbar, use_ai, client, ai_model, use_ai_profile_detection) for uni in batch]
                results = await asyncio.gather(*tasks)
                
                batch_elapsed = time.time() - batch_start
                
                # Assign time to each university in batch (approximation for parallel execution)
                for uni, contacts in zip(batch, results):
                    uni_name = uni.get("name", "Unknown")
                    university_times[uni_name] = {
                        "time": batch_elapsed / len(batch),  # Approximate time per uni
                        "contacts": len(contacts)
                    }
                    all_contacts.extend(contacts)
    
    total_scraping_time = time.time() - scraping_start
    
    print(f"\n✅ Extracted {len(all_contacts)} raw contacts")
    print(f"⏱️  Scraping time: {total_scraping_time:.1f}s ({total_scraping_time/60:.1f}min)")
    
    # Display per-university timing
    if university_times:
        print(f"\n📊 Per-University Extraction Times:")
        sorted_unis = sorted(university_times.items(), key=lambda x: x[1]["time"], reverse=True)
        for uni_name, stats in sorted_unis[:10]:  # Show top 10 slowest
            print(f"   {uni_name:40s}: {stats['time']:6.1f}s → {stats['contacts']} contacts")
        if len(sorted_unis) > 10:
            print(f"   ... and {len(sorted_unis) - 10} more universities")
    
    # STEP 2: AI evaluation (V3 logic)
    ai_start = time.time()
    evaluated_contacts, token_stats = await ai_evaluate_contacts(
        all_contacts, use_ai, client, ai_model, ai_batch_size, ai_min_score
    )
    ai_time = time.time() - ai_start
    
    # STEP 3: Filter by score
    if use_ai:
        final_contacts = [c for c in evaluated_contacts if c.get("AI_Score", 0) >= ai_min_score]
        print(f"✅ {len(final_contacts)} contacts passed AI threshold ({ai_min_score})")
        print(f"⏱️  AI evaluation time: {ai_time:.1f}s ({ai_time/60:.1f}min)")
    else:
        final_contacts = evaluated_contacts
    
    # STEP 4: Enrich with publications (Crossref API)
    if final_contacts:
        print(f"📚 Enriching {len(final_contacts)} contacts with publications...")
        async with ClientSession() as session:
            enrichment_tasks = [enrich_publications(session, contact) for contact in final_contacts]
            final_contacts = await asyncio.gather(*enrichment_tasks)
        
        pub_count = sum(1 for c in final_contacts if c.get("Publications") and len(c["Publications"]) > 0)
        print(f"✅ Found publications for {pub_count}/{len(final_contacts)} contacts")
    
    # STEP 5: Save by country
    by_country = defaultdict(list)
    for c in final_contacts:
        by_country[c["Country"]].append(c)
    
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    total_saved = 0
    for country, contacts in by_country.items():
        # Normalize column name BEFORE creating DataFrame (scraper uses source_url, but we want Source_URL in output)
        for contact in contacts:
            if "source_url" in contact and "Source_URL" not in contact:
                contact["Source_URL"] = contact["source_url"]
        
        df = pd.DataFrame(contacts)
        df = df.drop_duplicates(subset=["Email"], keep="first")
        
        # Format Publications as comma-separated string for better CSV readability
        if "Publications" in df.columns:
            df["Publications"] = df["Publications"].apply(lambda x: ", ".join(x) if isinstance(x, list) and x else "")
        
        columns = [
            "Full_name", "Email", "Title", "Role", "AI_Field", "AI_Score", "AI_Reason",
            "University", "Country", "University_Website_URL", "Source_URL", "Publications"
        ]
        
        # Ensure all expected columns exist (add empty columns if missing)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        
        filename = os.path.join(output_dir, f"{country}.csv")
        df.to_csv(filename, sep=";", index=False, columns=columns)
        print(f"✅ {country}: {len(df)} contacts → {filename}")
        total_saved += len(df)
    
    # Calculate total pipeline time
    total_pipeline_time = total_scraping_time + ai_time
    
    print(f"\n🎉 TOTAL: {total_saved} contacts across {len(by_country)} countries")
    print(f"💾 Results saved to: {output_dir}/")
    
    # Final summary with timing and costs
    print(f"\n" + "="*70)
    print(f"📈 EXTRACTION SUMMARY")
    print(f"="*70)
    print(f"🎯 Universities processed:     {len(universities)}")
    print(f"📧 Total contacts extracted:   {len(all_contacts)}")
    print(f"✅ Contacts after filtering:   {total_saved}")
    print(f"\n⏱️  TIMING BREAKDOWN:")
    print(f"   Scraping time:              {total_scraping_time:.1f}s ({total_scraping_time/60:.1f}min)")
    print(f"   AI evaluation time:         {ai_time:.1f}s ({ai_time/60:.1f}min)")
    print(f"   Total pipeline time:        {total_pipeline_time:.1f}s ({total_pipeline_time/60:.1f}min)")
    print(f"   Avg time per university:    {total_scraping_time/len(universities):.1f}s")
    
    if use_ai and token_stats["total_tokens"] > 0:
        print(f"\n💰 AI TOKEN USAGE & COST:")
        print(f"   Input tokens:               {token_stats['input_tokens']:,}")
        print(f"   Output tokens:              {token_stats['output_tokens']:,}")
        print(f"   Total tokens:               {token_stats['total_tokens']:,}")
        print(f"   Estimated cost:             ${token_stats['estimated_cost']:.4f} USD")
        print(f"   Model used:                 {ai_model}")
        print(f"   Cost per contact:           ${token_stats['estimated_cost']/max(1, total_saved):.4f}")
    
    print(f"="*70)

