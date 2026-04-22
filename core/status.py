import requests

def check_status(target):
    if not target.startswith("http"):
        target = f"http://{target}"
        
    try:
        # 5-second timeout so a dead site doesn't freeze your terminal
        response = requests.get(target, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False