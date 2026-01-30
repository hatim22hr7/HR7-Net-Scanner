"""
HR7 Net Scanner - Configuration File
"""

# الشبكة الافتراضية
DEFAULT_TARGET = "192.168.1.0/24"

# Timeout عام (بالثواني)
SOCKET_TIMEOUT = 0.5

# أشهر المنافذ (Top Ports)
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NETBIOS",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}

# MAC Blacklist (للتجربة)
BLACKLIST_MACS = [
    "00:11:22:33:44:55"
]

