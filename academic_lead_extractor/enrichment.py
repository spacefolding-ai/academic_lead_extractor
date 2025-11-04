"""
Publication enrichment via Crossref API.
"""

from aiohttp import ClientSession
from typing import Dict, Any


async def enrich_publications(session: ClientSession, contact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch publication URLs via Crossref API.
    Searches by author name and returns up to 5 recent publications.
    """
    name = contact.get("Full_name", "")
    if not name or len(name) < 3:
        contact["Publications"] = []
        return contact
    
    # Try Crossref API
    try:
        url = "https://api.crossref.org/works"
        params = {
            "query.author": name,
            "rows": 5,
            "sort": "issued",
            "order": "desc"
        }
        
        async with session.get(url, params=params, timeout=10, ssl=False) as resp:
            if resp.status == 200:
                data = await resp.json()
                items = data.get("message", {}).get("items", [])
                pubs = []
                
                for item in items:
                    pub_url = item.get("URL")
                    if pub_url:
                        pubs.append(pub_url)
                
                contact["Publications"] = pubs[:5]
                return contact
    except Exception as e:
        # Silently fail - publication enrichment is optional
        pass
    
    contact["Publications"] = []
    return contact

