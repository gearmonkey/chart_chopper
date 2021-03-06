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

def remaining_beats(beat_arr):
    """because audioQuantumLists really don't like being unwrapped in
    List comprehensions
    """
    num_beats = 0
    for beat in beat_arr:
        num_beats += sum([len(x) for x in beat])
    return num_beats

class hopper:
    def __init__(self, tracks):
        self.videos = []
        for track in tracks:
            if 'youtube.com' in track:
                #assume it's a youtube url
                try:
                    self.videos.append(video.loadavfromyoutube(track))
                except:
                    print 'unable to fetch', track
            else:
                self.videos.append(video.loadav(track))
        self.collectvid = video.EditableFrames(settings=self.videos[0].video.settings)
        self.collectaudio = audio.AudioQuantumList()
    
    def assemble_by(self, samesongdownweight=10000, method = 'random'):
        #use max time signature as time signature
        out_ts = max([v.audio.analysis.time_signature['value'] for v in self.videos])
        print 'out_ts:', out_ts
        all_beats = []
        for beat in range(1,out_ts+1):
            all_beats.append([v.audio.analysis.beats.that(fall_on_the(beat)) for v in self.videos])
            # all_beats.append(dict(zip(range(len(videos)),[v.audio.analysis.beats.that(fall_on_the(beat)) for v in self.videos])))
        print 'beat break down:'
        for idx, beat in enumerate(all_beats):
            print 'beat',idx+1,':',
            print ' '.join([str(len(x)) for x in beat])
        # this_beat = all_beats[1][0].pop(0)
        on_the = 0
        # self.collectvid += self.videos[0].video[this_beat]
        # self.collectaudio += self.videos[0].audio[this_beat]
        
        while remaining_beats(all_beats) > 0:
            print 'remaining: ', remaining_beats(all_beats)
            #grabs from a track that still has beats
            try:
                next_beat_from = random.sample([x for x in range(len(all_beats[on_the])) if len(all_beats[on_the][x])>0],1)[0]
            except ValueError:
                print 'not enough beats left, giving up...'
                return
            print 'fetching a', on_the, 'beat from ', next_beat_from
            this_beat = all_beats[on_the][next_beat_from].pop(0)            
            self.collectvid += self.videos[next_beat_from].video[this_beat]
            self.collectaudio.append(audio.Simultaneous([self.videos[next_beat_from].audio[this_beat]]))
            #advance the beatticker
            on_the += 1
            if on_the >= out_ts:
                on_the = 0
                
    def writeout(self, filename):
        outav = video.SynchronizedAV(audio=self.collectaudio.render(), video=self.collectvid)
        outav.save(filename)
        

class hopperTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()