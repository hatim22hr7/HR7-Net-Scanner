"""
HR7 Network Scanner - Main Entry Point
"""

from utils.config import DEFAULT_TARGET
from core.network_scanner import scan_network
from core.port_scanner import scan_ports
from core.os_detector import detect_os
from gui.main_gui import run_gui

def main_cli():
    """
    نسخة CLI لتجربة المشروع بدون GUI
    """
    print(f"HR7 Network Scanner - Scanning {DEFAULT_TARGET} ...")

    # 1️⃣ اكتشاف الأجهزة
    devices = scan_network(DEFAULT_TARGET)
    print(f"Found {len(devices)} devices.")

    # 2️⃣ تسجيل الأجهزة في قاعدة البيانات
    init_db()
    log_devices(devices)

    # 3️⃣ فحص المنافذ واكتشاف نظام التشغيل
    scan_results = {}
    for d in devices:
        ports = scan_ports(d["ip"])
        scan_results[d["ip"]] = [p["port"] for p in ports]
        os_name = detect_os(ports)
        print(f"\n{d['ip']} - OS: {os_name}")
        if not ports:
            print("  Open Ports: None")
        else:
            for p in ports:
                print(f"  - {p['port']} ({p['service']})")

    # 4️⃣ تحليل الأجهزة والتنبيهات
    alerts = analyze_devices(devices)
    if alerts:
        print("\n⚠ Alerts:")
        for a in alerts:
            print(f"  {a}")

    # 5️⃣ توليد تقرير
    report = ReportGenerator()
    report_path = report.generate_txt_report(DEFAULT_TARGET, scan_results)
    print(f"\nReport saved at: {report_path}")


if __name__ == "__main__":
    # لتشغيل GUI، استعمل run_gui()
    choice = input("Do you want to run GUI? (y/n): ").lower()
    if choice == "y":
        run_gui()
    else:
        main_cli()

