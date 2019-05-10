# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:09:13 2018

@author: 07160
"""

import asyncio
import urllib
from bs4 import BeautifulSoup
async def download():
    url = 'https://www.youtube.com/watch?v=rJ-gBIBfqx8'
    html=urllib.request.urlopen(url=url)
    soup=BeautifulSoup(html,'lxml')
    title=soup.title.string
    return 0

if __name__=="__main__":
    