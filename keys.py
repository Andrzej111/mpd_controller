#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
import os
import json_wrappers

env = os.environ.copy()
env['DISPLAY'] = ':0'

class keys:
    def GET(self,key_codes):
        import time
        time.sleep(2)
        p = subprocess.Popen(["xdotool","key",key_codes],env=env)
        return json_wrappers.ok()
        
    def POST(self,key_codes):
        import time
        time.sleep(2)
        data = web.data()
        p = subprocess.Popen(["xdotool","key",data],env=env)
        return json_wrappers.ok()
