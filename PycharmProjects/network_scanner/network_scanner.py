#!usr/bin/env/python
# Author: Simon Parris
# Date: 08/07/2021
# Definition: Discover all clients on Network.

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]

    print("IP\t\t\t\tMAC Address\n-------------------------------")
    clients_list = []
    for element in answered_list:
        # ip address: prsc
        # mac address: hwsrc
        clients_dictionary = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dictionary)
    return clients_list


def print_result(results_list):
    print("IP\t\t\t\tMAC Address\n-------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
