"""
HR7 Network Scanner
Network discovery using gateway-based scanning
"""

from scapy.all import ARP, Ether, srp
import netifaces
import ipaddress


def get_network_range():
    gateway = netifaces.gateways()['default'][netifaces.AF_INET]
    interface = gateway[1]

    iface_data = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
    ip = iface_data['addr']
    netmask = iface_data['netmask']

    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return str(network)


def scan_network(target_ip=None):
    if target_ip is None:
        target_ip = get_network_range()

    devices = []

    arp_request = ARP(pdst=target_ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered = srp(packet, timeout=2, verbose=0)[0]

    for _, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices

