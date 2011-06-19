'''
Created on Feb 19, 2010

@author: btbuxton
'''
import xml.dom.pulldom as pulldom
import itunes.domain as domain
import itunes.domain_store as store
import time
import os

from itunes.common import PreviousIterator, print_timing, func_and, every_do

is_element_start=lambda (type,node): type == pulldom.START_ELEMENT
is_element_end=lambda(type,node): type == pulldom.END_ELEMENT
is_characters=lambda (type,node): type == pulldom.CHARACTERS
is_name=lambda name: lambda (type,node): node.nodeName == name
is_key=is_name('key')
is_key_start = func_and(is_element_start, is_key)
is_key_end = func_and(is_element_end, is_key)
is_dict=is_name('dict')
is_dict_start = func_and(is_element_start, is_dict)
is_dict_end = func_and(is_element_end, is_dict)

class Track(object):
    def __init__(self, id):
        self.album_name = None
        self.album_artist_name = None
        self.artist_name = None
        self.disc_number = None
        self.genre_name = None
        self.itunes_id = id
        self.last_played = None
        self.play_count = 0
        self.title = ''
        self.total_time = None
        self.track_number = None
        self.year = None
    def is_valid(self):
        return not (self.title == 'Placeholder' \
            or self.album_name is None \
            or self.artist_name is None \
            or self.genre_name is None)


class TracksParser(object):
    track_mapping={
                  'Name': 'title',
                  'Artist': 'artist_name',
                  'Album': 'album_name',
                  'Album Artist': 'album_artist_name',
                  'Genre': 'genre_name',
                  'Total Time': 'total_time',
                  'Year': 'year',
                  'Play Count': 'play_count',
                  'Play Date': 'last_played',
                  'Persistent ID': 'persistent_id',
                  'Track Number': 'track_number',
                  'Disc Number': 'disc_number'
    }
    
    value_converter={
                     'integer': lambda value: int(value),
                     'string': lambda value: value,
                     'date': lambda value: time.strptime(value, '%Y-%m-%dT%H:%M:%SZ'),
                     'true': lambda value: True,
                     'false': lambda value: False
    }
    
    def __init__(self, library_name):
        self.library_name=library_name
        
    def __iter__(self):
        with open(self.library_name,'r') as stream:
            parser = PreviousIterator(pulldom.parse(stream))
            while True:
                value = self._get_key(parser) 
                if value == 'Tracks': break
                if value is None: parser.next()
            next=self._eat(parser)
            while True:
                key = self._get_key(parser) 
                if key is None: break
                next = self._eat(parser)
                if not is_dict_start(next): break
                track = self._get_track(parser, int(key))
                if track.is_valid():
                    yield track
                next = self._eat(parser)
            #print str(next)
            
    def _get_track(self, parser, id):
        track = Track(id)
        while True:
            key = self._get_key(parser)
            if key is None: break
            value = self._get_value(parser)
            if value is None: break
            try:
                setattr(track, self.track_mapping[key], value)
            except KeyError:
                pass
        return track
    
    def _get_key(self, parser):
        next = self._eat(parser)
        if (not is_key_start(next)):
            parser.previous()
            return None
        result = ''
        while True:
            next = parser.next()
            if is_key_end(next): break
            if is_characters(next): result=result + next[1].nodeValue
        return result
    
    def _get_value(self, parser):
        next = self._eat(parser)
        if (not is_element_start(next)):
            parser.previous()
            return None
        value_type = next[1].nodeName
        is_value_end=func_and(is_element_end, is_name(value_type))
        result = ''
        while True:
            next = parser.next()
            if is_value_end(next): break
            if is_characters(next): result=result + next[1].nodeValue
        return self.value_converter[value_type](result)
    
    def _eat(self,parser):
        while True: 
            next = parser.next()
            if not is_characters(next): break
        return next


@print_timing
def main():
    parser = TracksParser('../../data/itunes_library.xml')
    def commit(store):
        store.commit()
        print "commit"
    name='../../data/store.db'
    if os.path.isfile(name):
        os.remove(name)
    with store.DomainStore(name) as storage:
        do_commit=every_do(1024, lambda: commit(storage))
        storage.create_meta()
        for track in parser:
            domain.Song(track).save()
            do_commit()
    
main()
print "DONE!"