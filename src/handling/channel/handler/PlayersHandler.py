"""
PlayersHandler - Converted from Java source
Original: handling/channel/handler/PlayersHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any
import math
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleLieDetector import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from scripting.ReactorScriptManager import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.events.MapleCoconut import *  # TODO: import specific classes
# from server.events.MapleEventType import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleDoor import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class PlayersHandler:
    """
    Class PlayersHandler
    """


    def Note(self, slea: Any, chr: Any) -> None:
        type = slea.readByte()
        # switch (type):
            # case 0:
                name = slea.readMapleAsciiString()
                msg = slea.readMapleAsciiString()
                fame = slea.readByte() > 0
                slea.readInt()
                itemz = chr.getCashInventory().findByCashId(slea.readLong())
                if itemz is None || !itemz.getGiftFrom().lower() == name.lower() || !chr.getCashInventory().canSendNote(itemz.getUniqueId()):
                    return
                try:
                    chr.sendNote(name, msg, fame ? 1 : 0)
                    chr.getCashInventory().sendedNote(itemz.getUniqueId())
                except Exception as e:
                    e.printStackTrace()
                break
            # case 1:
                num = slea.readByte()
                slea.readByte()
                人气 = slea.readByte()
                for i in range(num):
                    id = slea.readInt()
                    chr.deleteNote(id, (人气 > 0) ? 人气 : 0)
                break
            # default:
                print("Unhandled note action, " + type + "")
                break

    def GiveFame(self, slea: Any, c: Any, chr: Any) -> None:
        who = slea.readInt()
        mode = slea.readByte()
        famechange = (mode == 0) ? -1 : 1
        target = chr.getMap().getMapObject(who, MapleMapObjectType.PLAYER)
        if target == chr:
            chr.getCheatTracker().registerOffense(CheatingOffense.添加自己声望)
            return
        if chr.getLevel() < 15:
            chr.getCheatTracker().registerOffense(CheatingOffense.声望十五级以下添加)
            return
        # switch (chr.canGiveFame(target)):
            # case OK:
                if abs(target.getFame() + famechange) <= 30000:
                    target.addFame(famechange)
                    target.updateSingleStat(MapleStat.FAME, target.getFame())
                if !chr.isGM():
                    chr.hasGivenFame(target)
                c.getSession().write(MaplePacketCreator.giveFameResponse(mode, target.getName(), target.getFame()))
                target.getClient().getSession().write(MaplePacketCreator.receiveFame(mode, chr.getName()))
                break
            # case NOT_TODAY:
                c.getSession().write(MaplePacketCreator.giveFameErrorResponse(3))
                break
            # case NOT_THIS_MONTH:
                c.getSession().write(MaplePacketCreator.giveFameErrorResponse(4))
                break

    def ChatRoomHandler(self, slea: Any, c: Any) -> None:
        NPCScriptManager.getInstance().dispose(c)
        if c.getPlayer().getTrade() is not None:
            c.getPlayer().dropMessage(1, "交易中无法进行其他操作！")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if c.getPlayer().getLevel() >= 1:
            NPCScriptManager.getInstance().start(c, 9900003)
            c.getSession().write(MaplePacketCreator.enableActions())
        else:
            c.getSession().write(MaplePacketCreator.getNPCTalk(9900004, 0, "玩家你好.等级不足1级无法使用快捷功能.", "00 00", 0))
            c.getSession().write(MaplePacketCreator.enableActions())

    def UseDoor(self, slea: Any, chr: Any) -> None:
        oid = slea.readInt()
        mode = slea.readByte() == 0
        for obj in chr.getMap().getAllDoorsThreadsafe():
            door = obj
            if door.getOwnerId() == oid:
                door.warp(chr, mode)
                break
        chr.getClient().getSession().write(MaplePacketCreator.enableActions())

    def TransformPlayer(self, slea: Any, c: Any, chr: Any) -> None:
        chr.updateTick(slea.readInt())
        slot = slea.readShort()
        itemId = slea.readInt()
        target = slea.readMapleAsciiString().lower()
        toUse = c.getPlayer().getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is None || toUse.getQuantity() < 1 || toUse.getItemId() != itemId:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        # switch (itemId):
            # case 2212000:
                search_chr = chr.getMap().getCharacterByName(target)
                if search_chr is not None:
                    MapleItemInformationProvider.getInstance().getItemEffect(2210023).applyTo(search_chr)
                    search_chr.dropMessage(6, chr.getName() + " 对你开了个玩笑！")
                    MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
                    break
                chr.dropMessage(1, "在当前地图中未找到 '" + target + "' 的玩家.")
                break
        c.getSession().write(MaplePacketCreator.enableActions())

    def HitReactor(self, slea: Any, c: Any) -> None:
        oid = slea.readInt()
        charPos = slea.readInt()
        stance = slea.readShort()
        reactor = c.getPlayer().getMap().getReactorByOid(oid)
        if reactor is None || !reactor.isAlive():
            return
        if c.getPlayer().isGM():
            c.getPlayer().dropMessage("[系统提示]你已攻击反应物" + reactor.getReactorId())
        reactor.hitReactor(charPos, stance, c)

    def TouchReactor(self, slea: Any, c: Any) -> None:
        oid = slea.readInt()
        touched = slea.readByte() > 0
        reactor = c.getPlayer().getMap().getReactorByOid(oid)
        if !touched || reactor is None || !reactor.isAlive() || reactor.getReactorId() < 6109013 || reactor.getReactorId() > 6109027 || reactor.getTouch() == 0:
            return
        if c.getPlayer().isAdmin():
            c.getPlayer().dropMessage(5, "反应堆信息 - oid: " + oid + " Touch: " + reactor.getTouch() + " isTimerActive: " + reactor.isTimerActive() + " ReactorType: " + reactor.getReactorType())
        if reactor.getTouch() == 2:
            ReactorScriptManager.getInstance().act(c, reactor)
        elif reactor.getTouch() == 1 && !reactor.isTimerActive():
            if reactor.getReactorType() == 100:
                itemid = GameConstants.getCustomReactItem(reactor.getReactorId(), reactor.getReactItem().getLeft())
                if c.getPlayer().haveItem(itemid, reactor.getReactItem().getRight()):
                    if reactor.getArea().__contains__(c.getPlayer().getTruePosition()):
                        MapleInventoryManipulator.removeById(c, GameConstants.getInventoryType(itemid), itemid, reactor.getReactItem().getRight(), True, False)
                        reactor.hitReactor(c)
                    else:
                        c.getPlayer().dropMessage(5, "距离太远。请靠近后重新尝试。")
                else:
                    c.getPlayer().dropMessage(5, "你没有所需的物品.")
            else:
                reactor.hitReactor(c)

    def hitCoconut(self, slea: Any, c: Any) -> None:
        id = slea.readShort()
        co = "椰子"
        map = c.getChannelServer().getEvent(MapleEventType.打椰子比赛)
        if map is None || !map.isRunning():
            map = c.getChannelServer().getEvent(MapleEventType.打瓶盖比赛)
            co = "瓶盖"
            if map is None || !map.isRunning():
                return
        final MapleCoconut.MapleCoconuts nut = map.getCoconut(id)
        if nut is None || !nut.isHittable():
            return
        if int(time.time() * 1000) < nut.getHitTime():
            return
        if nut.getHits() > 2 && random.random() < 0.4 && !nut.isStopped():
            nut.setHittable(False)
            if random.random() < 0.01 && map.getStopped() > 0:
                nut.setStopped(True)
                map.stopCoconut()
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.hitCoconut(False, id, 1))
                return
            nut.resetHits()
            if random.random() < 0.05 && map.getBombings() > 0:
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.hitCoconut(False, id, 2))
                map.bombCoconut()
            elif map.getFalling() > 0:
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.hitCoconut(False, id, 3))
                map.fallCoconut()
                if c.getPlayer().getTeam() == 0:
                    map.addMapleScore()
                    c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(5, c.getPlayer().getName() + " 彩虹队成功打掉了一个 " + co + "."))
                else:
                    map.addStoryScore()
                    c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(5, c.getPlayer().getName() + " 神秘队成功打掉一个 " + co + "."))
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.coconutScore(map.getCoconutScore()))
        else:
            nut.hit()
            c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.hitCoconut(False, id, 1))

    def RingAction(self, slea: Any, c: Any) -> None:
        mode = slea.readByte()
        # switch (mode):
            # case 0:
                name = slea.readMapleAsciiString()
                itemid = slea.readInt()
                newItemId = 1112300 + (itemid - 2240004)
                chr = c.getChannelServer().getPlayerStorage().getCharacterByName(name)
                errcode = 0
                if c.getPlayer().getMarriageId() > 0:
                    errcode = 23
                elif chr is None:
                    errcode = 18
                elif chr.getMapId() != c.getPlayer().getMapId():
                    errcode = 19
                elif !c.getPlayer().haveItem(itemid, 1) || itemid < 2240004 || itemid > 2240015:
                    errcode = 13
                elif chr.getMarriageId() > 0 || chr.getMarriageItemId() > 0:
                    errcode = 24
                elif !MapleInventoryManipulator.checkSpace(c, newItemId, 1, ""):
                    errcode = 20
                elif !MapleInventoryManipulator.checkSpace(chr.getClient(), newItemId, 1, ""):
                    errcode = 21
                if errcode > 0:
                    c.getSession().write(MaplePacketCreator.sendEngagement(errcode, 0, None, None))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                c.getPlayer().setMarriageItemId(itemid)
                chr.getClient().getSession().write(MaplePacketCreator.sendEngagementRequest(c.getPlayer().getName(), c.getPlayer().getId()))
                break
            # case 1:
                c.getPlayer().setMarriageItemId(0)
                break
            # case 2:
                accepted = slea.readByte() > 0
                name2 = slea.readMapleAsciiString()
                id = slea.readInt()
                chr = c.getChannelServer().getPlayerStorage().getCharacterByName(name2)
                if c.getPlayer().getMarriageId() > 0 || chr is None || chr.getId() != id || chr.getMarriageItemId() <= 0 || !chr.haveItem(chr.getMarriageItemId(), 1) || chr.getMarriageId() > 0:
                    c.getSession().write(MaplePacketCreator.sendEngagement(29, 0, None, None))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if accepted:
                    newItemId2 = 1112300 + (chr.getMarriageItemId() - 2240004)
                    if !MapleInventoryManipulator.checkSpace(c, newItemId2, 1, "") || !MapleInventoryManipulator.checkSpace(chr.getClient(), newItemId2, 1, ""):
                        c.getSession().write(MaplePacketCreator.sendEngagement(21, 0, None, None))
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    MapleInventoryManipulator.addById(c, newItemId2, 1, 0)
                    MapleInventoryManipulator.removeById(chr.getClient(), MapleInventoryType.USE, chr.getMarriageItemId(), 1, False, False)
                    MapleInventoryManipulator.addById(chr.getClient(), newItemId2, 1, 0)
                    chr.getClient().getSession().write(MaplePacketCreator.sendEngagement(16, newItemId2, chr, c.getPlayer()))
                    chr.setMarriageId(c.getPlayer().getId())
                    c.getPlayer().setMarriageId(chr.getId())
                else:
                    chr.getClient().getSession().write(MaplePacketCreator.sendEngagement(30, 0, None, None))
                c.getSession().write(MaplePacketCreator.enableActions())
                chr.setMarriageItemId(0)
                break
            # case 3:
                itemId = slea.readInt()
                type = GameConstants.getInventoryType(itemId)
                item = c.getPlayer().getInventory(type).findById(itemId)
                if item is not None && type == MapleInventoryType.ETC && itemId / 10000 == 421:
                    MapleInventoryManipulator.drop(c, type, item.getPosition(), item.getQuantity())
                    break
                break

    def LieDetector(self, slea: Any, c: Any, chr: Any, isItem: bool) -> None:
        if chr is None || chr.getMap() is None:
            return
        target = slea.readMapleAsciiString()
        slot = 0
        if isItem:
            slot = slea.readShort()
            itemId = slea.readInt()
            toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
            if toUse is None || toUse.getQuantity() <= 0 || toUse.getItemId() != itemId || itemId != 2190000:
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if (FieldLimitType.PotionUse.check(chr.getMap().getFieldLimit()) && isItem) || chr.getMap().getReturnMapId() == chr.getMapId():
                chr.dropMessage(5, "当前地图无法使用测谎仪.")
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            search_chr = chr.getMap().getCharacterByName(target)
            if search_chr is None || search_chr.getId() == chr.getId():
                chr.dropMessage(1, "未找到角色.")
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if search_chr.getEventInstance() is not None || search_chr.getMapId() == 180000001:
                chr.dropMessage(5, "当前地图无法使用测谎仪.")
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if search_chr.getAntiMacro().inProgress():
                c.getSession().write(MaplePacketCreator.LieDetectorResponse(3))
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if (search_chr.getAntiMacro().isPassed() && isItem) || search_chr.getAntiMacro().getAttempt() == 2:
                c.getSession().write(MaplePacketCreator.LieDetectorResponse(2))
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if !search_chr.getAntiMacro().startLieDetector(chr.getName(), isItem, False):
                chr.dropMessage(5, "使用测谎仪失败.")
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if isItem:
                MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
            search_chr.dropMessage(5, chr.getName() + " 对你使用了测谎仪.")
        else:
            chr.dropMessage(1, "".append(" 测谎仪还未完善，暂时关闭."))

    def LieDetectorResponse(self, slea: Any, c: Any) -> None:
        if c.getPlayer() is None || c.getPlayer().getMap() is None:
            return
        answer = slea.readMapleAsciiString()
        ld = c.getPlayer().getAntiMacro()
        if !ld.inProgress() || (ld.isPassed() && ld.getLastType() == 0) || ld.getAnswer() is None || answer <= 0:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if answer.lower() == ld.getAnswer(.lower()):
            search_chr = c.getPlayer().getMap().getCharacterByName(ld.getTester())
            if search_chr is not None && search_chr.getId() != c.getPlayer().getId():
                search_chr.dropMessage(5, c.getPlayer().getName() + " 通过了测谎仪的检测.")
            c.getSession().write(MaplePacketCreator.LieDetectorResponse(12, 1))
            c.getPlayer().gainMeso(5000, True)
            ld.end()
        elif ld.getAttempt() < 3:
            ld.startLieDetector(ld.getTester(), ld.getLastType() == 0, True)
        else:
            search_chr = c.getPlayer().getMap().getCharacterByName(ld.getTester())
            if search_chr is not None && search_chr.getId() != c.getPlayer().getId():
                search_chr.dropMessage(5, c.getPlayer().getName() + " 通过测谎仪的检测，恭喜你获得7000的金币.")
                search_chr.gainMeso(7000, True)
            ld.end()
            c.getPlayer().getClient().getSession().write(MaplePacketCreator.LieDetectorResponse(10, 4))
            map = c.getChannelServer().getMapFactory().getMap(180000001)
            c.getPlayer().getQuestNAdd(MapleQuest.getInstance(123456)).setCustomData(str(1800))
            c.getPlayer().changeMap(map, map.getPortal(0))

    def LieDetectorRefresh(self, slea: Any, c: Any) -> None:
        if c.getPlayer() is None || c.getPlayer().getMap() is None:
            return
        ld = c.getPlayer().getAntiMacro()
        if ld.getAttempt() < 3:
            ld.startLieDetector(ld.getTester(), ld.getLastType() == 0, True)
        else:
            ld.end()
            c.getPlayer().getClient().getSession().write(MaplePacketCreator.LieDetectorResponse(8, 4))
            map = c.getChannelServer().getMapFactory().getMap(180000001)
            c.getPlayer().getQuestNAdd(MapleQuest.getInstance(123456)).setCustomData(str(1800))
            c.getPlayer().changeMap(map, map.getPortal(0))

