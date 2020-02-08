#!/bin/python3

import requests
import time


class URLLOAD:

    def dorequest(self, url):
        time.sleep(1)  # add by zyx
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Mist/0.11.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36"}
        res = requests.get(url, headers=headers, verify=True, allow_redirects=False)
        if res.status_code == 200:
            return res.text
