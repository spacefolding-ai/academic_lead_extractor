"""
Main pipeline for processing universities and extracting contacts.
"""

import asyncio
import os
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
               ai_batch_size=20, ai_min_score=0.5):
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
    # Create session with proper SSL handling and connector
    connector = aiohttp.TCPConnector(ssl=False, limit=100)
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    async with ClientSession(connector=connector, headers=HEADERS, timeout=timeout) as session:
        with tqdm(total=len(universities), desc="🔍 Scanning universities") as pbar:
            for i in range(0, len(universities), UNI_PARALLEL):
                batch = universities[i:i + UNI_PARALLEL]
                # Pass AI parameters for link discovery
                tasks = [process_university(session, uni, pbar, use_ai, client, ai_model) for uni in batch]
                results = await asyncio.gather(*tasks)
                
                for contacts in results:
                    all_contacts.extend(contacts)
    
    print(f"\n✅ Extracted {len(all_contacts)} raw contacts")
    
    # STEP 2: AI evaluation (V3 logic)
    evaluated_contacts = await ai_evaluate_contacts(
        all_contacts, use_ai, client, ai_model, ai_batch_size, ai_min_score
    )
    
    # STEP 3: Filter by score
    if use_ai:
        final_contacts = [c for c in evaluated_contacts if c.get("AI_Score", 0) >= ai_min_score]
        print(f"✅ {len(final_contacts)} contacts passed AI threshold ({ai_min_score})")
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
            "Full_name", "Email", "Title_role", "AI_Field", "AI_Score", "AI_Reason",
            "University", "Country", "University_Website_URL", "Source_URL", "Publications"
        ]
        
        filename = os.path.join(output_dir, f"{country}.csv")
        df.to_csv(filename, sep=";", index=False, columns=columns)
        print(f"✅ {country}: {len(df)} contacts → {filename}")
        total_saved += len(df)
    
    print(f"\n🎉 TOTAL: {total_saved} contacts across {len(by_country)} countries")
    print(f"💾 Results saved to: {output_dir}/")

