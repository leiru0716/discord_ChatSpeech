# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 18:40:04 2018

@author: 07160
"""

import discord
import sys
import os
import re
import asyncio
import syncer

client = discord.Client(max_messages=10000)

sounds=[]



class SoundPlayer():
    player=None
    path=''
    yt=False
    voice=None
    def __init__(self,path='',insert=-1,y=False,voice=None):

        self.path=path
        self.yt=y
        self.voice=voice
        sounds.insert(len(sounds) if insert<0 else insert,self)
        print(sounds)
        if(len(sounds)==1):
            client.loop.create_task(self.player_standby())
            
    
    async def player_standby(self):
        print('player_standby')
        if(self.yt):
            self.player=await self.voice.create_ytdl_player(self.path,after=self.after)
            print(self.player.download_url)
        else:
            self.player=self.voice.create_ffmpeg_player(self.path,after=self.after)
        self.player.volume=0.5
        self.player.start()
        print(self.player.after)
        return 0
    
    def after(self):

        self.player.stop()
        print('再生終了'+str(len(sounds)))
        if(len(sounds)>1):
            print('次の曲を再生')
            client.loop.create_task(sounds[1].player_standby())
        del sounds[0]



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client.voice_clients)
    for s in client.servers:
        for ch in s.channels:
            if(ch.type==discord.ChannelType.voice):
                await client.join_voice_channel(ch)
        

@client.event
async def on_error():
    print('OnError!!')
    sys.exc_info()
    
@client.event
async def on_message(message):
    
    if(message.author.bot):
        return 0
    
    ch=message.author.voice.voice_channel
    if(bool(ch)):
        if(client.is_voice_connected(ch.server)):
            voice=client.voice_client_in(ch.server)
        else:
            voice=await client.join_voice_channel(ch)
    else:
        return 0
        
    SplitData=[splits for splits in message.content.split(' ') if bool(splits)]
    if SplitData[0]=='/music' and len(SplitData)>0:
        del SplitData[0]
        if SplitData[0]=='youtube':
            del SplitData[0]
            for data in SplitData:
                ins=-1
                if(data.startswith('ins')):
                    m=re.search(r"<.+>",data)
                    if(bool(m)):
                        string=m.group(0)
                        ins=string[1:len(string)-1]
                SoundPlayer(data,ins,True,voice)
        elif SplitData[0]=='local':
            del SplitData[0]
            if SplitData[0]=='list':
                lists=[file.split('.')[0] for file in os.listdir("./music/")]
                lists='\n'.join(lists)
                await client.send_message(message.channel,lists)
            else:
                for data in SplitData:
                    ins=-1
                    if(data.startswith('ins')):
                        m=re.search(r"<.+>",data)
                        if(bool(m)):
                            string=m.group(0)
                            ins=string[1:len(string)-1]
                    path=Music(data)
                    if bool(path):
                        SoundPlayer(path,ins,False,voice)
        
        elif SplitData[0]=='pause':
            sounds[0].player.pause()
        elif SplitData[0]=='resume':
            sounds[0].player.resume()
        elif SplitData[0]=='skip':
            if(len(sounds)==1):
                del sounds[0]
            else:
                sounds[0].after()
     
        elif SplitData[0]=='stop':
            sounds[0].player.stop()
        elif SplitData[0]=='start':
            sounds[0].player.start()
                
        elif SplitData[0]=='current':
            await client.send_message(message.channel,'再生中:'+sounds[0].path)
        elif SplitData[0]=='list':
            string=''
            num=1
            for s in sounds:
                string+=str(num)+':'+s.path+'\n'
                num+=1
                
            if(bool(string)):
                await client.send_message(message.channel,string)
            
def Music(file):

    path="./music/"
    lists=[file.split('.') for file in os.listdir("./music/")]
    if(os.path.isfile(path+file)):
        print('found file')
        return path+file
    else:
        for name in lists:
            print(name[0])
            if(name[0]==file):
                print('found \n')
                print(path+'/'+name[0]+name[1])
                return path+name[0]+'.'+name[1]
        return None
    
client.run("NDg4NjQ2NTY1MDI4NjkxOTg4.DoE1Hg.vnhlPByhPkkXXyh21ZS9OhYuAVY")