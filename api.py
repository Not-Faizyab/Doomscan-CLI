from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Import your weapons
from core.status import check_status
from core.ports import scan_ports
from core.subdomains import find_subdomains
from core.brute import brute_force_dirs
from core.crawler import crawl_links
from core.tech import fingerprint_tech
from core.wayback import get_ghost_endpoints

app = FastAPI(title="Target Annihilator API")

# This allows your React app to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scan")
def run_scan(target: str):
    """The main trigger point for the React frontend."""
    clean_target = target.replace("http://", "").replace("https://", "").split('/')[0]
    http_target = f"http://{clean_target}"

    # We build the JSON loot object directly to send back to React
    loot = {
        "target": clean_target,
        "scan_time": str(datetime.now()),
        "status": "Unknown",
        "tech_stack": {},
        "open_ports": [],
        "subdomains": [],
        "hidden_directories": [],
        "ghost_endpoints": [],
        "extracted_links": []
    }

    # Phase 1: Status & Tech
    if not check_status(clean_target):
        loot["status"] = "Dead/Unreachable"
        return {"error": "Target is down.", "data": loot}
        
    loot["status"] = "Alive"
    loot["tech_stack"] = fingerprint_tech(http_target)
    
    # Phase 2: Recon
    loot["ghost_endpoints"] = get_ghost_endpoints(clean_target)
    loot["open_ports"] = scan_ports(clean_target)
    loot["subdomains"] = find_subdomains(clean_target)
    loot["hidden_directories"] = brute_force_dirs(http_target)
    loot["extracted_links"] = crawl_links(http_target)

    # Send the massive JSON payload back to the browser
    return {"message": "Annihilation Complete", "data": loot}

if __name__ == "__main__":
    # Start the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)