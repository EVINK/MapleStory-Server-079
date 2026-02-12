"""
MapleGuildRanking - Converted from Java source
Original: handling/channel/MapleGuildRanking.java
Package: handling.channel
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import pymysql
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleGuildRanking:
    """
    Class MapleGuildRanking
    """

    def __init__(self):
        self.ranks = None
        self.ranks1 = None
        self.ranks2 = None
        self.name = None
        self.meso = None
        self.str = None
        self.dex = None
        self._int = None
        self.luk = None
        self.name = None
        self.level = None
        self.str = None
        self.dex = None
        self._int = None
        self.luk = None
        self.name = None
        self.gp = None
        self.logo = None
        self.logocolor = None
        self.logobg = None
        self.logobgcolor = None
        self.ranks = []
        self.ranks1 = []
        self.ranks2 = []

    # Static initializer
    # instance = MapleGuildRanking()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def RankingUpdate(self) -> None:
        def _task_1():
            try:
                MapleGuildRanking.self.reload()
                MapleGuildRanking.self.showLevelRank()
                MapleGuildRanking.self.showMesoRank()
            except Exception as ex:
                ex.printStackTrace()
                print("Could not update rankings")

        Timer.WorldTimer.getInstance().register(_task_1, 3600000, 3600000)

    def run(self) -> None:
        try:
            MapleGuildRanking.self.reload()
            MapleGuildRanking.self.showLevelRank()
            MapleGuildRanking.self.showMesoRank()
        except Exception as ex:
            ex.printStackTrace()
            print("Could not update rankings")

    def getGuildRank(self) -> list:
        if self.ranks == 0:
            self.reload()
        return self.ranks

    def getLevelRank(self) -> list:
        if self.ranks1 == 0:
            self.showLevelRank()
        return self.ranks1

    def getMesoRank(self) -> list:
        if self.ranks2 == 0:
            self.showMesoRank()
        return self.ranks2

    def reload(self) -> None:
        self.ranks.clear()
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT * FROM guilds ORDER BY `GP` DESC LIMIT 50")
        try:
            rs = ps.executeQuery()
            while rs.next():
                rank = GuildRankingInfo(rs.getString("name"), rs.getInt("GP"), rs.getInt("logo"), rs.getInt("logoColor"), rs.getInt("logoBG"), rs.getInt("logoBGColor"))
                self.ranks.add(rank)
            rs.close()
        except Exception as e:
            print("家族排行错误" + e)

    def MapleMSpvpdeaths(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `pvpdeaths`, `str`, `dex`, `int`, `luk` FROM characters ORDER BY `pvpdeaths` DESC LIMIT 20")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.MapleMSpvpdeaths(npcid, rs))
            ps.close()
            rs.close()
        except Exception as e:
            print("failed to display guild ranks." + e)

    def MapleMSpvpkills(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `pvpkills`, `str`, `dex`, `int`, `luk` FROM characters ORDER BY `pvpkills` WHERE gm < 1 DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.MapleMSpvpkills(npcid, rs))
            ps.close()
            rs.close()
        except Exception as e:
            print("failed to display guild ranks." + e)

    def showLevelRank(self) -> None:
        self.ranks1.clear()
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM characters WHERE gm < 1 ORDER BY `level` DESC LIMIT 100")
            rs = ps.executeQuery()
            while rs.next():
                rank1 = levelRankingInfo(rs.getString("name"), rs.getInt("level"), rs.getInt("str"), rs.getInt("dex"), rs.getInt("int"), rs.getInt("luk"))
                self.ranks1.add(rank1)
            ps.close()
            rs.close()
        except Exception as e:
            print("人物排行错误")

    def showMesoRank(self) -> None:
        self.ranks2.clear()
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT *, ( chr.meso + s.meso ) as money FROM `characters` as chr , `storages` as s WHERE chr.gm < 1 AND s.accountid = chr.accountid ORDER BY money DESC LIMIT 20")
        try:
            rs = ps.executeQuery()
            while rs.next():
                rank2 = mesoRankingInfo(rs.getString("name"), rs.getLong("money"), rs.getInt("str"), rs.getInt("dex"), rs.getInt("int"), rs.getInt("luk"))
                self.ranks2.add(rank2)
            rs.close()
        except Exception as e:
            print("金币排行错误")

    def getName(self) -> str:
        return self.name

    def getMeso(self) -> int:
        return self.meso

    def getStr(self) -> int:
        return self.str

    def getDex(self) -> int:
        return self.dex

    def getInt(self) -> int:
        return self._int

    def getLuk(self) -> int:
        return self.luk

    def getLevel(self) -> int:
        return self.level

    def getGP(self) -> int:
        return self.gp

    def getLogo(self) -> int:
        return self.logo

    def getLogoColor(self) -> int:
        return self.logocolor

    def getLogoBg(self) -> int:
        return self.logobg

    def getLogoBgColor(self) -> int:
        return self.logobgcolor


# Inner class from Java (originally nested)
class mesoRankingInfo:
    """
    Class mesoRankingInfo
    """

    def __init__(self, name: str, meso: int, str: int, dex: int, intt: int, luk: int):
        self.name = None
        self.meso = None
        self.str = None
        self.dex = None
        self._int = None
        self.luk = None
        self.name = name
        self.meso = meso
        self.str = str
        self.dex = dex
        self._int = intt
        self.luk = luk


    def getName(self) -> str:
        return self.name

    def getMeso(self) -> int:
        return self.meso

    def getStr(self) -> int:
        return self.str

    def getDex(self) -> int:
        return self.dex

    def getInt(self) -> int:
        return self._int

    def getLuk(self) -> int:
        return self.luk


# Inner class from Java (originally nested)
class levelRankingInfo:
    """
    Class levelRankingInfo
    """

    def __init__(self, name: str, level: int, str: int, dex: int, intt: int, luk: int):
        self.name = None
        self.level = None
        self.str = None
        self.dex = None
        self._int = None
        self.luk = None
        self.name = name
        self.level = level
        self.str = str
        self.dex = dex
        self._int = intt
        self.luk = luk


    def getName(self) -> str:
        return self.name

    def getLevel(self) -> int:
        return self.level

    def getStr(self) -> int:
        return self.str

    def getDex(self) -> int:
        return self.dex

    def getInt(self) -> int:
        return self._int

    def getLuk(self) -> int:
        return self.luk


# Inner class from Java (originally nested)
class GuildRankingInfo:
    """
    Class GuildRankingInfo
    """

    def __init__(self, name: str, gp: int, logo: int, logocolor: int, logobg: int, logobgcolor: int):
        self.name = None
        self.gp = None
        self.logo = None
        self.logocolor = None
        self.logobg = None
        self.logobgcolor = None
        self.name = name
        self.gp = gp
        self.logo = logo
        self.logocolor = logocolor
        self.logobg = logobg
        self.logobgcolor = logobgcolor


    def getName(self) -> str:
        return self.name

    def getGP(self) -> int:
        return self.gp

    def getLogo(self) -> int:
        return self.logo

    def getLogoColor(self) -> int:
        return self.logocolor

    def getLogoBg(self) -> int:
        return self.logobg

    def getLogoBgColor(self) -> int:
        return self.logobgcolor

