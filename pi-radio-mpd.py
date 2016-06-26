#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess,sys
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
    '/list', 'list',            # returns playlist in json
    '/clear', 'clear',          # clears playlist
    '/playid/(.*)','playid',    # plays song from playlist (specified by id) 
    '/playurl','playurl',       # plays song from network 
    '/radio/(.*)','radio',
    '/radio','radio_list',
    '/volume/(.*)', 'volume',
    '/stop', 'stop',
    '/status', 'status',
    '/pause','pause',
    '/start','start',
    '/next','next',
    '/prev','prev',
    '/search/(.*)','search',
    '/play/(.*)','play',
    
### not connected with music
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
        with mc as client:
            st_url=web.data()
            idd = client.addid(st_url)#] = 'Trojka'
            client.playid(idd)
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

class search:
    def GET(self,search):
        search_list = search.split('+')
    	print "search"
        llist = []
        with mc as client:
            for record in client.search_list(search_list):
                llist.append(record)
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0', 'list':llist }, separators=(',',':') ))


    def POST(self,search): return self.GET(search)

class play:
    def GET(self,search):
        search_list = search.split('+')
    	print "play"
        index = 0
        with mc as client:
            for record in client.search_list(search_list):
                idd = client.addid(record['file'])
                if index==0:
                    client.playid(idd)
                index+=1
            if index==0:
                s = ' '.join(search_list)
                out = subprocess.check_output(['./find_yt_link.pl',s])
                print out
                idd = client.addid(out)
                client.playid(idd)
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))


    def POST(self,search): return self.GET(search)

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

### YUUUK, but hey, it works
def list_in_list(l1,l2):
    for v1 in l1:
        print v1
    if not any(v1.lower() in s.decode('utf-8').lower() for s in l2):
            return False
    return True
def search_against_list(client, search):
    for i in client.search('any',search[0]):
        if len(search)<2:
            yield i
        else:
            if list_in_list(search[1:],i.values()):
                yield i
            else:
                continue
    return

mpd.MPDClient.search_list = search_against_list

mc = mpd_controller()

if __name__ == "__main__":
    app.run()
#    search=sys.argv[1:]
#    with mc as client:
#        for o in client.search_list(search):
#            print "AAA",o

