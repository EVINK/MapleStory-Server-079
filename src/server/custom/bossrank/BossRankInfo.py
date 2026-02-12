"""
BossRankInfo - Converted from Java source
Original: server/custom/bossrank/BossRankInfo.java
Package: server.custom.bossrank
"""

from typing import Optional, Any


class BossRankInfo:
    """
    Class BossRankInfo
    """

    def __init__(self):
        self.cid = 0
        self.cname = ""
        self.bossname = ""
        self.points = 0
        self.count = 0


    def getCid(self) -> int:
        return self.cid

    def setCid(self, cid: int) -> None:
        self.cid = cid

    def getCname(self) -> str:
        return self.cname

    def setCname(self, cname: str) -> None:
        self.cname = cname

    def getBossname(self) -> str:
        return self.bossname

    def setBossname(self, bossname: str) -> None:
        self.bossname = bossname

    def getPoints(self) -> int:
        return self.points

    def setPoints(self, points: int) -> None:
        self.points = points

    def getCount(self) -> int:
        return self.count

    def setCount(self, count: int) -> None:
        self.count = count

