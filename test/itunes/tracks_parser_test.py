'''
Created on Sep 22, 2012

@author: btbuxton
'''
import unittest
import StringIO
from itunes.parser import TracksParser

class Test(unittest.TestCase):


    def test_all(self):
        stream = self.get_stream()
        all = iter(TracksParser(stream))
        track = all.next()
        self.assertEquals(70960, track.total_time)
        track = all.next()
        self.assertEquals(11, track.play_count)
        

    def get_stream(self):
        return StringIO.StringIO('''
<dict>
    <key>Major Version</key><integer>1</integer>
    <key>Date</key><date>2012-09-22T01:07:25Z</date>
    <key>Application Version</key><string>10.7</string>
    <key>Show Content Ratings</key><true/>
    <key>Music Folder</key><string>file://localhost/Users/btbuxton/Music/iTunes/iTunes%20Media/</string>
    <key>Tracks</key>
    <dict>
        <key>5014</key>
        <dict>
            <key>Track ID</key><integer>5014</integer>
            <key>Name</key><string>Space: 1999 Main Titles</string>
            <key>Artist</key><string>Barry Gray</string>
            <key>Album</key><string>Space: 1999 - Year 1</string>
            <key>Grouping</key><string>Soundtrack</string>
            <key>Genre</key><string>Soundtrack</string>
            <key>Kind</key><string>AAC audio file</string>
            <key>Size</key><integer>1188548</integer>
            <key>Total Time</key><integer>70960</integer>
            <key>Disc Number</key><integer>1</integer>
            <key>Disc Count</key><integer>1</integer>
            <key>Track Number</key><integer>1</integer>
            <key>Track Count</key><integer>15</integer>
            <key>Year</key><integer>1973</integer>
            <key>Date Modified</key><date>2011-06-10T04:09:10Z</date>
            <key>Date Added</key><date>2011-01-01T16:17:16Z</date>
            <key>Bit Rate</key><integer>128</integer>
            <key>Sample Rate</key><integer>44100</integer>
            <key>Play Count</key><integer>11</integer>
            <key>Play Date</key><integer>3384413219</integer>
            <key>Play Date UTC</key><date>2011-03-31T15:46:59Z</date>
            <key>Rating</key><integer>100</integer>
            <key>Album Rating</key><integer>100</integer>
            <key>Album Rating Computed</key><true/>
            <key>Persistent ID</key><string>A403E503C41FB3F4</string>
            <key>Track Type</key><string>File</string>
            <key>Location</key><string>file://localhost/Users/btbuxton/Music/iTunes/iTunes%20Media/Music/Barry%20Gray/Space_%201999%20-%20Year%201/01%20Space_%201999%20Main%20Titles.m4a</string>
            <key>File Folder Count</key><integer>5</integer>
            <key>Library Folder Count</key><integer>1</integer>
        </dict>
        <key>5016</key>
        <dict>
            <key>Track ID</key><integer>5016</integer>
            <key>Name</key><string>Breakaway</string>
            <key>Artist</key><string>Barry Gray</string>
            <key>Album</key><string>Space: 1999 - Year 1</string>
            <key>Grouping</key><string>Soundtrack</string>
            <key>Genre</key><string>Soundtrack</string>
            <key>Kind</key><string>AAC audio file</string>
            <key>Size</key><integer>12233036</integer>
            <key>Total Time</key><integer>754946</integer>
            <key>Disc Number</key><integer>1</integer>
            <key>Disc Count</key><integer>1</integer>
            <key>Track Number</key><integer>2</integer>
            <key>Track Count</key><integer>15</integer>
            <key>Year</key><integer>1973</integer>
            <key>Date Modified</key><date>2011-06-10T04:09:10Z</date>
            <key>Date Added</key><date>2011-01-01T16:17:17Z</date>
            <key>Bit Rate</key><integer>128</integer>
            <key>Sample Rate</key><integer>44100</integer>
            <key>Play Count</key><integer>11</integer>
            <key>Play Date</key><integer>3384413974</integer>
            <key>Play Date UTC</key><date>2011-03-31T15:59:34Z</date>
            <key>Rating</key><integer>100</integer>
            <key>Album Rating</key><integer>100</integer>
            <key>Album Rating Computed</key><true/>
            <key>Persistent ID</key><string>5BB0E47218B5EB79</string>
            <key>Track Type</key><string>File</string>
            <key>Location</key><string>file://localhost/Users/btbuxton/Music/iTunes/iTunes%20Media/Music/Barry%20Gray/Space_%201999%20-%20Year%201/02%20Breakaway.m4a</string>
            <key>File Folder Count</key><integer>5</integer>
            <key>Library Folder Count</key><integer>1</integer>
        </dict>
    </dict>
</dict>
'''[1:-1])
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()