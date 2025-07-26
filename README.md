Port Scanner

Overview

This project provides a basic, multithreaded TCP port scanner written in Python. It's designed for quickly identifying open TCP ports on a target IP address or hostname using the TCP Connect (full handshake) method. This tool is ideal for straightforward network reconnaissance and learning about network fundamentals.

Features

    Multithreaded Scanning: Uses Python's threading module to perform concurrent port scans, significantly speeding up the process for large port ranges.

    TCP Connect Scan: Establishes a full TCP handshake to accurately determine if a port is open, closed, or filtered.

    Flexible Port Specification:

        Scan a single port (e.g., 80).

        Scan a range of ports (e.g., 1-1024).

        Scan multiple specific ports or ranges (e.g., 80,443,8080-8081).

    Configurable Parameters: Easily adjust the number of threads and the socket timeout to optimize scanning performance and reliability for different network conditions.

    Verbose Output: An optional mode to display more detailed information, including reports for closed or filtered ports and attempts to identify common services associated with open ports.

    Hostname Resolution: Automatically resolves hostnames to their corresponding IP addresses for scanning.

Installation

    Clone the Repository (Recommended):

    (Replace yourusername with your actual GitHub username, or the repository's path.)

    Or, Download the Script:
    Simply download the scanner.py file directly to your desired directory.

No additional Python libraries are required beyond the standard library.

Usage

Run the scanner.py script from your terminal, providing the target IP address or hostname and desired options.

Arguments:

    target: The target IP address or hostname (e.g., 192.168.1.1, example.com). This is a required argument.

    -p, --ports: Specifies the port range to scan.

        Default: 1-1024

        Examples:

            --ports 80 (scans only port 80)

            --ports 1-1000 (scans ports from 1 to 1000)

            --ports 22,80,443,8080-8081 (scans specific ports and ranges)

    -t, --threads: Number of concurrent threads to use for scanning.

        Default: 100

    -T, --timeout: Socket connection timeout in seconds.

        Default: 1.0 (1 second)

    -v, --verbose: Enable verbose output, showing closed/filtered ports and likely services.

Examples:

    Scan common ports on localhost:

    Scan ports 1-500 on example.com:

    Scan specific ports (21, 22, 23, 80, 443) on 192.168.1.100 with verbose output:

    Scan ports 1000-2000 using 500 threads and a 0.5-second timeout:

Important Disclaimer and Ethical Use

Please read carefully:

    Legal & Ethical Responsibility: Port scanning can be a grey area. Always ensure you have explicit permission before scanning any network or device you do not own or administer. Unauthorized port scanning can be illegal and unethical in many jurisdictions.

    Purpose: This tool is intended for educational purposes and for use in authorized security assessments or personal network analysis.

    Detectability: This scanner performs a TCP Connect Scan, which involves a full TCP handshake. This type of scan is generally not stealthy and can be easily detected and logged by firewalls, intrusion detection systems (IDS), and other network security mechanisms.

By using this script, you acknowledge and agree to take full responsibility for its use and to comply with all applicable laws and regulations.
