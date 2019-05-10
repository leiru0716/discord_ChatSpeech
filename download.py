# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:25:48 2018

@author: 07160
"""

import urllib.request
import sys


def download():
    url="https://cdn.discordapp.com/attachments/485433133588545571/488921612934971412/ea528aa0bc8ff20d.txt"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
    request=urllib.request.Request(url,headers=headers)
    data=urllib.request.urlopen(request).read()
    
    with open("test.txt",mode="wb") as f:
        f.write(data)
    
    
if __name__=="__main__":
    download()