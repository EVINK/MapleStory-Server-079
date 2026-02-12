"""
MapleMonsterInformationProvider - Converted from Java source
Original: server/life/MapleMonsterInformationProvider.java
Package: server.life
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes


class MapleMonsterInformationProvider:
    """
    Class MapleMonsterInformationProvider
    """

    def __init__(self):
        self.drops = None
        self.globaldrops = None
        self.drops = new HashMap<Integer, List<MonsterDropEntry>>()
        self.globaldrops = []
        self.retrieveGlobal()

    # Static initializer
    # instance = MapleMonsterInformationProvider()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getGlobalDrop(self) -> list:
        return self.globaldrops

    def retrieveGlobal(self) -> None:
        ps = None
        rs = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM drop_data_global WHERE chance > 0")
            rs = ps.executeQuery()
            while rs.next():
                self.globaldrops.add(MonsterGlobalDropEntry(rs.getInt("itemid"), rs.getInt("chance"), rs.getInt("continent"), rs.getByte("dropType"), rs.getInt("minimum_quantity"), rs.getInt("maximum_quantity"), rs.getShort("questid")))
            rs.close()
            ps.close()
        except Exception as e:
            print("Error retrieving drop" + e)
        finally:
            try:
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
            catch (SQLException ex) {}

    def retrieveDrop(self, monsterId: int) -> list:
        if (monsterId in self.drops):
            return self.drops.get(monsterId)
        ret = []
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM drop_data WHERE dropperid = ?")
            ps.setInt(1, monsterId)
            rs = ps.executeQuery()
            while rs.next():
                itemid = rs.getInt("itemid")
                chance = rs.getInt("chance")
                if GameConstants.getInventoryType(itemid) == MapleInventoryType.EQUIP:
                    chance /= 3
                ret.add(MonsterDropEntry(itemid, chance, rs.getInt("minimum_quantity"), rs.getInt("maximum_quantity"), rs.getShort("questid")))
            try:
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
            except Exception as ignore:
                return ret
        except Exception as e:
            return ret
        finally:
            try:
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
            except Exception as ignore2:
                return ret
        self.drops.put(monsterId, ret)
        return ret

    def clearDrops(self) -> None:
        self.drops.clear()
        self.globaldrops.clear()
        self.retrieveGlobal()

