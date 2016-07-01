#!/usr/bin/python
# -*- coding: utf-8 -*-

import web, json, time, mpd, collections,subprocess
from functools import wraps

def ok(d={}):
    web.header('Content-Type', 'application/json')
    dic = {'status':'0'}
    try:
        dic.update(d)
    except TypeError as e:
        pass
    return json.dumps(dic, separators=(',',':') )
