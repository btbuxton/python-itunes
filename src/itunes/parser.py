'''
Created on Feb 19, 2010

@author: btbuxton
'''
import itunes.plist_iter as plist_iter
import itunes.domain as domain
import itunes.domain_store as store
import os

from itunes.common import print_timing, every_do

_IS_END_DICT = lambda (elmt_type, value): elmt_type == plist_iter.END_DICT
_IS_KEY = lambda (elmt_type, value): elmt_type == plist_iter.KEY
_IS_TRACKS = lambda (elmt_type, value): _IS_KEY([elmt_type,value]) and value == 'Tracks'

class Track(object):
    def __init__(self, track_id):
        self.track_id = track_id
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
    
    def __init__(self, stream):
        self._plist_iter = plist_iter.PlistIter(stream)
    
    def _next_track(self):
        while not _IS_TRACKS(self._plist_iter.next()):
            pass
        self._plist_iter.next() #read START_DICT
        try:
            while True:
                next_elmt = self._plist_iter.next()
                if not _IS_KEY(next_elmt):
                    return
                id = next_elmt[1]
                self._plist_iter.next() #read START_DICT
                track = Track(id)
                next_key = None
                while True:
                    next_key = self._plist_iter.next()
                    if _IS_END_DICT(next_key): break
                    key = next_key[1]
                    next_value = self._plist_iter.next()
                    value = next_value[1]
                    try:
                        setattr(track, self.track_mapping[key], value)
                    except KeyError:
                        pass
                yield track
        except StopIteration:
            pass
    
    def __iter__(self):
        return self._next_track()

@print_timing
def main():
    with open('../../data/itunes_library.xml','r') as stream:
        parser = TracksParser(stream)
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
if __name__ == "__main__":
    main()
    print "DONE!"