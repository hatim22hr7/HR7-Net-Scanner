"""
HR7 Network Scanner - Professional Red Theme GUI
Adaptive network detection (Ethernet & Wi-Fi)
"""

import tkinter as tk
import threading
import time

from core.network_scanner import scan_network, get_active_network
from core.port_scanner import scan_ports
from core.os_detector import detect_os
from core.report_manager import save_scan_report


# ===== Colors =====
BG = "#0b0b0b"
RED = "#b30000"
RED_DARK = "#7a0000"
TXT = "#f2f2f2"
GREEN = "#6bff6b"


class HR7ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HR7 Network Scanner")
        self.root.geometry("980x600")
        self.root.configure(bg=BG)

        self.devices = []
        self.stop_loading = threading.Event()
        self.stop_scan = threading.Event()
        self.scanning = False

        # ===== Get active network automatically =====
        try:
            self.target = get_active_network()
        except Exception:
            self.target = "Unknown"
        
        self.build_ui()

    def build_ui(self):
        # ===== Header =====
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(10, 5))

        logo = tk.Canvas(header, width=80, height=60, bg=BG, highlightthickness=0)
        logo.pack(side="left", padx=15)
        self.draw_logo(logo)

        tk.Label(
            header,
            text="HR7 NETWORK SCANNER",
            fg=RED,
            bg=BG,
            font=("Arial Black", 22, "bold")
        ).pack(side="left")

        # ===== Controls =====
        controls = tk.Frame(header, bg=BG)
        controls.pack(fill="x", padx=15, pady=5)

        self.scan_btn = tk.Button(
            controls,
            text="SCAN NETWORK",
            command=self.toggle_scan,
            bg=RED,
            fg=TXT,
            activebackground=RED_DARK,
            activeforeground=TXT,
            relief="flat",
            font=("Arial", 12, "bold"),
            padx=16, pady=6
        )
        self.scan_btn.pack(side="left")

        self.status = tk.Label(
            controls,
            text=f"Target: {self.target}",
            fg="#aaaaaa",
            bg=BG,
            font=("Consolas", 10)
        )
        self.status.pack(side="right")

        # ===== Body =====
        body = tk.Frame(self.root, bg=BG)
        body.pack(expand=True, fill="both", padx=15, pady=10)

        # Left panel
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="DEVICES", fg=RED, bg=BG,
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.listbox = tk.Listbox(
            left,
            width=35,
            height=18,
            bg="#111111",
            fg=TXT,
            selectbackground=RED_DARK,
            font=("Consolas", 11),
            relief="flat"
        )
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right panel
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", expand=True, fill="both")

        tk.Label(right, text="DETAILS", fg=RED, bg=BG,
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.output = tk.Text(
            right,
            bg="#0f0f0f",
            fg=GREEN,
            font=("Consolas", 11),
            relief="flat"
        )
        self.output.pack(expand=True, fill="both", pady=5)

    def draw_logo(self, c):
        nodes = [(20, 30), (40, 10), (60, 30), (40, 50)]
        for x, y in nodes:
            c.create_oval(x-4, y-4, x+4, y+4, fill=RED, outline=RED)

        links = [
            (20, 30, 40, 10), (40, 10, 60, 30),
            (60, 30, 40, 50), (40, 50, 20, 30),
            (20, 30, 60, 30)
        ]
        for l in links:
            c.create_line(*l, fill=RED_DARK)

    # ===== Loading animation =====
    def loading_animation(self):
        symbols = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        i = 0
        while not self.stop_loading.is_set():
            self.status.config(
                text=f"Scanning network ... {symbols[i % len(symbols)]}"
            )
            i += 1
            time.sleep(0.1)

    # ===== Scan control =====
    def toggle_scan(self):
        if not self.scanning:
            self.start_scan()
        else:
            self.stop_scan_process()

    def start_scan(self):
        self.scanning = True
        self.scan_btn.config(text="STOP SCANNING", bg=RED_DARK)

        self.listbox.delete(0, tk.END)
        self.output.delete("1.0", tk.END)

        self.devices = []
        self.stop_loading.clear()
        self.stop_scan.clear()

        threading.Thread(target=self.loading_animation, daemon=True).start()
        threading.Thread(target=self.run_scan, daemon=True).start()

    def stop_scan_process(self):
        self.stop_scan.set()
        self.stop_loading.set()
        self.status.config(text="Scan stopped by user")
        self.scan_btn.config(text="SCAN NETWORK", bg=RED)
        self.scanning = False

    def run_scan(self):
        results = scan_network(self.target)

        for d in results:
            if self.stop_scan.is_set():
                break

            ports = scan_ports(d["ip"])
            os_name = detect_os(ports)

            d["ports"] = ports
            d["os"] = os_name
            self.devices.append(d)

            self.listbox.insert(tk.END, f"{d['ip']}  |  {d['mac']}")

        self.stop_loading.set()
        self.scanning = False

        self.scan_btn.config(text="SCAN NETWORK", bg=RED)

        self.status.config(text=f"Found {len(self.devices)} devices")

        if self.devices:
            save_scan_report(self.devices)
            self.listbox.selection_set(0)
            self.listbox.event_generate("<<ListboxSelect>>")

    # ===== Show details =====
    def on_select(self, event):
        if not self.listbox.curselection():
            return

        d = self.devices[self.listbox.curselection()[0]]

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"IP Address : {d['ip']}\n")
        self.output.insert(tk.END, f"MAC Address: {d['mac']}\n")
        self.output.insert(tk.END, f"OS         : {d.get('os', 'Unknown')}\n")
        self.output.insert(tk.END, "-" * 50 + "\n")

        ports = d.get("ports", [])
        if not ports:
            self.output.insert(tk.END, "Open Ports: None\n")
        else:
            self.output.insert(tk.END, "Open Ports:\n")
            for p in ports:
                self.output.insert(
                    tk.END, f"  - {p['port']} ({p['service']})\n"
                )


def run_gui():
    root = tk.Tk()
    HR7ScannerGUI(root)
    root.mainloop()

