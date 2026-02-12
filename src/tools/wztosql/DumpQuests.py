"""
DumpQuests - Converted from Java source
Original: tools/wztosql/DumpQuests.java
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
# from server.quest.MapleQuestActionType import *  # TODO: import specific classes
# from server.quest.MapleQuestRequirementType import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class DumpQuests:
    """
    Class DumpQuests
    """

    def __init__(self, update: bool):
        self.quest = None
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = None
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = DatabaseConnection.getConnection()
        self.update = update
        self.quest = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Quest.wz"))
        if self.quest is None:
            self.hadError = True


    def isHadError(self) -> bool:
        return self.hadError

    def dumpQuests(self) -> None:
        if not self.hadError:
            psai = self.con.prepareStatement("INSERT INTO wz_questactitemdata(uniqueid, itemid, count, period, gender, job, jobEx, prop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            psas = self.con.prepareStatement("INSERT INTO wz_questactskilldata(uniqueid, skillid, skillLevel, masterLevel) VALUES (?, ?, ?, ?)")
            psaq = self.con.prepareStatement("INSERT INTO wz_questactquestdata(uniqueid, quest, state) VALUES (?, ?, ?)")
            ps = self.con.prepareStatement("INSERT INTO wz_questdata(questid, name, autoStart, autoPreComplete, viewMedalItem, selectedSkillID, blocked, autoAccept, autoComplete) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
            psr = self.con.prepareStatement("INSERT INTO wz_questreqdata(questid, type, name, stringStore, intStoresFirst, intStoresSecond) VALUES (?, ?, ?, ?, ?, ?)")
            psq = self.con.prepareStatement("INSERT INTO wz_questpartydata(questid, rank, mode, property, value) VALUES(?,?,?,?,?)")
            psa = self.con.prepareStatement("INSERT INTO wz_questactdata(questid, type, name, intStore, applicableJobs, uniqueid) VALUES (?, ?, ?, ?, ?, ?)")
            try:
                self.dumpQuests(psai, psas, psaq, ps, psr, psq, psa)
            except Exception as e:
                print(self.id + " quest.")
                e.printStackTrace()
                self.hadError = True
            finally:
                psai.executeBatch()
                psai.close()
                psas.executeBatch()
                psas.close()
                psaq.executeBatch()
                psaq.close()
                psa.executeBatch()
                psa.close()
                psr.executeBatch()
                psr.close()
                psq.executeBatch()
                psq.close()
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

    def dumpQuests_psai_psas_psaq_ps_psr_psq_psa(self, psai: Any, psas: Any, psaq: Any, ps: Any, psr: Any, psq: Any, psa: Any) -> None:
        if not self.update:
            self.delete("DELETE FROM wz_questdata")
            self.delete("DELETE FROM wz_questactdata")
            self.delete("DELETE FROM wz_questactitemdata")
            self.delete("DELETE FROM wz_questactskilldata")
            self.delete("DELETE FROM wz_questactquestdata")
            self.delete("DELETE FROM wz_questreqdata")
            self.delete("DELETE FROM wz_questpartydata")
            print("Deleted wz_questdata successfully.")
        checkz = self.quest.getData("Check.img")
        actz = self.quest.getData("Act.img")
        infoz = self.quest.getData("QuestInfo.img")
        pinfoz = self.quest.getData("PQuest.img")
        print("Adding into wz_questdata.....")
        uniqueid = 0
        for qz in checkz.getChildren():
            self.id = int(qz.getName())
            if self.update and self.doesExist("SELECT * FROM wz_questdata WHERE questid = " + self.id):
                continue
            ps.setInt(1, self.id)
            for i in range(2):
                reqData = qz.getChildByPath(str(i))
                if reqData is not None:
                    psr.setInt(1, self.id)
                    psr.setInt(2, i)
                    for req in reqData.getChildren():
                        if MapleQuestRequirementType.getByWZName(req.getName()) == MapleQuestRequirementType.UNDEFINED:
                            continue
                        psr.setString(3, req.getName())
                        if req.getName() == ("fieldEnter"):
                            psr.setString(4, str(MapleDataTool.getIntConvert("0", req, 0)))
                        elif req.getName() == ("end") or req.getName() == ("startscript") or req.getName() == ("endscript"):
                            psr.setString(4, MapleDataTool.getString(req, ""))
                        else:
                            psr.setString(4, str(MapleDataTool.getInt(req, 0)))
                        intStore1 = ""
                        intStore2 = ""
                        dataStore = new LinkedList<Pair<Integer, Integer>>()
                        if req.getName() == ("job"):
                            child = req.getChildren()
                            for x in range(child):
                                dataStore.add(new Pair<Integer, Integer>(i, MapleDataTool.getInt(child.get(x), -1)))
                        elif req.getName() == ("skill"):
                            child = req.getChildren()
                            for x in range(child):
                                childdata = child.get(x)
                                if childdata is not None:
                                    dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("acquire"), 0)))
                        elif req.getName() == ("quest"):
                            child = req.getChildren()
                            for x in range(child):
                                childdata = child.get(x)
                                if childdata is not None:
                                    dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("state"), 0)))
                        elif req.getName() == ("item") or req.getName() == ("mob"):
                            child = req.getChildren()
                            for x in range(child):
                                childdata = child.get(x)
                                if childdata is not None:
                                    dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("count"), 0)))
                        elif req.getName() == ("mbcard"):
                            child = req.getChildren()
                            for x in range(child):
                                childdata = child.get(x)
                                if childdata is not None:
                                    dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("min"), 0)))
                        elif req.getName() == ("pet"):
                            child = req.getChildren()
                            for x in range(child):
                                childdata = child.get(x)
                                if childdata is not None:
                                    dataStore.add(new Pair<Integer, Integer>(i, MapleDataTool.getInt(childdata.getChildByPath("id"), 0)))
                        for data in dataStore:
                            if intStore1 > 0:
                                intStore1.append(", ")
                                intStore2.append(", ")
                            intStore1.append(data.getLeft())
                            intStore2.append(data.getRight())
                        psr.setString(5, intStore1)
                        psr.setString(6, intStore2)
                        psr.addBatch()
                actData = actz.getChildByPath(self.id + "/" + i)
                if actData is not None:
                    psa.setInt(1, self.id)
                    psa.setInt(2, i)
                    for act in actData.getChildren():
                        if MapleQuestActionType.getByWZName(act.getName()) == MapleQuestActionType.UNDEFINED:
                            continue
                        psa.setString(3, act.getName())
                        if act.getName() == ("sp"):
                            psa.setInt(4, MapleDataTool.getIntConvert("0/sp_value", act, 0))
                        else:
                            psa.setInt(4, MapleDataTool.getInt(act, 0))
                        applicableJobs = ""
                        if act.getName() == ("sp") or act.getName() == ("skill"):
                            index = 0
                            while act.getChildByPath(index + "/job") is not None:
                                for d in act.getChildByPath(index + "/job"):
                                    if applicableJobs > 0:
                                        applicableJobs.append(", ")
                                    applicableJobs.append(MapleDataTool.getInt(d, 0))
                        elif act.getChildByPath("job") is not None:
                            for d2 in act.getChildByPath("job"):
                                if applicableJobs > 0:
                                    applicableJobs.append(", ")
                                applicableJobs.append(MapleDataTool.getInt(d2, 0))
                        psa.setString(5, applicableJobs)
                        psa.setInt(6, -1)
                        if act.getName() == ("item"):
                            uniqueid += 1
                            psa.setInt(6, uniqueid)
                            psai.setInt(1, uniqueid)
                            for iEntry in act.getChildren():
                                psai.setInt(2, MapleDataTool.getInt("id", iEntry, 0))
                                psai.setInt(3, MapleDataTool.getInt("count", iEntry, 0))
                                psai.setInt(4, MapleDataTool.getInt("period", iEntry, 0))
                                psai.setInt(5, MapleDataTool.getInt("gender", iEntry, 2))
                                psai.setInt(6, MapleDataTool.getInt("job", iEntry, -1))
                                psai.setInt(7, MapleDataTool.getInt("jobEx", iEntry, -1))
                                if iEntry.getChildByPath("prop") is None:
                                    psai.setInt(8, -2)
                                else:
                                    psai.setInt(8, MapleDataTool.getInt("prop", iEntry, -1))
                                psai.addBatch()
                        elif act.getName() == ("skill"):
                            uniqueid += 1
                            psa.setInt(6, uniqueid)
                            psas.setInt(1, uniqueid)
                            for sEntry in act:
                                psas.setInt(2, MapleDataTool.getInt("id", sEntry, 0))
                                psas.setInt(3, MapleDataTool.getInt("skillLevel", sEntry, 0))
                                psas.setInt(4, MapleDataTool.getInt("masterLevel", sEntry, 0))
                                psas.addBatch()
                        elif act.getName() == ("quest"):
                            uniqueid += 1
                            psa.setInt(6, uniqueid)
                            psaq.setInt(1, uniqueid)
                            for sEntry in act:
                                psaq.setInt(2, MapleDataTool.getInt("id", sEntry, 0))
                                psaq.setInt(3, MapleDataTool.getInt("state", sEntry, 0))
                                psaq.addBatch()
                        psa.addBatch()
            infoData = infoz.getChildByPath(str(self.id))
            if infoData is not None:
                ps.setString(2, MapleDataTool.getString("name", infoData, ""))
                ps.setInt(3, (MapleDataTool.getInt("autoStart", infoData, 0) > 0) ? 1 : 0)
                ps.setInt(4, (MapleDataTool.getInt("autoPreComplete", infoData, 0) > 0) ? 1 : 0)
                ps.setInt(5, MapleDataTool.getInt("viewMedalItem", infoData, 0))
                ps.setInt(6, MapleDataTool.getInt("selectedSkillID", infoData, 0))
                ps.setInt(7, MapleDataTool.getInt("blocked", infoData, 0))
                ps.setInt(8, MapleDataTool.getInt("autoAccept", infoData, 0))
                ps.setInt(9, MapleDataTool.getInt("autoComplete", infoData, 0))
            else:
                ps.setString(2, "")
                ps.setInt(3, 0)
                ps.setInt(4, 0)
                ps.setInt(5, 0)
                ps.setInt(6, 0)
                ps.setInt(7, 0)
                ps.setInt(8, 0)
                ps.setInt(9, 0)
            ps.addBatch()
            pinfoData = pinfoz.getChildByPath(str(self.id))
            if pinfoData is not None and pinfoData.getChildByPath("rank") is not None:
                psq.setInt(1, self.id)
                for d3 in pinfoData.getChildByPath("rank"):
                    psq.setString(2, d3.getName())
                    for c in d3:
                        psq.setString(3, c.getName())
                        for b in c:
                            psq.setString(4, b.getName())
                            psq.setInt(5, MapleDataTool.getInt(b, 0))
                            psq.addBatch()
            print("Added quest: " + self.id)
        print("Done wz_questdata...")

    def currentId(self) -> int:
        return self.id

    def main(self, args: list) -> None:
        hadError = False
        update = False
        startTime = int(time.time() * 1000)
        for file in args:
            if file.lower() == "-update".lower():
                update = True
        currentQuest = 0
        try:
            dq = DumpQuests(update)
            print("Dumping quests")
            dq.dumpQuests()
            hadError |= dq.isHadError()
            currentQuest = dq.currentId()
        except Exception as e:
            hadError = True
            e.printStackTrace()
            print(currentQuest + " quest.")
        endTime = int(time.time() * 1000)
        elapsedSeconds = (endTime - startTime) / 1000.0
        elapsedSecs = elapsedSeconds % 60
        elapsedMinutes = (int)(elapsedSeconds / 60.0)
        withErrors = ""
        if hadError:
            withErrors = " with errors"
        print("Finished" + withErrors + " in " + elapsedMinutes + " minutes " + elapsedSecs + " seconds")

