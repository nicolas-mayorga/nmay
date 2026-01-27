import argparse

def main():
    parser = argparse.ArgumentParser(description="Welcome to nmay!")
    
    # Mandatory argument
    parser.add_argument("target", help="IP/Hostname to scan", )

    # Flags (optional)
    parser.add_argument("-pr", "--port-range", help="Ports to scan, space delimited (ex. 1 1024))", type=int, nargs=2, metavar=("START", "END"))
    parser.add_argument("-p", "--ports", help="Port(s) to scan, space delimited (ex: 22 80 443)", type=int, nargs="+")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Timeout in seconds")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", type=str, default="nmay.out")
    parser.add_argument("-sS", "--syn-scan", action="store_true", help="Perform TCP SYN scan")
    parser.add_argument("-sU", "--udp-scan", action="store_true", help="Scan UDP ports")
    parser.add_argument("-sD", "--service-detect", action="store_true", help="Try to identify running services on open ports")
    parser.add_argument("-s", "--safe", action="store_true", help="Scan only non-critical ports")
    parser.add_argument("-r", "--rate-limit", action="store_true", help="Prevent flooding")

    args = parser.parse_args()

    # create list of ports to scan from passed arguments
    ports_to_scan = []

    if not args.port_range and not args.ports:
        ports_to_scan = list(range(1, 65536))

    else:
        if args.port_range:
            start, end = args.port_range
            if (start < 1 or end < 1):
                parser.error("ports cannot be negative")
                exit()
            if (start > 65535 or end > 65535):
                parser.error("invalid port(s)")
                exit()
            if start > end:
                parser.error("start port must be <= end port")
                exit()

            for i in range(start, end + 1):
                ports_to_scan.append(i)


        if args.ports:
            for port in args.ports:
                try:
                    if port <= 0 or port > 65535:
                        raise ValueError(f"{port} is not 1-65535")

                    if port not in ports_to_scan:
                        ports_to_scan.append(port)

                except ValueError:
                    parser.error("invalid port(s), all ports must be in the range 1-65535")


    print(f"Scanning {args.target}\nPort(s): {ports_to_scan}\nTimeout: {args.timeout}\nRate Limited: {args.rate_limit}")