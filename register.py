import sys
import sqlite3

DB = "jarvis.db"

if len(sys.argv) < 2:
    print("usage: python register.py <mac> [name]")
    sys.exit(1)

mac = sys.argv[1].lower()
name = sys.argv[2] if len(sys.argv) > 2 else None

con = sqlite3.connect(DB)
cur = con.execute(
    "UPDATE device SET status = 'registered', name = COALESCE(?, name) WHERE mac = ?",
    (name, mac),
)
con.commit()

if cur.rowcount:
    print(f"Registered {mac}" + (f" as '{name}'" if name else ""))
else:
    print(f"No device with MAC {mac} - run detect.py first")
    