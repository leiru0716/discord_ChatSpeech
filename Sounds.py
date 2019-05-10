# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 18:33:24 2018

@author: 07160
"""


import discord

import glob

import subprocess
import janome
import Process

import datetime
import os
import time

import threading

client = discord.Client(max_messages=6000)
param={}

music=[]
music_pause=False
def music():
    while(True):
        time.sleep(0.1)
        if(len(music)!=0):
            while(not(music[0].is_done())):
                time.sleep(0.1)
            del music[0]

            
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    print('------')


@client.event
async def on_message_edit(befor,after):
    print('dictionary info update')
    m=await client.pins_from(after.channel)


    for pin in m:
        if pin.author==after.author and pin.content.startswith('/op'):
            read_info=pin.content
            param[pin.author]=read_info

@client.event
async def on_message(message):
    print('------')
    m=discord.Message
    server=client.get_server("485433133588545567")
    if(client.is_voice_connected(server)):
        voice=client.voice_client_in(server)
    else:
        channel=client.get_channel("485433133588545575")
        voice = await client.join_voice_channel(channel)    
    print(message.author)
    print(message.content)
    print(message.id)
    print(message.type)
    print(message.nonce)
    print(message.embeds)
    print(message.channel)
    print(message.server)
    
    print('------')
    
    read_info=''
    if message.author in param.keys():
        print('in')
        read_info=param[message.author]
    else:
        print('out')
        m=await client.pins_from(message.channel)
    

        for pin in m:
            if pin.author==message.author and pin.content.startswith('/op'):
                read_info=pin.content
                param[pin.author]=read_info
    print(read_info)
    
    if(message.content.startswith('/se')):
        playlist=message.content.split(' ')
        path='./SE/'
        del playlist[0]
        for pl in playlist:
            player=voice.create_ffmpeg_player(path+pl)
            player.start()
            
            while(not(player.is_done())):
                time.sleep(0.1)
    elif(message.content.startswith('/mu')):
        playlist=message.content.split(' ')
        if(playlist[1]=='pause'):
            music[0].pause()
        elif(playlist[1]=='resume'):
            music[0].resume()
        else:
            path='./music/'
            del playlist[0]
            for pl in playlist:
                player=voice.create_ffmpeg_player(path+pl)
                player.start()

        
    else:

        now=datetime.datetime.now()
        timecount="{0:02d}{1:02d}{2:02d}".format(now.hour,now.minute,now.second)
        
        filename=timecount+".wav"
        filepath=''
        if(read_info==''):
            filepath=Process.SofTalk_exec(W=message.content,R=filename)
        else:
            filepath=Process.SofTalk_exec(W=message.content,R=filename,info=read_info)
    
        player=voice.create_ffmpeg_player(filepath)
        player.run()
        
        while(player.is_playing()):
            time.sleep(0.1)
        os.remove(filepath)

if(__name__=='__main__'):
    client.run("NDg1NDI2NTI2NDk0NTIzNDAy.DnaPwg.TLbo_lqesIi_uRMZ-weatFmbyh8")