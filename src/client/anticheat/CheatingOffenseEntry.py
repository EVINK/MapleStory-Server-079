"""
CheatingOffenseEntry - Converted from Java source
Original: client/anticheat/CheatingOffenseEntry.java
Package: client.anticheat
"""

from typing import Optional, Any
import time


class CheatingOffenseEntry:
    """
    Class CheatingOffenseEntry
    """

    def __init__(self, offense: Any, characterid: int):
        self.offense = None
        self.count = 0
        self.characterid = None
        self.lastOffense = 0
        self.firstOffense = None
        self.param = ""
        self.dbid = 0
        self.count = 0
        self.dbid = -1
        self.offense = offense
        self.characterid = characterid
        self.firstOffense = int(time.time() * 1000)


    def getOffense(self) -> Any:
        return self.offense

    def getCount(self) -> int:
        return self.count

    def getChrfor(self) -> int:
        return self.characterid

    def incrementCount(self) -> None:
        self.count += 1
        self.lastOffense = int(time.time() * 1000)

    def isExpired(self) -> bool:
        return self.lastOffense < int(time.time() * 1000) - self.offense.getValidityDuration()

    def getPoints(self) -> int:
        return self.count * self.offense.getPoints()

    def getParam(self) -> str:
        return self.param

    def setParam(self, param: str) -> None:
        self.param = param

    def getLastOffenseTime(self) -> int:
        return self.lastOffense

    def getDbId(self) -> int:
        return self.dbid

    def setDbId(self, dbid: int) -> None:
        self.dbid = dbid

