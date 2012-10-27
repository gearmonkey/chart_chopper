#!/usr/bin/env python
# encoding: utf-8
"""
hopper.py

hops from one video to another, maintaining relative beat:bar position and attempting to minimize distance between beats, timbrally or harmonically and prefering to switch tracks.


Created by Benjamin Fields on 2012-10-27.
Copyright (c) 2012 . All rights reserved.
"""

import sys
import os
import unittest
import random
from echonest import audio, video
from echonest.selection import fall_on_the
from echonest.sorting import timbre_distance_from, pitch_distance_from

class hopper:
    def __init__(self, tracks):
        self.videos = []
        for track in tracks:
            if 'youtube.com' in track:
                #assume it's a youtube url
                self.videos.append(video.loadavfromyoutube(track))
            else:
                self.videos.append(video.loadav(input_filename))
        self.collectvid = video.EditableFrames(settings=self.videos[0].video.settings)
        self.collectaudio = audio.AudioQuantumList()
    
    def assemble_by(self, samesongdownweight=10000, method = 'random'):
        #use max time signature as time signature
        out_ts = max([v.audio.analysis.time_signature['value'] for v in self.videos])
        all_beats = []
        for beat in range(1,out_ts+1):
            all_beats.append([v.audio.analysis.beats.that(fall_on_the(beat)) for v in self.videos])
            # all_beats.append(dict(zip(range(len(videos)),[v.audio.analysis.beats.that(fall_on_the(beat)) for v in self.videos])))
        this_beat = all_beats[1][0].pop(0)
        on_the = 2
        self.collect.append(this_beat)
        while len([x for x in [beat for beat in all_beats if len(beat)>0] if len(x)>0])>0:
            print 'remaining: ', len([x for x in [beat for beat in all_beats if len(beat)>0] if len(x)>0])
            #grabs from a track that still has beats
            next_beat_from = random.sample([x for x in range(len(all_beats[on_the])) if len(all_beats[on_the][x])>0],1)[0]
            this_beat = all_beats[on_the][next_beat_from].pop(0)
            self.collectvid += self.videos[next_beat_from].video[this_beat]
            self.collectaudio += self.videos[next_beat_from].audio[this_beat]
            #advance the beatticker
            on_the += 1
            if on_the > out_ts:
                on_the = 1
                
    def writeout(self, filename):
        outav = video.SynchronizedAV(audio=self.collectaudio, video=self.collectvid)
        outav.save(filename)
        

class hopperTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()