import requests

def get_ghost_endpoints(target):
    """Pulls historical, hidden, or deleted URLs from the Wayback Machine API."""
    # We ask the API for up to 100 historical URLs for this domain
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{target}/*&output=json&collapse=urlkey&limit=100"
    
    try:
        # 10 second timeout because the archive can be slow
        response = requests.get(url, timeout=10) 
        data = response.json()
        
        ghost_urls = set()
        
        # The API returns a list of lists. Row 0 is headers, data starts at Row 1.
        if len(data) > 1:
            for row in data[1:]:
                original_url = row[2]
                # Filter for juicy targets: parameters or API routes
                if '?' in original_url or '.php' in original_url or '/api/' in original_url:
                    ghost_urls.add(original_url)
                    
        return list(ghost_urls)[:10] # Return the top 10 juiciest endpoints
    except Exception:
        return []