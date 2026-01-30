"""
HR7 OS Detector
Heuristic-based detection
"""

def detect_os(open_ports):
    """
    open_ports: list of dicts [{'port': 80, 'service': 'HTTP'}]
    """

    ports = [p["port"] for p in open_ports]

    if 3389 in ports:
        return "Windows (Probable)"

    if 22 in ports and (80 in ports or 443 in ports):
        return "Linux / Unix (Probable)"

    if 80 in ports and 443 in ports:
        return "Network Device / Router"

    return "Unknown"

