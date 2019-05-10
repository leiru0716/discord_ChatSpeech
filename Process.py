# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 10:45:51 2018

@author: 07160
"""

import subprocess
import os
import time
def SofTalk_exec(W="これはテストです",R="Output.wav",info="/op 0 100 80"):
    info=info.replace('/op ','')
    text=W
    filename='./softalk/dll/'+R
    cmd=["./softalk/SofTalk.exe"]
    TSV=["/T:","/S:","/V:"]
    W="/W:"+W
    R="/R:"+R
    i=0
    infos=info.split(' ')
    if(len(text)>10):
        infos[1]=str(int(infos[1])+len(text))
        print('読み上げ加速')
    for state in infos:
        cmd.append(TSV[i]+state)
        i+=1
    cmd.append(R)
    cmd.append(W)
    
    
    
    print(cmd)
    
    subprocess.call(cmd)
    timer=time.time()
    while(not(os.path.isfile(filename))):
        time.sleep(0.1)
    print(time.time()-timer)
    print(os.listdir('./softalk/dll/'))
    return filename

def SofTalk_add_udc(words="",reading="",fh=False):
    if(words=="" or reading==""):
        return '追加できませんでした'
    cmd=["./softalk/SofTalk.exe"]
    cmd.append("/P:"+reading+","+words+","+str(fh))
    subprocess.call(cmd)
    return '単語:'+words+'読み方:'+reading+'で追加しました'
if __name__=='__main__':
    filename=SofTalk_exec(W="このつぎ")
