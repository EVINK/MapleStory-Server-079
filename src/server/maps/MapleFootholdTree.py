"""
MapleFootholdTree - Converted from Java source
Original: server/maps/MapleFootholdTree.java
Package: server.maps
"""

from typing import List
from typing import Optional, Any
import math


class MapleFootholdTree:
    """
    Class MapleFootholdTree
    """

    def __init__(self, p1: Any, p2: Any):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.footholds = []
        self.p1 = None
        self.p2 = None
        self.center = None
        self.depth = 0
        self.maxDropX = 0
        self.minDropX = 0
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.footholds = []
        self.depth = 0
        self.p1 = p1
        self.p2 = p2
        self.center = Point((p2.x - p1.x) / 2, (p2.y - p1.y) / 2)

    # Static initializer
    # MapleFootholdTree.maxDepth = 8


    def insert(self, f: Any) -> None:
        if self.depth == 0:
            if f.getX1() > self.maxDropX:
                self.maxDropX = f.getX1()
            if f.getX1() < self.minDropX:
                self.minDropX = f.getX1()
            if f.getX2() > self.maxDropX:
                self.maxDropX = f.getX2()
            if f.getX2() < self.minDropX:
                self.minDropX = f.getX2()
        if self.depth == MapleFootholdTree.maxDepth || (f.getX1() >= self.p1.x && f.getX2() <= self.p2.x && f.getY1() >= self.p1.y && f.getY2() <= self.p2.y):
            self.footholds.add(f)
        else:
            if self.nw is None:
                self.nw = MapleFootholdTree(self.p1, self.center, self.depth + 1)
                self.ne = MapleFootholdTree(Point(self.center.x, self.p1.y), Point(self.p2.x, self.center.y), self.depth + 1)
                self.sw = MapleFootholdTree(Point(self.p1.x, self.center.y), Point(self.center.x, self.p2.y), self.depth + 1)
                self.se = MapleFootholdTree(self.center, self.p2, self.depth + 1)
            if f.getX2() <= self.center.x && f.getY2() <= self.center.y:
                self.nw.insert(f)
            elif f.getX1() > self.center.x && f.getY2() <= self.center.y:
                self.ne.insert(f)
            elif f.getX2() <= self.center.x && f.getY1() > self.center.y:
                self.sw.insert(f)
            else:
                self.se.insert(f)

    def getRelevants(self, p: Any) -> list:
        return self.getRelevants(p, [])

    def getRelevants_p_list(self, p: Any, list: list) -> list:
        list.addAll(self.footholds)
        if self.nw is not None:
            if p.x <= self.center.x && p.y <= self.center.y:
                self.nw.getRelevants(p, list)
            elif p.x > self.center.x && p.y <= self.center.y:
                self.ne.getRelevants(p, list)
            elif p.x <= self.center.x && p.y > self.center.y:
                self.sw.getRelevants(p, list)
            else:
                self.se.getRelevants(p, list)
        return list

    def findWallR(self, p1: Any, p2: Any) -> Any:
        for f in self.footholds:
            if f.isWall() && f.getX1() >= p1.x && f.getX1() <= p2.x && f.getY1() >= p1.y && f.getY2() <= p1.y:
                return f
        if self.nw is not None:
            if p1.x <= self.center.x && p1.y <= self.center.y:
                ret = self.nw.findWallR(p1, p2)
                if ret is not None:
                    return ret
            if (p1.x > self.center.x || p2.x > self.center.x) && p1.y <= self.center.y:
                ret = self.ne.findWallR(p1, p2)
                if ret is not None:
                    return ret
            if p1.x <= self.center.x && p1.y > self.center.y:
                ret = self.sw.findWallR(p1, p2)
                if ret is not None:
                    return ret
            if (p1.x > self.center.x || p2.x > self.center.x) && p1.y > self.center.y:
                ret = self.se.findWallR(p1, p2)
                if ret is not None:
                    return ret
        return None

    def findWall(self, p1: Any, p2: Any) -> Any:
        if p1.y != p2.y:
            raise ValueError()
        return self.findWallR(p1, p2)

    def checkRelevantFH(self, fromx: int, fromy: int, tox: int, toy: int) -> bool:
        fhdata = None
        for fh in self.footholds:
            if fh.getX1() <= fromx && fh.getX2() >= fromx && fh.getY1() <= fromy && fh.getY2() >= fromy:
                fhdata = fh
                break
        for fh2 in self.footholds:
            if fh2.getX1() <= tox && fh2.getX2() >= tox && fh2.getY1() <= toy && fh2.getY2() >= toy:
                if fhdata.getId() != fh2.getId() && fh2.getId() != fhdata.getNext() && fh2.getId() != fhdata.getPrev():
                    print("Couldn't find the correct pos for next/prev")
                    return False
                return True
        return False

    def findBelow(self, p: Any) -> Any:
        relevants = self.getRelevants(p)
        xMatches = []
        for fh in relevants:
            if fh.getX1() <= p.x && fh.getX2() >= p.x:
                if fh.getX1() == fh.getX2():
                    continue
                xMatches.add(fh)
        Collections.sort(xMatches)
        for fh in xMatches:
            if !fh.isWall() && fh.getY1() != fh.getY2():
                s1 = abs(fh.getY2() - fh.getY1())
                s2 = abs(fh.getX2() - fh.getX1())
                s3 = abs(p.x - fh.getX1())
                alpha = Math.atan(s2 / s1)
                beta = Math.atan(s1 / s2)
                s4 = Math.cos(alpha) * (s3 / Math.cos(beta))
                calcY = None
                if fh.getY2() < fh.getY1():
                    calcY = fh.getY1() - s4
                else:
                    calcY = fh.getY1() + s4
                if calcY >= p.y:
                    return fh
                continue
            else:
                if !fh.isWall() && fh.getY1() >= p.y:
                    return fh
                continue
        return None

    def getX1(self) -> int:
        return self.p1.x

    def getX2(self) -> int:
        return self.p2.x

    def getY1(self) -> int:
        return self.p1.y

    def getY2(self) -> int:
        return self.p2.y

    def getMaxDropX(self) -> int:
        return self.maxDropX

    def getMinDropX(self) -> int:
        return self.minDropX

