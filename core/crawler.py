import requests
import re

def crawl_links(target):
    """Scrapes the homepage and extracts all hyperlinks."""
    if not target.startswith("http"):
        target = f"http://{target}"
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target, headers=headers, timeout=5)
        
        # Regex magic to find everything inside href="..."
        raw_links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        
        clean_links = set() # Using a set automatically removes duplicates
        
        for link in raw_links:
            # If it's a full URL, keep it
            if link.startswith('http'):
                clean_links.add(link)
            # If it's a relative path (like /about), attach it to the target domain
            elif link.startswith('/'):
                clean_links.add(target + link)
                
        # Return only the first 15 links so we don't flood your terminal later
        return sorted(list(clean_links))[:15] 
        
    except requests.exceptions.RequestException:
        return []