#!/usr/bin/env python
import requests


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("insert url download location here") # insert url download location here
