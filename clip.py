#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
import os
import json_wrappers

env = os.environ.copy()
env['DISPLAY'] = ':0'

class clip:
    def GET(self):
        retv = subprocess.check_output(["xclip","-o","-selection","clipboard"],env=env)
        web.header('Content-Type', 'text/plain; charset=utf-8')
        return retv
        
    def POST(self):
        data = web.data()
        p = subprocess.Popen(["xclip","-selection","clipboard"],env=env,stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.communicate()[0]
        p.stdin.close()
        json_wrappers.ok()
        
