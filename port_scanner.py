import socket
import threading
from queue import Queue
import time
import argparse

# --- Configuration ---
NUM_THREADS = 100  # Number of concurrent threads
SOCKET_TIMEOUT = 1   # Seconds to wait for a connection attempt
VERBOSE = False      # Print more information during scanning

# --- Global Queue for Ports ---
q = Queue()

# --- Port Scan Function ---
def port_scan(port, target_ip):
    """
    Attempts to connect to a given port on the target IP.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)
        result = sock.connect_ex((target_ip, port))  # connect_ex returns an error indicator

        if result == 0:
            print(f"[+] Port {port} is OPEN")
            if VERBOSE:
                try:
                    service = socket.getservbyport(port)
                    print(f"    Likely service: {service}")
                except OSError:
                    print("    Service: Unknown")
        elif result == 111:  # Connection refused (often means closed)
            if VERBOSE:
                print(f"[-] Port {port} is CLOSED (Connection Refused)")
        else:
            if VERBOSE:
                print(f"[*] Port {port} is FILTERED or other error (Error code: {result})")
    except socket.gaierror:
        print(f"Error: Hostname '{target_ip}' could not be resolved.")
        return
    except socket.error as e:
        if VERBOSE:
            print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()

# --- Worker Function for Threads ---
def worker(target_ip):
    """
    Worker function to fetch ports from the queue and scan them.
    """
    while True:
        port = q.get()
        if port is None:  # Sentinel value to signal thread to exit
            break
        port_scan(port, target_ip)
        q.task_done()

# --- Main Scan Function ---
def run_scanner(target_ip, start_port, end_port):
    """
    Sets up threads and starts the port scanning process.
    """
    print(f"Starting scan on {target_ip} from port {start_port} to {end_port}...")
    start_time = time.time()

    # Create and start worker threads
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(target_ip,))
        t.daemon = True  # Allows the main program to exit even if threads are running
        t.start()
        threads.append(t)

    # Populate the queue with ports
    for port in range(start_port, end_port + 1):
        q.put(port)

    # Wait for all tasks in the queue to be processed
    q.join()

    # Signal threads to exit
    for _ in range(NUM_THREADS):
        q.put(None)
    for t in threads:
        t.join(timeout=SOCKET_TIMEOUT + 1) # Give threads a bit more time to finish

    end_time = time.time()
    print(f"\nScan finished in {end_time - start_time:.2f} seconds.")

# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A basic multithreaded TCP port scanner.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target", help="The target IP address or hostname (e.g., 192.168.1.1, example.com)")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range to scan (e.g., '1-100', '80,443', '1000-2000').\n"
                             "Default: 1-1024")
    parser.add_argument("-t", "--threads", type=int, default=NUM_THREADS,
                        help=f"Number of concurrent threads (default: {NUM_THREADS})")
    parser.add_argument("-T", "--timeout", type=float, default=SOCKET_TIMEOUT,
                        help=f"Socket connection timeout in seconds (default: {SOCKET_TIMEOUT})")
    parser.add_argument("-v", "--verbose", action="store_true", default=VERBOSE,
                        help="Enable verbose output (show closed/filtered ports and services)")

    args = parser.parse_args()

    NUM_THREADS = args.threads
    SOCKET_TIMEOUT = args.timeout
    VERBOSE = args.verbose

    target_ip_or_hostname = args.target

    # Resolve hostname to IP address if needed
    try:
        target_ip = socket.gethostbyname(target_ip_or_hostname)
    except socket.gaierror:
        print(f"Error: Could not resolve hostname: {target_ip_or_hostname}")
        exit(1)

    port_ranges_str = args.ports.split(',')
    all_ports_to_scan = set()

    for r_str in port_ranges_str:
        if '-' in r_str:
            try:
                start, end = map(int, r_str.split('-'))
                if start > end:
                    print(f"Warning: Invalid port range '{r_str}'. Skipping.")
                    continue
                all_ports_to_scan.update(range(start, end + 1))
            except ValueError:
                print(f"Warning: Invalid port range format '{r_str}'. Skipping.")
        else:
            try:
                port = int(r_str)
                all_ports_to_scan.add(port)
            except ValueError:
                print(f"Warning: Invalid single port format '{r_str}'. Skipping.")

    if not all_ports_to_scan:
        print("Error: No valid ports specified for scanning.")
        exit(1)

    min_port = min(all_ports_to_scan)
    max_port = max(all_ports_to_scan)

    # Put ports in order for processing by the queue
    sorted_ports_to_scan = sorted(list(all_ports_to_scan))
    for p in sorted_ports_to_scan:
        q.put(p)

    run_scanner(target_ip, min_port, max_port) # Pass the original min/max for display purposes