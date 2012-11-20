'''
Created on Nov 18, 2012

@author: btbuxton
'''
import os
import os.path

from xml.dom.minidom import getDOMImplementation
from ftplib import FTP
from StringIO import StringIO

from itunes.parser import TracksParser
from itunes.common import print_timing

def main():
    itunes_path = os.path.expanduser(os.environ['ITUNES_LIBRARY_PATH'])
    print "Using: %s" % (itunes_path)
    ftp_site = os.environ['FTP_SITE']
    ftp_user = os.environ['FTP_USER']
    ftp_password = os.environ['FTP_PASS']
    ftp_path = os.environ['FTP_PATH']
    print "ftp: %s@%s %s" % (ftp_user, ftp_site, ftp_path)
    send = lambda xml: send_to_ftp(ftp_site, ftp_user, ftp_password, ftp_path, xml)
    xml = create_top_xml(itunes_path)
    print "Sending..."
    send(xml)
    print "DONE!"

def create_top_xml(itunes_path):
    dom = getDOMImplementation()
    doc = dom.createDocument(None, 'lfm', None)
    top_node = doc.documentElement
    top_artists_node = doc.createElement('topartists')
    top_node.appendChild(top_artists_node)
    
    with open(itunes_path, 'r') as stream:
        for i, [artist, total] in list(enumerate(top_artists(stream, 200))):
            artist_node = doc.createElement('artist')
            top_artists_node.appendChild(artist_node)
            artist_node.setAttribute('rank', str(i + 1))
            create_node = lambda key, value: create_key_value(doc, artist_node, key, value)
            create_node('name', artist)
            create_node('playcount', total.value)
            create_node('playtime', total.value)
            create_node('time', total)
            print 'Writing %d. %s %s' % (i + 1, artist, str(total))
            
    io = StringIO() 
    doc.writexml(io, indent=" ", addindent=" ", newl="\n", encoding='UTF-8')
    io.seek(0)
    return io

def create_key_value(doc, parent, key, value):
    node = doc.createElement(key)
    parent.appendChild(node)
    node.appendChild(doc.createTextNode(str(value)))

def send_to_ftp(site, user, password, path, stream):
    ftp = FTP(site)
    try:
        ftp.login(user, password)
        ftp.storbinary('STOR %s' % (path), stream)
        ftp.quit()
    finally:
        ftp.close()
    

@print_timing
def top_artists(stream, depth):
    return sorted(artist_play_times(stream), key=lambda tup: tup[1], reverse=True)[:depth]
    
def artist_play_times(stream):
    artist_total = {}
    for track in TracksParser(stream):
        if track.total_time is None: continue
        if track.play_count is None: continue
        time = Duration(track.total_time) * track.play_count
        artist = track.artist_name
        if track.album_artist_name is not None: artist = track.album_artist_name
        try:
            artist_total[artist] += time
        except KeyError:
            artist_total[artist] = time
    return artist_total.items()

        
class Duration:
    def __init__(self, initial=0):
        self.value = initial
    def __add__(self, another):
        return Duration(self.value + another.value)
    def __mul__(self, number):
        return Duration(self.value * number)
    def __str__(self):
        rest = self.value // 1000
        seconds = rest % 60
        rest = rest // 60
        minutes = rest % 60
        hours = rest // 60
        return '%d:%02d:%02d' % (hours, minutes, seconds)
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value
    def __hash__(self):
        return hash(self.value)
    
    
if __name__ == '__main__':
    main()
