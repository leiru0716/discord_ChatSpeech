# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:15:13 2018

@author: 07160
"""
import pytube
import discord
from pydub import AudioSegment
import io
import sys
from pytube import YouTube
import asyncio

client = discord.Client(max_messages=10000)

size=1
class SoundPlayer():
    def __init__(self):
        pass


def rcallback(stream,chunck,file_handle,bytes_remaining):
    sys.stdout.flush()
    sys.stdout.write("\r%f" % (100-(bytes_remaining/size)*100))
    pass

def ccallback(stream,file_handle):

    print('comp')
    pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    print('------')
    ch=client.get_channel("485433133588545575")
    voice=await client.join_voice_channel(ch)

    yt=YouTube(url='https://www.youtube.com/watch?v=YZgtJSEmnQA',
               on_progress_callback=rcallback,on_complete_callback=ccallback).streams.first()
    size=yt.filesize
    stb=yt.stream_to_buffer()
    stb.seek(0)

    sound=AudioSegment.from_file(stb,format="webm")
    sound=sound.set_frame_rate(48000)
    b=sound.export("./stb_export.wav",format="wav")
    
    print("play")
    voice.encoder_options(sample_rate=48000)
    b.seek(0)
    player=voice.create_stream_player(b)
    player.start()
    print(player.is_playing())
    
    
@client.event
async def on_socket_raw_recieve(msg):
    pass
    

    
if __name__=="__main__":
    client.run("NDg4NjQ2NTY1MDI4NjkxOTg4.DoE1Hg.vnhlPByhPkkXXyh21ZS9OhYuAVY")
    

    