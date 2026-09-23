"""JARVIS detection loop.

Reads the Windows ARP table, compares each device on the hotspot against the
`device` table in SQLite, and classifies it:

    new device   -> insert as 'unknown'  -> ALERT
    known device -> update last_seen     -> no alert

This is the diamond in the detection flowchart, in code. The event and alert
tables in docs/schema.sql come online when alerting is built; this first
increment only touches the `device` table.
"""

import subprocess
import re
import sqlite3
from datetime import datetime, timezone

DB = "jarvis.db"
HOTSPOT_PREFIX = "192.168.137."


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def init_db() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS device (
            id          INTEGER PRIMARY KEY,
            mac         TEXT NOT NULL UNIQUE,
            vendor      TEXT,
            name        TEXT,
            status      TEXT NOT NULL DEFAULT 'unknown'
                        CHECK (status IN ('registered', 'unknown', 'ignored')),
            randomised  INTEGER NOT NULL DEFAULT 0,
            first_seen  TEXT NOT NULL,
            last_seen   TEXT NOT NULL,
            last_ip     TEXT
        )
    """)
    con.commit()
    return con


def read_arp() -> list[tuple[str, str, bool]]:
    """Return (mac, ip, randomised) for real devices on the hotspot."""
    out = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout
    pat = re.compile(r"(192\.168\.137\.\d+)\s+([\da-fA-F]{2}(?:[-:][\da-fA-F]{2}){5})")
    devices = []
    for ip, mac in pat.findall(out):
        last_octet = int(ip.split(".")[-1])
        if last_octet in (0, 255) or mac.lower().startswith("ff"):
            continue
        randomised = int(mac[1], 16) & 0b10 != 0  # locally-administered bit
        devices.append((mac.lower(), ip, randomised))
    return devices


def scan(con: sqlite3.Connection) -> None:
    for mac, ip, randomised in read_arp():
        row = con.execute("SELECT status FROM device WHERE mac = ?", (mac,)).fetchone()
        if row is None:
            con.execute(
                "INSERT INTO device (mac, status, randomised, first_seen, last_seen, last_ip) "
                "VALUES (?, 'unknown', ?, ?, ?, ?)",
                (mac, int(randomised), now(), now(), ip),
            )
            print(f"  NEW      {ip:<16} {mac}  ->  ALERT (unregistered)")
        else:
            con.execute(
                "UPDATE device SET last_ip = ?, last_seen = ? WHERE mac = ?",
                (ip, now(), mac),
            )
            print(f"  known    {ip:<16} {mac}  ({row[0]})")
    con.commit()


if __name__ == "__main__":
    con = init_db()
    print("Scanning hotspot...\n")
    scan(con)
    print("\nDone.")
