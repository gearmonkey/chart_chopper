#!/usr/bin/env python
# encoding: utf-8
"""
videoAwithAudioB.py

Created by Benjamin Fields on 2012-10-27.
Copyright (c) 2012 . All rights reserved.
"""

import sys
import os

import gdata.youtube
import gdata.youtube.service

import hopper
from keys import *
    

def main():
    print 'using', sys.argv[1:3], 'as source videos',
    print 'and saving to', sys.argv[3]
    hopped = hopper.hopper(sys.argv[1:3])
    hopped.assemble_by(method="overlap")
    try:
        hopped.writeout(sys.argv[3])
    except:
        #fall back on flv since I know that will work
        hopped.writeout('chart.flv')


if __name__ == '__main__':
    main()

