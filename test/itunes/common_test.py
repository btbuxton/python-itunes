'''
Created on Sep 8, 2012

@author: btbuxton
'''
import unittest

from itunes.common import func_and, func_or, every_do

class CommonTest(unittest.TestCase):
    def testFuncOr(self):
        self.assertTrue(func_or(lambda: True, lambda: True)(), "T | T = T")
        self.assertTrue(func_or(lambda: True, lambda: False)(), "T | F = T")
        self.assertTrue(func_or(lambda: False, lambda: True)(), "F | T = T")
        self.assertFalse(func_or(lambda: False, lambda: False)(), "F | F = F")
        
    def testFuncAnd(self):
        self.assertTrue(func_and(lambda: True, lambda: True)(), "T & T = T")
        self.assertFalse(func_and(lambda: True, lambda: False)(), "T & F = F")
        self.assertFalse(func_and(lambda: False, lambda: True)(), "F & T = F")
        self.assertFalse(func_and(lambda: False, lambda: False)(), "F & F = F")

if __name__ == "__main__":
    unittest.main()