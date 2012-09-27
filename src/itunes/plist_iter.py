'''
Created on Sep 21, 2012

@author: btbuxton
'''
import xml.dom.pulldom as pulldom
import time

START_DICT = 'START_DICT'
END_DICT = 'END_DICT'
KEY = 'KEY'
VALUE = 'VALUE'

_IS_ELEMENT_START=lambda (elmt_type,node): elmt_type == pulldom.START_ELEMENT
_IS_ELEMENT_END=lambda(elmt_type,node): elmt_type == pulldom.END_ELEMENT
_IS_CHARACTERS=lambda (elmt_type,node): elmt_type == pulldom.CHARACTERS
_IS_NAME=lambda name: lambda (elmt_type,node): node.nodeName == name
_IS_KEY=_IS_NAME('key')
_IS_DICT=_IS_NAME('dict')

_VALUE_CONVERTER={
    'integer': lambda value: int(value),
    'string': lambda value: value,
    'date': lambda value: time.strptime(value, '%Y-%m-%dT%H:%M:%SZ'),
    'true': lambda value: True,
    'false': lambda value: False
}

class PlistIter:
    def __init__(self,stream):
        self._parser = pulldom.parse(stream)
    
    def __iter__(self):
        return self
        
    def next(self):
        event = self.next_event()
        if event: return event
        raise StopIteration
    
    def next_event(self):
        for element in self._parser:
            if _IS_ELEMENT_START(element): 
                if _IS_KEY(element):
                    return [KEY, self._parse_key()]
                if _IS_DICT(element):
                    return [START_DICT, None]
                kind = element[1].nodeName
                if _VALUE_CONVERTER.__contains__(kind):
                    return [VALUE, self._parse_simple_value(kind)]
            elif _IS_ELEMENT_END(element):
                if _IS_DICT(element):
                    return [END_DICT, None]
        return None
                    
    def _parse_key(self):
        name=self._parser.next()[1].nodeValue
        self._eat_till_end()
        return name
    
    def _parse_simple_value(self, kind):
        next=self._parser.next()
        value=_VALUE_CONVERTER[kind](next[1].nodeValue)
        if not _IS_ELEMENT_END(next): self._eat_till_end()
        return value
    
    def _eat_till_end(self):
        while True:
            next = self._parser.next()
            if _IS_ELEMENT_END(next): break