.. _ranges:

.. currentmodule:: Ranger

Introducing the Range
----------------------

.. author, Eli Rodgers-Melnick

The core of Ranger's functionality is the :class:`Ranger.src.Range.Range.Range` class. This class
represent a contiguous segment of a comparable object such as an int, float, 
character, or date. Ranges can be open or closed on either side, meaning they
can include or exclude their boundary values. Ranges can also be unbounded on
either side, allowing them to stretch across the entire domain of an object.

Creating a Range
^^^^^^^^^^^^^^^^

Ranges are creating using one of the static methods in the ``Range`` class.
These explicitly specify the nature of the Range's bounds (i.e. open v. closed,
bounded v. unbounded)

.. doctest::
   
   >>> from Ranger import Range
   >>> import datetime
   >>> Range.closed(1,5)
   [1, 5]
   >>> Range.openClosed(1,5)
   (1, 5]
   >>> Range.closedOpen(1,5)
   [1, 5)
   >>> Range.open(1,5)
   (1, 5)
   >>> Range.greaterThan(1)
   (1 , )
   >>> Range.atLeast(1)
   [1 , )
   >>> Range.lessThan(5)
   ( , 5)
   >>> Range.atMost(5)
   ( , 5]
   >>> Range.closed(0.5, 0.51)
   [0.5, 0.51]
   >>> Range.closed('a','d')
   [a, d]
   >>> Range.closed(datetime.date(1985,12,21), datetime.date(1986,11,3))
   [1985-12-21 , 1986-11-03]

Note that the endpoints of the Range need to be in the same class (or one
needs to be in a subclass of another). For instance, observe the following error.

.. doctest::

   >>> Range.closed(1, 3.0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/usr/local/lib/python2.7/site-packages/Ranger/src/Range/Range.py", line 364, in closed
       Range._validate_cutpoints(lower, upper)
     File "/usr/local/lib/python2.7/site-packages/Ranger/src/Range/Range.py", line 331, in _validate_cutpoints
       raise ValueError("Cutpoints are not compatible")
   ValueError: Cutpoints are not compatible

Using Range objects
^^^^^^^^^^^^^^^^^^^

``Range`` objects have a number of methods that can be used to test for membership
or perform set algebraic operations. This is shown using ``date`` as an example
below, but it would apply equally to any other domain.

.. doctest::

   >>> dateRange = Range.closed(datetime.date(1985,12,21), datetime.date(1986,11,3))
   >>> dateRange
   [1985-12-21 , 1986-11-03]
   >>> dateRange.contains(datetime.date(1986,1,1))
   True
   >>> dateRange.contains(datetime.date(1985,1,1))
   False
   >>> dateRange.containsAll((datetime.date(1986,1,1), datetime.date(1986,3,17)))
   True
   >>> dateRange.containsAll((datetime.date(1986,1,1), datetime.date(1987,3,17)))
   False
   >>> smallRange = Range.closed(datetime.date(1985,12,25),datetime.date(1986,1,1))
   >>> dateRange.encloses(smallRange)
   True
   >>> smallRange2 = Range.closed(datetime.date(1985,12,20),datetime.date(1986,1,1))
   >>> dateRange.encloses(smallRange2)
   False
   >>> dateRange.intersection(smallRange2)
   [1985-12-21 , 1986-01-01]
   >>> dateRange.span(smallRange2)
   [1985-12-20 , 1986-11-03]
