'''
Created on Jul 15, 2016

@author: btbuxton
'''

import unittest
import os

def main(top_path):
    suites = unittest.defaultTestLoader.discover('tests', top_level_dir = top_path)
    test_suite = unittest.TestSuite(suites)
    unittest.TextTestRunner().run(test_suite)
    
if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_use = os.path.abspath(os.path.join(this_dir, '..'))
    #sys.path.insert(0, path_to_use)
    #print(sys.path)
    main(path_to_use)
