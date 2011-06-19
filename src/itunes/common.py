'''
Created on Feb 14, 2010

@author: btbuxton
'''
import time
from functools import wraps
def print_timing(func):
    @wraps(func)
    def wrapper(*arg, **kwds):
        begin = time.time()
        result = func(*arg, **kwds)
        end = time.time()
        print '%s took %0.3f ms' % (func.func_name, (end - begin) * 1000.0)
        return result
    return wrapper

class PreviousIterator:
    def __init__(self, internal):
        self.internal=iter(internal)
    def next(self):
        if hasattr(self, "previous_value"):
            result=self.previous_value
            del self.previous_value
        else:
            result=self.last=self.internal.next()
        return result
    def previous(self):
        self.previous_value=self.last
    def __iter__(self):
        return self
    def __getattr__(self, name):
        return getattr(self.internal, name)
    
def func_and(*funcs):
    def result(*args,**kwds):
        for each in funcs:
            if not each(*args,**kwds): return False
        return True
    return result

def func_or(*funcs):
    def result(*args,**kwds):
        for each in funcs:
            if each(*args,**kwds): return True
        return False
    return result

def every_do(times, func):
    index=[0]
    def anon(*args, **kwds): 
        index[0] += 1
        if (index[0] >= times):
            index[0] = 0
            func(*args, **kwds)
    return anon