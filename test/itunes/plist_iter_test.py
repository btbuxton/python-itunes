'''
Created on Sep 21, 2012

@author: btbuxton
'''
import unittest
import StringIO
import time
from itunes.plist_iter import PlistIter, START_DICT, END_DICT, KEY, VALUE

class Test(unittest.TestCase):
    def test_all(self):
        all_expected_events=[
            [START_DICT, None],
            [KEY, 'Major Version'],
            [VALUE, 1],
            [KEY, 'Date'],
            [VALUE, time.strptime('2012-09-22T01:07:25Z', '%Y-%m-%dT%H:%M:%SZ')],
            [KEY, u'Application Version'],
            [VALUE, '10.7'],
            [KEY, 'Show Content Ratings'],
            [VALUE, True],
            [VALUE, 'file://localhost/Users/btbuxton/Music/iTunes/iTunes%20Media/'],
            [KEY, 'Tracks'],
            [START_DICT, None],
            [KEY, '5014'],
            [START_DICT, None],
            [KEY, 'Track ID'],
            [VALUE, 5014],
            [END_DICT, None],
            [END_DICT, None],
            [END_DICT, None]
        ]
        stream = self.get_stream()
        plist = PlistIter(stream)
        for expected in all_expected_events:
            actual = plist.next()
            self.assertEquals(expected[0], actual[0])
            self.assertEquals(expected[1], actual[1])
        self.assertRaises(StopIteration, plist.next)

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
        </dict>
    </dict>
</dict>
'''[1:-1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()