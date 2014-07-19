from bisect import bisect_left
from collections import deque
from Ranger.src.Range.Range import Range


class RangeSet(object):
    """ Class used to represent a set of non-overlapping ranges of the
    same type. If a range is added that is connected to another range
    already in the set, those ranges are merged. Otherwise, it is added as
    a new range in the set
    """
    def __init__(self):
        """ Instantiates the RangeSet
        """
        ## Holds lower and upper cut points of ranges
        self.lower_cuts = []
        self.upper_cuts = []
        ## Holds the range objects in the set
        self.ranges = []
        ## Holds a queue of items to be added if desired to be done
        # in batch mode
        self.add_queue = deque()
    def __len__(self):
        return len(self.ranges)
    def add(self, aRange):
        """ Adds a range to the range set. If this range is not connected
        to any current ranges, it will place the new range on its own. If
        there is a connection, any connected ranges will be merged into a single
        range

        Parameters
        ----------
        aRange -- A Range object
            The Range to add to the RangeSet
        """
        # Get the insertion point (where the lower bound should go), should
        # this range be added on its own
        lower_ind = bisect_left(self.lower_cuts, aRange.lowerCut)
        if len(self) == 0:
            # Add on its own if there is nothing in the list
            self.ranges.append(aRange)
            self.lower_cuts.append(aRange.lowerCut)
            self.upper_cuts.append(aRange.upperCut)
        elif len(self) == lower_ind:
            if not aRange.isConnected(self.ranges[lower_ind-1]):
                # Add on its own if not connected to previous and last
                self.ranges.insert(lower_ind,aRange)
                self.lower_cuts.insert(lower_ind,aRange.lowerCut)
                self.upper_cuts.insert(lower_ind,aRange.upperCut)
            else:
                # If connected with the range below, replace with new range
                newLowerCut = min(aRange.lowerCut, self.lower_cuts[lower_ind-1])
                newUpperCut = max(aRange.upperCut, self.upper_cuts[lower_ind-1])
                newRange = Range(newLowerCut, newUpperCut)
                self.ranges[-1] = newRange
                self.lower_cuts[-1] = newLowerCut
                self.upper_cuts[-1] = newUpperCut
        elif not any((aRange.isConnected(self.ranges[lower_ind-1]),
                      aRange.isConnected(self.ranges[lower_ind]))):
            # Add on its own if not connected
            self.ranges.insert(lower_ind,aRange)
            self.lower_cuts.insert(lower_ind,aRange.lowerCut)
            self.upper_cuts.insert(lower_ind,aRange.upperCut)
        elif aRange.isConnected(self.ranges[lower_ind-1]):
            # If connected with range below
            newLowerCut = min(self.lower_cuts[lower_ind-1],
                              aRange.lowerCut)
            newUpperCut = aRange.upperCut
            removeCount = 1
            if len(self) == (lower_ind):
                # If hitting the last range, take the maximum uppercut
                newUpperCut = max(newUpperCut, self.upper_cuts[lower_ind-1])
                removeCount += 1
            else:
                # If not hitting the last range, go find the upper cut
                for i in range(lower_ind, len(self)):
                    if aRange.isConnected(self.ranges[i]):
                        newUpperCut = max(newUpperCut,self.upper_cuts[i])
                        removeCount += 1
                    else:
                        break
            # Make the new range
            newRange = Range(newLowerCut, newUpperCut)
            # Get rid of all overlapping ranges
            for i in range(removeCount):
                self.ranges.pop(lower_ind-1)
                self.lower_cuts.pop(lower_ind-1)
                self.upper_cuts.pop(lower_ind-1)
            # Add the new range
            self.ranges.insert(lower_ind-1,newRange)
            self.lower_cuts.insert(lower_ind-1,newRange.lowerCut)
            self.upper_cuts.insert(lower_ind-1,newRange.upperCut)
        elif aRange.isConnected(self.ranges[lower_ind]):
            # If connected with the range above
            newLowerCut = min(aRange.lowerCut, self.lower_cuts[lower_ind])
            newUpperCut = max(aRange.upperCut, self.upper_cuts[lower_ind])
            removeCount = 0
            if len(self) == (lower_ind + 1):
                # If hitting the last range, you're done
                removeCount += 1
            else:
                # Go find the upper cut
                for i in range(lower_ind, len(self)):
                    if aRange.isConnected(self.ranges[i]):
                        newUpperCut = max(newUpperCut, self.upper_cuts[i])
                        removeCount += 1
                    else:
                        break
            # Make the new range
            newRange = Range(newLowerCut, newUpperCut)
            # Remove the overlapping ranges
            for i in range(removeCount):
                self.ranges.pop(lower_ind)
                self.lower_cuts.pop(lower_ind)
                self.upper_cuts.pop(lower_ind)
            # Add the new range
            self.ranges.insert(lower_ind, newRange)
            self.lower_cuts.insert(lower_ind, newRange.lowerCut)
            self.upper_cuts.insert(lower_ind, newRange.upperCut)

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
        # Get the index+1 of the highest lower cut <= to the value or its
        # lower cutpoint and check if the value contained
        if isinstance(val, Range):
            lower_ind = bisect_left(self.lower_cuts, val.lowerCut)-1
            return self.ranges[lower_ind].encloses(val)
        else:
            lower_ind = bisect_left(self.lower_cuts, val)-1
            return self.ranges[lower_ind].contains(val)
