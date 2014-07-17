import unittest
from Ranger.test.src.Range.RangeTestSuite import RangeTestSuite

class mainTestSuite(unittest.TestSuite):
    def __init__(self):
        super(mainTestSuite, self).__init__()
        self.addTest(RangeTestSuite())

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(mainTestSuite())
