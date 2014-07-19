import unittest
from Ranger.test.src.Range.CutTest import CutTest
from Ranger.test.src.Range.RangeTest import RangeTest

class RangeTestSuite(unittest.TestSuite):
    def __init__(self):
        super(RangeTestSuite, self).__init__()
        self.addTest(unittest.makeSuite(CutTest))
        self.addTest(unittest.makeSuite(RangeTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(RangeTestSuite())
