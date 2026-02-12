"""
CheaterData - Converted from Java source
Original: handling/world/CheaterData.java
Package: handling.world
"""

from typing import Optional, Any


class CheaterData:
    """
    Class CheaterData
    Implements: Serializable, Comparable<CheaterData>
    """

    serialVersionUID = -8733673311051249885

    def __init__(self, points: int, info: str):
        self.points = None
        self.info = None
        self.points = points
        self.info = info


    def getInfo(self) -> str:
        return self.info

    def getPoints(self) -> int:
        return self.points

    def compareTo(self, o: Any) -> int:
        thisVal = self.getPoints()
        anotherVal = o.getPoints()
        return (thisVal < anotherVal) ? 1 : ((thisVal == anotherVal) ? 0 : -1)

    def equals(self, oth: Any) -> bool:
        if !(isinstance(oth, CheaterData)):
            return False
        obj = oth
        return obj.points == self.points && obj.info == (self.info)

