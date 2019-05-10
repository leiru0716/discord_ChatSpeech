# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 18:21:20 2018

@author: 07160
"""

import youtube_dl
url='https://www.youtube.com/watch?v=EkCtzZ32sgY'

with youtube_dl.YoutubeDL({'format':'137'}) as ydl:
    d=ydl.download([url])
    print(type(d))