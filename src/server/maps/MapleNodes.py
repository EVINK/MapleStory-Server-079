"""
MapleNodes - Converted from Java source
Original: server/maps/MapleNodes.java
Package: server.maps
"""

from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from tools.Pair import *  # TODO: import specific classes


class MapleNodes:
    """
    Class MapleNodes
    """

    def __init__(self, mapid: int):
        self.nodes = None
        self.areas = None
        self.platforms = None
        self.monsterPoints = None
        self.skillIds = None
        self.mobsToSpawn = None
        self.guardiansToSpawn = None
        self.nodeStart = 0
        self.nodeEnd = 0
        self.mapid = None
        self.firstHighest = False
        self.node = 0
        self.key = 0
        self.x = 0
        self.y = 0
        self.attr = 0
        self.edge = []
        self.name = ""
        self.start = 0
        self.speed = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.r = 0
        self.SN = []
        self.x = 0
        self.y = 0
        self.fh = 0
        self.cy = 0
        self.team = 0
        self.nodeStart = -1
        self.nodeEnd = -1
        self.firstHighest = True
        self.nodes = {}
        self.areas = []
        self.platforms = []
        self.skillIds = []
        self.monsterPoints = []
        self.mobsToSpawn = new ArrayList<Pair<Integer, Integer>>()
        self.guardiansToSpawn = new ArrayList<Pair<Point, Integer>>()
        self.mapid = mapid


    def setNodeStart(self, ns: int) -> None:
        self.nodeStart = ns

    def setNodeEnd(self, ns: int) -> None:
        self.nodeEnd = ns

    def addNode(self, mni: Any) -> None:
        self.nodes.put(mni.key, mni)

    def getNodes(self) -> list:
        return [])

    def getNode(self, index: int) -> Any:
        i = 1
        for x in self.getNodes():
            if i == index:
                return x
            i += 1
        return None

    def getNextNode(self, mni: Any) -> int:
        if mni is None:
            return -1
        self.addNode(mni)
        ret = -1
        for i in mni.edge:
            if self.nodes.get(i) is None:
                if ret != -1 && self.mapid / 100 == 9211204:
                    if self.firstHighest:
                        self.firstHighest = False
                        ret = max(ret, i)
                        break
                    ret = min(ret, i)
                else:
                    ret = i
        return ret

    def sortNodes(self) -> None:
        if self.nodes <= 0 || self.nodeStart < 0:
            return
        unsortedNodes = {}
        nodeSize = unsortedNodes
        self.nodes.clear()
        for (int nextNode = self.getNextNode(unsortedNodes.get(self.nodeStart)); self.nodes != nodeSize && nextNode >= 0; nextNode = self.getNextNode(unsortedNodes.get(nextNode))) {}

    def addMapleArea(self, rec: Any) -> None:
        self.areas.add(rec)

    def getAreas(self) -> list:
        return []

    def getArea(self, index: int) -> Any:
        return self.getAreas().get(index)

    def addPlatform(self, mp: Any) -> None:
        self.platforms.add(mp)

    def getPlatforms(self) -> list:
        return []

    def getMonsterPoints(self) -> list:
        return self.monsterPoints

    def addMonsterPoint(self, x: int, y: int, fh: int, cy: int, team: int) -> None:
        self.monsterPoints.add(MonsterPoint(x, y, fh, cy, team))

    def addMobSpawn(self, mobId: int, spendCP: int) -> None:
        self.mobsToSpawn.add(new Pair<Integer, Integer>(mobId, spendCP))

    def getMobsToSpawn(self) -> list:
        return self.mobsToSpawn

    def addGuardianSpawn(self, guardian: Any, team: int) -> None:
        self.guardiansToSpawn.add(new Pair<Point, Integer>(guardian, team))

    def getGuardians(self) -> list:
        return self.guardiansToSpawn

    def getSkillIds(self) -> list:
        return self.skillIds

    def addSkillId(self, z: int) -> None:
        self.skillIds.add(z)


# Inner class from Java (originally nested)
class MapleNodeInfo:
    """
    Class MapleNodeInfo
    """

    def __init__(self, node: int, key: int, x: int, y: int, attr: int, edge: list):
        self.node = 0
        self.key = 0
        self.x = 0
        self.y = 0
        self.attr = 0
        self.edge = []
        self.node = node
        self.key = key
        self.x = x
        self.y = y
        self.attr = attr
        self.edge = edge



# Inner class from Java (originally nested)
class MaplePlatform:
    """
    Class MaplePlatform
    """

    def __init__(self, name: str, start: int, speed: int, x1: int, y1: int, x2: int, y2: int, r: int, SN: list):
        self.name = ""
        self.start = 0
        self.speed = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.r = 0
        self.SN = []
        self.name = name
        self.start = start
        self.speed = speed
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.r = r
        self.SN = SN



# Inner class from Java (originally nested)
class MonsterPoint:
    """
    Class MonsterPoint
    """

    def __init__(self, x: int, y: int, fh: int, cy: int, team: int):
        self.x = 0
        self.y = 0
        self.fh = 0
        self.cy = 0
        self.team = 0
        self.x = x
        self.y = y
        self.fh = fh
        self.cy = cy
        self.team = team


