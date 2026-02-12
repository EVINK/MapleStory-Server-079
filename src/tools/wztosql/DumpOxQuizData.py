"""
DumpOxQuizData - Converted from Java source
Original: tools/wztosql/DumpOxQuizData.java
Package: tools.wztosql
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
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


class DumpOxQuizData:
    """
    Class DumpOxQuizData
    """

    def __init__(self):
        self.con = None
        self.con = DatabaseConnection.getConnection()

    # Static initializer
    # DumpOxQuizData.asciiEncoder = Charset.forName("ISO-8859-1").newEncoder()


    def main(self, args: list) -> None:
        print("OXQuiz.img Loading ...")
        dump = DumpOxQuizData()
        dump.dumpOxData()
        print("Ox quiz data is complete")

    def dumpOxData(self) -> None:
        stringProvider = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
        ox = stringProvider.getData("OXQuiz.img")
        ps = self.con.prepareStatement("DELETE FROM `wz_oxdata`")
        ps.execute()
        ps.close()
        for child1 in ox.getChildren():
            for child2 in child1.getChildren():
                q = child2.getChildByPath("q")
                d = child2.getChildByPath("d")
                a = MapleDataTool.getInt(child2.getChildByPath("a"))
                qs = ""
                ds = ""
                as = None
                if a == 0:
                    as = "x"
                else:
                    as = "o"
                if q is not None:
                    qs = q.getData()
                if d is not None:
                    ds = d.getData()
                if DumpOxQuizData.asciiEncoder.canEncode(child1.getName()) and DumpOxQuizData.asciiEncoder.canEncode(child2.getName()) and DumpOxQuizData.asciiEncoder.canEncode(qs) and DumpOxQuizData.asciiEncoder.canEncode(ds):
                    if not DumpOxQuizData.asciiEncoder.canEncode(as):
                        continue
                    ps = self.con.prepareStatement("INSERT INTO `wz_oxdata` (`questionset`, `questionid`, `question`, `display`, `answer`) VALUES (?, ?, ?, ?, ?)")
                    ps.setString(1, child1.getName())
                    ps.setString(2, child2.getName())
                    ps.setString(3, qs)
                    ps.setString(4, ds)
                    ps.setString(5, as)
                    ps.execute()
                    ps.close()

