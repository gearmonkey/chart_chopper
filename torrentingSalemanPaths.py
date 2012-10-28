#!/usr/bin/env python
# encoding: utf-8
"""
torrentingSalemanPaths.py

Created by Benjamin Fields on 2012-10-27.
Copyright (c) 2012 . All rights reserved.
"""

import sys
import os

import mmpy
import marmalade
import gdata.youtube
import gdata.youtube.service

import hopper
from keys import *

marmalade.config.TIMJ_API_KEY = JAM_KEY


def relgrps2ytvids(releasegroups):
    """
    resolves releasegroups by name to most relevant youtube video, return list of most relevant url for each
    """
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.developer_key = YT_DEV_KEY
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.orderby = 'relevance'
    query.racy = 'include'
    yt_links = []
    for relgrp in releasegroups:
        query.vq = '{0} {1}'.format(relgrp.name, relgrp.artist.name)
        feed = yt_service.YouTubeQuery(query)
        yt_links.append(feed.entry[0].media.player.url.strip('&feature=youtube_gdata_player'))
        print '{0}--{1} is at {2}'.format(relgrp.name, relgrp.artist.name,
                                          feed.entry[0].media.player.url.strip('&feature=youtube_gdata_player'))
    return yt_links
    

def topNsingles(n=10):
    """
    returns a list of the top n releasegroups (or all if that is less than n) that look like singles
    and don't have the exact same name as tracks thathave already been added (note: this is a crap way to confirm uniqueness)
    """
    p2p_diff = mmpy.Chart('p2p daily releasegroups')
    top_singles = []
    for (rank, val, relgrp) in ( rg for rg in p2p_diff.releasegroup if 'single' in rg[2].description.lower() ):
        if len(top_singles) == 0 or relgrp.name not in [rg.name for rg in top_singles]:
            top_singles.append(relgrp)
        if len(top_singles) >= n:
            break
    return top_singles

def jams2vids(jams, service ='youtube'):
    """
    convert list of jams to list of urls, filtered by service
    """
    return [j.get_url() for j in jams if service in j.get_url()]
    
def lastNJams(user, N=10):
    return marmalade.TIMJUser(user).get_jams()[:N]

def main():
    if len(sys.argv)>1:
        for username in sys.argv[1:]:
            print 'fetching the last 5 youtube jams from', username
            try:
                hopped = hopper.hopper(jams2vids(lastNJams(username))[:5]) #grab ten jams, to try and ensure 5 from yt
                hopped.assemble_by()
                try:
                    hopped.writeout(username+'.mp4')
                except:
                    hopped.writeout(username+'flv')
            except:
                print '**unable to deal with',username,'continuing...'
    else:
        top_singles = topNsingles(6)
        as_yt = relgrps2ytvids(top_singles)
        hopped = hopper.hopper(as_yt)
        hopped.assemble_by()
        try:
            hopped.writeout('chart.mp4')
        except:
            #fall back on flv since I know that will work
            hopped.writeout('chart.flv')


if __name__ == '__main__':
    main()

