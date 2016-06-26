#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
import clip

# radio stations i use, 
STATIONS =  {
    '1':['PR Jedynka','mms://stream.polskieradio.pl/program1'],
    '2':['PR Dwójka','mms://stream.polskieradio.pl/program2'],
    '3':['PR Trójka','mms://stream.polskieradio.pl/program3'],
    '4':['PR Czwórka','mms://stream.polskieradio.pl/program4']
}


urls = (
    '/', 'index',
    '/list', 'list',
    '/clear', 'clear',
    '/playid/(.*)','playid',
    '/playurl','playurl',
    '/radio/(.*)','radio',
    '/radio','radio_list',
    '/volume/(.*)', 'volume',
    '/stop', 'stop',
    '/status', 'status',
    '/pause','pause',
    '/start','start',
    '/next','next',
    '/prev','prev',

    '/clip','clip.clip'
)

app = web.application(urls, globals())
index_page = open('index.html', 'r').read()

class index:
    def GET(self): return index_page

class list:
    def GET(self):
        with mc as client:
            playlist =  client.playlistinfo()
            # full info 
            print playlist
        web.header('Content-Type', 'application/json')
    	return (json.dumps({'status':'0','list': playlist}, separators=(',',':') ))

class volume:
# I use amixer for that purpose
    def GET(self, arg): 
        print str(arg)
        if str(arg) in ['up','+']:
           subprocess.Popen(["amixer", "-q","set","Master","unmute"])
           subprocess.Popen(["amixer", "-q","set","Master","5%+"])
        elif str(arg) in ['down','-']:
           subprocess.Popen(["amixer", "-q","set","Master","5%-"])
        else:
           subprocess.Popen(["amixer", "-q","set","Master","unmute"])
           subprocess.Popen(["amixer", "-q","set","Master","{}%".format(arg)])
  
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))

    def POST(self, volume_level): return self.GET(volume_level)

class playid:
    def GET(self, id):
        with mc as client:
            client.playid(id)
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self, id): return self.GET(id)

class playurl:
    def GET(self):
        with mc as client:
            st_url='http://player.polskieradio.pl/-3'
            client.addid(st_url)#] = 'Trojka'
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    # TODO
    def POST(self):
    	client = mc.get_client()
        st_url=web.data()
        client.addid(st_url)#] = 'Trojka'
    	mc.release_client()
class radio_list:
    def GET(self):
    	web.header('Content-Type', 'application/json')
    	return (json.dumps({'result':'0', 'list':STATIONS }, separators=(',',':') ))

class radio:
    def GET(self,station):
        with mc as client:
            try:
                idd = client.addid(STATIONS[station][1])
                client.playid(idd)
            except:
                pass
        
class stop:
    def GET(self):
    	print "stop"
        with mc as client:
            client.stop()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class start:
    def GET(self):
    	print "start"
        with mc as client:
            client.play()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class pause:
    def GET(self):
    	print "pause"
        with mc as client:
            client.pause()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class clear:
    def GET(self):
    	print "clear"
        with mc as client:
            client.clear()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class next:
    def GET(self):
    	print "next"
        with mc as client:
            client.next()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class prev:
    def GET(self):
    	print "prev"
        with mc as client:
            client.next()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
    def POST(self): return self.GET()

class status:
    def GET(self):
    	mpd_status = mc.get_client().status()
    	print "status = " + str(mpd_status)
    	mc.release_client()
    	return (json.dumps({'response' :  {'result' : 1} }, separators=(',',':') ))


class mpd_controller:
    def __init__(self, host="localhost", port=6600):
        self._client = mpd.MPDClient()
        self._host=host
        self._port=port
    	try:
    	    self._client.connect(self._host,self._port)
    	except mpd.ConnectionError:
    	    print "already connected"
    	self._client.disconnect()

    def get_client(self):
    	try:
    	    self._client.connect(self._host,self._port)
    	except mpd.ConnectionError:
    	    print "already connected"
    	return self._client

    def release_client(self):
    	try:
            self._client.disconnect()
    	except mpd.ConnectionError:
    	    print "can't disconnect"

    def __enter__(self):
        return self.get_client()

    def __exit__(self,ex_t,ex_v,tb):
        self.release_client()
        return

mc = mpd_controller()

if __name__ == "__main__":
    app.run()

