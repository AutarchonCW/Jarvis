import subprocess, re

out = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout

pattern = re.compile(r"(192\.168\.137\.\d+)\s+([\da-fA-F]{2}(?:[-:][\da-fA-F]{2}){5})")

devices = []
for ip, mac in pattern.findall(out):
    last = int(ip.split(".")[-1])
    if last in (0, 255):            #
        continue
    if mac.lower().startswith("ff"):  
        continue
    randomised = int(mac[1], 16) & 0b10 != 0   
    devices.append((ip, mac, randomised))

print(f"{len(devices)} real device(s) on the hotspot:\n")
for ip, mac, rnd in devices:
    tag = "  (randomised MAC)" if rnd else ""
    print(f"  {ip:<16} {mac}{tag}")