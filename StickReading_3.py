"""
Created on Fri Sep 28 13:07:21 2018

@author: 07160
"""


# -*- coding: utf-8 -*-
import discord

import Process

import datetime
import os
import urllib.request
import keyword2se
import sys

import asyncio

client = discord.Client(max_messages=10000)
param={}

sounds=[]


class Sound():
    
    filepath=''
    sounddel=False
    player=None
    def __init__(self,voice,filepath,delete,vol):
        try:
            self.sounddel=delete
            self.filepath=filepath
            self.player=voice.create_ffmpeg_player(filepath,after=self.after,options='')
            if(vol>=0):
                self.player.volume=vol
            sounds.append(self)
            if(len(sounds)==1):
                sounds[0].player.start()
        except discord.ConnectionClosed:
            print('捕まえたぞ')
            
    def after(self):
        try:
            print('再生終了')
            print('path:'+self.filepath)
            if(self.sounddel):
                os.remove(self.filepath)
            if(len(sounds)>1):
                sounds[1].player.start()
            del sounds[0]
        except discord.ConnectionClosed:
            print('例外捕まえた')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    print('------')


@client.event
async def on_error():
    print('OnError!!')
    sys.exc_info()
    quit()

@client.event
async def on_message_edit(befor,after):
    await dictionaryupdate(after)

@client.event
async def on_voice_state_update(before,after):
    try:
        members=before.voice.voice_channel.voice_members
        mnum=len(members)
        for m in members:
            if(m.bot):
                mnum-=1
        
        print(mnum)
        if(mnum==0):
            print('disconnect')
            voice=client.voice_client_in(before.server)
            print(voice.is_connected())
        
    except:
        pass

@client.event
async def on_message(message):
    if(client.is_closed):
        await client.connect()
    
    if(message.author.bot):
        return 0

    
    if(client.is_voice_connected(message.server)):
        voice=client.voice_client_in(message.server)
    else:
        ch=message.author.voice.voice_channel
        if(bool(ch)):
            voice=await client.join_voice_channel(ch)
        else:
            return 0
    
#    target_server=message.server
#
#    
#    if(client.is_voice_connected(message.server)):
#        voice=client.voice_clients
#    else:
#        channel=client.get_channel("485433133588545575")
#        voice = await client.join_voice_channel(channel)  

    if message.author in param.keys():
        read_info=param[message.author]
    else:
        read_info=await dictionaryupdate(message)
    read_info=read_info if bool(read_info) else '0 100 80'
    infos=[info for info in read_info.split(' ') if bool(info)]
    
    SplitData=[splits for splits in message.content.split(' ') if bool(splits)]
    
    if SplitData[0]=='/se':
        #効果音再生用
        if len(SplitData)==3 and SplitData[1]=='add':
            url=message.attachments[0]['url']
            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
            request=urllib.request.Request(url,headers=headers)
            data=urllib.request.urlopen(request).read()
            with open("./SE/"+SplitData[2],mode="wb") as f:
                f.write(data)
        elif SplitData[1]=='list':
            lists=[file.split('.')[0] for file in os.listdir("./SE/")]
            lists='\n'.join(lists)
            await client.send_message(message.channel,lists)
        else:
            del SplitData[0]
            for file in SplitData:
                volume=Volume(infos)
                path=SE(file)
                if(bool(path)):
                    Sound(voice,path,False,volume)
                
    elif SplitData[0]=='/word':
        res=''
        if(len(SplitData)==4):
            res=Process.SofTalk_add_udc(words=SplitData[1],reading=SplitData[2],fh=bool(int(SplitData[3])))
        elif(len(SplitData)==3):
            res=Process.SofTalk_add_udc(words=SplitData[1],reading=SplitData[2])
        await client.send_message(message.channel,res)
    
    elif SplitData[0]=='/key' and len(SplitData)>=1:
        if len(SplitData)==3:
            ret=keyword2se.addKeyword(SplitData[1],SplitData[2])
            await client.send_message(message.channel,ret)
        elif SplitData[1]=='list':
            ret=keyword2se.keyList()
            await client.send_message(message.channel,ret)
    else:
        if(len(message.content)>100):
            message.content=message.content[:100]+'以下略'
        #通常の音声再生用
        
        ret=keyword2se.keyword(message.content)
        if(bool(ret)):
            volume=Volume(infos)
            path=SE(ret)
            Sound(voice,path,False,volume)
        else:
            filepath=Speech(message.content,read_info)
            Sound(voice,filepath,True,-1)
    
#    print('------')

#    print(message.author)
#    print(message.content)
#    print(message.id)
#    print(message.type)
#    print(message.nonce)
#    print(message.embeds)
#    print(message.channel)
#    print(message.server)

def Speech(text,read_info):
    now=datetime.datetime.now()
    timecount="{0:02d}{1:02d}{2:02d}".format(now.hour,now.minute,now.second)
    
    filename=timecount+".wav"
    filepath=''
    if(read_info==''):
        filepath=Process.SofTalk_exec(W=text,R=filename)
    else:
        filepath=Process.SofTalk_exec(W=text,R=filename,info=read_info)
    
    return filepath

def Volume(infos):
    volume=-1
    if(len(infos)==3):
        volume=int(infos[2])
        volume=float(volume)/100
    return volume

def SE(file):

    path="./SE/"
    lists=[file.split('.') for file in os.listdir("./SE/")]
    if(os.path.isfile(path+file)):
        print('found file')
        return path+file
    else:
        for name in lists:
            print(name[0])
            if(name[0]==file):
                print('found \n')
                print(path+name[0]+name[1])
                return path+name[0]+'.'+name[1]
        return None

async def dictionaryupdate(m):
    print('dictionary info update')
    pins=await client.pins_from(m.channel)

    read_info=''
    for pin in pins:
        if pin.author==m.author and pin.content.startswith('/op'):
            read_info=pin.content
            param[pin.author]=read_info
            return read_info

if(__name__=='__main__'):
    client.loop=asyncio.get_event_loop()
    try:
        client.loop.run_until_complete(client.start('NDg1NDI2NTI2NDk0NTIzNDAy.DnfPEg.usbjs_zuFIIMWHmbFnZuTAe5lL0'))
    except KeyboardInterrupt:
        client.loop.run_until_complete(client.logout())
    finally:
        print("programquit")
        client.loop.close()
    #client.run("NDg1NDI2NTI2NDk0NTIzNDAy.DnfPEg.usbjs_zuFIIMWHmbFnZuTAe5lL0")
    