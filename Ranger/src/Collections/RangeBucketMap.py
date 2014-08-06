from bisect import bisect_left
from collections import deque, Hashable
from Ranger.src.Collections.RangeMap import RangeMap
from Ranger.src.Range.Range import Range
from Ranger.src.Range.Cut import Cut

class RangeBucketMap(RangeMap):
    """ Class used to represent a mapping of disjoint ranges to sets of items. Ranges
    do not coalesce. However, if a new Range is added over an existing Range, items
    belonging to the existing Range are retained in that Range
    """
    def __init__(self, rangeDict = None):
        """ Instantiates a RangeBucketMap

        Parameters
        ----------
        rangeDict : Dictionary of Range -> object
            Dictionary to start off the RangeBucketMap with
        """
        self.recurseAdd = False
        super(RangeBucketMap, self).__init__(rangeDict)
    def iteritems(self, start = None, end = None):
        """ Iterates over pairs of (Range, value)

        Parameters
        ----------
        start : comparable, optional
            The starting point for iterating, inclusive
        end : comparable, optional
            The ending point for iterating, inclusive

        Returns
        -------
        Generator of (Range intersecting [start,end], value), ordered by start point
        """
        if start is None:
            start = self.lower_cuts[0]
        else:
            start = Cut.belowValue(start)
        if end is None:
            end = self.upper_cuts[-1]
        else:
            end = Cut.aboveValue(end)
        bounding_range = Range(start, end)
        # Get the bounding indices
        ovlapLowerInd = max(bisect_left(self.lower_cuts, start)-1,0)
        ovlapUpperInd = bisect_left(self.lower_cuts, end)
        # Create queue of values that need to be generated
        yield_vals = deque()
        # Create dictionary of values to be generated -> indices containing them
        vals_inds_dict = {}
        for i in range(ovlapLowerInd, ovlapUpperInd):
            # Check if anything can be released from the queue
            while len(yield_vals) > 0:
                if vals_inds_dict[yield_vals[0]][-1] < i-1:
                    # Yield the full range, value. Remove value from queue
                    val = yield_vals.popleft()
                    yield Range(max(self.lower_cuts[vals_inds_dict[val][0]],start),
                                min(self.upper_cuts[vals_inds_dict[val][-1]],end)), val
                    # Remove value from dict
                    del vals_inds_dict[val]
                else:
                    break
            try:
                # Get intersection of the ranges
                intersect = bounding_range.intersection(self.ranges[i])
                if not intersect.isEmpty():
                    # If overlapping with this range, put into queue
                    for val in self.items[i]:
                        if val not in vals_inds_dict:
                            yield_vals.append(val)
                            vals_inds_dict[val] = deque()
                        vals_inds_dict[val].append(i)
            except ValueError:
                # Continue if no overlap with this range
                continue
        ## Yield remaining values
        while len(yield_vals) > 0:
            # Yield the full range, value. Remove value from queue
            val = yield_vals.popleft()
            yield Range(max(self.lower_cuts[vals_inds_dict[val][0]],start),
                        min(self.upper_cuts[vals_inds_dict[val][-1]],end)), val
            # Remove value from dict
            del vals_inds_dict[val]
                
    def get(self, key):
        """ Get the item(s) corresponding to a given key. The key can be a
        Range or a single value that is within a Range

        Parameters
        ----------
        key : comparable
            A single value or Range object

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
                        returnSet = returnSet.union(self.items[i])
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
            return self.items[lower_ind]  
    def put(self, key, val):
        """ Creates a mapping from a Range to a value, adding to
        any existing values over that Range

        Parameters
        ----------
        key : Range object
            A Range to serve as a key
        val : value, hashable
            Some value that the Range should map to

        Raises
        ------
        TypeError
            If the key is not a Range object or value is not hashable
        """
        if not isinstance(key, Range):
            raise TypeError("key is not a Range")
        elif not any((isinstance(val, Hashable), self.recurseAdd)):
            raise TypeError("value not hashable")
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
            if not isinstance(val, set):
                self.items.insert(insertInd, set([val]))
            else:
                self.items.insert(insertInd, val)
            return
        else:
            # If this range has some overlap with existing ranges
            ovlapLowerInd = max(bisect_left(self.lower_cuts, key.lowerCut)-1,0)
            ovlapUpperInd = bisect_left(self.lower_cuts, key.upperCut)
            # Create queue ranges to add
            addRanges = deque()
            # Create queue of items to add
            addItems = deque()
            # Keep track of next lower cutpoint to add
            nextLowerCut = key.lowerCut
            for i in range(ovlapLowerInd, ovlapUpperInd):
                try:
                    # Get intersection of the ranges
                    intersect = key.intersection(self.ranges[i])
                    if not intersect.isEmpty():
                        # Add in a Range between the next LowerCut and
                        # the beginning of this intersection if necessary
                        if nextLowerCut < intersect.lowerCut:
                            addRanges.append(Range(nextLowerCut, intersect.lowerCut))
                            addItems.append(val)
                            nextLowerCut = intersect.lowerCut
                        if intersect == self.ranges[i]:
                            ## If key encompassing existing Range ##
                            # Add item to this range
                            self.items[i].add(val)
                            # Change the next lower cut
                            nextLowerCut = intersect.upperCut
                        elif self.lower_cuts[i] == intersect.lowerCut:
                            ## If key upper cutpoint enclosed by existing Range ##
                            # Add in the rest of the original Range
                            if self.upper_cuts[i] > intersect.upperCut:
                                addRanges.append(Range(intersect.upperCut,
                                                       self.upper_cuts[i]))
                                addItems.append(set(self.items[i]))
                            # Define original part to be shorter                            
                            self.upper_cuts[i] = intersect.upperCut
                            self.ranges[i] = Range(self.lower_cuts[i],
                                                   intersect.upperCut)
                            self.items[i].add(val)
                            # Change the next lower cut
                            nextLowerCut = intersect.upperCut
                        elif self.upper_cuts[i] == intersect.upperCut:
                            ## If key lower cutpoint enclosed by existing Range ##
                            # Add in the rest of the original Range
                            if intersect.lowerCut > self.lower_cuts[i]:
                                addRanges.append(Range(self.lower_cuts[i], intersect.lowerCut))
                                addItems.append(set(self.items[i]))
                            # Define original part to be shorter
                            self.lower_cuts[i] = intersect.lowerCut
                            self.ranges[i] = Range(self.lower_cuts[i],
                                                   intersect.upperCut)
                            self.items[i].add(val)
                            # Change the next lower cut
                            nextLowerCut = intersect.upperCut
                        else:
                            # If entire key enclosed by existing Range
                            # Add in lower part of original Range
                            addRanges.append(Range(self.lower_cuts[i], intersect.lowerCut))
                            addItems.append(self.items[i])
                            # Add in upper part of original Range
                            addRanges.append(Range(intersect.upperCut, self.upper_cuts[i]))
                            addItems.append(self.items[i])
                            # Define original part to be middle
                            self.lower_cuts[i] = intersect.lowerCut
                            self.upper_cuts[i] = intersect.upperCut
                            self.ranges[i] = Range(intersect.lowerCut,intersect.upperCut)
                            self.items[i].add(val)
                            # Change the next lower cut
                            nextLowerCut = intersect.upperCut
                except ValueError:
                    # Continue if no overlap with this range
                    continue
            # Put in a last range if necessary
            if nextLowerCut < key.upperCut:
                addRanges.append(Range(nextLowerCut, key.upperCut))
                addItems.append(val)
            # Use recursive call to place the pairs, which now
            # should not overlap with any other ranges
            self.recurseAdd = True
            while len(addRanges) > 0:
                self.put(addRanges.pop(),addItems.pop())
            self.recurseAdd = False
    def remove(self, aRange):
        """ Removes a range and its value(s) from the range set

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
            self.recurseAdd = True
            while len(addRanges) > 0:
                self.put(addRanges.pop(), addItems.pop())        
            self.recurseAdd = False
