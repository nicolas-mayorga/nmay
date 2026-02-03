import argparse
from core.scanner import run_tcp_scan
from utils.helpers import *


def main():
    parser = argparse.ArgumentParser(description="Welcome to nmay!")
    
    # Mandatory argument
    parser.add_argument("target", help="IP/Hostname to scan", )

    # Flags (optional)
    parser.add_argument("-pr", "--port-range", help="Ports to scan, space delimited (ex. 1 1024))", type=int, nargs=2, metavar=("START", "END"))
    parser.add_argument("-p", "--ports", help="Port(s) to scan, space delimited (ex: 22 80 443)", type=int, nargs="+")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Timeout in seconds")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-sS", "--syn-scan", action="store_true", help="Perform TCP SYN scan")
    parser.add_argument("-sU", "--udp-scan", action="store_true", help="Scan UDP ports")
    parser.add_argument("-sD", "--service-detect", action="store_true", help="Try to identify running services on open ports")
    parser.add_argument("-s", "--safe", action="store_true", help="Scan only non-critical ports")
    parser.add_argument("-r", "--rate-limit", action="store_true", help="Prevent flooding")

    args = parser.parse_args();

    # create list of ports to scan from passed arguments
    try:
        ports_to_scan = get_ports(args)
    except ValueError as e:
        parser.error(e)

    print(f"Scanning {args.target}\nPort(s): {ports_to_scan}\nTimeout: {args.timeout}\nRate Limited: {args.rate_limit}")

    run_tcp_scan(args.target, ports_to_scan, args.timeout)
