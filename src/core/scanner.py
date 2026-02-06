from network.tcp import tcp_connect_scan
from concurrent.futures import ThreadPoolExecutor, as_completed
import utils.helpers
from core.gemini_client import GeminiClient

def multithread_tcp_scan(target, ports, timeout, threads=10):
    open_ports = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []

        for port in ports:
            futures.append(executor.submit(tcp_connect_scan, target, port, timeout))

        for future in as_completed(futures):
            port, banner, is_open = future.result()
            
            if is_open:
                open_ports[port] = ""
                if not banner == "No banner":
                    open_ports[port] = banner
            
    return open_ports

def run_tcp_scan(target, ports, timeout, banners):
    open_ports = multithread_tcp_scan(target, ports, timeout)
    use_ai = True
    gemini = GeminiClient()
        
    print(f"{'PORT':<10} {'STATUS':<10} {'SERVICE'}")
    print("=" * 30)
        
    for port in open_ports:

        service = utils.helpers.get_tcp_service(port)
        
        print(f"{str(port) + '/tcp':<10} {'open':<10} {service}")
        
        if not open_ports.get(port) == "":
            print(open_ports.get(port))
            response = gemini.gemini_response(service, port, open_ports.get(port))
            print(response)