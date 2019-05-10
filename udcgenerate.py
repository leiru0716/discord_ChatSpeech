# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 18:25:53 2018

@author: 07160
"""

import subprocess

def udc_cost_cal():
    
    '"/Program Files (x86)/MeCab/bin/mecab-dict-index.exe"'
    "-m"
    "model_file"
    '"-d/Program Files (x86)/MeCab/dic/ipadic"'
    subprocess.call()