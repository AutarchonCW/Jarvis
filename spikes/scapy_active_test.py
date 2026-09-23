from scapy.all import ARP, Ether, srp, conf

TARGET_IP = "192.168.137.246"  # your phone

conf.iface = "Ethernet"  # placeholder, see note below

pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=TARGET_IP)
answered, unanswered = srp(pkt, timeout=2, verbose=True)

for sent, received in answered:
    print(f"Got reply: {received.psrc} is at {received.hwsrc}")

if not answered:
    print("No reply - check interface name or that the phone is connected")