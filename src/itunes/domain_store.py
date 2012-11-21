'''
Created on Feb 27, 2010

@author: btbuxton
'''

import sqlite3
import itunes.domain as domain

class DomainStore(object):
    mapping = {
        domain.Genre: lambda store,obj: store.save_genre(obj),
        domain.Artist: lambda store,obj: store.save_artist(obj),
        domain.Album: lambda store,obj: store.save_album(obj),
        domain.Song: lambda store,obj: store.save_song(obj)
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
        
    def save(self, obj):
        if hasattr(obj, "store_id"):
            print "gotcha!"
        self.to_save.append(obj)
        
    def store_to_db(self, obj):
        try:
            self.mapping[obj.__class__](self, obj)
        except KeyError:
            pass
        
    def save_genre(self, obj):
        self.curs.execute('insert into genre(name) values (?)', (obj.name,))
        obj.store_id=self.curs.lastrowid
    def save_artist(self, obj):
        self.curs.execute('insert into artist(genre_id,name) values (?,?)', (obj.genre.store_id,obj.name))
        obj.store_id=self.curs.lastrowid
    def save_album(self, obj):
        self.curs.execute('insert into album(artist_id,name,year) values (?,?,?)', (obj.artist.store_id,obj.name,obj.year))
        obj.store_id=self.curs.lastrowid
    def save_song(self, obj):
        self.curs.execute('insert into song(itunes_id, album_id, disc_number, last_played, play_count, title, total_time, track_number) values (?,?,?,?,?,?,?,?)', (obj.itunes_id,obj.album.store_id,obj.disc_number,obj.last_played, obj.play_count,obj.title,obj.total_time,obj.track_number))
        obj.store_id=self.curs.lastrowid
    

        