import unittest
from Ranger.test.src.Collections.RangeSetTest import RangeSetTest

class CollectionsTestSuite(unittest.TestSuite):
    def __init__(self):
        super(CollectionsTestSuite).__init__()
        self.addTest(unittest.makeSuite(RangeSetTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(RangeTestSuite())
