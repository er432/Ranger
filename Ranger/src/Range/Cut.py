
class Cut(object):
    """
    Class used to represent a cutpoint in a range, such that any range can
    be represented by 2 Cuts
    """
    def __init__(self, theType, aboveAll=False, belowAll=False, point = None,
                 below = False):
        """ Instantiates a cut point

        Parameters
        ----------
        theType : type
            Specify the most inclusive type that can be used for comparison
        aboveAll : boolean
            Specifies that cut point is above all possible values
            within the domain
        belowAll : boolean
            Specifies that cut point is below all possible values
            within the domain
        point : instance of the domain
            A specific point in the domain where the cut should
            occur
        below : boolean
            If true, cut point is infinitesimally below specified point.
            Otherwise, is infinitesimally above specified point 
            
        Raises
        ------
        ValueError
            If input is invalid
        """
        self.theType = theType
        self.aboveAll = False
        self.belowAll = False
        self.point = None
        self.below = False
        # Validate input
        if point is None:
            if not any((aboveAll, belowAll)):
                raise ValueError("Must specify a type of cut point")
            elif all((aboveAll, belowAll)):
                raise ValueError("Cannot be both aboveAll and belowAll")
            else:
                # Correct input
                self.aboveAll = aboveAll
                self.belowAll = belowAll
        else:
            if any((aboveAll, belowAll)):
                raise ValueError("Cannot be both point and above/below all")
            elif not isinstance(point, theType):
                raise ValueError("Point must be instance of theType")
            else:
                self.point = point
                self.below = below
    def _validate_query_pt(self, pt):
        if not isinstance(pt, self.theType):
            raise ValueError("Type is not compatible with cutpoint type")
        return True
    def __hash__(self):
        if self.belowAll:
            return hash(self.theType)*31-hash(None)
        elif self.aboveAll:
            return hash(self.theType)*31+hash(None)
        elif self.below:
            return hash(self.theType)*31-hash(self.point)
        else:
            return hash(self.theType)*31+hash(self.point)
    def __repr__(self):
        if self.belowAll:
            return "Cut(Below all %s)" % str(self.theType)
        elif self.aboveAll:
            return "Cut(Above all %s)" % str(self.theType)
        elif self.below:
            return "Cut(Below %s)" % str(self.point)
        else:
            return "Cut(Above %s)" % str(self.point)
    def __cmp__(self, other):
        if self == other:
            return 0
        elif self < other:
            return -1
        elif self > other: return 1
    def __eq__(self, other):
        """ Returns whether Cuts are at EXACT same place """
        if not isinstance(other, Cut):
            return False
        elif self.aboveAll:
            return other.aboveAll
        elif self.belowAll:
            return other.belowAll
        elif (self.point is not None) and (other.point is not None):
            return ((self.point == other.point) and (self.below == other.below))
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __lt__(self, other):
        """ Returns whether cutpoint is less than a specified value """
        if isinstance(other, Cut):
            if self.belowAll:
                return True
            elif self.aboveAll:
                return False
            elif other.belowAll:
                return False
            elif other.aboveAll:
                return True
            else:
                if self.point < other.point:
                    return True
                elif self.point == other.point and self.below and \
                  not other.below:
                    return True
                else:
                    return False
        else:
            return self.isLessThan(other)
    def __gt__(self, other):
        """ Returns whether cutpoint is greater than a specified value """
        if isinstance(other, Cut):
            if self.belowAll:
                return False
            elif self.aboveAll:
                return True
            elif other.belowAll:
                return True
            elif other.aboveAll:
                return False
            else:
                if self.point > other.point:
                    return True
                elif self.point == other.point and not self.below and \
                  other.below:
                    return True
                else:
                    return False
        else:
            return self.isGreaterThan(other)
    def __ge__(self, other):
        return (self.__eq__(other) or self.__gt__(other))
    def __le__(self, other):
        return (self.__eq__(other) or self.__lt__(other))
    def isLessThan(self, val):
        """ Returns whether the cutpoint is less than a specified value

        Parameters
        ----------
        val : Comparable, of compatible type
            The value to compare the cutpoint to

        Raises
        ------
        ValueError
            If the value type not compatible with cutpoint type

        Returns
        -------
        True if the cutpoint is strictly less than the specified value
        """
        self._validate_query_pt(val)
        if self.belowAll: return True
        elif self.aboveAll:
            return False
        elif self.point < val:
            return True
        elif self.point == val and self.below:
            return True
        else:
            return False
    def isGreaterThan(self, val):
        """ Returns whether the cutpoint is greater than a specified value

        Parameters
        ----------
        val : Comparable, of compatible type
            The value to compare the cutpoint to

        Raises
        ------
        ValueError
            If the value type not compatible with cutpoint type

        Returns
        -------
        True if the cutpoint is strictly greater than the specified value
        """
        self._validate_query_pt(val)
        if self.aboveAll: return True
        elif self.belowAll: return False
        elif self.point > val:
            return True
        elif self.point == val and not self.below:
            return True
        else:
            return False
    @staticmethod
    def belowValue(val, theType = None):
        """ Create a cut point, where everything below some value is
        included

        Parameters
        ----------
        val : value in the domain
            Cut point, where everything below value is included
        theType : type
            Most inclusive type that can be used for comparison. If
            None, then the type of the value is used
        Returns
        -------
        The cut object
        """
        if theType is None:
            return Cut(type(val), point=val, below=True)
        else:
            return Cut(theType, point=val, below=True)
    @staticmethod
    def belowAll(theType):
        """ Create a cut point outside the lower end of the domain

        Parameters
        ----------
        theType : type
            Most inclusive type that can be used for comparison.
         
        Returns
        -------
        The cut object
        """
        return Cut(theType, belowAll=True)
    @staticmethod
    def aboveValue(val, theType=None):
        """ Create a cut point, where everything above some value is
        included

        Parameters
        ----------
        val : value in the domain
            Cut point, where everything above value is included
        theType : type
            Most inclusive type that can be used for comparison. If
            None, then the type of the value is used
         
        Returns
        -------
        The cut object
        """
        if theType is None:
            return Cut(type(val), point=val, below=False)
        else:
            return Cut(theType, point=val, below=False)
    @staticmethod
    def aboveAll(theType):
        """ Create a cut point outside the upper end of the domain

        Parameters
        ----------
        theType : type
            Most inclusive type that can be used for comparison
        
        Returns
        -------
        The cut object
        """
        return Cut(theType, aboveAll=True)

    
