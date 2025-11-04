#!/usr/bin/env python3
"""
Direct crawler test to debug why no contacts are extracted.
"""

import asyncio
import aiohttp
from academic_lead_extractor.scraper import StaffCrawler

async def test_crawl():
    url = "https://www.kit.edu"
    print(f"Testing crawler on: {url}")
    print("=" * 80)
    
    crawler = StaffCrawler(url)
    contacts = await crawler.crawl()
    
    print(f"\n📊 Crawl Statistics:")
    print(f"   Visited pages: {len(crawler.visited)}")
    print(f"   Staff pages found: {len(crawler.found_pages)}")
    print(f"   Contacts extracted: {len(contacts)}")
    
    if crawler.found_pages:
        print(f"\n✅ Staff pages detected:")
        for page in crawler.found_pages[:5]:
            print(f"   - {page}")
    else:
        print(f"\n⚠️  No staff pages detected")
        print(f"   Visited URLs (first 10):")
        for visited_url in list(crawler.visited)[:10]:
            print(f"   - {visited_url}")
    
    if contacts:
        print(f"\n✅ Sample contacts:")
        for contact in contacts[:3]:
            print(f"   - {contact.get('Full_name')} <{contact.get('Email')}>")
    
    return contacts

if __name__ == "__main__":
    contacts = asyncio.run(test_crawl())

