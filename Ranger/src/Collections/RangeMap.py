from bisect import bisect_left
from Ranger.src.Range.Range import Range
from collections import deque

class RangeMap(object):
    """ Class used to represent a mapping of disjoint ranges to some objects.
    Ranges do not coalesce. If a new Range is added over an existing Range,
    it overwrites the overlapping part of the existing Range
    """
    def __init__(self, rangeDict = None):
        """ Instantiates a RangeMap
        
        Parameters
        ----------
        rangeDict : Dictionary of Range -> object
            Dictionary to start off the RangeMap with. Note that this will
            not be traversed in any particular order, so it may result in
            unexpected behavior if instantiated with any overlapping ranges
        """
        # Holds lower and upper cut points of ranges
        self.lower_cuts = []
        self.upper_cuts = []
        # Holds the actual range objects that are the keys
        self.ranges = []
        # Holds items mapping to each range
        self.items = []
        if rangeDict is not None:
            for rangeKey, val in rangeDict.iteritems():
                self.put(rangeKey, val)
    def __getitem__(self, key):
        return self.get(key)
    def __setitem__(self, key, value):
        self.put(key, value)
    def __delitem__(self, key):
        self.remove(key)
    def __iter__(self):
        return iter(self.ranges)
    def __eq__(self, other):
        if not isinstance(other, RangeMap): return False
        elif len(self) != len(other): return False
        for k1,v1,k2,v2 in zip(self.ranges, self.items,
                               other.ranges, other.items):
            if (k1 != k2 or v1 != v2):
                return False
        return True
    def __ne__(self, other):
        return not self.__eq__(other)
    def __len__(self):
        return len(self.ranges)
    def __repr__(self):
        returnStr = "{%s}" % ", ".join([
            "%s : %s" % (k,v) for k,v in zip(self.ranges, self.items)
            ])
        return returnStr
    def __missing__(self, key):
        raise KeyError(str(key))
    def contains(self, val):
        """ Returns true if any of the ranges fully enclose the given
        value, which can be a single value or a Range object

        Parameters
        ----------
        val : A single value or a Range object

        Raises
        ------
        ValueError
            If the value type not compatible with the ranges
        
        Returns
        -------
        true if any of the ranges fully enclose the given value
        """
        if len(self) == 0: return False
        # Get the index+1 of the highest lower cut <= to the value or its
        # lower cutpoint and check if the value contained
        if isinstance(val, Range):
            lower_ind = max(bisect_left(self.lower_cuts, val.lowerCut)-1,0)
            return self.ranges[lower_ind].encloses(val)
        else:
            lower_ind = max(bisect_left(self.lower_cuts, val)-1,0)
            return self.ranges[lower_ind].contains(val)
    def get(self, key):
        """ Get the item(s) corresponding to a given key. The key can be a
        Range or a single value that is within a Range

        Parameters
        ----------
        key : A single value or Range object

        Raises
        ------
        KeyError
            If there is no overlap with the key
        ValueError
            If the key type not compatible with the ranges
        
        Returns
        -------
        A set containing all overlapping items
        """
        if not self.overlaps(key):
            self.__missing__(key)
        elif isinstance(key, Range):
            # If this is a single value
            returnSet = set()
            # Get the bounding indices
            ovlapLowerInd = max(bisect_left(self.lower_cuts, key.lowerCut)-1,0)
            ovlapUpperInd = bisect_left(self.lower_cuts, key.upperCut)
            for i in range(ovlapLowerInd, ovlapUpperInd):
                try:
                    # Get intersection of the ranges
                    intersect = key.intersection(self.ranges[i])
                    if not intersect.isEmpty():
                        # If overlapping with this range, put its
                        # item in the return set
                        returnSet.add(self.items[i])
                except ValueError:
                    # Continue if no overlap with this range
                    continue
            # Return the set of items
            return returnSet
        else:
            # If this is a single value
            # Get the index of the range containing the value
            lower_ind = max(bisect_left(self.lower_cuts, key)-1,0)
            # Return the item at that value
            return set([self.items[lower_ind]])
            
    def overlaps(self, val):
        """ Returns true if any of the ranges at least partially overlap
        the given value, which can be a single value or a Range object

        Parameters
        ----------
        val : A single value or a Range object

        Raises:
        -------
        ValueError
            If the value type not compatible with the ranges

        Returns
        -------
        true if any of the ranges fully enclose the given value
        """
        if len(self) == 0: return False
        # Get the index+1 of the highest lower cut <= to the value or its
        # lower cutpoint and check if the value overlaps
        if isinstance(val, Range):
            lower_ind = bisect_left(self.lower_cuts, val.lowerCut)-1
            upper_ind = bisect_left(self.lower_cuts, val.upperCut)
            for i in range(lower_ind,upper_ind):
                if val.isConnected(self.ranges[i]):
                    if not self.ranges[i].intersection(val).isEmpty():
                        return True
            return False
        else:
            lower_ind = bisect_left(self.lower_cuts,val)-1
            return self.ranges[lower_ind].contains(val)        
    def put(self, key, val):
        """ Creates a mapping from a Range to a value. Note that if the
        key Range overlaps any existing ranges, it will replace those
        Range(s) over the intersection

        Parameters
        ----------
        key : Range object
            A Range to serve as a key
        val : value
            Some value that the Range should map to

        Raises
        ------
        TypeError
            If the key is not a Range object
        """
        if not isinstance(key, Range):
            raise TypeError("key is not a Range")
        elif key.isEmpty():
            # Skip if this is an empty range
            return
        # Figure out where to the key/value
        if not self.overlaps(key):
            # If this range is completely on its own, just insert
            insertInd = bisect_left(self.lower_cuts, key.lowerCut)
            self.ranges.insert(insertInd, key)
            self.lower_cuts.insert(insertInd, key.lowerCut)
            self.upper_cuts.insert(insertInd, key.upperCut)
            self.items.insert(insertInd, val)
            return
        else:
            # If this range has some overlap with existing ranges
            ovlapLowerInd = max(bisect_left(self.lower_cuts, key.lowerCut)-1,0)
            ovlapUpperInd = bisect_left(self.lower_cuts, key.upperCut)
            # Create queue or indices marked for removal
            removeRanges = deque()
            # Create queue ranges to add
            addRanges = deque()
            # Create queue of items to add
            addItems = deque()
            for i in range(ovlapLowerInd, ovlapUpperInd):
                try:
                    # Get intersection of the ranges
                    intersect = key.intersection(self.ranges[i])
                    if not intersect.isEmpty():
                        if intersect == self.ranges[i]:
                            # Mark range for removal
                            removeRanges.append(i)
                        elif self.lower_cuts[i] == intersect.lowerCut:
                            # If equal on left cutpoint, subtract out left
                            # part
                            self.lower_cuts[i] = intersect.upperCut
                            self.ranges[i] = Range(intersect.upperCut,
                                                   self.upper_cuts[i])
                        elif self.upper_cuts[i] == intersect.upperCut:
                            # If equal on right cutpoint, subtract out
                            # right part
                            self.upper_cuts[i] = intersect.lowerCut
                            self.ranges[i] = Range(self.lower_cuts[i],
                                                   intersect.lowerCut)
                        else:
                            # If in the middle, split into two parts, putting
                            # both in add queue and placing the old range index
                            # in the remove queue
                            addRanges.append(Range(self.lower_cuts[i],
                                                   intersect.lowerCut))
                            addRanges.append(Range(intersect.upperCut,
                                                   self.upper_cuts[i]))
                            addItems.append(self.items[i])
                            addItems.append(self.items[i])
                            removeRanges.append(i)
                except ValueError:
                    # Continue if no overlap with this range
                    continue
            # Remove any ranges that are marked for removal
            while len(removeRanges) > 0:
                removeInd = removeRanges.pop()
                self.ranges.pop(removeInd)
                self.lower_cuts.pop(removeInd)
                self.upper_cuts.pop(removeInd)
                self.items.pop(removeInd)
            addItems.append(val)
            addRanges.append(key)
            # Use recursive call to place the pairs, which now
            # should not overlap with any other ranges
            while len(addRanges) > 0:
                self.put(addRanges.pop(),addItems.pop())
    def remove(self, aRange):
        """ Removes a range and its value from the range set

        Parameters
        ----------
        aRange : A Range object
            The Range to remove

        Raises
        ------
        ValueError
            If removing range of type not compatible with previously
            added ranges
        TypeError
            If not a Range
        """
        if not isinstance(aRange, Range):
            raise TypeError("aRange is not a Range")
        elif aRange.isEmpty():
            # Skip if this is an empty range
            return
        # Check for compatibility of types if necessary
        if len(self) > 0:
            if not (issubclass(aRange.lowerCut.theType,
                               self.ranges[0].lowerCut.theType) or \
                    issubclass(self.ranges[0].lowerCut.theType,
                               aRange.lowerCut.theType)):
                raise ValueError("Range not compatible with previously added ranges")
        # Check if the range actually overlaps with the key set
        if not self.overlaps(aRange):
            return
        else:
            # There's some overlap, so deal with that
            # Determine where overlap occurs
            ovlapLowerInd = max(bisect_left(self.lower_cuts,
                                            aRange.lowerCut)-1,0)
            ovlapUpperInd = bisect_left(self.lower_cuts, aRange.upperCut)
            # Create queue of indices marked for removal
            removeRanges = deque()
            # Create queue of ranges to add
            addRanges = deque()
            # Create queue of items to add with the addRanges
            addItems = deque()
            for i in range(ovlapLowerInd, ovlapUpperInd):
                try:
                    # Get intersection of the ranges
                    intersect = aRange.intersection(self.ranges[i])
                    if not intersect.isEmpty():
                        if intersect == self.ranges[i]:
                            # Mark range for removal
                            removeRanges.append(i)
                        elif self.lower_cuts[i] == intersect.lowerCut:
                            # If equal on the left cutpoint, subtract
                            # out left part
                            self.lower_cuts[i] = intersect.upperCut
                            self.ranges[i] = Range(intersect.upperCut,
                                                   self.upper_cuts[i])
                        elif self.upper_cuts[i] == intersect.upperCut:
                            # If equal on right cutpoint, subtract out
                            # right part
                            self.upper_cuts[i] = intersect.lowerCut
                            self.ranges[i] = Range(self.lower_cuts[i],
                                                   intersect.lowerCut)
                        else:
                            # If in the middle, split into two parts, putting
                            # both in add queue and placing the old range index
                            # into the remove queue
                            addRanges.append(Range(self.lower_cuts[i],
                                                   intersect.lowerCut))
                            addItems.append(self.items[i])
                            addRanges.append(Range(intersect.upperCut,
                                                   self.upper_cuts[i]))
                            addItems.append(self.items[i])
                            removeRanges.append(i)
                except ValueError:
                    # Continue if no overlap with this range
                    continue
            # Remove any ranges that are marked for removal
            while len(removeRanges) > 0:
                removeInd = removeRanges.pop()
                self.ranges.pop(removeInd)
                self.lower_cuts.pop(removeInd)
                self.upper_cuts.pop(removeInd)
                self.items.pop(removeInd)
            # Add any pairs that need to be added
            while len(addRanges) > 0:
                self.put(addRanges.pop(), addItems.pop())
