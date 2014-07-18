import unittest
from Ranger.src.Range.Cut import Cut

debug = False

class CutTest(unittest.TestCase):
    """ Unit Tests for Cut.py """
    # TODO: Write unit tests for __eq__, __lt__, __gt__, __le__, __ge__
    def test_isLessThanInt(self):
        if debug: print("Testing isLessThan with integers")
        ptCut = Cut(int, point=2, below=False)
        belowAllCut = Cut(int, belowAll=True)
        aboveAllCut = Cut(int, aboveAll = True)
        self.assertTrue(ptCut.isLessThan(3))
        self.assertFalse(ptCut.isLessThan(2))
        self.assertFalse(ptCut.isLessThan(1))
        self.assertTrue(belowAllCut.isLessThan(-999))
        self.assertFalse(aboveAllCut.isLessThan(1000))
    def test_isGreaterThanInt(self):
        if debug: print("Testing isGreaterThan with integers")
        ptCut = Cut(int, point=2, below=False)
        belowAllCut = Cut(int, belowAll=True)
        aboveAllCut = Cut(int, aboveAll = True)
        self.assertFalse(ptCut.isGreaterThan(3))
        self.assertTrue(ptCut.isGreaterThan(2))
        self.assertTrue(ptCut.isGreaterThan(1))
        self.assertFalse(belowAllCut.isGreaterThan(-999))
        self.assertTrue(aboveAllCut.isGreaterThan(1000))
    def test_belowValue(self):
        if debug: print("Testing belowValue")
        theCut = Cut.belowValue(2)
        self.assertFalse(theCut.belowAll)
        self.assertFalse(theCut.aboveAll)
        self.assertEqual(theCut.point, 2)
        self.assertTrue(theCut.below)
    def test_belowAll(self):
        if debug: print("Testing belowAll")
        theCut = Cut.belowAll(int)
        self.assertTrue(theCut.belowAll)
        self.assertFalse(theCut.aboveAll)
        self.assertIsNone(theCut.point)
    def test_aboveValue(self):
        if debug: print("Testing aboveValue")
        theCut = Cut.aboveValue(2)
        self.assertFalse(theCut.belowAll)
        self.assertFalse(theCut.aboveAll)
        self.assertEqual(theCut.point, 2)
        self.assertFalse(theCut.below)
    def test_aboveAll(self):
        if debug: print("Testing aboveAll")
        theCut = Cut.aboveAll(int)
        self.assertFalse(theCut.belowAll)
        self.assertTrue(theCut.aboveAll)
        self.assertIsNone(theCut.point)        
if __name__ == "__main__":
    debug = True
    unittest.main(exit=False)
