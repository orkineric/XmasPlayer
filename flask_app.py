# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 23:33:25 2016

@author: orkin
"""

import os
from flask import Flask
import flask
import json
import pickle

app = Flask(__name__)

@app.route('/')
def hello_world():
    html = open('index.html', 'r').read()
    status = 'UNPAUSED'
    if os.path.exists('current_song'):
        status = open('current_song').read()
    if os.path.exists('PAUSE'):
        status = 'PAUSED'
    html = html.replace('{{status}}', status)
    html = html.replace('{{songlist}}', tagged_songlist('music'))
    return flask.Markup(html)

@app.route('/unpause')
def unpause():
    if os.path.exists('PAUSE'):
        os.remove('PAUSE')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/pause')
def pause():
    if not os.path.exists('PAUSE'):
        open('PAUSE', 'w').close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/no_timer')
def no_timer():
    open('NO_TIMER', 'w').close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/reinstate_timer')
def reinstate_timer():
    if os.path.exists('NO_TIMER'):
        os.remove('NO_TIMER')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def tagged_songlist(music_folder):
    last_fn = 'last_played.pkl'
    last_played = pickle.load(open(last_fn))
    songs = ['%2d <b>%s<b>' % (i+1, song) for (i, song) in enumerate(reversed(last_played))]
    for song in sorted(os.listdir(music_folder)):
        if song not in last_played:
            songs.append(song)
    return '<br><br>\n'.join(songs)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)