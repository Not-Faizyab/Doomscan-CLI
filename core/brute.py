import requests
import concurrent.futures

def check_directory(url):
    """Hits a single URL to see if it exists."""
    try:
        # We use a custom User-Agent so we don't look like a basic python bot
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=3)
        
        # 200 = OK, 403 = Forbidden (but it exists!)
        if response.status_code in [200, 403]:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

def brute_force_dirs(target):
    """Brute forces common directories using multithreading."""
    # Ensure URL is formatted correctly
    if not target.startswith("http"):
        target = f"http://{target}"
        
    # Small, lethal wordlist for speed
    directories = [
        'admin', 'login', 'dashboard', 'api', 'backup', 'dev', 'test', 'staging', 
        'robots.txt', '.git', 'config', 'uploads', 'assets', 'css', 'js', 'images'
    ]
    
    found_dirs = []
    
    # Spinning up 10 threads to rapid-fire requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # We build the full URL (e.g., http://target.com/admin) and submit it
        futures = {executor.submit(check_directory, f"{target}/{dir_name}"): dir_name for dir_name in directories}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found_dirs.append(result)
                
    return sorted(found_dirs)