#!/usr/bin/python3
import subprocess
from scapy.all import *

# Dictionary to store counts of requests from each IP address
ip_counts = {}

# Threshold for the number of requests
threshold = 20


# Function to add an IP address to UFW
def add_ip_to_ufw2(ip):
    subprocess.run(['sudo', 'ufw', 'deny', 'from', ip])


def add_ip_to_ufw(ip):
    # Check if the IP address is already in UFW
    ufw_status = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
    if ip not in ufw_status.stdout:
        # Add the IP address to UFW
        subprocess.run(['sudo', 'ufw', 'deny', 'from', ip])
        print(f"Added {ip} to UFW.")
    else:
        print(f"{ip} is already present in UFW.")


print("SNIFFING HTTP REQUESTS.........")


def print_pkt(pkt):
    if pkt.haslayer(TCP) and (pkt[TCP].dport == 80 or pkt[TCP].dport == 443):
        src_ip = pkt[IP].src
        if src_ip in ip_counts:
            ip_counts[src_ip] += 1
            if ip_counts[src_ip] >= threshold:
                print(f"Threshold exceeded for {src_ip}. Adding to UFW.")
                add_ip_to_ufw(src_ip)
        else:
            ip_counts[src_ip] = 1
        print("Source IP:", src_ip)
        print("Destination IP:", pkt[IP].dst)
        print("Protocol:", pkt[IP].proto)
        print("Destination Port:", pkt[TCP].dport)
        print("\n")


pkt = sniff(filter='tcp port 80 or tcp port 443', iface="eth0", prn=print_pkt)
