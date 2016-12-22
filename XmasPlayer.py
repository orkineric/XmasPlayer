# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:45:36 2015

@author: orkin
"""

from pygame import mixer
import os
import random
import time
from datetime import datetime
from contextlib import closing
import pickle

DONT_PLAY_LAST_N = 8

def log_song(song):
    with closing(open('player.log', 'a')) as log:
        log.write('%s: %s\n' % (datetime.now(), song))
    with closing(open('current_song', 'w')) as current:
        current.write('%s' % song)


def get_song(music_folder):
    last_fn = 'last_played.pkl'
    last_played = pickle.load(open(last_fn))
    songs = [song for song in os.listdir(music_folder) if song not in last_played]
    song = random.choice(songs)
    last_played.append(song)
    if len(last_played) > DONT_PLAY_LAST_N:
        last_played.pop(0)
    with closing(open(last_fn, 'w')) as lpfile:
        pickle.dump(last_played, lpfile)
    return song

def play_loop():
    music_folder = 'music'
    song = get_song(music_folder)
    log_song(song)
    song_path = os.path.join(music_folder, song)
    mixer.init()
    mixer.music.load(song_path)
    mixer.music.play()
    while mixer.music.get_busy():
        if os.path.exists('PAUSE'):
            mixer.music.stop()
        time.sleep(1)

def is_paused():
    return os.path.exists('PAUSE')

def is_no_timer():
    return os.path.exists('NO_TIMER')

if __name__=="__main__":
    while True:
        now = datetime.now()
        if not is_paused():
            play_loop()
            if not is_no_timer():
                for i in xrange(600, 0, -1):
                    with closing(open('current_song', 'w')) as current:
                        current.write('%d seconds until next song' % i)
                    time.sleep(1)
                    if is_paused() or is_no_timer():
                        break

