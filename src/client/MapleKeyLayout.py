"""
MapleKeyLayout - Converted from Java source
Original: client/MapleKeyLayout.java
Package: client
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class MapleKeyLayout:
    """
    Class MapleKeyLayout
    Implements: Serializable
    """

    def __init__(self):
        self.changed = False
        self.keymap = {}
        self.changed = False
        self.keymap = new HashMap<Integer, Pair<Byte, Integer>>()

    # Static initializer
    # MapleKeyLayout.serialVersionUID = 9179541993413738569


    def Layout(self) -> dict:
        self.changed = True
        return self.keymap

    def writeData(self, mplew: Any) -> None:
        for x in range(90):
            binding = self.keymap.get(x)
            if binding is not None:
                mplew.write(binding.getLeft())
                mplew.writeInt(binding.getRight())
            else:
                mplew.write(0)
                mplew.writeInt(0)

    def saveKeys(self, charid: int) -> None:
        if not self.changed or self.keymap == 0:
            return
        con = DatabaseConnection.getConnection()
        ps = None
        ps2 = None
        rs = None
        ps = con.prepareStatement("SELECT * FROM keymap WHERE `characterid` = ?")
        ps.setInt(1, charid)
        rs = ps.executeQuery()
        while rs.next():
            key = rs.getInt("key")
            find = False
            for (final Map.Entry<Integer, Pair<Byte, Integer>> keybinding : self.keymap.items())
                if key == keybinding.getKey():
                    find = True
                    break
            if not find:
                ps2 = con.prepareStatement("DELETE FROM keymap WHERE `characterid` = ? AND `key` = ?")
                ps2.setInt(1, charid)
                ps2.setInt(2, key)
                ps2.execute()
                ps2.close()
        ps.close()
        rs.close()
        ps = con.prepareStatement("SELECT * FROM keymap WHERE `characterid` = ? AND `key` = ? LIMIT 1")
        ps.setInt(1, charid)
        for (final Map.Entry<Integer, Pair<Byte, Integer>> keybinding2 : self.keymap.items())
            key2 = keybinding2.getKey()
            ps.setInt(2, key2)
            rs = ps.executeQuery()
            if rs.next():
                ps2 = con.prepareStatement("UPDATE keymap SET `type` = ?, `action` = ? WHERE `characterid` = ? AND `key` = ?")
                ps2.setInt(1, keybinding2.getValue().getLeft())
                ps2.setInt(2, keybinding2.getValue().getRight())
                ps2.setInt(3, charid)
                ps2.setInt(4, key2)
                ps2.executeUpdate()
                ps2.close()
            else:
                ps2 = con.prepareStatement("INSERT INTO keymap (`characterid`, `key`, `type`, `action`) VALUES (?, ?, ?, ?)")
                ps2.setInt(1, charid)
                ps2.setInt(2, key2)
                ps2.setInt(3, keybinding2.getValue().getLeft())
                ps2.setInt(4, keybinding2.getValue().getRight())
                ps2.execute()
                ps2.close()
            rs.close()
        ps.close()

