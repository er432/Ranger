import unittest
from Ranger.src.Collections.RangeMap import RangeMap
from Ranger.src.Range.Range import Range

debug = False

class RangeMapTest(unittest.TestCase):
    """ Unit Tests for RangeMap.py """
    def test_contains(self):
        if debug: print("Testing contains")
        theMap = RangeMap()
        theMap.put(Range.closed(3,5),'foo')
        theMap.put(Range.closed(7,10),'bar')
        self.assertTrue(theMap.contains(4))
        self.assertFalse(theMap.contains(2))
        self.assertTrue(theMap.contains(Range.closed(4,5)))
        self.assertTrue(theMap.contains(Range.closed(8,9)))
        self.assertFalse(theMap.contains(Range.closed(1,4)))
        self.assertFalse(theMap.contains(Range.closed(6,6)))
        self.assertFalse(theMap.contains(Range.closed(8,12)))
    def test_overlaps(self):
        if debug: print("Testing overlaps")
        theMap = RangeMap()
        theMap.put(Range.closed(3,5),'foo')
        theMap.put(Range.closed(7,10),'bar')
        self.assertTrue(theMap.overlaps(4))
        self.assertFalse(theMap.overlaps(Range.closedOpen(1,3)))
        self.assertFalse(theMap.overlaps(Range.open(5,7)))
        self.assertFalse(theMap.overlaps(2))
        self.assertTrue(theMap.overlaps(3))
        self.assertTrue(theMap.overlaps(10))
        self.assertTrue(theMap.overlaps(Range.closed(4,5)))
        self.assertTrue(theMap.overlaps(Range.closed(8,9)))
        self.assertTrue(theMap.overlaps(Range.closed(1,4)))
        self.assertFalse(theMap.overlaps(Range.closed(6,6)))
        self.assertTrue(theMap.overlaps(Range.closed(8,12)))
        self.assertTrue(theMap.overlaps(Range.closed(1,12)))    
    def test_put(self):
        if debug: print("Testing put")
        rangeMap = RangeMap()
        rangeMap.put(Range.closed(1,10),'foo')
        self.assertEqual(rangeMap.ranges[0], Range.closed(1,10))
        self.assertEqual(rangeMap.items[0], 'foo')
        rangeMap.put(Range.open(3,6), 'bar')
        self.assertEqual(rangeMap.ranges[0], Range.closed(1,3))
        self.assertEqual(rangeMap.ranges[1], Range.open(3,6))
        self.assertEqual(rangeMap.ranges[2], Range.closed(6,10))
        self.assertEqual(rangeMap.items[0],'foo')
        self.assertEqual(rangeMap.items[1], 'bar')
        self.assertEqual(rangeMap.items[2],'foo')
        rangeMap.put(Range.open(10,20), 'foo')
        self.assertEqual(len(rangeMap),4)        
        self.assertEqual(rangeMap.ranges[3], Range.open(10,20))
        self.assertEqual(rangeMap.items[0],'foo')
        self.assertEqual(rangeMap.items[1], 'bar')
        self.assertEqual(rangeMap.items[2],'foo')
        self.assertEqual(rangeMap.items[3],'foo')
    def test_remove(self):
        if debug: print("Testing remove")
        rangeMap = RangeMap()
        rangeMap.put(Range.closed(1,10),'foo')
        rangeMap.put(Range.open(3,6), 'bar')
        rangeMap.put(Range.open(10,20), 'foo')
        rangeMap.remove(Range.closed(5,11))
        self.assertEqual(len(rangeMap), 3)
        self.assertEqual(rangeMap.ranges[0], Range.closed(1,3))
        self.assertEqual(rangeMap.ranges[1], Range.open(3,5))
        self.assertEqual(rangeMap.ranges[2], Range.open(11,20))
        self.assertEqual(rangeMap.items[0],'foo')
        self.assertEqual(rangeMap.items[1], 'bar')
        self.assertEqual(rangeMap.items[2],'foo')
        rangeMap.remove(Range.closed(0,1))
        self.assertEqual(len(rangeMap), 3)
        self.assertEqual(rangeMap.ranges[0], Range.openClosed(1,3))
        self.assertEqual(rangeMap.ranges[1], Range.open(3,5))
        self.assertEqual(rangeMap.ranges[2], Range.open(11,20))
        self.assertEqual(rangeMap.items[0],'foo')
        self.assertEqual(rangeMap.items[1], 'bar')
        self.assertEqual(rangeMap.items[2],'foo')
    def test_get(self):
        if debug: print("Testing get")
        rangeMap = RangeMap()
        rangeMap.put(Range.closed(1,10),'foo')
        rangeMap.put(Range.open(3,6), 'bar')
        rangeMap.put(Range.open(10,20), 'foo')
        self.assertEqual(rangeMap.get(1),set(['foo']))
        self.assertEquals(rangeMap.get(4),set(['bar']))
        with self.assertRaises(KeyError):
            rangeMap.get(20)
        self.assertEqual(rangeMap.get(Range.closed(11,15)),set(['foo']))
        self.assertEquals(rangeMap.get(Range.closed(5,15)),set(['foo','bar']))
        with self.assertRaises(KeyError):
            rangeMap.get(Range.closed(20,30))
        self.assertEquals(rangeMap.get(Range.closed(15,100)),set(['foo']))
    def test_whichOverlaps(self):
        if debug: print("Testing whichOverlaps")
        theMap = RangeMap()
        theMap.put(Range.closed(3,5),'foo')
        theMap.put(Range.closed(7,10),'bar')
        self.assertEqual(theMap.whichOverlaps(4), set([Range.closed(3,5)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(0,4)),
                         set([Range.closed(3,5)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(4,5)),
                         set([Range.closed(3,5)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(4,6)),
                         set([Range.closed(3,5)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(6,7)),
                         set([Range.closed(7,10)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(8,11)),
                         set([Range.closed(7,10)]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(12,15)),
                         set([]))
        self.assertEqual(theMap.whichOverlaps(Range.closed(4,11)),
                         set([Range.closed(3,5), Range.closed(7,10)]))        
if __name__ == "__main__":
    debug = True
    unittest.main(exit = False)
