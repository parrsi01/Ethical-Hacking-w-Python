#!usr/bin/env/python

# Author:Simon Parris
# Date: 07/07/2021

# Definition: Code to change the user's mac address in the terminal
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address.")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac_address:
        parser.error("[-] Please specify a new Mac Address, use --help for more info.")
    return options


def change_mac_address(interface, new_mac_address):
    print("[+] Changing Mac Address for " + interface + " to " + new_mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC Address")


options = get_arguments()
current_mac_address = get_current_mac_address(options.interface)
print("Current MAC = " + str(current_mac_address))

change_mac_address(options.interface, options.new_mac_address)
current_mac_address = get_current_mac_address(options.interface)
if current_mac_address == options.new_mac_address:
    print("[+] MAC Address successfully changed to " + current_mac_address)
else:
    print("[-] MAC Address did not get changed.")