from network.tcp import tcp_connect_scan
from concurrent.futures import ThreadPoolExecutor, as_completed

def multithread_tcp_scan(target, ports, timeout, threads=10):
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []

        for port in ports:
            futures.append(executor.submit(tcp_connect_scan, target, port, timeout))

        for future in as_completed(futures):
            port, banner, is_open = future.result()
            print(banner)
            if is_open:
                open_ports.append(port)
    
    return open_ports

def run_tcp_scan(target, ports, timeout):
    open_ports = multithread_tcp_scan(target, ports, timeout)
    
    print(f"{'PORT':<10} {'STATUS':<10} {'SERVICE'}")
    print("=" * 30)
    
    for port in open_ports:
        service = "placeholder" 
        print(f"{str(port) + '/tcp':<10} {'open':<10} {service}")