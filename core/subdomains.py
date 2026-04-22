import socket
import concurrent.futures

def check_subdomain(subdomain, target):
    """Attempts to resolve the IP of a subdomain."""
    full_domain = f"{subdomain}.{target}"
    try:
        # If DNS resolves it, the subdomain exists
        socket.gethostbyname(full_domain)
        return full_domain
    except socket.error:
        return None

def find_subdomains(target):
    """Hunts for subdomains using a fast wordlist and multithreading."""
    # Mini wordlist for speed - we can make this massive later
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 
        'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 
        'new', 'mysql', 'old', 'vps', 'app', 'shop', 'api', 'portal', 'secure'
    ]
    found = []
    
    # 20 threads hammering the DNS records
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_subdomain, sub, target): sub for sub in subdomains}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found.append(result)
                
    return sorted(found)