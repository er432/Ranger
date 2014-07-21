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
    def test_overlaps(self):
        if debug: print("Testing overlaps")
        theSet = RangeSet()
        theSet.add(Range.closed(3,5))
        theSet.add(Range.closed(7,10))
        self.assertTrue(theSet.overlaps(4))
        self.assertFalse(theSet.overlaps(2))
        self.assertTrue(theSet.overlaps(3))
        self.assertTrue(theSet.overlaps(10))
        self.assertTrue(theSet.overlaps(Range.closed(4,5)))
        self.assertTrue(theSet.overlaps(Range.closed(8,9)))
        self.assertTrue(theSet.overlaps(Range.closed(1,4)))
        self.assertFalse(theSet.overlaps(Range.closed(6,6)))
        self.assertTrue(theSet.overlaps(Range.closed(8,12)))
        self.assertTrue(theSet.overlaps(Range.closed(1,12)))
    def test_union(self):
        if debug: print("Testing union")
        firstSet = RangeSet([Range.closed(3,5), Range.closed(7,10)])
        secondSet = RangeSet([Range.closed(2,4), Range.closed(5, 11),
                              Range.closed(13, 15)])
        union = firstSet.union(secondSet)
        self.assertEqual(union, RangeSet([Range.closed(2,11),
                                          Range.closed(13,15)]))
    def test_difference(self):
        if debug: print("Testing difference")
        startSet = RangeSet([Range.closed(3,5),Range.closed(7,10)])
        diffSet = startSet.difference(RangeSet([Range.closed(4,6)]))
        self.assertEqual(diffSet,
                         RangeSet([Range.closedOpen(3,4),
                                   Range.closed(7,10)]))
        diffSet = startSet.difference(RangeSet([Range.closed(2,6)]))
        self.assertEqual(diffSet,
                         RangeSet([Range.closed(7,10)]))
        diffSet = startSet.difference(RangeSet([Range.closed(-2,1)]))
        self.assertEqual(diffSet, startSet)
        diffSet = startSet.difference(RangeSet([Range.closed(1,3),
                                                Range.closed(6,9)]))
        self.assertEqual(diffSet,
                         RangeSet([Range.openClosed(3,5),
                                   Range.openClosed(9,10)]))
        diffSet = startSet.difference(RangeSet([Range.closed(1,11)]))
        self.assertEqual(len(diffSet),0)
if __name__ == "__main__":
    debug = True
    unittest.main(exit = False)
