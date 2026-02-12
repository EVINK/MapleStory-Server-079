"""
SpeedRunner - Converted from Java source
Original: server/SpeedRunner.java
Package: server
"""

from enum import Enum
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.maps.SpeedRunType import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class SpeedRunner:
    """
    Class SpeedRunner
    """

    def __init__(self):
        self.speedRunData = None
        self.speedRunData = new EnumMap<SpeedRunType, Pair<String, Map<Integer, String>>>(SpeedRunType.class)

    # Static initializer
    # instance = SpeedRunner()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getSpeedRunData(self, type: Any) -> Any:
        return self.speedRunData.get(type)

    def addSpeedRunData(self, type: Any, mib: Any) -> None:
        self.speedRunData.put(type, new Pair<String, Map<Integer, String>>(mib.getLeft(), mib.getRight()))

    def removeSpeedRunData(self, type: Any) -> None:
        self.speedRunData.remove(type)

    def loadSpeedRuns(self) -> None:
        if self.speedRunData > 0:
            return
        for type in SpeedRunType.values():
            self.loadSpeedRunData(type)

    def loadSpeedRunData(self, type: Any) -> None:
        ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM speedruns WHERE type = ? ORDER BY time LIMIT 25")
        ps.setString(1, type.name())
        ret = "") + ".#k\r\n\r\n")
        rett = {}
        rs = ps.executeQuery()
        rank = 1
        changed = None
        cont = changed = rs.first()
        while cont:
            self.addSpeedRunData(ret, rett, rs.getString("members"), rs.getString("leader"), rank, rs.getString("timestring"))
            rank += 1
        rs.close()
        ps.close()
        if changed:
            self.speedRunData.put(type, new Pair<String, Map<Integer, String>>(ret, rett))

    def addSpeedRunData_ret_rett_members_leader_rank_timestring(self, ret: Any, rett: dict, members: str, leader: str, rank: int, timestring: str) -> Any:
        rettt = ""
        membrz = members.split(",")
        rettt.append("#b该远征队 ").append(leader).append("'成功挑战排名为 ").append(rank).append(".#k\r\n\r\n")
        for i in range(len(membrz)):
            rettt.append("#r#e")
            rettt.append(i + 1)
            rettt.append(".#n ")
            rettt.append(membrz[i])
            rettt.append("#k\r\n")
        rett.put(rank, rettt)
        ret.append("#b")
        if len(membrz) > 1:
            ret.append("#L")
            ret.append(rank)
            ret.append("#")
        ret.append("Rank #e")
        ret.append(rank)
        ret.append("#n#k : ")
        ret.append(leader)
        ret.append(", in ")
        ret.append(timestring)
        if len(membrz) > 1:
            ret.append("#l")
        ret.append("\r\n")
        return new Pair<StringBuilder, Map<Integer, String>>(ret, rett)

