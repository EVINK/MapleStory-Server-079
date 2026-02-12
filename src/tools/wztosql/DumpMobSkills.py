"""
DumpMobSkills - Converted from Java source
Original: tools/wztosql/DumpMobSkills.java
Package: tools.wztosql
"""

from pathlib import Path
from pymysql import Connection
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys
import time

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes


class DumpMobSkills:
    """
    Class DumpMobSkills
    """

    def __init__(self, update: bool):
        self.skill = None
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = None
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = DatabaseConnection.getConnection()
        self.update = update
        self.skill = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Skill.wz"))
        if self.skill is None:
            self.hadError = True


    def main(self, args: list) -> None:
        hadError = False
        update = False
        startTime = int(time.time() * 1000)
        for file in args:
            if file.lower() == "-update".lower():
                update = True
        currentQuest = 0
        try:
            dq = DumpMobSkills(update)
            print("Dumping mobskills")
            dq.dumpMobSkills()
            hadError |= dq.isHadError()
            currentQuest = dq.currentId()
        except Exception as e:
            hadError = True
            print(e)
            print(currentQuest + " skill.")
        endTime = int(time.time() * 1000)
        elapsedSeconds = (endTime - startTime) / 1000.0
        elapsedSecs = elapsedSeconds % 60
        elapsedMinutes = (int)(elapsedSeconds / 60.0)
        withErrors = ""
        if hadError:
            withErrors = " with errors"
        print("Finished" + withErrors + " in " + elapsedMinutes + " minutes " + elapsedSecs + " seconds")

    def isHadError(self) -> bool:
        return self.hadError

    def dumpMobSkills(self) -> None:
        if !self.hadError:
            ps = self.con.prepareStatement("INSERT INTO wz_mobskilldata(skillid, `level`, hp, mpcon, x, y, time, prop, `limit`, spawneffect,`interval`, summons, ltx, lty, rbx, rby, once) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            try:
                self.dumpMobSkills(ps)
            except Exception as e:
                print(self.id + " skill.")
                print(e)
                self.hadError = True
            finally:
                ps.executeBatch()
                ps.close()

    def delete(self, sql: str) -> None:
        ps = self.con.prepareStatement(sql)
        ps.executeUpdate()
        ps.close()

    def doesExist(self, sql: str) -> bool:
        ps = self.con.prepareStatement(sql)
        rs = ps.executeQuery()
        ret = rs.next()
        rs.close()
        ps.close()
        return ret

    def dumpMobSkills_ps(self, ps: Any) -> None:
        if !self.update:
            self.delete("DELETE FROM wz_mobskilldata")
            print("Deleted wz_mobskilldata successfully.")
        skillz = self.skill.getData("MobSkill.img")
        print("Adding into wz_mobskilldata.....")
        for ids in skillz.getChildren():
            for lvlz in ids.getChildByPath("level").getChildren():
                self.id = int(ids.getName())
                lvl = int(lvlz.getName())
                if self.update && self.doesExist("SELECT * FROM wz_mobskilldata WHERE skillid = " + self.id + " AND level = " + lvl):
                    continue
                ps.setInt(1, self.id)
                ps.setInt(2, lvl)
                ps.setInt(3, MapleDataTool.getInt("hp", lvlz, 100))
                ps.setInt(4, MapleDataTool.getInt("mpCon", lvlz, 0))
                ps.setInt(5, MapleDataTool.getInt("x", lvlz, 1))
                ps.setInt(6, MapleDataTool.getInt("y", lvlz, 1))
                ps.setInt(7, MapleDataTool.getInt("time", lvlz, 0))
                ps.setInt(8, MapleDataTool.getInt("prop", lvlz, 100))
                ps.setInt(9, MapleDataTool.getInt("limit", lvlz, 0))
                ps.setInt(10, MapleDataTool.getInt("summonEffect", lvlz, 0))
                ps.setInt(11, MapleDataTool.getInt("interval", lvlz, 0))
                summ = ""
                toSummon = []
                i = 0
                while i > -1 && lvlz.getChildByPath(str(i)) is not None:
                    toSummon.add(MapleDataTool.getInt(lvlz.getChildByPath(str(i)), 0))
                for summon in toSummon:
                    if summ > 0:
                        summ.append(", ")
                    summ.append(str(summon))
                ps.setString(12, summ)
                if lvlz.getChildByPath("lt") is not None:
                    lt = lvlz.getChildByPath("lt").getData()
                    ps.setInt(13, lt.x)
                    ps.setInt(14, lt.y)
                else:
                    ps.setInt(13, 0)
                    ps.setInt(14, 0)
                if lvlz.getChildByPath("rb") is not None:
                    rb = lvlz.getChildByPath("rb").getData()
                    ps.setInt(15, rb.x)
                    ps.setInt(16, rb.y)
                else:
                    ps.setInt(15, 0)
                    ps.setInt(16, 0)
                ps.setByte(17, (byte)((MapleDataTool.getInt("summonOnce", lvlz, 0) > 0) ? 1 : 0))
                print("Added skill: " + self.id + " level " + lvl)
                ps.addBatch()
        print("Done wz_mobskilldata...")

    def currentId(self) -> int:
        return self.id

