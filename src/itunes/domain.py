'''
Created on Feb 11, 2010

@author: btbuxton
'''

class Domain(object):
    stores=[]
    @classmethod
    def register_store(cls,store):
        cls.stores.append(store)
    def save(self):
        for each in self.stores:
            each.save(self)
        
class Genre(Domain):
    @classmethod
    def named(cls, name):
        try:
            return cls.cache[name]
        except AttributeError:
            cls.cache={}
            return cls.named(name)
        except KeyError:
            result = cls(name)
            result.save()
            cls.cache[name] = result
            return result
        
    def __init__(self,name):
        self.name=name
        self.artists={}
        
    def artist_named(self,name):
        try:
            return self.artists[name]
        except KeyError:
            result = Artist(self,name)
            result.save()
            self.artists[name]=result
            return result
        
    def __str__(self):
        return self.name

class Artist(Domain):
    def __init__(self,genre,name):
        self.genre=genre
        self.name=name
        self.albums={}
        
    def album_named(self,name):
        try:
            return self.albums[name]
        except KeyError:
            result = Album(self,name)
            result.save()
            self.albums[name]=result
            return result
    def __str__(self):
        return self.name

class Album(Domain):
    def __init__(self,artist,name):
        self.artist = artist
        self.name = name
    def __str__(self):
        return "\"%s\" by %s" % (self.name, self.artist)
    
class Song(Domain):
    
    def __init__(self, track):
        self.set_genre_from(track)
        self.set_artist_from(track)
        self.set_album_from(track)
        self.disc_number = track.disc_number
        self.itunes_id = track.itunes_id
        self.last_played = track.last_played
        self.play_count = track.play_count
        self.title = track.title
        self.total_time = track.total_time
        self.track_number = track.track_number
        self.album.year = track.year
        
    def set_genre_from(self, track):
        self.genre=Genre.named(track.genre_name)
        
    def set_artist_from(self, track):
        name = track.artist_name
        if track.album_artist_name is not None:
            name = track.album_artist_name
        self.artist=self.genre.artist_named(name)
        del self.genre
        
    def set_album_from(self, track):
        self.album=self.artist.album_named(track.album_name)
        del self.artist
    
    def __str__(self):
        return "\"%s\" on %s" % (self.title, self.album)
        
        