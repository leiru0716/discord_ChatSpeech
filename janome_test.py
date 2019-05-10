# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 14:29:26 2018

@author: 07160
"""

from janome.tokenizer import Tokenizer

t=Tokenizer()

token=t.tokenize("「ポケモンGO」が一大ムーブメントを巻き起こした2016年7月から、もう2年以上が経過しました。私自身は、ポケモンGOのサービス開始から、ほぼ毎日のようにアプリを起動し、ポケモンゲットにいそしんでいる人間ですが、おかげで「徳力さん、まだポケモンGOやっているんですか？」と聞かれる機会も増えました。")

words=[td.surface for td in token]