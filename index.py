"""Main python file"""
# import time
# import hashlib
import json

# import requests
from flask import Flask, request

import soco

def getSonosForRoom(roomName):
    for c in COMPONENTS:
        if (c.player_name == roomName):
            return c



APP = Flask(__name__)

APP.config.from_pyfile('settings.py')

COMPONENTS = list(soco.discover())
sonos = getSonosForRoom('Kitchen')

print sonos.player_name
assert isinstance(sonos, soco.SoCo)
MAX_ITEMS = 500


@APP.route("/detail")
def getDetail():
    id = request.args.get('id', 'A:GENRE/Classical')
    type = request.args.get('type', 'genres')
    room = request.args.get('room', 'Kitchen')

    print id
    # print type

    temp = sonos.browse_by_idstring(type, id, max_items=MAX_ITEMS)
    r = {'parentId':''}
    res = []

    if len(temp)>0:
        parentId = temp[0].parent_id
        r = {'parentId':parentId}

        for a in temp[0:]:
            # print a.item_id
            # if a.item_id.startswith('A:ALBUM/Elgar'):
            #     q = 1

            istrack = True if a.item_class == u'object.item.audioItem.musicTrack' else False
            res.append({'title': a.title, 'id': a.item_id, 'uri': a.uri, 'istrack': istrack})

        # print res

    r['items'] = res
    ret = json.dumps(r)
    # print ret
    return ret

@APP.route('/')
def root():
  return APP.send_static_file('index.html')

@APP.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return APP.send_static_file(path)


@APP.route('/playTrack')
def play():
    uri = request.args.get('uri','')
    ret = ''

    if (id != ''):
        sonos.play_uri(uri)
        track = sonos.get_current_track_info()
        print "Playing: " + track['title']
        ret = uri
    return ret

@APP.route('/getStatus')
def getStatus():
    state = sonos.get_current_transport_info()
    ret = {'name':sonos.player_name, 'state':state}
    return json.dumps(ret)

# pause if playing, play if paused.
@APP.route('/playPause')
def pause():
    state = sonos.get_current_transport_info()
    print state

    if (state['current_transport_state'] == 'STOPPED' or state['current_transport_state'] == 'PAUSED_PLAYBACK'):
        sonos.play()
        return 'play'
    else:
        sonos.pause()
        return 'pause'





if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0')
__author__ = 'Andrew'
