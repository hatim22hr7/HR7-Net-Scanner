import os
from datetime import datetime


REPORTS_DIR = "reports"


def save_scan_report(devices):
    """
    devices: list of dict
    كل dict فيه: ip, mac, ports (list), os
    """

    # إنشاء مجلد reports إذا ما كانش
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_{timestamp}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)

    with open(filepath, "w") as f:
        f.write(f"HR7 Net Scanner Report\n")
        f.write(f"Scan Date: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        for d in devices:
            f.write(f"IP Address : {d['ip']}\n")
            f.write(f"MAC Address: {d['mac']}\n")
            f.write(f"OS         : {d.get('os', 'Unknown')}\n")

            ports = d.get("ports", [])
            if not ports:
                f.write("Open Ports : None\n")
            else:
                f.write("Open Ports :\n")
                for p in ports:
                    f.write(f"  - {p['port']} ({p['service']})\n")

            f.write("-" * 60 + "\n")

    return filepath

