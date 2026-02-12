"""
World - Converted from Java source
Original: handling/world/World.java
Package: handling.world
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import pymysql
import threading
import time

# Internal module imports
# from client.BuddyEntry import *  # TODO: import specific classes
# from client.BuddyList import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleCoolDownValueHolder import *  # TODO: import specific classes
# from client.MapleDiseaseValueHolder import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.PetDataFactory import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.channel.PlayerStorage import *  # TODO: import specific classes
# from handling.world.family.MapleFamily import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyCharacter import *  # TODO: import specific classes
# from handling.world.guild.MapleBBSThread import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildAlliance import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildCharacter import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildSummary import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapItem import *  # TODO: import specific classes
# from tools.CollectionUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes


class World:
    """
    Class World
    """

    CHANNELS_PER_THREAD = 3

    def __init__(self):
        self.numTimes = 0

    # Static initializer
    # World.isShutDown = False


    @staticmethod
    def init() -> None:
        Find.findChannel(0)
        Guild.lock
        Alliance.lock
        Family.lock
        Messenger.getMessenger(0)
        Party.getParty(0)

    def getStatus(self) -> str:
        ret = ""
        totalUsers = 0
        for cs in ChannelServer.getAllInstances():
            ret.append("Channel ")
            ret.append(cs.getChannel())
            ret.append(": ")
            channelUsers = cs.getConnectedClients()
            totalUsers += channelUsers
            ret.append(channelUsers)
            ret.append(" users\n")
        ret.append("Total users online: ")
        ret.append(totalUsers)
        ret.append("\n")
        return ret

    def getConnected(self) -> dict:
        ret = {}
        total = 0
        for cs in ChannelServer.getAllInstances():
            curConnected = cs.getConnectedClients()
            ret.put(cs.getChannel(), curConnected)
            total += curConnected
        ret.put(0, total)
        return ret

    def getCheaters(self) -> list:
        allCheaters = []
        for cs in ChannelServer.getAllInstances():
            allCheaters.addAll(cs.getCheaters())
        Collections.sort(allCheaters)
        return CollectionUtil.copyFirst(allCheaters, 10)

    def isConnected(self, charName: str) -> bool:
        return Find.findChannel(charName) > 0

    def toggleMegaphoneMuteState(self) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.toggleMegaphoneMuteState()

    def ChannelChange_Data(self, Data: Any, characterid: int, toChannel: int) -> None:
        getStorage(toChannel).registerPendingPlayer(Data, characterid)

    def isCharacterListConnected(self, charName: list) -> bool:
        for cs in ChannelServer.getAllInstances():
            for c in charName:
                if cs.getPlayerStorage().getCharacterByName(c) is not None:
                    return True
        return False

    def hasMerchant(self, accountID: int) -> bool:
        for cs in ChannelServer.getAllInstances():
            if cs.containsMerchant(accountID):
                return True
        return False

    def getStorage(self, channel: int) -> Any:
        if channel == -20:
            return CashShopServer.getPlayerStorageMTS()
        if channel == -10:
            return CashShopServer.getPlayerStorage()
        return ChannelServer.getInstance(channel).getPlayerStorage()

    def scheduleRateDelay(self, type: str, delay: int) -> None:
        def _task_1():
            rate = type
            if rate == ("经验"):
                for cservs in ChannelServer.getAllInstances():
                    cservs.setExpRate(1)
            elif rate == ("爆率"):
                for cservs in ChannelServer.getAllInstances():
                    cservs.setDropRate(1)
            elif rate == ("金币"):
                for cservs in ChannelServer.getAllInstances():
                    cservs.setMesoRate(1)
            elif rate.lower() == "boss爆率".lower():
                for cservs in ChannelServer.getAllInstances():
                    cservs.setBossDropRate(1)
            else if (rate == ("宠物经验")) {}
            for cservs in ChannelServer.getAllInstances():
                cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, " 系统双倍活动已经结束。系统已成功自动切换为正常游戏模式！"))

        Timer.WorldTimer.getInstance().schedule(_task_1, delay * 1000)

    def run(self) -> None:
        rate = type
        if rate == ("经验"):
            for cservs in ChannelServer.getAllInstances():
                cservs.setExpRate(1)
        elif rate == ("爆率"):
            for cservs in ChannelServer.getAllInstances():
                cservs.setDropRate(1)
        elif rate == ("金币"):
            for cservs in ChannelServer.getAllInstances():
                cservs.setMesoRate(1)
        elif rate.lower() == "boss爆率".lower():
            for cservs in ChannelServer.getAllInstances():
                cservs.setBossDropRate(1)
        else if (rate == ("宠物经验")) {}
        for cservs in ChannelServer.getAllInstances():
            cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, " 系统双倍活动已经结束。系统已成功自动切换为正常游戏模式！"))

    def handleCooldowns(self, chr: Any, numTimes: int, hurt: bool) -> None:
        if chr is None:
            return
        now = int(time.time() * 1000)
        for m in chr.getCooldowns():
            if m.startTime + len(m) < now:
                skil = m.skillId
                chr.removeCooldown(skil)
                chr.getClient().getSession().write(MaplePacketCreator.skillCooldown(skil, 0))
        for i in chr.getAllDiseases():
            if i.startTime + len(i) < now:
                chr.dispelDebuff(i.disease)
        if numTimes % 100 == 0:
            for pet in chr.getPets():
                if pet.getSummoned():
                    if pet.getPetItemId() == 5000054 and pet.getSecondsLeft() > 0:
                        pet.setSecondsLeft(pet.getSecondsLeft() - 1)
                        if pet.getSecondsLeft() <= 0:
                            chr.unequipPet(pet, True)
                            return
                    newFullness = pet.getFullness() - PetDataFactory.getHunger(pet.getPetItemId())
                    if newFullness <= 5:
                        pet.setFullness(15)
                        chr.unequipPet(pet, True)
                    else:
                        pet.setFullness(newFullness)
                        chr.getClient().getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
        if chr.isAlive():
            if chr.canRecovery():
                chr.doRecovery()
            if chr.canExpiration(now):
                chr.expirationTask(True)
            if chr.getDiseaseSize() > 0:
                for i in chr.getAllDiseases():
                    if i is not None and i.startTime + len(i) < now:
                        chr.dispelDebuff(i.disease)
            if numTimes % 7 == 0 and chr.getMount() is not None and chr.getMount().canTire(now):
                chr.getMount().increaseFatigue()
                if chr.getMount().getFatigue() >= 90:
                    chr.dropMessage(5, "坐骑疲劳值快满了，请使用坐骑疲劳恢复药。")
            if numTimes % 26 == 0:
                for pet in chr.getSummonedPets():
                    if pet.getPetItemId() == 5000054 and pet.getSecondsLeft() > 0:
                        pet.setSecondsLeft(pet.getSecondsLeft() - 1)
                        if pet.getSecondsLeft() <= 0:
                            chr.unequipPet(pet, True)
                            return
                    newFullness = pet.getFullness() - PetDataFactory.getHunger(pet.getPetItemId())
                    if newFullness <= 5:
                        pet.setFullness(15)
                        chr.unequipPet(pet, True)
                        chr.dropMessage(5, "宠物肚子饿，回家了~！")
                    else:
                        pet.setFullness(newFullness)
                        chr.getClient().getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
            if hurt and chr.getInventory(MapleInventoryType.EQUIPPED).findById(chr.getMap().getHPDecProtect()) is None:
                if (chr.getMapId() == 749040100 and chr.getInventory(MapleInventoryType.CASH).findById(5451000) is None) or (chr.getMapId() >= 211000000 and chr.getMapId() <= 211999999):
                    chr.addHP(-chr.getMap().getHPDec())
                elif chr.getMapId() != 749040100:
                    chr.addHP(-chr.getMap().getHPDec())

    def getAllowLoginTip(self, charNames: list) -> str:
        ret = ""
        for cserv in ChannelServer.getAllInstances():
            for name in charNames:
                if cserv.isConnected(name):
                    ret.append(name)
                    ret.append(" ")
        return ret

    def registerRespawn(self) -> None:
        Timer.WorldTimer.getInstance().register(Respawn(), 5000)
        print("[刷怪线程] 已经启动...")

    def handleMap(self, map: Any, numTimes: int, size: int) -> None:
        if map.getItemsSize() > 0:
            for item in map.getAllItemsThreadsafe():
                if item.shouldExpire():
                    item.expire(map)
                else:
                    if not item.shouldFFA():
                        continue
                    item.setDropType(2)
        if map.characterSize() > 0:
            if map.canSpawn():
                map.respawn(False)
            hurt = map.canHurt()
            for chr in map.getCharactersThreadsafe():
                handleCooldowns(chr, numTimes, hurt)
        if numTimes % 10 == 0 and map.getId() == 220080001 and map.playerCount() == 0:
            ChannelServer.getInstance(map.getChannel()).getMapFactory().getMap(220080000).resetReactors()

    @staticmethod
    def partyChat(partyid: int, chattext: str, namefrom: str) -> None:
        party = getParty(partyid)
        if party is None:
            raise ValueError("no party with the specified partyid exists")
        for partychar in party.getMembers():
            ch = Find.findChannel(partychar.getName())
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(partychar.getName())
                if chr is None or chr.getName().lower() == namefrom.lower():
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.multiChat(namefrom, chattext, 1))

    def updateParty(self, partyid: int, operation: Any, target: Any) -> None:
        party = getParty(partyid)
        if party is None:
            return
        # switch (operation):
            # case JOIN:
                party.addMember(target)
                break
            # case EXPEL:
            # case LEAVE:
                party.removeMember(target)
                break
            # case DISBAND:
                disbandParty(partyid)
                break
            # case SILENT_UPDATE:
            # case LOG_ONOFF:
                party.updateMember(target)
                break
            # case CHANGE_LEADER:
                party.setLeader(target)
                break
            # default:
                raise RuntimeError("Unhandeled updateParty operation " + operation.name())
        for partychar in party.getMembers():
            ch = Find.findChannel(partychar.getName())
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(partychar.getName())
                if chr is None:
                    continue
                if operation == PartyOperation.DISBAND:
                    chr.setParty(None)
                else:
                    chr.setParty(party)
                chr.getClient().getSession().write(MaplePacketCreator.updateParty(chr.getClient().getChannel(), party, operation, target))
        # switch (operation):
            # case EXPEL:
            # case LEAVE:
                ch2 = Find.findChannel(target.getName())
                if ch2 <= 0:
                    break
                chr2 = ChannelServer.getInstance(ch2).getPlayerStorage().getCharacterByName(target.getName())
                if chr2 is not None:
                    chr2.getClient().getSession().write(MaplePacketCreator.updateParty(chr2.getClient().getChannel(), party, operation, target))
                    chr2.setParty(None)
                    break
                break

    def createParty(self, chrfor: Any) -> Any:
        partyid = Party.runningPartyId.getAndIncrement()
        party = MapleParty(partyid, chrfor)
        Party.parties.put(party.getId(), party)
        return party

    def getParty(self, partyid: int) -> Any:
        return Party.parties.get(partyid)

    def disbandParty(self, partyid: int) -> Any:
        return Party.parties.remove(partyid)

    @staticmethod
    def buddyChat(recipientCharacterIds: list, cidFrom: int, nameFrom: str, chattext: str) -> None:
        for characterId in recipientCharacterIds:
            ch = Find.findChannel(characterId)
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(characterId)
                if chr is not None and chr.getBuddylist().containsVisible(cidFrom):
                    chr.getClient().getSession().write(MaplePacketCreator.multiChat(nameFrom, chattext, 0))

    def updateBuddies(self, characterId: int, channel: int, buddies: list, offline: bool, gmLevel: int, isHidden: bool) -> None:
        for buddy in buddies:
            ch = Find.findChannel(buddy)
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(buddy)
                if chr is None:
                    continue
                ble = chr.getBuddylist().get(characterId)
                if ble is None or not ble.isVisible():
                    continue
                mcChannel = None
                if offline or (isHidden and chr.getGMLevel() < gmLevel):
                    ble.setChannel(-1)
                    mcChannel = -1
                else:
                    ble.setChannel(channel)
                    mcChannel = channel - 1
                chr.getBuddylist().put(ble)
                chr.getClient().sendPacket(MaplePacketCreator.updateBuddyChannel(ble.getCharacterId(), mcChannel))

    def buddyChanged(self, cid: int, cidFrom: int, name: str, channel: int, operation: Any, level: int, job: int, group: str) -> None:
        ch = Find.findChannel(cid)
        if ch > 0:
            addChar = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(cid)
            if addChar is not None:
                buddylist = addChar.getBuddylist()
                # switch (operation):
                    # case ADDED:
                        if (cidFrom in buddylist):
                            buddylist.put(BuddyEntry(name, cidFrom, group, channel, True, level, job))
                            addChar.getClient().getSession().write(MaplePacketCreator.updateBuddyChannel(cidFrom, channel - 1))
                            break
                        break
                    # case DELETED:
                        if (cidFrom in buddylist):
                            buddylist.put(BuddyEntry(name, cidFrom, group, -1, buddylist.get(cidFrom).isVisible(), level, job))
                            addChar.getClient().getSession().write(MaplePacketCreator.updateBuddyChannel(cidFrom, -1))
                            break
                        break

    def requestBuddyAdd(self, addName: str, channelFrom: int, cidFrom: int, nameFrom: str, levelFrom: int, jobFrom: int) -> Any:
        ch = Find.findChannel(cidFrom)
        if ch > 0:
            addChar = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(addName)
            if addChar is not None:
                buddylist = addChar.getBuddylist()
                if buddylist.isFull():
                    return BuddyList.BuddyAddResult.BUDDYLIST_FULL
                if not (cidFrom in buddylist):
                    buddylist.addBuddyRequest(addChar.getClient(), cidFrom, nameFrom, channelFrom, levelFrom, jobFrom)
                elif buddylist.containsVisible(cidFrom):
                    return BuddyList.BuddyAddResult.ALREADY_ON_LIST
        return BuddyList.BuddyAddResult.OK

    def loggedOn(self, name: str, characterId: int, channel: int, buddies: list, gmLevel: int, isHidden: bool) -> None:
        updateBuddies(characterId, channel, buddies, False, gmLevel, isHidden)

    def loggedOff(self, name: str, characterId: int, channel: int, buddies: list, gmLevel: int, isHidden: bool) -> None:
        updateBuddies(characterId, channel, buddies, True, gmLevel, isHidden)

    @staticmethod
    def createMessenger(chrfor: Any) -> Any:
        messengerid = Messenger.runningMessengerId.getAndIncrement()
        messenger = MapleMessenger(messengerid, chrfor)
        Messenger.messengers.put(messenger.getId(), messenger)
        return messenger

    def declineChat(self, target: str, namefrom: str) -> None:
        ch = Find.findChannel(target)
        if ch > 0:
            cs = ChannelServer.getInstance(ch)
            chr = cs.getPlayerStorage().getCharacterByName(target)
            if chr is not None:
                messenger = chr.getMessenger()
                if messenger is not None:
                    chr.getClient().getSession().write(MaplePacketCreator.messengerNote(namefrom, 5, 0))

    def getMessenger(self, messengerid: int) -> Any:
        return Messenger.messengers.get(messengerid)

    def leaveMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        position = messenger.getPositionByName(target.getName())
        messenger.removeMember(target)
        for mmc in messenger.getMembers():
            if mmc is not None:
                ch = Find.findChannel(mmc.getId())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(mmc.getName())
                if chr is None:
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.removeMessengerPlayer(position))

    def silentLeaveMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.silentRemoveMember(target)

    def silentJoinMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.silentAddMember(target)

    def updateMessenger(self, messengerid: int, namefrom: str, fromchannel: int) -> None:
        messenger = getMessenger(messengerid)
        position = messenger.getPositionByName(namefrom)
        for messengerchar in messenger.getMembers():
            if messengerchar is not None and not messengerchar.getName() == (namefrom):
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                from = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(namefrom)
                chr.getClient().getSession().write(MaplePacketCreator.updateMessengerPlayer(namefrom, from, position, fromchannel - 1))

    def joinMessenger(self, messengerid: int, target: Any, from: str, fromchannel: int) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.addMember(target)
        position = messenger.getPositionByName(target.getName())
        for messengerchar in messenger.getMembers():
            if messengerchar is not None:
                mposition = messenger.getPositionByName(messengerchar.getName())
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                if not messengerchar.getName() == (from):
                    fromCh = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(from)
                    chr.getClient().getSession().write(MaplePacketCreator.addMessengerPlayer(from, fromCh, position, fromchannel - 1))
                    fromCh.getClient().getSession().write(MaplePacketCreator.addMessengerPlayer(chr.getName(), chr, mposition, messengerchar.getChannel() - 1))
                else:
                    chr.getClient().getSession().write(MaplePacketCreator.joinMessenger(mposition))

    def messengerChat(self, messengerid: int, chattext: str, namefrom: str) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        for messengerchar in messenger.getMembers():
            if messengerchar is not None and not messengerchar.getName() == (namefrom):
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.messengerChat(chattext))
            else:
                if messengerchar is None:
                    continue
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())

    def messengerInvite(self, sender: str, messengerid: int, target: str, fromchannel: int, gm: bool) -> None:
        if World.isConnected(target):
            ch = Find.findChannel(target)
            if ch > 0:
                from = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(sender)
                targeter = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(target)
                if targeter is not None and targeter.getMessenger() is None:
                    if not targeter.isGM() or gm:
                        targeter.getClient().getSession().write(MaplePacketCreator.messengerInvite(sender, messengerid))
                        from.getClient().getSession().write(MaplePacketCreator.messengerNote(target, 4, 1))
                    else:
                        from.getClient().getSession().write(MaplePacketCreator.messengerNote(target, 4, 0))
                else:
                    from.getClient().getSession().write(MaplePacketCreator.messengerChat(sender + " : " + target + " is already using Maple Messenger"))

    @staticmethod
    def createGuild(leaderId: int, name: str) -> int:
        return MapleGuild.createGuild(leaderId, name)

    def getGuild(self, id: int) -> Any:
        ret = None
        Guild.lock.readLock().lock()
        try:
            ret = Guild.guilds.get(id)
        finally:
            Guild.lock.readLock().unlock()
        if ret is None:
            Guild.lock.writeLock().lock()
            try:
                ret = MapleGuild(id)
                if ret is None or ret.getId() <= 0 or not ret.isProper():
                    return None
                Guild.guilds.put(id, ret)
            finally:
                Guild.lock.writeLock().unlock()
        return ret

    def getGuildByName(self, guildName: str) -> Any:
        Guild.lock.readLock().lock()
        try:
            for g in Guild.guilds.values():
                if g.getName().lower() == guildName.lower():
                    return g
            return None
        finally:
            Guild.lock.readLock().unlock()

    def getGuild_mc(self, mc: Any) -> Any:
        return getGuild(mc.getGuildId())

    def setGuildMemberOnline(self, mc: Any, bOnline: bool, channel: int) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.setOnline(mc.getId(), bOnline, channel)

    def guildPacket(self, gid: int, message: Any) -> None:
        g = getGuild(gid)
        if g is not None:
            g.broadcast(message)

    def addGuildMember(self, mc: Any) -> int:
        g = getGuild(mc.getGuildId())
        if g is not None:
            return g.addGuildMember(mc)
        return 0

    def leaveGuild(self, mc: Any) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.leaveGuild(mc)

    def guildChat(self, gid: int, name: str, cid: int, msg: str) -> None:
        g = getGuild(gid)
        if g is not None:
            g.guildChat(name, cid, msg)

    def changeRank(self, gid: int, cid: int, newRank: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.changeRank(cid, newRank)

    def expelMember(self, initiator: Any, name: str, cid: int) -> None:
        g = getGuild(initiator.getGuildId())
        if g is not None:
            g.expelMember(initiator, name, cid)

    def setGuildNotice(self, gid: int, notice: str) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setGuildNotice(notice)

    def memberLevelJobUpdate(self, mc: Any) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.memberLevelJobUpdate(mc)

    def changeRankTitle(self, gid: int, ranks: list) -> None:
        g = getGuild(gid)
        if g is not None:
            g.changeRankTitle(ranks)

    def setGuildEmblem(self, gid: int, bg: int, bgcolor: int, logo: int, logocolor: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setGuildEmblem(bg, bgcolor, logo, logocolor)

    def disbandGuild(self, gid: int) -> None:
        g = getGuild(gid)
        Guild.lock.writeLock().lock()
        try:
            if g is not None:
                g.disbandGuild()
                Guild.guilds.remove(gid)
        finally:
            Guild.lock.writeLock().unlock()

    def deleteGuildCharacter(self, guildid: int, charid: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            mc = g.getMGC(charid)
            if mc is not None:
                if mc.getGuildRank() > 1:
                    g.leaveGuild(mc)
                else:
                    g.disbandGuild()

    def increaseGuildCapacity(self, gid: int) -> bool:
        g = getGuild(gid)
        return g is not None and g.increaseCapacity()

    def gainGP(self, gid: int, amount: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.gainGP(amount)

    def getGP(self, gid: int) -> int:
        g = getGuild(gid)
        if g is not None:
            return g.getGP()
        return 0

    def getInvitedId(self, gid: int) -> int:
        g = getGuild(gid)
        if g is not None:
            return g.getInvitedId()
        return 0

    def setInvitedId(self, gid: int, inviteid: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setInvitedId(inviteid)

    def getGuildLeader(self, guildName: str) -> int:
        mga = getGuildByName(guildName)
        if mga is not None:
            return mga.getLeaderId()
        return 0

    def save(self) -> None:
        print("Saving guilds...")
        Guild.lock.writeLock().lock()
        try:
            for a in Guild.guilds.values():
                a.writeToDB(False)
        finally:
            Guild.lock.writeLock().unlock()

    def getBBS(self, gid: int) -> list:
        g = getGuild(gid)
        if g is not None:
            return g.getBBS()
        return None

    def addBBSThread(self, guildid: int, title: str, text: str, icon: int, bNotice: bool, posterID: int) -> int:
        g = getGuild(guildid)
        if g is not None:
            return g.addBBSThread(title, text, icon, bNotice, posterID)
        return -1

    def editBBSThread(self, guildid: int, localthreadid: int, title: str, text: str, icon: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.editBBSThread(localthreadid, title, text, icon, posterID, guildRank)

    def deleteBBSThread(self, guildid: int, localthreadid: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.deleteBBSThread(localthreadid, posterID, guildRank)

    def addBBSReply(self, guildid: int, localthreadid: int, text: str, posterID: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.addBBSReply(localthreadid, text, posterID)

    def deleteBBSReply(self, guildid: int, localthreadid: int, replyid: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.deleteBBSReply(localthreadid, replyid, posterID, guildRank)

    def changeEmblem(self, gid: int, affectedPlayers: int, mgs: Any) -> None:
        Broadcast.sendGuildPacket(affectedPlayers, MaplePacketCreator.guildEmblemChange(gid, mgs.getLogoBG(), mgs.getLogoBGColor(), mgs.getLogo(), mgs.getLogoColor()), -1, gid)
        setGuildAndRank(affectedPlayers, -1, -1, -1)

    def setGuildAndRank(self, cid: int, guildid: int, rank: int, alliancerank: int) -> None:
        ch = Find.findChannel(cid)
        if ch == -1:
            return
        mc = World.getStorage(ch).getCharacterById(cid)
        if mc is None:
            return
        bDifferentGuild = None
        if guildid == -1 and rank == -1:
            bDifferentGuild = True
        else:
            bDifferentGuild = (guildid != mc.getGuildId())
            mc.setGuildId(guildid)
            mc.setGuildRank(rank)
            mc.setAllianceRank(alliancerank)
            mc.saveGuildStatus()
        if bDifferentGuild and ch > 0:
            mc.getMap().broadcastMessage(mc, MaplePacketCreator.removePlayerFromMap(cid, mc), False)
            mc.getMap().broadcastMessage(mc, MaplePacketCreator.spawnPlayerMapobject(mc), False)

    @staticmethod
    def broadcastSmega(message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastSmega(message)

    def broadcastGMMessage(self, message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastGMMessage(message)

    def broadcastMessage(self, message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastMessage(message)

    def sendPacket(self, targetIds: list, packet: Any, exception: int) -> None:
        for i in targetIds:
            if i == exception:
                continue
            ch = Find.findChannel(i)
            if ch < 0:
                continue
            c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(i)
            if c is None:
                continue
            c.getClient().getSession().write(packet)

    def sendGuildPacket(self, targetIds: int, packet: Any, exception: int, guildid: int) -> None:
        if targetIds == exception:
            return
        ch = Find.findChannel(targetIds)
        if ch < 0:
            return
        c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(targetIds)
        if c is not None and c.getGuildId() == guildid:
            c.getClient().getSession().write(packet)

    def sendFamilyPacket(self, targetIds: int, packet: Any, exception: int, guildid: int) -> None:
        if targetIds == exception:
            return
        ch = Find.findChannel(targetIds)
        if ch < 0:
            return
        c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(targetIds)
        if c is not None and c.getFamilyId() == guildid:
            c.getClient().getSession().write(packet)

    def broadcastMessage_serverNotice(self, serverNotice: Any) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastMessage(serverNotice)

    @staticmethod
    def addClient(c: Any) -> None:
        if not (c in Client.clients):
            Client.clients.add(c)

    def removeClient(self, c: Any) -> bool:
        return Client.clients.remove(c)

    def getClients(self) -> list:
        return Client.clients

    @staticmethod
    def register(id: int, name: str, channel: int) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.put(id, channel)
            Find.nameToChannel.put(name.lower(), channel)
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister(self, id: int) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.remove(id)
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister_id(self, id: str) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.nameToChannel.remove(id.lower())
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister_id_name(self, id: int, name: str) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.remove(id)
            Find.nameToChannel.remove(name.lower())
        finally:
            Find.lock.writeLock().unlock()

    def findChannel(self, id: int) -> int:
        Find.lock.readLock().lock()
        ret = None
        try:
            ret = Find.idToChannel.get(id)
        finally:
            Find.lock.readLock().unlock()
        if ret is None:
            return -1
        if ret != -10 and ret != -20 and ChannelServer.getInstance(ret) is None:
            forceDeregister(id)
            return -1
        return ret

    def findChannel_st(self, st: str) -> int:
        Find.lock.readLock().lock()
        ret = None
        try:
            ret = Find.nameToChannel.get(st.lower())
        finally:
            Find.lock.readLock().unlock()
        if ret is None:
            return -1
        if ret != -10 and ret != -20 and ChannelServer.getInstance(ret) is None:
            forceDeregister(st)
            return -1
        return ret

    def multiBuddyFind(self, charIdFrom: int, characterIds: list) -> list:
        foundsChars = [])
        for i in characterIds:
            channel = findChannel(i)
            if channel > 0:
                foundsChars.add(CharacterIdChannelPair(i, channel))
        Collections.sort(foundsChars)
        return foundsChars])

    @staticmethod
    def getAlliance(allianceid: int) -> Any:
        ret = None
        Alliance.lock.readLock().lock()
        try:
            ret = Alliance.alliances.get(allianceid)
        finally:
            Alliance.lock.readLock().unlock()
        if ret is None:
            Alliance.lock.writeLock().lock()
            try:
                ret = MapleGuildAlliance(allianceid)
                if ret is None or ret.getId() <= 0:
                    return None
                Alliance.alliances.put(allianceid, ret)
            finally:
                Alliance.lock.writeLock().unlock()
        return ret

    def getAllianceLeader(self, allianceid: int) -> int:
        mga = getAlliance(allianceid)
        if mga is not None:
            return mga.getLeaderId()
        return 0

    def updateAllianceRanks(self, allianceid: int, ranks: list) -> None:
        mga = getAlliance(allianceid)
        if mga is not None:
            mga.setRank(ranks)

    def updateAllianceNotice(self, allianceid: int, notice: str) -> None:
        mga = getAlliance(allianceid)
        if mga is not None:
            mga.setNotice(notice)

    def canInvite(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.getCapacity() > mga.getNoGuilds()

    def changeAllianceLeader(self, allianceid: int, cid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.setLeaderId(cid)

    def changeAllianceRank(self, allianceid: int, cid: int, change: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.changeAllianceRank(cid, change)

    def changeAllianceCapacity(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.setCapacity()

    def disbandAlliance(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.disband()

    def addGuildToAlliance(self, allianceid: int, gid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.addGuild(gid)

    def removeGuildFromAlliance(self, allianceid: int, gid: int, expelled: bool) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.removeGuild(gid, expelled)

    def sendGuild(self, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        if alliance is not None:
            sendGuild(MaplePacketCreator.getAllianceUpdate(alliance), -1, allianceid)
            sendGuild(MaplePacketCreator.getGuildAlliance(alliance), -1, allianceid)

    def sendGuild_packet_exceptionId_allianceid(self, packet: Any, exceptionId: int, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        if alliance is not None:
            for i in range(alliance.getNoGuilds()):
                gid = alliance.getGuildId(i)
                if gid > 0 and gid != exceptionId:
                    Guild.guildPacket(gid, packet)

    def createAlliance(self, alliancename: str, cid: int, cid2: int, gid: int, gid2: int) -> bool:
        allianceid = MapleGuildAlliance.createToDb(cid, alliancename, gid, gid2)
        if allianceid <= 0:
            return False
        g = Guild.getGuild(gid)
        g_ = Guild.getGuild(gid2)
        g.setAllianceId(allianceid)
        g_.setAllianceId(allianceid)
        g.changeARank(True)
        g_.changeARank(False)
        alliance = getAlliance(allianceid)
        sendGuild(MaplePacketCreator.createGuildAlliance(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.getAllianceInfo(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.getGuildAlliance(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.changeAlliance(alliance, True), -1, allianceid)
        return True

    def allianceChat(self, gid: int, name: str, cid: int, msg: str) -> None:
        g = Guild.getGuild(gid)
        if g is not None:
            ga = getAlliance(g.getAllianceId())
            if ga is not None:
                for i in range(ga.getNoGuilds()):
                    g_ = Guild.getGuild(ga.getGuildId(i))
                    if g_ is not None:
                        g_.allianceChat(name, cid, msg)

    def setNewAlliance(self, gid: int, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        guild = Guild.getGuild(gid)
        if alliance is not None and guild is not None:
            for i in range(alliance.getNoGuilds()):
                if gid == alliance.getGuildId(i):
                    guild.setAllianceId(allianceid)
                    guild.broadcast(MaplePacketCreator.getAllianceInfo(alliance))
                    guild.broadcast(MaplePacketCreator.getGuildAlliance(alliance))
                    guild.broadcast(MaplePacketCreator.changeAlliance(alliance, True))
                    guild.changeARank()
                    guild.writeToDB(False)
                else:
                    g_ = Guild.getGuild(alliance.getGuildId(i))
                    if g_ is not None:
                        g_.broadcast(MaplePacketCreator.addGuildToAlliance(alliance, guild))
                        g_.broadcast(MaplePacketCreator.changeGuildInAlliance(alliance, guild, True))

    def setOldAlliance(self, gid: int, expelled: bool, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        g_ = Guild.getGuild(gid)
        if alliance is not None:
            for i in range(alliance.getNoGuilds()):
                guild = Guild.getGuild(alliance.getGuildId(i))
                if guild is None:
                    if gid != alliance.getGuildId(i):
                        alliance.removeGuild(gid, False)
                elif g_ is None or gid == alliance.getGuildId(i):
                    guild.changeARank(5)
                    guild.setAllianceId(0)
                    guild.broadcast(MaplePacketCreator.disbandAlliance(allianceid))
                elif g_ is not None:
                    guild.broadcast(MaplePacketCreator.serverNotice(5, "[" + g_.getName() + "] Guild has left the alliance."))
                    guild.broadcast(MaplePacketCreator.changeGuildInAlliance(alliance, g_, False))
                    guild.broadcast(MaplePacketCreator.removeGuildFromAlliance(alliance, g_, expelled))
        if gid == -1:
            Alliance.lock.writeLock().lock()
            try:
                Alliance.alliances.remove(allianceid)
            finally:
                Alliance.lock.writeLock().unlock()

    def getAllianceInfo(self, allianceid: int, start: bool) -> list:
        ret = []
        alliance = getAlliance(allianceid)
        if alliance is not None:
            if start:
                ret.add(MaplePacketCreator.getAllianceInfo(alliance))
                ret.add(MaplePacketCreator.getGuildAlliance(alliance))
            ret.add(MaplePacketCreator.getAllianceUpdate(alliance))
        return ret

    @staticmethod
    def getFamily(id: int) -> Any:
        ret = None
        Family.lock.readLock().lock()
        try:
            ret = Family.families.get(id)
        finally:
            Family.lock.readLock().unlock()
        if ret is None:
            Family.lock.writeLock().lock()
            try:
                ret = MapleFamily(id)
                if ret is None or ret.getId() <= 0 or not ret.isProper():
                    return None
                Family.families.put(id, ret)
            finally:
                Family.lock.writeLock().unlock()
        return ret

    def memberFamilyUpdate(self, mfc: Any, mc: Any) -> None:
        f = getFamily(mfc.getFamilyId())
        if f is not None:
            f.memberLevelJobUpdate(mc)

    def setFamilyMemberOnline(self, mfc: Any, bOnline: bool, channel: int) -> None:
        f = getFamily(mfc.getFamilyId())
        if f is not None:
            f.setOnline(mfc.getId(), bOnline, channel)

    def setRep(self, fid: int, cid: int, addrep: int, oldLevel: int) -> int:
        f = getFamily(fid)
        if f is not None:
            return f.setRep(cid, addrep, oldLevel)
        return 0

    def setFamily(self, familyid: int, seniorid: int, junior1: int, junior2: int, currentrep: int, totalrep: int, cid: int) -> None:
        ch = Find.findChannel(cid)
        if ch == -1:
            return
        mc = World.getStorage(ch).getCharacterById(cid)
        if mc is None:
            return
        bDifferent = mc.getFamilyId() != familyid or mc.getSeniorId() != seniorid or mc.getJunior1() != junior1 or mc.getJunior2() != junior2
        mc.setFamily(familyid, seniorid, junior1, junior2)
        mc.setCurrentRep(currentrep)
        mc.setTotalRep(totalrep)
        if bDifferent:
            mc.saveFamilyStatus()

    def familyPacket(self, gid: int, message: Any, cid: int) -> None:
        f = getFamily(gid)
        if f is not None:
            f.broadcast(message, -1, f.getMFC(cid).getPedigree())

    def disbandFamily(self, gid: int) -> None:
        g = getFamily(gid)
        Family.lock.writeLock().lock()
        try:
            if g is not None:
                g.disbandFamily()
                Family.families.remove(gid)
        finally:
            Family.lock.writeLock().unlock()


# Inner class from Java (originally nested)
class Party:
    """
    Class Party
    """

    # Static initializer
    # Party.parties = {}
    # Party.runningPartyId = AtomicInteger()
    # con = DatabaseConnection.getConnection()
    # try:
    # ps = con.prepareStatement("SELECT MAX(party)+2 FROM characters")
    # rs = ps.executeQuery()
    # rs.next()
    # Party.runningPartyId.set(rs.getInt(1))
    # rs.close()
    # ps.close()
    # except Exception as e:
    # e.printStackTrace()


    @staticmethod
    def partyChat(partyid: int, chattext: str, namefrom: str) -> None:
        party = getParty(partyid)
        if party is None:
            raise ValueError("no party with the specified partyid exists")
        for partychar in party.getMembers():
            ch = Find.findChannel(partychar.getName())
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(partychar.getName())
                if chr is None or chr.getName().lower() == namefrom.lower():
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.multiChat(namefrom, chattext, 1))

    def updateParty(self, partyid: int, operation: Any, target: Any) -> None:
        party = getParty(partyid)
        if party is None:
            return
        # switch (operation):
            # case JOIN:
                party.addMember(target)
                break
            # case EXPEL:
            # case LEAVE:
                party.removeMember(target)
                break
            # case DISBAND:
                disbandParty(partyid)
                break
            # case SILENT_UPDATE:
            # case LOG_ONOFF:
                party.updateMember(target)
                break
            # case CHANGE_LEADER:
                party.setLeader(target)
                break
            # default:
                raise RuntimeError("Unhandeled updateParty operation " + operation.name())
        for partychar in party.getMembers():
            ch = Find.findChannel(partychar.getName())
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(partychar.getName())
                if chr is None:
                    continue
                if operation == PartyOperation.DISBAND:
                    chr.setParty(None)
                else:
                    chr.setParty(party)
                chr.getClient().getSession().write(MaplePacketCreator.updateParty(chr.getClient().getChannel(), party, operation, target))
        # switch (operation):
            # case EXPEL:
            # case LEAVE:
                ch2 = Find.findChannel(target.getName())
                if ch2 <= 0:
                    break
                chr2 = ChannelServer.getInstance(ch2).getPlayerStorage().getCharacterByName(target.getName())
                if chr2 is not None:
                    chr2.getClient().getSession().write(MaplePacketCreator.updateParty(chr2.getClient().getChannel(), party, operation, target))
                    chr2.setParty(None)
                    break
                break

    def createParty(self, chrfor: Any) -> Any:
        partyid = Party.runningPartyId.getAndIncrement()
        party = MapleParty(partyid, chrfor)
        Party.parties.put(party.getId(), party)
        return party

    def getParty(self, partyid: int) -> Any:
        return Party.parties.get(partyid)

    def disbandParty(self, partyid: int) -> Any:
        return Party.parties.remove(partyid)


# Inner class from Java (originally nested)
class Buddy:
    """
    Class Buddy
    """


    def buddyChat(self, recipientCharacterIds: list, cidFrom: int, nameFrom: str, chattext: str) -> None:
        for characterId in recipientCharacterIds:
            ch = Find.findChannel(characterId)
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(characterId)
                if chr is not None and chr.getBuddylist().containsVisible(cidFrom):
                    chr.getClient().getSession().write(MaplePacketCreator.multiChat(nameFrom, chattext, 0))

    def updateBuddies(self, characterId: int, channel: int, buddies: list, offline: bool, gmLevel: int, isHidden: bool) -> None:
        for buddy in buddies:
            ch = Find.findChannel(buddy)
            if ch > 0:
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(buddy)
                if chr is None:
                    continue
                ble = chr.getBuddylist().get(characterId)
                if ble is None or not ble.isVisible():
                    continue
                mcChannel = None
                if offline or (isHidden and chr.getGMLevel() < gmLevel):
                    ble.setChannel(-1)
                    mcChannel = -1
                else:
                    ble.setChannel(channel)
                    mcChannel = channel - 1
                chr.getBuddylist().put(ble)
                chr.getClient().sendPacket(MaplePacketCreator.updateBuddyChannel(ble.getCharacterId(), mcChannel))

    def buddyChanged(self, cid: int, cidFrom: int, name: str, channel: int, operation: Any, level: int, job: int, group: str) -> None:
        ch = Find.findChannel(cid)
        if ch > 0:
            addChar = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(cid)
            if addChar is not None:
                buddylist = addChar.getBuddylist()
                # switch (operation):
                    # case ADDED:
                        if (cidFrom in buddylist):
                            buddylist.put(BuddyEntry(name, cidFrom, group, channel, True, level, job))
                            addChar.getClient().getSession().write(MaplePacketCreator.updateBuddyChannel(cidFrom, channel - 1))
                            break
                        break
                    # case DELETED:
                        if (cidFrom in buddylist):
                            buddylist.put(BuddyEntry(name, cidFrom, group, -1, buddylist.get(cidFrom).isVisible(), level, job))
                            addChar.getClient().getSession().write(MaplePacketCreator.updateBuddyChannel(cidFrom, -1))
                            break
                        break

    def requestBuddyAdd(self, addName: str, channelFrom: int, cidFrom: int, nameFrom: str, levelFrom: int, jobFrom: int) -> Any:
        ch = Find.findChannel(cidFrom)
        if ch > 0:
            addChar = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(addName)
            if addChar is not None:
                buddylist = addChar.getBuddylist()
                if buddylist.isFull():
                    return BuddyList.BuddyAddResult.BUDDYLIST_FULL
                if not (cidFrom in buddylist):
                    buddylist.addBuddyRequest(addChar.getClient(), cidFrom, nameFrom, channelFrom, levelFrom, jobFrom)
                elif buddylist.containsVisible(cidFrom):
                    return BuddyList.BuddyAddResult.ALREADY_ON_LIST
        return BuddyList.BuddyAddResult.OK

    def loggedOn(self, name: str, characterId: int, channel: int, buddies: list, gmLevel: int, isHidden: bool) -> None:
        updateBuddies(characterId, channel, buddies, False, gmLevel, isHidden)

    def loggedOff(self, name: str, characterId: int, channel: int, buddies: list, gmLevel: int, isHidden: bool) -> None:
        updateBuddies(characterId, channel, buddies, True, gmLevel, isHidden)


# Inner class from Java (originally nested)
class Messenger:
    """
    Class Messenger
    """

    # Static initializer
    # messengers = {}
    # (runningMessengerId = AtomicInteger()).set(1)


    @staticmethod
    def createMessenger(chrfor: Any) -> Any:
        messengerid = Messenger.runningMessengerId.getAndIncrement()
        messenger = MapleMessenger(messengerid, chrfor)
        Messenger.messengers.put(messenger.getId(), messenger)
        return messenger

    def declineChat(self, target: str, namefrom: str) -> None:
        ch = Find.findChannel(target)
        if ch > 0:
            cs = ChannelServer.getInstance(ch)
            chr = cs.getPlayerStorage().getCharacterByName(target)
            if chr is not None:
                messenger = chr.getMessenger()
                if messenger is not None:
                    chr.getClient().getSession().write(MaplePacketCreator.messengerNote(namefrom, 5, 0))

    def getMessenger(self, messengerid: int) -> Any:
        return Messenger.messengers.get(messengerid)

    def leaveMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        position = messenger.getPositionByName(target.getName())
        messenger.removeMember(target)
        for mmc in messenger.getMembers():
            if mmc is not None:
                ch = Find.findChannel(mmc.getId())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(mmc.getName())
                if chr is None:
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.removeMessengerPlayer(position))

    def silentLeaveMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.silentRemoveMember(target)

    def silentJoinMessenger(self, messengerid: int, target: Any) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.silentAddMember(target)

    def updateMessenger(self, messengerid: int, namefrom: str, fromchannel: int) -> None:
        messenger = getMessenger(messengerid)
        position = messenger.getPositionByName(namefrom)
        for messengerchar in messenger.getMembers():
            if messengerchar is not None and not messengerchar.getName() == (namefrom):
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                from = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(namefrom)
                chr.getClient().getSession().write(MaplePacketCreator.updateMessengerPlayer(namefrom, from, position, fromchannel - 1))

    def joinMessenger(self, messengerid: int, target: Any, from: str, fromchannel: int) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        messenger.addMember(target)
        position = messenger.getPositionByName(target.getName())
        for messengerchar in messenger.getMembers():
            if messengerchar is not None:
                mposition = messenger.getPositionByName(messengerchar.getName())
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                if not messengerchar.getName() == (from):
                    fromCh = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(from)
                    chr.getClient().getSession().write(MaplePacketCreator.addMessengerPlayer(from, fromCh, position, fromchannel - 1))
                    fromCh.getClient().getSession().write(MaplePacketCreator.addMessengerPlayer(chr.getName(), chr, mposition, messengerchar.getChannel() - 1))
                else:
                    chr.getClient().getSession().write(MaplePacketCreator.joinMessenger(mposition))

    def messengerChat(self, messengerid: int, chattext: str, namefrom: str) -> None:
        messenger = getMessenger(messengerid)
        if messenger is None:
            raise ValueError("No messenger with the specified messengerid exists")
        for messengerchar in messenger.getMembers():
            if messengerchar is not None and not messengerchar.getName() == (namefrom):
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())
                if chr is None:
                    continue
                chr.getClient().getSession().write(MaplePacketCreator.messengerChat(chattext))
            else:
                if messengerchar is None:
                    continue
                ch = Find.findChannel(messengerchar.getName())
                if ch <= 0:
                    continue
                ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(messengerchar.getName())

    def messengerInvite(self, sender: str, messengerid: int, target: str, fromchannel: int, gm: bool) -> None:
        if World.isConnected(target):
            ch = Find.findChannel(target)
            if ch > 0:
                from = ChannelServer.getInstance(fromchannel).getPlayerStorage().getCharacterByName(sender)
                targeter = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(target)
                if targeter is not None and targeter.getMessenger() is None:
                    if not targeter.isGM() or gm:
                        targeter.getClient().getSession().write(MaplePacketCreator.messengerInvite(sender, messengerid))
                        from.getClient().getSession().write(MaplePacketCreator.messengerNote(target, 4, 1))
                    else:
                        from.getClient().getSession().write(MaplePacketCreator.messengerNote(target, 4, 0))
                else:
                    from.getClient().getSession().write(MaplePacketCreator.messengerChat(sender + " : " + target + " is already using Maple Messenger"))


# Inner class from Java (originally nested)
class Guild:
    """
    Class Guild
    """

    # Static initializer
    # guilds = {}
    # Guild.lock = ReentrantReadWriteLock()
    # print("加载 家族 :::")
    # allGuilds = MapleGuild.loadAll()
    # for g in allGuilds:
    # if g.isProper():
    # Guild.guilds.put(g.getId(), g)


    @staticmethod
    def createGuild(leaderId: int, name: str) -> int:
        return MapleGuild.createGuild(leaderId, name)

    def getGuild(self, id: int) -> Any:
        ret = None
        Guild.lock.readLock().lock()
        try:
            ret = Guild.guilds.get(id)
        finally:
            Guild.lock.readLock().unlock()
        if ret is None:
            Guild.lock.writeLock().lock()
            try:
                ret = MapleGuild(id)
                if ret is None or ret.getId() <= 0 or not ret.isProper():
                    return None
                Guild.guilds.put(id, ret)
            finally:
                Guild.lock.writeLock().unlock()
        return ret

    def getGuildByName(self, guildName: str) -> Any:
        Guild.lock.readLock().lock()
        try:
            for g in Guild.guilds.values():
                if g.getName().lower() == guildName.lower():
                    return g
            return None
        finally:
            Guild.lock.readLock().unlock()

    def getGuild_mc(self, mc: Any) -> Any:
        return getGuild(mc.getGuildId())

    def setGuildMemberOnline(self, mc: Any, bOnline: bool, channel: int) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.setOnline(mc.getId(), bOnline, channel)

    def guildPacket(self, gid: int, message: Any) -> None:
        g = getGuild(gid)
        if g is not None:
            g.broadcast(message)

    def addGuildMember(self, mc: Any) -> int:
        g = getGuild(mc.getGuildId())
        if g is not None:
            return g.addGuildMember(mc)
        return 0

    def leaveGuild(self, mc: Any) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.leaveGuild(mc)

    def guildChat(self, gid: int, name: str, cid: int, msg: str) -> None:
        g = getGuild(gid)
        if g is not None:
            g.guildChat(name, cid, msg)

    def changeRank(self, gid: int, cid: int, newRank: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.changeRank(cid, newRank)

    def expelMember(self, initiator: Any, name: str, cid: int) -> None:
        g = getGuild(initiator.getGuildId())
        if g is not None:
            g.expelMember(initiator, name, cid)

    def setGuildNotice(self, gid: int, notice: str) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setGuildNotice(notice)

    def memberLevelJobUpdate(self, mc: Any) -> None:
        g = getGuild(mc.getGuildId())
        if g is not None:
            g.memberLevelJobUpdate(mc)

    def changeRankTitle(self, gid: int, ranks: list) -> None:
        g = getGuild(gid)
        if g is not None:
            g.changeRankTitle(ranks)

    def setGuildEmblem(self, gid: int, bg: int, bgcolor: int, logo: int, logocolor: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setGuildEmblem(bg, bgcolor, logo, logocolor)

    def disbandGuild(self, gid: int) -> None:
        g = getGuild(gid)
        Guild.lock.writeLock().lock()
        try:
            if g is not None:
                g.disbandGuild()
                Guild.guilds.remove(gid)
        finally:
            Guild.lock.writeLock().unlock()

    def deleteGuildCharacter(self, guildid: int, charid: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            mc = g.getMGC(charid)
            if mc is not None:
                if mc.getGuildRank() > 1:
                    g.leaveGuild(mc)
                else:
                    g.disbandGuild()

    def increaseGuildCapacity(self, gid: int) -> bool:
        g = getGuild(gid)
        return g is not None and g.increaseCapacity()

    def gainGP(self, gid: int, amount: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.gainGP(amount)

    def getGP(self, gid: int) -> int:
        g = getGuild(gid)
        if g is not None:
            return g.getGP()
        return 0

    def getInvitedId(self, gid: int) -> int:
        g = getGuild(gid)
        if g is not None:
            return g.getInvitedId()
        return 0

    def setInvitedId(self, gid: int, inviteid: int) -> None:
        g = getGuild(gid)
        if g is not None:
            g.setInvitedId(inviteid)

    def getGuildLeader(self, guildName: str) -> int:
        mga = getGuildByName(guildName)
        if mga is not None:
            return mga.getLeaderId()
        return 0

    def save(self) -> None:
        print("Saving guilds...")
        Guild.lock.writeLock().lock()
        try:
            for a in Guild.guilds.values():
                a.writeToDB(False)
        finally:
            Guild.lock.writeLock().unlock()

    def getBBS(self, gid: int) -> list:
        g = getGuild(gid)
        if g is not None:
            return g.getBBS()
        return None

    def addBBSThread(self, guildid: int, title: str, text: str, icon: int, bNotice: bool, posterID: int) -> int:
        g = getGuild(guildid)
        if g is not None:
            return g.addBBSThread(title, text, icon, bNotice, posterID)
        return -1

    def editBBSThread(self, guildid: int, localthreadid: int, title: str, text: str, icon: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.editBBSThread(localthreadid, title, text, icon, posterID, guildRank)

    def deleteBBSThread(self, guildid: int, localthreadid: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.deleteBBSThread(localthreadid, posterID, guildRank)

    def addBBSReply(self, guildid: int, localthreadid: int, text: str, posterID: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.addBBSReply(localthreadid, text, posterID)

    def deleteBBSReply(self, guildid: int, localthreadid: int, replyid: int, posterID: int, guildRank: int) -> None:
        g = getGuild(guildid)
        if g is not None:
            g.deleteBBSReply(localthreadid, replyid, posterID, guildRank)

    def changeEmblem(self, gid: int, affectedPlayers: int, mgs: Any) -> None:
        Broadcast.sendGuildPacket(affectedPlayers, MaplePacketCreator.guildEmblemChange(gid, mgs.getLogoBG(), mgs.getLogoBGColor(), mgs.getLogo(), mgs.getLogoColor()), -1, gid)
        setGuildAndRank(affectedPlayers, -1, -1, -1)

    def setGuildAndRank(self, cid: int, guildid: int, rank: int, alliancerank: int) -> None:
        ch = Find.findChannel(cid)
        if ch == -1:
            return
        mc = World.getStorage(ch).getCharacterById(cid)
        if mc is None:
            return
        bDifferentGuild = None
        if guildid == -1 and rank == -1:
            bDifferentGuild = True
        else:
            bDifferentGuild = (guildid != mc.getGuildId())
            mc.setGuildId(guildid)
            mc.setGuildRank(rank)
            mc.setAllianceRank(alliancerank)
            mc.saveGuildStatus()
        if bDifferentGuild and ch > 0:
            mc.getMap().broadcastMessage(mc, MaplePacketCreator.removePlayerFromMap(cid, mc), False)
            mc.getMap().broadcastMessage(mc, MaplePacketCreator.spawnPlayerMapobject(mc), False)


# Inner class from Java (originally nested)
class Broadcast:
    """
    Class Broadcast
    """


    def broadcastSmega(self, message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastSmega(message)

    def broadcastGMMessage(self, message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastGMMessage(message)

    def broadcastMessage(self, message: bytes) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastMessage(message)

    def sendPacket(self, targetIds: list, packet: Any, exception: int) -> None:
        for i in targetIds:
            if i == exception:
                continue
            ch = Find.findChannel(i)
            if ch < 0:
                continue
            c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(i)
            if c is None:
                continue
            c.getClient().getSession().write(packet)

    def sendGuildPacket(self, targetIds: int, packet: Any, exception: int, guildid: int) -> None:
        if targetIds == exception:
            return
        ch = Find.findChannel(targetIds)
        if ch < 0:
            return
        c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(targetIds)
        if c is not None and c.getGuildId() == guildid:
            c.getClient().getSession().write(packet)

    def sendFamilyPacket(self, targetIds: int, packet: Any, exception: int, guildid: int) -> None:
        if targetIds == exception:
            return
        ch = Find.findChannel(targetIds)
        if ch < 0:
            return
        c = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterById(targetIds)
        if c is not None and c.getFamilyId() == guildid:
            c.getClient().getSession().write(packet)

    def broadcastMessage_serverNotice(self, serverNotice: Any) -> None:
        for cs in ChannelServer.getAllInstances():
            cs.broadcastMessage(serverNotice)


# Inner class from Java (originally nested)
class Client:
    """
    Class Client
    """

    # Static initializer
    # clients = []


    @staticmethod
    def addClient(c: Any) -> None:
        if not (c in Client.clients):
            Client.clients.add(c)

    def removeClient(self, c: Any) -> bool:
        return Client.clients.remove(c)

    def getClients(self) -> list:
        return Client.clients


# Inner class from Java (originally nested)
class Find:
    """
    Class Find
    """

    # Static initializer
    # lock = ReentrantReadWriteLock()
    # idToChannel = {}
    # nameToChannel = {}


    @staticmethod
    def register(id: int, name: str, channel: int) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.put(id, channel)
            Find.nameToChannel.put(name.lower(), channel)
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister(self, id: int) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.remove(id)
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister_id(self, id: str) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.nameToChannel.remove(id.lower())
        finally:
            Find.lock.writeLock().unlock()

    def forceDeregister_id_name(self, id: int, name: str) -> None:
        Find.lock.writeLock().lock()
        try:
            Find.idToChannel.remove(id)
            Find.nameToChannel.remove(name.lower())
        finally:
            Find.lock.writeLock().unlock()

    def findChannel(self, id: int) -> int:
        Find.lock.readLock().lock()
        ret = None
        try:
            ret = Find.idToChannel.get(id)
        finally:
            Find.lock.readLock().unlock()
        if ret is None:
            return -1
        if ret != -10 and ret != -20 and ChannelServer.getInstance(ret) is None:
            forceDeregister(id)
            return -1
        return ret

    def findChannel_st(self, st: str) -> int:
        Find.lock.readLock().lock()
        ret = None
        try:
            ret = Find.nameToChannel.get(st.lower())
        finally:
            Find.lock.readLock().unlock()
        if ret is None:
            return -1
        if ret != -10 and ret != -20 and ChannelServer.getInstance(ret) is None:
            forceDeregister(st)
            return -1
        return ret

    def multiBuddyFind(self, charIdFrom: int, characterIds: list) -> list:
        foundsChars = [])
        for i in characterIds:
            channel = findChannel(i)
            if channel > 0:
                foundsChars.add(CharacterIdChannelPair(i, channel))
        Collections.sort(foundsChars)
        return foundsChars])


# Inner class from Java (originally nested)
class Alliance:
    """
    Class Alliance
    """

    # Static initializer
    # alliances = {}
    # Alliance.lock = ReentrantReadWriteLock()
    # print("加载 家族联盟 :::")
    # allGuilds = MapleGuildAlliance.loadAll()
    # for g in allGuilds:
    # Alliance.alliances.put(g.getId(), g)


    @staticmethod
    def getAlliance(allianceid: int) -> Any:
        ret = None
        Alliance.lock.readLock().lock()
        try:
            ret = Alliance.alliances.get(allianceid)
        finally:
            Alliance.lock.readLock().unlock()
        if ret is None:
            Alliance.lock.writeLock().lock()
            try:
                ret = MapleGuildAlliance(allianceid)
                if ret is None or ret.getId() <= 0:
                    return None
                Alliance.alliances.put(allianceid, ret)
            finally:
                Alliance.lock.writeLock().unlock()
        return ret

    def getAllianceLeader(self, allianceid: int) -> int:
        mga = getAlliance(allianceid)
        if mga is not None:
            return mga.getLeaderId()
        return 0

    def updateAllianceRanks(self, allianceid: int, ranks: list) -> None:
        mga = getAlliance(allianceid)
        if mga is not None:
            mga.setRank(ranks)

    def updateAllianceNotice(self, allianceid: int, notice: str) -> None:
        mga = getAlliance(allianceid)
        if mga is not None:
            mga.setNotice(notice)

    def canInvite(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.getCapacity() > mga.getNoGuilds()

    def changeAllianceLeader(self, allianceid: int, cid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.setLeaderId(cid)

    def changeAllianceRank(self, allianceid: int, cid: int, change: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.changeAllianceRank(cid, change)

    def changeAllianceCapacity(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.setCapacity()

    def disbandAlliance(self, allianceid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.disband()

    def addGuildToAlliance(self, allianceid: int, gid: int) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.addGuild(gid)

    def removeGuildFromAlliance(self, allianceid: int, gid: int, expelled: bool) -> bool:
        mga = getAlliance(allianceid)
        return mga is not None and mga.removeGuild(gid, expelled)

    def sendGuild(self, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        if alliance is not None:
            sendGuild(MaplePacketCreator.getAllianceUpdate(alliance), -1, allianceid)
            sendGuild(MaplePacketCreator.getGuildAlliance(alliance), -1, allianceid)

    def sendGuild_packet_exceptionId_allianceid(self, packet: Any, exceptionId: int, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        if alliance is not None:
            for i in range(alliance.getNoGuilds()):
                gid = alliance.getGuildId(i)
                if gid > 0 and gid != exceptionId:
                    Guild.guildPacket(gid, packet)

    def createAlliance(self, alliancename: str, cid: int, cid2: int, gid: int, gid2: int) -> bool:
        allianceid = MapleGuildAlliance.createToDb(cid, alliancename, gid, gid2)
        if allianceid <= 0:
            return False
        g = Guild.getGuild(gid)
        g_ = Guild.getGuild(gid2)
        g.setAllianceId(allianceid)
        g_.setAllianceId(allianceid)
        g.changeARank(True)
        g_.changeARank(False)
        alliance = getAlliance(allianceid)
        sendGuild(MaplePacketCreator.createGuildAlliance(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.getAllianceInfo(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.getGuildAlliance(alliance), -1, allianceid)
        sendGuild(MaplePacketCreator.changeAlliance(alliance, True), -1, allianceid)
        return True

    def allianceChat(self, gid: int, name: str, cid: int, msg: str) -> None:
        g = Guild.getGuild(gid)
        if g is not None:
            ga = getAlliance(g.getAllianceId())
            if ga is not None:
                for i in range(ga.getNoGuilds()):
                    g_ = Guild.getGuild(ga.getGuildId(i))
                    if g_ is not None:
                        g_.allianceChat(name, cid, msg)

    def setNewAlliance(self, gid: int, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        guild = Guild.getGuild(gid)
        if alliance is not None and guild is not None:
            for i in range(alliance.getNoGuilds()):
                if gid == alliance.getGuildId(i):
                    guild.setAllianceId(allianceid)
                    guild.broadcast(MaplePacketCreator.getAllianceInfo(alliance))
                    guild.broadcast(MaplePacketCreator.getGuildAlliance(alliance))
                    guild.broadcast(MaplePacketCreator.changeAlliance(alliance, True))
                    guild.changeARank()
                    guild.writeToDB(False)
                else:
                    g_ = Guild.getGuild(alliance.getGuildId(i))
                    if g_ is not None:
                        g_.broadcast(MaplePacketCreator.addGuildToAlliance(alliance, guild))
                        g_.broadcast(MaplePacketCreator.changeGuildInAlliance(alliance, guild, True))

    def setOldAlliance(self, gid: int, expelled: bool, allianceid: int) -> None:
        alliance = getAlliance(allianceid)
        g_ = Guild.getGuild(gid)
        if alliance is not None:
            for i in range(alliance.getNoGuilds()):
                guild = Guild.getGuild(alliance.getGuildId(i))
                if guild is None:
                    if gid != alliance.getGuildId(i):
                        alliance.removeGuild(gid, False)
                elif g_ is None or gid == alliance.getGuildId(i):
                    guild.changeARank(5)
                    guild.setAllianceId(0)
                    guild.broadcast(MaplePacketCreator.disbandAlliance(allianceid))
                elif g_ is not None:
                    guild.broadcast(MaplePacketCreator.serverNotice(5, "[" + g_.getName() + "] Guild has left the alliance."))
                    guild.broadcast(MaplePacketCreator.changeGuildInAlliance(alliance, g_, False))
                    guild.broadcast(MaplePacketCreator.removeGuildFromAlliance(alliance, g_, expelled))
        if gid == -1:
            Alliance.lock.writeLock().lock()
            try:
                Alliance.alliances.remove(allianceid)
            finally:
                Alliance.lock.writeLock().unlock()

    def getAllianceInfo(self, allianceid: int, start: bool) -> list:
        ret = []
        alliance = getAlliance(allianceid)
        if alliance is not None:
            if start:
                ret.add(MaplePacketCreator.getAllianceInfo(alliance))
                ret.add(MaplePacketCreator.getGuildAlliance(alliance))
            ret.add(MaplePacketCreator.getAllianceUpdate(alliance))
        return ret

    def save(self) -> None:
        print("Saving alliances...")
        Alliance.lock.writeLock().lock()
        try:
            for a in Alliance.alliances.values():
                a.saveToDb()
        finally:
            Alliance.lock.writeLock().unlock()


# Inner class from Java (originally nested)
class Family:
    """
    Class Family
    """

    # Static initializer
    # families = {}
    # Family.lock = ReentrantReadWriteLock()
    # print("加载 冒险学院 :::")
    # allGuilds = MapleFamily.loadAll()
    # for g in allGuilds:
    # if g.isProper():
    # Family.families.put(g.getId(), g)


    @staticmethod
    def getFamily(id: int) -> Any:
        ret = None
        Family.lock.readLock().lock()
        try:
            ret = Family.families.get(id)
        finally:
            Family.lock.readLock().unlock()
        if ret is None:
            Family.lock.writeLock().lock()
            try:
                ret = MapleFamily(id)
                if ret is None or ret.getId() <= 0 or not ret.isProper():
                    return None
                Family.families.put(id, ret)
            finally:
                Family.lock.writeLock().unlock()
        return ret

    def memberFamilyUpdate(self, mfc: Any, mc: Any) -> None:
        f = getFamily(mfc.getFamilyId())
        if f is not None:
            f.memberLevelJobUpdate(mc)

    def setFamilyMemberOnline(self, mfc: Any, bOnline: bool, channel: int) -> None:
        f = getFamily(mfc.getFamilyId())
        if f is not None:
            f.setOnline(mfc.getId(), bOnline, channel)

    def setRep(self, fid: int, cid: int, addrep: int, oldLevel: int) -> int:
        f = getFamily(fid)
        if f is not None:
            return f.setRep(cid, addrep, oldLevel)
        return 0

    def save(self) -> None:
        print("Saving families...")
        Family.lock.writeLock().lock()
        try:
            for a in Family.families.values():
                a.writeToDB(False)
        finally:
            Family.lock.writeLock().unlock()

    def setFamily(self, familyid: int, seniorid: int, junior1: int, junior2: int, currentrep: int, totalrep: int, cid: int) -> None:
        ch = Find.findChannel(cid)
        if ch == -1:
            return
        mc = World.getStorage(ch).getCharacterById(cid)
        if mc is None:
            return
        bDifferent = mc.getFamilyId() != familyid or mc.getSeniorId() != seniorid or mc.getJunior1() != junior1 or mc.getJunior2() != junior2
        mc.setFamily(familyid, seniorid, junior1, junior2)
        mc.setCurrentRep(currentrep)
        mc.setTotalRep(totalrep)
        if bDifferent:
            mc.saveFamilyStatus()

    def familyPacket(self, gid: int, message: Any, cid: int) -> None:
        f = getFamily(gid)
        if f is not None:
            f.broadcast(message, -1, f.getMFC(cid).getPedigree())

    def disbandFamily(self, gid: int) -> None:
        g = getFamily(gid)
        Family.lock.writeLock().lock()
        try:
            if g is not None:
                g.disbandFamily()
                Family.families.remove(gid)
        finally:
            Family.lock.writeLock().unlock()


# Inner class from Java (originally nested)
class Respawn(Runnable):
    """
    Class Respawn
    Implements: Runnable
    """

    def __init__(self):
        self.numTimes = 0
        self.numTimes = 0


    def run(self) -> None:
        self.numTimes += 1
        for cserv in ChannelServer.getAllInstances():
            for map in cserv.getMapFactory().getAllMaps():
                World.handleMap(map, self.numTimes, map.getCharactersSize())
            for map in cserv.getMapFactory().getAllInstanceMaps():
                World.handleMap(map, self.numTimes, map.getCharactersSize())

