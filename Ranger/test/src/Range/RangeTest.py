import unittest
from Ranger.src.Range.Range import Range

debug = False

class RangeTest(unittest.TestCase):
    """ Unit Tests for Range.py """
    def test_closed(self):
        if debug: print("Testing closed")
        # Floats
        floatRange = Range.closed(2.,5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertTrue(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertTrue(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.closed('b','e')
        self.assertFalse(letterRange.contains('a'))
        self.assertTrue(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertTrue(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_closedOpen(self):
        if debug: print("Testing closedOpen")
        # Floats
        floatRange = Range.closedOpen(2.,5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertTrue(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertFalse(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.closedOpen('b','e')
        self.assertFalse(letterRange.contains('a'))
        self.assertTrue(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertFalse(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_openClosed(self):
        if debug: print("Testing openClosed")
        # Floats
        floatRange = Range.openClosed(2.,5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertFalse(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertTrue(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.openClosed('b','e')
        self.assertFalse(letterRange.contains('a'))
        self.assertFalse(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertTrue(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_open(self):
        if debug: print("Testing open")
        # Floats
        floatRange = Range.open(2.,5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertFalse(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertFalse(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.open('b','e')
        self.assertFalse(letterRange.contains('a'))
        self.assertFalse(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertFalse(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_lessThan(self):
        if debug: print("Testing lessThan")
        # Floats
        floatRange = Range.lessThan(5.)
        self.assertTrue(floatRange.contains(1.99))
        self.assertTrue(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertFalse(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.lessThan('e')
        self.assertTrue(letterRange.contains('a'))
        self.assertTrue(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertFalse(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_atMost(self):
        if debug: print("Testing atMost")
        # Floats
        floatRange = Range.atMost(5.)
        self.assertTrue(floatRange.contains(1.99))
        self.assertTrue(floatRange.contains(2.))
        self.assertTrue(floatRange.contains(3.))
        self.assertTrue(floatRange.contains(5.))
        self.assertFalse(floatRange.contains(5.01))
        # Letters
        letterRange = Range.atMost('e')
        self.assertTrue(letterRange.contains('a'))
        self.assertTrue(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertTrue(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
    def test_greaterThan(self):
        if debug: print("Testing greaterThan")
        # Floats
        floatRange = Range.greaterThan(5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertFalse(floatRange.contains(2.))
        self.assertFalse(floatRange.contains(3.))
        self.assertFalse(floatRange.contains(5.))
        self.assertTrue(floatRange.contains(5.01))
        # Letters
        letterRange = Range.greaterThan('e')
        self.assertFalse(letterRange.contains('a'))
        self.assertFalse(letterRange.contains('b'))
        self.assertFalse(letterRange.contains('c'))
        self.assertFalse(letterRange.contains('e'))
        self.assertTrue(letterRange.contains('f'))
    def test_atLeast(self):
        if debug: print("Testing atLeast")
        # Floats
        floatRange = Range.atLeast(5.)
        self.assertFalse(floatRange.contains(1.99))
        self.assertFalse(floatRange.contains(2.))
        self.assertFalse(floatRange.contains(3.))
        self.assertTrue(floatRange.contains(5.))
        self.assertTrue(floatRange.contains(5.01))
        # Letters
        letterRange = Range.atLeast('e')
        self.assertFalse(letterRange.contains('a'))
        self.assertFalse(letterRange.contains('b'))
        self.assertFalse(letterRange.contains('c'))
        self.assertTrue(letterRange.contains('e'))
        self.assertTrue(letterRange.contains('f'))        
if __name__ == "__main__":
    debug = True
    unittest.main(exit = False)
