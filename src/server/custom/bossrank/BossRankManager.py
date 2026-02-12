"""
BossRankManager - Converted from Java source
Original: server/custom/bossrank/BossRankManager.java
Package: server.custom.bossrank
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import logging
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class BossRankManager:
    """
    Class BossRankManager
    """

    def __init__(self):
        pass
        pass

    # Static initializer
    # instance = BossRankManager()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getInfoMap(self, cid: int) -> dict:
        info_map = {}
        con1 = DatabaseConnection.getConnection()
        ps = None
        rs = None
        try:
            ps = con1.prepareStatement("select * from bossrank where cid = ?")
            ps.setInt(1, cid)
            rs = ps.executeQuery()
            while rs.next():
                info = BossRankInfo()
                info.setCid(rs.getInt("cid"))
                info.setCname(rs.getString("cname"))
                info.setBossname(rs.getString("bossname"))
                info.setPoints(rs.getInt("points"))
                info.setCount(rs.getInt("count"))
                info_map.put(info.getBossname(), info)
        except Exception as Ex:
            Ex.printStackTrace()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex2)
        return info_map

    def getInfo(self, cid: int, bossname: str) -> Any:
        info = None
        con1 = DatabaseConnection.getConnection()
        ps = None
        rs = None
        try:
            ps = con1.prepareStatement("select * from bossrank where cid = ? and bossname = ?")
            ps.setInt(1, cid)
            ps.setString(2, bossname)
            rs = ps.executeQuery()
            if rs.next():
                info = BossRankInfo()
                info.setCid(rs.getInt("cid"))
                info.setCname(rs.getString("cname"))
                info.setBossname(rs.getString("bossname"))
                info.setPoints(rs.getInt("points"))
                info.setCount(rs.getInt("count"))
        except Exception as Ex:
            Ex.printStackTrace()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex2)
        return info

    def setLog(self, cid: int, cname: str, bossname: str, type: int, update: int) -> int:
        ret = -1
        info = self.getInfo(cid, bossname)
        add = False
        doUpdate = True
        if info is None:
            doUpdate = False
            add = True
            info = BossRankInfo()
            info.setCid(cid)
            info.setCname(cname)
            info.setBossname(bossname)
        # switch (type):
            # case 1:
                ret = info.getPoints() + update
                info.setPoints(ret)
                break
            # case 2:
                ret = info.getCount() + update
                info.setCount(ret)
                break
            # default:
                doUpdate = False
                break
        if not doUpdate:
            if add:
                self.add(info)
            return ret
        self.update(info)
        return ret

    def update(self, info: Any) -> None:
        if info is None:
            return
        con1 = DatabaseConnection.getConnection()
        ps = None
        try:
            ps = con1.prepareStatement("update bossrank set points = ?,count = ? where cid = ? and bossname = ?")
            ps.setInt(1, info.getPoints())
            ps.setInt(2, info.getCount())
            ps.setInt(3, info.getCid())
            ps.setString(4, info.getBossname())
            ps.executeUpdate()
        except Exception as Ex:
            Ex.printStackTrace()
            if ps is not None:
                try:
                    ps.close()
                except Exception as ex:
                    Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            if ps is not None:
                try:
                    ps.close()
                except Exception as ex2:
                    Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex2)

    def add(self, info: Any) -> None:
        if info is None:
            return
        con1 = DatabaseConnection.getConnection()
        ps = None
        try:
            ps = con1.prepareStatement("insert into bossrank (cid,cname,bossname,points,count) values (?,?,?,?,?)")
            ps.setInt(1, info.getCid())
            ps.setString(2, info.getCname())
            ps.setString(3, info.getBossname())
            ps.setInt(4, info.getPoints())
            ps.setInt(5, info.getCount())
            ps.executeUpdate()
        except Exception as Ex:
            Ex.printStackTrace()
            if ps is not None:
                try:
                    ps.close()
                except Exception as ex:
                    Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            if ps is not None:
                try:
                    ps.close()
                except Exception as ex2:
                    Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex2)

    def getRank(self, bossname: str, type: int) -> list:
        list = []
        con = DatabaseConnection.getConnection()
        ps = None
        rs = None
        try:
            # switch (type):
                # case 1:
                    ps = con.prepareStatement("SELECT * FROM bossrank WHERE bossname = ? ORDER BY points DESC LIMIT 100")
                    break
                # case 2:
                    ps = con.prepareStatement("SELECT * FROM bossrank WHERE bossname = ? ORDER BY count DESC LIMIT 100")
                    break
                # default:
                    ps = con.prepareStatement("SELECT * FROM bossrank WHERE bossname = ? ORDER BY points DESC LIMIT 100")
                    break
            ps.setString(1, bossname)
            rs = ps.executeQuery()
            while rs.next():
                info = BossRankInfo()
                info.setCid(rs.getInt("cid"))
                info.setCname(rs.getString("cname"))
                info.setBossname(rs.getString("bossname"))
                info.setPoints(rs.getInt("points"))
                info.setCount(rs.getInt("count"))
                list.add(info)
        except Exception as e:
            e.printStackTrace()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(BossRankManager.class.getName()).log(Level.SEVERE, None, ex2)
        return list


# Inner class from Java (originally nested)
class InstanceHolder:
    """
    Class InstanceHolder
    """

    # Static initializer
    # instance = BossRankManager()

    pass

