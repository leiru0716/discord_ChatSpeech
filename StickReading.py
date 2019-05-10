# -*- coding: utf-8 -*-
import discord

import Process

import datetime
import os
import urllib.request
import keyword2se
import sys

client = discord.Client(max_messages=10000)
param={}

sounds=[]


class Sound():
    
    filepath=''
    sounddel=False
    player=None
    def __init__(self,voice,filepath,delete,vol):
        self.sounddel=delete
        self.filepath=filepath
        self.player=voice.create_ffmpeg_player(filepath,after=self.after)
        if(vol>=0):
            self.player.volume=vol
        sounds.append(self)
        if(len(sounds)==1):
            sounds[0].player.start()
        
    def after(self):
        print('再生終了')
        print('path:'+self.filepath)
        if(self.sounddel):
            os.remove(self.filepath)
        if(len(sounds)>1):
            sounds[1].player.start()
        del sounds[0]


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    print('------')


@client.event
async def on_error():
    sys.exc_info()
    quit()

@client.event
async def on_message_edit(befor,after):
    await dictionaryupdate(after)

@client.event
async def on_message(message):
    if(message.author==client.user):
        return 0
#    print('------')
    server=client.get_server("485452714415751169")

    if(client.is_voice_connected(server)):
        voice=client.voice_client_in(server)
    else:
        channel=client.get_channel("485452714415751173")
        voice = await client.join_voice_channel(channel)  
#    print(message.author)
#    print(message.content)
#    print(message.id)
#    print(message.type)
#    print(message.nonce)
#    print(message.embeds)
#    print(message.channel)
#    print(message.server)
    if(len(message.content)>100):
        message.content=message.content[:100]+'以下略'
    print('------')
    
    read_info=''
    if message.author in param.keys():
        read_info=param[message.author]
    else:
        read_info=await dictionaryupdate(message)
    print(read_info)
    if(read_info==None):
        read_info='0 100 80'
    if(message.content.startswith('/se')):    
        playlist=message.content.split(' ')
        path='./SE/'
        del playlist[0]
        for pl in playlist:
            if(pl=='list'):
                await client.send_message(message.channel,os.listdir(path))
                break
            elif(pl=='add' and len(message.attachments)!=0):
                url=message.attachments[0]['url']
                
                print(url)
                headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
                request=urllib.request.Request(url,headers=headers)
                data=urllib.request.urlopen(request).read()
                with open("./SE/"+playlist[1],mode="wb") as f:
                    f.write(data)
                break
            
            elif(os.path.isfile(path+pl)):
                info=read_info.split(' ')
                volume=-1
                if(len(info)==3):
                    volume=int(info[2])
                    volume=float(volume)/100
                
                Sound(voice,path+pl,False,volume)
                
    elif(message.content.startswith('/word')):
        content=message.content.split(' ')
        print(content)
        res=''
        if(len(content)==4):
            res=Process.SofTalk_add_udc(words=content[1],reading=content[2],fh=bool(int(content[3])))
        elif(len(content)==3):
            res=Process.SofTalk_add_udc(words=content[1],reading=content[2])
        await client.send_message(message.channel,res)
        
    else:
        ret=keyword2se.keyword(message.content)
        if(bool(ret)):
            info=read_info.split(' ')
            volume=-1
            if(len(info)==3):
                volume=int(info[2])
                volume=float(volume)/100
            if(os.path.isfile('./SE/'+ret)):
                Sound(voice,'./SE/'+ret,False,volume)
        else:
            filepath=Speech(message.content,read_info)
            Sound(voice,filepath,True,-1)

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
    client.run("NDg1NDI2NTI2NDk0NTIzNDAy.DnfPEg.usbjs_zuFIIMWHmbFnZuTAe5lL0")
    



