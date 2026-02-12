"""
ItemMakerHandler - Converted from Java source
Original: handling/channel/handler/ItemMakerHandler.java
Package: handling.channel.handler
"""

from typing import Dict
from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.ItemMakerFactory import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class ItemMakerHandler:
    """
    Class ItemMakerHandler
    """


    def ItemMaker(self, slea: Any, c: Any) -> None:
        makerType = slea.readInt()
        # switch (makerType):
            # case 1:
                toCreate = slea.readInt()
                if GameConstants.isGem(toCreate):
                    final ItemMakerFactory.GemCreateEntry gem = ItemMakerFactory.getInstance().getGemInfo(toCreate)
                    if gem is None:
                        return
                    if !hasSkill(c, gem.getReqSkillLevel()):
                        return
                    if c.getPlayer().getMeso() < gem.getCost():
                        return
                    randGemGiven = getRandomGem(gem.getRandomReward())
                    if c.getPlayer().getInventory(GameConstants.getInventoryType(randGemGiven)).isFull():
                        return
                    taken = checkRequiredNRemove(c, gem.getReqRecipes())
                    if taken == 0:
                        return
                    c.getPlayer().gainMeso(-gem.getCost(), False)
                    MapleInventoryManipulator.addById(c, randGemGiven, (byte)((taken == randGemGiven) ? 9 : 1), 0)
                    c.getSession().write(MaplePacketCreator.ItemMaker_Success())
                    c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.ItemMaker_Success_3rdParty(c.getPlayer().getId()), False)
                    break
                elif GameConstants.isOtherGem(toCreate):
                    final ItemMakerFactory.GemCreateEntry gem = ItemMakerFactory.getInstance().getGemInfo(toCreate)
                    if gem is None:
                        return
                    if !hasSkill(c, gem.getReqSkillLevel()):
                        return
                    if c.getPlayer().getMeso() < gem.getCost():
                        return
                    if c.getPlayer().getInventory(GameConstants.getInventoryType(toCreate)).isFull():
                        return
                    if checkRequiredNRemove(c, gem.getReqRecipes()) == 0:
                        return
                    c.getPlayer().gainMeso(-gem.getCost(), False)
                    if GameConstants.getInventoryType(toCreate) == MapleInventoryType.EQUIP:
                        MapleInventoryManipulator.addbyItem(c, MapleItemInformationProvider.getInstance().getEquipById(toCreate))
                    else:
                        MapleInventoryManipulator.addById(c, toCreate, 1, 0)
                    c.getSession().write(MaplePacketCreator.ItemMaker_Success())
                    c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.ItemMaker_Success_3rdParty(c.getPlayer().getId()), False)
                    break
                else:
                    stimulator = slea.readByte() > 0
                    numEnchanter = slea.readInt()
                    final ItemMakerFactory.ItemMakerCreateEntry create = ItemMakerFactory.getInstance().getCreateInfo(toCreate)
                    if create is None:
                        return
                    if numEnchanter > create.getTUC():
                        return
                    if !hasSkill(c, create.getReqSkillLevel()):
                        return
                    if c.getPlayer().getMeso() < create.getCost():
                        return
                    if c.getPlayer().getInventory(GameConstants.getInventoryType(toCreate)).isFull():
                        return
                    if checkRequiredNRemove(c, create.getReqItems()) == 0:
                        return
                    c.getPlayer().gainMeso(-create.getCost(), False)
                    ii = MapleItemInformationProvider.getInstance()
                    toGive = ii.getEquipById(toCreate)
                    if stimulator || numEnchanter > 0:
                        if c.getPlayer().haveItem(create.getStimulator(), 1, False, True):
                            ii.randomizeStats(toGive)
                            MapleInventoryManipulator.removeById(c, MapleInventoryType.ETC, create.getStimulator(), 1, False, False)
                        for i in range(numEnchanter):
                            enchant = slea.readInt()
                            if c.getPlayer().haveItem(enchant, 1, False, True):
                                stats = ii.getItemMakeStats(enchant)
                                if stats is not None:
                                    addEnchantStats(stats, toGive)
                                    MapleInventoryManipulator.removeById(c, MapleInventoryType.ETC, enchant, 1, False, False)
                    MapleInventoryManipulator.addbyItem(c, toGive)
                    c.getSession().write(MaplePacketCreator.ItemMaker_Success())
                    c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.ItemMaker_Success_3rdParty(c.getPlayer().getId()), False)
                    break
            # case 3:
                etc = slea.readInt()
                if c.getPlayer().haveItem(etc, 100, False, True):
                    MapleInventoryManipulator.addById(c, getCreateCrystal(etc), 1, 0)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.ETC, etc, 100, False, False)
                    c.getSession().write(MaplePacketCreator.ItemMaker_Success())
                    c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.ItemMaker_Success_3rdParty(c.getPlayer().getId()), False)
                    break
                break
            # case 4:
                itemId = slea.readInt()
                c.getPlayer().updateTick(slea.readInt())
                slot = slea.readInt()
                toUse = c.getPlayer().getInventory(MapleInventoryType.EQUIP).getItem(slot)
                if toUse is None || toUse.getItemId() != itemId || toUse.getQuantity() < 1:
                    return
                ii2 = MapleItemInformationProvider.getInstance()
                if !ii2.isDropRestricted(itemId) && !ii2.isAccountShared(itemId):
                    toGive2 = getCrystal(itemId, ii2.getReqLevel(itemId))
                    MapleInventoryManipulator.addById(c, toGive2[0], toGive2[1], 0)
                    MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.EQUIP, slot, 1, False)
                c.getSession().write(MaplePacketCreator.ItemMaker_Success())
                c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.ItemMaker_Success_3rdParty(c.getPlayer().getId()), False)
                break

    def getCreateCrystal(self, etc: int) -> int:
        level = MapleItemInformationProvider.getInstance().getItemMakeLevel(etc)
        itemid = None
        if level >= 31 && level <= 50:
            itemid = 4260000
        elif level >= 51 && level <= 60:
            itemid = 4260001
        elif level >= 61 && level <= 70:
            itemid = 4260002
        elif level >= 71 && level <= 80:
            itemid = 4260003
        elif level >= 81 && level <= 90:
            itemid = 4260004
        elif level >= 91 && level <= 100:
            itemid = 4260005
        elif level >= 101 && level <= 110:
            itemid = 4260006
        elif level >= 111 && level <= 120:
            itemid = 4260007
        else:
            if level < 121:
                raise RuntimeError("Invalid Item Maker id")
            itemid = 4260008
        return itemid

    def getCrystal(self, itemid: int, level: int) -> list:
        all = { -1, 0 }
        if level >= 31 && level <= 50:
            all[0] = 4260000
        elif level >= 51 && level <= 60:
            all[0] = 4260001
        elif level >= 61 && level <= 70:
            all[0] = 4260002
        elif level >= 71 && level <= 80:
            all[0] = 4260003
        elif level >= 81 && level <= 90:
            all[0] = 4260004
        elif level >= 91 && level <= 100:
            all[0] = 4260005
        elif level >= 101 && level <= 110:
            all[0] = 4260006
        elif level >= 111 && level <= 120:
            all[0] = 4260007
        else:
            if level < 121 || level > 200:
                raise RuntimeError("Invalid Item Maker type" + level)
            all[0] = 4260008
        if GameConstants.isWeapon(itemid) || GameConstants.isOverall(itemid):
            all[1] = Randomizer.rand(5, 11)
        else:
            all[1] = Randomizer.rand(3, 7)
        return all

    def addEnchantStats(self, stats: dict, item: Any) -> None:
        s = stats.get("incPAD")
        if s != 0:
            item.setWatk((short)(item.getWatk() + s))
        s = stats.get("incMAD")
        if s != 0:
            item.setMatk((short)(item.getMatk() + s))
        s = stats.get("incACC")
        if s != 0:
            item.setAcc((short)(item.getAcc() + s))
        s = stats.get("incEVA")
        if s != 0:
            item.setAvoid((short)(item.getAvoid() + s))
        s = stats.get("incSpeed")
        if s != 0:
            item.setSpeed((short)(item.getSpeed() + s))
        s = stats.get("incJump")
        if s != 0:
            item.setJump((short)(item.getJump() + s))
        s = stats.get("incMaxHP")
        if s != 0:
            item.setHp((short)(item.getHp() + s))
        s = stats.get("incMaxMP")
        if s != 0:
            item.setMp((short)(item.getMp() + s))
        s = stats.get("incSTR")
        if s != 0:
            item.setStr((short)(item.getStr() + s))
        s = stats.get("incDEX")
        if s != 0:
            item.setDex((short)(item.getDex() + s))
        s = stats.get("incINT")
        if s != 0:
            item.setInt((short)(item.getInt() + s))
        s = stats.get("incLUK")
        if s != 0:
            item.setLuk((short)(item.getLuk() + s))
        s = stats.get("randOption")
        if s > 0:
            success = Randomizer.nextBoolean()
            ma = item.getMatk()
            wa = item.getWatk()
            if wa > 0:
                item.setWatk((short)(success ? (wa + s) : (wa - s)))
            if ma > 0:
                item.setMatk((short)(success ? (ma + s) : (ma - s)))
        s = stats.get("randStat")
        if s > 0:
            success = Randomizer.nextBoolean()
            str = item.getStr()
            dex = item.getDex()
            luk = item.getLuk()
            int_ = item.getInt()
            if str > 0:
                item.setStr((short)(success ? (str + s) : (str - s)))
            if dex > 0:
                item.setDex((short)(success ? (dex + s) : (dex - s)))
            if int_ > 0:
                item.setInt((short)(success ? (int_ + s) : (int_ - s)))
            if luk > 0:
                item.setLuk((short)(success ? (luk + s) : (luk - s)))

    def getRandomGem(self, rewards: list) -> int:
        items = []
        for p in rewards:
            itemid = p.getLeft()
            for i in range(p.getRight()):
            items.add(itemid)
        return (items.get(Randomizer.nextInt(items)))

    def checkRequiredNRemove(self, c: Any, recipe: list) -> int:
        itemid = 0
        for p in recipe:
            if !c.getPlayer().haveItem(p.getLeft(), p.getRight(), False, True):
                return 0
        for p in recipe:
            itemid = p.getLeft()
            MapleInventoryManipulator.removeById(c, GameConstants.getInventoryType(itemid), itemid, p.getRight(), False, False)
        return itemid

    def hasSkill(self, c: Any, reqlvl: int) -> bool:
        if GameConstants.isKOC(c.getPlayer().getJob()):
            return c.getPlayer().getSkillLevel(SkillFactory.getSkill(10001007)) >= reqlvl
        if GameConstants.isAran(c.getPlayer().getJob()):
            return c.getPlayer().getSkillLevel(SkillFactory.getSkill(20001007)) >= reqlvl
        if GameConstants.isEvan(c.getPlayer().getJob()):
            return c.getPlayer().getSkillLevel(SkillFactory.getSkill(20011007)) >= reqlvl
        if GameConstants.isResist(c.getPlayer().getJob()):
            return c.getPlayer().getSkillLevel(SkillFactory.getSkill(30001007)) >= reqlvl
        return c.getPlayer().getSkillLevel(SkillFactory.getSkill(1007)) >= reqlvl

