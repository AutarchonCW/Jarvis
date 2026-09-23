# Development log

Newest entries at the top. One entry per working session. Record what was
done, what was decided, and what was learned — especially things that
changed the plan. This log is portfolio evidence of individual, incremental
work; keep it honest, including dead ends.

---

## 2026-09-18 — Detection spike works end to end

**Done**
- Set up project: `C:\Dev\jarvis`, Python 3.14 venv, Git repo.
- Installed scapy, fastapi, uvicorn. `from scapy.all import sniff` imports
  cleanly on 3.14 (pre-built wheels, no build errors).
- Confirmed Windows Mobile hotspot uses the `192.168.137.x` range with the
  laptop as gateway/DHCP at `192.168.137.1`.
- Wrote `spikes/read_arp.py`: reads the Windows ARP table, filters to the
  hotspot range, drops broadcast/multicast, flags randomised MACs.

**Result**
- Phone (S25 Ultra) detected as `192.168.137.246`, MAC `aa-cd-0e-1d-ed-cf`,
  correctly flagged as a randomised MAC.

**Learned / decisions**
- Live Scapy sniffing on the Windows hotspot virtual adapter is unreliable
  (wrong default interface, quiet ARP once devices know the gateway). The
  Windows ARP table is a robust alternative and gives MAC+IP directly, which
  is all the schema needs. **Decision: build the PoC detection loop on the
  ARP table; keep live capture as a documented "next step", not a blocker.**
- ARP entries here are typed `static`, not `dynamic` — do not filter on the
  type word, filter on the address range.
- The phone uses a randomised (locally-administered) MAC. This is the exact
  case the schema was designed for: an "unknown" device is not always an
  unfamiliar one. Belongs in the limitations section.

**Next**
- `detect.py`: read ARP -> compare against `device` table -> insert new as
  `unknown` (alert), update last_seen for known (no alert).
- Add a "register this device" action (flip status to `registered`).
- Then: FastAPI endpoint exposing the device list.

---

## 2026-09-17 — Environment and tooling

**Done**
- Installed Wireshark (+ Npcap), Python, Git, VS Code, Android Studio,
  DB Browser for SQLite. Arduino IDE still to install (needed later, not now).
- Chose to run the PoC on the laptop's own Wi-Fi hotspot rather than an
  external router — a network I own outright, avoids capturing on the Fontys
  campus network (policy), and makes the laptop the gateway so all client
  traffic is visible.

**Learned**
- Hotspot must be 2.4 GHz: the ESP32 has no 5 GHz radio.
- Being the access point means JARVIS is the gateway, not a passive peer on a
  shared segment. Detection logic is identical; network position is not.
  Document as a limitation (same shape as laptop-vs-Pi).
