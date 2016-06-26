#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
import os

env = os.environ.copy()
env['DISPLAY'] = ':0'

class clip:
    def GET(self):
        retv = subprocess.check_output(["xclip","-o","-selection","clipboard"],env=env)
        web.header('Content-Type', 'text/plain; charset=utf-8')
        print '--'*20
        print retv
        print '--'*20
        return retv
        
    def POST(self):
        data = web.data()
        p = subprocess.Popen(["xclip","-selection","clipboard"],env=env,stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.communicate()[0]
        p.stdin.close()
        web.header('Content-Type', 'application/json')
        return (json.dumps({'status':'0' }, separators=(',',':') ))
        
