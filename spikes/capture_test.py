from scapy.all import sniff, conf
print(conf.ifaces)
print('\nSniffing 5 ARP packets - connect/reconnect your phone now...\n')
sniff(filter='arp', count=5, prn=lambda p: print(p.summary()))
