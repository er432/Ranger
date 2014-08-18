from Ranger.src.Range.Cut import Cut

class Range(object):
    """
    Class used to represent a range along some 1-D domain. The range
    is represented by 2 cutpoints can can be unbounded by specifying an
    aboveAll or belowAll Cut.
    """
    def __init__(self, lowerCut, upperCut):
        """ Instantiates a Range

        Parameters
        ----------
        lowerCut : Cut object
            Specifies the lower cut for the range
        upperCut : Cut object
            Specifies the upper cut for the range

        Raises
        ------
        ValueError
            If bound(s) are not Cut objects or lower > upper
        """
        if not all(map(lambda x: isinstance(x, Cut), (lowerCut,upperCut))):
            raise ValueError("Bounds must be Cut objects")
        elif lowerCut > upperCut:
            raise ValueError("Lower bound cannot be greater than upper bound")
        self.lowerCut = lowerCut
        self.upperCut = upperCut
    def __repr__(self):
        try:
            return_str = '[' if self.isLowerBoundClosed() else '('
        except TypeError:
            return_str = '('
        return_str += (str(self.lowerCut.point) if not self.lowerCut.belowAll \
          else '')
        return_str += ' , '
        return_str += (str(self.upperCut.point) if not self.upperCut.aboveAll \
          else '')
        try:
            return_str += ']' if self.isUpperBoundClosed() else ')'
        except TypeError:
            return_str += ')'
        return return_str
    def __hash__(self):
        return (hash(self.lowerCut)*31 + hash(self.upperCut))
    def __eq__(self, other):
        if not isinstance(other, Range):
            return False
        else:
            return ((self.lowerCut == other.lowerCut) and \
                    (self.upperCut == other.upperCut))
    def __ne__(self, other):
        return not self.__eq__(other)
    def contains(self, val):
        """ Returns true if the range contains the value

        Parameters
        ----------
        val : Comparable object of the appropriate type for the range
            Value to query whether in the range

        Raises
        ------
        ValueError
            If the value type not compatible with cutpoint type

        Returns
        -------
        True if the range contains the value
        """
        return (self.lowerCut < val and \
                self.upperCut > val)
    def containsAll(self, vals):
        """ Returns True if the range contains all values in some
        iterable

        Parameters
        ----------
        vals : Iterable of comparable object of appropriate type for range
            Values to query against the range

        Raises
        ------
        ValueError
            If there is a value type not compatible with the cutpoint type

        Returns
        -------
        True if the range contains all values
        """
        for val in vals:
            if not self.contains(val):
                return False
        return True
    def getDistanceFromPoint(self, val, distFunc = lambda x1, x2: abs(x1-x2)):
        """ Returns the minimum distance of a Range from a Point, returning 0
        if there is an overlap.

        Note that both upper and lower bounds must be closed for this function
        to work

        Parameters
        ----------
        val : comparable, compatible with cutpoint type
            The value of the point where the distance is desired
        distFunc : callable
            Function that calculates the distance between two points in the
            domain of the Range

        Raises
        ------
        TypeError
            If the upper and/or lower bounds of this Range are not closed
            or if the distFunc not compatible with the type
        
        Returns
        -------
        The minimum distance between the Range and the Point. Returns 0
        if there is an overlap
        """
        if not all((self.isLowerBoundClosed(), self.isUpperBoundClosed())):
            raise TypeError("Range is not closed")
        if self.contains(val):
            return 0.
        else:
            return min(distFunc(self.lowerCut.point, val),
                       distFunc(self.upperCut.point, val))
    def getDistanceFromRange(self, other, distFunc = lambda x1,x2: abs(x1-x2)):
        """ Returns the minimum distance of a Range from another Range, returning
        0 if there is any overlap

        Note that both Ranges must be closed for this function to work

        Parameters
        ----------
        other : Range, compatible with this Range's domain
            The Range to compare to
        distFunc : callable
            Function that calculates the distance between two points in the
            domain of the Range

        Raises
        ------
        TypeError
            If the upper and/or lower bounds of this Range are not closed
            or if the distFunc not compatible with the type

        Returns
        -------
        Minimum distance between the ranges        
        """
        if not isinstance(other, Range):
            raise TypeError("other is not a Range")
        if not all((self.isLowerBoundClosed(), self.isUpperBoundClosed(),
                    other.isLowerBoundClosed(), other.isUpperBoundClosed())):
            raise TypeError("Not all Ranges closed")
        if self.isConnected(other):
            return 0.
        else:
            return min(distFunc(self.lowerCut.point, other.upperCut.point),
                       distFunc(other.lowerCut.point, self.upperCut.point))
    def hasLowerBound(self):
        """ Returns True if the range has a lower endpoint (not unbounded
        at the lower end)

        Returns
        -------
        True if the range has a lower endpoint
        """
        return (not self.lowerCut.belowAll)
    def hasUpperBound(self):
        """ Returns True if the range has an upper endpoint (not unbounded
        at the upper end)

        Returns
        -------
        True if the range has an upper endpoint
        """
        return (not self.upperCut.aboveAll)
    def lowerEndpoint(self):
        """ Returns the lower endpoint of the range if it exists. Otherwise
        raises a TypeError

        Raises
        ------
        TypeError
            If the range is unbounded below

        Returns
        -------
        The lower endpoint of the range
        """
        if self.lowerCut.point is None:
            raise TypeError("Range unbounded below")
        else:
            return self.lowerCut.point
    def upperEndpoint(self):
        """ Returns the upper endpoint of the range if it exists. Otherwise
        raises a TypeError

        Raises
        ------
        TypeError
            If the range is unbounded above

        Returns
        -------
        The upper endpoint of the range
        """
        if self.upperCut.point is None:
            raise TypeError("Range unbounded above")
        else:
            return self.upperCut.point
    def isLowerBoundClosed(self):
        """ Returns whether the lower bound is closed (if there is a
        lower bound)

        Raises
        ------
        TypeError
            If the range is unbounded below

        Returns
        -------
        True if the lower bound is closed
        """
        if self.lowerCut.point is None:
            raise TypeError("Range unbounded below")
        else:
            return self.lowerCut.below
    def isUpperBoundClosed(self):
        """ Returns whether the upper bound is closed (if there is an
        upper bound)

        Raises
        ------
        TypeError
            If the range is unbounded above

        Returns
        -------
        True if the upper bound is closed
        """
        if self.upperCut.point is None:
            raise TypeError("Range unbounded above")
        else:
            return (not self.upperCut.below)
    def isEmpty(self):
        """ Returns True if the range is of form [v, v) or (v, v]

        Returns
        -------

        True if the range is of the form [v,v) or (v,v]
        """
        return self.lowerCut == self.upperCut
    def encloses(self, other):
        """ Returns True if the bounds of the other range do not extend
        outside the bounds of this range

        Examples:
            [3,6] encloses [4,5]
            (3,6) encloses (3,6)
            [3,6] encloses [4,4]
            (3,6] does not enclose [3,6]
            [4,5] does not enclose (3,6)

        Parameters
        ----------
        other : A Range
            The range to compare to

        Raises
        ------
        ValueError
            If object passed in is not a Range

        Returns
        -------
        True if the bounds of the other range do not extend outside
        the bounds of this range
        """
        if not isinstance(other, Range):
            raise ValueError("Range required")
        return ((self.lowerCut <= other.lowerCut) and \
            (self.upperCut >= other.upperCut))
    def isConnected(self, other):
        """ Returns True if there is a (possibly empty) range that is
        enclosed by both this range and other

        Examples:
            [2,4] and [5,7] are not connected
            [2,4] and [3,5] are connected
            [2,4] and [4,6] are connected
            [3,5] and (5,10) are connected
        
        Parameters
        ----------
        other : A range
            The range to compare to

        Raises
        ------
        ValueError
            If object passed in is not a Range
        
        Returns
        -------
        True if there is a (possibly empty) range that is enclosed by
        both this range and other
        """
        if not isinstance(other, Range):
            raise ValueError("Range required")
        return ((self.lowerCut <= other.upperCut) and \
                (other.lowerCut <= self.upperCut))
    def intersection(self, other):
        """ Returns the maximal range enclosed by both this range and the
        other range, if such a range exists

        Examples:
            Intersection of [1,5] and [3,7] is [3,5]
            Intersection of [1,5] and [5,7] is [5,5]

        Parameters
        ----------
        other : A range
            The range to compare to

        Raises
        ------
        ValueError
            If object passed in is not a Range or if there is no intersection

        Returns
        -------
        The intersection range
        """
        if not isinstance(other, Range):
            raise ValueError("Range required")
        if ((self.lowerCut >= other.lowerCut) and \
            (self.upperCut <= other.upperCut)):
            return Range(self.lowerCut, self.upperCut)
        elif ((self.lowerCut <= other.lowerCut) and \
              (self.upperCut >= other.upperCut)):
            return Range(other.lowerCut, other.upperCut)
        else:
            newLower = self.lowerCut if (self.lowerCut >= other.lowerCut) else \
                                         other.lowerCut
            newUpper = self.upperCut if (self.upperCut <= other.upperCut) else \
                                         other.upperCut
            return Range(newLower, newUpper)
    def span(self, other):
        """ Returns the minimal range that encloses both this range and
        the other. Note that if the input ranges are not connected, the span can
        contain values that are not contained within either input range

        Examples:
            Span of [1,3] and [5,7] is [1,7]

        Parameters
        ----------
        other : A range
            A range to span with

        Raises
        ------
        ValueError
            If object passed in is not a Range or if there is no intersection
        
        Returns
        -------
        The minimal range enclosing both with and the other range
        """
        if ((self.lowerCut <= other.lowerCut) and \
            (self.upperCut >= other.upperCut)):
            return Range(self.lowerCut, self.upperCut)
        elif ((self.lowerCut >= other.lowerCut) and \
              (self.upperCut <= other.upperCut)):
            return Range(other.lowerCut, other.upperCut)
        else:
            newLower = self.lowerCut if (self.lowerCut <= other.lowerCut) else \
                other.lowerCut
            newUpper = self.upperCut if (self.upperCut >= other.upperCut) else \
                other.upperCut
            return Range(newLower, newUpper)
    ##################
    # Static methods #
    ##################
    @staticmethod
    def _validate_cutpoints(*pts):
        if not all(map(lambda x: (hasattr(x, "__lt__") and \
                hasattr(x, "__gt__")) or hasattr(x,'__cmp__'), pts)):
            raise ValueError("Cutpoint type(s) not comparable")
        if len(pts) == 2:
            if not (issubclass(type(pts[0]),type(pts[1])) or \
              issubclass(type(pts[1]),type(pts[0]))):
                raise ValueError("Cutpoints are not compatible")
        return True
    @staticmethod
    def _get_type(*pts):
        if len(pts) == 1: return type(pts[0])
        elif len(pts) == 2:
            if issubclass(type(pts[0]),type(pts[1])):
                return type(pts[1])
            elif issubclass(type(pts[1]),type(pts[0])):
                return type(pts[0])
            else:
                raise ValueError("Cutpoints are not compatible")
    @staticmethod
    def closed(lower, upper):
        """ Creates a range including the endpoints (i.e. [lower, upper])

        Parameters
        ----------
        lower : comparable, of same type as or subclass of upper type
            The lower bound
        upper : comparable, of same type as or subclass of lower type
            The upper bound

        Raises
        ------
        ValueError
            If type(s) are not comparable or compatible
        
        Returns
        -------
        A Range object [lower, upper]
        """
        # Ensure cutpoints are of compatible, appropriate types
        Range._validate_cutpoints(lower, upper)
        theType = Range._get_type(lower,upper)
        return Range(Cut.belowValue(lower, theType=theType),
                     Cut.aboveValue(upper, theType=theType))
    @staticmethod
    def closedOpen(lower, upper):
        """ Creates a range including the lower endpoint (i.e. [lower, upper))

        Parameters
        ----------
        lower : comparable, of same type as or subclass of upper type
            The lower bound
        upper : comparable, of same type as or subclass of lower type
            The upper bound

        Raises
        ------
        ValueError
            If type(s) are not comparable or compatible
        
        Returns
        -------
        A Range object [lower, upper)
        """
        # Ensure cutpoints are of compatible, appropriate types
        Range._validate_cutpoints(lower, upper)
        theType = Range._get_type(lower,upper)
        return Range(Cut.belowValue(lower, theType=theType),
                     Cut.belowValue(upper, theType=theType))
    @staticmethod
    def openClosed(lower, upper):
        """ Creates a range including the upper (i.e. (lower, upper])

        Parameters
        ----------
        lower : comparable, of same type as or subclass of upper type
            The lower bound
        upper : comparable, of same type as or subclass of lower type
            The upper bound

        Raises
        ------
        ValueError
            If type(s) are not comparable or compatible
        
        Returns
        -------
        A Range object (lower, upper]
        """
        # Ensure cutpoints are of compatible, appropriate types
        Range._validate_cutpoints(lower, upper)
        theType = Range._get_type(lower,upper)
        return Range(Cut.aboveValue(lower, theType=theType),
                     Cut.aboveValue(upper, theType=theType))
    @staticmethod
    def open(lower, upper):
        """ Creates a range excluding the endpoints (i.e. (lower, upper))

        Parameters
        ----------
        lower : comparable, of same type as or subclass of upper type
            The lower bound
        upper : comparable, of same type as or subclass of lower type
            The upper bound

        Raises
        ------
        ValueError
            If type(s) are not comparable or compatible or if constructing
            a range of type (v,v), which is invalid
        
        Returns
        -------
        A Range object (lower, upper)
        """
        # Ensure cutpoints are of compatible, appropriate types
        Range._validate_cutpoints(lower, upper)
        theType = Range._get_type(lower,upper)
        if lower == upper:
            raise TypeError("Range of type (v,v) is not valid")        
        return Range(Cut.aboveValue(lower, theType=theType),
                     Cut.belowValue(upper, theType=theType))
    @staticmethod
    def lessThan(val):
        """ Makes range including all values less than some value
        (i.e. (-inf, val))

        Parameters
        ----------
        val : comparable
            The upper bound

        Raises
        ------
        ValueError
            If type not comparable

        Returns
        -------
        A Range object (-inf, val)
        """
        Range._validate_cutpoints(val)
        theType = Range._get_type(val)
        return Range(Cut.belowAll(theType=theType),
                     Cut.belowValue(val, theType=theType))
    @staticmethod
    def atMost(val):
        """ Makes range including all values less than or equal to
        some value (i.e. (-inf, val])

        Parameters
        ----------
        val : comparable
            The upper bound

        Raises
        ------
        ValueError
            If type not comparable

        Returns
        -------
        A Range object (-inf, val]
        """
        Range._validate_cutpoints(val)
        theType = Range._get_type(val)
        return Range(Cut.belowAll(theType=theType),
                     Cut.aboveValue(val, theType=theType))
    @staticmethod
    def greaterThan(val):
        """ Makes range including all values greater than
        some value (i.e. (val, inf])

        Parameters
        ----------
        val : comparable
            The lower bound

        Raises
        ------
        ValueError
            If type not comparable

        Returns
        -------
        A Range object (val, inf)
        """
        Range._validate_cutpoints(val)
        theType = Range._get_type(val)
        return Range(Cut.aboveValue(val,theType=theType),
                     Cut.aboveAll(theType=theType))
    @staticmethod
    def atLeast(val):
        """ Makes range including all values greater than or equal to
        some value (i.e. [val, inf))

        Parameters
        ----------
        val : comparable
            The lower bound

        Raises
        ------
        ValueError
            If type not comparable

        Returns
        -------
        A Range object [val, inf)
        """
        Range._validate_cutpoints(val)
        theType = Range._get_type(val)
        return Range(Cut.belowValue(val, theType=theType),
                     Cut.aboveAll(theType=theType))
