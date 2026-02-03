import socket

# use TCP (SOCK_STREAM) to connect to a host over a port, and see if it's open
def tcp_connect_scan(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((host, port))
        return True
    except:
        return False
    finally:
        s.close()

        