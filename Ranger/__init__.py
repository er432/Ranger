from Ranger import release

__author__ = '%s <%s>\n' % release.authors['Rodgers-Melnick']
__license__ = release.license
__date__ = release.date
__version__ = release.version

# Make imports
from Ranger.src.Range.Range import Range
from Ranger.src.Collections.RangeSet import RangeSet
from Ranger.src.Collections.RangeMap import RangeMap
from Ranger.src.Collections.RangeBucketMap import RangeBucketMap
