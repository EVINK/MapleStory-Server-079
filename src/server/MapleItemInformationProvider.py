"""
MapleItemInformationProvider - Converted from Java source
Original: server/MapleItemInformationProvider.java
Package: server
"""

from pathlib import Path
from random import Random
from typing import Dict
from typing import List
from typing import Optional, Any
import math
import os
import random
import sys

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class MapleItemInformationProvider:
    """
    Class MapleItemInformationProvider
    """

    def __init__(self):
        self.onEquipUntradableCache = {}
        self.etcData = None
        self.itemData = None
        self.equipData = None
        self.stringData = None
        self.cashStringData = None
        self.consumeStringData = None
        self.eqpStringData = None
        self.etcStringData = None
        self.insStringData = None
        self.petStringData = None
        self.scrollReqCache = {}
        self.slotMaxCache = {}
        self.getExpCache = {}
        self.faceList = {}
        self.hairList = {}
        self.chrData = None
        self.potentialCache = {}
        self.itemEffects = {}
        self.equipStatsCache = {}
        self.itemMakeStatsCache = {}
        self.itemMakeLevel = {}
        self.equipCache = {}
        self.priceCache = {}
        self.wholePriceCache = {}
        self.projectileWatkCache = {}
        self.monsterBookID = {}
        self.nameCache = {}
        self.descCache = {}
        self.msgCache = {}
        self.SkillStatsCache = {}
        self.consumeOnPickupCache = {}
        self.dropRestrictionCache = {}
        self.accCache = {}
        self.pickupRestrictionCache = {}
        self.stateChangeCache = {}
        self.mesoCache = {}
        self.notSaleCache = {}
        self.karmaEnabledCache = {}
        self.karmaCache = {}
        self.onEquipUntradableCache = {}
        self.etcData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
        self.itemData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Item.wz"))
        self.equipData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Character.wz"))
        self.stringData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz"))
        self.cashStringData = self.stringData.getData("Cash.img")
        self.consumeStringData = self.stringData.getData("Consume.img")
        self.eqpStringData = self.stringData.getData("Eqp.img")
        self.etcStringData = self.stringData.getData("Etc.img")
        self.insStringData = self.stringData.getData("Ins.img")
        self.petStringData = self.stringData.getData("Pet.img")
        self.scrollReqCache = new HashMap<Integer, List<Integer>>()
        self.slotMaxCache = {}
        self.getExpCache = {}
        self.potentialCache = new HashMap<Integer, List<StructPotentialItem>>()
        self.itemEffects = {}
        self.equipStatsCache = new HashMap<Integer, Map<String, Integer>>()
        self.itemMakeStatsCache = new HashMap<Integer, Map<String, Byte>>()
        self.itemMakeLevel = {}
        self.equipCache = {}
        self.priceCache = {}
        self.wholePriceCache = {}
        self.projectileWatkCache = {}
        self.monsterBookID = {}
        self.nameCache = {}
        self.descCache = {}
        self.msgCache = {}
        self.SkillStatsCache = new HashMap<Integer, Map<String, Integer>>()
        self.consumeOnPickupCache = {}
        self.dropRestrictionCache = {}
        self.accCache = {}
        self.pickupRestrictionCache = {}
        self.stateChangeCache = {}
        self.mesoCache = {}
        self.notSaleCache = {}
        self.karmaEnabledCache = {}
        self.karmaCache = {}
        self.isQuestItemCache = {}
        self.blockPickupCache = {}
        self.petsCanConsumeCache = new HashMap<Integer, List<Integer>>()
        self.logoutExpireCache = {}
        self.summonMobCache = new HashMap<Integer, List<Pair<Integer, Integer>>>()
        self.itemNameCache = new ArrayList<Pair<Integer, String>>()
        self.equipIncsCache = new HashMap<Integer, Map<Integer, Map<String, Integer>>>()
        self.equipSkillsCache = new HashMap<Integer, Map<Integer, List<Integer>>>()
        self.RewardItem = new HashMap<Integer, Pair<Integer, List<StructRewardItem>>>()
        self.setItems = {}
        self.questItems = new HashMap<Integer, Pair<Integer, List<Integer>>>()
        self.inventoryTypeCache = {}

    # Static initializer
    # instance = MapleItemInformationProvider()
    # rand = Random()
    # whiteItemList = {}  # 物品上限白名单
    # whiteItemList.put(4001126, Short.valueOf("30000"))  # 枫叶
    # whiteItemList.put(46354, Short.valueOf("234"))  # 心跳箱子


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self) -> None:
        if self.setItems != 0 or self.potentialCache != 0:
            return
        self.getAllItems()

    def getPotentialInfo(self, potId: int) -> list:
        return self.potentialCache.get(potId)

    def getAllPotentialInfo(self) -> dict:
        return self.potentialCache

    def getAllItems(self) -> list:
        if self.itemNameCache != 0:
            return self.itemNameCache
        itemPairs = new ArrayList<Pair<Integer, String>>()
        itemsData = self.stringData.getData("Cash.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Consume.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Eqp.img").getChildByPath("Eqp")
        for eqpType in itemsData.getChildren():
            for itemFolder2 in eqpType.getChildren():
                itemPairs.add(new Pair<Integer, String>(int(itemFolder2.getName()), MapleDataTool.getString("name", itemFolder2, "NO-NAME")))
        itemsData = self.stringData.getData("Etc.img").getChildByPath("Etc")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Ins.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Pet.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        return itemPairs

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

    def getItemData(self, itemId: int) -> Any:
        ret = None
        idStr = "0" + str(itemId)
        root = self.itemData.getRoot()
        for topDir in root.getSubdirectories():
            for iFile in topDir.getFiles():
                if iFile.getName() == (idStr[0:4] + ".img"):
                    ret = self.itemData.getData(topDir.getName() + "/" + iFile.getName())
                    if ret is None:
                        return None
                    ret = ret.getChildByPath(idStr)
                    return ret
                else:
                    if iFile.getName() == (idStr[1:] + ".img"):
                        return self.itemData.getData(topDir.getName() + "/" + iFile.getName())
                    continue
        root = self.equipData.getRoot()
        for topDir in root.getSubdirectories():
            for iFile in topDir.getFiles():
                if iFile.getName() == (idStr + ".img"):
                    return self.equipData.getData(topDir.getName() + "/" + iFile.getName())
        return ret

    def getSlotMax(self, c: Any, itemId: int) -> int:
        if (itemId in self.slotMaxCache):
            return self.slotMaxCache.get(itemId)
        ret = 0
        item = self.getItemData(itemId)
        if item is not None:
            tmp = whiteItemList.get(itemId)
            if None == tmp:
                smEntry = item.getChildByPath("info/slotMax")
                if smEntry is None:
                    if GameConstants.getInventoryType(itemId) == MapleInventoryType.EQUIP:
                        ret = 1
                    else:
                        ret = 100
                else:
                    ret = MapleDataTool.getInt(smEntry)
            else:
                ret = tmp
        self.slotMaxCache.put(itemId, ret)
        return ret

    def getWholePrice(self, itemId: int) -> int:
        if (itemId in self.wholePriceCache):
            return self.wholePriceCache.get(itemId)
        item = self.getItemData(itemId)
        if item is None:
            return -1
        pEntry = 0
        pData = item.getChildByPath("info/price")
        if pData is None:
            return -1
        pEntry = MapleDataTool.getInt(pData)
        self.wholePriceCache.put(itemId, pEntry)
        return pEntry

    def getPrice(self, itemId: int) -> float:
        if (itemId in self.priceCache):
            return self.priceCache.get(itemId)
        item = self.getItemData(itemId)
        if item is None:
            return -1.0
        pEntry = 0.0
        pData = item.getChildByPath("info/unitPrice")
        if pData is not None:
            try:
                pEntry = MapleDataTool.getDouble(pData)
            except Exception as e:
                pEntry = MapleDataTool.getIntConvert(pData)
        else:
            pData = item.getChildByPath("info/price")
            if pData is None:
                return -1.0
            pEntry = MapleDataTool.getIntConvert(pData)
        if itemId == 2070019 or itemId == 2330007:
            pEntry = 1.0
        self.priceCache.put(itemId, pEntry)
        return pEntry

    def getItemMakeStats(self, itemId: int) -> dict:
        if (itemId in self.itemMakeStatsCache):
            return self.itemMakeStatsCache.get(itemId)
        if itemId / 10000 != 425:
            return None
        ret = {}
        item = self.getItemData(itemId)
        if item is None:
            return None
        info = item.getChildByPath("info")
        if info is None:
            return None
        ret.put("incPAD", MapleDataTool.getInt("incPAD", info, 0))
        ret.put("incMAD", MapleDataTool.getInt("incMAD", info, 0))
        ret.put("incACC", MapleDataTool.getInt("incACC", info, 0))
        ret.put("incEVA", MapleDataTool.getInt("incEVA", info, 0))
        ret.put("incSpeed", MapleDataTool.getInt("incSpeed", info, 0))
        ret.put("incJump", MapleDataTool.getInt("incJump", info, 0))
        ret.put("incMaxHP", MapleDataTool.getInt("incMaxHP", info, 0))
        ret.put("incMaxMP", MapleDataTool.getInt("incMaxMP", info, 0))
        ret.put("incSTR", MapleDataTool.getInt("incSTR", info, 0))
        ret.put("incINT", MapleDataTool.getInt("incINT", info, 0))
        ret.put("incLUK", MapleDataTool.getInt("incLUK", info, 0))
        ret.put("incDEX", MapleDataTool.getInt("incDEX", info, 0))
        ret.put("randOption", MapleDataTool.getInt("randOption", info, 0))
        ret.put("randStat", MapleDataTool.getInt("randStat", info, 0))
        self.itemMakeStatsCache.put(itemId, ret)
        return ret

    def rand(self, min: int, max: int) -> int:
        return abs(Randomizer.rand(min, max))

    def levelUpEquip(self, equip: Any, sta: dict) -> Any:
        nEquip = equip.copy()
        try:
            for (final Map.Entry<String, Integer> stat : sta.items())
                s = stat.getKey()
                # switch (s):
                    # case "STRMin":
                        nEquip.setStr((short) (nEquip.getStr() + self.rand(stat.getValue(), sta.get("STRMax"))))
                        continue
                    # case "DEXMin":
                        nEquip.setDex((short) (nEquip.getDex() + self.rand(stat.getValue(), sta.get("DEXMax"))))
                        continue
                    # case "INTMin":
                        nEquip.setInt((short) (nEquip.getInt() + self.rand(stat.getValue(), sta.get("INTMax"))))
                        continue
                    # case "LUKMin":
                        nEquip.setLuk((short) (nEquip.getLuk() + self.rand(stat.getValue(), sta.get("LUKMax"))))
                        continue
                    # case "PADMin":
                        nEquip.setWatk((short) (nEquip.getWatk() + self.rand(stat.getValue(), sta.get("PADMax"))))
                        continue
                    # case "PDDMin":
                        nEquip.setWdef((short) (nEquip.getWdef() + self.rand(stat.getValue(), sta.get("PDDMax"))))
                        continue
                    # case "MADMin":
                        nEquip.setMatk((short) (nEquip.getMatk() + self.rand(stat.getValue(), sta.get("MADMax"))))
                        continue
                    # case "MDDMin":
                        nEquip.setMdef((short) (nEquip.getMdef() + self.rand(stat.getValue(), sta.get("MDDMax"))))
                        continue
                    # case "ACCMin":
                        nEquip.setAcc((short) (nEquip.getAcc() + self.rand(stat.getValue(), sta.get("ACCMax"))))
                        continue
                    # case "EVAMin":
                        nEquip.setAvoid((short) (nEquip.getAvoid() + self.rand(stat.getValue(), sta.get("EVAMax"))))
                        continue
                    # case "SpeedMin":
                        nEquip.setSpeed((short) (nEquip.getSpeed() + self.rand(stat.getValue(), sta.get("SpeedMax"))))
                        continue
                    # case "JumpMin":
                        nEquip.setJump((short) (nEquip.getJump() + self.rand(stat.getValue(), sta.get("JumpMax"))))
                        continue
                    # case "MHPMin":
                        nEquip.setHp((short) (nEquip.getHp() + self.rand(stat.getValue(), sta.get("MHPMax"))))
                        continue
                    # case "MMPMin":
                        nEquip.setMp((short) (nEquip.getMp() + self.rand(stat.getValue(), sta.get("MMPMax"))))
                        continue
                    # case "MaxHPMin":
                        nEquip.setHp((short) (nEquip.getHp() + self.rand(stat.getValue(), sta.get("MaxHPMax"))))
                        continue
                    # case "MaxMPMin":
                        nEquip.setMp((short) (nEquip.getMp() + self.rand(stat.getValue(), sta.get("MaxMPMax"))))
                        continue
        except NullPointerException as e:
            e.printStackTrace()
        return nEquip

    def getEquipIncrements(self, itemId: int) -> dict:
        if (itemId in self.equipIncsCache):
            return self.equipIncsCache.get(itemId)
        ret = new LinkedHashMap<Integer, Map<String, Integer>>()
        item = self.getItemData(itemId)
        if item is None:
            return None
        info = item.getChildByPath("info/level/info")
        if info is None:
            return None
        for dat in info.getChildren():
            incs = {}
            for data in dat.getChildren():
                if data.getName() > 3:
                    incs.put(data.getName()[3:], MapleDataTool.getIntConvert(data.getName(), dat, 0))
            ret.put(int(dat.getName()), incs)
        self.equipIncsCache.put(itemId, ret)
        return ret

    def getEquipSkills(self, itemId: int) -> dict:
        if (itemId in self.equipSkillsCache):
            return self.equipSkillsCache.get(itemId)
        ret = new LinkedHashMap<Integer, List<Integer>>()
        item = self.getItemData(itemId)
        if item is None:
            return None
        info = item.getChildByPath("info/level/case")
        if info is None:
            return None
        for dat in info.getChildren():
            for data in dat.getChildren():
                if data.getName() == 1:
                    adds = []
                    for skil in data.getChildByPath("Skill").getChildren():
                        adds.add(MapleDataTool.getIntConvert("id", skil, 0))
                    ret.put(int(data.getName()), adds)
        self.equipSkillsCache.put(itemId, ret)
        return ret

    def getEquipStats(self, itemId: int) -> dict:
        if (itemId in self.equipStatsCache):
            return self.equipStatsCache.get(itemId)
        ret = {}
        item = self.getItemData(itemId)
        if item is None:
            return None
        info = item.getChildByPath("info")
        if info is None:
            return None
        for data in info.getChildren():
            if data.getName().startswith("inc"):
                ret.put(data.getName()[3:], MapleDataTool.getIntConvert(data))
        ret.put("tuc", MapleDataTool.getInt("tuc", info, 0))
        ret.put("reqLevel", MapleDataTool.getInt("reqLevel", info, 0))
        ret.put("reqJob", MapleDataTool.getInt("reqJob", info, 0))
        ret.put("reqSTR", MapleDataTool.getInt("reqSTR", info, 0))
        ret.put("reqDEX", MapleDataTool.getInt("reqDEX", info, 0))
        ret.put("reqINT", MapleDataTool.getInt("reqINT", info, 0))
        ret.put("reqLUK", MapleDataTool.getInt("reqLUK", info, 0))
        ret.put("reqPOP", MapleDataTool.getInt("reqPOP", info, 0))
        ret.put("cash", MapleDataTool.getInt("cash", info, 0))
        ret.put("canLevel", (info.getChildByPath("level") is not None) ? 1 : 0)
        ret.put("cursed", MapleDataTool.getInt("cursed", info, 0))
        ret.put("success", MapleDataTool.getInt("success", info, 0))
        ret.put("setItemID", MapleDataTool.getInt("setItemID", info, 0))
        ret.put("equipTradeBlock", MapleDataTool.getInt("equipTradeBlock", info, 0))
        ret.put("durability", MapleDataTool.getInt("durability", info, -1))
        if GameConstants.isMagicWeapon(itemId):
            ret.put("elemDefault", MapleDataTool.getInt("elemDefault", info, 100))
            ret.put("incRMAS", MapleDataTool.getInt("incRMAS", info, 100))
            ret.put("incRMAF", MapleDataTool.getInt("incRMAF", info, 100))
            ret.put("incRMAL", MapleDataTool.getInt("incRMAL", info, 100))
            ret.put("incRMAI", MapleDataTool.getInt("incRMAI", info, 100))
        self.equipStatsCache.put(itemId, ret)
        return ret

    def canEquip(self, stats: dict, itemid: int, level: int, job: int, fame: int, str: int, dex: int, luk: int, int_: int, supremacy: int) -> bool:
        if level + supremacy >= stats.get("reqLevel") and str >= stats.get("reqSTR") and dex >= stats.get("reqDEX") and luk >= stats.get("reqLUK") and int_ >= stats.get("reqINT"):
            fameReq = stats.get("reqPOP")
            return fameReq == 0 or fame >= fameReq
        return False

    def getReqLevel(self, itemId: int) -> int:
        if self.getEquipStats(itemId) is None:
            return 0
        return self.getEquipStats(itemId).get("reqLevel")

    def isCashItem(self, itemId: int) -> bool:
        return self.getEquipStats(itemId) is not None and self.getEquipStats(itemId).get("cash") == 1

    def getSlots(self, itemId: int) -> int:
        if self.getEquipStats(itemId) is None:
            return 0
        return self.getEquipStats(itemId).get("tuc")

    def getSetItemID(self, itemId: int) -> int:
        if self.getEquipStats(itemId) is None:
            return 0
        return self.getEquipStats(itemId).get("setItemID")

    def getSetItem(self, setItemId: int) -> Any:
        return self.setItems.get(setItemId)

    def getScrollReqs(self, itemId: int) -> list:
        if (itemId in self.scrollReqCache):
            return self.scrollReqCache.get(itemId)
        ret = []
        data = self.getItemData(itemId).getChildByPath("req")
        if data is None:
            return ret
        for req in data.getChildren():
            ret.add(MapleDataTool.getInt(req))
        self.scrollReqCache.put(itemId, ret)
        return ret

    def scrollEquipWithId(self, equip: Any, scrollId: Any, ws: bool, chr: Any, vegas: int, checkIfGM: bool) -> Any:
        if equip.getType() == 1:
            nEquip = equip
            stats = self.getEquipStats(scrollId.getItemId())
            eqstats = self.getEquipStats(equip.getItemId())
            succ = GameConstants.isTablet(scrollId.getItemId()) ? GameConstants.getSuccessTablet(scrollId.getItemId(), nEquip.getLevel()) : ((GameConstants.isEquipScroll(scrollId.getItemId()) or GameConstants.isPotentialScroll(scrollId.getItemId())) ? 0 : stats.get("success"))
            curse = GameConstants.isTablet(scrollId.getItemId()) ? GameConstants.getCurseTablet(scrollId.getItemId(), nEquip.getLevel()) : ((GameConstants.isEquipScroll(scrollId.getItemId()) or GameConstants.isPotentialScroll(scrollId.getItemId())) ? 0 : stats.get("cursed"))
            success = succ + ((vegas == 5610000 and succ == 10) ? 20 : ((vegas == 5610001 and succ == 60) ? 30 : 0))
            if GameConstants.isPotentialScroll(scrollId.getItemId()) or GameConstants.isEquipScroll(scrollId.getItemId()) or Randomizer.nextInt(100) <= success or checkIfGM:
                # switch (scrollId.getItemId()):
                    # case 2049000:
                    # case 2049001:
                    # case 2049002:
                    # case 2049003:
                    # case 2049004:
                    # case 2049005:
                        if nEquip.getLevel() + nEquip.getUpgradeSlots() < eqstats.get("tuc"):
                            nEquip.setUpgradeSlots((byte) (nEquip.getUpgradeSlots() + 1))
                            break
                        break
                    # case 2049006:
                    # case 2049007:
                    # case 2049008:
                        if nEquip.getLevel() + nEquip.getUpgradeSlots() < eqstats.get("tuc"):
                            nEquip.setUpgradeSlots((byte) (nEquip.getUpgradeSlots() + 2))
                            break
                        break
                    # case 2040727:
                        flag = nEquip.getFlag()
                        flag |= ItemFlag.SPIKES.getValue()
                        nEquip.setFlag(flag)
                        break
                    # case 2041058:
                        flag = nEquip.getFlag()
                        flag |= ItemFlag.COLD.getValue()
                        nEquip.setFlag(flag)
                        break
                    # default:
                        if GameConstants.isChaosScroll(scrollId.getItemId()):
                            z = GameConstants.getChaosNumber(scrollId.getItemId())
                            if scrollId.getItemId() == 2049122 or scrollId.getItemId() == 2049124:
                                if nEquip.getStr() > 0:
                                    nEquip.setStr((short) (nEquip.getStr() + Randomizer.nextInt(z) + 1))
                                if nEquip.getDex() > 0:
                                    nEquip.setDex((short) (nEquip.getDex() + Randomizer.nextInt(z) + 1))
                                if nEquip.getInt() > 0:
                                    nEquip.setInt((short) (nEquip.getInt() + Randomizer.nextInt(z) + 1))
                                if nEquip.getLuk() > 0:
                                    nEquip.setLuk((short) (nEquip.getLuk() + Randomizer.nextInt(z) + 1))
                                if nEquip.getWatk() > 0:
                                    nEquip.setWatk((short) (nEquip.getWatk() + Randomizer.nextInt(z) + 1))
                                if nEquip.getWdef() > 0:
                                    nEquip.setWdef((short) (nEquip.getWdef() + Randomizer.nextInt(z) + 1))
                                if nEquip.getMatk() > 0:
                                    nEquip.setMatk((short) (nEquip.getMatk() + Randomizer.nextInt(z) + 1))
                                if nEquip.getMdef() > 0:
                                    nEquip.setMdef((short) (nEquip.getMdef() + Randomizer.nextInt(z) + 1))
                                if nEquip.getAcc() > 0:
                                    nEquip.setAcc((short) (nEquip.getAcc() + Randomizer.nextInt(z) + 1))
                                if nEquip.getAvoid() > 0:
                                    nEquip.setAvoid((short) (nEquip.getAvoid() + Randomizer.nextInt(z) + 1))
                                if nEquip.getSpeed() > 0:
                                    nEquip.setSpeed((short) (nEquip.getSpeed() + Randomizer.nextInt(z) + 1))
                                if nEquip.getJump() > 0:
                                    nEquip.setJump((short) (nEquip.getJump() + Randomizer.nextInt(z) + 1))
                                if nEquip.getHp() > 0:
                                    nEquip.setHp((short) (nEquip.getHp() + Randomizer.nextInt(z) + 1))
                                if nEquip.getMp() > 0:
                                    nEquip.setMp((short) (nEquip.getMp() + Randomizer.nextInt(z) + 1))
                                    break
                                break
                            else:
                                if nEquip.getStr() > 0:
                                    nEquip.setStr((short) (nEquip.getStr() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getDex() > 0:
                                    nEquip.setDex((short) (nEquip.getDex() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getInt() > 0:
                                    nEquip.setInt((short) (nEquip.getInt() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getLuk() > 0:
                                    nEquip.setLuk((short) (nEquip.getLuk() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getWatk() > 0:
                                    nEquip.setWatk((short) (nEquip.getWatk() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getWdef() > 0:
                                    nEquip.setWdef((short) (nEquip.getWdef() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getMatk() > 0:
                                    nEquip.setMatk((short) (nEquip.getMatk() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getMdef() > 0:
                                    nEquip.setMdef((short) (nEquip.getMdef() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getAcc() > 0:
                                    nEquip.setAcc((short) (nEquip.getAcc() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getAvoid() > 0:
                                    nEquip.setAvoid((short) (nEquip.getAvoid() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getSpeed() > 0:
                                    nEquip.setSpeed((short) (nEquip.getSpeed() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getJump() > 0:
                                    nEquip.setJump((short) (nEquip.getJump() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getHp() > 0:
                                    nEquip.setHp((short) (nEquip.getHp() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                if nEquip.getMp() > 0:
                                    nEquip.setMp((short) (nEquip.getMp() + Randomizer.nextInt(z) * (Randomizer.nextBoolean() ? 1 : -1)))
                                    break
                                break
                        else:
                            if GameConstants.isEquipScroll(scrollId.getItemId()):
                                break
                            if GameConstants.isPotentialScroll(scrollId.getItemId()):
                                break
                            for (final Map.Entry<String, Integer> stat : stats.items())
                                s = None
                                key = s = stat.getKey()
                                # switch (s):
                                    # case "STR":
                                        nEquip.setStr((short) (nEquip.getStr() + stat.getValue()))
                                        continue
                                    # case "DEX":
                                        nEquip.setDex((short) (nEquip.getDex() + stat.getValue()))
                                        continue
                                    # case "INT":
                                        nEquip.setInt((short) (nEquip.getInt() + stat.getValue()))
                                        continue
                                    # case "LUK":
                                        nEquip.setLuk((short) (nEquip.getLuk() + stat.getValue()))
                                        continue
                                    # case "PAD":
                                        nEquip.setWatk((short) (nEquip.getWatk() + stat.getValue()))
                                        continue
                                    # case "PDD":
                                        nEquip.setWdef((short) (nEquip.getWdef() + stat.getValue()))
                                        continue
                                    # case "MAD":
                                        nEquip.setMatk((short) (nEquip.getMatk() + stat.getValue()))
                                        continue
                                    # case "MDD":
                                        nEquip.setMdef((short) (nEquip.getMdef() + stat.getValue()))
                                        continue
                                    # case "ACC":
                                        nEquip.setAcc((short) (nEquip.getAcc() + stat.getValue()))
                                        continue
                                    # case "EVA":
                                        nEquip.setAvoid((short) (nEquip.getAvoid() + stat.getValue()))
                                        continue
                                    # case "Speed":
                                        nEquip.setSpeed((short) (nEquip.getSpeed() + stat.getValue()))
                                        continue
                                    # case "Jump":
                                        nEquip.setJump((short) (nEquip.getJump() + stat.getValue()))
                                        continue
                                    # case "MHP":
                                        nEquip.setHp((short) (nEquip.getHp() + stat.getValue()))
                                        continue
                                    # case "MMP":
                                        nEquip.setMp((short) (nEquip.getMp() + stat.getValue()))
                                        continue
                                    # case "MHPr":
                                        nEquip.setHpR((short) (nEquip.getHpR() + stat.getValue()))
                                        continue
                                    # case "MMPr":
                                        nEquip.setMpR((short) (nEquip.getMpR() + stat.getValue()))
                                        continue
                            break
                if not GameConstants.isCleanSlate(scrollId.getItemId()) and not GameConstants.isSpecialScroll(scrollId.getItemId()) and not GameConstants.isEquipScroll(scrollId.getItemId()) and not GameConstants.isPotentialScroll(scrollId.getItemId()):
                    nEquip.setUpgradeSlots((byte) (nEquip.getUpgradeSlots() - 1))
                    nEquip.setLevel((byte) (nEquip.getLevel() + 1))
            else:
                if not ws and not GameConstants.isCleanSlate(scrollId.getItemId()) and not GameConstants.isSpecialScroll(scrollId.getItemId()) and not GameConstants.isEquipScroll(scrollId.getItemId()) and not GameConstants.isPotentialScroll(scrollId.getItemId()):
                    nEquip.setUpgradeSlots((byte) (nEquip.getUpgradeSlots() - 1))
                if Randomizer.nextInt(99) < curse:
                    return None
        return equip

    def getEquipById(self, equipId: int) -> Any:
        return self.getEquipById(equipId, -1)

    def getEquipById_equipId_ringId(self, equipId: int, ringId: int) -> Any:
        nEquip = Equip(equipId, 0, ringId, 0)
        nEquip.setQuantity(1)
        stats = self.getEquipStats(equipId)
        if stats is not None:
            for (final Map.Entry<String, Integer> stat : stats.items())
                s = None
                key = s = stat.getKey()
                # switch (s):
                    # case "STR":
                        nEquip.setStr((short) stat.getValue())
                        continue
                    # case "DEX":
                        nEquip.setDex((short) stat.getValue())
                        continue
                    # case "INT":
                        nEquip.setInt((short) stat.getValue())
                        continue
                    # case "LUK":
                        nEquip.setLuk((short) stat.getValue())
                        continue
                    # case "PAD":
                        nEquip.setWatk((short) stat.getValue())
                        continue
                    # case "PDD":
                        nEquip.setWdef((short) stat.getValue())
                        continue
                    # case "MAD":
                        nEquip.setMatk((short) stat.getValue())
                        continue
                    # case "MDD":
                        nEquip.setMdef((short) stat.getValue())
                        continue
                    # case "ACC":
                        nEquip.setAcc((short) stat.getValue())
                        continue
                    # case "EVA":
                        nEquip.setAvoid((short) stat.getValue())
                        continue
                    # case "Speed":
                        nEquip.setSpeed((short) stat.getValue())
                        continue
                    # case "Jump":
                        nEquip.setJump((short) stat.getValue())
                        continue
                    # case "MHP":
                        nEquip.setHp((short) stat.getValue())
                        continue
                    # case "MMP":
                        nEquip.setMp((short) stat.getValue())
                        continue
                    # case "MHPr":
                        nEquip.setHpR((short) stat.getValue())
                        continue
                    # case "MMPr":
                        nEquip.setMpR((short) stat.getValue())
                        continue
                    # case "tuc":
                        nEquip.setUpgradeSlots(stat.getValue().byteValue())
                        continue
                    # case "Craft":
                        nEquip.setHands(stat.getValue().shortValue())
                        continue
                    # case "durability":
                        nEquip.setDurability(stat.getValue())
                        continue
        self.equipCache.put(equipId, nEquip)
        return nEquip.copy()

    def getRandStat(self, defaultValue: int) -> int:
        if defaultValue == 0:
            return 0
        maxRange = 5
        defaultMaxRange = 0.1
        tmp = MapleItemInformationProvider.rand.nextInt(1200)
        if tmp >= 1199:
            maxRange = 100
            defaultMaxRange = 2.0
        elif tmp >= 1099:
            maxRange = 80
            defaultMaxRange = 1.7
        elif tmp >= 999:
            maxRange = 65
            defaultMaxRange = 1.5
        elif tmp >= 960:
            maxRange = 55
            defaultMaxRange = 1.3
        elif tmp >= 930:
            maxRange = 45
            defaultMaxRange = 1.0
        elif tmp >= 850:
            maxRange = 35
            defaultMaxRange = 0.8
        elif tmp >= 706:
            maxRange = 25
            defaultMaxRange = 0.6
        elif tmp >= 386:
            maxRange = 15
            defaultMaxRange = 0.4
        else:
            maxRange = 10
            defaultMaxRange = 0.2
        lMaxRange = min(math.ceil(defaultValue * defaultMaxRange), maxRange)
        return (short) (defaultValue - lMaxRange + math.floor(random.random() * (lMaxRange * 2 + 1)))

    def randomizeStats(self, equip: Any) -> Any:
        equip.setStr(self.getRandStat(equip.getStr()))
        equip.setDex(self.getRandStat(equip.getDex()))
        equip.setInt(self.getRandStat(equip.getInt()))
        equip.setLuk(self.getRandStat(equip.getLuk()))
        equip.setMatk(self.getRandStat(equip.getMatk()))
        equip.setWatk(self.getRandStat(equip.getWatk()))
        equip.setAcc(self.getRandStat(equip.getAcc()))
        equip.setAvoid(self.getRandStat(equip.getAvoid()))
        equip.setJump(self.getRandStat(equip.getJump()))
        equip.setHands(self.getRandStat(equip.getHands()))
        equip.setSpeed(self.getRandStat(equip.getSpeed()))
        equip.setWdef(self.getRandStat(equip.getWdef()))
        equip.setMdef(self.getRandStat(equip.getMdef()))
        equip.setHp(self.getRandStat(equip.getHp()))
        equip.setMp(self.getRandStat(equip.getMp()))
        return equip

    def getItemEffect(self, itemId: int) -> Any:
        ret = self.itemEffects.get(itemId)
        if ret is None:
            item = self.getItemData(itemId)
            if item is None:
                return None
            ret = MapleStatEffect.loadItemEffectFromData(item.getChildByPath("spec"), itemId)
            self.itemEffects.put(itemId, ret)
        return ret

    def getSummonMobs(self, itemId: int) -> list:
        if (itemId in self.summonMobCache):
            return self.summonMobCache.get(itemId)
        if not GameConstants.isSummonSack(itemId):
            return None
        data = self.getItemData(itemId).getChildByPath("mob")
        if data is None:
            return None
        mobPairs = new ArrayList<Pair<Integer, Integer>>()
        for child in data.getChildren():
            mobPairs.add(new Pair<Integer, Integer>(MapleDataTool.getIntConvert("id", child), MapleDataTool.getIntConvert("prob", child)))
        self.summonMobCache.put(itemId, mobPairs)
        return mobPairs

    def getCardMobId(self, id: int) -> int:
        if id == 0:
            return 0
        if (id in self.monsterBookID):
            return self.monsterBookID.get(id)
        data = self.getItemData(id)
        monsterid = MapleDataTool.getIntConvert("info/mob", data, 0)
        if monsterid == 0:
            return 0
        self.monsterBookID.put(id, monsterid)
        return self.monsterBookID.get(id)

    def getWatkForProjectile(self, itemId: int) -> int:
        atk = self.projectileWatkCache.get(itemId)
        if atk is not None:
            return atk
        data = self.getItemData(itemId)
        atk = MapleDataTool.getInt("info/incPAD", data, 0)
        self.projectileWatkCache.put(itemId, atk)
        return atk

    def canScroll(self, scrollid: int, itemid: int) -> bool:
        return scrollid / 100 % 100 == itemid / 10000 % 100

    def getName(self, itemId: int) -> str:
        if (itemId in self.nameCache):
            return self.nameCache.get(itemId)
        strings = self.getStringData(itemId)
        if strings is None:
            return None
        ret = MapleDataTool.getString("name", strings, None)
        self.nameCache.put(itemId, ret)
        return ret

    def getDesc(self, itemId: int) -> str:
        if (itemId in self.descCache):
            return self.descCache.get(itemId)
        strings = self.getStringData(itemId)
        if strings is None:
            return None
        ret = MapleDataTool.getString("desc", strings, None)
        self.descCache.put(itemId, ret)
        return ret

    def getMsg(self, itemId: int) -> str:
        if (itemId in self.msgCache):
            return self.msgCache.get(itemId)
        strings = self.getStringData(itemId)
        if strings is None:
            return None
        ret = MapleDataTool.getString("msg", strings, None)
        self.msgCache.put(itemId, ret)
        return ret

    def getItemMakeLevel(self, itemId: int) -> int:
        if (itemId in self.itemMakeLevel):
            return self.itemMakeLevel.get(itemId)
        if itemId / 10000 != 400:
            return 0
        lvl = MapleDataTool.getIntConvert("info/lv", self.getItemData(itemId), 0)
        self.itemMakeLevel.put(itemId, lvl)
        return lvl

    def isConsumeOnPickup(self, itemId: int) -> int:
        if (itemId in self.consumeOnPickupCache):
            return self.consumeOnPickupCache.get(itemId)
        data = self.getItemData(itemId)
        consume = MapleDataTool.getIntConvert("spec/consumeOnPickup", data, 0)
        if consume == 0:
            consume = MapleDataTool.getIntConvert("specEx/consumeOnPickup", data, 0)
        if consume == 1 and MapleDataTool.getIntConvert("spec/party", self.getItemData(itemId), 0) > 0:
            consume = 2
        self.consumeOnPickupCache.put(itemId, consume)
        return consume

    def isDropRestricted(self, itemId: int) -> bool:
        if (itemId in self.dropRestrictionCache):
            return self.dropRestrictionCache.get(itemId)
        data = self.getItemData(itemId)
        trade = False
        if MapleDataTool.getIntConvert("info/tradeBlock", data, 0) == 1 or MapleDataTool.getIntConvert("info/quest", data, 0) == 1:
            trade = True
        self.dropRestrictionCache.put(itemId, trade)
        return trade

    def isPickupRestricted(self, itemId: int) -> bool:
        if (itemId in self.pickupRestrictionCache):
            return self.pickupRestrictionCache.get(itemId)
        bRestricted = MapleDataTool.getIntConvert("info/only", self.getItemData(itemId), 0) == 1
        self.pickupRestrictionCache.put(itemId, bRestricted)
        return bRestricted

    def isAccountShared(self, itemId: int) -> bool:
        if (itemId in self.accCache):
            return self.accCache.get(itemId)
        bRestricted = MapleDataTool.getIntConvert("info/accountSharable", self.getItemData(itemId), 0) == 1
        self.accCache.put(itemId, bRestricted)
        return bRestricted

    def getStateChangeItem(self, itemId: int) -> int:
        if (itemId in self.stateChangeCache):
            return self.stateChangeCache.get(itemId)
        triggerItem = MapleDataTool.getIntConvert("info/stateChangeItem", self.getItemData(itemId), 0)
        self.stateChangeCache.put(itemId, triggerItem)
        return triggerItem

    def getMeso(self, itemId: int) -> int:
        if (itemId in self.mesoCache):
            return self.mesoCache.get(itemId)
        triggerItem = MapleDataTool.getIntConvert("info/meso", self.getItemData(itemId), 0)
        self.mesoCache.put(itemId, triggerItem)
        return triggerItem

    def isKarmaEnabled(self, itemId: int) -> bool:
        if (itemId in self.karmaEnabledCache):
            return self.karmaEnabledCache.get(itemId) == 1
        iRestricted = MapleDataTool.getIntConvert("info/tradeAvailable", self.getItemData(itemId), 0)
        self.karmaEnabledCache.put(itemId, iRestricted)
        return iRestricted == 1

    def isPKarmaEnabled(self, itemId: int) -> bool:
        if (itemId in self.karmaEnabledCache):
            return self.karmaEnabledCache.get(itemId) == 2
        iRestricted = MapleDataTool.getIntConvert("info/tradeAvailable", self.getItemData(itemId), 0)
        self.karmaEnabledCache.put(itemId, iRestricted)
        return iRestricted == 2

    def isPickupBlocked(self, itemId: int) -> bool:
        if (itemId in self.blockPickupCache):
            return self.blockPickupCache.get(itemId)
        iRestricted = MapleDataTool.getIntConvert("info/pickUpBlock", self.getItemData(itemId), 0) == 1
        self.blockPickupCache.put(itemId, iRestricted)
        return iRestricted

    def isLogoutExpire(self, itemId: int) -> bool:
        if (itemId in self.logoutExpireCache):
            return self.logoutExpireCache.get(itemId)
        iRestricted = MapleDataTool.getIntConvert("info/expireOnLogout", self.getItemData(itemId), 0) == 1
        self.logoutExpireCache.put(itemId, iRestricted)
        return iRestricted

    def cantSell(self, itemId: int) -> bool:
        if (itemId in self.notSaleCache):
            return self.notSaleCache.get(itemId)
        bRestricted = MapleDataTool.getIntConvert("info/notSale", self.getItemData(itemId), 0) == 1
        self.notSaleCache.put(itemId, bRestricted)
        return bRestricted

    def getRewardItem(self, itemid: int) -> Any:
        if (itemid in self.RewardItem):
            return self.RewardItem.get(itemid)
        data = self.getItemData(itemid)
        if data is None:
            return None
        rewards = data.getChildByPath("reward")
        if rewards is None:
            return None
        totalprob = 0
        all = []
        for reward in rewards:
            struct = StructRewardItem()
            struct.itemid = MapleDataTool.getInt("item", reward, 0)
            struct.prob = MapleDataTool.getInt("prob", reward, 0)
            struct.quantity = MapleDataTool.getInt("count", reward, 0)
            struct.effect = MapleDataTool.getString("Effect", reward, "")
            struct.worldmsg = MapleDataTool.getString("worldMsg", reward, None)
            struct.period = MapleDataTool.getInt("period", reward, -1)
            totalprob += struct.prob
            all.add(struct)
        toreturn = new Pair<Integer, List<StructRewardItem>>(totalprob, all)
        self.RewardItem.put(itemid, toreturn)
        return toreturn

    def getSkillStats(self, itemId: int) -> dict:
        if (itemId in self.SkillStatsCache):
            return self.SkillStatsCache.get(itemId)
        if itemId / 10000 != 228 and itemId / 10000 != 229 and itemId / 10000 != 562:
            return None
        item = self.getItemData(itemId)
        if item is None:
            return None
        info = item.getChildByPath("info")
        if info is None:
            return None
        ret = {}
        for data in info.getChildren():
            if data.getName().startswith("inc"):
                ret.put(data.getName()[3:], MapleDataTool.getIntConvert(data))
        ret.put("masterLevel", MapleDataTool.getInt("masterLevel", info, 0))
        ret.put("reqSkillLevel", MapleDataTool.getInt("reqSkillLevel", info, 0))
        ret.put("success", MapleDataTool.getInt("success", info, 0))
        skill = info.getChildByPath("skill")
        for i in range(skill.getChildren()):
            ret.put("skillid" + i, MapleDataTool.getInt(Integer.toString(i), skill, 0))
        self.SkillStatsCache.put(itemId, ret)
        return ret

    def petsCanConsume(self, itemId: int) -> list:
        if self.petsCanConsumeCache.get(itemId) is not None:
            return self.petsCanConsumeCache.get(itemId)
        ret = []
        data = self.getItemData(itemId)
        if data is None or data.getChildByPath("spec") is None:
            return ret
        curPetId = 0
        for c in data.getChildByPath("spec"):
            try:
                int(c.getName())
            except NumberFormatException as e:
                continue
            curPetId = MapleDataTool.getInt(c, 0)
            if curPetId == 0:
                break
            ret.add(curPetId)
        self.petsCanConsumeCache.put(itemId, ret)
        return ret

    def isQuestItem(self, itemId: int) -> bool:
        if (itemId in self.isQuestItemCache):
            return self.isQuestItemCache.get(itemId)
        questItem = MapleDataTool.getIntConvert("info/quest", self.getItemData(itemId), 0) == 1
        self.isQuestItemCache.put(itemId, questItem)
        return questItem

    def questItemInfo(self, itemId: int) -> Any:
        if (itemId in self.questItems):
            return self.questItems.get(itemId)
        if itemId / 10000 != 422 or self.getItemData(itemId) is None:
            return None
        itemD = self.getItemData(itemId).getChildByPath("info")
        if itemD is None or itemD.getChildByPath("consumeItem") is None:
            return None
        consumeItems = []
        for consume in itemD.getChildByPath("consumeItem"):
            consumeItems.add(MapleDataTool.getInt(consume, 0))
        questItem = new Pair<Integer, List<Integer>>(MapleDataTool.getIntConvert("questId", itemD, 0), consumeItems)
        self.questItems.put(itemId, questItem)
        return questItem

    def itemExists(self, itemId: int) -> bool:
        return GameConstants.getInventoryType(itemId) != MapleInventoryType.UNDEFINED and self.getItemData(itemId) is not None

    def isCash(self, itemId: int) -> bool:
        if self.getEquipStats(itemId) is None:
            return GameConstants.getInventoryType(itemId) == MapleInventoryType.CASH
        return GameConstants.getInventoryType(itemId) == MapleInventoryType.CASH or self.getEquipStats(itemId).get("cash") > 0

    def getInventoryType(self, itemId: int) -> Any:
        if (itemId in self.inventoryTypeCache):
            return self.inventoryTypeCache.get(itemId)
        idStr = "0" + str(itemId)
        root = self.itemData.getRoot()
        for topDir in root.getSubdirectories():
            for iFile in topDir.getFiles():
                if iFile.getName() == (idStr[0:4] + ".img"):
                    ret = MapleInventoryType.getByWZName(topDir.getName())
                    self.inventoryTypeCache.put(itemId, ret)
                    return ret
                if iFile.getName() == (idStr[1:] + ".img"):
                    ret = MapleInventoryType.getByWZName(topDir.getName())
                    self.inventoryTypeCache.put(itemId, ret)
                    return ret
        root = self.equipData.getRoot()
        for topDir in root.getSubdirectories():
            for iFile in topDir.getFiles():
                if iFile.getName() == (idStr + ".img"):
                    ret = MapleInventoryType.EQUIP
                    self.inventoryTypeCache.put(itemId, ret)
                    return ret
        ret = MapleInventoryType.UNDEFINED
        self.inventoryTypeCache.put(itemId, ret)
        return ret

    def getPetFlagInfo(self, itemId: int) -> int:
        flag = 0
        if itemId / 10000 != 500:
            return flag
        item = self.getItemData(itemId)
        if item is None:
            return flag
        if MapleDataTool.getIntConvert("info/pickupItem", item, 0) > 0:
            flag |= 0x1
        if MapleDataTool.getIntConvert("info/longRange", item, 0) > 0:
            flag |= 0x2
        if MapleDataTool.getIntConvert("info/pickupAll", item, 0) > 0:
            flag |= 0x4
        if MapleDataTool.getIntConvert("info/sweepForDrop", item, 0) > 0:
            flag |= 0x10
        if MapleDataTool.getIntConvert("info/consumeHP", item, 0) > 0:
            flag |= 0x20
        if MapleDataTool.getIntConvert("info/consumeMP", item, 0) > 0:
            flag |= 0x40
        return flag

    def isKarmaAble(self, itemId: int) -> bool:
        if (itemId in self.karmaCache):
            return self.karmaCache.get(itemId)
        data = self.getItemData(itemId)
        bRestricted = MapleDataTool.getIntConvert("info/tradeAvailable", data, 0) > 0
        self.karmaCache.put(itemId, bRestricted)
        return bRestricted

    def getItemLevelupStats(self, itemId: int, level: int, timeless: bool) -> list:
        list = new LinkedList<Pair<String, Integer>>()
        data = self.getItemData(itemId)
        data2 = data.getChildByPath("info").getChildByPath("level")
        if data2 is not None:
            data3 = data2.getChildByPath("info").getChildByPath(Integer.toString(level))
            if data3 is not None:
                for da in data3.getChildren():
                    if random.random() < 0.9:
                        if da.getName().startswith("incDEXMin"):
                            list.add(new Pair<String, Integer>("incDEX", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incDEXMax")))))
                        elif da.getName().startswith("incSTRMin"):
                            list.add(new Pair<String, Integer>("incSTR", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incSTRMax")))))
                        elif da.getName().startswith("incINTMin"):
                            list.add(new Pair<String, Integer>("incINT", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incINTMax")))))
                        elif da.getName().startswith("incLUKMin"):
                            list.add(new Pair<String, Integer>("incLUK", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incLUKMax")))))
                        elif da.getName().startswith("incMHPMin"):
                            list.add(new Pair<String, Integer>("incMHP", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incMHPMax")))))
                        elif da.getName().startswith("incMMPMin"):
                            list.add(new Pair<String, Integer>("incMMP", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incMMPMax")))))
                        elif da.getName().startswith("incPADMin"):
                            list.add(new Pair<String, Integer>("incPAD", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incPADMax")))))
                        elif da.getName().startswith("incMADMin"):
                            list.add(new Pair<String, Integer>("incMAD", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incMADMax")))))
                        elif da.getName().startswith("incPDDMin"):
                            list.add(new Pair<String, Integer>("incPDD", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incPDDMax")))))
                        elif da.getName().startswith("incMDDMin"):
                            list.add(new Pair<String, Integer>("incMDD", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incMDDMax")))))
                        elif da.getName().startswith("incACCMin"):
                            list.add(new Pair<String, Integer>("incACC", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incACCMax")))))
                        elif da.getName().startswith("incEVAMin"):
                            list.add(new Pair<String, Integer>("incEVA", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incEVAMax")))))
                        elif da.getName().startswith("incSpeedMin"):
                            list.add(new Pair<String, Integer>("incSpeed", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incSpeedMax")))))
                        else:
                            if not da.getName().startswith("incJumpMin"):
                                continue
                            list.add(new Pair<String, Integer>("incJump", self.rand(MapleDataTool.getInt(da), MapleDataTool.getInt(data3.getChildByPath("incJumpMax")))))
        return list

    def isUntradeableOnEquip(self, itemId: int) -> bool:
        if (itemId in self.onEquipUntradableCache):
            return self.onEquipUntradableCache.get(itemId)
        untradableOnEquip = MapleDataTool.getIntConvert("info/equipTradeBlock", self.getItemData(itemId), 0) > 0
        self.onEquipUntradableCache.put(itemId, untradableOnEquip)
        return untradableOnEquip

    def getExpCache(self, itemId: int) -> int:
        if (itemId in self.getExpCache):
            return self.getExpCache.get(itemId)
        item = self.getItemData(itemId)
        if item is None:
            return 0
        pEntry = 0
        pData = item.getChildByPath("spec/exp")
        if pData is None:
            return 0
        pEntry = MapleDataTool.getInt(pData)
        self.getExpCache.put(itemId, pEntry)
        return pEntry

    def hairExists(self, hair: int) -> bool:
        return (hair in self.hairList)

    def faceExists(self, face: int) -> bool:
        return (face in self.faceList)

    def getLimitBreak(self, itemId: int) -> int:
        if self.getEquipStats(itemId) is None or not self.getEquipStats(itemId).__contains__("limitBreak"):
            return 999999
        return self.getEquipStats(itemId).get("limitBreak")

    def getAllItems2(self) -> list:
        itemPairs = new ArrayList<Pair<Integer, String>>()
        itemsData = self.stringData.getData("Cash.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Consume.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Eqp.img").getChildByPath("Eqp")
        for eqpType in itemsData.getChildren():
            for itemFolder2 in eqpType.getChildren():
                itemPairs.add(new Pair<Integer, String>(int(itemFolder2.getName()), MapleDataTool.getString("name", itemFolder2, "NO-NAME")))
        itemsData = self.stringData.getData("Etc.img").getChildByPath("Etc")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Ins.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        itemsData = self.stringData.getData("Pet.img")
        for itemFolder in itemsData.getChildren():
            itemPairs.add(new Pair<Integer, String>(int(itemFolder.getName()), MapleDataTool.getString("name", itemFolder, "NO-NAME")))
        return itemPairs

    def loadHairFace(self, reload: bool) -> None:
        if reload:
            self.hairList.clear()
            self.faceList.clear()
        if not self.hairList == 0 or not self.faceList == 0:
            return
        array = None
        types = array = new String[]{"Hair", "Face"}
        for type in array:
            data = None
            for d in self.chrData.getRoot().getSubdirectories():
                if d.getName() == (type):
                    data = d
                    break
            if data is not None:
                for c in self.stringData.getData("Item.img").getChildByPath("Eqp/" + type):
                    if data.getEntry(StringUtil.getLeftPaddedStr(c.getName() + ".img", '0', 12)) is not None:
                        dataid = int(c.getName())
                        name = MapleDataTool.getString("name", c, "无名字")
                        if type == ("Hair"):
                            self.hairList.put(dataid, name)
                        else:
                            self.faceList.put(dataid, name)

    def getTotalStat(self, equip: Any) -> int:
        return equip.getStr() + equip.getDex() + equip.getInt() + equip.getLuk() + equip.getMatk() * 5 + equip.getWatk() * 5

