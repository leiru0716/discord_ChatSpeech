# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 19:28:37 2018

@author: 07160
"""

import pandas as pd

def keyword(words=''):
    if(words==''):
        return None
    
    df=pd.read_csv('./k2se.csv',header=None)
    series=df[df[0]==words]
    if(len(series)==0):
        return None
    return series.values[0][1]

def addKeyword(words='',se=''):
    if bool(words) and bool(se):
        df=pd.read_csv('./k2se.csv',header=None)
        index=list(df[0])
        try:
            line=index.index(words)
            drop=df.drop(line,axis=0)
            add=pd.Series([words,se],index=df.columns,name=str(len(df)))
            append=drop.append(add)
            append.to_csv('./k2se.csv',header=False,index=False)
            return '単語:'+words+'を音声:'+se+'に変更'
        except ValueError:
            add=pd.Series([words,se],index=df.columns,name=str(len(df)))
            append=df.append(add)
            append.to_csv('./k2se.csv',header=False,index=False)
            return '単語:'+words+',音声:'+se+'で追加'
    return '単語と音声ファイルの二種類を入力してください'

def keyList():
    df=pd.read_csv('./k2se.csv',header=None)
    li=df.values
    li=li.tolist()
    string=''
    for l in li:
        string+=':'.join(l)+'\n'
    
    return string

if __name__=="__main__":
    string=keyList()