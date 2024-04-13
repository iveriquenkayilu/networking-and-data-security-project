#!/usr/bin/python3
from scapy.all import *

print("SNIFFING HTTP REQUESTS.........")


def print_pkt(pkt):
    if pkt.haslayer(TCP) and (pkt[TCP].dport == 80 or pkt[TCP].dport == 443):
        print("Source IP:", pkt[IP].src)
        print("Destination IP:", pkt[IP].dst)
        print("Protocol:", pkt[IP].proto)
        print("Destination Port:", pkt[TCP].dport)
        if pkt.haslayer(Raw):
            http_payload = pkt[Raw].load.decode('utf-8', 'ignore')
            if "HTTP" in http_payload:  # Check if the packet contains HTTP data
                headers, _, body = http_payload.partition('\r\n\r\n')
                print("HTTP Headers:")
                for header in headers.split('\r\n'):
                    print(header)
                print("\nHTTP Body:")
                print(body)
                print("\n")
            else:
                print("Non-HTTP payload:\n", http_payload)
                print("\n")


pkt = sniff(filter='tcp port 80 or tcp port 443', iface="eth0", prn=print_pkt)
