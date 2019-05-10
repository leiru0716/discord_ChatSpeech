# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:22:57 2018

@author: 07160
"""

import discord
import glob
import re
import io
import aiohttp

import urllib.request
from bs4 import BeautifulSoup
import asyncio
import syncer
import threading
import random


client = discord.Client(max_messages=10000)

sounds=[]

filearray=None



class SoundPlayer():
    player=None
    path=''
    yt=False
    voice=None
    def __init__(self,path='',y=False,title=""):
        if bool(client.voice_clients):
            self.title=title
            print(self.title)
            self.voice=list(client.voice_clients)[0]
            self.path=path
            self.yt=y
            sounds.append(self)
            if(len(sounds)==1):
                client.loop.create_task(self.player_standby())
        else:
            pass
    
    async def player_standby(self):
        print('player_standby')
        option='-af dynaudnorm'
        if(self.yt):
            self.player=await self.voice.create_ytdl_player(self.path
                                                                ,options=option
                                                                ,after=self.after)
            
            print(self.player.download_url)
        else:
            self.player=self.voice.create_ffmpeg_player(self.path
                                                        ,options=option
                                                        ,after=self.after)
        self.player.volume=0.25
        self.player.start()
        
        
        print(type(self.player.process))
        return 0
    
    def after(self):

        self.player.stop()
        print('再生終了'+str(len(sounds)))
        if(len(sounds)==1):
            s=random.randrange(len(filearray))
            SoundPlayer(filearray[s][1],False,filearray[s][0])
        if(len(sounds)!=1):
            print('次の曲を再生')
            client.loop.create_task(sounds[1].player_standby())
        del sounds[0]



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if(message.author.bot):
        return 0
        
    SplitData=[splits for splits in message.content.split(' ') if bool(splits)]

    if SplitData[0]=='/music' and len(SplitData)>0:
        del SplitData[0]
        if SplitData[0]=='call':
            print(type(discord.member.Member))
            if type(message.author)==discord.member.Member:
                print("connecting")
                for i in list(client.voice_clients):
                    await i.disconnect()
                ch=message.author.voice.voice_channel
                if(bool(ch)):
                    if(client.is_voice_connected(ch.server)):
                        voice=client.voice_client_in(ch.server)
                    else:
                        voice=await client.join_voice_channel(ch)
                else:
                    return 0
        if bool(client.voice_clients):
            if SplitData[0]=='url':
                del SplitData[0]
                if SplitData[0]=='list':
                    lists='<!DOCTYPE html><html><body>'
                    with open("youtube_dl_list.txt","r") as f:
                        lists+='<br>'.join([u for u in f])
                    lists+='</body></html>'
                    bio=io.BytesIO(lists.encode())
                    bio.seek(0)
                    print("send")
                    await client.send_file(message.channel,bio,filename="Readable.html",content="読み込み可能なURLのリストです")
                    bio.close()
                else:
                    if(bool(re.match(r"<.+>",SplitData[0]))):
                        path=SplitData[0][1:len(SplitData[0])-1]
                    else:
                        path=SplitData[0]
                    SoundPlayer(path,True,"<"+path+">")
            elif SplitData[0]=='local':
                del SplitData[0]
                if SplitData[0]=='list':
                    del SplitData[0]
                    lists='<!DOCTYPE html><html><body>'
                    lists+='<br>'.join([f[0] for f in filearray])
                    lists+='</body></html>'
                    bio=io.BytesIO(lists.encode())
                    bio.seek(0)
                    print("send")
                    await client.send_file(message.channel,bio,filename="MusicList.html",content="曲目です")
                    bio.close()
                elif SplitData[0].isdigit():
                    s=int(SplitData[0])
                    SoundPlayer(filearray[s][1],False,filearray[s][0])
                    del SplitData[0]
                elif SplitData[0]=='random':
                    s=random.randrange(len(filearray))
                    SoundPlayer(filearray[s][1],False,filearray[s][0])
                    del SplitData[0]
            if bool(len(sounds)) or len(SplitData)!=0:
                if SplitData[0]=='pause':
                    sounds[0].player.pause()
                elif SplitData[0]=='resume':
                    sounds[0].player.resume()
                elif SplitData[0]=='skip':
                    if(len(sounds)==1):
                        sounds[0].player.stop()
                        del sounds[0]
                    else:
                        sounds[0].after()
                        
                elif SplitData[0]=='current':
                    await client.send_message(message.channel,'再生中:'+sounds[0].title)
                elif SplitData[0]=='list':
                    string=''
                    num=1
                    for s in sounds:
                        string+=str(num)+':'+s.title+'\n'
                        num+=1
                        
                    if(bool(string)):
                        await client.send_message(message.channel,string)
                elif SplitData[0]=='help':
                    await client.send_file(message.channel,'./help.html')

            
            
        


def localfiles():
    files=[]
    extensions=['m4a','mp4','flac','mp3']
    for e in extensions:
        files.extend(glob.glob("D:/Music/**/*."+e,recursive=True))
    
    filelist=[]
    for i in range(len(files)):
        name=files[i].split('\\')
        name=name[len(name)-1]
        name=name[:name.rfind(".")]
        name=re.split(r'[0-9]+( |-)',name)
        name=name[len(name)-1]
        name=name.replace(" ","_").replace(".","_")
        f=[name,files[i]]
        filelist.append(f)
    
    filelist=sorted(filelist)
    
    for i in range(len(filelist)):
        filelist[i][0]='['+str(i)+']:'+filelist[i][0]
    return filelist

@syncer.sync
async def SiteTitle(url,sp):
    req=urllib.request.urlopen(url=url)
    soup=BeautifulSoup(req,'lxml')
    sp.title=soup.title.string
    print("titlecomp")

if __name__=="__main__":
    filearray=localfiles()
    try:
        client.run("NDg4NjQ2NTY1MDI4NjkxOTg4.DoE1Hg.vnhlPByhPkkXXyh21ZS9OhYuAVY")
    except KeyboardInterrupt:
        client.close()