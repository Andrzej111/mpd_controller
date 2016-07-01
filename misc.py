#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
def debug(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            val = func(*args,**kwargs)
        except Exception as e:
            if __debug__:
                import pdb; 
                pdb.set_trace()
            else:
                raise e
        return val
    return wrapper
