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
        # Integers
        intRange = Range.closed(2,5)
        self.assertTrue(intRange.contains(2))
        self.assertFalse(intRange.contains(1))
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
        with self.assertRaises(TypeError):
            Range.open(3.,3.)
        # Letters
        letterRange = Range.open('b','e')
        self.assertFalse(letterRange.contains('a'))
        self.assertFalse(letterRange.contains('b'))
        self.assertTrue(letterRange.contains('c'))
        self.assertFalse(letterRange.contains('e'))
        self.assertFalse(letterRange.contains('f'))
        with self.assertRaises(TypeError):
            Range.open('b','b')
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
    def test_hasLowerBound(self):
        if debug: print("Testing hasLowerBound")
        self.assertTrue(Range.atLeast(5.).hasLowerBound())
        self.assertFalse(Range.atMost(5.).hasLowerBound())
        self.assertTrue(Range.closed(2.,5.).hasLowerBound())
    def test_hasUpperBound(self):
        if debug: print("Testing hasUpperBound")
        self.assertFalse(Range.atLeast(5.).hasUpperBound())
        self.assertTrue(Range.atMost(5.).hasUpperBound())
        self.assertTrue(Range.closed(2.,5.).hasUpperBound())
    def test_lowerEndpoint(self):
        if debug: print("Testing lowerEndpoint")
        with self.assertRaises(TypeError):
            Range.atMost(5.).lowerEndpoint()
        self.assertEqual(Range.atLeast(5.).lowerEndpoint(),5.)
        self.assertEqual(Range.closed(5.,10.).lowerEndpoint(),5.)
    def test_upperEndpoint(self):
        if debug: print("Testing upperEndpoint")
        with self.assertRaises(TypeError):
            Range.atLeast(5.).upperEndpoint()
        self.assertEqual(Range.atMost(5.).upperEndpoint(),5.)
        self.assertEqual(Range.closed(5.,10.).upperEndpoint(),10.)
    def test_isLowerBoundClosed(self):
        if debug: print("Testing isLowerBoundClosed")
        with self.assertRaises(TypeError):
            Range.atMost(5.).isLowerBoundClosed()
        self.assertTrue(Range.closedOpen(5.,10.).isLowerBoundClosed())
        self.assertFalse(Range.openClosed(5.,10.).isLowerBoundClosed())
    def test_isUpperBoundClosed(self):
        if debug: print("Testing isUpperBoundClosed")
        with self.assertRaises(TypeError):
            Range.atLeast(5.).isUpperBoundClosed()
        self.assertFalse(Range.closedOpen(5.,10.).isUpperBoundClosed())
        self.assertTrue(Range.openClosed(5.,10.).isUpperBoundClosed())
    def test_isEmpty(self):
        if debug: print("Testing isEmpty")
        self.assertTrue(Range.closedOpen(3.,3.).isEmpty())
        self.assertTrue(Range.openClosed(3.,3.).isEmpty())
        self.assertFalse(Range.openClosed(3.,3.001).isEmpty())
    def test_containsAll(self):
        if debug: print("Testing containsAll")
        self.assertTrue(Range.openClosed(3.,5.).containsAll([4.,4.5,5.]))
        self.assertFalse(Range.closedOpen(3.,5.).containsAll([4.,4.5,5.]))
        self.assertFalse(Range.closedOpen(3.,5.).containsAll([3.,4.,5.]))
        self.assertFalse(Range.closedOpen(3.,5.).containsAll([2.,4.,5.]))
    def test_encloses(self):
        if debug: print("Testing encloses")
        range1 = Range.closed(3.,6.)
        range2 = Range.closed(4.,5.)
        self.assertTrue(range1.encloses(range2))
        range1 = Range.open(3.,6.)
        range2 = Range.open(3.,6.)
        self.assertTrue(range1.encloses(range2))
        range2 = Range.closed(4.,4.)
        self.assertTrue(range1.encloses(range2))
        range1 = Range.openClosed(3.,6.)
        range2 = Range.closed(3.,6.)
        self.assertFalse(range1.encloses(range2))
        self.assertTrue(range2.encloses(range1))
        range1 = Range.closed(4.,5.)
        range2 = Range.open(3.,6.)
        self.assertFalse(range1.encloses(range2))
        self.assertTrue(range2.encloses(range1))
    def test_isConnected(self):
        if debug: print("Testing isConnected")
        range1 = Range.closed(2.,4.)
        range2 = Range.closed(5.,7.)
        self.assertFalse(range1.isConnected(range2))
        range2 = Range.closed(3.,5.)
        self.assertTrue(range1.isConnected(range2))
        range2 = Range.closed(4.,6.)
        self.assertTrue(range1.isConnected(range2))
    def test_intersection(self):
        if debug: print("Testing intersection")
        range1 = Range.closed(1.,5.)
        range2 = Range.closed(3.,7.)
        self.assertEqual(range1.intersection(range2),
                         Range.closed(3.,5.))
        range2 = Range.closed(5.,7.)
        self.assertEqual(range1.intersection(range2),
                         Range.closed(5.,5.))
        range2 = Range.closed(6.,7.)
        with self.assertRaises(ValueError):
            range1.intersection(range2)
    def test_span(self):
        if debug: print("Testing span")
        range1 = Range.closed(1.,3.)
        range2 = Range.closed(5.,7.)
        self.assertEqual(range1.span(range2),
                         Range.closed(1.,7.))
        range2 = Range.closed(2.,5.)
        self.assertEqual(range1.span(range2),
                         Range.closed(1.,5.))
    def test_getDistanceFromPoint(self):
        if debug: print("Testing getDistanceFromPoint")
        range1 = Range.closed(1.,3.)
        self.assertAlmostEqual(range1.getDistanceFromPoint(1.),0.)
        self.assertAlmostEqual(range1.getDistanceFromPoint(2.),0.)
        self.assertAlmostEqual(range1.getDistanceFromPoint(3.),0.)
        self.assertAlmostEqual(range1.getDistanceFromPoint(100.),97.)
        self.assertAlmostEqual(range1.getDistanceFromPoint(0.99),0.01)
        range1 = Range.openClosed(1.,3.)
        with self.assertRaises(TypeError):
            range1.getDistanceFromPoint(0.99)
    def test_getDistanceFromRange(self):
        if debug: print("Testing getDistanceFromRange")
        range1 = Range.closed(1.,3.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(5.,7.)),2.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(-1.,0.)),1.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(-5.,10.)),0.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(-5.,2.)),0.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(2.,10.)),0.)
        self.assertAlmostEqual(range1.getDistanceFromRange(Range.closed(1.5,2.1)),0.)
        with self.assertRaises(TypeError):
            range1.getDistanceFromRange(Range.closedOpen(1.5,2.1))
if __name__ == "__main__":
    debug = True
    unittest.main(exit = False)
