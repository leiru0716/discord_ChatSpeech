# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 16:51:40 2018

@author: 07160
"""

from janome.tokenizer import Tokenizer
t=Tokenizer("./udc")
tokens=t.tokenize("なぜあんなことに(゜Д゜)")
for token in tokens:
    print(token)