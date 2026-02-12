"""
DumpItems - Converted from Java source
Original: tools/wztosql/DumpItems.java
Package: tools.wztosql
"""

from pathlib import Path
from pymysql import Connection
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set
import os
import pymysql
import sys
import time

# Internal module imports
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class DumpItems:
    """
    Class DumpItems
    """

    def __init__(self, update: bool):
        self.item = None
        self.string = None
        self.character = None
        self.cashStringData = None
        self.consumeStringData = None
        self.eqpStringData = None
        self.etcStringData = None
        self.insStringData = None
        self.petStringData = None
        self.doneIds = None
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = None
        self.subCon = None
        self.subMain = None
        self.string = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz"))
        self.cashStringData = self.string.getData("Cash.img")
        self.consumeStringData = self.string.getData("Consume.img")
        self.eqpStringData = self.string.getData("Eqp.img")
        self.etcStringData = self.string.getData("Etc.img")
        self.insStringData = self.string.getData("Ins.img")
        self.petStringData = self.string.getData("Pet.img")
        self.doneIds = new LinkedHashSet<Integer>()
        self.hadError = False
        self.update = False
        self.id = 0
        self.con = DatabaseConnection.getConnection()
        self.subCon = []
        self.subMain = []
        self.update = update
        self.item = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Item.wz"))
        self.character = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Character.wz"))
        if self.item is None or self.string is None or self.character is None:
            self.hadError = True


    def isHadError(self) -> bool:
        return self.hadError

    def dumpItems(self) -> None:
        if not self.hadError:
            psa = self.con.prepareStatement("INSERT INTO wz_itemadddata(itemid, `key`, `subKey`, `value`) VALUES (?, ?, ?, ?)")
            psr = self.con.prepareStatement("INSERT INTO wz_itemrewarddata(itemid, item, prob, quantity, period, worldMsg, effect) VALUES (?, ?, ?, ?, ?, ?, ?)")
            ps = self.con.prepareStatement("INSERT INTO wz_itemdata(itemid, name, msg, `desc`, slotMax, price, wholePrice, stateChange, flags, karma, meso, monsterBook, itemMakeLevel, questId, scrollReqs, consumeItem, totalprob, incSkill, replaceId, replaceMsg, `create`, afterImage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            pse = self.con.prepareStatement("INSERT INTO wz_itemequipdata(itemid, itemLevel, `key`, `value`) VALUES (?, ?, ?, ?)")
            try:
                self.dumpItems(psa, psr, ps, pse)
            except Exception as e:
                print(self.id + " quest.")
                self.hadError = True
            finally:
                psr.executeBatch()
                psr.close()
                psa.executeBatch()
                psa.close()
                pse.executeBatch()
                pse.close()
                ps.executeBatch()
                ps.close()

    def delete(self, sql: str) -> None:
        # try-with-resources: final PreparedStatement ps = self.con.prepareStatement(sql)
        try:
            ps.executeUpdate()

    def doesExist(self, sql: str) -> bool:
        ret = None
        # try-with-resources: final PreparedStatement ps = self.con.prepareStatement(sql
        try:
        rs = ps.executeQuery())
            ret = rs.next()
        return ret

    def dumpItems_d_psa_psr_ps_pse_charz(self, d: Any, psa: Any, psr: Any, ps: Any, pse: Any, charz: bool) -> None:
        for topDir in d.getRoot().getSubdirectories():
            if not topDir.getName().lower() == "Special".lower() and not topDir.getName().lower() == "Hair".lower() and not topDir.getName().lower() == "Face".lower() and not topDir.getName().lower() == "Afterimage".lower():
                for ifile in topDir.getFiles():
                    iz = d.getData(topDir.getName() + "/" + ifile.getName())
                    if charz or topDir.getName().lower() == "Pet".lower():
                        self.dumpItem(psa, psr, ps, pse, iz)
                    else:
                        for itemData in iz:
                            self.dumpItem(psa, psr, ps, pse, itemData)

    def dumpItem(self, psa: Any, psr: Any, ps: Any, pse: Any, iz: Any) -> None:
        try:
            if iz.getName().endswith(".img"):
                self.id = int(iz.getName()[0:iz.getName(] - 4))
            else:
                self.id = int(iz.getName())
        except ValueError as nfe:
            return
        if (self.id in self.doneIds) or GameConstants.getInventoryType(self.id) == MapleInventoryType.UNDEFINED:
            return
        self.doneIds.add(self.id)
        if self.update and self.doesExist("SELECT * FROM wz_itemdata WHERE itemid = " + self.id):
            return
        ps.setInt(1, self.id)
        stringData = self.getStringData(self.id)
        if stringData is None:
            ps.setString(2, "")
            ps.setString(3, "")
            ps.setString(4, "")
        else:
            ps.setString(2, MapleDataTool.getString("name", stringData, ""))
            ps.setString(3, MapleDataTool.getString("msg", stringData, ""))
            ps.setString(4, MapleDataTool.getString("desc", stringData, ""))
        smEntry = iz.getChildByPath("info/slotMax")
        ret = None
        if smEntry is None:
            if GameConstants.getInventoryType(self.id) == MapleInventoryType.EQUIP:
                ret = 1
            else:
                ret = 100
        else:
            ret = MapleDataTool.getIntConvert(smEntry)
        ps.setInt(5, ret)
        pData = iz.getChildByPath("info/unitPrice")
        pEntry = None
        if pData is not None:
            try:
                pEntry = MapleDataTool.getDouble(pData)
            except Exception as e:
                pEntry = MapleDataTool.getIntConvert(pData)
        else:
            pData = iz.getChildByPath("info/price")
            if pData is None:
                pEntry = -1.0
            else:
                pEntry = MapleDataTool.getIntConvert(pData)
        if self.id == 2070019 or self.id == 2330007:
            pEntry = 1.0
        ps.setString(6, str(pEntry))
        ps.setInt(7, MapleDataTool.getIntConvert("info/price", iz, -1))
        ps.setInt(8, MapleDataTool.getIntConvert("info/stateChangeItem", iz, 0))
        flags = MapleDataTool.getIntConvert("info/bagType", iz, 0)
        if MapleDataTool.getIntConvert("info/notSale", iz, 0) > 0:
            flags |= 0x10
        if MapleDataTool.getIntConvert("info/expireOnLogout", iz, 0) > 0:
            flags |= 0x20
        if MapleDataTool.getIntConvert("info/pickUpBlock", iz, 0) > 0:
            flags |= 0x40
        if MapleDataTool.getIntConvert("info/only", iz, 0) > 0:
            flags |= 0x80
        if MapleDataTool.getIntConvert("info/accountSharable", iz, 0) > 0:
            flags |= 0x100
        if MapleDataTool.getIntConvert("info/quest", iz, 0) > 0:
            flags |= 0x200
        if self.id != 4310008 and MapleDataTool.getIntConvert("info/tradeBlock", iz, 0) > 0:
            flags |= 0x400
        if MapleDataTool.getIntConvert("info/accountShareTag", iz, 0) > 0:
            flags |= 0x800
        if MapleDataTool.getIntConvert("info/mobHP", iz, 0) > 0 and MapleDataTool.getIntConvert("info/mobHP", iz, 0) < 100:
            flags |= 0x1000
        ps.setInt(9, flags)
        ps.setInt(10, MapleDataTool.getIntConvert("info/tradeAvailable", iz, 0))
        ps.setInt(11, MapleDataTool.getIntConvert("info/meso", iz, 0))
        ps.setInt(12, MapleDataTool.getIntConvert("info/mob", iz, 0))
        ps.setInt(13, MapleDataTool.getIntConvert("info/lv", iz, 0))
        ps.setInt(14, MapleDataTool.getIntConvert("info/questId", iz, 0))
        totalprob = 0
        scrollReqs = ""
        consumeItem = ""
        incSkill = ""
        dat = iz.getChildByPath("req")
        if dat is not None:
            for req in dat:
                if scrollReqs > 0:
                    scrollReqs.append(",")
                scrollReqs.append(MapleDataTool.getIntConvert(req))
        dat = iz.getChildByPath("consumeItem")
        if dat is not None:
            for req in dat:
                if consumeItem > 0:
                    consumeItem.append(",")
                consumeItem.append(MapleDataTool.getIntConvert(req))
        ps.setString(15, scrollReqs)
        ps.setString(16, consumeItem)
        equipStats = new HashMap<Integer, Map<String, Integer>>()
        equipStats.put(-1, {})
        dat = iz.getChildByPath("mob")
        if dat is not None:
            for child in dat:
                equipStats.get(-1).put("mob" + MapleDataTool.getIntConvert("id", child, 0), MapleDataTool.getIntConvert("prob", child, 0))
        dat = iz.getChildByPath("info/level/case")
        if dat is not None:
            for info in dat:
                for data in info:
                    if data.getName() == 1 and data.getChildByPath("Skill") is not None:
                        for skil in data.getChildByPath("Skill"):
                            incSkillz = MapleDataTool.getIntConvert("id", skil, 0)
                            if incSkillz != 0:
                                if incSkill > 0:
                                    incSkill.append(",")
                                incSkill.append(incSkillz)
        dat = iz.getChildByPath("info/level/info")
        if dat is not None:
            for info in dat:
                if MapleDataTool.getIntConvert("exp", info, 0) == 0:
                    continue
                lv = int(info.getName())
                if equipStats.get(lv) is None:
                    equipStats.put(lv, {})
                for data2 in info:
                    if data2.getName() > 3:
                        equipStats.get(lv).put(data2.getName()[3:], MapleDataTool.getIntConvert(data2))
        dat = iz.getChildByPath("info")
        if dat is not None:
            ps.setString(22, MapleDataTool.getString("afterImage", dat, ""))
            rett = equipStats.get(-1)
            for data3 in dat.getChildren():
                if data3.getName().startswith("inc"):
                    gg = MapleDataTool.getIntConvert(data3)
                    if gg == 0:
                        continue
                    rett.put(data3.getName()[3:], gg)
            for stat in GameConstants.stats:
                d = dat.getChildByPath(stat)
                if stat == ("canLevel"):
                    if dat.getChildByPath("level") is not None:
                        rett.put(stat, 1)
                elif d is not None:
                    if stat == ("skill"):
                        for i in range(d.getChildren()):
                            rett.put("skillid" + i, MapleDataTool.getIntConvert(Integer.toString(i), d, 0))
                    else:
                        dd = MapleDataTool.getIntConvert(d)
                        if dd != 0:
                            rett.put(stat, dd)
        else:
            ps.setString(22, "")
        pse.setInt(1, self.id)
        for (final Map.Entry<Integer, Map<String, Integer>> stats : equipStats.items())
            pse.setInt(2, stats.getKey())
            for (final Map.Entry<String, Integer> stat2 : stats.getValue().items())
                pse.setString(3, stat2.getKey())
                pse.setInt(4, stat2.getValue())
                pse.addBatch()
        dat = iz.getChildByPath("info/addition")
        if dat is not None:
            psa.setInt(1, self.id)
            for d2 in dat.getChildren():
                incs = None
                name = d2.getName()
                # switch (name):
                    # case "statinc":
                    # case "critical":
                    # case "skill":
                    # case "mobdie":
                    # case "hpmpchange":
                    # case "elemboost":
                    # case "elemBoost":
                    # case "mobcategory":
                    # case "boss":
                        for subKey in d2.getChildren():
                            if subKey.getName() == ("con"):
                                for conK in subKey.getChildren():
                                    name2 = conK.getName()
                                    # switch (name2):
                                        # case "job":
                                            sbbb = ""
                                            if conK.getData() is None:
                                                for ids in conK.getChildren():
                                                    sbbb.append(ids.getData())
                                                    sbbb.append(",")
                                                sbbb.deleteCharAt(sbbb - 1)
                                            else:
                                                sbbb.append(conK.getData())
                                            psa.setString(2, d2.getName() == ("elemBoost") ? "elemboost" : d2.getName())
                                            psa.setString(3, "con:job")
                                            psa.setString(4, sbbb)
                                            psa.addBatch()
                                            continue
                                        # case "weekDay":
                                            continue
                                        # default:
                                            psa.setString(2, d2.getName() == ("elemBoost") ? "elemboost" : d2.getName())
                                            psa.setString(3, "con:" + conK.getName())
                                            psa.setString(4, conK.getData())
                                            psa.addBatch()
                                            continue
                            else:
                                psa.setString(2, d2.getName() == ("elemBoost") ? "elemboost" : d2.getName())
                                psa.setString(3, subKey.getName())
                                psa.setString(4, subKey.getData())
                                psa.addBatch()
                        continue
                    # default:
                        print("UNKNOWN EQ ADDITION : " + d2.getName() + " from " + self.id)
                        continue
        dat = iz.getChildByPath("reward")
        if dat is not None:
            psr.setInt(1, self.id)
            for reward in dat:
                psr.setInt(2, MapleDataTool.getIntConvert("item", reward, 0))
                psr.setInt(3, MapleDataTool.getIntConvert("prob", reward, 0))
                psr.setInt(4, MapleDataTool.getIntConvert("count", reward, 0))
                psr.setInt(5, MapleDataTool.getIntConvert("period", reward, 0))
                psr.setString(6, MapleDataTool.getString("worldMsg", reward, ""))
                psr.setString(7, MapleDataTool.getString("Effect", reward, ""))
                psr.addBatch()
                totalprob += MapleDataTool.getIntConvert("prob", reward, 0)
        ps.setInt(17, totalprob)
        ps.setString(18, incSkill)
        dat = iz.getChildByPath("replace")
        if dat is not None:
            ps.setInt(19, MapleDataTool.getInt("itemid", dat, 0))
            ps.setString(20, MapleDataTool.getString("msg", dat, ""))
        else:
            ps.setInt(19, 0)
            ps.setString(20, "")
        ps.setInt(21, MapleDataTool.getInt("info/create", iz, 0))
        ps.addBatch()

    def dumpItems_psa_psr_ps_pse(self, psa: Any, psr: Any, ps: Any, pse: Any) -> None:
        if not self.update:
            self.delete("DELETE FROM wz_itemdata")
            self.delete("DELETE FROM wz_itemequipdata")
            self.delete("DELETE FROM wz_itemadddata")
            self.delete("DELETE FROM wz_itemrewarddata")
            print("Deleted wz_itemdata successfully.")
        print("Adding into wz_itemdata.....")
        self.dumpItems(self.item, psa, psr, ps, pse, False)
        self.dumpItems(self.character, psa, psr, ps, pse, True)
        print("Done wz_itemdata...")
        if not self.subMain == 0:
            print(self.subMain)
        if not self.subCon == 0:
            print(self.subCon)

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
            dq = DumpItems(update)
            print("Dumping Items")
            dq.dumpItems()
            hadError |= dq.isHadError()
            currentQuest = dq.currentId()
        except Exception as e:
            hadError = True
            print(currentQuest + " quest.")
        endTime = int(time.time() * 1000)
        elapsedSeconds = (endTime - startTime) / 1000.0
        elapsedSecs = elapsedSeconds % 60
        elapsedMinutes = (int)(elapsedSeconds / 60.0)
        withErrors = ""
        if hadError:
            withErrors = " with errors"
        print("Finished" + withErrors + " in " + elapsedMinutes + " minutes " + elapsedSecs + " seconds")

    def getStringData(self, itemId: int) -> Any:
        cat = None
        data = None
        if itemId >= 5010000:
            data = self.cashStringData
        elif itemId >= 2000000 and itemId < 3000000:
            data = self.consumeStringData
        elif (itemId >= 1132000 and itemId < 1183000) or (itemId >= 1010000 and itemId < 1040000) or (itemId >= 1122000 and itemId < 1123000):
            data = self.eqpStringData
            cat = "Eqp/Accessory"
        elif itemId >= 1172000 and itemId < 1180000:
            data = self.eqpStringData
            cat = "Eqp/MonsterBook"
        elif itemId >= 1662000 and itemId < 1680000:
            data = self.eqpStringData
            cat = "Eqp/Android"
        elif itemId >= 1000000 and itemId < 1010000:
            data = self.eqpStringData
            cat = "Eqp/Cap"
        elif itemId >= 1102000 and itemId < 1103000:
            data = self.eqpStringData
            cat = "Eqp/Cape"
        elif itemId >= 1040000 and itemId < 1050000:
            data = self.eqpStringData
            cat = "Eqp/Coat"
        elif itemId >= 20000 and itemId < 22000:
            data = self.eqpStringData
            cat = "Eqp/Face"
        elif itemId >= 1080000 and itemId < 1090000:
            data = self.eqpStringData
            cat = "Eqp/Glove"
        elif itemId >= 30000 and itemId < 35000:
            data = self.eqpStringData
            cat = "Eqp/Hair"
        elif itemId >= 1050000 and itemId < 1060000:
            data = self.eqpStringData
            cat = "Eqp/Longcoat"
        elif itemId >= 1060000 and itemId < 1070000:
            data = self.eqpStringData
            cat = "Eqp/Pants"
        elif itemId >= 1610000 and itemId < 1660000:
            data = self.eqpStringData
            cat = "Eqp/Mechanic"
        elif itemId >= 1802000 and itemId < 1820000:
            data = self.eqpStringData
            cat = "Eqp/PetEquip"
        elif itemId >= 1920000 and itemId < 2000000:
            data = self.eqpStringData
            cat = "Eqp/Dragon"
        elif itemId >= 1112000 and itemId < 1120000:
            data = self.eqpStringData
            cat = "Eqp/Ring"
        elif itemId >= 1092000 and itemId < 1100000:
            data = self.eqpStringData
            cat = "Eqp/Shield"
        elif itemId >= 1070000 and itemId < 1080000:
            data = self.eqpStringData
            cat = "Eqp/Shoes"
        elif itemId >= 1900000 and itemId < 1920000:
            data = self.eqpStringData
            cat = "Eqp/Taming"
        elif itemId >= 1200000 and itemId < 1210000:
            data = self.eqpStringData
            cat = "Eqp/Totem"
        elif itemId >= 1210000 and itemId < 1800000:
            data = self.eqpStringData
            cat = "Eqp/Weapon"
        elif itemId >= 4000000 and itemId < 5000000:
            data = self.etcStringData
            cat = "Etc"
        elif itemId >= 3000000 and itemId < 4000000:
            data = self.insStringData
        else:
            if itemId < 5000000 or itemId >= 5010000:
                return None
            data = self.petStringData
        if cat is None:
            return data.getChildByPath(str(itemId))
        return data.getChildByPath(cat + "/" + itemId)

