import socket

# use TCP (SOCK_STREAM) to connect to a host over a port, and see if it's open
def tcp_connect_scan(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    is_open = False
    banner = ""
    try:
        is_open = not s.connect_ex((host, port))
        banner = s.recv(1024).decode(errors='ignore').strip() # check to see if there's a banner on the open port
        

        if not banner:
            s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n") # if not, send a generic http request to see if anything happens
            banner = s.recv(1024).decode(errors='ignore').strip()
        
    except:
        banner = "Unknown/no banner"
    finally:
        s.close()
    return port, banner, is_open
        