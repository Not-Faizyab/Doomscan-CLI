import socket
import concurrent.futures

def scan_single_port(target, port):
    """Attempts to connect to a single port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # 1 second timeout so it doesn't hang
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except socket.error:
        pass
    return None

def scan_ports(target):
    """Scans common ports using multithreading."""
    # Top 20 common ports for speed
    common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    open_ports = []

    # Using 10 workers to scan 10 ports at the exact same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_single_port, target, port): port for port in common_ports}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                
    return sorted(open_ports)