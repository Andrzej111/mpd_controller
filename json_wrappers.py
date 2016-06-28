#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
from functools import wraps

def json_ok(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        val = func(*args,**kwargs)
        web.header('Content-Type', 'application/json')
        dic = {'status':'0'}
        try:
            dic.update(val)
        except TypeError as e:
            pass
    	return json.dumps(dic, separators=(',',':') )

    return wrapper
