"""
HR7 Scan Logger
SQLite storage
"""

import sqlite3
from datetime import datetime

DB_PATH = "storage/scans.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            mac TEXT,
            hostname TEXT,
            scan_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_devices(devices):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for d in devices:
        cur.execute(
            "INSERT INTO devices (ip, mac, hostname, scan_time) VALUES (?,?,?,?)",
            (
                d.get("ip"),
                d.get("mac"),
                d.get("hostname", "Unknown"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

    conn.commit()
    conn.close()

