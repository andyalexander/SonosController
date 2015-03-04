import time
import hashlib
import json

import requests
from flask import Flask, render_template, url_for, request

import soco

app = Flask(__name__)

app.config.from_pyfile('settings.py')

components = list(soco.discover())
sonos = components[1]
print sonos.player_name
assert isinstance(sonos, soco.SoCo)
# sonos = SoCo(app.config['SPEAKER_IP'])
MAX_ITEMS = 1000


@app.route("/detail")
def getDetail():
    id = request.args.get('id','A:GENRE/Classical')
    type = request.args.get('type','genres')

    print id
    # print type

    temp = sonos.browse_by_idstring(type, id, max_items=MAX_ITEMS)
    parentId = temp[1].parent_id

    r = {'parentId':parentId}
    res = []
    for a in temp[1:]:
        istrack = True if a.item_class == u'object.item.audioItem.musicTrack' else False
        res.append({'title': a.title, 'id': a.item_id, 'uri': a.uri, 'istrack': istrack})

    # print res

    r['items'] = res
    ret = json.dumps(r)
    # print ret
    return ret

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


@app.route('/playTrack')
def play():
    uri = request.args.get('uri','')
    ret = ''

    if (id != ''):
        sonos.play_uri(uri)
        track = sonos.get_current_track_info()
        print "Playing: " + track['title']
        ret = uri
    return ret

@app.route('/getStatus')
def getStatus():
    state = sonos.get_current_transport_info();
    ret = {'name':sonos.player_name, 'state':state}
    return json.dumps(ret)

# pause if playing, play if paused.
@app.route('/playPause')
def pause():
    state = sonos.get_current_transport_info();
    print state

    if (state['current_transport_state'] == 'STOPPED' or state['current_transport_state'] == 'PAUSED_PLAYBACK'):
        sonos.play()
        return 'play'
    else:
        sonos.pause()
        return 'pause'




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
__author__ = 'Andrew'