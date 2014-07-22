import unittest
from Ranger.test.src.Collections.RangeSetTest import RangeSetTest
from Ranger.test.src.Collections.RangeMapTest import RangeMapTest

class CollectionsTestSuite(unittest.TestSuite):
    def __init__(self):
        super(CollectionsTestSuite, self).__init__()
        self.addTest(unittest.makeSuite(RangeSetTest))
        self.addTest(unittest.makeSuite(RangeMapTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(CollectionsTestSuite())
