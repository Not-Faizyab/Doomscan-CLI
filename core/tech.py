import requests

def fingerprint_tech(target):
    """Interrogates server headers to identify the tech stack and missing security."""
    if not target.startswith("http"):
        target = f"http://{target}"
        
    try:
        response = requests.get(target, timeout=5)
        headers = response.headers
        
        tech_data = {
            "Server": headers.get("Server", "Unknown"),
            "Powered_By": headers.get("X-Powered-By", headers.get("X-Generator", "Unknown")),
            "Missing_Sec_Headers": []
        }
        
        # Checking for critical security headers
        critical_headers = ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options', 'Content-Security-Policy']
        for header in critical_headers:
            if header not in headers:
                tech_data["Missing_Sec_Headers"].append(header)
                
        return tech_data
    except requests.exceptions.RequestException:
        return None