"""
NPCHandler - Converted from Java source
Original: handling/channel/handler/NPCHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.RockPaperScissors import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from scripting.NPCConversationManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.AutobanManager import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleShop import *  # TODO: import specific classes
# from server.MapleStorage import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class NPCHandler:
    """
    Class NPCHandler
    """


    def NPCAnimation(self, slea: Any, c: Any) -> None:
        length = slea.available()
        if length < 4:
            return
        map = c.getPlayer().getMap()
        if map is None:
            return
        oid = slea.readInt()
        npc = map.getNPCByOid(oid)
        if npc is None:
            if c.getPlayer().isAdmin():
                c.getPlayer().dropMessage("NPC OID =" + oid)
            return
        # switch (npc.getId()):
            # case 2103:
            # case 10000:
            # case 1010100:
            # case 1012003:
            # case 1012106:
            # case 1032004:
            # case 1052103:
            case 1061100: {}
            # default:
                if !c.getPlayer().isMapObjectVisible(npc):
                    return
                mplew = MaplePacketLittleEndianWriter()
                mplew.writeShort(SendPacketOpcode.NPC_ACTION.getValue())
                mplew.writeInt(oid)
                if length == 6:
                    mplew.writeShort(slea.readShort())
                else:
                    if length <= 9:
                        if c.getPlayer().isAdmin():
                            c.getPlayer().dropMessage("NPC, Packet:" + slea)
                        return
                    mplew.write(slea.read(length - 13))
                c.sendPacket(mplew.getPacket())

    def NPCShop(self, slea: Any, c: Any, chr: Any) -> None:
        bmode = slea.readByte()
        if chr is None:
            return
        # switch (bmode):
            # case 0:
                shop = chr.getShop()
                if shop is None:
                    return
                slea.skip(2)
                itemId = slea.readInt()
                quantity = slea.readShort()
                shop.buy(c, itemId, quantity)
                break
            # case 1:
                shop = chr.getShop()
                if shop is None:
                    return
                slot = slea.readShort()
                itemId2 = slea.readInt()
                quantity2 = slea.readShort()
                shop.sell(c, GameConstants.getInventoryType(itemId2), slot, quantity2)
                break
            # case 2:
                shop = chr.getShop()
                if shop is None:
                    return
                slot = slea.readShort()
                shop.recharge(c, slot)
                break
            # default:
                chr.setConversation(0)
                break

    def NPCTalk(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || chr.getMap() is None:
            return
        npc = chr.getMap().getNPCByOid(slea.readInt())
        slea.readInt()
        if npc is None:
            return
        chr.setCurrenttime(int(time.time() * 1000))
        if chr.getCurrenttime() - chr.getLasttime() < chr.getDeadtime():
            chr.dropMessage("悠着点!")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        chr.setLasttime(int(time.time() * 1000))
        if chr.getConversation() != 0:
            NPCScriptManager.getInstance().dispose(c)
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if npc.hasShop():
            c.getSession().write(MaplePacketCreator.confirmShopTransaction(20))
            chr.setConversation(1)
            npc.sendShop(c)
        else:
            NPCScriptManager.getInstance().start(c, npc.getId())

    def QuestAction(self, slea: Any, c: Any, chr: Any) -> None:
        action = slea.readByte()
        quest = slea.readShort()
        if quest < 0:
            quest += 65536
        if chr is None:
            return
        if !chr.canQuestAction():
            chr.dropMessage(1, "提交操作过快请稍后！")
            c.sendPacket(MaplePacketCreator.enableActions())
            return
        q = MapleQuest.getInstance(quest)
        # switch (action):
            # case 0:
                chr.updateTick(slea.readInt())
                itemid = slea.readInt()
                MapleQuest.getInstance(quest).RestoreLostItem(chr, itemid)
                break
            # case 1:
                npc = slea.readInt()
                q.start(chr, npc)
                if c.getPlayer().isAdmin():
                    c.getPlayer().dropMessage("开始任务[" + quest + "] NPC: " + npc)
                    break
                break
            # case 2:
                npc = slea.readInt()
                chr.updateTick(slea.readInt())
                if slea.available() >= 4:
                    q.complete(chr, npc, slea.readInt())
                else:
                    q.complete(chr, npc)
                if c.getPlayer().isAdmin():
                    c.getPlayer().dropMessage("完成任务[" + quest + "] NPC: " + npc)
                    break
                break
            # case 3:
                if GameConstants.canForfeit(q.getId()):
                    q.forfeit(chr)
                    break
                chr.dropMessage(1, "你不可以放弃这个任务.")
                break
            # case 4:
                npc = slea.readInt()
                slea.readInt()
                NPCScriptManager.getInstance().startQuest(c, npc, quest)
                if c.getPlayer().isAdmin():
                    c.getPlayer().dropMessage("脚本开始任务[" + quest + "] NPC: " + npc)
                    break
                break
            # case 5:
                npc = slea.readInt()
                NPCScriptManager.getInstance().endQuest(c, npc, quest, False)
                c.getSession().write(MaplePacketCreator.showSpecialEffect(9))
                chr.getMap().broadcastMessage(chr, MaplePacketCreator.showSpecialEffect(chr.getId(), 9), False)
                if c.getPlayer().isAdmin():
                    c.getPlayer().dropMessage("脚本完成任务[" + quest + "] NPC: " + npc)
                    break
                break

    def Storage(self, slea: Any, c: Any, chr: Any) -> None:
        mode = slea.readByte()
        if chr is None:
            return
        storage = chr.getStorage()
        ii = MapleItemInformationProvider.getInstance()
        # switch (mode):
            # case 4:
                type = slea.readByte()
                slot = storage.getSlot(MapleInventoryType.getByType(type), slea.readByte())
                item = storage.takeOut(slot)
                if ii.isCash(item.getItemId()):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if item is not None:
                    if !MapleInventoryManipulator.checkSpace(c, item.getItemId(), item.getQuantity(), item.getOwner()):
                        storage.store(item)
                        chr.dropMessage(1, "你的物品栏已经满了..")
                    else:
                        MapleInventoryManipulator.addFromDrop(c, item, False)
                    storage.sendTakenOut(c, GameConstants.getInventoryType(item.getItemId()))
                    break
                print("[作弊] " + chr.getName() + " (等级 " + chr.getLevel() + ") 试图从仓库取出不存在的道具.")
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 5:
                slot2 = slea.readShort()
                itemId = slea.readInt()
                if itemId >= 1112446 && itemId <= 1112495:
                    c.getPlayer().dropMessage(1, "禁止存入仓库")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                quantity = slea.readShort()
                if quantity < 1:
                    AutobanManager.getInstance().autoban(c, "试图存入到仓库的道具数量: " + quantity + " 道具ID: " + itemId)
                    return
                if storage.isFull():
                    c.getSession().write(MaplePacketCreator.getStorageFull())
                    return
                type2 = GameConstants.getInventoryType(itemId)
                if chr.getInventory(type2).getItem(slot2) is None:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if chr.getMeso() < 100:
                    chr.dropMessage(1, "你没有足够的金币.需要100金币")
                    break
                item2 = chr.getInventory(type2).getItem(slot2).copy()
                if ii.isCash(item2.getItemId()):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if GameConstants.isPet(item2.getItemId()):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                flag = item2.getFlag()
                if ii.isPickupRestricted(item2.getItemId()) && storage.findById(item2.getItemId()) is not None:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if item2.getItemId() == itemId && (item2.getQuantity() >= quantity || GameConstants.is飞镖道具(itemId) || GameConstants.is子弹道具(itemId)):
                    if ii.isDropRestricted(item2.getItemId()):
                        if ItemFlag.KARMA_EQ.check(flag):
                            item2.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
                        elif ItemFlag.KARMA_USE.check(flag):
                            item2.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
                        else:
                            if !ItemFlag.LOCK.check(flag):
                                c.getSession().write(MaplePacketCreator.enableActions())
                                return
                            item2.setFlag((byte)(flag - ItemFlag.LOCK.getValue()))
                    if GameConstants.is飞镖道具(itemId) || GameConstants.is子弹道具(itemId):
                        quantity = item2.getQuantity()
                    chr.gainMeso(-100, False, True, False)
                    MapleInventoryManipulator.removeFromSlot(c, type2, slot2, quantity, False)
                    item2.setQuantity(quantity)
                    storage.store(item2)
                    storage.sendStored(c, GameConstants.getInventoryType(itemId))
                    break
                AutobanManager.getInstance().addPoints(c, 1000, 0, "试图存入到仓库的道具: " + itemId + " 数量: " + quantity + " 当前玩家用道具: " + item2.getItemId() + " 数量: " + item2.getQuantity())
            # case 6:
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 7:
                meso = slea.readInt()
                storageMesos = storage.getMeso()
                playerMesos = chr.getMeso()
                if (meso > 0 && storageMesos >= meso) || (meso < 0 && playerMesos >= -meso):
                    if meso < 0 && storageMesos - meso < 0:
                        meso = -(Integer.MAX_VALUE - storageMesos)
                        if -meso > playerMesos:
                            return
                    elif meso > 0 && playerMesos + meso < 0:
                        meso = Integer.MAX_VALUE - playerMesos
                        if meso > storageMesos:
                            return
                    storage.setMeso(storageMesos - meso)
                    chr.gainMeso(meso, False, True, False)
                    storage.sendMeso(c)
                    break
                AutobanManager.getInstance().addPoints(c, 1000, 0, "Trying to store or take out unavailable amount of mesos (" + meso + "/" + storage.getMeso() + "/" + c.getPlayer().getMeso() + ")")
            # case 8:
                storage.close()
                chr.setConversation(0)
                break
            # default:
                print("未知的仓库操作包 0x0: " + mode)
                break

    def NPCMoreTalk(self, slea: Any, c: Any) -> None:
        player = c.getPlayer()
        if player is None:
            return
        lastMsg = slea.readByte()
        action = slea.readByte()
        cm = NPCScriptManager.getInstance().getCM(c)
        if cm is None || c.getPlayer().getConversation() == 0 || cm.getLastMsg() != lastMsg:
            return
        cm.setLastMsg((byte)(-1))
        if lastMsg == 2:
            if action != 0:
                cm.setGetText(slea.readMapleAsciiString())
                # switch (cm.getType()):
                    # case 0:
                        NPCScriptManager.getInstance().startQuest(c, action, lastMsg, -1)
                        break
                    # case 1:
                        NPCScriptManager.getInstance().endQuest(c, action, lastMsg, -1)
                        break
                    # default:
                        NPCScriptManager.getInstance().action(c, action, lastMsg, -1)
                        break
            else:
                cm.dispose()
        else:
            selection = -1
            if slea.available() >= 4:
                selection = slea.readInt()
            elif slea.available() > 0:
                selection = slea.readByte()
            if lastMsg == 4 && selection == -1:
                cm.dispose()
                return
            if selection >= -1 && action != -1:
                # switch (cm.getType()):
                    # case 0:
                        NPCScriptManager.getInstance().startQuest(c, action, lastMsg, selection)
                        break
                    # case 1:
                        NPCScriptManager.getInstance().endQuest(c, action, lastMsg, selection)
                        break
                    # default:
                        NPCScriptManager.getInstance().action(c, action, lastMsg, selection)
                        break
            else:
                cm.dispose()

    def UpdateQuest(self, slea: Any, c: Any) -> None:
        quest = MapleQuest.getInstance(slea.readShort())
        if quest is not None:
            c.getPlayer().updateQuest(c.getPlayer().getQuest(quest), True)

    def RPSGame(self, slea: Any, c: Any) -> None:
        if slea.available() == 0 || !c.getPlayer().getMap().containsNPC(9000019):
            if c.getPlayer().getRPS() is not None:
                c.getPlayer().getRPS().dispose(c)
            return
        mode = slea.readByte()
        # switch (mode):
            # case 0:
            # case 5:
                if c.getPlayer().getRPS() is not None:
                    c.getPlayer().getRPS().reward(c)
                if c.getPlayer().getMeso() >= 1000:
                    c.getPlayer().setRPS(RockPaperScissors(c, mode))
                    break
                c.getSession().write(MaplePacketCreator.getRPSMode(8, -1, -1, -1))
                break
            # case 1:
                if c.getPlayer().getRPS() is None || !c.getPlayer().getRPS().answer(c, slea.readByte()):
                    c.getSession().write(MaplePacketCreator.getRPSMode(13, -1, -1, -1))
                    break
                break
            # case 2:
                if c.getPlayer().getRPS() is None || !c.getPlayer().getRPS().timeOut(c):
                    c.getSession().write(MaplePacketCreator.getRPSMode(13, -1, -1, -1))
                    break
                break
            # case 3:
                if c.getPlayer().getRPS() is None || !c.getPlayer().getRPS().nextRound(c):
                    c.getSession().write(MaplePacketCreator.getRPSMode(13, -1, -1, -1))
                    break
                break
            # case 4:
                if c.getPlayer().getRPS() is not None:
                    c.getPlayer().getRPS().dispose(c)
                    break
                c.getSession().write(MaplePacketCreator.getRPSMode(13, -1, -1, -1))
                break

