import json
from datetime import datetime

def save_json_report(target, recon_data):
    """Compiles all gathered intel into a structured JSON file."""
    # Get current time to make a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{target}_recon_{timestamp}.json"
    
    try:
        with open(filename, "w") as f:
            # indent=4 makes the JSON readable instead of one giant block of text
            json.dump(recon_data, f, indent=4) 
        return filename
    except Exception as e:
        print(f"[-] Error saving report: {e}")
        return None