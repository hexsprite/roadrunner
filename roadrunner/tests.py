"""
"""

import unittest


class TestRoadrunner(unittest.TestCase):
    def setUp(self):
        pass
    def test_stub(self):
        assert 1 == 1

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRoadrunner))
    return suite
    
if __name__ == '__main__':
    unittest.main()