#!/usr/bin/env python3

import scapy.all as scapy


def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac_address = get_mac_address(packet[scapy.ARP].psrc)
            response_mac_address = packet[scapy.ARP].hwsrc
            if real_mac_address != response_mac_address:
                print("[+] You are under attack!")
        except IndexError:
            pass
        print(packet.show())


sniff("eth0")
