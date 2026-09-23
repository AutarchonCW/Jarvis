# Technology Selection and Justification

*Draft section for the JARVIS analysis document. Substantiated claims are referenced (APA 7); the reference list is at the end.*

---

## 1. Selection method

Technology choices in this project were not made on preference but against a fixed set of criteria derived from the project context: a four-week individual proof of concept with a single developer, no budget for licences, and an explicit assessment requirement that the result demonstrates my own understanding of the underlying mechanisms rather than the output of a pre-built tool.

The following criteria were applied to every decision below:

| ID | Criterion | Rationale |
|----|-----------|-----------|
| C1 | Fitness for the functional requirement | The option must be technically capable of the task at all. |
| C2 | Time-to-working-increment | With four weeks and five subsystems, a technology that delays the first working increment is a project risk. |
| C3 | Transparency of mechanism | The learning objectives require that I can explain *how* the result was produced, not only *that* it was produced. |
| C4 | Alignment with the human-in-the-loop design principle | JARVIS alerts the homeowner; it does not act autonomously and does not generate intrusive traffic. |
| C5 | Cost and availability | No licence cost, and hardware obtainable within the project window. |

C3 deserves a comment, because "I want to learn it" is not by itself an engineering argument. It is admissible here because the assignment is a learning-oriented proof of concept, in which demonstrable understanding is a stated deliverable rather than a personal preference. It is weighted below C1 and C4: where a choice would have made the system less fit for purpose or less privacy-respecting, C3 did not decide the outcome.

---

## 2. Decisions

### 2.1 Backend language: Python

**Chosen:** Python.
**Alternatives considered:** Java, C#, Node.js.

Python was selected for the backend because it combines an accessible syntax with the specific libraries this project needs (packet handling, embedded HTTP APIs, SQLite) in one ecosystem.

The claim that Python lowers the entry barrier relative to Java is supported in the computing-education literature: Lo, Lin and Wu (2015) compare Java and Python as a first language and identify the simpler syntax and higher-level data structures of Python as the main advantage for novices, whereas the syntactic complexity of C/C++/Java is a documented obstacle. The claim that this translates into faster delivery is supported by Prechelt's (2000) empirical comparison of seven languages, in which script languages such as Python and Perl required roughly half the development time of C, C++ and Java for the same task, at the cost of runtime performance — a trade-off that is irrelevant for a home-scale monitoring tool handling tens of devices.

Ecosystem availability was the second consideration. Python's adoption has continued to grow, and Stack Overflow's 2025 Developer Survey records the largest year-on-year increase of any language in the survey, attributing it in part to back-end use (Stack Overflow, 2025). For a single developer with no team to fall back on, the practical consequence is a larger body of documentation and community answers.

**Counter-evidence acknowledged:** the empirical picture on first-language choice is not one-sided. Savić, Ivanović, Radovanović and Budimac (2016) found no deep impact of the introductory language on the acquisition of core programming concepts. This argues that Python is not *pedagogically necessary*; the justification here therefore rests primarily on library fit and delivery speed (C1, C2), with accessibility as a supporting rather than a decisive factor.

### 2.2 Python IDE: Visual Studio Code

**Chosen:** Visual Studio Code.
**Alternative considered:** PyCharm.

Both editors are functionally sufficient for this project, so this is a low-risk decision. VS Code was selected because a single editor covers the Python backend, the ESP32 sketch and the project documentation, whereas PyCharm's advantages (deep refactoring, integrated database and framework tooling) target codebases considerably larger than a four-week proof of concept. VS Code and Visual Studio have held the top positions in the Stack Overflow developer environment rankings for four consecutive years, which is relevant mainly for the availability of extensions and troubleshooting material (Stack Overflow, 2025).

Note that this decision is not fully consistent: the Android application is developed in Android Studio (§2.7) and the ESP32 firmware in the Arduino IDE (§2.9), so the "one editor" argument applies to the Python and documentation work only.

### 2.3 Network discovery: Scapy

**Chosen:** Scapy (Python library).
**Alternative considered:** Nmap.

Scapy is a Python-based interactive packet manipulation library that can construct, send, capture and dissect packets across a wide range of protocols, and the documentation notes it can replace parts of Nmap, tcpdump and tshark (Scapy, n.d.). Two arguments support the choice.

First, **architectural fit (C1).** Scapy runs inside the backend process. Device discovery based on observing ARP traffic returns Python objects that can be written straight into SQLite and compared against the registered-device table. Nmap is a separate binary; using it would require shelling out to a subprocess and parsing its output, adding an integration layer without adding capability at this scale.

Second, **alignment with the design principle (C4).** Nmap is a scanner: host discovery and port scanning generate active probe traffic toward every device on the network (Lyon, 2009). JARVIS is specified as a *passive* monitor that observes and alerts. Introducing an active scanner would contradict that specification and would generate exactly the kind of unrequested traffic toward guests' devices that the system exists to make visible.

Third, **transparency (C3).** Building discovery from ARP responses requires understanding what an ARP reply contains and why an unregistered MAC address on the local segment is a signal at all. Nmap's host-discovery logic is well engineered and well documented, but it is opaque from the caller's perspective.

**Honest limitation:** Scapy is the weaker option for service and OS fingerprinting, and the documentation itself notes it may drop packets under heavy load. If JARVIS were extended toward device identification beyond MAC/vendor level, Nmap would become the appropriate tool.

### 2.4 Network analysis during development: Wireshark

**Chosen:** Wireshark.
**Alternative considered:** tcpdump.

This is a *development and verification* tool, not a runtime component of JARVIS — it is used to confirm that what the Scapy layer reports matches what is actually on the wire. Wireshark provides a graphical interface that decodes protocol structure into a navigable tree, with display filters and traffic statistics (Wireshark Foundation, n.d.). For verifying that a captured ARP or DHCP exchange has been parsed correctly, being able to see the decoded field alongside the raw bytes materially shortens the debugging loop.

tcpdump was not rejected on quality grounds; it is a capable capture tool and its underlying library (libpcap) is what Scapy depends on for capture. It is text-based and therefore better suited to headless capture and scripted use, which this project does not require. Wireshark also ships a command-line equivalent (TShark), so the two are complementary rather than exclusive (Wireshark Foundation, n.d.).

### 2.5 Backend API: FastAPI

**Chosen:** FastAPI.
**Alternative considered:** Flask.

The Android application communicates with the backend over HTTP, which requires an API layer. FastAPI was selected because request and response validation and API documentation are produced from the same source: models are declared with standard Python type hints, Pydantic validates incoming data against them, and the framework generates an OpenAPI schema rendered as interactive documentation (Ramírez, n.d.).

Two concrete benefits for this project follow. First, malformed requests from the Android client are rejected by the framework with a structured error, rather than surfacing as an exception in application code — relevant because client and server are developed by one person in alternation. Second, the generated interactive documentation makes it possible to exercise every endpoint from a browser before any Android code exists, decoupling backend progress from app progress (C2).

Flask is a capable microframework and would be sufficient functionally, but it does not provide schema validation or OpenAPI generation out of the box; both require additional extensions and configuration. Given a fixed four-week window, adopting a framework where these are defaults rather than add-ons reduces setup effort.

### 2.6 Host machine: laptop

**Chosen:** development laptop.
**Alternative considered:** Raspberry Pi.

For the proof of concept the backend, database and packet capture run on the development laptop. This removes cross-compilation, remote deployment and headless debugging from a four-week schedule, and the machine is already available at no additional cost (C2, C5).

**This is the weakest choice in the stack and is documented as such.** A passive network monitor is only useful if it is running; a laptop is not always on and is not always attached to the home network. The proof of concept therefore demonstrates the *capability* rather than the *deployment*. A Raspberry Pi — always-on, low-power, permanently wired to the home network — is the correct target for any production version, and the backend is kept platform-neutral (Python 3 + SQLite, no laptop-specific dependencies) so that migration is a deployment task rather than a rewrite. Naming this limitation explicitly is preferable to presenting the laptop as an unqualified best choice.

### 2.7 Android development: Android Studio with Kotlin

**Chosen:** Android Studio + Kotlin (Jetpack Compose).
**Alternatives considered:** Flutter, React Native.

Kotlin is Google's recommended language for new Android applications; Android has followed a stated Kotlin-first approach since 2019, with new Jetpack APIs offered in Kotlin first (Android Developers, n.d.-a). Choosing the platform-recommended path means the official documentation, samples and API references match the code being written, which for a solo developer is a significant reduction in friction.

Cross-platform frameworks were rejected on requirements grounds rather than quality grounds: there is no iOS requirement in this project, so their principal benefit does not apply, while they add a second toolchain and an abstraction layer between the app and the platform APIs. That matters specifically here, because the app depends on two platform-level capabilities — the speech recognition service (§2.10) and local-network communication — which are reached most directly through the native SDK.

### 2.8 IoT controller: ESP32

**Chosen:** ESP32.
**Alternatives considered:** Arduino Uno R3, Raspberry Pi.

The controller must join the home Wi-Fi network as an ordinary client so that it can (a) receive commands from the backend and (b) appear in JARVIS's own device discovery as a real network device. The ESP32 integrates 802.11 b/g/n Wi-Fi and Bluetooth on the SoC, and supports infrastructure Station mode, SoftAP mode and promiscuous mode (Espressif Systems, 2025). Station mode is precisely the "normal client" behaviour required, and needs no additional hardware.

The Arduino Uno R3 is built around the ATmega328P and provides USB and I/O but no wireless connectivity; Wi-Fi requires either a shield or a different board in the UNO family, such as the UNO WiFi Rev2 (Arduino, n.d.-a; Arduino, n.d.-b). Adding a shield adds cost, wiring and a second library stack for no benefit over an ESP32.

A Raspberry Pi would satisfy the connectivity requirement but is a full Linux computer. Using one to drive a single output is disproportionate in cost, power draw and configuration overhead, and it would blur the architectural boundary between the host running the monitoring backend (§2.6) and the endpoint being controlled.

### 2.9 IoT development environment: Arduino IDE

**Chosen:** Arduino IDE.
**Alternative considered:** PlatformIO.

The firmware for this project is small: connect to Wi-Fi, expose or poll a command endpoint, and drive one output. The Arduino IDE installs the ESP32 board support package through the boards manager and requires no project configuration file, dependency manifest or build-system knowledge before the first upload. PlatformIO offers dependency management, multi-environment builds, unit testing and better editor integration — all of which are advantages in a larger or longer-lived embedded project, and none of which this firmware requires. The decision is scoped to this proof of concept and would be revisited if the firmware grew beyond a single sketch.

### 2.10 Voice input: Android SpeechRecognizer

**Chosen:** Android platform `SpeechRecognizer` API.
**Alternative considered:** a custom or third-party speech model.

The Android SDK exposes speech recognition through `android.speech.SpeechRecognizer`, which converts spoken input into text that the application can map to commands, and requires the `RECORD_AUDIO` permission (Android Developers, n.d.-b). Using the platform service means no model training, no audio pipeline and no additional runtime dependency, so voice control can be validated against the small fixed command set this project needs before any effort is spent on recognition quality (C2).

**A privacy caveat must be stated, because it goes to the core premise of this project.** The platform documentation notes that the implementation is likely to stream audio to remote servers, and that the API is consequently not intended for continuous recognition (Android Developers, n.d.-b). JARVIS is motivated by homeowners' concern about devices listening to them; shipping a component that sends microphone audio off-device without acknowledgement would undermine that premise. Two mitigations apply and are adopted:

1. Recognition is invoked explicitly by the user (press-to-talk), never continuously — which is also what the documentation recommends on battery and bandwidth grounds.
2. `SpeechRecognizer.createOnDeviceSpeechRecognizer()` is used where available, with `isOnDeviceRecognitionAvailable()` checked at runtime, so that recognition is kept on the device on supporting hardware (Android Developers, n.d.-b).

Where on-device recognition is unavailable, this is documented as a known limitation of the proof of concept rather than presented as solved.

### 2.11 Version control: Git and GitHub

**Chosen:** Git with a GitHub remote.
**Alternative considered:** manual archived copies (ZIP snapshots).

Git provides commit-level history, branching and an off-machine remote (Chacon & Straub, 2014). Beyond the general case for version control, two project-specific reasons apply: the commit history is direct evidence of individual work and of incremental progress across the four weeks, which is relevant to assessment; and the off-machine remote is the only backup for a project whose backend runs on a single laptop (§2.6).

Manual ZIP archiving is not a serious alternative — it provides no diffing, no branch isolation for experimental work, and no reliable ordering — and is listed here only because it is the default fallback when version control is skipped.

### 2.12 Architecture and documentation: diagrams.net (draw.io)

**Chosen:** diagrams.net / draw.io.
**Alternative considered:** Microsoft Visio.

diagrams.net is free and runs in the browser or as a desktop application, with no licence dependency (C5) and no barrier to an assessor opening a diagram. Diagram files are stored as XML alongside the source code, so architecture diagrams are versioned in the same repository as the implementation they describe and cannot drift out of sync unnoticed. Visio is a mature product with stronger enterprise stencil and integration support, but those advantages are not exercised in a single-developer project and its licensing would restrict who can open the source files.

### 2.13 Smart-home simulation hardware

**Chosen:** LED, current-limiting resistor, jumper wires, breadboard, driven from an ESP32 GPIO pin.

The purpose of the physical component is to demonstrate end-to-end control — voice command → Android app → API → backend → network → ESP32 → physical state change — not to build production hardware. An LED on a breadboard makes that chain observable at the lowest possible cost and risk, requires no mains wiring, and is safe to iterate on. Substituting a commercial smart bulb would introduce a vendor cloud, a proprietary protocol and an integration dependency, all outside the project scope; substituting a relay would introduce mains voltage into a student proof of concept for no additional demonstrated capability.

*Consistency check required:* the analysis document elsewhere describes a servo-driven simulated smart lock. Confirm before submission whether the demonstrator is a light (LED) or a lock (servo), or state explicitly that both actuator types are driven from the same ESP32 endpoint.

---

## 3. Summary

| Decision area | Selected | Rejected | Decisive criterion |
|---|---|---|---|
| Backend language | Python | Java, C#, Node.js | C1, C2 |
| Python IDE | VS Code | PyCharm | C2 |
| Network discovery | Scapy | Nmap | C4, C1 |
| Traffic verification | Wireshark | tcpdump | C3 |
| API framework | FastAPI | Flask | C2 |
| Host machine | Laptop | Raspberry Pi | C2, C5 (with documented limitation) |
| Mobile app | Android Studio + Kotlin | Flutter, React Native | C1 |
| IoT controller | ESP32 | Arduino Uno, Raspberry Pi | C1 |
| IoT toolchain | Arduino IDE | PlatformIO | C2 |
| Voice input | Android SpeechRecognizer | Custom speech model | C2 (with privacy mitigation) |
| Version control | Git + GitHub | ZIP snapshots | C1 |
| Diagramming | diagrams.net | Visio | C5 |

---

## 4. Threats to the validity of these choices

1. **The laptop host undermines continuous operation.** The proof of concept demonstrates capability, not deployment (§2.6).
2. **Cloud speech recognition conflicts with the project's privacy premise** unless on-device recognition is available on the test device (§2.10).
3. **Scapy is the weaker option for device fingerprinting**, which constrains how far device identification can be extended (§2.3).
4. **"Learning value" as a criterion is defensible only within the assignment context.** In a commercial setting, C3 would carry far less weight and some of these decisions — particularly Scapy over Nmap — would be reweighted.

---

## References

Android Developers. (n.d.-a). *Android's Kotlin-first approach*. Google. Retrieved September 9, 2026, from https://developer.android.com/kotlin/first

Android Developers. (n.d.-b). *SpeechRecognizer*. Google. Retrieved September 9, 2026, from https://developer.android.com/reference/android/speech/SpeechRecognizer

Arduino. (n.d.-a). *Arduino UNO Rev3*. Retrieved September 9, 2026, from https://store.arduino.cc/products/arduino-uno-rev3

Arduino. (n.d.-b). *An overview of different UNO boards*. Arduino Help Center. Retrieved September 9, 2026, from https://support.arduino.cc/hc/en-us/articles/7901453165724-An-overview-of-different-UNO-boards

Chacon, S., & Straub, B. (2014). *Pro Git* (2nd ed.). Apress. https://git-scm.com/book/en/v2

Espressif Systems. (2025). *ESP32 series datasheet* (v5.3). https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf

Lo, C. A., Lin, Y. T., & Wu, C. C. (2015). Which programming language should students learn first? A comparison of Java and Python. In *2015 International Conference on Learning and Teaching in Computing and Engineering (LaTiCE)* (pp. 225–226). IEEE. https://ieeexplore.ieee.org/document/7126267

Lyon, G. F. (2009). *Nmap network scanning: The official Nmap project guide to network discovery and security scanning*. Nmap Software LLC. https://nmap.org/book/

Prechelt, L. (2000). An empirical comparison of seven programming languages. *Computer, 33*(10), 23–29.

Ramírez, S. (n.d.). *Features*. FastAPI documentation. Retrieved September 9, 2026, from https://fastapi.tiangolo.com/features/

Savić, M., Ivanović, M., Radovanović, M., & Budimac, Z. (2016). Modula-2 versus Java as the first programming language: Evaluation of students' performance. In *Proceedings of the 17th International Conference on Computer Systems and Technologies (CompSysTech '16)*. ACM. https://doi.org/10.1145/2983468.2983511

Scapy. (n.d.). *Introduction*. Scapy documentation. Retrieved September 9, 2026, from https://scapy.readthedocs.io/en/latest/introduction.html

Stack Overflow. (2025). *2025 developer survey: Technology*. https://survey.stackoverflow.co/2025/technology

Wireshark Foundation. (n.d.). *Wireshark user's guide*. Retrieved September 9, 2026, from https://www.wireshark.org/docs/wsug_html/

---

## 5. Before submitting: verify these yourself

Two claims in §2.9 and §2.12 (PlatformIO's feature set; diagrams.net licensing and file format) are stated from general knowledge and currently carry no citation. Either add the primary sources (docs.platformio.org and diagrams.net) or soften the wording. Also open the Stack Overflow 2025 survey page and confirm the exact Python and IDE figures against how they are phrased in §2.1 and §2.2, since survey pages are updated.
