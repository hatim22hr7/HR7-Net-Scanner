"""
HR7 Port Scanner
"""

import socket
from utils.config import COMMON_PORTS, SOCKET_TIMEOUT


def scan_ports(target_ip):
    open_ports = []

    for port, service in COMMON_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)

        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append({
                "port": port,
                "service": service
            })

        sock.close()

    return open_ports

