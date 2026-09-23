# Technology decisions

The full, referenced justification lives in the analysis document
(`Analyses JARVIS PROJECT`). This file is the short in-repo version, plus any
decision made during development that post-dates that document.

Every choice is judged against: fitness for purpose, time-to-working-increment
(four weeks, one developer), transparency of mechanism (a learning project),
alignment with the human-in-the-loop principle, and cost/availability.

| Area | Chosen | Over | One-line reason |
|---|---|---|---|
| Backend language | Python | Java, C#, Node.js | Library fit (Scapy, SQLite, FastAPI) + fast delivery |
| Discovery | ARP table / Scapy | Nmap | Passive; no active probing (see principle) |
| Traffic verification | Wireshark | tcpdump | GUI decode shortens the debug loop |
| API | FastAPI | Flask | Validation + OpenAPI docs from the same source |
| Host | Laptop hotspot | Router / Pi | Owned network, laptop is the gateway; PoC not deployment |
| Controller | ESP32 | Arduino Uno, Pi | On-board Wi-Fi client, no extra hardware |
| Mobile | Kotlin / Android Studio | Flutter, React Native | No iOS need; direct platform APIs |
| Voice | Android SpeechRecognizer | Custom model | No training; on-device where available |
| Version control | Git + GitHub | ZIP snapshots | History = evidence; off-machine backup |
| Diagrams | draw.io | Visio | Free, XML files versioned beside the code |

## Decisions made during development

- **2026-09-18 — Detection source: ARP table, not live capture (for the PoC).**
  Live Scapy sniffing on the Windows hotspot adapter proved unreliable. The
  ARP table gives MAC+IP directly and robustly. Live capture stays as a
  documented enhancement. Does not change the design principle — discovery is
  still passive observation, not active probing.

## Open decision

- **Actuator: LED vs servo-driven lock.** The tools table lists an LED; earlier
  project notes describe a servo lock. Resolve before the hardware section is
  written, or state that both are driven from the same ESP32 endpoint.
