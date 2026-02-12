"""
InventoryHandler - Converted from Java source
Original: handling/channel/handler/InventoryHandler.java
Package: handling.channel.handler
"""

from threading import Lock
from typing import Dict
from typing import List
from typing import Optional, Any
import math
import threading
import time

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IEquip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MapleMount import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.AutobanManager import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleShopFactory import *  # TODO: import specific classes
# from server.PredictCardFactory import *  # TODO: import specific classes
# from server.RandomRewards import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.StructRewardItem import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleLove import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapItem import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleMist import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from server.shops.HiredMerchant import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class InventoryHandler:
    """
    Class InventoryHandler
    """

    # Static initializer
    # InventoryHandler.OWL_ID = 2


    @staticmethod
    def ItemMove(slea: Any, c: Any) -> None:
        if c.getPlayer().getPlayerShop() is not None || c.getPlayer().getConversation() > 0 || c.getPlayer().getTrade() is not None:
            return
        c.getPlayer().updateTick(slea.readInt())
        type = MapleInventoryType.getByType(slea.readByte())
        src = slea.readShort()
        dst = slea.readShort()
        quantity = slea.readShort()
        if src < 0 && dst > 0:
            MapleInventoryManipulator.unequip(c, src, dst)
        elif dst < 0:
            MapleInventoryManipulator.equip(c, src, dst)
        elif dst == 0:
            MapleInventoryManipulator.drop(c, type, src, quantity)
        else:
            if c.getPlayer().getGMLevel() > 0:
                itemided = c.getPlayer().getInventory(type).getItem(src).getItemId()
                c.getPlayer().dropMessage("此物品的ID是:" + itemided)
            MapleInventoryManipulator.move(c, type, src, dst)

    def ItemSort(self, slea: Any, c: Any) -> None:
        c.getPlayer().updateTick(slea.readInt())
        pInvType = MapleInventoryType.getByType(slea.readByte())
        if pInvType == MapleInventoryType.UNDEFINED:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        pInv = c.getPlayer().getInventory(pInvType)
        sorted = False
        while !sorted:
            freeSlot = pInv.getNextFreeSlot()
            if freeSlot != -1:
                itemSlot = -1
                i = (byte)(freeSlot + 1)
                while i <= pInv.getSlotLimit():
                    if pInv.getItem(i) is not None:
                        itemSlot = i
                        break
                if itemSlot > 0:
                    MapleInventoryManipulator.move(c, pInvType, itemSlot, freeSlot)
                else:
                    sorted = True
            else:
                sorted = True
        c.getSession().write(MaplePacketCreator.finishedSort(pInvType.getType()))
        c.getSession().write(MaplePacketCreator.enableActions())

    def ItemGather(self, slea: Any, c: Any) -> None:
        c.getPlayer().updateTick(slea.readInt())
        mode = slea.readByte()
        invType = MapleInventoryType.getByType(mode)
        Inv = c.getPlayer().getInventory(invType)
        itemMap = []
        for item in Inv.list():
            itemMap.add(item.copy())
        for itemStats in itemMap:
            if itemStats.getItemId() != 5110000:
                MapleInventoryManipulator.removeById(c, invType, itemStats.getItemId(), itemStats.getQuantity(), True, False)
        sortedItems = sortItems(itemMap)
        for item2 in sortedItems:
            if item2.getItemId() != 5110000:
                MapleInventoryManipulator.addFromDrop(c, item2, False)
        c.getSession().write(MaplePacketCreator.finishedGather(mode))
        c.getSession().write(MaplePacketCreator.enableActions())
        itemMap.clear()
        sortedItems.clear()

    def sortItems(self, passedMap: list) -> list:
        itemIds = []
        for item in passedMap:
            itemIds.add(item.getItemId())
        Collections.sort(itemIds)
        sortedList = []
        for val in itemIds:
            for item2 in passedMap:
                if val == item2.getItemId():
                    sortedList.add(item2)
                    passedMap.remove(item2)
                    break
        return sortedList

    def UseRewardItem(self, slot: int, itemId: int, c: Any, chr: Any) -> bool:
        toUse = c.getPlayer().getInventory(GameConstants.getInventoryType(itemId)).getItem(slot)
        c.getSession().write(MaplePacketCreator.enableActions())
        if toUse is not None && toUse.getQuantity() >= 1 && toUse.getItemId() == itemId:
            if chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot() > -1 && chr.getInventory(MapleInventoryType.USE).getNextFreeSlot() > -1 && chr.getInventory(MapleInventoryType.SETUP).getNextFreeSlot() > -1 && chr.getInventory(MapleInventoryType.ETC).getNextFreeSlot() > -1:
                ii = MapleItemInformationProvider.getInstance()
                rewards = ii.getRewardItem(itemId)
                if rewards is not None && rewards.getLeft() > 0:
                    rewarded = False
                    while !rewarded:
                        for reward in rewards.getRight():
                            if reward.prob > 0 && Randomizer.nextInt(rewards.getLeft()) < reward.prob:
                                if GameConstants.getInventoryType(reward.itemid) == MapleInventoryType.EQUIP:
                                    item = ii.getEquipById(reward.itemid)
                                    if reward.period > 0:
                                        item.setExpiration(int(time.time() * 1000) + reward.period * 60 * 60 * 10)
                                    MapleInventoryManipulator.addbyItem(c, item)
                                else:
                                    MapleInventoryManipulator.addById(c, reward.itemid, reward.quantity, 0)
                                MapleInventoryManipulator.removeById(c, GameConstants.getInventoryType(itemId), itemId, 1, False, False)
                                rewarded = True
                                return True
                else:
                    chr.dropMessage(6, "Unknown error.")
            else:
                chr.dropMessage(6, "你有一個欄位滿了 請空出來再打開")
        return False

    def QuestKJ(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || !chr.isAlive() || chr.getCSPoints(2) < 200:
            chr.dropMessage(1, "你没有足够的抵用卷！")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        action = (byte)(slea.readByte() + 1)
        quest = slea.readShort()
        if quest < 0:
            quest += 65536
        if chr is None:
            return
        q = MapleQuest.getInstance(quest)
        # switch (action):
            # case 2:
                npc = slea.readInt()
                q.complete(chr, npc)
                break
        chr.modifyCSPoints(2, -200)

    def UseItem(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || !chr.isAlive() || chr.getMapId() == 749040100 || chr.getMap() is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        time = int(time.time() * 1000)
        if chr.getNextConsume() > time:
            chr.dropMessage(5, "暂时无法使用这个道具，请稍后在试。")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        c.getPlayer().updateTick(slea.readInt())
        slot = slea.readShort()
        itemId = slea.readInt()
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is None || toUse.getQuantity() < 1 || toUse.getItemId() != itemId:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if !FieldLimitType.PotionUse.check(chr.getMap().getFieldLimit()) || chr.getMapId() == 610030600:
            if MapleItemInformationProvider.getInstance().getItemEffect(toUse.getItemId()).applyTo(chr):
                MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
                if chr.getMap().getConsumeItemCoolTime() > 0:
                    chr.setNextConsume(time + chr.getMap().getConsumeItemCoolTime() * 1000)
        else:
            c.getSession().write(MaplePacketCreator.enableActions())

    def UseReturnScroll(self, slea: Any, c: Any, chr: Any) -> None:
        if !chr.isAlive() || chr.getMapId() == 749040100:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        c.getPlayer().updateTick(slea.readInt())
        slot = slea.readShort()
        itemId = slea.readInt()
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is None || toUse.getQuantity() < 1 || toUse.getItemId() != itemId:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if MapleItemInformationProvider.getInstance().getItemEffect(toUse.getItemId()).applyReturnScroll(chr):
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
        else:
            c.getSession().write(MaplePacketCreator.enableActions())

    def UseUpgradeScroll(self, slot: int, dst: int, ws: int, c: Any, chr: Any) -> bool:
        return UseUpgradeScroll(slot, dst, ws, c, chr, 0)

    def UseUpgradeScroll_slot_dst_ws_c_chr_vegas(self, slot: int, dst: int, ws: int, c: Any, chr: Any, vegas: int) -> bool:
        whiteScroll = False
        legendarySpirit = False
        ii = MapleItemInformationProvider.getInstance()
        if (ws & 0x2) == 0x2:
            whiteScroll = True
        toScroll = None
        if dst < 0:
            toScroll = chr.getInventory(MapleInventoryType.EQUIPPED).getItem(dst)
        else:
            legendarySpirit = True
            toScroll = chr.getInventory(MapleInventoryType.EQUIP).getItem(dst)
        if toScroll is None:
            return False
        oldLevel = toScroll.getLevel()
        oldEnhance = toScroll.getEnhance()
        oldState = toScroll.getState()
        oldFlag = toScroll.getFlag()
        oldSlots = toScroll.getUpgradeSlots()
        checkIfGM = c.getPlayer().isGM()
        scroll = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if scroll is None:
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if !GameConstants.isSpecialScroll(scroll.getItemId()) && !GameConstants.isCleanSlate(scroll.getItemId()) && !GameConstants.isEquipScroll(scroll.getItemId()) && !GameConstants.isPotentialScroll(scroll.getItemId()):
            if toScroll.getUpgradeSlots() < 1:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                return False
        elif GameConstants.isEquipScroll(scroll.getItemId()):
            if toScroll.getUpgradeSlots() >= 1 || toScroll.getEnhance() >= 100 || vegas > 0 || ii.isCash(toScroll.getItemId()):
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                return False
        elif GameConstants.isPotentialScroll(scroll.getItemId()) && (toScroll.getState() >= 1 || (toScroll.getLevel() == 0 && toScroll.getUpgradeSlots() == 0) || vegas > 0 || ii.isCash(toScroll.getItemId())):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if !GameConstants.canScroll(toScroll.getItemId()) && !GameConstants.isChaosScroll(toScroll.getItemId()):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if (GameConstants.isCleanSlate(scroll.getItemId()) || GameConstants.isTablet(scroll.getItemId()) || GameConstants.isChaosScroll(scroll.getItemId())) && (vegas > 0 || ii.isCash(toScroll.getItemId())):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if GameConstants.isTablet(scroll.getItemId()) && toScroll.getDurability() < 0:
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if !GameConstants.isTablet(scroll.getItemId()) && toScroll.getDurability() >= 0:
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        wscroll = None
        scrollReqs = ii.getScrollReqs(scroll.getItemId())
        if scrollReqs > 0 && !(toScroll.getItemId( in scrollReqs)):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return False
        if whiteScroll:
            wscroll = chr.getInventory(MapleInventoryType.USE).findById(2340000)
            if wscroll is None:
                whiteScroll = False
        if scroll.getItemId() == 2049115 && toScroll.getItemId() != 1003068:
            return False
        if GameConstants.isTablet(scroll.getItemId()):
            # switch (scroll.getItemId() % 1000 / 100):
                # case 0:
                    if GameConstants.isTwoHanded(toScroll.getItemId()) || !GameConstants.isWeapon(toScroll.getItemId()):
                        return False
                    break
                # case 1:
                    if !GameConstants.isTwoHanded(toScroll.getItemId()) || !GameConstants.isWeapon(toScroll.getItemId()):
                        return False
                    break
                # case 2:
                    if GameConstants.isAccessory(toScroll.getItemId()) || GameConstants.isWeapon(toScroll.getItemId()):
                        return False
                    break
                # case 3:
                    if !GameConstants.isAccessory(toScroll.getItemId()) || GameConstants.isWeapon(toScroll.getItemId()):
                        return False
                    break
        elif !GameConstants.isAccessoryScroll(scroll.getItemId()) && !GameConstants.isChaosScroll(scroll.getItemId()) && !GameConstants.isCleanSlate(scroll.getItemId()) && !GameConstants.isEquipScroll(scroll.getItemId()) && !GameConstants.isPotentialScroll(scroll.getItemId()) && !ii.canScroll(scroll.getItemId(), toScroll.getItemId()):
            return False
        if GameConstants.isAccessoryScroll(scroll.getItemId()) && !GameConstants.isAccessory(toScroll.getItemId()):
            return False
        if scroll.getQuantity() <= 0:
            return False
        if legendarySpirit && vegas == 0 && chr.getSkillLevel(SkillFactory.getSkill(1003)) <= 0 && chr.getSkillLevel(SkillFactory.getSkill(10001003)) <= 0 && chr.getSkillLevel(SkillFactory.getSkill(20001003)) <= 0 && chr.getSkillLevel(SkillFactory.getSkill(20011003)) <= 0 && chr.getSkillLevel(SkillFactory.getSkill(30001003)) <= 0:
            AutobanManager.getInstance().addPoints(c, 50, 120000, "Using the Skill 'Legendary Spirit' without having it.")
            return False
        scrolled = ii.scrollEquipWithId(toScroll, scroll, whiteScroll, chr, vegas, checkIfGM)
        IEquip.ScrollResult scrollSuccess
        if scrolled is None:
            scrollSuccess = IEquip.ScrollResult.CURSE
        elif scrolled.getLevel() > oldLevel || scrolled.getEnhance() > oldEnhance || scrolled.getState() > oldState || scrolled.getFlag() > oldFlag:
            scrollSuccess = IEquip.ScrollResult.SUCCESS
        elif GameConstants.isCleanSlate(scroll.getItemId()) && scrolled.getUpgradeSlots() > oldSlots:
            scrollSuccess = IEquip.ScrollResult.SUCCESS
        else:
            scrollSuccess = IEquip.ScrollResult.FAIL
        chr.getInventory(MapleInventoryType.USE).removeItem(scroll.getPosition(), 1, False)
        if whiteScroll:
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, wscroll.getPosition(), 1, False, False)
        if scrollSuccess == IEquip.ScrollResult.CURSE:
            c.getSession().write(MaplePacketCreator.scrolledItem(scroll, toScroll, True, False))
            if dst < 0:
                chr.getInventory(MapleInventoryType.EQUIPPED).removeItem(toScroll.getPosition())
            else:
                chr.getInventory(MapleInventoryType.EQUIP).removeItem(toScroll.getPosition())
        elif vegas == 0:
            c.getSession().write(MaplePacketCreator.scrolledItem(scroll, scrolled, False, False))
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.getScrollEffect(c.getPlayer().getId(), scrollSuccess, legendarySpirit), vegas == 0)
        if dst < 0 && (scrollSuccess == IEquip.ScrollResult.SUCCESS || scrollSuccess == IEquip.ScrollResult.CURSE) && vegas == 0:
            chr.equipChanged()
        return True

    def UseCatchItem(self, slea: Any, c: Any, chr: Any) -> None:
        c.getPlayer().updateTick(slea.readInt())
        slot = slea.readShort()
        itemid = slea.readInt()
        mob = chr.getMap().getMonsterByOid(slea.readInt())
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is not None && toUse.getQuantity() > 0 && toUse.getItemId() == itemid && mob is not None:
            # switch (itemid):
                # case 2270004:
                    map = chr.getMap()
                    if mob.getHp() <= mob.getMobMaxHp() / 2:
                        map.broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 1))
                        map.killMonster(mob, chr, True, False, 0)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemid, 1, False, False)
                        MapleInventoryManipulator.addById(c, 4001169, 1, 0)
                        break
                    map.broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 0))
                    chr.dropMessage(5, "怪物的生命力还很强大,无法捕捉.")
                    break
                # case 2270002:
                    map = chr.getMap()
                    if mob.getHp() <= mob.getMobMaxHp() / 2:
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 1))
                        map.killMonster(mob, chr, True, False, 0)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemid, 1, False, False)
                        c.getPlayer().setAPQScore(c.getPlayer().getAPQScore() + 1)
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.updateAriantPQRanking(c.getPlayer().getName(), c.getPlayer().getAPQScore(), False))
                        break
                    c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 0))
                    c.sendPacket(MaplePacketCreator.catchMob(mob.getId(), itemid, 0))
                    break
                # case 2270000:
                    if mob.getId() != 9300101:
                        break
                    map = c.getPlayer().getMap()
                    map.broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 1))
                    map.killMonster(mob, chr, True, False, 0)
                    MapleInventoryManipulator.addById(c, 1902000, 1, None, 0)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemid, 1, False, False)
                    break
                # case 2270003:
                    if mob.getId() != 9500320:
                        break
                    map = c.getPlayer().getMap()
                    if mob.getHp() <= mob.getMobMaxHp() / 2:
                        map.broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 1))
                        map.killMonster(mob, chr, True, False, 0)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemid, 1, False, False)
                        break
                    map.broadcastMessage(MaplePacketCreator.catchMonster(mob.getId(), itemid, 0))
                    chr.dropMessage(5, "怪物的生命力还很强大,无法捕捉.")
                    break
        c.getSession().write(MaplePacketCreator.enableActions())

    def UseMountFood(self, slea: Any, c: Any, chr: Any) -> None:
        c.getPlayer().updateTick(slea.readInt())
        slot = slea.readShort()
        itemid = slea.readInt()
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        mount = chr.getMount()
        if itemid / 10000 == 226 && toUse is not None && toUse.getQuantity() > 0 && toUse.getItemId() == itemid && mount is not None:
            fatigue = mount.getFatigue()
            levelup = False
            mount.setFatigue((byte)(-30))
            if fatigue > 0:
                mount.increaseExp()
                level = mount.getLevel()
                if mount.getExp() >= GameConstants.getMountExpNeededForLevel(level + 1) && level < 31:
                    mount.setLevel((byte)(level + 1))
                    levelup = True
            chr.getMap().broadcastMessage(MaplePacketCreator.updateMount(chr, levelup))
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
        c.getSession().write(MaplePacketCreator.enableActions())

    def UsePenguinBox(self, slea: Any, c: Any) -> None:
        gift = []
        slot = slea.readShort()
        item = slea.readInt()
        toUse = c.getPlayer().getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse.getItemId() != item:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getInventory(MapleInventoryType.EQUIP).getNumFreeSlot() <= 2:
            c.getPlayer().dropMessage(1, "您无法获得物品\r\n背包装备栏剩余栏位不足\r\n装备栏最少留下3个空格")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getInventory(MapleInventoryType.USE).getNumFreeSlot() <= 2:
            c.getPlayer().dropMessage(1, "您无法获得物品\r\n背包消耗栏剩余栏位不足\r\n消耗栏最少留下3个空格")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getInventory(MapleInventoryType.SETUP).getNumFreeSlot() <= 2:
            c.getPlayer().dropMessage(1, "您无法获得物品\r\n背包设置栏剩余栏位不足\r\n设置栏最少留下3个空格")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getInventory(MapleInventoryType.ETC).getNumFreeSlot() <= 2:
            c.getPlayer().dropMessage(1, "您无法获得物品\r\n背包其他栏剩余栏位不足\r\n其他栏最少留下3个空格")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getInventory(MapleInventoryType.CASH).getNumFreeSlot() <= 2:
            c.getPlayer().dropMessage(1, "您无法获得物品\r\n背包特殊栏剩余栏位不足\r\n特殊栏最少留下3个空格")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        # switch (item):
            # case 2022570:
                gift.add(1302119)
                gift.add(1312045)
                gift.add(1322073)
                break
            # case 2022571:
                gift.add(1372053)
                gift.add(1382070)
                break
            # case 2022572:
                gift.add(1462066)
                gift.add(1452073)
                break
            # case 2022573:
                gift.add(1332088)
                gift.add(1472089)
                break
            # case 2022574:
                gift.add(1482037)
                gift.add(1492038)
                break
            # case 2022575:
                gift.add(1040145)
                gift.add(1041148)
                break
            # case 2022576:
                gift.add(1050155)
                gift.add(1051191)
                break
            # case 2022577:
                gift.add(1040146)
                gift.add(1041149)
                break
            # case 2022578:
                gift.add(1040147)
                gift.add(1041150)
                break
            # case 2022579:
                gift.add(1052208)
                break
            # case 2022580:
                gift.add(1072399)
                gift.add(1060134)
                gift.add(1061156)
                break
            # case 2022581:
                gift.add(1072400)
                break
            # case 2022582:
                gift.add(1072401)
                gift.add(1060135)
                gift.add(1061157)
                break
            # case 2022583:
                gift.add(1072402)
                gift.add(1060136)
                gift.add(1061158)
                break
            # case 2022336:
                NPCScriptManager.getInstance().start(c, 9900004, 6666)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022670:
                NPCScriptManager.getInstance().start(c, 9900004, 6000)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022613:
                NPCScriptManager.getInstance().start(c, 9900004, 6001)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022615:
                NPCScriptManager.getInstance().start(c, 9900004, 6002)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022618:
                NPCScriptManager.getInstance().start(c, 9900004, 6003)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022465:
                NPCScriptManager.getInstance().start(c, 9900004, 6004)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022466:
                NPCScriptManager.getInstance().start(c, 9900004, 6005)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022467:
                NPCScriptManager.getInstance().start(c, 9900004, 6006)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2022468:
                NPCScriptManager.getInstance().start(c, 9900004, 6007)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
        if gift == 0:
            if (c.getPlayer().isGM()) {}
        else:
            rand = ThreadLocalRandom.current().nextInt(gift)
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
            MapleInventoryManipulator.addById(c, gift.get(rand), 1, 0)
            gift.clear()
        c.getSession().write(MaplePacketCreator.enableActions())

    def SunziBF(self, slea: Any, c: Any) -> None:
        slea.readInt()
        slot = slea.readShort()
        itemid = slea.readInt()
        ii = MapleItemInformationProvider.getInstance()
        item = c.getPlayer().getInventory(MapleInventoryType.USE).getItem(slot)
        if item is None || item.getItemId() != itemid || c.getPlayer().getLevel() > 255:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        expGained = ii.getExpCache(itemid) * c.getChannelServer().getExpRate()
        c.getPlayer().gainExp(expGained, True, False, False)
        c.getSession().write(MaplePacketCreator.enableActions())
        MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)

    def UseSummonBag(self, slea: Any, c: Any, chr: Any) -> None:
        if !chr.isAlive():
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if chr.getMapId() >= 910000000 && chr.getMapId() <= 910000022:
            c.getSession().write(MaplePacketCreator.enableActions())
            c.getPlayer().dropMessage(5, "市场无法使用召唤包.")
            return
        c.getPlayer().updateTick(slea.readInt())
        slot = slea.readShort()
        itemId = slea.readInt()
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is not None && toUse.getQuantity() >= 1 && toUse.getItemId() == itemId:
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
            if c.getPlayer().isGM() || !FieldLimitType.SummoningBag.check(chr.getMap().getFieldLimit()):
                toSpawn = MapleItemInformationProvider.getInstance().getSummonMobs(itemId)
                if toSpawn is None:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                type = 0
                for i in range(toSpawn):
                    if Randomizer.nextInt(99) <= toSpawn.get(i).getRight():
                        ht = MapleLifeFactory.getMonster(toSpawn.get(i).getLeft())
                        chr.getMap().spawnMonster_sSack(ht, chr.getPosition(), type)
        c.getSession().write(MaplePacketCreator.enableActions())

    def UseTreasureChest(self, slea: Any, c: Any, chr: Any) -> None:
        slot = slea.readShort()
        itemid = slea.readInt()
        useCash = slea.readByte() > 0
        toUse = chr.getInventory(MapleInventoryType.ETC).getItem(slot)
        if toUse is None || toUse.getQuantity() <= 0 || toUse.getItemId() != itemid:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        ii = MapleItemInformationProvider.getInstance()
        reward = 0
        keyIDforRemoval = 0
        box = None
        key = None
        price = 0
        # switch (toUse.getItemId()):
            # case 4280000:
                reward = RandomRewards.getInstance().getGoldBoxReward()
                keyIDforRemoval = 5490000
                box = "永恒的谜之蛋"
                key = "永恒的热度"
                price = 800
                break
            # case 4280001:
                reward = RandomRewards.getInstance().getSilverBoxReward()
                keyIDforRemoval = 5490001
                box = "重生的谜之蛋"
                key = "重生的热度"
                price = 500
                break
            # default:
                return
        amount = 1
        # switch (reward):
            # case 2000004:
                amount = 200
                break
            # case 2000005:
                amount = 100
                break
        if useCash && chr.getCSPoints(2) < price:
            chr.dropMessage(1, "抵用券不足" + price + "点")
            c.getSession().write(MaplePacketCreator.enableActions())
        elif chr.getInventory(MapleInventoryType.CASH).countById(keyIDforRemoval) < 0:
            chr.dropMessage(1, "孵化" + box + "需要" + key + "，请到商城购买！")
            c.getSession().write(MaplePacketCreator.enableActions())
        elif chr.getInventory(MapleInventoryType.CASH).countById(keyIDforRemoval) > 0 || (useCash && chr.getCSPoints(2) > price):
            item = MapleInventoryManipulator.addbyId_Gachapon(c, reward, amount)
            if item is None:
                chr.dropMessage(1, "孵化失败，请重试一次。\r\n你的背包可能满了")
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.ETC, slot, 1, True)
            if useCash:
                chr.modifyCSPoints(2, -price, True)
            else:
                MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, keyIDforRemoval, 1, True, False)
            c.getSession().write(MaplePacketCreator.getShowItemGain(reward, amount, True))
            rareness = GameConstants.gachaponRareItem(item.getItemId())
            if rareness > 0 || reward > 0:
                World.Broadcast.broadcastMessage(MaplePacketCreator.getGachaponMega(c.getPlayer().getName(), " : 从" + box + "中获得{" + ii.getName(item.getItemId()) + "}！大家一起恭喜他（她）吧！！！！", item, rareness, c.getChannel()))
        else:
            chr.dropMessage(5, "孵化" + box + "失败\r\n请检查是否有" + key + "\r\n或者抵用卷是否有" + price + "点。")
            c.getSession().write(MaplePacketCreator.enableActions())

    def UseCashItem(self, slea: Any, c: Any) -> None:
        slot = slea.readShort()
        itemId = slea.readInt()
        toUse = c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(slot)
        if toUse is None || toUse.getItemId() != itemId || toUse.getQuantity() < 1:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        used = False
        cc = False
        Label_10360:
            # switch (itemId):
                # case 5042000:
                    c.getPlayer().changeMap(701000200)
                    used = True
                    break
                # case 5042001:
                    used = True
                    break
                # case 5043000:
                    questid = slea.readShort()
                    npcid = slea.readInt()
                    quest = MapleQuest.getInstance(questid)
                    if c.getPlayer().getQuest(quest).getStatus() == 1 && quest.canComplete(c.getPlayer(), npcid):
                        mapId = MapleLifeFactory.getNPCLocation(npcid)
                        if mapId != -1:
                            map = c.getChannelServer().getMapFactory().getMap(mapId)
                            if map.containsNPC(npcid) && !FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) && !FieldLimitType.VipRock.check(map.getFieldLimit()) && c.getPlayer().getEventInstance() is None:
                                c.getPlayer().changeMap(map, map.getPortal(0))
                            used = True
                        else:
                            c.getPlayer().dropMessage(1, "发生未知错误.")
                        break
                    break
                # case 5040000:
                # case 5040001:
                # case 5041000:
                    if slea.readByte() == 0:
                        target = c.getChannelServer().getMapFactory().getMap(slea.readInt())
                        if target is not None && ((itemId == 5041000 && c.getPlayer().isRockMap(target.getId())) || (itemId != 5041000 && c.getPlayer().isRegRockMap(target.getId()))) && !FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) && !FieldLimitType.VipRock.check(target.getFieldLimit()) && c.getPlayer().getEventInstance() is None:
                            c.getPlayer().changeMap(target, target.getPortal(0))
                            used = True
                        break
                    victim = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
                    if victim is not None && !victim.isGM() && c.getPlayer().getEventInstance() is None && victim.getEventInstance() is None:
                        if !FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) && !FieldLimitType.VipRock.check(c.getChannelServer().getMapFactory().getMap(victim.getMapId()).getFieldLimit()) && (itemId == 5041000 || victim.getMapId() / 100000000 == c.getPlayer().getMapId() / 100000000):
                            c.getPlayer().changeMap(victim.getMap(), victim.getMap().findClosestSpawnpoint(victim.getPosition()))
                            used = True
                    else:
                        c.getPlayer().dropMessage(1, "在此频道未找到该玩家.")
                    break
                # case 5050000:
                    statupdate = new ArrayList<Pair<MapleStat, Integer>>(2)
                    apto = slea.readInt()
                    apfrom = slea.readInt()
                    if apto == apfrom:
                        break
                    job = c.getPlayer().getJob()
                    playerst = c.getPlayer().getStat()
                    used = True
                    if apfrom == 8192 && apto != 32768:
                        c.sendPacket(MaplePacketCreator.enableActions())
                        return
                    if apfrom == 32768 && apto != 8192:
                        c.sendPacket(MaplePacketCreator.enableActions())
                        return
                    # switch (apto):
                        # case 256:
                            if playerst.getStr() >= 999:
                                used = False
                                break
                            break
                        # case 512:
                            if playerst.getDex() >= 999:
                                used = False
                                break
                            break
                        # case 1024:
                            if playerst.getInt() >= 999:
                                used = False
                                break
                            break
                        # case 2048:
                            if playerst.getLuk() >= 999:
                                used = False
                                break
                            break
                    # switch (apfrom):
                        # case 256:
                            if playerst.getStr() <= 4:
                                used = False
                                break
                            break
                        # case 512:
                            if playerst.getDex() <= 4:
                                used = False
                                break
                            break
                        # case 1024:
                            if playerst.getInt() <= 4:
                                used = False
                                break
                            break
                        # case 2048:
                            if playerst.getLuk() <= 4:
                                used = False
                                break
                            break
                    if used:
                        # switch (apto):
                            # case 256:
                                toSet = playerst.getStr() + 1
                                playerst.setStr(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.STR, toSet))
                                break
                            # case 512:
                                toSet = playerst.getDex() + 1
                                playerst.setDex(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.DEX, toSet))
                                break
                            # case 1024:
                                toSet = playerst.getInt() + 1
                                playerst.setInt(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.INT, toSet))
                                break
                            # case 2048:
                                toSet = playerst.getLuk() + 1
                                playerst.setLuk(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.LUK, toSet))
                        # switch (apfrom):
                            # case 256:
                                toSet = playerst.getStr() - 1
                                playerst.setStr(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.STR, toSet))
                                break
                            # case 512:
                                toSet = playerst.getDex() - 1
                                playerst.setDex(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.DEX, toSet))
                                break
                            # case 1024:
                                toSet = playerst.getInt() - 1
                                playerst.setInt(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.INT, toSet))
                                break
                            # case 2048:
                                toSet = playerst.getLuk() - 1
                                playerst.setLuk(toSet)
                                statupdate.add(new Pair<MapleStat, Integer>(MapleStat.LUK, toSet))
                        c.getSession().write(MaplePacketCreator.updatePlayerStats(statupdate, True, c.getPlayer().getJob()))
                        break
                    break
                # case 5050001:
                # case 5050002:
                # case 5050003:
                # case 5050004:
                    skill1 = slea.readInt()
                    skill2 = slea.readInt()
                    skillSPTo = SkillFactory.getSkill(skill1)
                    skillSPFrom = SkillFactory.getSkill(skill2)
                    if skillSPTo.isBeginnerSkill():
                        break
                    if skillSPFrom.isBeginnerSkill():
                        break
                    if c.getPlayer().getSkillLevel(skillSPTo) + 1 <= skillSPTo.getMaxLevel() && c.getPlayer().getSkillLevel(skillSPFrom) > 0:
                        c.getPlayer().changeSkillLevel(skillSPFrom, (byte)(c.getPlayer().getSkillLevel(skillSPFrom) - 1), c.getPlayer().getMasterLevel(skillSPFrom))
                        c.getPlayer().changeSkillLevel(skillSPTo, (byte)(c.getPlayer().getSkillLevel(skillSPTo) + 1), c.getPlayer().getMasterLevel(skillSPTo))
                        used = True
                        break
                    break
                # case 5060000:
                    daojuquming = None
                    zhuangbeicao = slea.readShort()
                    daojuquming = c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).getItem(zhuangbeicao)
                    c.getSession().write(MaplePacketCreator.serverNotice(5, "请将道具直接点在你需要刻名的装备上."))
                    if daojuquming is None:
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    daojuquming.setOwner(c.getPlayer().getName())
                    c.getSession().write(MaplePacketCreator.updateEquipSlot(daojuquming))
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getSession().write(MaplePacketCreator.serverNotice(5, "道具刻名成功~！"))
                    break
                # case 5080000:
                # case 5080001:
                # case 5080002:
                # case 5080003:
                    love = MapleLove(c.getPlayer(), c.getPlayer().getPosition(), c.getPlayer().getMap().getFootholds().findBelow(c.getPlayer().getPosition()).getId(), slea.readMapleAsciiString(), itemId)
                    c.getPlayer().getMap().spawnLove(love)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    break
                # case 5201004:
                    DDcount = 20
                    c.getPlayer().gainBeans(DDcount)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getPlayer().dropMessage(5, "成功充值20豆豆！！")
                    c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), DDcount))
                    cc = True
                    break
                # case 5201005:
                    DDcount = 50
                    c.getPlayer().gainBeans(DDcount)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getPlayer().dropMessage(5, "成功充值50豆豆！！")
                    c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), DDcount))
                    cc = True
                    c.getPlayer().saveToDB(True, True)
                    break
                # case 5201001:
                    DDcount = 500
                    c.getPlayer().gainBeans(DDcount)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getPlayer().dropMessage(5, "成功充值500豆豆！！")
                    c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), DDcount))
                    cc = True
                    c.getPlayer().saveToDB(True, True)
                    break
                # case 5201000:
                    DDcount = 2000
                    c.getPlayer().gainBeans(DDcount)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getPlayer().dropMessage(5, "成功充值2000豆豆！！")
                    c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), DDcount))
                    cc = True
                    c.getPlayer().saveToDB(True, True)
                    break
                # case 5201002:
                    DDcount = 3000
                    c.getPlayer().gainBeans(DDcount)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                    c.getPlayer().dropMessage(5, "成功充值3000豆豆！！")
                    c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), DDcount))
                    cc = True
                    c.getPlayer().saveToDB(True, True)
                    break
                # case 5520000:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && !ItemFlag.KARMA_EQ.check(item.getFlag()) && !ItemFlag.KARMA_USE.check(item.getFlag()) && ((itemId == 5520000 && MapleItemInformationProvider.getInstance().isKarmaEnabled(item.getItemId())) || MapleItemInformationProvider.getInstance().isPKarmaEnabled(item.getItemId())):
                        flag = item.getFlag()
                        if type == MapleInventoryType.EQUIP:
                            flag |= ItemFlag.KARMA_EQ.getValue()
                        else:
                            flag |= ItemFlag.KARMA_USE.getValue()
                        flag &= (byte)~ItemFlag.UNTRADEABLE.getValue()
                        item.setFlag(flag)
                        c.getPlayer().forceReAddItem_Flag(item, type)
                        used = True
                        break
                    break
                # case 5570000:
                    slea.readInt()
                    item2 = c.getPlayer().getInventory(MapleInventoryType.EQUIP).getItem(slea.readInt())
                    if item2 is None:
                        break
                    if GameConstants.canHammer(item2.getItemId()) && MapleItemInformationProvider.getInstance().getSlots(item2.getItemId()) > 0 && item2.getViciousHammer() <= 2:
                        item2.setViciousHammer((byte)(item2.getViciousHammer() + 1))
                        item2.setUpgradeSlots((byte)(item2.getUpgradeSlots() + 1))
                        c.getPlayer().forceReAddItem(item2, MapleInventoryType.EQUIP)
                        used = True
                        cc = True
                        break
                    c.getPlayer().dropMessage(5, "你不得在这个物品上使用它.")
                    cc = True
                    break
                # case 5060001:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && item.getExpiration() == -1:
                        flag = item.getFlag()
                        flag |= ItemFlag.LOCK.getValue()
                        item.setFlag(flag)
                        c.getPlayer().forceReAddItem_Flag(item, type)
                        used = True
                        break
                    break
                # case 5061000:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && item.getExpiration() == -1:
                        flag = item.getFlag()
                        flag |= ItemFlag.LOCK.getValue()
                        item.setFlag(flag)
                        item.setExpiration(int(time.time() * 1000) + 604800000)
                        c.getPlayer().forceReAddItem_Flag(item, type)
                        used = True
                        break
                    break
                # case 5061001:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && item.getExpiration() == -1:
                        flag2 = item.getFlag()
                        flag2 |= ItemFlag.LOCK.getValue()
                        item.setFlag(flag2)
                        days = 0
                        # switch (itemId):
                            # case 5061001:
                                days = 30
                                break
                        if days > 0:
                            item.setExpiration(int(time.time() * 1000) + days * 24 * 60 * 60 * 1000)
                        c.getPlayer().forceUpdateItem(type, item)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                        c.getPlayer().dropMessage(5, "使用封印之锁 物品ID: " + itemId + " 天数: " + days)
                        c.getSession().write(MaplePacketCreator.enableActions())
                        break
                    c.getPlayer().dropMessage(1, "使用道具出现错误.")
                    break
                # case 5061002:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && item.getExpiration() == -1:
                        flag2 = item.getFlag()
                        flag2 |= ItemFlag.LOCK.getValue()
                        item.setFlag(flag2)
                        days = 0
                        # switch (itemId):
                            # case 5061002:
                                days = 90
                                break
                        if days > 0:
                            item.setExpiration(int(time.time() * 1000) + days * 24 * 60 * 60 * 1000)
                        c.getPlayer().forceUpdateItem(type, item)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                        c.getPlayer().dropMessage(5, "使用封印之锁 物品ID: " + itemId + " 天数: " + days)
                        c.getSession().write(MaplePacketCreator.enableActions())
                        break
                    c.getPlayer().dropMessage(1, "使用道具出现错误.")
                    break
                # case 5061003:
                    type = MapleInventoryType.getByType(slea.readInt())
                    item = c.getPlayer().getInventory(type).getItem(slea.readInt())
                    if item is not None && item.getExpiration() == -1:
                        flag2 = item.getFlag()
                        flag2 |= ItemFlag.LOCK.getValue()
                        item.setFlag(flag2)
                        days = 0
                        # switch (itemId):
                            # case 5061003:
                                days = 365
                                break
                        if days > 0:
                            item.setExpiration(int(time.time() * 1000) + days * 24 * 60 * 60 * 1000)
                        c.getPlayer().forceUpdateItem(type, item)
                        MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, itemId, 1, True, False)
                        c.getPlayer().dropMessage(5, "使用封印之锁 物品ID: " + itemId + " 天数: " + days)
                        c.getSession().write(MaplePacketCreator.enableActions())
                        break
                    c.getPlayer().dropMessage(1, "使用道具出现错误.")
                    break
                # case 5070000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    sb = ""
                    addMedalString(c.getPlayer(), sb)
                    sb.append(c.getPlayer().getName())
                    sb.append(" : ")
                    sb.append(message)
                    ear = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(2, sb))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(2, sb))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5071000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    ear2 = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    sb2 = ""
                    addMedalString(c.getPlayer(), sb2)
                    sb2.append(c.getPlayer().getName())
                    sb2.append(" : ")
                    sb2.append(message)
                    if c.getPlayer().isPlayer():
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(2, sb2))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(2, sb2))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5077000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    numLines = slea.readByte()
                    if numLines > 3:
                        return
                    messages = []
                    for i in range(numLines):
                        message2 = slea.readMapleAsciiString()
                        if message2 > 65:
                            break
                        messages.add(c.getPlayer().getName() + " : " + message2)
                    ear3 = slea.readByte() > 0
                    if (c.getPlayer().isPlayer() && messages.find("幹") != -1) || messages.find("豬") != -1 || messages.find("笨") != -1 || messages.find("靠") != -1 || messages.find("腦包") != -1 || messages.find("腦") != -1 || messages.find("智障") != -1 || messages.find("白目") != -1 || messages.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.tripleSmega(messages, ear3, c.getChannel()).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + messages)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.tripleSmega(messages, ear3, c.getChannel()).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + messages)
                    used = True
                    break
                # case 5073000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    sb = ""
                    addMedalString(c.getPlayer(), sb)
                    sb.append(c.getPlayer().getName())
                    sb.append(" : ")
                    sb.append(message)
                    ear = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5074000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    sb = ""
                    addMedalString(c.getPlayer(), sb)
                    sb.append(c.getPlayer().getName())
                    sb.append(" : ")
                    sb.append(message)
                    ear = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(12, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(12, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5072000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須要10等以上才能使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    sb = ""
                    addMedalString(c.getPlayer(), sb)
                    sb.append(c.getPlayer().getName())
                    sb.append(" : ")
                    sb.append(message)
                    ear = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, c.getChannel(), sb, ear).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5076000:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    message = slea.readMapleAsciiString()
                    if message > 65:
                        break
                    sb = ""
                    addMedalString(c.getPlayer(), sb)
                    sb.append(c.getPlayer().getName())
                    sb.append(" : ")
                    sb.append(message)
                    ear = slea.readByte() > 0
                    item3 = None
                    if slea.readByte() == 1:
                        invType = slea.readInt()
                        pos = slea.readInt()
                        item3 = c.getPlayer().getInventory(MapleInventoryType.getByType(invType)).getItem(pos)
                    if (c.getPlayer().isPlayer() && message.find("幹") != -1) || message.find("豬") != -1 || message.find("笨") != -1 || message.find("靠") != -1 || message.find("腦包") != -1 || message.find("腦") != -1 || message.find("智障") != -1 || message.find("白目") != -1 || message.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.itemMegaphone(sb, ear, c.getChannel(), item3).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.itemMegaphone(sb, ear, c.getChannel(), item3).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + message)
                    used = True
                    break
                # case 5075000:
                # case 5075001:
                # case 5075002:
                    c.getPlayer().dropMessage(5, "没有mapletvs广播消息.")
                    break
                # case 5075003:
                # case 5075004:
                # case 5075005:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必須等級10級以上才可以使用.")
                        break
                    tvType = itemId % 10
                    if tvType == 3:
                        slea.readByte()
                    ear2 = tvType != 1 && tvType != 2 && slea.readByte() > 1
                    victim2 = (tvType == 1 || tvType == 4) ? None : c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
                    if tvType == 0 || tvType == 3:
                        victim2 = None
                    elif victim2 is None:
                        c.getPlayer().dropMessage(1, "这个角色不是在频道里.")
                        break
                    message3 = slea.readMapleAsciiString()
                    World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, c.getChannel(), c.getPlayer().getName() + " : " + message3, ear2).encode("utf-8"))
                    break
                # case 5090000:
                # case 5090100:
                    sendTo = slea.readMapleAsciiString()
                    msg = slea.readMapleAsciiString()
                    c.getPlayer().sendNote(sendTo, msg)
                    used = True
                    break
                # case 5100000:
                    c.getPlayer().getMap().broadcastMessage(MTSCSPacket.playCashSong(5100000, c.getPlayer().getName()))
                    used = True
                    break
                # case 5152049:
                # case 5152100:
                # case 5152101:
                # case 5152102:
                # case 5152103:
                # case 5152104:
                # case 5152105:
                # case 5152106:
                # case 5152107:
                    chr = c.getPlayer()
                    color = (itemId - 5152100) * 100
                    if chr.isGM():
                        print("使用一次性隐形眼镜 - 道具: " + itemId + " 颜色: " + color)
                    if color >= 0:
                        changeFace(chr, color)
                        used = True
                        break
                    chr.dropMessage(1, "使用一次性隐形眼镜出现错误.")
                    break
                # case 5190000:
                # case 5190001:
                # case 5190002:
                # case 5190003:
                # case 5190004:
                # case 5190005:
                # case 5190006:
                # case 5190007:
                # case 5190008:
                    uniqueid = slea.readLong()
                    pet = c.getPlayer().getPet(0)
                    slo = 0
                    if pet is None:
                        break
                    if pet.getUniqueId() != uniqueid:
                        pet = c.getPlayer().getPet(1)
                        slo = 1
                        if pet is None:
                            break
                        if pet.getUniqueId() != uniqueid:
                            pet = c.getPlayer().getPet(2)
                            slo = 2
                            if pet is None:
                                break
                            if pet.getUniqueId() != uniqueid:
                                break
                    final MaplePet.PetFlag zz = MaplePet.PetFlag.getByAddId(itemId)
                    if zz is not None && !zz.check(pet.getFlags()):
                        pet.setFlags(pet.getFlags() | zz.getValue())
                        c.getSession().write(PetPacket.updatePet(pet, c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
                        c.getPlayer().getClient().getSession().write(PetPacket.petStatUpdate(c.getPlayer()))
                        c.getSession().write(MaplePacketCreator.enableActions())
                        c.getSession().write(MTSCSPacket.changePetFlag(uniqueid, True, zz.getValue()))
                        used = True
                        break
                    break
                # case 5191000:
                # case 5191001:
                # case 5191002:
                # case 5191003:
                # case 5191004:
                    uniqueid = slea.readLong()
                    pet = c.getPlayer().getPet(0)
                    slo = 0
                    if pet is None:
                        break
                    if pet.getUniqueId() != uniqueid:
                        pet = c.getPlayer().getPet(1)
                        slo = 1
                        if pet is None:
                            break
                        if pet.getUniqueId() != uniqueid:
                            pet = c.getPlayer().getPet(2)
                            slo = 2
                            if pet is None:
                                break
                            if pet.getUniqueId() != uniqueid:
                                break
                    final MaplePet.PetFlag zz = MaplePet.PetFlag.getByDelId(itemId)
                    if zz is not None && zz.check(pet.getFlags()):
                        pet.setFlags(pet.getFlags() - zz.getValue())
                        c.getSession().write(PetPacket.updatePet(pet, c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
                        c.getSession().write(MaplePacketCreator.enableActions())
                        c.getSession().write(MTSCSPacket.changePetFlag(uniqueid, False, zz.getValue()))
                        used = True
                        break
                    break
                # case 5170000:
                    pet2 = c.getPlayer().getPet(0)
                    slo2 = 0
                    if pet2 is None:
                        break
                    nName = slea.readMapleAsciiString()
                    pet2.setName(nName)
                    c.getSession().write(PetPacket.updatePet(pet2, c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet2.getInventoryPosition()), True))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    c.getPlayer().getMap().broadcastMessage(MTSCSPacket.changePetName(c.getPlayer(), nName, slo2))
                    used = True
                    break
                # case 5240000:
                # case 5240001:
                # case 5240002:
                # case 5240003:
                # case 5240004:
                # case 5240005:
                # case 5240006:
                # case 5240007:
                # case 5240008:
                # case 5240009:
                # case 5240010:
                # case 5240011:
                # case 5240012:
                # case 5240013:
                # case 5240014:
                # case 5240015:
                # case 5240016:
                # case 5240017:
                # case 5240018:
                # case 5240019:
                # case 5240020:
                # case 5240021:
                # case 5240022:
                # case 5240023:
                # case 5240024:
                # case 5240025:
                # case 5240026:
                # case 5240027:
                # case 5240028:
                    pet2 = c.getPlayer().getPet(0)
                    if pet2 is None:
                        break
                    if !pet2.canConsume(itemId):
                        pet2 = c.getPlayer().getPet(1)
                        if pet2 is None:
                            break
                        if !pet2.canConsume(itemId):
                            pet2 = c.getPlayer().getPet(2)
                            if pet2 is None:
                                break
                            if !pet2.canConsume(itemId):
                                break
                    petindex = c.getPlayer().getPetIndex(pet2)
                    pet2.setFullness(100)
                    if pet2.getCloseness() < 30000:
                        if pet2.getCloseness() + 100 > 30000:
                            pet2.setCloseness(30000)
                        else:
                            pet2.setCloseness(pet2.getCloseness() + 100)
                        if pet2.getCloseness() >= GameConstants.getClosenessNeededForLevel(pet2.getLevel() + 1):
                            pet2.setLevel(pet2.getLevel() + 1)
                            c.getSession().write(PetPacket.showOwnPetLevelUp(c.getPlayer().getPetIndex(pet2)))
                            c.getPlayer().getMap().broadcastMessage(PetPacket.showPetLevelUp(c.getPlayer(), petindex))
                    c.getSession().write(PetPacket.updatePet(pet2, c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet2.getInventoryPosition()), True))
                    c.getPlayer().getMap().broadcastMessage(c.getPlayer(), PetPacket.commandResponse(c.getPlayer().getId(), 1, petindex, True, True), True)
                    used = True
                    break
                # case 5230000:
                    itemSearch = slea.readInt()
                    hms = c.getChannelServer().searchMerchant(itemSearch)
                    if hms > 0:
                        c.getSession().write(MaplePacketCreator.getOwlSearched(itemSearch, hms))
                        used = True
                        break
                    c.getPlayer().dropMessage(1, "无法找到该项目.")
                    break
                # case 5280001:
                # case 5281000:
                # case 5281001:
                    bounds = Rectangle(c.getPlayer().getPosition().getX(), c.getPlayer().getPosition().getY(), 1, 1)
                    mist = MapleMist(bounds, c.getPlayer())
                    c.getPlayer().getMap().spawnMist(mist, 10000, True)
                    c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.getChatText(c.getPlayer().getId(), "Oh no, I farted!", False, 1))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    used = True
                    break
                # case 5320000:
                    name = slea.readMapleAsciiString()
                    otherName = slea.readMapleAsciiString()
                    unk = slea.readInt()
                    unk_2 = slea.readInt()
                    cardId = slea.readByte()
                    unk_3 = slea.readShort()
                    unk_4 = slea.readByte()
                    comm = Randomizer.rand(0, 6)
                    pcf = PredictCardFactory.getInstance()
                    final PredictCardFactory.PredictCard Card = pcf.getPredictCard(cardId)
                    final PredictCardFactory.PredictCardComment Comment = pcf.getPredictCardComment(comm)
                    if Card is None:
                        break
                    if Comment is None:
                        break
                    c.getPlayer().dropMessage(5, "爱情占卜成功。")
                    love2 = Randomizer.rand(1, Comment.score) + 5
                    c.getSession().write(MTSCSPacket.show塔罗牌(name, otherName, love2, cardId, Comment.effectType))
                    used = True
                    break
                # case 5370000:
                    if c.getPlayer().getMapId() / 1000000 == 109:
                        c.getPlayer().dropMessage(1, "请勿在活动地图使用黑板")
                        break
                    c.getPlayer().setChalkboard(slea.readMapleAsciiString())
                    break
                # case 5370001:
                    if c.getPlayer().getMapId() / 1000000 == 910:
                        c.getPlayer().setChalkboard(slea.readMapleAsciiString())
                        break
                    break
                # case 5390000:
                # case 5390001:
                # case 5390002:
                # case 5390003:
                # case 5390004:
                # case 5390005:
                # case 5390006:
                    if c.getPlayer().getLevel() < 10:
                        c.getPlayer().dropMessage(5, "必须等级10级以上才可以使用.")
                        break
                    if !c.getPlayer().getCheatTracker().canAvatarSmega2():
                        c.getPlayer().dropMessage(6, "很抱歉為了防止刷廣,所以你每10秒只能用一次.")
                        break
                    if c.getChannelServer().getMegaphoneMuteState():
                        c.getPlayer().dropMessage(5, "目前喇叭停止使用.")
                        break
                    text = slea.readMapleAsciiString()
                    if text > 55:
                        break
                    ear2 = slea.readByte() != 0
                    if (c.getPlayer().isPlayer() && text.find("幹") != -1) || text.find("豬") != -1 || text.find("笨") != -1 || text.find("靠") != -1 || text.find("腦包") != -1 || text.find("腦") != -1 || text.find("智障") != -1 || text.find("白目") != -1 || text.find("白吃") != -1:
                        c.getPlayer().dropMessage("說髒話是不禮貌的，請勿說髒話。")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if c.getPlayer().isPlayer():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.getAvatarMega(c.getPlayer(), c.getChannel(), itemId, text, ear2).encode("utf-8"))
                        print("[玩家廣播頻道 " + c.getPlayer().getName() + "] : " + text)
                    elif c.getPlayer().isGM():
                        World.Broadcast.broadcastSmega(MaplePacketCreator.getAvatarMega(c.getPlayer(), c.getChannel(), itemId, text, ear2).encode("utf-8"))
                        print("[ＧＭ廣播頻道 " + c.getPlayer().getName() + "] : " + text)
                    used = True
                    break
                # case 5450000:
                    MapleShopFactory.getInstance().getShop(61).sendShop(c)
                    used = True
                    break
                # case 5500001:
                # case 5500002:
                    item4 = c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).getItem(slea.readShort())
                    ii = MapleItemInformationProvider.getInstance()
                    days2 = 20
                    if item4 is not None && !GameConstants.isAccessory(item4.getItemId()) && item4.getExpiration() > -1 && !ii.isCash(item4.getItemId()) && int(time.time() * 1000) + 8640000000 > item4.getExpiration() + days2 * 24 * 60 * 60 * 1000:
                        change = True
                        for z in GameConstants.RESERVED:
                            if c.getPlayer().getName().find(z) != -1 || item4.getOwner().find(z) != -1:
                                change = False
                        if change:
                            item4.setExpiration(item4.getExpiration() + days2 * 24 * 60 * 60 * 1000)
                            c.getPlayer().forceReAddItem(item4, MapleInventoryType.EQUIPPED)
                            used = True
                        else:
                            c.getPlayer().dropMessage(1, "此装备无法使用.")
                        break
                    break
                # default:
                    # switch (itemId / 10000):
                        # case 512:
                            ii2 = MapleItemInformationProvider.getInstance()
                            msg = ii2.getMsg(itemId).replaceFirst("%s", c.getPlayer().getName()).replaceFirst("%s", slea.readMapleAsciiString())
                            c.getPlayer().getMap().startMapEffect(msg, itemId)
                            buff = ii2.getStateChangeItem(itemId)
                            if buff != 0:
                                for mChar in c.getPlayer().getMap().getCharactersThreadsafe():
                                    ii2.getItemEffect(buff).applyTo(mChar)
                            used = True
                            Label_10360 = None
                        # case 510:
                            c.getPlayer().getMap().startJukebox(c.getPlayer().getName(), itemId)
                            used = True
                            Label_10360 = None
                        # case 520:
                            mesars = MapleItemInformationProvider.getInstance().getMeso(itemId)
                            if mesars <= 0 || c.getPlayer().getMeso() >= Integer.MAX_VALUE - mesars:
                                Label_10360 = None
                            used = True
                            if random.random() > 0.1:
                                gainmes = Randomizer.nextInt(mesars)
                                c.getPlayer().gainMeso(gainmes, False)
                                c.getSession().write(MTSCSPacket.sendMesobagSuccess(gainmes))
                                Label_10360 = None
                            c.getSession().write(MTSCSPacket.sendMesobagFailed())
                            Label_10360 = None
                        # case 553:
                            UseRewardItem(slot, itemId, c, c.getPlayer())
                            Label_10360 = None
                        # default:
                            print("Unhandled CS item : " + itemId)
                            print(slea.toString(True))
                            Label_10360 = None
        if used:
            MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.CASH, slot, 1, False, True)
        c.getSession().write(MaplePacketCreator.enableActions())
        c.getSession().write(MaplePacketCreator.enableActions())
        if cc:
            if !c.getPlayer().isAlive() || c.getPlayer().getEventInstance() is not None || FieldLimitType.ChannelSwitch.check(c.getPlayer().getMap().getFieldLimit()):
                c.getPlayer().dropMessage(1, "刷新人物数据失败.")
                return
            c.getPlayer().dropMessage(5, "正在刷新人数据.请等待...")
            c.getPlayer().fakeRelog()

    def Pickup_Player(self, slea: Any, c: Any, chr: Any) -> None:
        if c.getPlayer().getPlayerShop() is not None || c.getPlayer().getConversation() > 0 || c.getPlayer().getTrade() is not None:
            return
        chr.updateTick(slea.readInt())
        slea.skip(1)
        Client_Reportedpos = slea.readPos()
        if chr is None || chr.getMap() is None:
            return
        ob = chr.getMap().getMapObject(slea.readInt(), MapleMapObjectType.ITEM)
        if ob is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        mapitem = ob
        lock = mapitem.getLock()
        lock.lock()
        try:
            if mapitem.isPickedUp():
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if mapitem.getOwner() != chr.getId() && ((!mapitem.isPlayerDrop() && mapitem.getDropType() == 0) || (mapitem.isPlayerDrop() && chr.getMap().getEverlast())):
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if !mapitem.isPlayerDrop() && mapitem.getDropType() == 1 && mapitem.getOwner() != chr.getId() && (chr.getParty() is None || chr.getParty().getMemberById(mapitem.getOwner()) is None):
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            Distance = Client_Reportedpos.distanceSq(mapitem.getPosition())
            if Distance > 2500.0:
                chr.getCheatTracker().registerOffense(CheatingOffense.全图吸物_客户端, str(Distance))
                World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[GM消息] " + chr.getName() + " ID: " + chr.getId() + " (等级 " + chr.getLevel() + ") 全屏捡物。地图ID: " + chr.getMapId() + " 范围: " + Distance).encode("utf-8"))
            elif chr.getPosition().distanceSq(mapitem.getPosition()) > 640000.0:
                chr.getCheatTracker().registerOffense(CheatingOffense.全图吸物_服务端)
                World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[GM消息] " + chr.getName() + " ID: " + chr.getId() + " (等级 " + chr.getLevel() + ") 全屏捡物。地图ID: " + chr.getMapId() + " 范围: " + Distance).encode("utf-8"))
            if mapitem.getMeso() > 0:
                if chr.getParty() is not None && mapitem.getOwner() != chr.getId():
                    toGive = []
                    for z in chr.getParty().getMembers():
                        m = chr.getMap().getCharacterById(z.getId())
                        if m is not None:
                            toGive.add(m)
                    for i in toGive:
                        i.gainMeso(mapitem.getMeso() / toGive + (i.getStat().hasPartyBonus ? ((int)(mapitem.getMeso() / 20.0)) : 0), True, True)
                else:
                    chr.gainMeso(mapitem.getMeso(), True, True)
                removeItem(chr, mapitem, ob)
            elif MapleItemInformationProvider.getInstance().isPickupBlocked(mapitem.getItem().getItemId()):
                c.getSession().write(MaplePacketCreator.enableActions())
                c.getPlayer().dropMessage(5, "这个道具无法捡取.")
            elif useItem(c, mapitem.getItemId()):
                removeItem(c.getPlayer(), mapitem, ob)
            elif MapleInventoryManipulator.checkSpace(c, mapitem.getItem().getItemId(), mapitem.getItem().getQuantity(), mapitem.getItem().getOwner()):
                if mapitem.getItem().getQuantity() >= 50 && GameConstants.isUpgradeScroll(mapitem.getItem().getItemId()):
                    c.setMonitored(True)
                if MapleInventoryManipulator.addFromDrop(c, mapitem.getItem(), True, mapitem.getDropper() instanceof MapleMonster):
                    removeItem(chr, mapitem, ob)
            else:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                c.getSession().write(MaplePacketCreator.enableActions())
        finally:
            lock.unlock()

    def Pickup_Pet(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        petz = c.getPlayer().getPetIndex(slea.readLong())
        pet = chr.getPet(petz)
        slea.skip(1)
        chr.updateTick(slea.readInt())
        Client_Reportedpos = slea.readPos()
        ob = chr.getMap().getMapObject(slea.readInt(), MapleMapObjectType.ITEM)
        if ob is None || pet is None:
            return
        mapitem = ob
        if mapitem.isPickedUp():
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return
        if mapitem.getOwner() != chr.getId() && mapitem.isPlayerDrop():
            return
        if mapitem.getOwner() != chr.getId() && ((!mapitem.isPlayerDrop() && mapitem.getDropType() == 0) || (mapitem.isPlayerDrop() && chr.getMap().getEverlast())):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if !mapitem.isPlayerDrop() && mapitem.getDropType() == 1 && mapitem.getOwner() != chr.getId() && (chr.getParty() is None || chr.getParty().getMemberById(mapitem.getOwner()) is None):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if mapitem.isPlayerDrop() && mapitem.getDropType() == 2 && mapitem.getOwner() == chr.getId():
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if mapitem.isPlayerDrop() && mapitem.getDropType() == 0 && mapitem.getOwner() == chr.getId() && mapitem.getMeso() != 0:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        Distance = Client_Reportedpos.distanceSq(mapitem.getPosition())
        if Distance > 10000.0 && (mapitem.getMeso() > 0 || mapitem.getItemId() != 4001025):
            chr.getCheatTracker().registerOffense(CheatingOffense.宠物全图吸物_客户端, str(Distance))
            World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[GM消息] " + chr.getName() + " ID: " + chr.getId() + " (等级 " + chr.getLevel() + ") 全屏宠吸。地图ID: " + chr.getMapId() + " 范围: " + Distance).encode("utf-8"))
        elif pet.getPos().distanceSq(mapitem.getPosition()) > 640000.0:
            chr.getCheatTracker().registerOffense(CheatingOffense.宠物全图吸物_服务端)
            World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[GM消息] " + chr.getName() + " ID: " + chr.getId() + " (等级 " + chr.getLevel() + ") 全屏宠吸。地图ID: " + chr.getMapId() + " 范围: " + Distance).encode("utf-8"))
        if mapitem.getMeso() > 0:
            if chr.getParty() is not None && mapitem.getOwner() != chr.getId():
                toGive = []
                splitMeso = mapitem.getMeso() * 40 / 100
                for z in chr.getParty().getMembers():
                    m = chr.getMap().getCharacterById(z.getId())
                    if m is not None && m.getId() != chr.getId():
                        toGive.add(m)
                for i in toGive:
                    i.gainMeso(splitMeso / toGive + (i.getStat().hasPartyBonus ? ((int)(mapitem.getMeso() / 20.0)) : 0), True)
                chr.gainMeso(mapitem.getMeso() - splitMeso, True)
            else:
                chr.gainMeso(mapitem.getMeso(), True)
            removeItem_Pet(chr, mapitem, petz)
        elif MapleItemInformationProvider.getInstance().isPickupBlocked(mapitem.getItemId()) || mapitem.getItemId() / 10000 == 291:
            c.getSession().write(MaplePacketCreator.enableActions())
        elif useItem(c, mapitem.getItemId()):
            removeItem_Pet(chr, mapitem, petz)
        elif MapleInventoryManipulator.checkSpace(c, mapitem.getItemId(), mapitem.getItem().getQuantity(), mapitem.getItem().getOwner()):
            if mapitem.getItem().getQuantity() >= 50 && mapitem.getItemId() == 2340000:
                c.setMonitored(True)
            MapleInventoryManipulator.pet_addFromDrop(c, mapitem.getItem(), True, mapitem.getDropper() instanceof MapleMonster)
            removeItem_Pet(chr, mapitem, petz)

    def useItem(self, c: Any, id: int) -> bool:
        if GameConstants.isUse(id):
            ii = MapleItemInformationProvider.getInstance()
            consumeval = ii.isConsumeOnPickup(id)
            if consumeval > 0:
                if consumeval == 2:
                    if c.getPlayer().getParty() is not None:
                        for pc in c.getPlayer().getParty().getMembers():
                            chr = c.getPlayer().getMap().getCharacterById(pc.getId())
                            if chr is not None:
                                ii.getItemEffect(id).applyTo(chr)
                    else:
                        ii.getItemEffect(id).applyTo(c.getPlayer())
                else:
                    ii.getItemEffect(id).applyTo(c.getPlayer())
                c.getSession().write(MaplePacketCreator.getShowItemGain(id, 1))
                return True
        return False

    def removeItem_Pet(self, chr: Any, mapitem: Any, pet: int) -> None:
        mapitem.setPickedUp(True)
        chr.getMap().broadcastMessage(MaplePacketCreator.removeItemFromMap(mapitem.getObjectId(), 5, chr.getId(), pet), mapitem.getPosition())
        chr.getMap().removeMapObject(mapitem)

    def removeItem(self, chr: Any, mapitem: Any, ob: Any) -> None:
        mapitem.setPickedUp(True)
        chr.getMap().broadcastMessage(MaplePacketCreator.removeItemFromMap(mapitem.getObjectId(), 2, chr.getId()), mapitem.getPosition())
        chr.getMap().removeMapObject(ob)

    def addMedalString(self, c: Any, sb: Any) -> None:
        medal = c.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-26))
        if medal is not None:
            sb.append("<")
            sb.append(MapleItemInformationProvider.getInstance().getName(medal.getItemId()))
            sb.append("> ")

    def OwlMinerva(self, slea: Any, c: Any) -> None:
        slot = slea.readShort()
        itemid = slea.readInt()
        toUse = c.getPlayer().getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is not None && toUse.getQuantity() > 0 && toUse.getItemId() == itemid && itemid == 2310000:
            itemSearch = slea.readInt()
            hms = c.getChannelServer().searchMerchant(itemSearch)
            if hms > 0:
                c.getSession().write(MaplePacketCreator.getOwlSearched(itemSearch, hms))
                MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemid, 1, True, False)
            else:
                c.getPlayer().dropMessage(1, "没有找到这个道具.")
        c.getSession().write(MaplePacketCreator.enableActions())

    def Owl(self, slea: Any, c: Any) -> None:
        if c.getPlayer().haveItem(5230000, 1, True, False) || c.getPlayer().haveItem(5230001, 1, True, False):
            if c.getPlayer().getMapId() >= 910000000 && c.getPlayer().getMapId() <= 910000022:
                c.getSession().write(MaplePacketCreator.getOwlOpen())
            else:
                c.getPlayer().dropMessage(5, "商店搜索器只能在自由市场使用.")
                c.getSession().write(MaplePacketCreator.enableActions())

    def OwlWarp(self, slea: Any, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.enableActions())
        if c.getPlayer().getMapId() >= 910000000 && c.getPlayer().getMapId() <= 910000022 && c.getPlayer().getPlayerShop() is None:
            id = slea.readInt()
            map = slea.readInt()
            if map >= 910000001 && map <= 910000022:
                mapp = c.getChannelServer().getMapFactory().getMap(map)
                c.getPlayer().changeMap(mapp, mapp.getPortal(0))
                merchant = None
                # switch (InventoryHandler.OWL_ID):
                    # case 0:
                        objects = mapp.getAllHiredMerchantsThreadsafe()
                        for ob in objects:
                            if isinstance(ob, IMaplePlayerShop):
                                ips = ob
                                if !(isinstance(ips, HiredMerchant)):
                                    continue
                                merch = ips
                                if merch.getOwnerId() == id:
                                    merchant = merch
                                    break
                                continue
                        break
                    # case 1:
                        objects = mapp.getAllHiredMerchantsThreadsafe()
                        for ob in objects:
                            if isinstance(ob, IMaplePlayerShop):
                                ips = ob
                                if !(isinstance(ips, HiredMerchant)):
                                    continue
                                merch = ips
                                if merch.getStoreId() == id:
                                    merchant = merch
                                    break
                                continue
                        break
                    # default:
                        ob2 = mapp.getMapObject(id, MapleMapObjectType.HIRED_MERCHANT)
                        if !(isinstance(ob2, IMaplePlayerShop)):
                            break
                        ips2 = ob2
                        if isinstance(ips2, HiredMerchant):
                            merchant = ips2
                            break
                        break
                if merchant is not None:
                    if merchant.isOwner(c.getPlayer()):
                        merchant.setOpen(False)
                        merchant.removeAllVisitors(16, 0)
                        c.getPlayer().setPlayerShop(merchant)
                        c.getSession().write(PlayerShopPacket.getHiredMerch(c.getPlayer(), merchant, False))
                    elif !merchant.isOpen() || !merchant.isAvailable():
                        c.getPlayer().dropMessage(1, "主人正在整理商店物品\r\n请稍后再度光临！.")
                    elif merchant.getFreeSlot() == -1:
                        c.getPlayer().dropMessage(1, "店铺已达到最大人数\r\n请稍后再度光临！.")
                    elif merchant.isInBlackList(c.getPlayer().getName()):
                        c.getPlayer().dropMessage(1, "你被禁止进入该店铺")
                    else:
                        c.getPlayer().setPlayerShop(merchant)
                        merchant.addVisitor(c.getPlayer())
                        c.getSession().write(PlayerShopPacket.getHiredMerch(c.getPlayer(), merchant, False))
                else:
                    c.getPlayer().dropMessage(1, "主人正在整理商店物品\r\n请稍后再度光临！")

    def UseSkillBook(self, slea: Any, c: Any, chr: Any) -> bool:
        slea.skip(4)
        slot = slea.readShort()
        itemId = slea.readInt()
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is None || toUse.getQuantity() < 1 || toUse.getItemId() != itemId:
            return False
        skilldata = MapleItemInformationProvider.getInstance().getSkillStats(toUse.getItemId())
        if skilldata is None:
            return False
        canuse = False
        success = False
        skill = 0
        maxlevel = 0
        SuccessRate = skilldata.get("success")
        ReqSkillLevel = skilldata.get("reqSkillLevel")
        MasterLevel = skilldata.get("masterLevel")
        i = 0
        while True:
            CurrentLoopedSkillId = skilldata.get("skillid" + i)
            i += 1
            if CurrentLoopedSkillId is None:
                break
            if math.floor(CurrentLoopedSkillId / 10000) != chr.getJob():
                continue
            CurrSkillData = SkillFactory.getSkill(CurrentLoopedSkillId)
            if chr.getSkillLevel(CurrSkillData) >= ReqSkillLevel && chr.getMasterLevel(CurrSkillData) < MasterLevel:
                canuse = True
                if Randomizer.nextInt(99) <= SuccessRate && SuccessRate != 0:
                    success = True
                    skill2 = CurrSkillData
                    chr.changeSkillLevel(skill2, chr.getSkillLevel(skill2), MasterLevel)
                else:
                    success = False
                MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
                break
            canuse = False
        c.getSession().write(MaplePacketCreator.useSkillBook(chr, skill, maxlevel, canuse, success))
        c.getSession().write(MaplePacketCreator.enableActions())
        return canuse

    def changeFace(self, player: Any, color: int) -> None:
        if player.getFace() % 1000 < 100:
            player.setFace(player.getFace() + color)
        elif player.getFace() % 1000 >= 100 && player.getFace() % 1000 < 200:
            player.setFace(player.getFace() - 100 + color)
        elif player.getFace() % 1000 >= 200 && player.getFace() % 1000 < 300:
            player.setFace(player.getFace() - 200 + color)
        elif player.getFace() % 1000 >= 300 && player.getFace() % 1000 < 400:
            player.setFace(player.getFace() - 300 + color)
        elif player.getFace() % 1000 >= 400 && player.getFace() % 1000 < 500:
            player.setFace(player.getFace() - 400 + color)
        elif player.getFace() % 1000 >= 500 && player.getFace() % 1000 < 600:
            player.setFace(player.getFace() - 500 + color)
        elif player.getFace() % 1000 >= 600 && player.getFace() % 1000 < 700:
            player.setFace(player.getFace() - 600 + color)
        elif player.getFace() % 1000 >= 700 && player.getFace() % 1000 < 800:
            player.setFace(player.getFace() - 700 + color)
        player.updateSingleStat(MapleStat.FACE, player.getFace())
        player.equipChanged()

