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


def get_all_local_subnets():
    subnets = []

    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                netmask = addr.get('netmask')
                if ip and netmask:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    subnets.append(str(network))

    return list(set(subnets))


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

