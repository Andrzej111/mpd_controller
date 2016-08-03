#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections, subprocess, sys
import clip, keys
import json_wrappers
from lyrics_getter import get_lyrics

# radio stations i use,
STATIONS = {
    '1': ['PR Jedynka', 'mms://stream.polskieradio.pl/program1'],
    '2': ['PR Dwójka', 'mms://stream.polskieradio.pl/program2'],
    '3': ['PR Trójka', 'mms://stream.polskieradio.pl/program3'],
    '4': ['PR Czwórka', 'mms://stream.polskieradio.pl/program4']
}

PLAYLIST_STRING = 'list'

urls = (
    '/', 'index',
    '/list', 'list',                # returns playlist in json
    '/clear', 'clear',              # clears playlist
    '/playid/(.*)', 'playid',       # plays song from playlist (specified by id)
    '/searchid/(.*)', 'searchid',   # return info about song from playlist (spec. by id)
    '/playurl', 'playurl',          # plays song from network
    '/radio/(.*)', 'radio',
    '/radio', 'radio_list',
    '/volume/(.*)', 'volume',
    '/status', 'status',
    '/start', 'start',
    '/stop', 'stop',
    '/pause', 'pause',
    '/toggle', 'pause',
    '/next', 'next',
    '/prev', 'prev',
    '/search/(.*)', 'search',
    '/play/(.*)', 'play',
    '/current', 'current',
    '/lyrics', 'lyrics',

    ### not connected with music
    '/clip', 'clip.clip',
    '/keys/(.*)', 'keys.keys'
)

app = web.application(urls, globals())


# index_page = open('index.html', 'r').read()

class index:
    def GET(self):
        with open('index.html', 'r') as f:
            return f.read()


class list:
    def GET(self):
        with mc as client:
            playlist = client.playlistinfo()
            return json_wrappers.ok({PLAYLIST_STRING: playlist})


class volume:
    # I use amixer for that purpose
    def GET(self, arg):
        print (str(arg))
        if str(arg) in ['up', '+']:
            subprocess.Popen(["amixer", "-q", "set", "Master", "unmute"])
            subprocess.Popen(["amixer", "-q", "set", "Master", "5%+"])
        elif str(arg) in ['down', '-']:
            subprocess.Popen(["amixer", "-q", "set", "Master", "5%-"])
        else:
            subprocess.Popen(["amixer", "-q", "set", "Master", "unmute"])
            subprocess.Popen(["amixer", "-q", "set", "Master", "{}%".format(arg)])
        return json_wrappers.ok()

    def POST(self, volume_level):
        return self.GET(volume_level)


class playid:
    def GET(self, id):
        with mc as client:
            client.playid(id)
        return json_wrappers.ok()

    def POST(self, id): return self.GET(id)


class playurl:
    def GET(self):
        with mc as client:
            st_url = 'http://player.polskieradio.pl/-3'
            client.addid(st_url)
        return json_wrappers.ok()

    def POST(self):
        with mc as client:
            st_url = web.data()
            idd = client.addid(st_url)
            client.playid(idd)
        return json_wrappers.ok()


class radio_list:
    def GET(self):
        return json_wrappers.ok({PLAYLIST_STRING: STATIONS})


class radio:
    def GET(self, station):
        with mc as client:
            try:
                idd = client.addid(STATIONS[station][1])
                client.playid(idd)
            except:
                pass
        return json_wrappers.ok()


class stop:
    def GET(self):
        print ("stop")
        with mc as client:
            client.stop()
        return json_wrappers.ok()

    def POST(self): return self.GET()


class start:
    def GET(self):
        print ("start")
        with mc as client:
            client.play()
        return json_wrappers.ok()

    def POST(self): return self.GET()

class pause:
    def GET(self):
        print ("pause")
        with mc as client:
            client.pause()
        return json_wrappers.ok()

    def POST(self): return self.GET()


class clear:
    def GET(self):
        print ("clear")
        with mc as client:
            client.clear()
        return json_wrappers.ok()

    def POST(self): return self.GET()


class next:
    def GET(self):
        print ("next")
        with mc as client:
            client.next()
        return json_wrappers.ok()

    def POST(self): return self.GET()


class prev:
    def GET(self):
        print ("prev")
        with mc as client:
            client.next()
        return json_wrappers.ok()

    def POST(self): return self.GET()


class status:
    def GET(self):
        with mc as client:
            mpd_status = client.status()
            print ("status = " + str(mpd_status))
            return json_wrappers.ok({'response': mpd_status})


class current:
    def GET(self):
        with mc as client:
            return json_wrappers.ok({'response': client.currentsong()})

class lyrics:
    _cache = {}
    def GET(self):
        try:
            with mc as client:
                song = client.currentsong()
                text = ''
                try:
                    text = lyrics._cache[song['file']]
                except KeyError:
                    artist = song['artist']
                    title = song['title']
                    text = get_lyrics(artist,title)
                    lyrics._cache[song['file']] = text
                return json_wrappers.ok({'response': text})
        except Exception as e:
            print (e)
            return json_wrappers.fail()


class search:
    def GET(self, search):
        search_list = search.split('+')
        print ("search")
        llist = []
        with mc as client:
            for record in client.search_list(search_list):
                llist.append(record)
        return json_wrappers.ok({'list': llist})

    def POST(self, search): return self.GET(search)


class play:
    def GET(self, search):
        search_list = search.split('+')
        print ("play")
        index = 0
        with mc as client:
            for record in client.search_list(search_list):
                idd = client.addid(record['file'])
                if index == 0:
                    client.playid(idd)
                index += 1
            if index == 0:
                s = ' '.join(search_list)
                out = subprocess.check_output(['./find_yt_link.pl', s])
                print (out)
                idd = client.addid(out)
                client.playid(idd)
        return json_wrappers.ok()

    def POST(self, search):
        return self.GET(search)


# MPDClient object wrapper
class mpd_controller:
    def __init__(self, host="localhost", port=6600):
        self._client = mpd.MPDClient()
        self._host = host
        self._port = port
        try:
            self._client.connect(self._host, self._port)
        except mpd.ConnectionError:
            print ("already connected")
        self._client.disconnect()

    def get_client(self):
        try:
            self._client.connect(self._host, self._port)
        except mpd.ConnectionError:
            print ("already connected")
        return self._client

    def release_client(self):
        try:
            self._client.disconnect()
        except mpd.ConnectionError:
            print ("can't disconnect")

    def __enter__(self):
        return self.get_client()

    def __exit__(self, ex_t, ex_v, tb):
        self.release_client()
        return


### YUUUK, but hey, it works
def list_in_list(l1, l2):
    for v1 in l1:
        # str(s) to prevent double genre error (when it is list)
        if not any(v1.lower() in str(s).decode('utf-8').lower() for s in l2):
            return False
    return True


def search_against_list(client, search):
    for i in client.search('any', search[0]):
        if len(search) < 2:
            yield i
        else:
            if list_in_list(search[1:], i.values()):
                yield i
            else:
                continue
    return


mpd.MPDClient.search_list = search_against_list

mc = mpd_controller()

if __name__ == "__main__":
    app.run()
