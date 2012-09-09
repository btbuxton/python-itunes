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
        self.assertFalse(func_or()(), "F")
        
    def testFuncAnd(self):
        self.assertTrue(func_and(lambda: True, lambda: True)(), "T & T = T")
        self.assertFalse(func_and(lambda: True, lambda: False)(), "T & F = F")
        self.assertFalse(func_and(lambda: False, lambda: True)(), "F & T = F")
        self.assertFalse(func_and(lambda: False, lambda: False)(), "F & F = F")
        self.assertTrue(func_and()(), "T")
        
    def testEveryDo(self):
        result=[0]
        def addOne():
            result[0] += 1
        action = every_do(2, addOne)
        action()
        self.assertEqual(0, result[0])
        action()
        self.assertEqual(1, result[0])
        action()
        self.assertEqual(1, result[0])
        action()
        self.assertEqual(2, result[0])

if __name__ == "__main__":
    unittest.main()