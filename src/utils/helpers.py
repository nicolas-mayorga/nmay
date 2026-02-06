# contains helper functions 
import json
import socket 

# check if a port contains valid integers (no alphabetic chars etc.)
def is_port_valid(port: int):
    return 1 <= port <= 65535

# check if a list of ports contains only valid ports 
def are_ports_valid(ports):
    for port in ports:
            if not is_port_valid(port):
                raise ValueError(f"Port {port} is invalid.")

    return True

# check if a range is valid (ex: user enters -9999999 9999999, check the range first to avoid building a huge list just for it to be invalid)
def is_range_valid(start, end):
    return 1 <= start <= end <= 65535


# build a list of VALID ports to scan
def get_ports(args):
    ports_to_scan = set() # use set to avoid duplicates

    if not args.port_range and not args.ports:
        ports_to_scan = list(range(1, 65536)) # default to 1-65535 if no ports are specified by user
        return ports_to_scan

    # user provides a port range
    if args.port_range:
        start, end = args.port_range
        if not is_range_valid(start, end):
            raise ValueError("Invalid port range (port range can be 1 - 65535)")
        ports_to_scan.update(range(start, end + 1))

    # user provides specific ports
    if args.ports:
        are_ports_valid(args.ports)
        ports_to_scan.update(args.ports)

    return sorted(ports_to_scan)

def get_tcp_service(port):
    try:
        return socket.getservbyport(port, "tcp")
    except (OSError, socket.error):
        return "unknown"