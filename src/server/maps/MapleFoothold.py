"""
MapleFoothold - Converted from Java source
Original: server/maps/MapleFoothold.java
Package: server.maps
"""

from typing import Optional, Any


class MapleFoothold:
    """
    Class MapleFoothold
    Implements: Comparable<MapleFoothold>
    """

    def __init__(self, p1: Any, p2: Any, id: int):
        self.p1 = None
        self.p2 = None
        self.id = None
        self.next = 0
        self.prev = 0
        self.p1 = p1
        self.p2 = p2
        self.id = id


    def isWall(self) -> bool:
        return self.p1.x == self.p2.x

    def getX1(self) -> int:
        return self.p1.x

    def getX2(self) -> int:
        return self.p2.x

    def getY1(self) -> int:
        return self.p1.y

    def getY2(self) -> int:
        return self.p2.y

    def compareTo(self, o: Any) -> int:
        other = o
        if self.p2.y < other.getY1():
            return -1
        if self.p1.y > other.getY2():
            return 1
        return 0

    def equals(self, o: Any) -> bool:
        if !(isinstance(o, MapleFoothold)):
            return False
        oth = o
        return oth.getY1() == self.p1.y && oth.getY2() == self.p2.y && oth.getX1() == self.p1.x && oth.getX2() == self.p2.x && self.id == oth.getId()

    def getId(self) -> int:
        return self.id

    def getNext(self) -> int:
        return self.next

    def setNext(self, next: int) -> None:
        self.next = next

    def getPrev(self) -> int:
        return self.prev

    def setPrev(self, prev: int) -> None:
        self.prev = prev

