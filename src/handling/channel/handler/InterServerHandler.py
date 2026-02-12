"""
InterServerHandler - Converted from Java source
Original: handling/channel/handler/InterServerHandler.java
Package: handling.channel.handler
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from socket import socket
from typing import Collection
from typing import Iterator
from typing import List
from typing import Optional, Any
import logging
import pymysql

# Internal module imports
# from client.BuddyEntry import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.CharacterIdChannelPair import *  # TODO: import specific classes
# from handling.world.CharacterTransfer import *  # TODO: import specific classes
# from handling.world.MapleMessenger import *  # TODO: import specific classes
# from handling.world.MapleMessengerCharacter import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PartyOperation import *  # TODO: import specific classes
# from handling.world.PlayerBuffStorage import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from scripting.EventInstanceManager import *  # TODO: import specific classes
# from scripting.EventManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from tools.DateUtil import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.FamilyPacket import *  # TODO: import specific classes


class InterServerHandler:
    """
    Class InterServerHandler
    """


    def EnterCS(self, c: Any, chr: Any) -> None:
        if c.getPlayer().getMap().getId() != 180000001:
            if !c.getChannelServer().WarpCSShop():
                try:
                    socket = c.getChannelServer().getIP().split(":")
                    if c.getPlayer().getBuffedValue(MapleBuffStat.召唤兽) is not None:
                        c.getPlayer().cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
                    ch = ChannelServer.getInstance(c.getChannel())
                    chr.changeRemoval()
                    if chr.getMessenger() is not None:
                        messengerplayer = MapleMessengerCharacter(chr)
                        World.Messenger.leaveMessenger(chr.getMessenger().getId(), messengerplayer)
                    PlayerBuffStorage.addBuffsToStorage(chr.getId(), chr.getAllBuffs())
                    PlayerBuffStorage.addCooldownsToStorage(chr.getId(), chr.getCooldowns())
                    PlayerBuffStorage.addDiseaseToStorage(chr.getId(), chr.getAllDiseases())
                    World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), -10)
                    ch.removePlayer(chr)
                    c.updateLoginState(MapleClient.CHANGE_CHANNEL, c.getSessionIPAddress())
                    c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(CashShopServer.getIP().split(":")[1])))
                    chr.saveToDB(False, False)
                    chr.getMap().removePlayer(chr)
                    c.getPlayer().expirationTask(True, False)
                    c.setPlayer(None)
                    c.setReceiving(False)
                except UnknownHostException as ex:
                    Logger.getLogger(InterServerHandler.class.getName()).log(Level.SEVERE, None, ex)
            else:
                NPCScriptManager.getInstance().start(c, 9900004, 9999)
                c.getSession().write(MaplePacketCreator.enableActions())
        else:
            c.getPlayer().dropMessage(1, "你在小黑屋里，无法进行任何操作")
            c.getSession().write(MaplePacketCreator.enableActions())

    def EnterMTS(self, c: Any, chr: Any) -> None:
        if c.getPlayer().getMap().getId() != 180000001:
            if !c.getChannelServer().WarpMTS():
                try:
                    socket = c.getChannelServer().getIP().split(":")
                    if c.getPlayer().getBuffedValue(MapleBuffStat.召唤兽) is not None:
                        c.getPlayer().cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
                    ch = ChannelServer.getInstance(c.getChannel())
                    chr.changeRemoval()
                    if chr.getMessenger() is not None:
                        messengerplayer = MapleMessengerCharacter(chr)
                        World.Messenger.leaveMessenger(chr.getMessenger().getId(), messengerplayer)
                    PlayerBuffStorage.addBuffsToStorage(chr.getId(), chr.getAllBuffs())
                    PlayerBuffStorage.addCooldownsToStorage(chr.getId(), chr.getCooldowns())
                    PlayerBuffStorage.addDiseaseToStorage(chr.getId(), chr.getAllDiseases())
                    World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), -20)
                    ch.removePlayer(chr)
                    c.updateLoginState(MapleClient.CHANGE_CHANNEL, c.getSessionIPAddress())
                    c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(CashShopServer.getIP().split(":")[1])))
                    chr.saveToDB(False, False)
                    chr.getMap().removePlayer(chr)
                    c.setPlayer(None)
                    c.setReceiving(False)
                except UnknownHostException as ex:
                    Logger.getLogger(InterServerHandler.class.getName()).log(Level.SEVERE, None, ex)
            else:
                NPCScriptManager.getInstance().dispose(c)
                if c.getPlayer().getTrade() is not None:
                    c.getPlayer().dropMessage(1, "交易中无法进行其他操作！")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if c.getPlayer().getLevel() >= 1:
                    NPCScriptManager.getInstance().start(c, 9900004)
                    c.getSession().write(MaplePacketCreator.enableActions())
                else:
                    c.getSession().write(MaplePacketCreator.getNPCTalk(9900004, 0, "玩家你好.等级不足1级无法使用快捷功能.", "00 00", 0))
                    c.getSession().write(MaplePacketCreator.enableActions())
        else:
            c.getPlayer().dropMessage(1, "你在小黑屋里，无法进行任何操作")
            c.getSession().write(MaplePacketCreator.enableActions())

    def getSameAccountOtherCharID(self, charid: int) -> list:
        try:
            accountid = 0
            IDs = []
            con = DatabaseConnection.getConnection()
            ps = None
            rs = None
            ps = con.prepareStatement("select * from characters where id = ?")
            ps.setInt(1, charid)
            rs = ps.executeQuery()
            if rs.next():
                accountid = rs.getInt("accountid")
            rs.close()
            ps.close()
            if accountid == 0:
                return None
            ps = con.prepareStatement("select * from characters where accountid = ? and id != ?")
            ps.setInt(1, accountid)
            ps.setInt(2, charid)
            rs = ps.executeQuery()
            while rs.next():
                IDs.add(rs.getInt("id"))
            rs.close()
            ps.close()
            if !IDs == 0:
                return IDs
            return None
        except Exception as ex:
            Logger.getLogger(InterServerHandler.class.getName()).log(Level.SEVERE, None, ex)
            return None

    def Loggedin(self, playerid: int, c: Any) -> None:
        channelServer = c.getChannelServer()
        IDs = getSameAccountOtherCharID(playerid)
        if IDs is not None && IDs > 0:
            for id in IDs:
                channelServer.getPlayerStorage().deregisterPendingPlayer(id)
        transfer = channelServer.getPlayerStorage().getPendingCharacter(playerid)
        firstLoggedIn = True
        player = None
        if transfer is None:
            player = MapleCharacter.loadCharFromDB(playerid, c, True)
        else:
            player = MapleCharacter.ReconstructChr(transfer, c, True)
            firstLoggedIn = False
        c.setPlayer(player)
        c.setAccID(player.getAccountID())
        c.loadAccountData(player.getAccountID())
        ChannelServer.forceRemovePlayerByAccId(c, c.getAccID())
        state = c.getLoginState()
        allowLogin = False
        allowLoginTip = None
        if state == MapleClient.LOGIN_SERVER_TRANSITION || state == MapleClient.CHANGE_CHANNEL || state == MapleClient.LOGIN_NOTLOGGEDIN:
            charNames = c.loadCharacterNames(c.getWorld())
            allowLogin = !World.isCharacterListConnected(charNames)
            if !allowLogin:
                allowLoginTip = World.getAllowLoginTip(charNames)
        if !allowLogin:
            msg = "检测账号下已有角色登陆游戏 服务端断开这个连接 [角色ID: " + player.getId() + " 名字: " + player.getName() + " ]\r\n" + allowLoginTip
            print("自动断开连接2")
            c.setPlayer(None)
            c.getSession().close(True)
            print(msg)
            return
        c.updateLoginState(MapleClient.LOGIN_LOGGEDIN, c.getSessionIPAddress())
        channelServer.addPlayer(player)
        c.getSession().write(MaplePacketCreator.getCharInfo(player))
        if player.isGM():
            SkillFactory.getSkill(9001004).getEffect(1).applyTo(player)
        c.getSession().write(MaplePacketCreator.temporaryStats_Reset())
        player.getMap().addPlayer(player)
        try:
            player.silentGiveBuffs(PlayerBuffStorage.getBuffsFromStorage(player.getId()))
            player.giveCoolDowns(PlayerBuffStorage.getCooldownsFromStorage(player.getId()))
            player.giveSilentDebuff(PlayerBuffStorage.getDiseaseFromStorage(player.getId()))
            buddyIds = player.getBuddylist().getBuddiesIds()
            World.Buddy.loggedOn(player.getName(), player.getId(), c.getChannel(), buddyIds, player.getGMLevel(), player.isHidden())
            if player.getParty() is not None:
                World.Party.updateParty(player.getParty().getId(), PartyOperation.LOG_ONOFF, MaplePartyCharacter(player))
            multiBuddyFind = None
            onlineBuddies = multiBuddyFind = World.Find.multiBuddyFind(player.getId(), buddyIds)
            for onlineBuddy in multiBuddyFind:
                ble = player.getBuddylist().get(onlineBuddy.getCharacterId())
                ble.setChannel(onlineBuddy.getChannel())
                player.getBuddylist().put(ble)
            c.sendPacket(MaplePacketCreator.updateBuddylist(player.getBuddylist().getBuddies()))
            messenger = player.getMessenger()
            if messenger is not None:
                World.Messenger.silentJoinMessenger(messenger.getId(), MapleMessengerCharacter(c.getPlayer()))
                World.Messenger.updateMessenger(messenger.getId(), c.getPlayer().getName(), c.getChannel())
            if player.getGuildId() > 0:
                World.Guild.setGuildMemberOnline(player.getMGC(), True, c.getChannel())
                c.getSession().write(MaplePacketCreator.showGuildInfo(player))
                gs = World.Guild.getGuild(player.getGuildId())
                if gs is not None:
                    packetList = World.Alliance.getAllianceInfo(gs.getAllianceId(), True)
                    if packetList is not None:
                        for pack in packetList:
                            if pack is not None:
                                c.getSession().write(pack)
            if player.getFamilyId() > 0:
                World.Family.setFamilyMemberOnline(player.getMFC(), True, c.getChannel())
            c.getSession().write(FamilyPacket.getFamilyInfo(player))
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.Login_Error, e)
        c.getSession().write(FamilyPacket.getFamilyData())
        for status in player.getStartedQuests():
            if status.hasMobKills():
                c.getSession().write(MaplePacketCreator.updateQuestMobKills(status))
        pendingBuddyRequest = player.getBuddylist().pollPendingRequest()
        if pendingBuddyRequest is not None:
            player.getBuddylist().put(BuddyEntry(pendingBuddyRequest.getName(), pendingBuddyRequest.getCharacterId(), "ETC", -1, False, pendingBuddyRequest.getLevel(), pendingBuddyRequest.getJob()))
            c.sendPacket(MaplePacketCreator.requestBuddylistAdd(pendingBuddyRequest.getCharacterId(), pendingBuddyRequest.getName(), pendingBuddyRequest.getLevel(), pendingBuddyRequest.getJob()))
        player.expirationTask()
        if player.getJob() == 132:
            player.checkBerserk()
        player.sendMacros()
        c.getSession().write(MaplePacketCreator.showCharCash(c.getPlayer()))
        player.getClient().getSession().write(MaplePacketCreator.serverMessage(channelServer.getServerMessage()))
        player.showNote()
        player.updatePartyMemberHP()
        player.startFairySchedule(False)
        player.updatePetEquip()
        player.baseSkills()
        player.spawnSavedPets()
        c.getSession().write(MaplePacketCreator.getKeymap(player.getKeyLayout()))
        c.getSession().write(MaplePacketCreator.weirdStatUpdate())
        if firstLoggedIn:
            if player.getGMLevel() == 0:
                if player.getGender() == 0:
                    World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, c.getChannel(), "[登录公告] 【帅哥】" + c.getPlayer().getName() + " : " + "".append("进入游戏，大家热烈欢迎他吧！！！")).encode("utf-8"))
                else:
                    World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(11, c.getChannel(), "[登录公告] 【美女】" + c.getPlayer().getName() + " : " + "".append("进入游戏，大家热烈欢迎她吧！！！")).encode("utf-8"))
            else:
                p = 0
                for cserv in ChannelServer.getAllInstances():
                    for chr in cserv.getPlayerStorage().getAllCharacters():
                        if chr is not None:
                            p += 1
                player.dropMessage(6, "[服务器信息]：尊敬的管理员，欢迎进入游戏。当前在线人数：" + p + "人")
        if player.haveItem(2022336):
            player.dropMessage(5, "欢迎来到" + ServerProperties.getProperty("RoyMS.ServerName") + ",请按“I”键，打开背包，双击使用神秘箱子，领取新人礼包")
        if player.getLevel() == 1:
            player.dropMessage(1, "欢迎来到 " + c.getChannelServer().getServerName() + ", " + player.getName() + " ！\r\n使用 @help 可以查看您当前能使用的命令\r\n祝您玩的愉快！")
            player.dropMessage(5, "使用 @help 可以查看您当前能使用的命令 祝您玩的愉快！")
        if c.getPlayer().hasEquipped(1122017):
            player.dropMessage(5, "您装备了精灵吊坠！打猎时可以额外获得10%的道具佩戴经验奖励！在线1小时后，经验增加10%，最高可获得30%")
        if c.getChannelServer().getDoubleExp() > 1:
            player.dropMessage(6, "[系统提示] 当前服务器处于双倍经验活动中，祝您玩的愉快！目前倍率：" + c.getChannelServer().getDoubleExp() + " 倍")
        阴森世界地图 = 551030200
        if c.getPlayer().getHp() != 50 && (c.getPlayer().getBossLog("狮熊Boss") >= 1 || c.getPlayer().getBossLogChannel("狮熊Boss") > 0) && c.getPlayer().getMap().getId() != 阴森世界地图 && c.getPlayer().获取怪物数量(阴森世界地图) >= 1 && c.getPlayer().getBossLogChannel("狮熊Boss") == c.getChannel():
            c.getPlayer().changeMap(阴森世界地图)
        else:
            c.getPlayer().resetBossLog("狮熊Boss")
        树精地图 = 541020800
        if c.getPlayer().getHp() != 50 && (c.getPlayer().getBossLog("树精Boss") >= 1 || c.getPlayer().getBossLogChannel("树精Boss") > 0) && c.getPlayer().getMap().getId() != 树精地图 && c.getPlayer().获取怪物数量(树精地图) >= 0 && c.getPlayer().getBossLogChannel("树精Boss") == c.getChannel():
            c.getPlayer().changeMap(树精地图)
        else:
            c.getPlayer().resetBossLog("树精Boss")
        普通黑龙地图阶段1 = 240060000
        普通黑龙地图阶段2 = 240060100
        普通黑龙地图阶段3 = 240060200
        if c.getPlayer().getHp() != 50 && (c.getPlayer().getBossLog("普通黑龙") >= 1 || c.getPlayer().getBossLogChannel("普通黑龙") > 0):
            type = c.getPlayer().getBossLogType("普通黑龙")
            mapID = 0
            # switch (type):
                # case 1:
                    mapID = 普通黑龙地图阶段1
                    break
                # case 2:
                    mapID = 普通黑龙地图阶段2
                    break
                # case 3:
                    mapID = 普通黑龙地图阶段3
                    break
            if c.getPlayer().getMap().getId() != mapID && c.getPlayer().getBossLogChannel("普通黑龙") == c.getChannel():
                preheadCheck = 4
                if type == 1:
                    if c.getPlayer().获取怪物数量(mapID) >= 1:
                        preheadCheck = 2
                    else:
                        preheadCheck = 0
                if type == 2:
                    if c.getPlayer().获取怪物数量(mapID) >= 1:
                        preheadCheck = 4
                    else:
                        preheadCheck = 2
                em = c.getChannelServer().getEventSM().getEventManager("HorntailBattle")
                eim = em.getInstance("HorntailBattle")
                if eim is None:
                    eim = em.newInstance("HorntailBattle")
                    eim.startEventTimer(43200000)
                    eim.schedule("CheckHorntailHead", 3000)
                em.setProperty("state", "" + type)
                em.setProperty("preheadCheck", "" + preheadCheck)
                c.getPlayer().changeMap(mapID)
            else:
                c.getPlayer().resetBossLog("普通黑龙")
        else:
            c.getPlayer().resetBossLog("普通黑龙")
        扎昆祭台地图 = 280030000
        if c.getPlayer().getHp() != 50 && (c.getPlayer().getBossLog("普通扎昆") >= 1 || c.getPlayer().getBossLogChannel("普通扎昆") > 0) && c.getPlayer().getMap().getId() != 扎昆祭台地图 && c.getPlayer().获取怪物数量(扎昆祭台地图) >= 1 && c.getPlayer().getBossLogChannel("普通扎昆") == c.getChannel():
            c.getPlayer().changeMap(扎昆祭台地图)
        else:
            c.getPlayer().resetBossLog("普通扎昆")
        player.checkCopyItems()
        print("login: "+DateUtil.getCurrentDateStr()+"[服务端-用户:][名字:" + c.getPlayer().getName() + "][  等级:" + c.getPlayer().getLevel() + "] 进入游戏.")

    def ChangeChannel(self, slea: Any, c: Any, chr: Any) -> None:
        if c.getPlayer().getTrade() is not None || !chr.isAlive() || chr.getEventInstance() is not None || chr.getMap() is None || FieldLimitType.ChannelSwitch.check(chr.getMap().getFieldLimit()):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        chr.changeChannel(slea.readByte() + 1)

