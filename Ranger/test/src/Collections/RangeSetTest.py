import unittest
from Ranger.src.Collections.RangeSet import RangeSet
from Ranger.src.Range.Range import Range
from Ranger.src.Range.Cut import Cut

debug = False

class RangeSetTest(unittest.TestCase):
    """ Unit Tests for RangeSet.py """
    def test_add(self):
        if debug: print("Testing add with integers")
        theSet = RangeSet()
        # Adding initial part
        theSet.add(Range.closed(3,5))
        self.assertEqual(theSet.lower_cuts[0], Cut.belowValue(3))
        self.assertEqual(theSet.upper_cuts[0], Cut.aboveValue(5))
        self.assertEqual(len(theSet),1)
        # Adding distinct range above initial one
        theSet.add(Range.closed(7,10))
        self.assertEqual(len(theSet),2)
        self.assertEqual(theSet.ranges[1],Range.closed(7,10))
        self.assertEqual(theSet.ranges[0],Range.closed(3,5))
        # Adding range below/overlapping with initial one
        theSet.add(Range.closed(2,3))
        self.assertEqual(len(theSet),2)
        self.assertEqual(Range.closed(2,5), theSet.ranges[0])
        self.assertEqual(Cut.belowValue(2), theSet.lower_cuts[0])
        self.assertEqual(Cut.aboveValue(5), theSet.upper_cuts[0])
        self.assertEqual(Range.closed(7,10), theSet.ranges[1])
        self.assertEqual(Cut.belowValue(7), theSet.lower_cuts[1])
        self.assertEqual(Cut.aboveValue(10), theSet.upper_cuts[1])
        # Adding range above/overlapping second one
        theSet.add(Range.closed(9,11))
        self.assertEqual(len(theSet),2)
        self.assertEqual(Range.closed(7,11), theSet.ranges[1])
        self.assertEqual(Cut.belowValue(7), theSet.lower_cuts[1])
        self.assertEqual(Cut.aboveValue(11), theSet.upper_cuts[1])
        # Adding range encompasing second one
        theSet.add(Range.closed(6,12))
        self.assertEqual(len(theSet),2)
        self.assertEqual(Range.closed(6,12), theSet.ranges[1])
        self.assertEqual(Cut.belowValue(6), theSet.lower_cuts[1])
        self.assertEqual(Cut.aboveValue(12), theSet.upper_cuts[1])
        # Adding range encompassing all
        theSet.add(Range.closed(3, 11))
        self.assertEqual(len(theSet),1)
        self.assertEqual(len(theSet.lower_cuts),1)
        self.assertEqual(len(theSet.upper_cuts),1)
        self.assertEqual(Range.closed(2,12), theSet.ranges[0])
        self.assertEqual(Cut.belowValue(2), theSet.lower_cuts[0])
        self.assertEqual(Cut.aboveValue(12), theSet.upper_cuts[0])

    def test_contains(self):
        if debug: print("Testing contains")
        theSet = RangeSet()
        theSet.add(Range.closed(3,5))
        theSet.add(Range.closed(7,10))
        self.assertTrue(theSet.contains(4))
        self.assertFalse(theSet.contains(2))
        self.assertTrue(theSet.contains(Range.closed(4,5)))
        self.assertTrue(theSet.contains(Range.closed(8,9)))
        self.assertFalse(theSet.contains(Range.closed(1,4)))
        self.assertFalse(theSet.contains(Range.closed(6,6)))
        self.assertFalse(theSet.contains(Range.closed(8,12)))
if __name__ == "__main__":
    debug = True
    unittest.main(exit = False)
