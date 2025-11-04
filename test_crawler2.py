#!/usr/bin/env python3
import asyncio
from academic_lead_extractor.scraper import StaffCrawler

async def test():
    crawler = StaffCrawler("https://www.kit.edu")
    await crawler.crawl()
    
    print(f"Total visited: {len(crawler.visited)}")
    print(f"\nURLs containing 'mitarbeitende':")
    mitarbeitende_urls = [url for url in crawler.visited if 'mitarbeitende' in url.lower()]
    for url in mitarbeitende_urls:
        print(f"  - {url}")
    
    print(f"\nURLs containing 'personal':")
    personal_urls = [url for url in crawler.visited if 'personal' in url.lower()]
    for url in personal_urls[:5]:
        print(f"  - {url}")
    
    print(f"\nURLs containing 'kontakt':")
    kontakt_urls = [url for url in crawler.visited if 'kontakt' in url.lower()]
    for url in kontakt_urls[:5]:
        print(f"  - {url}")

asyncio.run(test())

