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
            If bound(s) are not Cut objects
        """
        if not all(map(lambda x: isinstance(x, Cut), (lowerCut,upperCut))):
            raise ValueError("Bounds must be Cut objects")
        self.lowerCut = lowerCut
        self.upperCut = upperCut
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
        return (self.lowerCut.isLessThan(val) and \
                self.upperCut.isGreaterThan(val))
    @staticmethod
    def _validate_cutpoints(*pts):
        if not all(map(lambda x: hasattr(x, "__lt__") and \
                       hasattr(x, "__gt__"), pts)):
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
            If type(s) are not comparable or compatible
        
        Returns
        -------
        A Range object (lower, upper)
        """
        # Ensure cutpoints are of compatible, appropriate types
        Range._validate_cutpoints(lower, upper)
        theType = Range._get_type(lower,upper)
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
