"""
ReactorScriptManager - Converted from Java source
Original: scripting/ReactorScriptManager.java
Package: scripting
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql
import tkinter

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.maps.ReactorDropEntry import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes


class ReactorScriptManager(AbstractScriptManager):
    """
    Class ReactorScriptManager
    Extends: AbstractScriptManager
    """

    def __init__(self):
        self.drops = None
        self.drops = new HashMap<Integer, List<ReactorDropEntry>>()

    # Static initializer
    # instance = ReactorScriptManager()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def act(self, c: Any, reactor: Any) -> None:
        try:
            if c.getPlayer().isGM():
                c.getPlayer().dropMessage("[系统提示]您已经建立与reactor:" + reactor.getReactorId() + "的对话。")
            iv = self.getInvocable("reactor"+ File.separator + reactor.getReactorId() + ".js", c)
            if iv is None:
                return
            scriptengine = iv
            rm = ReactorActionManager(c, reactor)
            scriptengine.put("rm", rm)
            iv.invokeFunction("act", new Object[0])
        except Exception as e:
            print("Error executing reactor script. ReactorID: " + reactor.getReactorId() + ", ReactorName: " + reactor.getName() + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing reactor script. ReactorID: " + reactor.getReactorId() + ", ReactorName: " + reactor.getName() + ":" + e)

    def getDrops(self, rid: int) -> list:
        ret = self.drops.get(rid)
        if ret is not None:
            return ret
        ret = []
        ps = None
        rs = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM reactordrops WHERE reactorid = ?")
            ps.setInt(1, rid)
            rs = ps.executeQuery()
            while rs.next():
                ret.add(ReactorDropEntry(rs.getInt("itemid"), rs.getInt("chance"), rs.getInt("questid")))
            rs.close()
            ps.close()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ignore:
                return ret
        except Exception as e:
            print("Could not retrieve drops for reactor " + rid + e)
            return ret
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ignore2:
                return ret
        self.drops.put(rid, ret)
        return ret

    def clearDrops(self) -> None:
        self.drops.clear()

