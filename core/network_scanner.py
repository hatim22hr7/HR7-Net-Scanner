"""
HR7 Network Scanner
True interface-based network discovery (ETH / WLAN)
"""

from scapy.all import ARP, Ether, srp
import netifaces
import ipaddress


def get_active_network():
    """
    Returns the real connected network (CIDR) from any active interface
    """
    for iface in netifaces.interfaces():
        # تجاهل loopback
        if iface == "lo":
            continue

        addrs = netifaces.ifaddresses(iface)

        if netifaces.AF_INET not in addrs:
            continue

        for addr in addrs[netifaces.AF_INET]:
            ip = addr.get("addr")
            netmask = addr.get("netmask")

            if not ip or not netmask:
                continue

            # تجاهل APIPA
            if ip.startswith("169.254"):
                continue

            try:
                network = ipaddress.IPv4Network(
                    f"{ip}/{netmask}", strict=False
                )
                return str(network)
            except Exception:
                continue

    raise RuntimeError("No active Ethernet/WLAN network detected")


def scan_network(target_ip=None):
    if target_ip is None:
        target_ip = get_active_network()

    devices = []

    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered = srp(packet, timeout=2, verbose=0)[0]

    for _, rcv in answered:
        devices.append({
            "ip": rcv.psrc,
            "mac": rcv.hwsrc
        })

    return devices

