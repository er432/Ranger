from bisect import bisect_left
from collections import deque
from Ranger.src.Range.Range import Range

class RangeSet(object):
    """ Class used to represent a set of non-overlapping ranges of the
    same type. If a range is added that is connected to another range
    already in the set, those ranges are merged. Otherwise, it is added as
    a new range in the set
    """
    def __init__(self, ranges = None):
        """ Instantiates the RangeSet

        Parameters
        ----------
        ranges : List of Range objects
            Ranges to add to the Set
        """
        ## Holds lower and upper cut points of ranges
        self.lower_cuts = []
        self.upper_cuts = []
        ## Holds the range objects in the set
        self.ranges = []
        if ranges is not None:
            for aRange in ranges:
                self.add(aRange)
    def __repr__(self):
        return "RangeSet(%s)" % ", ".join(map(str, self.ranges))
    def __len__(self):
        return len(self.ranges)
    def __eq__(self, other):
        if not isinstance(other, RangeSet):
            return False
        elif len(self) != len(other):
            return False
        else:
            for r1,r2 in zip(self.ranges, other.ranges):
                if r1 != r2: return False
            return True
    def __ne__(self, other):
        return not self.__eq__(other)
    def add(self, aRange):
        """ Adds a range to the range set. If this range is not connected
        to any current ranges, it will place the new range on its own. If
        there is a connection, any connected ranges will be merged into a single
        range

        Parameters
        ----------
        aRange : A Range object
            The Range to add to the RangeSet

        Raises
        ------
        ValueError
            If adding range of type not compatible with previously
            added ranges
        """
        # Check for compatibility of types if necessary
        if len(self) > 0:
            if not (issubclass(aRange.lowerCut.theType,
                               self.ranges[0].lowerCut.theType) or \
                    issubclass(self.ranges[0].lowerCut.theType,
                               aRange.lowerCut.theType)):
                raise ValueError("Range not compatible with previously added ranges")
        # Get the insertion point (where the lower bound should go), should
        # this range be added on its own
        lower_ind = bisect_left(self.lower_cuts, aRange.lowerCut)
        if len(self) == 0:
            # Add on its own if there is nothing in the list
            self.ranges.append(aRange)
            self.lower_cuts.append(aRange.lowerCut)
            self.upper_cuts.append(aRange.upperCut)
        elif len(self) == lower_ind:
            if not aRange.isConnected(self.ranges[max(lower_ind-1,0)]):
                # Add on its own if not connected to previous and last
                self.ranges.insert(lower_ind,aRange)
                self.lower_cuts.insert(lower_ind,aRange.lowerCut)
                self.upper_cuts.insert(lower_ind,aRange.upperCut)
            else:
                # If connected with the range below, replace with new range
                newLowerCut = min(aRange.lowerCut,
                                  self.lower_cuts[max(lower_ind-1,0)])
                newUpperCut = max(aRange.upperCut,
                                  self.upper_cuts[max(lower_ind-1,0)])
                newRange = Range(newLowerCut, newUpperCut)
                self.ranges[-1] = newRange
                self.lower_cuts[-1] = newLowerCut
                self.upper_cuts[-1] = newUpperCut
        elif not any((aRange.isConnected(self.ranges[max(lower_ind-1,0)]),
                      aRange.isConnected(self.ranges[lower_ind]))):
            # Add on its own if not connected
            self.ranges.insert(lower_ind,aRange)
            self.lower_cuts.insert(lower_ind,aRange.lowerCut)
            self.upper_cuts.insert(lower_ind,aRange.upperCut)
        elif aRange.isConnected(self.ranges[max(lower_ind-1,0)]):
            # If connected with range below
            newLowerCut = min(self.lower_cuts[max(lower_ind-1,0)],
                              aRange.lowerCut)
            newUpperCut = max(aRange.upperCut,
                              self.upper_cuts[max(lower_ind-1,0)])
            removeCount = 1
            if len(self) == (lower_ind):
                # If hitting the last range, take the maximum uppercut
                newUpperCut = max(newUpperCut, self.upper_cuts[max(lower_ind-1,0)])
            else:
                # If not hitting the last range, go find the upper cut
                for i in range(max(1,lower_ind), len(self)):
                    if aRange.isConnected(self.ranges[i]):
                        newUpperCut = max(newUpperCut,self.upper_cuts[i])
                        removeCount += 1
                    else:
                        break
            # Make the new range
            newRange = Range(newLowerCut, newUpperCut)
            # Get rid of all overlapping ranges
            for i in range(removeCount):
                self.ranges.pop(max(lower_ind-1,0))
                self.lower_cuts.pop(max(lower_ind-1,0))
                self.upper_cuts.pop(max(lower_ind-1,0))
            # Add the new range
            self.ranges.insert(max(lower_ind-1,0),newRange)
            self.lower_cuts.insert(max(lower_ind-1,0),newRange.lowerCut)
            self.upper_cuts.insert(max(lower_ind-1,0),newRange.upperCut)
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
            lower_ind = max(bisect_left(self.lower_cuts, val.lowerCut)-1,0)
            return self.ranges[lower_ind].encloses(val)
        else:
            lower_ind = max(bisect_left(self.lower_cuts, val)-1,0)
            return self.ranges[lower_ind].contains(val)
    def difference(self, otherSet):
        """ Creates a new RangeSet in which all elements in another RangeSet
        are taken out of this RangeSet

        Parameters
        ----------
        otherSet : RangeSet object
            The RangeSet used for this difference

        Raises
        ------
        TypeError
            If the object passed in is not a RangeSet
        ValueError
            If the value type of the ranges in the other set not compatible
            with the range's values

        Returns
        -------
        RangeSet consisting of the difference of the two sets
        """
        if not isinstance(otherSet, RangeSet):
            raise TypeError("otherSet is not a RangeSet")
        newSet = RangeSet()
        for addRange in self.ranges:
            if otherSet.overlaps(addRange):
                # Determine where overlap occurs
                otherLowerInd = max(bisect_left(otherSet.lower_cuts,
                                            addRange.lowerCut)-1,0)
                otherUpperInd = bisect_left(otherSet.lower_cuts,
                                            addRange.upperCut)
                newLowerCut = addRange.lowerCut
                newUpperCut = addRange.upperCut
                add = True
                for i in range(otherLowerInd, otherUpperInd):
                    # Get the intersection of the ranges
                    intersect = addRange.intersection(otherSet.ranges[i])
                    if not intersect.isEmpty():
                        if addRange == intersect:
                            add = False
                            break
                        elif addRange.lowerCut == intersect.lowerCut:
                            # If equal on the left cutpoint, subtract out left
                            # part
                            newLowerCut = intersect.upperCut
                        elif addRange.upperCut == intersect.upperCut:
                            # If equal on right cutpoint, subtract out right
                            # part
                            newUpperCut = intersect.lowerCut
                        else:
                            # If in the middle, split into two parts and
                            # add the lower one immediately
                            newSet.add(Range(addRange.lowerCut,
                                             intersect.lowerCut))
                            newLowerCut = intersect.upperCut
                            newUpperCut = addRange.upperCut
                if add:
                    newSet.add(Range(newLowerCut, newUpperCut))
            else:
                newSet.add(addRange)
        return newSet
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
        # Get the index+1 of the highest lower cut <= to the value or its
        # lower cutpoint and check if the value overlaps
        if isinstance(val, Range):
            lower_ind = bisect_left(self.lower_cuts, val.lowerCut)-1
            upper_ind = bisect_left(self.lower_cuts, val.upperCut)
            for i in range(lower_ind,upper_ind):
                if val.isConnected(self.ranges[i]):
                    return True
            return False
        else:
            lower_ind = bisect_left(self.lower_cuts,val)-1
            return self.ranges[lower_ind].contains(val)
    def union(self, otherSet):
        """ Creates a new RangeSet that is the union of this set and
        another RangeSet object

        Parameters
        ----------
        otherSet : RangeSet object
            The RangeSet used for the union

        Raises
        ------
        TypeError
            If the object passed in is not a RangeSet
        ValueError
            If the value type of the set not compatible with the ranges

        Returns
        -------
        RangeSet consisting of union of two sets
        """
        if not isinstance(otherSet, RangeSet):
            raise TypeError("otherSet is not a RangeSet")
        return RangeSet(set(self.ranges+otherSet.ranges))
