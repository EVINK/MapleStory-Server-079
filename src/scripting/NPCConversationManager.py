"""
NPCConversationManager - Converted from Java source
Original: scripting/NPCConversationManager.java
Package: scripting
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from socket import socket
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import logging
import math
import pymysql
import threading
import time
import tkinter

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.SkillEntry import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.channel.MapleGuildRanking import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.CharacterTransfer import *  # TODO: import specific classes
# from handling.world.MapleMessengerCharacter import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PlayerBuffStorage import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildAlliance import *  # TODO: import specific classes
# from server.MapleCarnivalChallenge import *  # TODO: import specific classes
# from server.MapleCarnivalParty import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.MapleShopFactory import *  # TODO: import specific classes
# from server.MapleSquad import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.MerchItemPackage import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.SpeedRunner import *  # TODO: import specific classes
# from server.StructPotentialItem import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.custom.forum.Forum_Reply import *  # TODO: import specific classes
# from server.custom.forum.Forum_Section import *  # TODO: import specific classes
# from server.custom.forum.Forum_Thread import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MapleMonsterInformationProvider import *  # TODO: import specific classes
# from server.life.MonsterDropEntry import *  # TODO: import specific classes
# from server.life.MonsterGlobalDropEntry import *  # TODO: import specific classes
# from server.maps.AramiaFireWorks import *  # TODO: import specific classes
# from server.maps.Event_DojoAgent import *  # TODO: import specific classes
# from server.maps.Event_PyramidSubway import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.SpeedRunType import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class NPCConversationManager(AbstractPlayerInteraction):
    """
    Class NPCConversationManager
    Extends: AbstractPlayerInteraction
    """

    def __init__(self, c: Any, npc: int, questid: int, type: int, iv: Any, wh: int):
        self.c = None
        self.npc = None
        self.questid = None
        self.getText = ""
        self.type = None
        self.lastMsg = 0
        self.pendingDisposal = False
        self.iv = None
        self.wh = 0
        super(c)
        self.lastMsg = -1
        self.pendingDisposal = False
        self.wh = 0
        self.c = c
        self.npc = npc
        self.questid = questid
        self.type = type
        self.iv = iv
        self.wh = wh


    def loadItemFrom_Database(self, charid: int, accountid: int) -> Any:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * from hiredmerch where characterid = ? OR accountid = ?")
            ps.setInt(1, charid)
            ps.setInt(2, accountid)
            rs = ps.executeQuery()
            if not rs.next():
                ps.close()
                rs.close()
                return None
            packageid = rs.getInt("PackageId")
            pack = MerchItemPackage()
            pack.setPackageid(packageid)
            pack.setMesos(rs.getInt("Mesos"))
            pack.setSentTime(rs.getLong("time"))
            ps.close()
            rs.close()
            items = ItemLoader.HIRED_MERCHANT.loadItems(False, charid)
            if items is not None:
                iters = []
                for z in items.values():
                    iters.add(z.left)
                pack.setItems(iters)
            return pack
        except Exception as e:
            e.printStackTrace()
            return None

    def hairExists(self, hair: int) -> bool:
        return MapleItemInformationProvider.getInstance().hairExists(hair)

    def faceExists(self, face: int) -> bool:
        return MapleItemInformationProvider.getInstance().faceExists(face)

    def getwh(self) -> int:
        return self.wh

    def ms(self) -> str:
        result = "缘分"
        return result

    def getIv(self) -> Any:
        return self.iv

    def serverName(self) -> str:
        return self.c.getChannelServer().getServerName()

    def getNpc(self) -> int:
        return self.npc

    def getQuest(self) -> int:
        return self.questid

    def getType(self) -> int:
        return self.type

    def safeDispose(self) -> None:
        self.pendingDisposal = True

    def dispose(self) -> None:
        NPCScriptManager.getInstance().dispose(self.c)

    def askMapSelection(self, sel: str) -> None:
        if self.lastMsg > -1:
            return
        self.c.getSession().write(MaplePacketCreator.getMapSelection(self.npc, sel))
        self.lastMsg = 13

    def sendNext(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "00 01", 0))
        self.lastMsg = 0

    def sendNextS(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimpleS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "00 01", type))
        self.lastMsg = 0

    def sendPrev(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "01 00", 0))
        self.lastMsg = 0

    def sendPrevS(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimpleS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "01 00", type))
        self.lastMsg = 0

    def sendNextPrev(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "01 01", 0))
        self.lastMsg = 0

    def PlayerToNpc(self, text: str) -> None:
        self.sendNextPrevS(text, 3)

    def sendNextPrevS(self, text: str) -> None:
        self.sendNextPrevS(text, 3)

    def sendNextPrevS_text_type(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimpleS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "01 01", type))
        self.lastMsg = 0

    def sendOk(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "00 00", 0))
        self.lastMsg = 0

    def sendOkS(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimpleS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 0, text, "00 00", type))
        self.lastMsg = 0

    def sendYesNo(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 1, text, "", 0))
        self.lastMsg = 1

    def sendYesNoS(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimpleS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 1, text, "", type))
        self.lastMsg = 1

    def sendAcceptDecline(self, text: str) -> None:
        self.askAcceptDecline(text)

    def sendAcceptDeclineNoESC(self, text: str) -> None:
        self.askAcceptDeclineNoESC(text)

    def askAcceptDecline(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 11, text, "", 0))
        self.lastMsg = 11

    def askAcceptDeclineNoESC(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 12, text, "", 0))
        self.lastMsg = 12

    def askAvatar(self, text: str, card: int, args: int) -> None:
        if self.lastMsg > -1:
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalkStyle(self.npc, text, card, args))
        self.lastMsg = 7

    def sendSimple(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if not ("#L" in text):
            self.sendNext(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 4, text, "", 0))
        self.lastMsg = 4

    def sendSimple_text_speaker(self, text: str, speaker: int) -> None:
        if self.lastMsg > -1:
            return
        if not ("#L" in text):
            self.sendNext(text)
            return
        self.getClient().getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 4, text, "", speaker))
        self.lastMsg = 4

    def sendSimpleS(self, text: str, type: int) -> None:
        if self.lastMsg > -1:
            return
        if not ("#L" in text):
            self.sendNextS(text, type)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalk(self.npc, 4, text, "", type))
        self.lastMsg = 4

    def sendStyle(self, text: str, styles: list) -> None:
        if self.lastMsg > -1:
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalkStyle(self.npc, text, 0, styles))
        self.lastMsg = 9

    def sendStyle_text_caid_styles(self, text: str, caid: int, styles: list) -> None:
        if self.lastMsg > -1:
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalkStyle(self.npc, text, caid, styles))
        self.lastMsg = 7

    def sendGetNumber(self, text: str, def: int, min: int, max: int) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalkNum(self.npc, text, def, min, max))
        self.lastMsg = 3

    def sendGetText(self, text: str) -> None:
        if self.lastMsg > -1:
            return
        if ("#L" in text):
            self.sendSimple(text)
            return
        self.c.getSession().write(MaplePacketCreator.getNPCTalkText(self.npc, text))
        self.lastMsg = 2

    def setGetText(self, text: str) -> None:
        self.getText = text

    def getText(self) -> str:
        return self.getText

    def setHair(self, hair: int) -> None:
        self.getPlayer().setHair(hair)
        self.getPlayer().updateSingleStat(MapleStat.HAIR, hair)
        self.getPlayer().equipChanged()

    def setFace(self, face: int) -> None:
        self.getPlayer().setFace(face)
        self.getPlayer().updateSingleStat(MapleStat.FACE, face)
        self.getPlayer().equipChanged()

    def setSkin(self, color: int) -> None:
        self.getPlayer().setSkinColor(color)
        self.getPlayer().updateSingleStat(MapleStat.SKIN, color)
        self.getPlayer().equipChanged()

    def setRandomAvatar(self, ticket: int, args_all: list) -> int:
        if not self.haveItem(ticket):
            return -1
        self.gainItem(ticket, (short)(-1))
        args = args_all[Randomizer.nextInt(len(args_all))]
        if args < 100:
            self.c.getPlayer().setSkinColor(args)
            self.c.getPlayer().updateSingleStat(MapleStat.SKIN, args)
        elif args < 30000:
            self.c.getPlayer().setFace(args)
            self.c.getPlayer().updateSingleStat(MapleStat.FACE, args)
        else:
            self.c.getPlayer().setHair(args)
            self.c.getPlayer().updateSingleStat(MapleStat.HAIR, args)
        self.c.getPlayer().equipChanged()
        return 1

    def setAvatar(self, ticket: int, args: int) -> int:
        if not self.haveItem(ticket):
            return -1
        self.gainItem(ticket, (short)(-1))
        if args < 100:
            self.c.getPlayer().setSkinColor(args)
            self.c.getPlayer().updateSingleStat(MapleStat.SKIN, args)
        elif args < 30000:
            self.c.getPlayer().setFace(args)
            self.c.getPlayer().updateSingleStat(MapleStat.FACE, args)
        else:
            self.c.getPlayer().setHair(args)
            self.c.getPlayer().updateSingleStat(MapleStat.HAIR, args)
        self.c.getPlayer().equipChanged()
        return 1

    def sendStorage(self) -> None:
        self.c.getPlayer().setConversation(4)
        self.c.getPlayer().getStorage().sendStorage(self.c, self.npc)

    def openShop(self, id: int) -> None:
        MapleShopFactory.getInstance().getShop(id).sendShop(self.c)

    def gainGachaponItem(self, id: int, quantity: int) -> int:
        return self.gainGachaponItem(id, quantity, self.c.getPlayer().getMap().getStreetName() + " - " + self.c.getPlayer().getMap().getMapName())

    def gainGachaponItem_id_quantity_msg(self, id: int, quantity: int, msg: str) -> int:
        try:
            if not MapleItemInformationProvider.getInstance().itemExists(id):
                return -1
            item = MapleInventoryManipulator.addbyId_Gachapon(self.c, id, quantity)
            if item is None:
                return -1
            rareness = GameConstants.gachaponRareItem(item.getItemId())
            if rareness > 0:
                World.Broadcast.broadcastMessage(MaplePacketCreator.getGachaponMega("[" + msg + "] " + self.c.getPlayer().getName(), " : 恭喜获得道具!", item, rareness, self.getPlayer().getClient().getChannel()).encode("utf-8"))
            return item.getItemId()
        except Exception as e:
            e.printStackTrace()
            return -1

    def gainGachaponItem_id_quantity_msg_概率(self, id: int, quantity: int, msg: str, 概率: int) -> int:
        try:
            if not MapleItemInformationProvider.getInstance().itemExists(id):
                return -1
            item = MapleInventoryManipulator.addbyId_Gachapon(self.c, id, quantity)
            if item is None:
                return -1
            if 概率 > 0:
                World.Broadcast.broadcastMessage(MaplePacketCreator.getGachaponMega("[" + msg + "] " + self.c.getPlayer().getName(), " : 从抽奖中获得!大家恭喜他（她）吧！！！", item, 0, self.getPlayer().getClient().getChannel()).encode("utf-8"))
            return item.getItemId()
        except Exception as e:
            e.printStackTrace()
            return -1

    def changeJob(self, job: int) -> None:
        self.c.getPlayer().changeJob(job)

    def startQuest(self, id: int) -> None:
        MapleQuest.getInstance(id).start(self.getPlayer(), self.npc)

    def completeQuest(self, id: int) -> None:
        MapleQuest.getInstance(id).complete(self.getPlayer(), self.npc)

    def forfeitQuest(self, id: int) -> None:
        MapleQuest.getInstance(id).forfeit(self.getPlayer())

    def forceStartQuest(self) -> None:
        MapleQuest.getInstance(self.questid).forceStart(self.getPlayer(), self.getNpc(), None)

    def forceStartQuest_id(self, id: int) -> None:
        MapleQuest.getInstance(id).forceStart(self.getPlayer(), self.getNpc(), None)

    def forceStartQuest_customData(self, customData: str) -> None:
        MapleQuest.getInstance(self.questid).forceStart(self.getPlayer(), self.getNpc(), customData)

    def forceCompleteQuest(self) -> None:
        MapleQuest.getInstance(self.questid).forceComplete(self.getPlayer(), self.getNpc())

    def forceCompleteQuest_id(self, id: int) -> None:
        MapleQuest.getInstance(id).forceComplete(self.getPlayer(), self.getNpc())

    def getQuestCustomData(self) -> str:
        return self.c.getPlayer().getQuestNAdd(MapleQuest.getInstance(self.questid)).getCustomData()

    def setQuestCustomData(self, customData: str) -> None:
        self.getPlayer().getQuestNAdd(MapleQuest.getInstance(self.questid)).setCustomData(customData)

    def getLevel(self) -> int:
        return self.getPlayer().getLevel()

    def getJobId(self) -> int:
        return self.getPlayer().getJob()

    def changeJobById(self, job: int) -> None:
        self.c.getPlayer().changeJob(job)

    def getMeso(self) -> int:
        return self.getPlayer().getMeso()

    def gainAp(self, amount: int) -> None:
        self.c.getPlayer().gainAp(amount)

    def expandInventory(self, type: int, amt: int) -> None:
        self.c.getPlayer().expandInventory(type, amt)

    def unequipEverything(self) -> None:
        equipped = self.getPlayer().getInventory(MapleInventoryType.EQUIPPED)
        equip = self.getPlayer().getInventory(MapleInventoryType.EQUIP)
        ids = []
        for item in equipped.list():
            ids.add(item.getPosition())
        for id in ids:
            MapleInventoryManipulator.unequip(self.getC(), id, equip.getNextFreeSlot())

    def clearSkills(self) -> None:
        skills = self.getPlayer().getSkills()
        for (final Map.Entry<ISkill, SkillEntry> skill : skills.items())
            self.getPlayer().changeSkillLevel(skill.getKey(), 0, 0)

    def hasSkill(self, skillid: int) -> bool:
        theSkill = SkillFactory.getSkill(skillid)
        return theSkill is not None and self.c.getPlayer().getSkillLevel(theSkill) > 0

    def showEffect(self, broadcast: bool, effect: str) -> None:
        if broadcast:
            self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.showEffect(effect))
        else:
            self.c.getSession().write(MaplePacketCreator.showEffect(effect))

    def playSound(self, broadcast: bool, sound: str) -> None:
        if broadcast:
            self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.playSound(sound))
        else:
            self.c.getSession().write(MaplePacketCreator.playSound(sound))

    def environmentChange(self, broadcast: bool, env: str) -> None:
        if broadcast:
            self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.environmentChange(env, 2))
        else:
            self.c.getSession().write(MaplePacketCreator.environmentChange(env, 2))

    def updateBuddyCapacity(self, capacity: int) -> None:
        self.c.getPlayer().setBuddyCapacity(capacity)

    def getBuddyCapacity(self) -> int:
        return self.c.getPlayer().getBuddyCapacity()

    def partyMembersInMap(self) -> int:
        inMap = 0
        for char2 in self.getPlayer().getMap().getCharactersThreadsafe():
            if char2.getParty() == self.getPlayer().getParty():
                inMap += 1
        return inMap

    def getPartyMembers(self) -> list:
        if self.getPlayer().getParty() is None:
            return None
        chars = []
        for chr in self.getPlayer().getParty().getMembers():
            for channel in ChannelServer.getAllInstances():
                ch = channel.getPlayerStorage().getCharacterById(chr.getId())
                if ch is not None:
                    chars.add(ch)
        return chars

    def warpPartyWithExp(self, mapId: int, exp: int) -> None:
        target = self.getMap(mapId)
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.c.getChannelServer().getPlayerStorage().getCharacterByName(chr.getName())
            if (curChar.getEventInstance() is None and self.getPlayer().getEventInstance() is None) or curChar.getEventInstance() == self.getPlayer().getEventInstance():
                curChar.changeMap(target, target.getPortal(0))
                curChar.gainExp(exp, True, False, True)

    def warpPartyWithExpMeso(self, mapId: int, exp: int, meso: int) -> None:
        target = self.getMap(mapId)
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.c.getChannelServer().getPlayerStorage().getCharacterByName(chr.getName())
            if (curChar.getEventInstance() is None and self.getPlayer().getEventInstance() is None) or curChar.getEventInstance() == self.getPlayer().getEventInstance():
                curChar.changeMap(target, target.getPortal(0))
                curChar.gainExp(exp, True, False, True)
                curChar.gainMeso(meso, True)

    def getSquad(self, type: str) -> Any:
        return self.c.getChannelServer().getMapleSquad(type)

    def getSquadAvailability(self, type: str) -> int:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is None:
            return -1
        return squad.getStatus()

    def registerSquad(self, type: str, minutes: int, startText: str) -> bool:
        if self.c.getChannelServer().getMapleSquad(type) is None:
            squad = MapleSquad(self.c.getChannel(), type, self.c.getPlayer(), minutes * 60 * 1000, startText)
            ret = self.c.getChannelServer().addMapleSquad(squad, type)
            if ret:
                map = self.c.getPlayer().getMap()
                map.broadcastMessage(MaplePacketCreator.getClock(minutes * 60))
                map.broadcastMessage(MaplePacketCreator.serverNotice(6, self.c.getPlayer().getName() + startText))
            else:
                squad.clear()
            return ret
        return False

    def getSquadList(self, type: str, type_: int) -> bool:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is None:
            return False
        # switch (type_):
            # case 0:
            # case 3:
                self.sendNext(squad.getSquadMemberString(type_))
                break
            # case 1:
                self.sendSimple(squad.getSquadMemberString(type_))
                break
            # case 2:
                if squad.getBannedMemberSize() > 0:
                    self.sendSimple(squad.getSquadMemberString(type_))
                    break
                self.sendNext(squad.getSquadMemberString(type_))
                break
        return True

    def isSquadLeader(self, type: str) -> int:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is None:
            return -1
        if squad.getLeader() is not None and squad.getLeader().getId() == self.c.getPlayer().getId():
            return 1
        return 0

    def reAdd(self, eim: str, squad: str) -> bool:
        eimz = self.getDisconnected(eim)
        squadz = self.getSquad(squad)
        if eimz is not None and squadz is not None:
            squadz.reAddMember(self.getPlayer())
            eimz.registerPlayer(self.getPlayer())
            return True
        return False

    def banMember(self, type: str, pos: int) -> None:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is not None:
            squad.banMember(pos)

    def acceptMember(self, type: str, pos: int) -> None:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is not None:
            squad.acceptMember(pos)

    def getReadableMillis(self, startMillis: int, endMillis: int) -> str:
        return StringUtil.getReadableMillis(startMillis, endMillis)

    def addMember(self, type: str, join: bool) -> int:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is not None:
            return squad.addMember(self.c.getPlayer(), join)
        return -1

    def isSquadMember(self, type: str) -> int:
        squad = self.c.getChannelServer().getMapleSquad(type)
        if squad is None:
            return -1
        if squad.getMembers().__contains__(self.c.getPlayer()):
            return 1
        if squad.isBanned(self.c.getPlayer()):
            return 2
        return 0

    def resetReactors(self) -> None:
        self.getPlayer().getMap().resetReactors()

    def genericGuildMessage(self, code: int) -> None:
        self.c.getSession().write(MaplePacketCreator.genericGuildMessage(code))

    def disbandGuild(self) -> None:
        gid = self.c.getPlayer().getGuildId()
        if gid <= 0 or self.c.getPlayer().getGuildRank() != 1:
            return
        World.Guild.disbandGuild(gid)

    def increaseGuildCapacity(self) -> None:
        if self.c.getPlayer().getMeso() < 2500000:
            self.c.getSession().write(MaplePacketCreator.serverNotice(1, "你没有足够的金币."))
            return
        gid = self.c.getPlayer().getGuildId()
        if gid <= 0:
            return
        World.Guild.increaseGuildCapacity(gid)
        self.c.getPlayer().gainMeso(-2500000, True, False, True)

    def increaseCharacterSlots(self, price: int) -> None:
        useNX = 1
        slots = self.c.getCharacterSlots()
        if slots >= LoginServer.getMaxCharacters():
            self.c.getPlayer().dropMessage(1, "角色列表已满无法增加！")
            return
        if self.c.getPlayer().getCSPoints(useNX) < price:
            return
        self.c.getPlayer().modifyCSPoints(useNX, -price, False)
        if self.c.gainCharacterSlot():
            self.c.getPlayer().dropMessage(1, "角色列表已增加到：" + self.c.getCharacterSlots() + "个")

    def displayGuildRanks(self) -> None:
        self.c.getSession().write(MaplePacketCreator.showGuildRanks(self.npc, MapleGuildRanking.getInstance().getGuildRank()))

    def removePlayerFromInstance(self) -> bool:
        if self.c.getPlayer().getEventInstance() is not None:
            self.c.getPlayer().getEventInstance().removePlayer(self.c.getPlayer())
            return True
        return False

    def isPlayerInstance(self) -> bool:
        return self.c.getPlayer().getEventInstance() is not None

    def changeStat(self, slot: int, type: int, amount: int) -> None:
        sel = self.c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).getItem(slot)
        # switch (type):
            # case 0:
                sel.setStr(amount)
                break
            # case 1:
                sel.setDex(amount)
                break
            # case 2:
                sel.setInt(amount)
                break
            # case 3:
                sel.setLuk(amount)
                break
            # case 4:
                sel.setHp(amount)
                break
            # case 5:
                sel.setMp(amount)
                break
            # case 6:
                sel.setWatk(amount)
                break
            # case 7:
                sel.setMatk(amount)
                break
            # case 8:
                sel.setWdef(amount)
                break
            # case 9:
                sel.setMdef(amount)
                break
            # case 10:
                sel.setAcc(amount)
                break
            # case 11:
                sel.setAvoid(amount)
                break
            # case 12:
                sel.setHands(amount)
                break
            # case 13:
                sel.setSpeed(amount)
                break
            # case 14:
                sel.setJump(amount)
                break
            # case 15:
                sel.setUpgradeSlots(amount)
                break
            # case 16:
                sel.setViciousHammer(amount)
                break
            # case 17:
                sel.setLevel(amount)
                break
            # case 18:
                sel.setEnhance(amount)
                break
            # case 19:
                sel.setPotential1(amount)
                break
            # case 20:
                sel.setPotential2(amount)
                break
            # case 21:
                sel.setPotential3(amount)
                break
            # case 22:
                sel.setOwner(self.getText())
                break
        self.c.getPlayer().equipChanged()

    def killAllMonsters(self) -> None:
        map = self.c.getPlayer().getMap()
        range = Double.POSITIVE_INFINITY
        for monstermo in map.getMapObjectsInRange(self.c.getPlayer().getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER)):
            mob = monstermo
            if mob.getStats().isBoss():
                map.killMonster(mob, self.c.getPlayer(), False, False, 1)

    def giveMerchantMesos(self) -> None:
        mesos = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM hiredmerchants WHERE merchantid = ?")
            ps.setInt(1, self.getPlayer().getId())
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
            else:
                mesos = rs.getLong("mesos")
            rs.close()
            ps.close()
            ps = con.prepareStatement("UPDATE hiredmerchants SET mesos = 0 WHERE merchantid = ?")
            ps.setInt(1, self.getPlayer().getId())
            ps.executeUpdate()
            ps.close()
        except Exception as ex:
            print("Error gaining mesos in hired merchant" + ex)
        self.c.getPlayer().gainMeso(mesos, True)

    def dc(self) -> None:
        victim = self.c.getChannelServer().getPlayerStorage().getCharacterByName(self.c.getPlayer().getName())
        victim.getClient().getSession().close(True)
        victim.getClient().disconnect(True, False)

    def getMerchantMesos(self) -> int:
        mesos = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM hiredmerchants WHERE merchantid = ?")
            ps.setInt(1, self.getPlayer().getId())
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
            else:
                mesos = rs.getLong("mesos")
            rs.close()
            ps.close()
        except Exception as ex:
            print("Error gaining mesos in hired merchant" + ex)
        return mesos

    def openDuey(self) -> None:
        self.c.getPlayer().setConversation(2)
        self.c.getSession().write(MaplePacketCreator.sendDuey(9, None))

    def openMerchantItemStore(self) -> None:
        self.c.getPlayer().setConversation(3)
        self.c.getSession().write(PlayerShopPacket.merchItemStore(34))

    def openMerchantItemStore1(self) -> None:
        pack = loadItemFrom_Database(self.c.getPlayer().getId(), self.c.getPlayer().getAccountID())
        self.c.getSession().write(PlayerShopPacket.merchItemStore_ItemData(pack))

    def getDojoPoints(self) -> int:
        return self.c.getPlayer().getDojo()

    def getDojoRecord(self) -> int:
        return self.c.getPlayer().getDojoRecord()

    def setDojoRecord(self, reset: bool) -> None:
        self.c.getPlayer().setDojoRecord(reset)

    def start_DojoAgent(self, dojo: bool, party: bool) -> bool:
        if dojo:
            return Event_DojoAgent.warpStartDojo(self.c.getPlayer(), party)
        return Event_DojoAgent.warpStartAgent(self.c.getPlayer(), party)

    def start_PyramidSubway(self, pyramid: int) -> bool:
        if pyramid >= 0:
            return Event_PyramidSubway.warpStartPyramid(self.c.getPlayer(), pyramid)
        return Event_PyramidSubway.warpStartSubway(self.c.getPlayer())

    def bonus_PyramidSubway(self, pyramid: int) -> bool:
        if pyramid >= 0:
            return Event_PyramidSubway.warpBonusPyramid(self.c.getPlayer(), pyramid)
        return Event_PyramidSubway.warpBonusSubway(self.c.getPlayer())

    def getKegs(self) -> int:
        return AramiaFireWorks.getInstance().getKegsPercentage()

    def giveKegs(self, kegs: int) -> None:
        AramiaFireWorks.getInstance().giveKegs(self.c.getPlayer(), kegs)

    def getSunshines(self) -> int:
        return AramiaFireWorks.getInstance().getSunsPercentage()

    def addSunshines(self, kegs: int) -> None:
        AramiaFireWorks.getInstance().giveSuns(self.c.getPlayer(), kegs)

    def getDecorations(self) -> int:
        return AramiaFireWorks.getInstance().getDecsPercentage()

    def addDecorations(self, kegs: int) -> None:
        try:
            AramiaFireWorks.getInstance().giveDecs(self.c.getPlayer(), kegs)
        except Exception as e:
            e.printStackTrace()

    def getInventory(self, type: int) -> Any:
        return self.c.getPlayer().getInventory(MapleInventoryType.getByType(type))

    def getCarnivalParty(self) -> Any:
        return self.c.getPlayer().getCarnivalParty()

    def getNextCarnivalRequest(self) -> Any:
        return self.c.getPlayer().getNextCarnivalRequest()

    def getCarnivalChallenge(self, chr: Any) -> Any:
        return MapleCarnivalChallenge(chr)

    def setHP(self, hp: int) -> None:
        self.c.getPlayer().getStat().setHp(hp)

    def maxStats(self) -> None:
        statup = new ArrayList<Pair<MapleStat, Integer>>(2)
        self.c.getPlayer().getStat().setStr(32767)
        self.c.getPlayer().getStat().setDex(32767)
        self.c.getPlayer().getStat().setInt(32767)
        self.c.getPlayer().getStat().setLuk(32767)
        self.c.getPlayer().getStat().setMaxHp(30000)
        self.c.getPlayer().getStat().setMaxMp(30000)
        self.c.getPlayer().getStat().setHp(30000)
        self.c.getPlayer().getStat().setMp(30000)
        statup.add(new Pair<MapleStat, Integer>(MapleStat.STR, 32767))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.DEX, 32767))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.LUK, 32767))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.INT, 32767))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.HP, 30000))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXHP, 30000))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MP, 30000))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXMP, 30000))
        self.c.getSession().write(MaplePacketCreator.updatePlayerStats(statup, self.c.getPlayer().getJob()))

    def getSpeedRun(self, typ: str) -> Any:
        type = SpeedRunType.valueOf(typ)
        if SpeedRunner.getInstance().getSpeedRunData(type) is not None:
            return SpeedRunner.getInstance().getSpeedRunData(type)
        return new Pair<String, Map<Integer, String>>("", {})

    def getSR(self, ma: Any, sel: int) -> bool:
        if ma.getRight().get(sel) is None or ma.getRight().get(sel) <= 0:
            self.dispose()
            return False
        self.sendOk(ma.getRight().get(sel))
        return True

    def getEquip(self, itemid: int) -> Any:
        return MapleItemInformationProvider.getInstance().getEquipById(itemid)

    def setExpiration(self, statsSel: Any, expire: int) -> None:
        if isinstance(statsSel, Equip):
            (statsSel).setExpiration(int(time.time() * 1000) + expire * 24 * 60 * 60 * 1000)

    def setLock(self, statsSel: Any) -> None:
        if isinstance(statsSel, Equip):
            eq = statsSel
            if eq.getExpiration() == -1:
                eq.setFlag((byte)(eq.getFlag() | ItemFlag.LOCK.getValue()))
            else:
                eq.setFlag((byte)(eq.getFlag() | ItemFlag.UNTRADEABLE.getValue()))

    def addFromDrop(self, statsSel: Any) -> bool:
        if isinstance(statsSel, IItem):
            it = statsSel
            return MapleInventoryManipulator.checkSpace(self.getClient(), it.getItemId(), it.getQuantity(), it.getOwner()) and MapleInventoryManipulator.addFromDrop(self.getClient(), it, False)
        return False

    def replaceItem(self, slot: int, invType: int, statsSel: Any, offset: int, type: str) -> bool:
        return self.replaceItem(slot, invType, statsSel, offset, type, False)

    def replaceItem_slot_invType_statsSel_offset_type_takeSlot(self, slot: int, invType: int, statsSel: Any, offset: int, type: str, takeSlot: bool) -> bool:
        inv = MapleInventoryType.getByType(invType)
        if inv is None:
            return False
        item = self.getPlayer().getInventory(inv).getItem(slot)
        if item is None or isinstance(statsSel, IItem):
            item = statsSel
        if offset > 0:
            if inv != MapleInventoryType.EQUIP:
                return False
            eq = item
            if takeSlot:
                if eq.getUpgradeSlots() < 1:
                    return False
                eq.setUpgradeSlots((byte)(eq.getUpgradeSlots() - 1))
            if type.lower() == "Slots".lower():
                eq.setUpgradeSlots((byte)(eq.getUpgradeSlots() + offset))
            elif type.lower() == "Level".lower():
                eq.setLevel((byte)(eq.getLevel() + offset))
            elif type.lower() == "Hammer".lower():
                eq.setViciousHammer((byte)(eq.getViciousHammer() + offset))
            elif type.lower() == "STR".lower():
                eq.setStr((short)(eq.getStr() + offset))
            elif type.lower() == "DEX".lower():
                eq.setDex((short)(eq.getDex() + offset))
            elif type.lower() == "INT".lower():
                eq.setInt((short)(eq.getInt() + offset))
            elif type.lower() == "LUK".lower():
                eq.setLuk((short)(eq.getLuk() + offset))
            elif type.lower() == "HP".lower():
                eq.setHp((short)(eq.getHp() + offset))
            elif type.lower() == "MP".lower():
                eq.setMp((short)(eq.getMp() + offset))
            elif type.lower() == "WATK".lower():
                eq.setWatk((short)(eq.getWatk() + offset))
            elif type.lower() == "MATK".lower():
                eq.setMatk((short)(eq.getMatk() + offset))
            elif type.lower() == "WDEF".lower():
                eq.setWdef((short)(eq.getWdef() + offset))
            elif type.lower() == "MDEF".lower():
                eq.setMdef((short)(eq.getMdef() + offset))
            elif type.lower() == "ACC".lower():
                eq.setAcc((short)(eq.getAcc() + offset))
            elif type.lower() == "Avoid".lower():
                eq.setAvoid((short)(eq.getAvoid() + offset))
            elif type.lower() == "Hands".lower():
                eq.setHands((short)(eq.getHands() + offset))
            elif type.lower() == "Speed".lower():
                eq.setSpeed((short)(eq.getSpeed() + offset))
            elif type.lower() == "Jump".lower():
                eq.setJump((short)(eq.getJump() + offset))
            elif type.lower() == "ItemEXP".lower():
                eq.setItemEXP(eq.getItemEXP() + offset)
            elif type.lower() == "Expiration".lower():
                eq.setExpiration(eq.getExpiration() + offset)
            elif type.lower() == "Flag".lower():
                eq.setFlag((byte)(eq.getFlag() + offset))
            if eq.getExpiration() == -1:
                eq.setFlag((byte)(eq.getFlag() | ItemFlag.LOCK.getValue()))
            else:
                eq.setFlag((byte)(eq.getFlag() | ItemFlag.UNTRADEABLE.getValue()))
            item = eq.copy()
        MapleInventoryManipulator.removeFromSlot(self.getClient(), inv, slot, item.getQuantity(), False)
        return MapleInventoryManipulator.addFromDrop(self.getClient(), item, False)

    def replaceItem_slot_invType_statsSel_upgradeSlots(self, slot: int, invType: int, statsSel: Any, upgradeSlots: int) -> bool:
        return self.replaceItem(slot, invType, statsSel, upgradeSlots, "Slots")

    def isCash(self, itemId: int) -> bool:
        return MapleItemInformationProvider.getInstance().isCash(itemId)

    def buffGuild(self, buff: int, duration: int, msg: str) -> None:
        ii = MapleItemInformationProvider.getInstance()
        if ii.getItemEffect(buff) is not None and self.getPlayer().getGuildId() > 0:
            mse = ii.getItemEffect(buff)
            for cserv in ChannelServer.getAllInstances():
                for chr in cserv.getPlayerStorage().getAllCharacters():
                    if chr.getGuildId() == self.getPlayer().getGuildId():
                        mse.applyTo(chr, chr, True, None, duration)
                        chr.dropMessage(5, "Your guild has gotten a " + msg + " buff.")

    def createAlliance(self, alliancename: str) -> bool:
        pt = self.c.getPlayer().getParty()
        otherChar = self.c.getChannelServer().getPlayerStorage().getCharacterById(pt.getMemberByIndex(1).getId())
        if otherChar is None or otherChar.getId() == self.c.getPlayer().getId():
            return False
        try:
            return World.Alliance.createAlliance(alliancename, self.c.getPlayer().getId(), otherChar.getId(), self.c.getPlayer().getGuildId(), otherChar.getGuildId())
        except Exception as re:
            re.printStackTrace()
            return False

    def addCapacityToAlliance(self) -> bool:
        try:
            gs = World.Guild.getGuild(self.c.getPlayer().getGuildId())
            if gs is not None and self.c.getPlayer().getGuildRank() == 1 and self.c.getPlayer().getAllianceRank() == 1 and World.Alliance.getAllianceLeader(gs.getAllianceId()) == self.c.getPlayer().getId() and World.Alliance.changeAllianceCapacity(gs.getAllianceId()):
                self.gainMeso(-MapleGuildAlliance.CHANGE_CAPACITY_COST)
                return True
        except Exception as re:
            re.printStackTrace()
        return False

    def disbandAlliance(self) -> bool:
        try:
            gs = World.Guild.getGuild(self.c.getPlayer().getGuildId())
            if gs is not None and self.c.getPlayer().getGuildRank() == 1 and self.c.getPlayer().getAllianceRank() == 1 and World.Alliance.getAllianceLeader(gs.getAllianceId()) == self.c.getPlayer().getId() and World.Alliance.disbandAlliance(gs.getAllianceId()):
                return True
        except Exception as re:
            re.printStackTrace()
        return False

    def getLastMsg(self) -> int:
        return self.lastMsg

    def setLastMsg(self, last: int) -> None:
        self.lastMsg = last

    def maxAllSkills(self) -> None:
        for skil in SkillFactory.getAllSkills():
            if GameConstants.isApplicableSkill(skil.getId()):
                self.teachSkill(skil.getId(), skil.getMaxLevel(), skil.getMaxLevel())

    def resetStats(self, str: int, dex: int, z: int, luk: int) -> None:
        self.c.getPlayer().resetStats(str, dex, z, luk)

    def dropItem(self, slot: int, invType: int, quantity: int) -> bool:
        inv = MapleInventoryType.getByType(invType)
        return inv is not None and MapleInventoryManipulator.drop(self.c, inv, slot, quantity, True)

    def getAllPotentialInfo(self) -> list:
        return [].getAllPotentialInfo().keys())

    def getPotentialInfo(self, id: int) -> str:
        potInfo = MapleItemInformationProvider.getInstance().getPotentialInfo(id)
        builder = ""
        builder.append(id)
        builder.append("#n#k\r\n\r\n")
        minLevel = 1
        maxLevel = 10
        for item in potInfo:
            builder.append("#eLevels ")
            builder.append(minLevel)
            builder.append("~")
            builder.append(maxLevel)
            builder.append(": #n")
            builder.append(item)
            minLevel += 10
            maxLevel += 10
            builder.append("\r\n")
        return builder

    def sendRPS(self) -> None:
        self.c.getSession().write(MaplePacketCreator.getRPSMode(8, -1, -1, -1))

    def setQuestRecord(self, ch: Any, questid: int, data: str) -> None:
        (ch).getQuestNAdd(MapleQuest.getInstance(questid)).setCustomData(data)

    def doWeddingEffect2(self, ch: Any) -> None:
        def _task_1():
            if chr is None or NPCConversationManager.self.getPlayer() is None:
                NPCConversationManager.self.warpMap(680000500, 0)
            else:
                NPCConversationManager.self.getMap().broadcastMessage(MaplePacketCreator.yellowChat(chr.getName() + ", 你愿意嫁给 " + NPCConversationManager.self.getPlayer().getName() + " 吗？无论他将来是富有还是贫穷、或无论他将来身体健康或不适，你都愿意和他永远在一起吗?"))

        def _task_2():
            if chr is None or NPCConversationManager.self.getPlayer() is None:
                if NPCConversationManager.self.getPlayer() is not None:
                    NPCConversationManager.self.setQuestRecord(NPCConversationManager.self.getPlayer(), 160001, "3")
                    NPCConversationManager.self.setQuestRecord(NPCConversationManager.self.getPlayer(), 160002, "0")
                elif chr is not None:
                    NPCConversationManager.self.setQuestRecord(chr, 160001, "3")
                    NPCConversationManager.self.setQuestRecord(chr, 160002, "0")
                NPCConversationManager.self.warpMap(680000500, 0)
            else:
                NPCConversationManager.self.setQuestRecord(NPCConversationManager.self.getPlayer(), 160001, "2")
                NPCConversationManager.self.setQuestRecord(chr, 160001, "2")
                NPCConversationManager.self.sendNPCText("好，我以圣灵、圣父、圣子的名义宣布：" + NPCConversationManager.self.getPlayer().getName() + " 和 " + chr.getName() + ", 结为夫妻。 希望你们在!" + chr.getClient().getChannelServer().getServerName() + " 游戏中玩的愉快!", 9201002)
                NPCConversationManager.self.getMap().startExtendedMapEffect("You may now kiss the bride, " + NPCConversationManager.self.getPlayer().getName() + "not ", 5120006)
                if chr.getGuildId() > 0:
                    World.Guild.guildPacket(chr.getGuildId(), MaplePacketCreator.sendMarriage(False, chr.getName()))
                if chr.getFamilyId() > 0:
                    World.Family.familyPacket(chr.getFamilyId(), MaplePacketCreator.sendMarriage(True, chr.getName()), chr.getId())
                if NPCConversationManager.self.getPlayer().getGuildId() > 0:
                    World.Guild.guildPacket(NPCConversationManager.self.getPlayer().getGuildId(), MaplePacketCreator.sendMarriage(False, NPCConversationManager.self.getPlayer().getName()))
                if NPCConversationManager.self.getPlayer().getFamilyId() > 0:
                    World.Family.familyPacket(NPCConversationManager.self.getPlayer().getFamilyId(), MaplePacketCreator.sendMarriage(True, chr.getName()), NPCConversationManager.self.getPlayer().getId())

        chr = ch
        self.getMap().broadcastMessage(MaplePacketCreator.yellowChat(self.getPlayer().getName() + ", 你愿意娶 " + chr.getName() + " 为妻吗？无论她将来是富有还是贫穷、或无论她将来身体健康或不适，你都愿意和她永远在一起吗？"))
        Timer.CloneTimer.getInstance().schedule(_task_1, 10000)
        Timer.CloneTimer.getInstance().schedule(_task_2, 20000)

    def run(self) -> None:
        if chr is None or NPCConversationManager.self.getPlayer() is None:
            NPCConversationManager.self.warpMap(680000500, 0)
        else:
            NPCConversationManager.self.getMap().broadcastMessage(MaplePacketCreator.yellowChat(chr.getName() + ", 你愿意嫁给 " + NPCConversationManager.self.getPlayer().getName() + " 吗？无论他将来是富有还是贫穷、或无论他将来身体健康或不适，你都愿意和他永远在一起吗?"))

    def openDD(self, type: int) -> None:
        self.c.getSession().write(MaplePacketCreator.openBeans(self.getPlayer().getBeans(), type))

    def worldMessage(self, text: str) -> None:
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, text).encode("utf-8"))

    def getBeans(self) -> int:
        return self.getClient().getPlayer().getBeans()

    def gainBeans(self, s: int) -> None:
        self.getPlayer().gainBeans(s)
        self.c.getSession().write(MaplePacketCreator.updateBeans(self.c.getPlayer().getId(), s))

    def getHyPay(self, type: int) -> int:
        return self.getPlayer().getHyPay(type)

    def szhs(self, ss: str) -> None:
        self.c.getSession().write(MaplePacketCreator.游戏屏幕中间黄色字体(ss))

    def szhs_ss_id(self, ss: str, id: int) -> None:
        self.c.getSession().write(MaplePacketCreator.游戏屏幕中间黄色字体(ss, id))

    def gainHyPay(self, hypay: int) -> int:
        return self.getPlayer().gainHyPay(hypay)

    def addHyPay(self, hypay: int) -> int:
        return self.getPlayer().addHyPay(hypay)

    def delPayReward(self, pay: int) -> int:
        return self.getPlayer().delPayReward(pay)

    def getItemLevel(self, id: int) -> int:
        ii = MapleItemInformationProvider.getInstance()
        return ii.getReqLevel(id)

    def alatPQ(self) -> None:
        pass

    def xlkc(self, days: int) -> None:
        marr = self.getPlayer().getQuestNoAdd(MapleQuest.getInstance(122700))
        if marr is not None and marr.getCustomData() is not None and int(marr.getCustomData()) >= int(time.time() * 1000):
            self.getPlayer().dropMessage(1, "项链扩充失败，您已经进行过项链扩充。")
        else:
            customData = str(int(time.time() * 1000) + days * 24 * 60 * 60 * 1000)
            self.getPlayer().getQuestNAdd(MapleQuest.getInstance(122700)).setCustomData(customData)
            self.getPlayer().dropMessage(1, "项链" + days + "扩充扩充成功！")

    def checkDrop(self, mobId: int) -> str:
        rate = self.getClient().getChannelServer().getDropRate()
        mob = MapleLifeFactory.getMonster(mobId)
        if MapleLifeFactory.getMonster(mobId) is not None and mob.getStats().isBoss():
            rate = self.getClient().getChannelServer().getBossDropRate()
        ranks = MapleMonsterInformationProvider.getInstance().retrieveDrop(mobId)
        if ranks is not None and ranks > 0:
            num = 0
            itemId = 0
            ch = 0
            ii = MapleItemInformationProvider.getInstance()
            name = ""
            for i in range(ranks):
                de = ranks.get(i)
                if de.chance > 0 and (de.questid <= 0 or (de.questid > 0 and MapleQuest.getInstance(de.questid).getName() > 0)):
                    itemId = de.itemId
                    if ii.itemExists(itemId):
                        if num == 0:
                            name.append("当前怪物 #o").append(mobId).append("# 的爆率为:\r\n")
                            name.append("--------------------------------------\r\n")
                        namez = "#z" + itemId + "#"
                        if itemId == 0:
                            itemId = 4031041
                            namez = de.Minimum * self.getClient().getChannelServer().getMesoRate() + " - " + de.Maximum * self.getClient().getChannelServer().getMesoRate() + " 的金币"
                        ch = de.chance * rate
                        name.append(num + 1).append(") #v").append(itemId).append("#").append(namez).append(" - ").append(((ch >= 999999) ? 1000000 : ch) / 10000.0).append("%的爆率. ").append((de.questid > 0 and MapleQuest.getInstance(de.questid).getName() > 0) ? ("需要接受任务: " + MapleQuest.getInstance(de.questid).getName()) : "").append("\r\n")
                        num += 1
            if name > 0:
                return name
        return "没有找到这个怪物的爆率数据。"

    def checkDropper(self, itemid: int) -> str:
        con = DatabaseConnection.getConnection()
        ps = None
        rs = None
        ret = []
        try:
            ps = con.prepareStatement("SELECT * FROM drop_data WHERE itemid = ?")
            ps.setInt(1, itemid)
            rs = ps.executeQuery()
            while rs.next():
                dropperid = rs.getInt("dropperid")
                ret.add(dropperid)
            rs.close()
            ps.close()
        except Exception as e:
            print("[database error]" + e)
        ii = MapleItemInformationProvider.getInstance()
        name = ""
        if ret > 0:
            name.append(" 当前物品 #e#b#v").append(itemid).append("##z").append(itemid).append("##k#n 的掉落为：#e\r\n")
            for i in range(ret):
                name.append(" #o").append(ret.get(i)).append("#\r\n")
        if name > 0:
            return name
        return "没有找到这个物品的爆率数据。"

    def checkMapDrop(self) -> str:
        ranks = [].getGlobalDrop())
        mapid = self.c.getPlayer().getMap().getId()
        cashServerRate = getClient().getChannelServer().getCashRate()
        globalServerRate = 1
        if ranks is not None and ranks > 0:
            num = 0
            name = ""
            for i in range(ranks):
                de = ranks.get(i)
                if de.continent < 0 or (de.continent < 10 and mapid / 100000000 == de.continent) or (de.continent < 100 and mapid / 10000000 == de.continent) or (de.continent < 1000 and mapid / 1000000 == de.continent):
                    itemId = de.itemId
                    if num == 0:
                        name.append("当前地图 #r").append(mapid).append("#k - #m").append(mapid).append("# 的全局爆率为:")
                        name.append("\r\n--------------------------------------\r\n")
                    names = "#z" + itemId + "#"
                    if itemId == 0 and cashServerRate != 0:
                        itemId = 4031041
                        names = (de.Minimum * cashServerRate) + " - " + (de.Maximum * cashServerRate) + " 的抵用卷"
                    chance = de.chance * globalServerRate
                    if getPlayer().isAdmin():
                        name.append(num + 1).append(") #v").append(itemId).append("#").append(names).append(" - ").append(Integer.valueOf((chance >= 999999) ? 1000000 : chance) / 10000.0).append("%的爆率. ").append((de.questid > 0 and MapleQuest.getInstance(de.questid).getName() > 0) ? ("需要接受任务: " + MapleQuest.getInstance(de.questid).getName()) : "").append("\r\n")
                    else:
                        name.append(num + 1).append(") #v").append(itemId).append("#").append(names).append((de.questid > 0 and MapleQuest.getInstance(de.questid).getName() > 0) ? ("需要接受任务: " + MapleQuest.getInstance(de.questid).getName()) : "").append("\r\n")
                    num += 1
            if name > 0:
            return name
        return "当前地图没有设置全局爆率。"

    def translated_获取签到奖励领取状态(self) -> int:
        money = 0
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            limitCheck = con.prepareStatement("SELECT * FROM accounts WHERE id=" + cid + "")
            rs = limitCheck.executeQuery()
            if rs.next():
                money = rs.getInt("qiandaolb")
            limitCheck.close()
            rs.close()
        except Exception as ex:
            ex.getStackTrace()
        return money

    def translated_设置签到奖励领取状态(self, slot: int) -> None:
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("UPDATE accounts SET qiandaolb =qiandaolb+ " + slot + " WHERE id = " + cid + "")
            try:
                ps.executeUpdate()
        except Exception as ex:
            ex.getStackTrace()

    def translated_获取礼包领取状态(self) -> int:
        money = 0
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            limitCheck = con.prepareStatement("SELECT * FROM accounts WHERE id=" + cid + "")
            rs = limitCheck.executeQuery()
            if rs.next():
                money = rs.getInt("lb")
            limitCheck.close()
            rs.close()
        except Exception as ex:
            ex.getStackTrace()
        return money

    def translated_设置礼包领取状态(self, slot: int) -> None:
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("UPDATE accounts SET lb =lb+ " + slot + " WHERE id = " + cid + "")
            try:
                ps.executeUpdate()
        except Exception as ex:
            ex.getStackTrace()

    def getzb(self) -> int:
        money = 0
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            limitCheck = con.prepareStatement("SELECT * FROM accounts WHERE id=" + cid + "")
            rs = limitCheck.executeQuery()
            if rs.next():
                money = rs.getInt("money")
            limitCheck.close()
            rs.close()
        except Exception as ex:
            ex.getStackTrace()
        return money

    def setzb(self, slot: int) -> None:
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("UPDATE accounts SET money =money+ " + slot + " WHERE id = " + cid + "")
            try:
                ps.executeUpdate()
        except Exception as ex:
            ex.getStackTrace()

    def getmoneyb(self) -> int:
        moneyb = 0
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            rs = None
            # try-with-resources: final PreparedStatement limitCheck = con.prepareStatement("SELECT * FROM accounts WHERE id=" + cid + "")
            try:
                rs = limitCheck.executeQuery()
                if rs.next():
                    moneyb = rs.getInt("moneyb")
            rs.close()
        except Exception as ex:
            ex.getStackTrace()
        return moneyb

    def setmoneyb(self, slot: int) -> None:
        try:
            cid = self.getPlayer().getAccountID()
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts SET moneyb =moneyb+ " + slot + " WHERE id = " + cid + "")
            ps.executeUpdate()
            ps.close()
        except Exception as ex:
            ex.getStackTrace()

    def getMapFactory(self) -> Any:
        return self.getClient().getChannelServer().getMapFactory()

    def warpBackoff(self) -> None:
        self.c.sendPacket(MaplePacketCreator.stopClock())

    def warpBack(self, mid: int, retmap: int, time: int) -> None:
        def _task_1():
            warpMap = NPCConversationManager.self.c.getChannelServer().getMapFactory().getMap(retmap)
            if NPCConversationManager.self.c.getPlayer() is not None:
                NPCConversationManager.self.c.sendPacket(MaplePacketCreator.stopClock())
                NPCConversationManager.self.c.getPlayer().changeMap(warpMap, warpMap.getPortal(0))
                NPCConversationManager.self.c.getPlayer().dropMessage(6, "到达目的地ヘ!")

        warpMap = self.c.getChannelServer().getMapFactory().getMap(mid)
        self.c.getPlayer().changeMap(warpMap, warpMap.getPortal(0))
        self.c.sendPacket(MaplePacketCreator.getClock(time))
        Timer.EventTimer.getInstance().schedule(_task_1, 1000 * time)

    def warpMapWithClock(self, mid: int, seconds: int) -> None:
        def _task_1():
            if NPCConversationManager.self.c.getPlayer() is not None:
                for chr in NPCConversationManager.self.c.getPlayer().getMap().getCharactersThreadsafe():
                    chr.changeMap(mid)

        self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.getClock(seconds))
        Timer.MapTimer.getInstance().schedule(_task_1, seconds * 1000)

    def showlvl(self) -> None:
        self.c.sendPacket(MaplePacketCreator.showlevelRanks(self.npc, MapleGuildRanking.getInstance().getLevelRank()))

    def showmeso(self) -> None:
        self.c.sendPacket(MaplePacketCreator.showmesoRanks(self.npc, MapleGuildRanking.getInstance().getMesoRank()))

    def ShowMarrageEffect(self) -> None:
        self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.sendMarrageEffect())

    def translated_给全服发点卷(self, 数量: int, 类型: int) -> int:
        count = 0
        try:
            if 数量 <= 0 or 类型 <= 0:
                return 0
            if 类型 == 1 or 类型 == 2:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.modifyCSPoints(类型, 数量)
                        cash = None
                        if 类型 == 1:
                            cash = "点卷"
                        elif 类型 == 2:
                            cash = "抵用卷"
                        count += 1
            elif 类型 == 3:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainMeso(数量, True)
                        count += 1
            elif 类型 == 4:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainExp(数量, True, False, True)
                        count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给全服发点卷出错：" + e.getMessage())
        return count

    def translated_给当前地图发点卷(self, 数量: int, 类型: int) -> int:
        count = 0
        mapId = self.c.getPlayer().getMapId()
        try:
            if 数量 <= 0 or 类型 <= 0:
                return 0
            if 类型 == 1 or 类型 == 2:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        if mch.getMapId() != mapId:
                            continue
                        mch.modifyCSPoints(类型, 数量)
                        cash = None
                        if 类型 == 1:
                            cash = "点卷"
                        elif 类型 == 2:
                            cash = "抵用卷"
                        count += 1
            elif 类型 == 3:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        if mch.getMapId() != mapId:
                            continue
                        mch.gainMeso(数量, True)
                        count += 1
            elif 类型 == 4:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        if mch.getMapId() != mapId:
                            continue
                        mch.gainExp(数量, True, False, True)
                        count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给当前地图发点卷出错：" + e.getMessage())
        return count

    def translated_给当前频道发点卷(self, 数量: int, 类型: int) -> int:
        count = 0
        chlId = self.c.getPlayer().getMap().getChannel()
        try:
            if 数量 <= 0 or 类型 <= 0:
                return 0
            if 类型 == 1 or 类型 == 2:
                for cserv1 in ChannelServer.getAllInstances():
                    if cserv1.getChannel() != chlId:
                        continue
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.modifyCSPoints(类型, 数量)
                        cash = None
                        if 类型 == 1:
                            cash = "点卷"
                        elif 类型 == 2:
                            cash = "抵用卷"
                        count += 1
            elif 类型 == 3:
                for cserv1 in ChannelServer.getAllInstances():
                    if cserv1.getChannel() != chlId:
                        continue
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainMeso(数量, True)
                        count += 1
            elif 类型 == 4:
                for cserv1 in ChannelServer.getAllInstances():
                    if cserv1.getChannel() != chlId:
                        continue
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainExp(数量, True, False, True)
                        count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给当前频道发点卷出错：" + e.getMessage())
        return count

    def translated_给全服发物品(self, 物品ID: int, 数量: int, 力量: int, 敏捷: int, 智力: int, 运气: int, HP: int, MP: int, 可加卷次数: int, 制作人名字: str, 给予时间: int, 是否可以交易: str, 攻击力: int, 魔法力: int, 物理防御: int, 魔法防御: int) -> int:
        count = 0
        try:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(物品ID)
            for cserv1 in ChannelServer.getAllInstances():
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    if 数量 >= 0:
                        if not MapleInventoryManipulator.checkSpace(mch.getClient(), 物品ID, 数量, ""):
                            return 0
                        if (type == (MapleInventoryType.EQUIP) and not GameConstants.isThrowingStar(物品ID) and not GameConstants.isBullet(物品ID)) or (type == (MapleInventoryType.CASH) and 物品ID >= 5000000 and 物品ID <= 5000100):
                            item = ii.getEquipById(物品ID)
                            if ii.isCash(物品ID):
                                item.setUniqueId(1)
                            if 力量 > 0 and 力量 <= 32767:
                                item.setStr(力量)
                            if 敏捷 > 0 and 敏捷 <= 32767:
                                item.setDex(敏捷)
                            if 智力 > 0 and 智力 <= 32767:
                                item.setInt(智力)
                            if 运气 > 0 and 运气 <= 32767:
                                item.setLuk(运气)
                            if 攻击力 > 0 and 攻击力 <= 32767:
                                item.setWatk(攻击力)
                            if 魔法力 > 0 and 魔法力 <= 32767:
                                item.setMatk(魔法力)
                            if 物理防御 > 0 and 物理防御 <= 32767:
                                item.setWdef(物理防御)
                            if 魔法防御 > 0 and 魔法防御 <= 32767:
                                item.setMdef(魔法防御)
                            if HP > 0 and HP <= 30000:
                                item.setHp(HP)
                            if MP > 0 and MP <= 30000:
                                item.setMp(MP)
                            if "可以交易" == (是否可以交易):
                                flag = item.getFlag()
                                if item.getType() == MapleInventoryType.EQUIP.getType():
                                    flag |= ItemFlag.KARMA_EQ.getValue()
                                else:
                                    flag |= ItemFlag.KARMA_USE.getValue()
                                item.setFlag(flag)
                            if 给予时间 > 0:
                                item.setExpiration(int(time.time() * 1000) + 给予时间 * 24 * 60 * 60 * 1000)
                            if 可加卷次数 > 0:
                                item.setUpgradeSlots(可加卷次数)
                            if 制作人名字 is not None:
                                item.setOwner(制作人名字)
                            name = ii.getName(物品ID)
                            if 物品ID / 10000 == 114 and name is not None and name > 0:
                                msg = "你已获得称号 <" + name + ">"
                                mch.getClient().getPlayer().dropMessage(5, msg)
                            MapleInventoryManipulator.addbyItem(mch.getClient(), item.copy())
                        else:
                            MapleInventoryManipulator.addById(mch.getClient(), 物品ID, 数量, "", None, 给予时间, 0)
                    else:
                        MapleInventoryManipulator.removeById(mch.getClient(), GameConstants.getInventoryType(物品ID), 物品ID, -数量, True, False)
                    mch.getClient().getSession().write(MaplePacketCreator.getShowItemGain(物品ID, 数量, True))
                    count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给全服发物品出错：" + e.getMessage())
        return count

    def translated_给当前地图发物品(self, 物品ID: int, 数量: int, 力量: int, 敏捷: int, 智力: int, 运气: int, HP: int, MP: int, 可加卷次数: int, 制作人名字: str, 给予时间: int, 是否可以交易: str, 攻击力: int, 魔法力: int, 物理防御: int, 魔法防御: int) -> int:
        count = 0
        mapId = self.c.getPlayer().getMapId()
        try:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(物品ID)
            for cserv1 in ChannelServer.getAllInstances():
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    if mch.getMapId() != mapId:
                        continue
                    if 数量 >= 0:
                        if not MapleInventoryManipulator.checkSpace(mch.getClient(), 物品ID, 数量, ""):
                            return 0
                        if (type == (MapleInventoryType.EQUIP) and not GameConstants.isThrowingStar(物品ID) and not GameConstants.isBullet(物品ID)) or (type == (MapleInventoryType.CASH) and 物品ID >= 5000000 and 物品ID <= 5000100):
                            item = ii.getEquipById(物品ID)
                            if ii.isCash(物品ID):
                                item.setUniqueId(1)
                            if 力量 > 0 and 力量 <= 32767:
                                item.setStr(力量)
                            if 敏捷 > 0 and 敏捷 <= 32767:
                                item.setDex(敏捷)
                            if 智力 > 0 and 智力 <= 32767:
                                item.setInt(智力)
                            if 运气 > 0 and 运气 <= 32767:
                                item.setLuk(运气)
                            if 攻击力 > 0 and 攻击力 <= 32767:
                                item.setWatk(攻击力)
                            if 魔法力 > 0 and 魔法力 <= 32767:
                                item.setMatk(魔法力)
                            if 物理防御 > 0 and 物理防御 <= 32767:
                                item.setWdef(物理防御)
                            if 魔法防御 > 0 and 魔法防御 <= 32767:
                                item.setMdef(魔法防御)
                            if HP > 0 and HP <= 30000:
                                item.setHp(HP)
                            if MP > 0 and MP <= 30000:
                                item.setMp(MP)
                            if "可以交易" == (是否可以交易):
                                flag = item.getFlag()
                                if item.getType() == MapleInventoryType.EQUIP.getType():
                                    flag |= ItemFlag.KARMA_EQ.getValue()
                                else:
                                    flag |= ItemFlag.KARMA_USE.getValue()
                                item.setFlag(flag)
                            if 给予时间 > 0:
                                item.setExpiration(int(time.time() * 1000) + 给予时间 * 24 * 60 * 60 * 1000)
                            if 可加卷次数 > 0:
                                item.setUpgradeSlots(可加卷次数)
                            if 制作人名字 is not None:
                                item.setOwner(制作人名字)
                            name = ii.getName(物品ID)
                            if 物品ID / 10000 == 114 and name is not None and name > 0:
                                msg = "你已获得称号 <" + name + ">"
                                mch.getClient().getPlayer().dropMessage(5, msg)
                            MapleInventoryManipulator.addbyItem(mch.getClient(), item.copy())
                        else:
                            MapleInventoryManipulator.addById(mch.getClient(), 物品ID, 数量, "", None, 给予时间, 0)
                    else:
                        MapleInventoryManipulator.removeById(mch.getClient(), GameConstants.getInventoryType(物品ID), 物品ID, -数量, True, False)
                    mch.getClient().getSession().write(MaplePacketCreator.getShowItemGain(物品ID, 数量, True))
                    count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给当前地图发物品出错：" + e.getMessage())
        return count

    def translated_给当前频道发物品(self, 物品ID: int, 数量: int, 力量: int, 敏捷: int, 智力: int, 运气: int, HP: int, MP: int, 可加卷次数: int, 制作人名字: str, 给予时间: int, 是否可以交易: str, 攻击力: int, 魔法力: int, 物理防御: int, 魔法防御: int) -> int:
        count = 0
        chlId = self.c.getPlayer().getMap().getChannel()
        try:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(物品ID)
            for cserv1 in ChannelServer.getAllInstances():
                if cserv1.getChannel() != chlId:
                    continue
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    if 数量 >= 0:
                        if not MapleInventoryManipulator.checkSpace(mch.getClient(), 物品ID, 数量, ""):
                            return 0
                        if (type == (MapleInventoryType.EQUIP) and not GameConstants.isThrowingStar(物品ID) and not GameConstants.isBullet(物品ID)) or (type == (MapleInventoryType.CASH) and 物品ID >= 5000000 and 物品ID <= 5000100):
                            item = ii.getEquipById(物品ID)
                            if ii.isCash(物品ID):
                                item.setUniqueId(1)
                            if 力量 > 0 and 力量 <= 32767:
                                item.setStr(力量)
                            if 敏捷 > 0 and 敏捷 <= 32767:
                                item.setDex(敏捷)
                            if 智力 > 0 and 智力 <= 32767:
                                item.setInt(智力)
                            if 运气 > 0 and 运气 <= 32767:
                                item.setLuk(运气)
                            if 攻击力 > 0 and 攻击力 <= 32767:
                                item.setWatk(攻击力)
                            if 魔法力 > 0 and 魔法力 <= 32767:
                                item.setMatk(魔法力)
                            if 物理防御 > 0 and 物理防御 <= 32767:
                                item.setWdef(物理防御)
                            if 魔法防御 > 0 and 魔法防御 <= 32767:
                                item.setMdef(魔法防御)
                            if HP > 0 and HP <= 30000:
                                item.setHp(HP)
                            if MP > 0 and MP <= 30000:
                                item.setMp(MP)
                            if "可以交易" == (是否可以交易):
                                flag = item.getFlag()
                                if item.getType() == MapleInventoryType.EQUIP.getType():
                                    flag |= ItemFlag.KARMA_EQ.getValue()
                                else:
                                    flag |= ItemFlag.KARMA_USE.getValue()
                                item.setFlag(flag)
                            if 给予时间 > 0:
                                item.setExpiration(int(time.time() * 1000) + 给予时间 * 24 * 60 * 60 * 1000)
                            if 可加卷次数 > 0:
                                item.setUpgradeSlots(可加卷次数)
                            if 制作人名字 is not None:
                                item.setOwner(制作人名字)
                            name = ii.getName(物品ID)
                            if 物品ID / 10000 == 114 and name is not None and name > 0:
                                msg = "你已获得称号 <" + name + ">"
                                mch.getClient().getPlayer().dropMessage(5, msg)
                            MapleInventoryManipulator.addbyItem(mch.getClient(), item.copy())
                        else:
                            MapleInventoryManipulator.addById(mch.getClient(), 物品ID, 数量, "", None, 给予时间, 0)
                    else:
                        MapleInventoryManipulator.removeById(mch.getClient(), GameConstants.getInventoryType(物品ID), 物品ID, -数量, True, False)
                    mch.getClient().getSession().write(MaplePacketCreator.getShowItemGain(物品ID, 数量, True))
                    count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给当前频道发物品出错：" + e.getMessage())
        return count

    def translated_是否是认证玩家(self) -> int:
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) as DATA FROM 会员 WHERE name = ?")
            try:
                ps.setString(1, self.getName())
                # try-with-resources: final ResultSet rs = ps.executeQuery()
                try:
                    if rs.next():
                        return rs.getInt("DATA")
        except Exception as Ex:
            print("查询认证玩家出错 - 数据库查询失败：" + Ex)
        return 0

    def translated_白名单(self) -> int:
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) as DATA FROM 白名单 WHERE name = ?")
            try:
                ps.setString(1, self.getName())
                # try-with-resources: final ResultSet rs = ps.executeQuery()
                try:
                    if rs.next():
                        return rs.getInt("DATA")
        except Exception as Ex:
            print("查询白名单出错 - 数据库查询失败：" + Ex)
        return 0

    def translated_判断当前地图是否已禁用此脚本(self, scriptId: int) -> bool:
        try:
            mapId = self.c.getPlayer().getMapId()
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) as DATA FROM 禁用脚本地图 WHERE scriptId = ? AND mapId = ?")
            try:
                ps.setInt(1, scriptId)
                ps.setInt(2, mapId)
                # try-with-resources: final ResultSet rs = ps.executeQuery()
                try:
                    if rs.next():
                        return rs.getInt("DATA") > 0
        except Exception as Ex:
            print("判断当前地图是否已禁用此脚本出错 - 数据库查询失败：" + Ex)
        return False

    def translated_认证主播(self) -> int:
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) as DATA FROM 认证主播 WHERE name = ?")
            try:
                ps.setString(1, self.getName())
                # try-with-resources: final ResultSet rs = ps.executeQuery()
                try:
                    if rs.next():
                        return rs.getInt("DATA")
        except Exception as Ex:
            print("查询认证主播出错 - 数据库查询失败：" + Ex)
        return 0

    def translated_传送当前地图所有人到指定地图(self, destMapId: int, includeSelf: bool) -> int:
        count = 0
        myMapId = self.c.getPlayer().getMapId()
        myId = self.c.getPlayer().getId()
        try:
            tomap = self.getMapFactory().getMap(destMapId)
            frommap = self.getMapFactory().getMap(myMapId)
            list = frommap.getCharactersThreadsafe()
            if tomap is not None and frommap is not None and list is not None and frommap.getCharactersSize() > 0:
                for mmo in list:
                    chr = mmo
                    if chr.getId() == myId:
                        if not includeSelf:
                            continue
                        chr.changeMap(tomap, tomap.getPortal(0))
                        count += 1
                    else:
                        chr.changeMap(tomap, tomap.getPortal(0))
                        count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("传送当前地图所有人到指定地图出错：" + e.getMessage())
        return count

    def translated_杀死当前地图所有人(self, includeSelf: bool) -> int:
        count = 0
        myMapId = self.c.getPlayer().getMapId()
        myId = self.c.getPlayer().getId()
        try:
            frommap = self.getMapFactory().getMap(myMapId)
            list = frommap.getCharactersThreadsafe()
            if frommap is not None and list is not None and frommap.getCharactersSize() > 0:
                for mmo in list:
                    if mmo is not None:
                        chr = mmo
                        if chr.getId() == myId:
                            if not includeSelf:
                                continue
                            chr.setHp(0)
                            chr.updateSingleStat(MapleStat.HP, 0)
                            count += 1
                        else:
                            chr.setHp(0)
                            chr.updateSingleStat(MapleStat.HP, 0)
                            count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("杀死当前地图所有人出错：" + e.getMessage())
        return count

    def translated_复活当前地图所有人(self, includeSelf: bool) -> int:
        count = 0
        myMapId = self.c.getPlayer().getMapId()
        myId = self.c.getPlayer().getId()
        try:
            frommap = self.getMapFactory().getMap(myMapId)
            list = frommap.getCharactersThreadsafe()
            if frommap is not None and list is not None and frommap.getCharactersSize() > 0:
                for mmo in list:
                    if mmo is not None:
                        chr = mmo
                        if chr.getId() == myId:
                            if not includeSelf:
                                continue
                            chr.getStat().setHp(chr.getStat().getMaxHp())
                            chr.updateSingleStat(MapleStat.HP, chr.getStat().getMaxHp())
                            chr.getStat().setMp(chr.getStat().getMaxMp())
                            chr.updateSingleStat(MapleStat.MP, chr.getStat().getMaxMp())
                            chr.dispelDebuffs()
                            count += 1
                        else:
                            chr.getStat().setHp(chr.getStat().getMaxHp())
                            chr.updateSingleStat(MapleStat.HP, chr.getStat().getMaxHp())
                            chr.getStat().setMp(chr.getStat().getMaxMp())
                            chr.updateSingleStat(MapleStat.MP, chr.getStat().getMaxMp())
                            chr.dispelDebuffs()
                            count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("复活当前地图所有人出错：" + e.getMessage())
        return count

    def translated_跟踪玩家(self, charName: str) -> None:
        for chl in ChannelServer.getAllInstances():
            for chr in chl.getPlayerStorage().getAllCharacters():
                if chr.getName() == charName:
                    self.c.getPlayer().changeMap(chr.getMapId())

    def translated_给指定地图发物品(self, 地图ID: int, 物品ID: int, 数量: int, 力量: int, 敏捷: int, 智力: int, 运气: int, HP: int, MP: int, 可加卷次数: int, 制作人名字: str, 给予时间: int, 是否可以交易: str, 攻击力: int, 魔法力: int, 物理防御: int, 魔法防御: int) -> int:
        count = 0
        if 地图ID < 1:
            地图ID = self.c.getPlayer().getMapId()
        try:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(物品ID)
            frommap = self.getMapFactory().getMap(地图ID)
            list = frommap.getCharactersThreadsafe()
            if list is not None and frommap.getCharactersSize() > 0:
                for mmo in list:
                    if mmo is not None:
                        chr = mmo
                        if 数量 >= 0:
                            if not MapleInventoryManipulator.checkSpace(chr.getClient(), 物品ID, 数量, ""):
                                return 0
                            if (type == (MapleInventoryType.EQUIP) and not GameConstants.isThrowingStar(物品ID) and not GameConstants.isBullet(物品ID)) or (type == (MapleInventoryType.CASH) and 物品ID >= 5000000 and 物品ID <= 5000100):
                                item = ii.getEquipById(物品ID)
                                if ii.isCash(物品ID):
                                    item.setUniqueId(1)
                                if 力量 > 0 and 力量 <= 32767:
                                    item.setStr(力量)
                                if 敏捷 > 0 and 敏捷 <= 32767:
                                    item.setDex(敏捷)
                                if 智力 > 0 and 智力 <= 32767:
                                    item.setInt(智力)
                                if 运气 > 0 and 运气 <= 32767:
                                    item.setLuk(运气)
                                if 攻击力 > 0 and 攻击力 <= 32767:
                                    item.setWatk(攻击力)
                                if 魔法力 > 0 and 魔法力 <= 32767:
                                    item.setMatk(魔法力)
                                if 物理防御 > 0 and 物理防御 <= 32767:
                                    item.setWdef(物理防御)
                                if 魔法防御 > 0 and 魔法防御 <= 32767:
                                    item.setMdef(魔法防御)
                                if HP > 0 and HP <= 30000:
                                    item.setHp(HP)
                                if MP > 0 and MP <= 30000:
                                    item.setMp(MP)
                                if "可以交易" == (是否可以交易):
                                    flag = item.getFlag()
                                    if item.getType() == MapleInventoryType.EQUIP.getType():
                                        flag |= ItemFlag.KARMA_EQ.getValue()
                                    else:
                                        flag |= ItemFlag.KARMA_USE.getValue()
                                    item.setFlag(flag)
                                if 给予时间 > 0:
                                    item.setExpiration(int(time.time() * 1000) + 给予时间 * 24 * 60 * 60 * 1000)
                                if 可加卷次数 > 0:
                                    item.setUpgradeSlots(可加卷次数)
                                if 制作人名字 is not None:
                                    item.setOwner(制作人名字)
                                name = ii.getName(物品ID)
                                if 物品ID / 10000 == 114 and name is not None and name > 0:
                                    msg = "你已获得称号 <" + name + ">"
                                    chr.dropMessage(5, msg)
                                MapleInventoryManipulator.addbyItem(chr.getClient(), item.copy())
                            else:
                                MapleInventoryManipulator.addById(chr.getClient(), 物品ID, 数量, "", None, 给予时间, 0)
                        else:
                            MapleInventoryManipulator.removeById(chr.getClient(), GameConstants.getInventoryType(物品ID), 物品ID, -数量, True, False)
                        chr.getClient().getSession().write(MaplePacketCreator.getShowItemGain(物品ID, 数量, True))
                        count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给指定地图发物品出错：" + e.getMessage())
        return count

    def translated_给指定地图发物品_地图ID_物品ID_数量(self, 地图ID: int, 物品ID: int, 数量: int) -> int:
        return self.给指定地图发物品(地图ID, 物品ID, 数量, 0, 0, 0, 0, 0, 0, 0, "", 0, "", 0, 0, 0, 0)

    def translated_给指定地图发点卷(self, 地图ID: int, 数量: int, 类型: int) -> int:
        count = 0
        name = self.c.getPlayer().getName()
        if 地图ID < 1:
            地图ID = self.c.getPlayer().getMapId()
        try:
            if 数量 <= 0 or 类型 <= 0:
                return 0
            frommap = self.getMapFactory().getMap(地图ID)
            list = frommap.getCharactersThreadsafe()
            if list is not None and frommap.getCharactersSize() > 0:
                if 类型 == 1 or 类型 == 2:
                    for mmo in list:
                        if mmo is not None:
                            chr = mmo
                            chr.modifyCSPoints(类型, 数量)
                            cash = None
                            if 类型 == 1:
                                cash = "点卷"
                            elif 类型 == 2:
                                cash = "抵用卷"
                            count += 1
                elif 类型 == 3:
                    for mmo in list:
                        if mmo is not None:
                            chr = mmo
                            chr.gainMeso(数量, True)
                            count += 1
                elif 类型 == 4:
                    for mmo in list:
                        if mmo is not None:
                            chr = mmo
                            chr.gainExp(数量, True, False, True)
                            count += 1
        except Exception as e:
            self.c.getPlayer().dropMessage("给指定地图发点卷出错：" + e.getMessage())
        return count

    def translated_获取指定地图玩家数量(self, mapId: int) -> int:
        return self.getMapFactory().getMap(mapId).characterSize()

    def translated_给指定地图发公告(self, mapId: int, msg: str, itemId: int) -> None:
        self.getMapFactory().getMap(mapId).startMapEffect(msg, itemId)

    def getServerName(self) -> str:
        return ServerProperties.getProperty("RoyMS.ServerName")

    def translated_克隆(self) -> None:
        self.c.getPlayer().cloneLook()

    def translated_取消克隆(self) -> None:
        self.c.getPlayer().disposeClones()

    def translated_设置天气(self, 天气ID: int) -> None:
        if self.c.getPlayer().getMap().getPermanentWeather() > 0:
            self.c.getPlayer().getMap().setPermanentWeather(0)
            self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.removeMapEffect())
        elif not MapleItemInformationProvider.getInstance().itemExists(天气ID) or 天气ID / 10000 != 512:
            self.c.getPlayer().dropMessage(5, "无效的天气ID。")
        else:
            self.c.getPlayer().getMap().setPermanentWeather(天气ID)
            self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.startMapEffect("", 天气ID, False))
            self.c.getPlayer().dropMessage(5, "地图天气已启用。")

    def MapleMSpvpkills(self) -> None:
        MapleGuildRanking.MapleMSpvpkills(self.c, self.npc)

    def MapleMSpvpdeaths(self) -> None:
        MapleGuildRanking.MapleMSpvpdeaths(self.c, self.npc)

    def translated_爆物开关(self) -> None:
        self.c.getPlayer().getMap().toggleDrops()

    def translated_发言(self, 内容: list) -> None:
        for cserv in ChannelServer.getAllInstances():
            for victim in cserv.getPlayerStorage().getAllCharacters():
                if victim.getId() != self.c.getPlayer().getId():
                    victim.getMap().broadcastMessage(MaplePacketCreator.getChatText(victim.getId(), StringUtil.joinStringFrom(内容, 1), victim.isGM(), 0))

    def translated_人气排行榜(self) -> None:
        MapleGuild.人气排行(self.getClient(), self.npc)

    def translated_豆豆排行榜(self) -> None:
        MapleGuild.豆豆排行(self.getClient(), self.npc)

    def translated_战斗力排行榜(self) -> None:
        MapleGuild.战斗力排行(self.getClient(), self.npc)

    def translated_破攻排行榜(self) -> None:
        MapleGuild.破攻排行(self.getClient(), self.npc)

    def translated_杀怪排行榜(self) -> None:
        MapleGuild.杀怪排行榜(self.getClient(), self.npc)

    def translated_总在线时间排行榜(self) -> None:
        MapleGuild.总在线时间排行(self.getClient(), self.npc)

    def translated_查询今日在线时间(self) -> int:
        data = 0
        con = DatabaseConnection.getConnection()
        try:
            psu = con.prepareStatement("SELECT todayOnlineTime FROM characters WHERE id = ?")
            psu.setInt(1, self.c.getPlayer().getId())
            rs = psu.executeQuery()
            if rs.next():
                data = rs.getInt("todayOnlineTime")
            rs.close()
            psu.close()
        except Exception as ex:
            print("查询今日在线时间出错：" + ex.getMessage())
        return data

    def translated_查询总在线时间(self) -> int:
        data = 0
        con = DatabaseConnection.getConnection()
        try:
            psu = con.prepareStatement("SELECT totalOnlineTime FROM characters WHERE id = ?")
            psu.setInt(1, self.c.getPlayer().getId())
            rs = psu.executeQuery()
            if rs.next():
                data = rs.getInt("totalOnlineTime")
            rs.close()
            psu.close()
        except Exception as ex:
            print("查询总在线时间出错：" + ex.getMessage())
        return data

    def translated_查询在线人数(self) -> int:
        count = 0
        for chl in ChannelServer.getAllInstances():
            count += chl.getPlayerStorage().getAllCharacters()
        return count

    def translated_获取最高玩家等级(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高等级玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `level` FROM characters WHERE gm = 0 ORDER BY `level` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("level")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家人气(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高人气玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `fame` FROM characters WHERE gm = 0 ORDER BY `fame` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("fame")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家金币(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高金币玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `meso` FROM characters WHERE gm = 0 ORDER BY `meso` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("meso")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家在线(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高在线玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `totalOnlineTime` FROM characters WHERE gm = 0 ORDER BY `totalOnlineTime` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("totalOnlineTime")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取家族名称(self, guildId: int) -> str:
        data = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT name as DATA FROM guilds WHERE guildid = ?")
            ps.setInt(1, guildId)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getString("DATA")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取自己等级排名(self) -> int:
        DATA = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT rank FROM (SELECT @rownum := @rownum + 1 AS rank, `name`, `level`, `id` FROM characters, (SELECT @rownum := 0) r WHERE gm = 0 ORDER BY `level` DESC) AS T1 WHERE `id` = ?")
            ps.setInt(1, self.c.getPlayer().getId())
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    DATA = rs.getInt("rank")
            ps.close()
        except Exception as Ex:
            print("获取自己等级排名出错 - 数据库查询失败：" + Ex)
        return DATA

    def GetPlayerList(self) -> str:
        ret = ""
        for cs in ChannelServer.getAllInstances():
            for chr in cs.getPlayerStorage().getAllCharacters():
                if not chr.isGM():
                    ret = ret + "#b#L" + chr.getId() + "#[跟踪] 玩家名: #r" + chr.getName() + " #k#l \r\n"
        return ret

    def GetPlayer(self, cid: int) -> Any:
        ret = None
        for cs in ChannelServer.getAllInstances():
            for chr in cs.getPlayerStorage().getAllCharacters():
                if not chr.isGM() and chr.getId() == cid:
                    ret = chr
        return ret

    def getItemName(self, id: int) -> str:
        ii = MapleItemInformationProvider.getInstance()
        return ii.getName(id)

    def translated_进入商城1(self) -> None:
        try:
            chr = self.c.getPlayer()
            if chr.getBuffedValue(MapleBuffStat.召唤兽) is not None:
                chr.cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
            socket = self.c.getChannelServer().getIP().split(":")
            ch = ChannelServer.getInstance(self.c.getChannel())
            chr.changeRemoval()
            if chr.getMessenger() is not None:
                messengerplayer = MapleMessengerCharacter(chr)
                World.Messenger.leaveMessenger(chr.getMessenger().getId(), messengerplayer)
            PlayerBuffStorage.addBuffsToStorage(chr.getId(), chr.getAllBuffs())
            PlayerBuffStorage.addCooldownsToStorage(chr.getId(), chr.getCooldowns())
            PlayerBuffStorage.addDiseaseToStorage(chr.getId(), chr.getAllDiseases())
            World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), -10)
            ch.removePlayer(chr)
            self.c.updateLoginState(MapleClient.CHANGE_CHANNEL, self.c.getSessionIPAddress())
            self.c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(CashShopServer.getIP().split(":")[1])))
            chr.saveToDB(False, False)
            chr.getMap().removePlayer(chr)
            self.c.getPlayer().expirationTask(True, False)
            self.c.setPlayer(None)
            self.c.setReceiving(False)
        except UnknownHostException as ex:
            Logger.getLogger(NPCConversationManager.class.getName()).log(Level.SEVERE, None, ex)

    def translated_进入商城2(self) -> None:
        try:
            chr = self.c.getPlayer()
            socket = self.c.getChannelServer().getIP().split(":")
            ch = ChannelServer.getInstance(self.c.getChannel())
            chr.changeRemoval()
            if chr.getMessenger() is not None:
                messengerplayer = MapleMessengerCharacter(chr)
                World.Messenger.leaveMessenger(chr.getMessenger().getId(), messengerplayer)
            PlayerBuffStorage.addBuffsToStorage(chr.getId(), chr.getAllBuffs())
            PlayerBuffStorage.addCooldownsToStorage(chr.getId(), chr.getCooldowns())
            PlayerBuffStorage.addDiseaseToStorage(chr.getId(), chr.getAllDiseases())
            World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), -20)
            ch.removePlayer(chr)
            self.c.updateLoginState(MapleClient.CHANGE_CHANNEL, self.c.getSessionIPAddress())
            self.c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(CashShopServer.getIP().split(":")[1])))
            chr.saveToDB(False, False)
            chr.getMap().removePlayer(chr)
            self.c.getPlayer().expirationTask(True, False)
            self.c.setPlayer(None)
            self.c.setReceiving(False)
        except UnknownHostException as ex:
            Logger.getLogger(NPCConversationManager.class.getName()).log(Level.SEVERE, None, ex)

    def translated_获取分解的矿石(self) -> int:
        return GameConstants.分解的矿石()

    def getMount(self, s: int) -> int:
        return GameConstants.getMountS(s)

    def translated_喇叭(self, lx: int, msg: str) -> None:
        # switch (lx):
            # case 1:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 2:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(12, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 3:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 4:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(9, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 5:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(6, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 6:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(18, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break
            # case 7:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(10, self.c.getChannel(), "[全服公告] : " + msg).encode("utf-8"))
                break

    def translated_即时存档(self) -> None:
        self.c.getPlayer().saveToDB(True, True)

    def translated_刷新状态(self) -> None:
        self.c.getPlayer().getClient().getSession().write(MaplePacketCreator.getCharInfo(self.c.getPlayer()))
        self.c.getPlayer().getMap().removePlayer(self.c.getPlayer())
        self.c.getPlayer().getMap().addPlayer(self.c.getPlayer())
        self.c.getSession().write(MaplePacketCreator.enableActions())

    def translated_刷新地图(self) -> None:
        custMap = True
        mapid = self.c.getPlayer().getMapId()
        map = custMap ? self.c.getPlayer().getClient().getChannelServer().getMapFactory().getMap(mapid) : self.c.getPlayer().getMap()
        if self.c.getPlayer().getClient().getChannelServer().getMapFactory().destroyMap(mapid):
            newMap = self.c.getPlayer().getClient().getChannelServer().getMapFactory().getMap(mapid)
            newPor = newMap.getPortal(0)
            mcs = new LinkedHashSet<MapleCharacter>(map.getCharacters())
            for m in mcs:
                x = 0
                while x < 5:
                    try:
                        m.changeMap(newMap, newPor)
                    except Exception as t:
                        x += 1
                        continue
                    break

    def translated_组队征集喇叭(self, lx: int, msg: str) -> None:
        # switch (lx):
            # case 1:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, self.c.getChannel(), "[组队征集令] : " + msg).encode("utf-8"))
                break
            # case 2:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(12, self.c.getChannel(), "[组队征集令]: " + msg).encode("utf-8"))
                break
            # case 3:
                World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, self.c.getChannel(), "[组队征集令]: " + msg).encode("utf-8"))
                break

    def deleteItem(self, inventorytype: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("Select * from inventoryitems where characterid=? and inventorytype=?")
            ps.setInt(1, self.getPlayer().getId())
            ps.setInt(2, inventorytype)
            re = ps.executeQuery()
            type = None
            # switch (inventorytype):
                # case 1:
                    type = MapleInventoryType.EQUIP
                    break
                # case 2:
                    type = MapleInventoryType.USE
                    break
                # case 3:
                    type = MapleInventoryType.SETUP
                    break
                # case 4:
                    type = MapleInventoryType.ETC
                    break
                # case 5:
                    type = MapleInventoryType.CASH
                    break
            while re.next():
                MapleInventoryManipulator.removeById(self.getC(), type, re.getInt("itemid"), re.getInt("quantity"), True, True)
            re.close()
            ps.close()
        except SQLException as ex:
            pass

    def translated_全服漂浮喇叭(self, msg: str, itemId: int) -> None:
        ret = 0
        for cserv in ChannelServer.getAllInstances():
            for mch in cserv.getPlayerStorage().getAllCharacters():
                mch.startMapEffect(msg, itemId)
                ret += 1

    def translated_气泡喇叭(self, 气泡喇叭: str) -> None:
        self.getClient().getSession().write(MaplePacketCreator.sendHint(气泡喇叭, 200, 200))

    def getHour(self) -> int:
        return Calendar.getInstance().get(11)

    def getMin(self) -> int:
        return Calendar.getInstance().get(12)

    def getSec(self) -> int:
        return Calendar.getInstance().get(13)

    def Startqmdb(self) -> None:
        for ii in range(= 20):
            Thread.sleep(700)
            总数 = self.getPlayer().获取全民夺宝总数()
            a = random.random() * 总数 + 1.0
            A = Double(a)
            iterator = ChannelServer.getAllInstances().iterator()
            if iterator.hasNext():
                cserv1 = iterator.next()
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    mch.getClient().getSession().write(MaplePacketCreator.sendHint("#b===========全民冒险岛==========#k\r\n==============================#r\r\n#b========全民夺宝活动开始=======#k\r\n==============================#r\r\n#b===========随机抽取中==========#k\r\n◆正在随机抽选中奖的幸运玩家◆\r\n#b===========幸运玩家===========#r\r\n" + mch.全民夺宝2(A), 200, 200))
                    if ii == 20:
                        mch.getClient().getSession().write(MaplePacketCreator.sendHint("#e#r★★★★★全民夺宝★★★★★\r\n中奖玩家：" + mch.全民夺宝2(A), 200, 200))
                        mch.startMapEffect("★恭喜玩家:" + mch.全民夺宝2(A) + " 赢得了 [全民夺宝] not not ★", 5120025)
                        self.c.getSession().write(MaplePacketCreator.enableActions())

    def translated_谁是卧底(self) -> None:
        def _task_1():
            pass

        if self.getPlayer().getParty() is None or self.getPlayer().getParty().getMembers() < 6:
            return
        cMap = self.getPlayer().getMapId()
        随机给予卧底值 = Randomizer.nextInt(6)
        随机给予卧底值2 = Randomizer.nextInt(6)
        人数 = self.getPlayer().getParty().getMembers()
        确定人数 = 0
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None and curChar.getMapId() == cMap:
                确定人数 += 1
                if (随机给予卧底值 == 随机给予卧底值2) {}
                if 人数 != 确定人数:
                    continue
                final Timer.MapTimer tMan = Timer.MapTimer.getInstance()
                tMan.schedule(_task_1, 60000)

    def translated_家族排行榜(self) -> None:
        MapleGuild.displayGuildRanks(self.getClient(), self.npc)

    def translated_等级排行榜(self) -> None:
        MapleGuild.displayLevelRanks(self.getClient(), self.npc)

    def translated_金币排行榜(self) -> None:
        MapleGuild.meso(self.getClient(), self.npc)

    def translated_VIP排行榜(self) -> None:
        MapleGuild.VIP排行(self.getClient(), self.npc)

    def getEquipId(self, slot: int) -> int:
        equip = self.getPlayer().getInventory(MapleInventoryType.EQUIP)
        eu = equip.getItem(slot)
        if eu is None:
            return -1
        return equip.getItem(slot).getItemId()

    def getUseId(self, slot: int) -> int:
        use = self.getPlayer().getInventory(MapleInventoryType.USE)
        return use.getItem(slot).getItemId()

    def getSetupId(self, slot: int) -> int:
        setup = self.getPlayer().getInventory(MapleInventoryType.SETUP)
        return setup.getItem(slot).getItemId()

    def getCashId(self, slot: int) -> int:
        cash = self.getPlayer().getInventory(MapleInventoryType.CASH)
        return cash.getItem(slot).getItemId()

    def getETCId(self, slot: int) -> int:
        etc = self.getPlayer().getInventory(MapleInventoryType.ETC)
        return etc.getItem(slot).getItemId()

    def EquipList(self, c: Any) -> str:
        str = ""
        equip = c.getPlayer().getInventory(MapleInventoryType.EQUIP)
        stra = []
        for item in equip.list():
            stra.add("#L" + item.getPosition() + "##v" + item.getItemId() + "##l")
        for strb in stra:
            str.append(strb)
        return str

    def UseList(self, c: Any) -> str:
        str = ""
        use = c.getPlayer().getInventory(MapleInventoryType.USE)
        stra = []
        for item in use.list():
            stra.add("#L" + item.getPosition() + "##v" + item.getItemId() + "##l")
        for strb in stra:
            str.append(strb)
        return str

    def CashList(self, c: Any) -> str:
        str = ""
        cash = c.getPlayer().getInventory(MapleInventoryType.CASH)
        stra = []
        for item in cash.list():
            stra.add("#L" + item.getPosition() + "##v" + item.getItemId() + "##l")
        for strb in stra:
            str.append(strb)
        return str

    def ETCList(self, c: Any) -> str:
        str = ""
        etc = c.getPlayer().getInventory(MapleInventoryType.ETC)
        stra = []
        for item in etc.list():
            stra.add("#L" + item.getPosition() + "##v" + item.getItemId() + "##l")
        for strb in stra:
            str.append(strb)
        return str

    def SetupList(self, c: Any) -> str:
        str = ""
        setup = c.getPlayer().getInventory(MapleInventoryType.SETUP)
        stra = []
        for item in setup.list():
            stra.add("#L" + item.getPosition() + "##v" + item.getItemId() + "##l")
        for strb in stra:
            str.append(strb)
        return str

    def getCanHair(self, hairs: list) -> list:
        canHair = []
        cantHair = []
        for hair in hairs:
            if hairExists(hair):
                canHair.add(hair)
            else:
                cantHair.add(hair)
        if cantHair > 0 and self.c.getPlayer().isAdmin():
            sb = ""
            sb.append(cantHair).append("个发型客户端不支持显示，已经被清除：")
            for i in range(cantHair):
                sb.append(cantHair.get(i))
                if i < cantHair - 1:
                    sb.append(",")
            self.playerMessage(sb)
        getHair = new int[canHair]
        for i in range(canHair):
            getHair[i] = canHair.get(i)
        return getHair

    def getCanFace(self, faces: list) -> list:
        canFace = []
        cantFace = []
        for face in faces:
            if faceExists(face):
                canFace.add(face)
            else:
                cantFace.add(face)
        if cantFace > 0 and self.c.getPlayer().isAdmin():
            sb = ""
            sb.append(cantFace).append("个脸型客户端不支持显示，已经被清除：")
            for i in range(cantFace):
                sb.append(cantFace.get(i))
                if i < cantFace - 1:
                    sb.append(",")
            self.playerMessage(sb)
        getFace = new int[canFace]
        for i in range(canFace):
            getFace[i] = canFace.get(i)
        return getFace

    def translated_刷新能力值(self) -> None:
        if self.c.getPlayer().getRemainingAp() < 0:
            self.c.getPlayer().setRemainingAp(0)

    def translated_重载事件(self) -> None:
        iterator = ChannelServer.getAllInstances().iterator()
        if iterator.hasNext():
            instance = iterator.next()
            instance.reloadEvents()

    def translated_重载任务(self) -> None:
        MapleQuest.clearQuests()

    def translated_重载商店(self) -> None:
        MapleShopFactory.getInstance().clear()

    def translated_重载传送点(self) -> None:
        PortalScriptManager.getInstance().clearScripts()

    def translated_重载爆率(self) -> None:
        MapleMonsterInformationProvider.getInstance().clearDrops()

    def translated_重载反应堆(self) -> None:
        ReactorScriptManager.getInstance().clearDrops()

    def openNpc(self, id: int) -> None:
        NPCScriptManager.getInstance().start(self.getClient(), id)

    def openNpc_id_wh(self, id: int, wh: int) -> None:
        NPCScriptManager.getInstance().dispose(self.c)
        NPCScriptManager.getInstance().start(self.getClient(), id, wh)

    def getjf(self) -> int:
        return self.c.getPlayer().getjf()

    def gainjf(self, s: int) -> None:
        self.c.getPlayer().gainjf(s)

    def setjf(self, s: int) -> None:
        self.c.getPlayer().setjf(s)

    def getdjjl(self) -> int:
        return self.c.getPlayer().getdjjl()

    def setdjjl(self, s: int) -> None:
        self.c.getPlayer().setdjjl(s)

    def gaindjjl(self, s: int) -> None:
        self.c.getPlayer().gaindjjl(s)

    def EnterCS(self) -> None:
        try:
            chr = self.c.getPlayer()
            socket = self.c.getChannelServer().getIP().split(":")
            ch = ChannelServer.getInstance(self.c.getChannel())
            chr.changeRemoval()
            if chr.getMessenger() is not None:
                messengerplayer = MapleMessengerCharacter(chr)
                World.Messenger.leaveMessenger(chr.getMessenger().getId(), messengerplayer)
            PlayerBuffStorage.addBuffsToStorage(chr.getId(), chr.getAllBuffs())
            PlayerBuffStorage.addCooldownsToStorage(chr.getId(), chr.getCooldowns())
            PlayerBuffStorage.addDiseaseToStorage(chr.getId(), chr.getAllDiseases())
            World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), -20)
            ch.removePlayer(chr)
            self.c.updateLoginState(MapleClient.CHANGE_CHANNEL, self.c.getSessionIPAddress())
            self.c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(CashShopServer.getIP().split(":")[1])))
            chr.saveToDB(False, False)
            chr.getMap().removePlayer(chr)
            self.c.setPlayer(None)
            self.c.setReceiving(False)
        except UnknownHostException as ex:
            Logger.getLogger(NPCConversationManager.class.getName()).log(Level.SEVERE, None, ex)

    def getForum(self) -> list:
        return Forum_Section.getAllSection()

    def addSection(self, name: str) -> bool:
        return Forum_Section.addSection(name)

    def deleteSection(self, id: int) -> bool:
        return Forum_Section.deleteSection(id)

    def getSectionById(self, id: int) -> Any:
        return Forum_Section.getSectionById(id)

    def getCurrentAllThread(self, sid: int) -> list:
        return Forum_Thread.getCurrentAllThread(sid)

    def getThreadById(self, sid: int, id: int) -> Any:
        return Forum_Thread.getThreadById(sid, id)

    def getThreadByName(self, sid: int, name: str) -> Any:
        return Forum_Thread.getThreadByName(sid, name)

    def addThread(self, sid: int, tname: str, cid: int, cname: str) -> bool:
        return Forum_Thread.addThread(sid, tname, cid, cname)

    def deleteThread(self, sid: int, tid: int) -> bool:
        return Forum_Thread.deleteThread(sid, tid, False)

    def getCurrentAllReply(self, tid: int) -> list:
        return Forum_Reply.getCurrentAllReply(tid)

    def addReply(self, tid: int, cid: int, cname: str, news: str) -> bool:
        return Forum_Reply.addReply(tid, cid, cname, news)

    def translated_获取怪物id(self, id: int) -> Any:
        return self.c.getPlayer().getMap().getMonsterById(id)

