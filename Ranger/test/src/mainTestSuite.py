import unittest
from Ranger.test.src.Range.RangeTestSuite import RangeTestSuite
from Ranger.test.src.Collections.CollectionsTestSuite import CollectionsTestSuite

class mainTestSuite(unittest.TestSuite):
    def __init__(self):
        super(mainTestSuite, self).__init__()
        self.addTest(RangeTestSuite())
        self.addTest(CollectionsTestSuite())

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(mainTestSuite())
