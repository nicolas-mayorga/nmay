from network.tcp import tcp_connect_scan

def run_tcp_scan(target, ports, timeout):

    for port in ports:
        open = tcp_connect_scan(target, port, timeout)

        if open:
            print(f"{port} OPEN")