'''
Created on Feb 27, 2010

@author: btbuxton
'''

import sqlite3
import itunes.domain as domain

class DomainStore(object):
    mapping = {
        domain.Genre: lambda store,object: store.save_genre(object),
        domain.Artist: lambda store,object: store.save_artist(object),
        domain.Album: lambda store,object: store.save_album(object),
        domain.Song: lambda store,object: store.save_song(object)
    }
    def __init__(self, file_name=None):
        if file_name is None:
            self.file_name = ":memory:"
        else:
            self.file_name = file_name
        
    def __enter__(self):
        self.conn=sqlite3.connect(self.file_name)
        self.curs = self.conn.cursor()
        self.reset()
        domain.Domain.register_store(self)
        return self
        
    def __exit__(self, type, value, traceback):
        self.commit()
        self.conn.close()
        
    def create_meta(self):
        self.curs.execute('''create table genre(id integer primary key, name text unique)''')
        self.curs.execute('''create table artist(id integer primary key, genre_id integer, name text)''')
        self.curs.execute('''create table album(id integer primary key, artist_id integer, name text, year integer)''')
        self.curs.execute('''create table song(id integer primary key, itunes_id integer, album_id integer, disc_number integer, last_played integer, play_count integer, title text, total_time integer, track_number integer)''')
        self.commit()
    
    def reset(self):
        self.to_save=[]
    
    def commit(self):
        for each in self.to_save:
            self.store_to_db(each)
        self.conn.commit()
        self.reset()
        
    def save(self, object):
        if hasattr(object, "store_id"):
            print "gotcha!"
        self.to_save.append(object)
        
    def store_to_db(self, object):
        try:
            self.mapping[object.__class__](self, object)
        except KeyError:
            pass
        
    def save_genre(self, object):
        self.curs.execute('insert into genre(name) values (?)', (object.name,))
        object.store_id=self.curs.lastrowid
    def save_artist(self, object):
        self.curs.execute('insert into artist(genre_id,name) values (?,?)', (object.genre.store_id,object.name))
        object.store_id=self.curs.lastrowid
    def save_album(self, object):
        self.curs.execute('insert into album(artist_id,name,year) values (?,?,?)', (object.artist.store_id,object.name,object.year))
        object.store_id=self.curs.lastrowid
    def save_song(self, object):
        self.curs.execute('insert into song(itunes_id, album_id, disc_number, last_played, play_count, title, total_time, track_number) values (?,?,?,?,?,?,?,?)', (object.itunes_id,object.album.store_id,object.disc_number,object.last_played, object.play_count,object.title,object.total_time,object.track_number))
        object.store_id=self.curs.lastrowid
    

        