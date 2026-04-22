# Doomscan CLI

`Doomscan-CLI` is a high-density, CLI-based infrastructure reconnaissance utility. It provides automated asset discovery, network interface mapping, and historical path telemetry in a single .txt file.

## Features

* **Infrastructure Fingerprinting:** Identifies server environments, backend frameworks, and missing security headers.
* **Network Interface Mapping:** Scans for exposed TCP/IP ports on the target asset.
* **Subdomain Inventory:** Automated DNS enumeration to discover related infrastructure.
* **Historical Telemetry:** Integrates with the Wayback Machine API to uncover forgotten or hidden endpoints (`?id=`, `/api/`, etc.).

## Installation
Requires Python 3.8+

```bash
pip install -r requirements.txt
python main.py
```

## Usage
1. Input the target domain (e.g., `example.com`) into the command field.
2. Execute the inquiry. The system will retrieve and format the telemetry data in real-time.

## Disclaimer

`Doomscan-CLI` is developed strictly for educational purposes, authorized penetration testing, and defensive infrastructure auditing. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Only execute inquiries against assets you own or have explicit permission to audit. 
