"""
DumpNpcNames - Converted from Java source
Original: tools/wztosql/DumpNpcNames.java
Package: tools.wztosql
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Iterator
from typing import Optional, Any
import os
import pymysql
import sys

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class DumpNpcNames:
    """
    Class DumpNpcNames
    """

    def __init__(self):
        self.con = None
        self.con = DatabaseConnection.getConnection()

    # Static initializer
    # npcNames = {}


    def main(self, args: list) -> None:
        print("Dumping npc name data.")
        dump = DumpNpcNames()
        dump.dumpNpcNameData()
        print("Dump complete.")

    def dumpNpcNameData(self) -> None:
        dataFile = File(os.environ.get("wzPath") + "/Npc.wz")
        strDataFile = File(os.environ.get("wzPath") + "/String.wz")
        npcData = MapleDataProviderFactory.getDataProvider(dataFile)
        stringDataWZ = MapleDataProviderFactory.getDataProvider(strDataFile)
        npcStringData = stringDataWZ.getData("Npc.img")
        # try-with-resources: final PreparedStatement ps = self.con.prepareStatement("DELETE FROM `wz_npcnamedata`")
        try:
            ps.execute()
        for c in npcStringData:
            nid = int(c.getName())
            n = StringUtil.getLeftPaddedStr(nid + ".img", '0', 11)
            try:
                if npcData.getData(n) is None:
                    continue
                name = MapleDataTool.getString("name", c, "MISSINGNO")
                if ("Maple TV" in name) || ("Baby Moon Bunny" in name):
                    continue
                DumpNpcNames.npcNames.put(nid, name)
            catch (NullPointerException ex2) {}
            catch (RuntimeException ex3) {}
        for key in DumpNpcNames.npcNames.keys():
            try:
                # try-with-resources: final PreparedStatement ps2 = self.con.prepareStatement("INSERT INTO `wz_npcnamedata` (`npc`, `name`) VALUES (?, ?)")
                try:
                    ps2.setInt(1, key)
                    ps2.setString(2, DumpNpcNames.npcNames.get(key))
                    ps2.execute()
                print("key: " + key + " name: " + DumpNpcNames.npcNames.get(key))
            except Exception as ex:
                print("Failed to save key " + key)

