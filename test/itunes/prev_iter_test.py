'''
Created on Sep 8, 2012

@author: btbuxton
'''
import unittest
from itunes.common import PreviousIterator

class PreviousIteratorTest(unittest.TestCase):
    def testSimple(self):
        orig = xrange(3)
        subject = PreviousIterator(orig)
        self.assertEqual(0, subject.next())
        self.assertEqual(1, subject.next())
        self.assertEqual(2, subject.next())
        self.assertRaises(StopIteration, subject.next)
    def testBackOne(self):
        orig = xrange(3)
        subject = PreviousIterator(orig)
        self.assertEqual(0, subject.next())
        self.assertEqual(1, subject.next())
        subject.previous()
        self.assertEqual(1, subject.next())
        self.assertEqual(2, subject.next())
        self.assertRaises(StopIteration, subject.next)
    def testBackTwo(self):
        orig = xrange(3)
        subject = PreviousIterator(orig)
        self.assertEqual(0, subject.next())
        self.assertEqual(1, subject.next())
        subject.previous()
        subject.previous()
        self.assertEqual(1, subject.next())
        self.assertEqual(2, subject.next())
        self.assertRaises(StopIteration, subject.next)

if __name__ == "__main__":
    unittest.main()

    