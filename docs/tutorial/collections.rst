.. _collections:

.. currentmodule:: Ranger

Range Collections
-----------------

.. author, Eli Rodgers-Melnick

While the ``Range`` class may be the engine of Ranger, it really gets its traction
from the various classes in the :mod:`Ranger.src.Collections` module.
These include ``RangeSet``, ``RangeMap``, and ``RangeBucketMap``. These allow the
user to work with multiple ranges along with mappings of Ranges to objects.

Using the RangeSet
^^^^^^^^^^^^^^^^^^

The :class:`Ranger.src.Collections.RangeSet.RangeSet` class is a collection of
unique, disjoint Ranges of the same type. When a new ``Range`` is added to an
existing ``RangeSet``, it is checked for a connection to any existing Ranges 
already in the ``RangeSet``. If it is not connected, the new ``Range`` is added
on its own. If it is connected, the new ``Range`` coalesces with all connected
``Ranges``. This is shown below with integers

.. doctest::

   >>> from Ranger import RangeSet
   >>> from Ranger import Range
   >>> intRangeSet = RangeSet()
   >>> intRangeSet.add(Range.closed(1,5))
   >>> intRangeSet
   RangeSet([1 , 5])
   >>> intRangeSet.add(Range.closedOpen(8,10))
   >>> intRangeSet
   RangeSet([1 , 5], [8 , 10))
   >>> intRangeSet.add(Range.openClosed(5,7))
   >>> intRangeSet
   RangeSet([1 , 7], [8 , 10))
   >>> intRangeSet.add(Range.closed(5,9))
   >>> intRangeSet
   RangeSet([1 , 10))
   >>> intRangeSet.add(Range.atLeast(6))
   >>> intRangeSet
   RangeSet([1 , ))

The ``RangeSet`` then has multiple methods for performing set operations or 
determining whether any overlap exists with query Ranges. Continuing where
we left off...

.. doctest::

   >>> intRangeSet.contains(Range.closed(-1,4))
   False
   >>> intRangeSet.overlaps(Range.closed(-1,4))
   True
   >>> otherRangeSet = RangeSet()
   >>> otherRangeSet.add(Range.closed(5,10))
   >>> otherRangeSet.add(Range.closed(12,15))
   >>> otherRangeSet
   RangeSet([5 , 10], [12 , 15])
   >>> intRangeSet.difference(otherRangeSet)
   RangeSet([1 , 5), (10 , 12), (15 , ))])
   >>> otherRangeSet2 = RangeSet()
   >>> otherRangeSet2.add(Range.closed(-1,6))
   >>> otherRangeSet2
   RangeSet([-1 , 6])
   >>> otherRangeSet2.intersection(otherRangeSet)
   RangeSet([5 , 6])
   >>> otherRangeSet2.union(otherRangeSet)
   RangeSet([-1 , 10], [12 , 15])

Using the RangeMap
^^^^^^^^^^^^^^^^^^

The :class:`Ranger.src.Collections.RangeMap` class acts like a traditional 
hashmap, using disjoint ``Range`` objects as keys that can map to single
objects. One important thing to note when using a ``RangeMap`` is that a given
section's value will be replaced if a new key/value pair is added over that
position. 

.. doctest::

   >>> from Ranger import RangeMap
   >>> from Ranger import Range
   >>> theMap = RangeMap()
   >>> theMap[Range.closed(2,5)] = 'a'
   >>> theMap
   {[2 , 5] : a}
   >>> theMap[Range.closed(8,10)] = 'b'
   >>> theMap
   {[2 , 5] : a, [8 , 10] : b}
   >>> theMap[Range.closed(0,3)] = 'c'
   >>> theMap
   {[0 , 3] : c, (3 , 5] : a, [8 , 10] : b})}
   >>> theMap[Range.closed(4,4)] = 'b'
   >>> theMap
   {[0 , 3] : c, (3 , 4) : a, [4 , 4] : b, (4 , 5] : a, [8 , 10] : b})}
   >>> theMap[3]
   set(['c'])
   >>> theMap[4]
   set(['b'])
   >>> theMap[Range.closed(4,20)]
   set(['a', 'b'])
   >>> theMap[Range.closed(4,20)]
   set(['a', 'b'])
   >>> del theMap[Range.closed(4,20)]
   >>> theMap
   {[0 , 3] : c, (3 , 4) : a}

Using the RangeBucketMap
^^^^^^^^^^^^^^^^^^^^^^^^

The ``RangeMap`` is all well and good if you want sections in your Range domain
to map only to a *single* item. For instance, it could be used to form the basis
of a calendar that only supports a single event for any instance in time. However,
oftentimes more than one mapping is desired for any particular ``Range``. For instance,
a particular chromosomal region could map to mutiple mRNAs, or a calendar could
keep track of what multiple users are doing at any given time. The ``RangeBucketMap``
accomplishes this feat.

The :class:`Ranger.src.Collections.RangeBucketMap` class maps disjoint Ranges to
one or more *hashable* objects. When a new key/value pair is added to a particular
Range, that value is kept along with any pre-existing values in the Range.

.. doctest::

   >>> from Ranger import Range
   >>> from Ranger import RangeBucketMap
   >>> buckets = RangeBucketMap()
   >>> buckets[Range.closed(3,5)] = 'a'
   >>> buckets
   {[3 , 5] : set(['a'])}
   >>> buckets[Range.closed(8,10)] = 'b'
   >>> buckets
   {[3 , 5] : set(['a']), [8 , 10] : set(['b'])}
   >>> buckets[Range.closed(1,6)] = 'c'
   >>> buckets
   {[1 , 3) : set(['c']), [3 , 5] : set(['a', 'c']), 
   (5 , 6] : set(['c']), [8 , 10] : set(['b'])}
   >>> buckets[Range.closed(4,100)]
   set(['a', 'c', 'b'])
   >>> del buckets[Range.closed(4,8)]
   >>> buckets
   {[1 , 3) : set(['c']), [3 , 4) : set(['a', 'c']), (8 , 10] : set(['b'])}]}
