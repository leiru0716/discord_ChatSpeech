# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 15:32:17 2018

@author: 07160
"""

from joblib import Parallel,delayed
import pytube
import asyncio
import time
import sys

size=1

def rcallback(stream,chunck,file_handle,bytes_remaining):
    print("progressing")
    pass

def ccallback(stream,file_handle):

    print('comp')
    pass

async def downloads():
    print("test")
    yt=pytube.YouTube('https://www.youtube.com/watch?v=YZgtJSEmnQA',
                      on_progress_callback=rcallback,on_complete_callback=ccallback).streams.first().download()
    print("return")
    return 0

if __name__=="__main__":
    loop=asyncio.get_event_loop()
    asyncio.ensure_future(downloads())
    try:
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        loop.close()
        quit()
    finally:
        loop.close()
        print("conmpleate")
    