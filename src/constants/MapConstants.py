"""
MapConstants - Converted from Java source
Original: constants/MapConstants.java
Package: constants
"""

from typing import Optional, Any


class MapConstants:
    """
    Class MapConstants
    """


    def isStartingEventMap(self, mapid: int) -> bool:
        # switch (mapid):
            # case 109010000:
            # case 109020001:
            # case 109030001:
            # case 109030101:
            # case 109030201:
            # case 109030301:
            # case 109030401:
            # case 109040000:
            # case 109060001:
            # case 109060002:
            # case 109060003:
            # case 109060004:
            # case 109060005:
            # case 109060006:
            # case 109080000:
            # case 109080001:
            # case 109080002:
            # case 109080003:
                return True
            # default:
                return False

    def isEventMap(self, mapid: int) -> bool:
        return (mapid >= 109010000 and mapid < 109050000) or (mapid > 109050001 and mapid < 109090000)

