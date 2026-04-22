import argparse
from datetime import datetime
from core.status import check_status
from core.ports import scan_ports
from core.subdomains import find_subdomains
from core.brute import brute_force_dirs
from core.crawler import crawl_links
from core.tech import fingerprint_tech
from core.wayback import get_ghost_endpoints
from utils.report import save_json_report

def display_banner():
    print("\n[+]====================================[+]")
    print("[+]      TARGET ANNIHILATOR v2.0       [+]")
    print("[+]        DEEP RECON EDITION          [+]")
    print("[+]====================================[+]\n")

def main():
    parser = argparse.ArgumentParser(description="Massive Reconnaissance Framework")
    parser.add_argument("-t", "--target", help="Target domain (e.g., example.com)", required=True)
    
    args = parser.parse_args()
    target = args.target
    clean_target = target.replace("http://", "").replace("https://", "").split('/')[0]
    http_target = f"http://{clean_target}"

    display_banner()

    master_data = {
        "target": clean_target,
        "scan_time": str(datetime.now()),
        "status": "Unknown",
        "tech_stack": {},
        "open_ports": [],
        "subdomains": [],
        "hidden_directories": [],
        "extracted_links": [],
        "ghost_endpoints": []
    }

    # --- PHASE 1: STATUS & TECH STACK ---
    print(f"[*] Checking status for {clean_target}...")
    if not check_status(clean_target):
        print("[-] Target is down. Aborting mission. 💀")
        master_data["status"] = "Dead/Unreachable"
        save_json_report(clean_target, master_data)
        return
        
    print("[+] Target is ALIVE.")
    master_data["status"] = "Alive"
    
    print(f"[*] Fingerprinting Tech Stack...")
    tech = fingerprint_tech(http_target)
    if tech:
        print(f"    - Server: {tech['Server']}")
        print(f"    - Powered By: {tech['Powered_By']}")
        print(f"    - Missing Sec Headers: {len(tech['Missing_Sec_Headers'])}")
        master_data["tech_stack"] = tech
    print()

    # --- PHASE 2: PASSIVE GHOST RECON ---
    print(f"[*] Querying Wayback Machine for hidden endpoints...")
    ghosts = get_ghost_endpoints(clean_target)
    if ghosts:
        print(f"[+] Found {len(ghosts)} historical/hidden parameters:")
        master_data["ghost_endpoints"] = ghosts
        for g in ghosts[:3]:
            print(f"    - {g}")
        print("    - (Full list in report)\n")
    else:
        print("[-] No juicy ghost endpoints found.\n")

    # --- PHASE 3: PORTS ---
    print(f"[*] Scanning ports on {clean_target}...")
    open_ports = scan_ports(clean_target)
    if open_ports:
        print(f"[+] Found open ports: {open_ports}\n")
        master_data["open_ports"] = open_ports
    else:
        print("[-] No common ports open.\n")

    # --- PHASE 4: SUBDOMAINS ---
    print(f"[*] Hunting subdomains for {clean_target}...")
    subdomains = find_subdomains(clean_target)
    if subdomains:
        print(f"[+] Discovered {len(subdomains)} subdomains. (List in report)\n")
        master_data["subdomains"] = subdomains
    else:
        print("[-] No common subdomains found.\n")

    # --- PHASE 5: DIRECTORY BRUTE-FORCING ---
    print(f"[*] Brute-forcing hidden directories on {http_target}...")
    directories = brute_force_dirs(http_target)
    if directories:
        print(f"[+] Discovered {len(directories)} endpoints. (List in report)\n")
        master_data["hidden_directories"] = directories
    else:
        print("[-] No common hidden directories found.\n")

    # --- PHASE 6: GENERATE REPORT ---
    print("[*] Compiling Deep Intelligence Report...")
    report_file = save_json_report(clean_target, master_data)

    print("\n[+]====================================[+]")
    print("[+]        RECONNAISSANCE COMPLETE     [+]")
    if report_file:
        print(f"[+]   LOOT SAVED: {report_file} ")
    print("[+]====================================[+]\n")

if __name__ == "__main__":
    main()