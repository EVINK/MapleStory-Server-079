"""
MaplePvpStats - Converted from Java source
Original: client/MaplePvpStats.java
Package: client
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class MaplePvpStats:
    """
    Class MaplePvpStats
    Implements: Serializable
    """

    serialVersionUID = -639523813413728519

    def __init__(self, watk: int, matk: int, wdef: int, mdef: int, acc: int, avoid: int, wdef_rate: int, mdef_rate: int, ignore_def: int, damage_rate: int, ignore_damage: int):
        self.watk = 0
        self.matk = 0
        self.wdef = 0
        self.mdef = 0
        self.acc = 0
        self.avoid = 0
        self.wdef_rate = 0
        self.mdef_rate = 0
        self.ignore_def = 0
        self.damage_rate = 0
        self.ignore_damage = 0
        self.watk = watk
        self.matk = matk
        self.wdef = wdef
        self.mdef = mdef
        self.acc = acc
        self.avoid = avoid
        self.wdef_rate = wdef_rate
        self.mdef_rate = mdef_rate
        self.ignore_def = ignore_def
        self.damage_rate = damage_rate
        self.ignore_damage = ignore_damage


    def loadOrCreateFromDB(self, accountId: int) -> Any:
        ret = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM pvpstats WHERE accountid = ?")
            ps.setInt(1, accountId)
            rs = ps.executeQuery()
            if rs.next():
                ret = MaplePvpStats(rs.getInt("watk"), rs.getInt("matk"), rs.getInt("wdef"), rs.getInt("mdef"), rs.getInt("acc"), rs.getInt("avoid"), rs.getInt("wdef_rate"), rs.getInt("mdef_rate"), rs.getInt("ignore_def"), rs.getInt("damage_rate"), rs.getInt("ignore_damage"))
            else:
                psu = con.prepareStatement("INSERT INTO pvpstats (accountid, watk, matk, wdef, mdef, acc, avoid, wdef_rate, mdef_rate, ignore_def, damage_rate, ignore_damage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                psu.setInt(1, accountId)
                psu.setInt(2, 0)
                psu.setInt(3, 0)
                psu.setInt(4, 0)
                psu.setInt(5, 0)
                psu.setInt(6, 100)
                psu.setInt(7, 0)
                psu.setInt(8, 0)
                psu.setInt(9, 0)
                psu.setInt(10, 0)
                psu.setInt(11, 0)
                psu.setInt(12, 0)
                psu.executeUpdate()
                psu.close()
                ret = MaplePvpStats(0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0)
            rs.close()
            ps.close()
        except Exception as ex:
            print("加载角色 Pvp 属性出现错误." + ex)
        return ret

    def saveToDb(self, accountId: int) -> None:
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("UPDATE pvpstats SET watk = ?, matk = ?, wdef = ?, mdef = ?, acc = ?, avoid = ?, wdef_rate = ?, mdef_rate = ?, ignore_def = ?, damage_rate = ?, ignore_damage = ? WHERE accountId = ?")
            ps.setInt(1, accountId)
            ps.setInt(2, self.watk)
            ps.setInt(3, self.matk)
            ps.setInt(4, self.wdef)
            ps.setInt(5, self.mdef)
            ps.setInt(6, self.acc)
            ps.setInt(7, self.avoid)
            ps.setInt(8, self.wdef_rate)
            ps.setInt(9, self.mdef_rate)
            ps.setInt(10, self.ignore_def)
            ps.setInt(11, self.damage_rate)
            ps.setInt(12, self.ignore_damage)
            ps.executeUpdate()
            ps.close()
        except Exception as ex:
            print("保存角色 Pvp 属性出现错误." + ex)

    def getWatk(self) -> int:
        return self.watk

    def setWatk(self, gain: int) -> None:
        self.watk = gain

    def gainWatk(self, gain: int) -> None:
        self.watk += gain

    def getMatk(self) -> int:
        return self.matk

    def setMatk(self, gain: int) -> None:
        self.matk = gain

    def gainMatk(self, gain: int) -> None:
        self.matk += gain

    def getWdef(self) -> int:
        return self.wdef

    def setWdef(self, gain: int) -> None:
        self.wdef = gain

    def gainWdef(self, gain: int) -> None:
        self.wdef += gain

    def getMdef(self) -> int:
        return self.mdef

    def setMdef(self, gain: int) -> None:
        self.mdef = gain

    def gainMdef(self, gain: int) -> None:
        self.mdef += gain

    def getAcc(self) -> int:
        return self.acc

    def setAcc(self, gain: int) -> None:
        self.acc = gain

    def gainAcc(self, gain: int) -> None:
        self.acc += gain

    def getAvoid(self) -> int:
        return self.avoid

    def setAvoid(self, gain: int) -> None:
        self.avoid = gain

    def gainAvoid(self, gain: int) -> None:
        self.avoid += gain

    def getWdefRate(self) -> int:
        return self.wdef_rate

    def setWdefRate(self, gain: int) -> None:
        self.wdef_rate = gain

    def gainWdefRate(self, gain: int) -> None:
        self.wdef_rate += gain

    def getMdefRate(self) -> int:
        return self.mdef_rate

    def setMdefRate(self, gain: int) -> None:
        self.mdef_rate = gain

    def gainMdefRate(self, gain: int) -> None:
        self.mdef_rate += gain

    def getIgnoreDef(self) -> int:
        return self.ignore_def

    def setIgnoreDef(self, gain: int) -> None:
        self.ignore_def = gain

    def gainIgnoreDef(self, gain: int) -> None:
        self.ignore_def += gain

    def getDamageRate(self) -> int:
        return self.damage_rate

    def setDamageRate(self, gain: int) -> None:
        self.damage_rate = gain

    def gainDamageRate(self, gain: int) -> None:
        self.damage_rate += gain

    def getIgnoreDamage(self) -> int:
        return self.ignore_damage

    def setIgnoreDamage(self, gain: int) -> None:
        self.ignore_damage = gain

    def gainIgnoreDamage(self, gain: int) -> None:
        self.ignore_damage += gain

