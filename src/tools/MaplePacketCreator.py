"""
MaplePacketCreator - Converted from Java source
Original: tools/MaplePacketCreator.java
Package: tools
"""

from io import TextIOWrapper
from io import open
from pathlib import Path
from pymysql import Error
from pymysql.cursors import Cursor
from socket import socket
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import math
import os
import pymysql
import threading
import time

# Internal module imports
# from client.BuddyEntry import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.MapleKeyLayout import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.SkillMacro import *  # TODO: import specific classes
# from client.inventory.IEquip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MapleMount import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from client.inventory.ModifyInventory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.ByteArrayMaplePacket import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from handling.channel.MapleGuildRanking import *  # TODO: import specific classes
# from handling.channel.handler.InventoryHandler import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PartyOperation import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleBBSThread import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildAlliance import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildCharacter import *  # TODO: import specific classes
# from server.MapleDueyActions import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleShopItem import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.MapleTrade import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.events.MapleSnowball import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from server.life.PlayerNPC import *  # TODO: import specific classes
# from server.life.SummonAttackEntry import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapItem import *  # TODO: import specific classes
# from server.maps.MapleMist import *  # TODO: import specific classes
# from server.maps.MapleNodes import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.maps.MapleSummon import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from server.shops.HiredMerchant import *  # TODO: import specific classes
# from server.shops.MaplePlayerShopItem import *  # TODO: import specific classes
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes
# from tools.packet.PacketHelper import *  # TODO: import specific classes


class MaplePacketCreator:
    """
    Class MaplePacketCreator
    """

    showPacket = False

    # Static initializer
    # MaplePacketCreator.EMPTY_STATUPDATE = Collections.emptyList()
    # CHAR_INFO_MAGIC = new byte[] { -1, -55, -102, 59 }


    @staticmethod
    def getServerIP(port: int, clientId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getServerIP--------------------")
        mplew.writeShort(SendPacketOpcode.SERVER_IP.getValue())
        mplew.writeShort(0)
        try:
            mplew.write(InetAddress.getByName(ServerProperties.getProperty("RoyMS.IP")).getAddress())
        except UnknownHostException as e:
            print("登录服务器IP：" + e)
        mplew.writeShort(port)
        mplew.writeInt(clientId)
        mplew.write(new byte[] { 1, 0, 0, 0, 0 })
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getChannelChange(self, inetAddr: Any, port: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getChannelChange--------------------")
        mplew.writeShort(SendPacketOpcode.CHANGE_CHANNEL.getValue())
        mplew.write(1)
        try:
            mplew.write(InetAddress.getByName(ServerProperties.getProperty("RoyMS.IP")).getAddress())
        except UnknownHostException as ex:
            pass
        mplew.writeShort(port)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getCharInfo(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getCharInfo--------------------")
        mplew.writeShort(SendPacketOpcode.WARP_TO_MAP.getValue())
        mplew.writeInt(chr.getClient().getChannel() - 1)
        mplew.write(0)
        mplew.write(1)
        mplew.write(1)
        mplew.writeShort(0)
        chr.CRand().connectData(mplew)
        PacketHelper.addCharacterInfo(mplew, chr)
        mplew.writeLong(PacketHelper.getTime(int(time.time() * 1000)))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def enableActions(self) -> Any:
        if ServerConstants.调试输出封包:
            print("enableActions--------------------")
        return updatePlayerStats(MaplePacketCreator.EMPTY_STATUPDATE, True, 0)

    def updatePlayerStats(self, stats: list, evan: int) -> Any:
        if ServerConstants.调试输出封包:
            print("updatePlayerStatsA--------------------")
        return updatePlayerStats(stats, False, evan)

    def updatePlayerStats_stats_itemReaction_evan(self, stats: list, itemReaction: bool, evan: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updatePlayerStats--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(itemReaction ? 1 : 0)
        updateMask = 0
        for statupdate in stats:
            updateMask |= statupdate.getLeft().getValue()
        mystats = stats
        if mystats > 1:
            Collections.sort(mystats, new Comparator<Pair<MapleStat, Integer>>()
                public int compare(final Pair<MapleStat, Integer> o1, final Pair<MapleStat, Integer> o2)
                    val1 = o1.getLeft().getValue()
                    val2 = o2.getLeft().getValue()
                    return (val1 < val2) ? -1 : ((val1 == val2) ? 0 : 1)
        mplew.writeInt(updateMask)
        for statupdate2 in mystats:
            if statupdate2.getLeft().getValue() >= 1:
                if statupdate2.getLeft().getValue() == 1:
                    mplew.writeShort(statupdate2.getRight().shortValue())
                elif statupdate2.getLeft().getValue() <= 4:
                    mplew.writeInt(statupdate2.getRight())
                elif statupdate2.getLeft().getValue() < 128:
                    mplew.write(statupdate2.getRight().shortValue())
                elif statupdate2.getLeft().getValue() < 262144:
                    mplew.writeShort(statupdate2.getRight().shortValue())
                else:
                    mplew.writeInt(statupdate2.getRight())
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def compare(self, o1: Any, o2: Any) -> int:
        val1 = o1.getLeft().getValue()
        val2 = o2.getLeft().getValue()
        return (val1 < val2) ? -1 : ((val1 == val2) ? 0 : 1)

    def blockedPortal(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("blockedPortal--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(1)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def weirdStatUpdate(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("weirdStatUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(0)
        mplew.write(56)
        mplew.writeShort(0)
        mplew.writeLong(0)
        mplew.writeLong(0)
        mplew.writeLong(0)
        mplew.write(0)
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateSp(self, chr: Any, itemReaction: bool) -> Any:
        if ServerConstants.调试输出封包:
            print("updateSpA--------------------")
        return updateSp(chr, itemReaction, False)

    def updateSp_chr_itemReaction_overrideJob(self, chr: Any, itemReaction: bool, overrideJob: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateSp--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(itemReaction ? 1 : 0)
        mplew.writeInt(131072)
        mplew.writeShort(chr.getRemainingSp())
        mplew.writeShort(0)
        return mplew.getPacket()

    def getWarpToMap(self, to: Any, spawnPoint: int, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getWarpToMap--------------------")
        mplew.writeShort(SendPacketOpcode.WARP_TO_MAP.getValue())
        mplew.writeInt(chr.getClient().getChannel() - 1)
        mplew.write(0)
        mplew.write(3)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(to.getId())
        mplew.write(spawnPoint)
        mplew.writeShort(chr.getStat().getHp())
        mplew.writeLong(PacketHelper.getTime(int(time.time() * 1000)))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnPortal(self, townId: int, targetId: int, skillId: int, pos: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnPortal--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_PORTAL.getValue())
        mplew.writeInt(townId)
        mplew.writeInt(targetId)
        if pos is not None:
            mplew.writePos(pos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnDoor(self, oid: int, pos: Any, town: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnDoor--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_DOOR.getValue())
        mplew.write(town ? 1 : 0)
        mplew.writeInt(oid)
        mplew.writePos(pos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeDoor(self, oid: int, town: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeDoor--------------------")
        if town:
            mplew.writeShort(SendPacketOpcode.SPAWN_PORTAL.getValue())
            mplew.writeInt(999999999)
            mplew.writeInt(999999999)
        else:
            mplew.writeShort(SendPacketOpcode.REMOVE_DOOR.getValue())
            mplew.write(0)
            mplew.writeInt(oid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnSummon(self, summon: Any, animated: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnSummon--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_SUMMON.getValue())
        mplew.writeInt(summon.getOwnerId())
        mplew.writeInt(summon.getObjectId())
        mplew.writeInt(summon.getSkill())
        mplew.write(summon.getOwnerLevel())
        mplew.write(summon.getSkillLevel())
        mplew.writeShort(summon.getPosition().x)
        mplew.writeInt(summon.getPosition().y)
        mplew.write(0)
        mplew.write(summon.getMovementType().getValue())
        mplew.write(summon.getSummonType())
        mplew.write(animated ? 0 : 1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeSummon(self, summon: Any, animated: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeSummon--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_SUMMON.getValue())
        mplew.writeInt(summon.getOwnerId())
        mplew.writeInt(summon.getObjectId())
        mplew.write(animated ? 4 : 1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def serverMessage(self, message: str) -> Any:
        if ServerConstants.调试输出封包:
            print("serverMessageA--------------------")
        return serverMessage(4, 0, message, False)

    def serverNotice(self, type: int, message: str) -> Any:
        if ServerConstants.调试输出封包:
            print("serverNoticeA--------------------")
        return serverMessage(type, 0, message, False)

    def serverNotice_type_channel_message(self, type: int, channel: int, message: str) -> Any:
        if ServerConstants.调试输出封包:
            print("serverNoticeB--------------------")
        return serverMessage(type, channel, message, False)

    def serverNotice_type_channel_message_smegaEar(self, type: int, channel: int, message: str, smegaEar: bool) -> Any:
        if ServerConstants.调试输出封包:
            print("serverNoticeC--------------------")
        return serverMessage(type, channel, message, smegaEar)

    def serverMessage_type_channel_message_megaEar(self, type: int, channel: int, message: str, megaEar: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("serverMessage--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERMESSAGE.getValue())
        mplew.write(type)
        if type == 4:
            mplew.write(1)
        mplew.writeMapleAsciiString(message)
        # switch (type):
            # case 3:
            # case 9:
            # case 10:
            # case 11:
            # case 12:
                mplew.write(channel - 1)
                mplew.write(megaEar ? 1 : 0)
                break
            # case 6:
            # case 18:
                mplew.writeInt((channel >= 1000000 and channel < 6000000) ? channel : 0)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGachaponMega(self, name: str, message: str, item: Any, rareness: int, channel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getGachaponMega--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERMESSAGE.getValue())
        mplew.write(14)
        mplew.writeMapleAsciiString(name + message)
        mplew.writeInt(channel - 1)
        PacketHelper.addItemInfo(mplew, item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def tripleSmega(self, message: list, ear: bool, channel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("tripleSmega--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERMESSAGE.getValue())
        mplew.write(10)
        if message.get(0) is not None:
            mplew.writeMapleAsciiString(message.get(0))
        mplew.write(message)
        for i in range(1, message):
            if message.get(i) is not None:
                mplew.writeMapleAsciiString(message.get(i))
        mplew.write(channel - 1)
        mplew.write(ear ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getAvatarMega(self, chr: Any, channel: int, itemId: int, message: str, ear: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getAvatarMega--------------------")
        mplew.writeShort(SendPacketOpcode.AVATAR_MEGA.getValue())
        mplew.writeInt(itemId)
        mplew.writeMapleAsciiString(chr.getName())
        mplew.writeMapleAsciiString(message)
        mplew.writeInt(channel - 1)
        mplew.write(ear ? 1 : 0)
        PacketHelper.addCharLook(mplew, chr, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def itemMegaphone(self, msg: str, whisper: bool, channel: int, item: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("itemMegaphone--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERMESSAGE.getValue())
        mplew.write(8)
        mplew.writeMapleAsciiString(msg)
        mplew.write(channel - 1)
        mplew.write(whisper ? 1 : 0)
        if item is None:
            mplew.write(0)
        else:
            PacketHelper.addItemInfo(mplew, item, False, False, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnNPC(self, life: Any, show: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnNPC--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_NPC.getValue())
        mplew.writeInt(life.getObjectId())
        mplew.writeInt(life.getId())
        mplew.writeShort(life.getPosition().x)
        mplew.writeShort(life.getCy())
        mplew.write((life.getF() != 1) ? 1 : 0)
        mplew.writeShort(life.getFh())
        mplew.writeShort(life.getRx0())
        mplew.writeShort(life.getRx1())
        mplew.write(show ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeNPCController(self, objectid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.SPAWN_NPC_REQUEST_CONTROLLER.getValue())
        mplew.write(0)
        mplew.writeInt(objectid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeNPC(self, objectid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeNPC--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_NPC.getValue())
        mplew.writeLong(objectid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnNPCRequestController(self, life: Any, MiniMap: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnNPCRequestController--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_NPC_REQUEST_CONTROLLER.getValue())
        mplew.write(1)
        mplew.writeInt(life.getObjectId())
        mplew.writeInt(life.getId())
        mplew.writeShort(life.getPosition().x)
        mplew.writeShort(life.getCy())
        mplew.write((life.getF() != 1) ? 1 : 0)
        mplew.writeShort(life.getFh())
        mplew.writeShort(life.getRx0())
        mplew.writeShort(life.getRx1())
        mplew.write(MiniMap ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnPlayerNPC(self, npc: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnPlayerNPC--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_NPC.getValue())
        mplew.write((npc.getF() != 1) ? 1 : 0)
        mplew.writeInt(npc.getId())
        mplew.writeMapleAsciiString(npc.getName())
        mplew.write(npc.getGender())
        mplew.write(npc.getSkin())
        mplew.writeInt(npc.getFace())
        mplew.write(0)
        mplew.writeInt(npc.getHair())
        equip = npc.getEquips()
        myEquip = {}
        maskedEquip = {}
        for (final Map.Entry<Byte, Integer> position : equip.items())
            pos = (byte)(position.getKey() * -1)
            if pos < 100 and myEquip.get(pos) is None:
                myEquip.put(pos, position.getValue())
            elif (pos > 100 or pos == -128) and pos != 111:
                pos = (byte)((pos == -128) ? 28 : (pos - 100))
                if myEquip.get(pos) is not None:
                    maskedEquip.put(pos, myEquip.get(pos))
                myEquip.put(pos, position.getValue())
            else:
                if myEquip.get(pos) is None:
                    continue
                maskedEquip.put(pos, position.getValue())
        for (final Map.Entry<Byte, Integer> entry : myEquip.items())
            mplew.write(entry.getKey())
            mplew.writeInt(entry.getValue())
        mplew.write(255)
        for (final Map.Entry<Byte, Integer> entry : maskedEquip.items())
            mplew.write(entry.getKey())
            mplew.writeInt(entry.getValue())
        mplew.write(255)
        cWeapon = equip.get(-111)
        if cWeapon is not None:
            mplew.writeInt(cWeapon)
        else:
            mplew.writeInt(0)
        for i in range(3):
            mplew.writeInt(npc.getPet(i))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getChatText(self, cidfrom: int, text: str, whiteBG: bool, show: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getChatText--------------------")
        mplew.writeShort(SendPacketOpcode.CHATTEXT.getValue())
        mplew.writeInt(cidfrom)
        mplew.write(whiteBG ? 1 : 0)
        mplew.writeMapleAsciiString(text)
        mplew.write(show)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def GameMaster_Func(self, value: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("GameMaster_Func--------------------")
        mplew.writeShort(SendPacketOpcode.GM_EFFECT.getValue())
        mplew.write(value)
        mplew.writeZeroBytes(17)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPacketFromHexString(self, hex: str) -> Any:
        if ServerConstants.调试输出封包:
            print("getPacketFromHexString--------------------")
        return ByteArrayMaplePacket(HexTool.getByteArrayFromHexString(hex))

    def GainEXP_Monster(self, gain: int, white: bool, 结婚奖励经验值: int, 组队经验值: int, Class_Bonus_EXP: int, 道具佩戴附加经验值: int, 网吧特别经验: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("GainEXP_Monster--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(3)
        mplew.write(white ? 1 : 0)
        mplew.writeInt(gain)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.writeInt(结婚奖励经验值)
        mplew.write(0)
        mplew.writeInt(组队经验值)
        mplew.writeInt(道具佩戴附加经验值)
        mplew.writeInt(网吧特别经验)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def GainEXP_Others(self, gain: int, inChat: bool, white: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("GainEXP_Others--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(3)
        mplew.write(white ? 1 : 0)
        mplew.writeInt(gain)
        mplew.write(0)
        mplew.writeInt(inChat ? 1 : 0)
        mplew.writeShort(0)
        mplew.writeZeroBytes(4)
        if inChat:
            mplew.writeZeroBytes(13)
        else:
            mplew.writeZeroBytes(13)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getShowFameGain(self, gain: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getShowFameGain--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(4)
        mplew.writeInt(gain)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMesoGain(self, gain: int, inChat: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showMesoGain--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        if not inChat:
            mplew.write(0)
            mplew.write(1)
            mplew.write(0)
        else:
            mplew.write(5)
        mplew.writeInt(gain)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getShowItemGain(self, itemId: int, quantity: int) -> Any:
        if ServerConstants.调试输出封包:
            print("getShowItemGainA--------------------")
        return getShowItemGain(itemId, quantity, False)

    def getShowItemGain_itemId_quantity_inChat(self, itemId: int, quantity: int, inChat: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getShowItemGain--------------------")
        if inChat:
            mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
            mplew.write(3)
            mplew.write(1)
            mplew.writeInt(itemId)
            mplew.writeInt(quantity)
        else:
            mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
            mplew.writeShort(0)
            mplew.writeInt(itemId)
            mplew.writeInt(quantity)
            mplew.writeInt(0)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showRewardItemAnimation(self, itemId: int, effect: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showRewardItemAnimationA--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(11)
        mplew.writeInt(itemId)
        mplew.write((effect is not None and effect > 0) ? 1 : 0)
        if effect is not None and effect > 0:
            mplew.writeMapleAsciiString(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showRewardItemAnimation_itemId_effect_from_playerid(self, itemId: int, effect: str, from_playerid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showRewardItemAnimationB--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(from_playerid)
        mplew.write(11)
        mplew.writeInt(itemId)
        mplew.write((effect is not None and effect > 0) ? 1 : 0)
        if effect is not None and effect > 0:
            mplew.writeMapleAsciiString(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def dropItemFromMapObject(self, drop: Any, dropfrom: Any, dropto: Any, mod: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("dropItemFromMapObject--------------------")
        mplew.writeShort(SendPacketOpcode.DROP_ITEM_FROM_MAPOBJECT.getValue())
        mplew.write(mod)
        mplew.writeInt(drop.getObjectId())
        mplew.write((drop.getMeso() > 0) ? 1 : 0)
        mplew.writeInt(drop.getItemId())
        mplew.writeInt(drop.getOwner())
        mplew.write(drop.getDropType())
        mplew.writePos(dropto)
        mplew.writeInt(0)
        if mod != 2:
            mplew.writePos(dropfrom)
        mplew.write(0)
        if mod != 2:
            mplew.write(0)
            mplew.write(1)
        if drop.getMeso() == 0:
            PacketHelper.addExpirationTime(mplew, drop.getItem().getExpiration())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnPlayerMapobject(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnPlayerMapobject--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_PLAYER.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(chr.getLevel())
        mplew.writeMapleAsciiString(chr.getName())
        if chr.isAriantPQMap():
            mplew.writeMapleAsciiString("1st")
            mplew.write(new byte[6])
        elif chr.getGuildId() <= 0:
            mplew.writeMapleAsciiString("")
            mplew.write(new byte[6])
        else:
            gs = World.Guild.getGuild(chr.getGuildId())
            if gs is not None:
                mplew.writeMapleAsciiString(gs.getName())
                mplew.writeShort(gs.getLogoBG())
                mplew.write(gs.getLogoBGColor())
                mplew.writeShort(gs.getLogo())
                mplew.write(gs.getLogoColor())
            else:
                mplew.writeMapleAsciiString("")
                mplew.write(new byte[6])
        mplew.writeInt(0)
        mplew.write(0)
        mplew.write(224)
        mplew.write(31)
        mplew.write(0)
        if chr.getBuffedValue(MapleBuffStat.变身) is not None:
            mplew.writeInt(2)
        else:
            mplew.writeInt(0)
        buffmask = 0
        buffvalue = None
        if chr.getBuffedValue(MapleBuffStat.隐身术) is not None and not chr.isHidden():
            buffmask |= MapleBuffStat.隐身术.getValue()
        if chr.getBuffedValue(MapleBuffStat.斗气集中) is not None:
            buffmask |= MapleBuffStat.斗气集中.getValue()
            buffvalue = chr.getBuffedValue(MapleBuffStat.斗气集中)
        if chr.getBuffedValue(MapleBuffStat.影分身) is not None:
            buffmask |= MapleBuffStat.影分身.getValue()
        if chr.getBuffedValue(MapleBuffStat.无形箭弩) is not None:
            buffmask |= MapleBuffStat.无形箭弩.getValue()
        if chr.getBuffedValue(MapleBuffStat.变身) is not None:
            buffvalue = chr.getBuffedValue(MapleBuffStat.变身)
        mplew.writeInt((int)(buffmask >> 32 & -1))
        if buffvalue is not None:
            if chr.getBuffedValue(MapleBuffStat.变身) is not None:
                mplew.writeShort(buffvalue)
            else:
                mplew.write(buffvalue.byteValue())
        CHAR_MAGIC_SPAWN = Randomizer.nextInt()
        mplew.writeInt((int)(buffmask & -1))
        mplew.write(new byte[6])
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.writeShort(0)
        mplew.write(0)
        mount = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18))
        if chr.getBuffedValue(MapleBuffStat.骑兽技能) is not None and mount is not None:
            mplew.writeInt(mount.getItemId())
            mplew.writeInt(1004)
            mplew.writeInt(19275520)
            mplew.write(0)
        else:
            mplew.writeInt(CHAR_MAGIC_SPAWN)
            mplew.writeLong(0)
            mplew.write(0)
        mplew.writeLong(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.write(0)
        mplew.write(1)
        mplew.write(65)
        mplew.write(154)
        mplew.write(112)
        mplew.write(7)
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.writeLong(0)
        mplew.writeInt(0)
        mplew.write(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(CHAR_MAGIC_SPAWN)
        mplew.write(0)
        mplew.writeShort(chr.getJob())
        PacketHelper.addCharLook(mplew, chr, False)
        mplew.writeInt(min(250, chr.getInventory(MapleInventoryType.CASH).countById(5110000)))
        mplew.writeInt(chr.getItemEffect())
        mplew.writeInt(0)
        mplew.writeInt(-1)
        mplew.writeInt((GameConstants.getInventoryType(chr.getChair()) == MapleInventoryType.SETUP) ? chr.getChair() : 0)
        mplew.writePos(chr.getPosition())
        mplew.write(chr.getStance())
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(chr.getMount().getLevel())
        mplew.writeInt(chr.getMount().getExp())
        mplew.writeInt(chr.getMount().getFatigue())
        PacketHelper.addAnnounceBox(mplew, chr)
        mplew.write((chr.getChalkboard() is not None and chr.getChalkboard() > 0) ? 1 : 0)
        if chr.getChalkboard() is not None and chr.getChalkboard() > 0:
            mplew.writeMapleAsciiString(chr.getChalkboard())
        rings = chr.getRings(False)
        allrings = rings.getLeft()
        allrings.addAll(rings.getRight())
        addRingInfo(mplew, allrings)
        addRingInfo(mplew, allrings)
        addMarriageRingLook(mplew, chr)
        mplew.writeShort(0)
        if chr.getCarnivalParty() is not None:
            mplew.write(chr.getCoconutTeam())
        elif chr.getMapId() == 109080000 or chr.getMapId() == 109080010:
            mplew.write(chr.getCoconutTeam())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removePlayerFromMap(self, cid: int, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removePlayerFromMap--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_PLAYER_FROM_MAP.getValue())
        mplew.writeInt(cid)
        ERROR = ServerConstants()
        if (ServerConstants.PACKET_ERROR_OFF and ERROR.getChannel() != 1) or ERROR.getRemovePlayerFromMap() != 1:
            note = "时间：" + FileoutputUtil.CurrentReadable_Time() + " or 玩家名字：" + chr.getName() + " or 玩家地图：" + chr.getMapId() + "\r\n38错误：" + ERROR.getPACKET_ERROR() + "\r\n\r\n"
            FileoutputUtil.packetLog("logs/38掉线/" + chr.getName() + ".log", note)
        return mplew.getPacket()

    def facialExpression(self, from: Any, expression: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("facialExpression--------------------")
        mplew.writeShort(SendPacketOpcode.FACIAL_EXPRESSION.getValue())
        mplew.writeInt(from.getId())
        mplew.writeInt(expression)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def movePlayer(self, cid: int, moves: list, startPos: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.MOVE_PLAYER.getValue())
        mplew.writeInt(cid)
        mplew.writePos(startPos)
        PacketHelper.serializeMovementList(mplew, moves)
        return mplew.getPacket()

    def moveSummon(self, cid: int, oid: int, startPos: Any, moves: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveSummon--------------------")
        mplew.writeShort(SendPacketOpcode.MOVE_SUMMON.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(oid)
        mplew.writeShort(startPos.x)
        mplew.writeShort(startPos.y)
        PacketHelper.serializeMovementList(mplew, moves)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def summonAttack(self, cid: int, summonSkillId: int, newStance: int, allDamage: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("summonAttack--------------------")
        mplew.writeShort(SendPacketOpcode.SUMMON_ATTACK.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(summonSkillId)
        mplew.write(newStance)
        mplew.write(allDamage)
        for attackEntry in allDamage:
            mplew.writeInt(attackEntry.getMonster().getObjectId())
            mplew.write(1)
            mplew.write(6)
            mplew.writeInt(attackEntry.getDamage())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR("summonAttack-2158：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def closeRangeAttack(self, cid: int, tbyte: int, skill: int, level: int, display: int, animation: int, speed: int, damage: list, energy: bool, lvl: int, mastery: int, unk: int, charge: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("closeRangeAttack--------------------")
        mplew.writeShort(energy ? SendPacketOpcode.ENERGY_ATTACK.getValue() : SendPacketOpcode.CLOSE_RANGE_ATTACK.getValue())
        mplew.writeInt(cid)
        mplew.write(tbyte)
        mplew.write(lvl)
        if skill > 0:
            mplew.write(level)
            mplew.writeInt(skill)
        else:
            mplew.write(0)
        mplew.write(unk)
        mplew.write(display)
        mplew.write(animation)
        mplew.write(speed)
        mplew.write(mastery)
        mplew.writeInt(0)
        if skill == 4211006:
            for oned in damage:
                if oned.attack is not None:
                    mplew.writeInt(oned.objectid)
                    mplew.write(7)
                    mplew.write(oned.attack)
                    for eachd in oned.attack:
                        mplew.writeInt(eachd.left)
        else:
            for oned in damage:
                if oned.attack is not None:
                    mplew.writeInt(oned.objectid)
                    mplew.write(7)
                    for eachd in oned.attack:
                        if eachd.right:
                            mplew.writeInt(eachd.left + Integer.MIN_VALUE)
                        else:
                            mplew.writeInt(eachd.left)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def rangedAttack(self, cid: int, tbyte: int, skill: int, level: int, display: int, animation: int, speed: int, itemid: int, damage: list, pos: Any, lvl: int, mastery: int, unk: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("rangedAttack--------------------")
        mplew.writeShort(SendPacketOpcode.RANGED_ATTACK.getValue())
        mplew.writeInt(cid)
        mplew.write(tbyte)
        mplew.write(lvl)
        if skill > 0:
            mplew.write(level)
            mplew.writeInt(skill)
        else:
            mplew.write(0)
        mplew.write(unk)
        mplew.write(display)
        mplew.write(animation)
        mplew.write(speed)
        mplew.write(mastery)
        mplew.writeInt(itemid)
        for oned in damage:
            if oned.attack is not None:
                mplew.writeInt(oned.objectid)
                mplew.write(7)
                for eachd in oned.attack:
                    if eachd.right:
                        mplew.writeInt(eachd.left + Integer.MIN_VALUE)
                    else:
                        mplew.writeInt(eachd.left)
        mplew.writePos(pos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def magicAttack(self, cid: int, tbyte: int, skill: int, level: int, display: int, animation: int, speed: int, damage: list, charge: int, lvl: int, unk: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("magicAttack--------------------")
        mplew.writeShort(SendPacketOpcode.MAGIC_ATTACK.getValue())
        mplew.writeInt(cid)
        mplew.write(tbyte)
        mplew.write(lvl)
        mplew.write(level)
        mplew.writeInt(skill)
        mplew.write(unk)
        mplew.write(display)
        mplew.write(animation)
        mplew.write(speed)
        mplew.write(0)
        mplew.writeInt(0)
        for oned in damage:
            if oned.attack is not None:
                mplew.writeInt(oned.objectid)
                mplew.write(-1)
                for eachd in oned.attack:
                    if eachd.right:
                        mplew.writeInt(eachd.left + Integer.MIN_VALUE)
                    else:
                        mplew.writeInt(eachd.left)
        if charge > 0:
            mplew.writeInt(charge)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getNPCShop(self, c: Any, sid: int, items: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        ii = MapleItemInformationProvider.getInstance()
        if ServerConstants.调试输出封包:
            print("getNPCShop--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_NPC_SHOP.getValue())
        mplew.writeInt(sid)
        mplew.writeShort(items)
        for item in items:
            mplew.writeInt(item.getItemId())
            mplew.writeInt(item.getPrice())
            if not GameConstants.is飞镖道具(item.getItemId()) and not GameConstants.is子弹道具(item.getItemId()):
                mplew.writeShort(1)
                mplew.writeShort(item.getBuyable())
            else:
                mplew.writeZeroBytes(6)
                mplew.writeShort(BitTools.doubleToShortBits(ii.getPrice(item.getItemId())))
                mplew.writeShort(ii.getSlotMax(c, item.getItemId()))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def confirmShopTransaction(self, code: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("confirmShopTransaction--------------------")
        mplew.writeShort(SendPacketOpcode.CONFIRM_SHOP_TRANSACTION.getValue())
        mplew.write(code)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addInventorySlot(self, type: Any, item: Any) -> Any:
        if ServerConstants.调试输出封包:
            print("addInventorySlotA--------------------")
        return addInventorySlot(type, item, False)

    def addInventorySlot_type_item_fromDrop(self, type: Any, item: Any, fromDrop: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addInventorySlot--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(fromDrop ? 1 : 0)
        mplew.writeShort(1)
        mplew.write(type.getType())
        mplew.write(item.getPosition())
        PacketHelper.addItemInfo(mplew, item, True, False)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def pet_updateInventorySlot(self, type: Any, item: Any, fromDrop: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateInventorySlot--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(fromDrop ? 1 : 0)
        mplew.write(1)
        mplew.write(1)
        mplew.write(type.getType())
        mplew.writeShort(item.getPosition())
        mplew.writeShort(item.getQuantity())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateInventorySlot(self, type: Any, item: Any, fromDrop: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateInventorySlot--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(fromDrop ? 1 : 0)
        mplew.write(1)
        mplew.write(1)
        mplew.write(type.getType())
        mplew.writeShort(item.getPosition())
        mplew.writeShort(item.getQuantity())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveInventoryItem(self, type: Any, src: int, dst: int) -> Any:
        if ServerConstants.调试输出封包:
            print("moveInventoryItemA--------------------")
        return moveInventoryItem(type, src, dst, (short)(-1))

    def loveEffect(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(72)
        mplew.writeZeroBytes(20)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveInventoryItem_type_src_dst_equipIndicator(self, type: Any, src: int, dst: int, equipIndicator: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveInventoryItemB--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("01 01 02"))
        mplew.write(type.getType())
        mplew.writeShort(src)
        mplew.writeShort(dst)
        if equipIndicator != -1:
            mplew.write(equipIndicator)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveAndMergeInventoryItem(self, type: Any, src: int, dst: int, total: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveAndMergeInventoryItem--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("01 02 03"))
        mplew.write(type.getType())
        mplew.writeShort(src)
        mplew.write(1)
        mplew.write(type.getType())
        mplew.writeShort(dst)
        mplew.writeShort(total)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveAndMergeWithRestInventoryItem(self, type: Any, src: int, dst: int, srcQ: int, dstQ: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveAndMergeWithRestInventoryItem--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("01 02 01"))
        mplew.write(type.getType())
        mplew.writeShort(src)
        mplew.writeShort(srcQ)
        mplew.write(HexTool.getByteArrayFromHexString("01"))
        mplew.write(type.getType())
        mplew.writeShort(dst)
        mplew.writeShort(dstQ)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def clearInventoryItem(self, type: Any, slot: int, fromDrop: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("clearInventoryItem--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(fromDrop ? 1 : 0)
        mplew.write(HexTool.getByteArrayFromHexString("01 03"))
        mplew.write(type.getType())
        mplew.writeShort(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateSpecialItemUse(self, item: Any, invType: int) -> Any:
        if ServerConstants.调试输出封包:
            print("updateSpecialItemUseA--------------------")
        return updateSpecialItemUse(item, invType, item.getPosition())

    def updateSpecialItemUse_item_invType_pos(self, item: Any, invType: int, pos: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateSpecialItemUseB--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(0)
        mplew.write(2)
        mplew.write(3)
        mplew.write(invType)
        mplew.writeShort(pos)
        mplew.write(0)
        mplew.write(invType)
        if item.getType() == 1:
            mplew.writeShort(pos)
        else:
            mplew.write(pos)
        PacketHelper.addItemInfo(mplew, item, True, True)
        if item.getPosition() < 0:
            mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateSpecialItemUse_(self, item: Any, invType: int) -> Any:
        if ServerConstants.调试输出封包:
            print("updateSpecialItemUse_A--------------------")
        return updateSpecialItemUse_(item, invType, item.getPosition())

    def updateSpecialItemUse__item_invType_pos(self, item: Any, invType: int, pos: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateSpecialItemUse_B--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(0)
        mplew.write(1)
        mplew.write(0)
        mplew.write(invType)
        if item.getType() == 1:
            mplew.writeShort(pos)
        else:
            mplew.write(pos)
        PacketHelper.addItemInfo(mplew, item, True, True)
        if item.getPosition() < 0:
            mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def scrolledItem(self, scroll: Any, item: Any, destroyed: bool, potential: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("scrolledItem--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(1)
        mplew.write(destroyed ? 2 : 3)
        mplew.write((scroll.getQuantity() > 0) ? 1 : 3)
        mplew.write(GameConstants.getInventoryType(scroll.getItemId()).getType())
        mplew.writeShort(scroll.getPosition())
        if scroll.getQuantity() > 0:
            mplew.writeShort(scroll.getQuantity())
        mplew.write(3)
        if not destroyed:
            mplew.write(MapleInventoryType.EQUIP.getType())
            mplew.writeShort(item.getPosition())
            mplew.write(0)
        mplew.write(MapleInventoryType.EQUIP.getType())
        mplew.writeShort(item.getPosition())
        if not destroyed:
            PacketHelper.addItemInfo(mplew, item, True, True)
        if not potential:
            mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getScrollEffect(self, chr: int, scrollSuccess: Any, legendarySpirit: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getScrollEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_SCROLL_EFFECT.getValue())
        mplew.writeInt(chr)
        # switch (scrollSuccess):
            # case SUCCESS:
                mplew.writeShort(1)
                mplew.writeShort(legendarySpirit ? 1 : 0)
                break
            # case FAIL:
                mplew.writeShort(0)
                mplew.writeShort(legendarySpirit ? 1 : 0)
                break
            # case CURSE:
                mplew.write(0)
                mplew.write(1)
                mplew.writeShort(legendarySpirit ? 1 : 0)
                break
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def ItemMaker_Success(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("ItemMaker_Success--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(17)
        mplew.writeZeroBytes(4)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def ItemMaker_Success_3rdParty(self, from_playerid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("ItemMaker_Success_3rdParty--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(from_playerid)
        mplew.write(17)
        mplew.writeZeroBytes(4)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def explodeDrop(self, oid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("explodeDrop--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_ITEM_FROM_MAP.getValue())
        mplew.write(4)
        mplew.writeInt(oid)
        mplew.writeShort(655)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeItemFromMap(self, oid: int, animation: int, cid: int) -> Any:
        if ServerConstants.调试输出封包:
            print("removeItemFromMapA--------------------")
        return removeItemFromMap(oid, animation, cid, 0)

    def removeItemFromMap_oid_animation_cid_slot(self, oid: int, animation: int, cid: int, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeItemFromMapB--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_ITEM_FROM_MAP.getValue())
        mplew.write(animation)
        mplew.writeInt(oid)
        if animation >= 2:
            mplew.writeInt(cid)
            if animation == 5:
                mplew.write(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateCharLook(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateCharLook--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_CHAR_LOOK.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(1)
        PacketHelper.addCharLook(mplew, chr, False)
        rings = chr.getRings(False)
        allrings = rings.getLeft()
        allrings.addAll(rings.getRight())
        addRingInfo(mplew, allrings)
        addRingInfo(mplew, allrings)
        addMarriageRingLook(mplew, chr)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addMarriageRingLook(self, mplew: Any, chr: Any) -> None:
        mplew.write((byte)((chr.getMarriageRing(False) is not None) ? 1 : 0))
        if chr.getMarriageRing(False) is not None:
            mplew.writeInt(chr.getId())
            mplew.writeInt(chr.getMarriageRing(False).getPartnerChrId())
            mplew.writeInt(chr.getMarriageRing(False).getRingId())

    def addRingInfo(self, mplew: Any, rings: list) -> None:
        if ServerConstants.调试输出封包:
            print("addRingInfo--------------------")
        mplew.write((rings > 0) ? 1 : 0)
        mplew.writeInt(rings)
        for ring in rings:
            mplew.writeLong(ring.getRingId())
            mplew.writeLong(ring.getPartnerRingId())
            mplew.writeInt(ring.getItemId())

    def dropInventoryItem(self, type: Any, src: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("dropInventoryItem--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("01 01 03"))
        mplew.write(type.getType())
        mplew.writeShort(src)
        if src < 0:
            mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def dropInventoryItemUpdate(self, type: Any, item: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("dropInventoryItemUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("01 01 01"))
        mplew.write(type.getType())
        mplew.writeShort(item.getPosition())
        mplew.writeShort(item.getQuantity())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def damagePlayer(self, skill: int, monsteridfrom: int, cid: int, damage: int, fake: int, direction: int, reflect: int, is_pg: bool, oid: int, pos_x: int, pos_y: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("damagePlayer--------------------")
        mplew.writeShort(SendPacketOpcode.DAMAGE_PLAYER.getValue())
        mplew.writeInt(cid)
        mplew.write(skill)
        mplew.writeInt(damage)
        mplew.writeInt(monsteridfrom)
        mplew.write(direction)
        if reflect > 0:
            mplew.write(reflect)
            mplew.write(is_pg ? 1 : 0)
            mplew.writeInt(oid)
            mplew.write(6)
            mplew.writeShort(pos_x)
            mplew.writeShort(pos_y)
            mplew.write(0)
        else:
            mplew.writeShort(0)
        mplew.writeInt(damage)
        if fake > 0:
            mplew.writeInt(fake)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateQuest(self, quest: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuest--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(1)
        mplew.writeShort(quest.getQuest().getId())
        mplew.write(quest.getStatus())
        # switch (quest.getStatus()):
            # case 0:
                mplew.writeZeroBytes(10)
                break
            # case 1:
                mplew.writeMapleAsciiString((quest.getCustomData() is not None) ? quest.getCustomData() : "")
                break
            # case 2:
                mplew.writeLong(PacketHelper.getTime(int(time.time() * 1000)))
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateInfoQuest(self, quest: int, data: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateInfoQuest--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(10)
        mplew.writeShort(quest)
        mplew.writeMapleAsciiString(data)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateQuestInfo(self, c: Any, quest: int, npc: int, progress: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuestInfo--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_QUEST_INFO.getValue())
        mplew.write(progress)
        mplew.writeShort(quest)
        mplew.writeInt(npc)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateQuestFinish(self, quest: int, npc: int, nextquest: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuestFinish--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_QUEST_INFO.getValue())
        mplew.write(8)
        mplew.writeShort(quest)
        mplew.writeInt(npc)
        mplew.writeInt(nextquest)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def charInfo(self, chr: Any, isSelf: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("charInfo--------------------")
        mplew.writeShort(SendPacketOpcode.CHAR_INFO.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(chr.getLevel())
        mplew.writeShort(chr.getJob())
        mplew.writeShort(chr.getFame())
        mplew.write((chr.getMarriageId() > 0) ? 1 : 0)
        guildName = "-"
        allianceName = "-"
        gs = World.Guild.getGuild(chr.getGuildId())
        if chr.getGuildId() > 0 and gs is not None:
            guildName = gs.getName()
            if gs.getAllianceId() > 0:
                allianceNameA = World.Alliance.getAlliance(gs.getAllianceId())
                if allianceNameA is not None:
                    allianceName = allianceNameA.getName()
        mplew.writeMapleAsciiString(guildName)
        mplew.writeMapleAsciiString(allianceName)
        inv = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-114))
        peteqid = (inv is not None) ? inv.getItemId() : 0
        inv2 = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-122))
        peteqid2 = (inv2 is not None) ? inv2.getItemId() : 0
        inv3 = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-124))
        peteqid3 = (inv3 is not None) ? inv3.getItemId() : 0
        for pet in chr.getPets():
            if pet.getSummoned():
                mplew.write(pet.getUniqueId())
                mplew.writeInt(pet.getPetItemId())
                mplew.writeMapleAsciiString(pet.getName())
                mplew.write(pet.getLevel())
                mplew.writeShort(pet.getCloseness())
                mplew.write(pet.getFullness())
                mplew.writeShort(pet.getFlags())
                mplew.writeInt(peteqid)
        mplew.write(0)
        if chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18)) is not None:
            itemid = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18)).getItemId()
            mount = chr.getMount()
            canwear = MapleItemInformationProvider.getInstance().getReqLevel(itemid) <= chr.getLevel()
            mplew.write(canwear ? 1 : 0)
            mplew.writeInt(mount.getLevel())
            mplew.writeInt(mount.getExp())
            mplew.writeInt(mount.getFatigue())
        else:
            mplew.write(0)
        mplew.write(0)
        chr.getMonsterBook().addCharInfoPacket(chr.getMonsterBookCover(), mplew)
        medal = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-49))
        mplew.writeInt((medal is None) ? 0 : medal.getItemId())
        medalQuests = []
        completed = chr.getCompletedQuests()
        for q in completed:
            if q.getQuest().getMedalItem() > 0 and GameConstants.getInventoryType(q.getQuest().getMedalItem()) == MapleInventoryType.EQUIP:
                medalQuests.add(q.getQuest().getId())
        mplew.writeShort(medalQuests)
        for x in medalQuests:
            mplew.writeShort(x)
        iv = chr.getInventory(MapleInventoryType.SETUP)
        chairItems = []
        for item in iv.list():
            if item.getItemId() >= 3010000 and item.getItemId() <= 3020001:
                chairItems.add(item)
        mplew.writeInt(chairItems)
        for item in chairItems:
            mplew.writeInt(item.getItemId())
        勋章列表 = chr.getInventory(MapleInventoryType.EQUIP)
        勋章列表Items = []
        for item2 in 勋章列表.list():
            if item2.getItemId() >= 1142000 and item2.getItemId() <= 1142999:
                勋章列表Items.add(item2)
        mplew.writeInt(勋章列表Items)
        for item2 in 勋章列表Items:
            mplew.writeInt(item2.getItemId())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def writeLongMask(self, mplew: Any, statups: list) -> None:
        if ServerConstants.调试输出封包:
            print("writeLongMask--------------------")
        firstmask = 0
        secondmask = 0
        for statup in statups:
            if statup.getLeft().isFirst():
                firstmask |= statup.getLeft().getValue()
            else:
                secondmask |= statup.getLeft().getValue()
        mplew.writeLong(firstmask)
        mplew.writeLong(secondmask)

    def writeLongDiseaseMask(self, mplew: Any, statups: list) -> None:
        if ServerConstants.调试输出封包:
            print("writeLongDiseaseMask--------------------")
        firstmask = 0
        secondmask = 0
        for statup in statups:
            if statup.getLeft().isFirst():
                firstmask |= statup.getLeft().getValue()
            else:
                secondmask |= statup.getLeft().getValue()
        mplew.writeLong(firstmask)
        mplew.writeLong(secondmask)

    def writeLongMaskFromListM(self, mplew: Any, statups: list) -> None:
        if ServerConstants.调试输出封包:
            print("writeLongMaskFromList--------------------")
        firstmask = 0
        secondmask = 0
        mplew.write(0)
        for statup in statups:
            if statup.isFirst():
                firstmask |= statup.getValue()
            else:
                secondmask |= statup.getValue()
        mplew.writeLong(firstmask)
        mplew.writeInt(0)
        mplew.writeZeroBytes(3)

    def writeLongMaskFromList(self, mplew: Any, statups: list) -> None:
        if ServerConstants.调试输出封包:
            print("writeLongMaskFromList--------------------")
        firstmask = 0
        secondmask = 0
        for statup in statups:
            if statup.isFirst():
                firstmask |= statup.getValue()
            else:
                secondmask |= statup.getValue()
        mplew.writeLong(firstmask)
        mplew.writeLong(secondmask)

    def giveMount(self, c: Any, buffid: int, skillid: int, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
        print("giveMount--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.write(0)
        writeLongMask(mplew, statups)
        for statup in statups:
            if (statup.getRight()).shortValue() >= 1000 and (statup.getRight()).shortValue() != 1002:
                mplew.writeShort((statup.getRight()).shortValue() + c.getGender() * 100)
            else:
                mplew.write(0)
            mplew.writeInt(buffid)
            mplew.writeInt(skillid)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.write(2)
        a = giveBuff(c, buffid)
        if a > 0:
        mplew.write(a)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveBuff(self, c: Any, buffid: int) -> int:
        a = 0
        # switch (buffid):
            # case 1002:
            # case 8000:
            # case 1121000:
            # case 1221000:
            # case 1321000:
            # case 2121000:
            # case 2221000:
            # case 2321000:
            # case 3121000:
            # case 3221000:
            # case 4101004:
            # case 4121000:
            # case 4201003:
            # case 4221000:
            # case 4341000:
            # case 5101007:
            # case 5121000:
            # case 5221000:
            # case 5321005:
            # case 9001001:
            # case 10001002:
            # case 10008000:
            # case 14101003:
            # case 20001002:
            # case 20008000:
            # case 20018000:
            # case 21121000:
            # case 22171000:
            # case 23121005:
            # case 30008000:
            # case 31121004:
            # case 32121007:
            # case 33121007:
            # case 35121007:
                a = 5
                break
            # case 32101003:
                a = 29
                break
            # case -2022458:
            # case 33121006:
                a = 6
                break
            # case 5111005:
            # case 5121003:
            # case 13111005:
            # case 15111002:
                a = 7
                break
            # case 5301003:
                a = 3
                break
        return a

    def givePirate(self, statups: list, duration: int, skillid: int) -> Any:
        infusion = skillid == 5121009 or skillid == 15111005
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("givePirate--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.writeLong(0)
        mplew.writeLong(MapleBuffStat.变身.getValue())
        mplew.writeShort(0)
        mplew.writeInt(skillid)
        mplew.writeZeroBytes(1)
        mplew.writeInt(duration)
        mplew.writeZeroBytes(6)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveForeignPirate(self, statups: list, duration: int, cid: int, skillid: int) -> Any:
        infusion = skillid == 5121009 or skillid == 15111005
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveForeignPirate--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        writeLongMask(mplew, statups)
        mplew.writeShort(0)
        for stat in statups:
            mplew.writeInt(stat.getRight())
            mplew.writeLong(skillid)
            mplew.writeZeroBytes(infusion ? 7 : 1)
            mplew.writeShort(duration)
        mplew.writeShort(infusion ? 600 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveHoming(self, skillid: int, mobid: int, x: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveHoming--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.writeLong(MapleBuffStat.导航辅助.getValue())
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.writeInt(x)
        mplew.writeLong(skillid)
        mplew.write(0)
        mplew.writeInt(mobid)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveEnergyChargeTest(self, bar: int, bufflength: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveEnergyChargeTestA--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.writeLong(MapleBuffStat.能量获得.getValue())
        mplew.writeLong(0)
        mplew.writeShort(0)
        mplew.writeInt(min(bar, 10000))
        mplew.writeLong(0)
        mplew.write(0)
        mplew.writeInt((bar >= 10000) ? bufflength : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def givePirateBuff(self, buffid: int, bufflength: int, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.writeLong(MapleBuffStat.能量获得.getValue())
        mplew.writeLong(0)
        mplew.writeShort(0)
        for statup in statups:
            mplew.writeShort((statup.getRight()).shortValue())
            mplew.writeShort(0)
            mplew.writeInt(buffid)
            mplew.writeInt(0)
            mplew.write(0)
            mplew.writeShort(bufflength)
        mplew.writeShort(0)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_能量条(self, statups: list, duration: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.write(0)
        mplew.writeLong(MapleBuffStat.能量获得.getValue())
        mplew.writeLong(0)
        mplew.write(0)
        for stat in statups:
            mplew.writeInt((stat.getRight()).shortValue())
            mplew.writeInt(0)
            mplew.writeInt(0)
            mplew.write(0)
            mplew.writeShort(duration)
        mplew.writeShort(0)
        mplew.write(2)
        return mplew.getPacket()

    def translated_能量条2(self, statups: list, duration: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        mplew.write(0)
        mplew.writeLong(MapleBuffStat.能量获得.getValue())
        mplew.writeLong(0)
        mplew.write(0)
        for stat in statups:
            mplew.writeInt((stat.getRight()).shortValue())
            mplew.writeInt(0)
            mplew.writeInt(0)
            mplew.write(0)
            mplew.writeShort(duration)
        mplew.writeShort(0)
        mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveEnergyChargeTest_cid_bar_bufflength(self, cid: int, bar: int, bufflength: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveEnergyChargeTestB--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        mplew.writeLong(0)
        mplew.writeLong(MapleBuffStat.能量获得.getValue())
        mplew.writeShort(0)
        mplew.writeInt(min(bar, 10000))
        mplew.writeLong(0)
        mplew.writeInt((bar >= 10000) ? bufflength : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveBuff_buffid_bufflength_statups_effect(self, buffid: int, bufflength: int, statups: list, effect: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveBuff--1------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        writeLongMask(mplew, statups)
        for statup in statups:
            mplew.writeShort(statup.getRight().shortValue())
            mplew.writeInt(buffid)
            mplew.writeInt(bufflength)
        mplew.writeShort(0)
        mplew.writeShort(0)
        if effect is None or (not effect.is斗气集中() and not effect.isFinalAttack()):
            mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveDebuff(self, statups: list, skillid: int, level: int, duration: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveDebuff--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_BUFF.getValue())
        writeLongDiseaseMask(mplew, statups)
        for statup in statups:
            mplew.writeShort(statup.getRight().shortValue())
            mplew.writeShort(skillid)
            mplew.writeShort(level)
            mplew.writeInt(duration)
        mplew.writeShort(0)
        mplew.writeShort(900)
        mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveForeignDebuff(self, cid: int, statups: list, skillid: int, level: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveForeignDebuff--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        writeLongDiseaseMask(mplew, statups)
        mplew.writeShort(skillid)
        mplew.writeShort(level)
        mplew.writeShort(0)
        mplew.writeShort(900)
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelForeignDebuff(self, cid: int, mask: int, first: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelForeignDebuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        mplew.writeLong(first ? mask : 0)
        mplew.writeLong(first ? 0 : mask)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMonsterRiding(self, cid: int, statups: list, itemId: int, skillId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showMonsterRiding--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        mplew.write(0)
        writeLongMask(mplew, statups)
        mplew.write(0)
        mplew.writeInt(itemId)
        mplew.writeInt(skillId)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveForeignBuff(self, c: Any, cid: int, statups: list, effect: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
        print("giveForeignBuff--------------------")
        mplew.writeShort(SendPacketOpcode.GIVE_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        writeLongMask(mplew, statups)
        for statup in statups:
            if effect.isMorph() and (statup.getRight()) <= 255:
                mplew.write((statup.getRight()).byteValue())
                continue
            if effect.isPirateMorph():
                mplew.writeShort((statup.getRight()).shortValue() + c.getGender() * 100)
                continue
            mplew.writeShort((statup.getRight()).shortValue())
        mplew.writeShort(0)
        if effect.isMorph() and not effect.isPirateMorph():
        mplew.writeShort(0)
        mplew.write(0)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelForeignBuff(self, cid: int, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelForeignBuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        writeLongMaskFromList(mplew, statups)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelForeignBuffMONSTER(self, cid: int, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelForeignBuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        writeLongMaskFromListM(mplew, statups)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelBuffMONSTER(self, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelBuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_BUFF.getValue())
        writeLongMaskFromListM(mplew, statups)
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelBuff(self, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelBuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_BUFF.getValue())
        writeLongMaskFromList(mplew, statups)
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelHoming(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelHoming--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_BUFF.getValue())
        mplew.writeLong(MapleBuffStat.导航辅助.getValue())
        mplew.writeLong(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelDebuff(self, mask: int, first: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelDebuff--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_BUFF.getValue())
        mplew.writeLong(first ? mask : 0)
        mplew.writeLong(first ? 0 : mask)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateMount(self, chr: Any, levelup: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateMount--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_MOUNT.getValue())
        mplew.writeInt(chr.getId())
        mplew.writeInt(chr.getMount().getLevel())
        mplew.writeInt(chr.getMount().getExp())
        mplew.writeInt(chr.getMount().getFatigue())
        mplew.write(levelup ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def mountInfo(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("mountInfo--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_MOUNT.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(1)
        mplew.writeInt(chr.getMount().getLevel())
        mplew.writeInt(chr.getMount().getExp())
        mplew.writeInt(chr.getMount().getFatigue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPlayerShopNewVisitor(self, c: Any, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getPlayerShopNewVisitor--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("04 0" + slot))
        PacketHelper.addCharLook(mplew, c, False)
        mplew.writeMapleAsciiString(c.getName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPlayerShopRemoveVisitor(self, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getPlayerShopRemoveVisitor--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("0A 0" + slot))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradePartnerAdd(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradePartnerAdd--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(4)
        mplew.write(1)
        PacketHelper.addCharLook(mplew, c, False)
        mplew.writeMapleAsciiString(c.getName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeInvite(self, c: Any, 现金交易: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeInvite--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(2)
        mplew.write(现金交易 ? 6 : 3)
        mplew.writeMapleAsciiString(c.getName())
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeMesoSet(self, number: int, meso: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeMesoSet--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(15)
        mplew.write(number)
        mplew.writeInt(meso)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeItemAdd(self, number: int, item: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeItemAdd--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(14)
        mplew.write(number)
        PacketHelper.addItemInfo(mplew, item, False, False, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeStart(self, c: Any, trade: Any, number: int, 现金交易: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeStart--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(5)
        mplew.write(现金交易 ? 6 : 3)
        mplew.write(2)
        mplew.write(number)
        if number == 1:
            mplew.write(0)
            PacketHelper.addCharLook(mplew, trade.getPartner().getChr(), False)
            mplew.writeMapleAsciiString(trade.getPartner().getChr().getName())
        mplew.write(number)
        PacketHelper.addCharLook(mplew, c.getPlayer(), False)
        mplew.writeMapleAsciiString(c.getPlayer().getName())
        mplew.write(255)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeConfirmation(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeConfirmation--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(16)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def TradeMessage(self, UserSlot: int, message: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("TradeMessage--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(10)
        mplew.write(UserSlot)
        mplew.write(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTradeCancel(self, UserSlot: int, unsuccessful: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTradeCancel--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(10)
        mplew.write(UserSlot)
        mplew.write((unsuccessful == 0) ? 2 : ((unsuccessful == 1) ? 9 : 10))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getNPCTalk(self, npc: int, msgType: int, talk: str, endBytes: str, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getNPCTalk--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.write(msgType)
        mplew.write(type)
        mplew.writeMapleAsciiString(talk)
        mplew.write(HexTool.getByteArrayFromHexString(endBytes))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMapSelection(self, npcid: int, sel: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMapSelection--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npcid)
        mplew.writeShort(13)
        mplew.writeInt(0)
        mplew.writeInt(5)
        mplew.writeMapleAsciiString(sel)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getNPCTalkStyle(self, npc: int, talk: str, card: int, args: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getNPCTalkStyle--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.writeShort(7)
        mplew.writeMapleAsciiString(talk)
        mplew.write(len(args))
        for i in range(len(args)):
            mplew.writeInt(args[i])
        mplew.writeInt(card)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getNPCTalkNum(self, npc: int, talk: str, def: int, min: int, max: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getNPCTalkNum--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.writeShort(3)
        mplew.writeMapleAsciiString(talk)
        mplew.writeInt(def)
        mplew.writeInt(min)
        mplew.writeInt(max)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getNPCTalkText(self, npc: int, talk: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getNPCTalkText--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.writeShort(2)
        mplew.writeMapleAsciiString(talk)
        mplew.writeInt(0)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showForeignEffect(self, cid: int, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showForeignEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(cid)
        mplew.write(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBuffeffect(self, cid: int, skillid: int, effectid: int) -> Any:
        if ServerConstants.调试输出封包:
            print("showBuffeffect--------------------")
        return showBuffeffect(cid, skillid, effectid, 3)

    def showBuffeffect_cid_skillid_effectid_direction(self, cid: int, skillid: int, effectid: int, direction: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBuffeffectA--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(cid)
        mplew.write(effectid)
        mplew.writeInt(skillid)
        mplew.write(2)
        mplew.write(1)
        if direction != 3:
            mplew.write(direction)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showOwnBuffEffect(self, skillid: int, effectid: int) -> Any:
        if ServerConstants.调试输出封包:
            print("showOwnBuffEffectA--------------------")
        return showOwnBuffEffect(skillid, effectid, 3)

    def showOwnBuffEffect_skillid_effectid_direction(self, skillid: int, effectid: int, direction: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showOwnBuffEffectB--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(effectid)
        mplew.writeInt(skillid)
        mplew.write(169)
        mplew.write(1)
        if direction != 3:
            mplew.write(direction)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showItemLevelupEffect(self) -> Any:
        if ServerConstants.调试输出封包:
            print("showItemLevelupEffect--------------------")
        return showSpecialEffect(17)

    def showMonsterBookPickup(self) -> Any:
        return showSpecialEffect(14)

    def showEquipmentLevelUp(self) -> Any:
        return showSpecialEffect(17)

    def showItemLevelup(self) -> Any:
        return showSpecialEffect(17)

    def showForeignItemLevelupEffect(self, cid: int) -> Any:
        if ServerConstants.调试输出封包:
            print("showForeignItemLevelupEffect--------------------")
        return showSpecialEffect(cid, 17)

    def showSpecialEffect(self, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showSpecialEffectA--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showSpecialEffect_cid_effect(self, cid: int, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showSpecialEffectB--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(cid)
        mplew.write(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateSkill(self, skillid: int, level: int, masterlevel: int, expiration: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateSkill--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_SKILLS.getValue())
        mplew.write(1)
        mplew.writeShort(1)
        mplew.writeInt(skillid)
        mplew.writeInt(level)
        mplew.writeInt(masterlevel)
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateQuestMobKills(self, status: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuestMobKills--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(1)
        mplew.writeShort(status.getQuest().getId())
        mplew.write(1)
        sb = ""
        for kills in status.getMobKills().values():
            sb.append(StringUtil.getLeftPaddedStr(str(kills), '0', 3))
        mplew.writeMapleAsciiString(sb)
        mplew.writeZeroBytes(8)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_游戏屏幕中间黄色字体(self, status: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuestMobKills--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(1)
        mplew.writeShort(4761)
        mplew.write(1)
        mplew.writeMapleAsciiString(status)
        mplew.writeZeroBytes(8)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_游戏屏幕中间黄色字体_status_id(self, status: str, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateQuestMobKills--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(1)
        mplew.writeShort(id)
        mplew.write(1)
        mplew.writeMapleAsciiString(status)
        mplew.writeZeroBytes(8)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getShowQuestCompletion(self, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getShowQuestCompletion--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_QUEST_COMPLETION.getValue())
        mplew.writeShort(id)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getKeymap(self, layout: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getKeymap--------------------")
        mplew.writeShort(SendPacketOpcode.KEYMAP.getValue())
        mplew.write(0)
        layout.writeData(mplew)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getWhisper(self, sender: str, channel: int, text: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getWhisper--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(18)
        mplew.writeMapleAsciiString(sender)
        mplew.writeShort(channel - 1)
        mplew.writeMapleAsciiString(text)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getWhisperReply(self, target: str, reply: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getWhisperReply--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(10)
        mplew.writeMapleAsciiString(target)
        mplew.write(reply)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getFindReplyWithMap(self, target: str, mapid: int, buddy: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFindReplyWithMap--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(buddy ? 72 : 9)
        mplew.writeMapleAsciiString(target)
        mplew.write(1)
        mplew.writeInt(mapid)
        mplew.writeZeroBytes(8)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getFindReply(self, target: str, channel: int, buddy: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFindReply--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(buddy ? 72 : 9)
        mplew.writeMapleAsciiString(target)
        mplew.write(3)
        mplew.writeInt(channel - 1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getInventoryFull(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getInventoryFull--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(1)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getShowInventoryFull(self) -> Any:
        if ServerConstants.调试输出封包:
            print("getShowInventoryFull--------------------")
        return getShowInventoryStatus(255)

    def showItemUnavailable(self) -> Any:
        if ServerConstants.调试输出封包:
            print("showItemUnavailable--------------------")
        return getShowInventoryStatus(254)

    def getShowInventoryStatus(self, mode: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getShowInventoryStatus--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(0)
        mplew.write(mode)
        mplew.writeInt(0)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getStorage(self, npcId: int, slots: int, items: list, meso: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getStorage--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_STORAGE.getValue())
        mplew.write(22)
        mplew.writeInt(npcId)
        mplew.write(slots)
        mplew.writeShort(126)
        mplew.writeShort(0)
        mplew.writeInt(0)
        mplew.writeInt(meso)
        mplew.write(items)
        for item in items:
            if GameConstants.is豆豆装备(item.getItemId()):
                PacketHelper.addDDItemInfo(mplew, item, True, True, False)
            else:
                PacketHelper.addItemInfo(mplew, item, True, True)
        mplew.writeShort(0)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getStorageFull(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getStorageFull--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_STORAGE.getValue())
        mplew.write(17)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def mesoStorage(self, slots: int, meso: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("mesoStorage--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_STORAGE.getValue())
        mplew.write(19)
        mplew.write(slots)
        mplew.writeShort(2)
        mplew.writeShort(0)
        mplew.writeInt(0)
        mplew.writeInt(meso)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def storeStorage(self, slots: int, type: Any, items: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("storeStorage--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_STORAGE.getValue())
        mplew.write(13)
        mplew.write(slots)
        mplew.writeShort(type.getBitfieldEncoding())
        mplew.writeShort(0)
        mplew.writeInt(0)
        mplew.write(items)
        for item in items:
            PacketHelper.addItemInfo(mplew, item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def takeOutStorage(self, slots: int, type: Any, items: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("takeOutStorage--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_STORAGE.getValue())
        mplew.write(9)
        mplew.write(slots)
        mplew.writeShort(type.getBitfieldEncoding())
        mplew.writeShort(0)
        mplew.writeInt(0)
        mplew.write(items)
        for item in items:
            PacketHelper.addItemInfo(mplew, item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def fairyPendantMessage(self, type: int, percent: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("fairyPendantMessage--------------------")
        mplew.writeShort(SendPacketOpcode.FAIRY_PEND_MSG.getValue())
        mplew.writeShort(21)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.writeShort(percent)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveFameResponse(self, mode: int, charname: str, newfame: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveFameResponse--------------------")
        mplew.writeShort(SendPacketOpcode.FAME_RESPONSE.getValue())
        mplew.write(0)
        mplew.writeMapleAsciiString(charname)
        mplew.write(mode)
        mplew.writeShort(newfame)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def giveFameErrorResponse(self, status: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("giveFameErrorResponse--------------------")
        mplew.writeShort(SendPacketOpcode.FAME_RESPONSE.getValue())
        mplew.write(status)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def receiveFame(self, mode: int, charnameFrom: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("receiveFame--------------------")
        mplew.writeShort(SendPacketOpcode.FAME_RESPONSE.getValue())
        mplew.write(5)
        mplew.writeMapleAsciiString(charnameFrom)
        mplew.write(mode)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def partyCreated(self, partyid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("partyCreated--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        mplew.write(8)
        mplew.writeInt(partyid)
        mplew.write(MaplePacketCreator.CHAR_INFO_MAGIC)
        mplew.write(MaplePacketCreator.CHAR_INFO_MAGIC)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def partyInvite(self, from: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("partyInvite--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        mplew.write(4)
        mplew.writeInt(from.getParty().getId())
        mplew.writeMapleAsciiString(from.getName())
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def partyStatusMessage(self, message: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("partyStatusMessageA--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        mplew.write(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def partyStatusMessage_message_charname(self, message: int, charname: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("partyStatusMessageB--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        mplew.write(message)
        mplew.writeMapleAsciiString(charname)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addPartyStatus(self, forchannel: int, party: Any, lew: Any, leaving: bool) -> None:
        if ServerConstants.调试输出封包:
            print("addPartyStatus--------------------")
        partymembers = [])
        while partymembers < 6:
            partymembers.add(MaplePartyCharacter())
        for partychar in partymembers:
            lew.writeInt(partychar.getId())
        for partychar in partymembers:
            lew.writeAsciiString(StringUtil.getRightPaddedStr(partychar.getName(), '\0', 13))
        for partychar in partymembers:
            lew.writeInt(partychar.getJobId())
        for partychar in partymembers:
            lew.writeInt(partychar.getLevel())
        for partychar in partymembers:
            if partychar.isOnline():
                lew.writeInt(partychar.getChannel() - 1)
            else:
                lew.writeInt(-2)
        lew.writeInt(party.getLeader().getId())
        for partychar in partymembers:
            if partychar.getChannel() == forchannel:
                lew.writeInt(partychar.getMapid())
            else:
                lew.writeInt(0)
        for partychar in partymembers:
            if partychar.getChannel() == forchannel and not leaving:
                lew.writeInt(partychar.getDoorTown())
                lew.writeInt(partychar.getDoorTarget())
                lew.writeInt(partychar.getDoorPosition().x)
                lew.writeInt(partychar.getDoorPosition().y)
            else:
                lew.writeInt(0)
                lew.writeInt(0)
                lew.writeInt(0)
                lew.writeInt(0)

    def updateParty(self, forChannel: int, party: Any, op: Any, target: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateParty--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        # switch (op):
            # case DISBAND:
            # case EXPEL:
            # case LEAVE:
                mplew.write(12)
                mplew.writeInt(party.getId())
                mplew.writeInt(target.getId())
                mplew.write((op != PartyOperation.DISBAND) ? 1 : 0)
                if op == PartyOperation.DISBAND:
                    mplew.writeInt(target.getId())
                    break
                mplew.write((op == PartyOperation.EXPEL) ? 1 : 0)
                mplew.writeMapleAsciiString(target.getName())
                addPartyStatus(forChannel, party, mplew, False)
                break
            # case JOIN:
                mplew.write(15)
                mplew.writeInt(party.getId())
                mplew.writeMapleAsciiString(target.getName())
                addPartyStatus(forChannel, party, mplew, False)
                break
            # case SILENT_UPDATE:
            # case LOG_ONOFF:
                mplew.write(7)
                mplew.writeInt(party.getId())
                addPartyStatus(forChannel, party, mplew, False)
                break
            # case CHANGE_LEADER:
                mplew.write(26)
                mplew.writeInt(target.getId())
                mplew.write(0)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def partyPortal(self, townId: int, targetId: int, skillId: int, position: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("partyPortal--------------------")
        mplew.writeShort(SendPacketOpcode.PARTY_OPERATION.getValue())
        mplew.writeShort(35)
        mplew.writeInt(townId)
        mplew.writeInt(targetId)
        mplew.writePos(position)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updatePartyMemberHP(self, cid: int, curhp: int, maxhp: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updatePartyMemberHP--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_PARTYMEMBER_HP.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(curhp)
        mplew.writeInt(maxhp)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def multiChat(self, name: str, chattext: str, mode: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("multiChat--------------------")
        mplew.writeShort(SendPacketOpcode.MULTICHAT.getValue())
        mplew.write(mode)
        mplew.writeMapleAsciiString(name)
        mplew.writeMapleAsciiString(chattext)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getClock(self, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getClock--------------------")
        mplew.writeShort(SendPacketOpcode.CLOCK.getValue())
        mplew.write(2)
        mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getClockTime(self, hour: int, min: int, sec: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getClockTime--------------------")
        mplew.writeShort(SendPacketOpcode.CLOCK.getValue())
        mplew.write(1)
        mplew.write(hour)
        mplew.write(min)
        mplew.write(sec)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnMist(self, mist: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnMist--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_MIST.getValue())
        mplew.writeInt(mist.getObjectId())
        mplew.writeInt(mist.isMobMist() ? 0 : ((mist.isPoisonMist() != 0) ? 1 : 2))
        mplew.writeInt(mist.getOwnerId())
        if mist.getMobSkill() is None:
            mplew.writeInt(mist.getSourceSkill().getId())
        else:
            mplew.writeInt(mist.getMobSkill().getSkillId())
        mplew.write(mist.getSkillLevel())
        mplew.writeShort(mist.getSkillDelay())
        mplew.writeInt(mist.getBox().x)
        mplew.writeInt(mist.getBox().y)
        mplew.writeInt(mist.getBox().x + mist.getBox().width)
        mplew.writeInt(mist.getBox().y + mist.getBox().height)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeMist(self, oid: int, eruption: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeMist--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_MIST.getValue())
        mplew.writeInt(oid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def damageSummon(self, cid: int, summonSkillId: int, damage: int, unkByte: int, monsterIdFrom: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("damageSummon--------------------")
        mplew.writeShort(SendPacketOpcode.DAMAGE_SUMMON.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(summonSkillId)
        mplew.write(unkByte)
        mplew.writeInt(damage)
        mplew.writeInt(monsterIdFrom)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def buddylistMessage(self, message: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("buddylistMessage--------------------")
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateBuddylist(self, buddylist: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateBuddylist--------------------")
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(7)
        mplew.write(buddylist)
        for buddy in buddylist:
            if buddy.isVisible():
                mplew.writeInt(buddy.getCharacterId())
                mplew.writeAsciiString(StringUtil.getRightPaddedStr(buddy.getName(), '\0', 13))
                mplew.write(0)
                mplew.writeInt((buddy.getChannel() == -1) ? -1 : (buddy.getChannel() - 1))
                mplew.writeAsciiString(StringUtil.getRightPaddedStr(buddy.getGroup(), '\0', 17))
        for x in range(buddylist):
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def requestBuddylistAdd(self, cidFrom: int, nameFrom: str, levelFrom: int, jobFrom: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("requestBuddylistAdd--------------------")
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(9)
        mplew.writeInt(cidFrom)
        mplew.writeMapleAsciiString(nameFrom)
        mplew.writeInt(cidFrom)
        mplew.writeAsciiString(StringUtil.getRightPaddedStr(nameFrom, '\0', 13))
        mplew.write(1)
        mplew.write(5)
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeAsciiString(StringUtil.getRightPaddedStr("群未定", '\0', 17))
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateBuddyChannel(self, characterid: int, channel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateBuddyChannel--------------------")
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(20)
        mplew.writeInt(characterid)
        mplew.write(0)
        mplew.writeInt(channel)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def itemEffect(self, characterid: int, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("itemEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_EFFECT.getValue())
        mplew.writeInt(characterid)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def itemEffects(self, characterid: int, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("itemEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.writeInt(characterid)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateBuddyCapacity(self, capacity: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateBuddyCapacity--------------------")
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(21)
        mplew.write(capacity)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showChair(self, characterid: int, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showChair--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_CHAIR.getValue())
        mplew.writeInt(characterid)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelChair(self, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelChair--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_CHAIR.getValue())
        if id == -1:
            mplew.write(0)
        else:
            mplew.write(1)
            mplew.writeShort(id)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnReactor(self, reactor: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnReactor--------------------")
        mplew.writeShort(SendPacketOpcode.REACTOR_SPAWN.getValue())
        mplew.writeInt(reactor.getObjectId())
        mplew.writeInt(reactor.getReactorId())
        mplew.write(reactor.getState())
        mplew.writePos(reactor.getPosition())
        mplew.write(reactor.getFacingDirection())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def triggerReactor(self, reactor: Any, stance: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("triggerReactor--------------------")
        mplew.writeShort(SendPacketOpcode.REACTOR_HIT.getValue())
        mplew.writeInt(reactor.getObjectId())
        mplew.write(reactor.getState())
        mplew.writePos(reactor.getPosition())
        mplew.writeInt(stance)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def destroyReactor(self, reactor: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("destroyReactor--------------------")
        mplew.writeShort(SendPacketOpcode.REACTOR_DESTROY.getValue())
        mplew.writeInt(reactor.getObjectId())
        mplew.write(reactor.getState())
        mplew.writePos(reactor.getPosition())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def musicChange(self, song: str) -> Any:
        if ServerConstants.调试输出封包:
            print("musicChange--------------------")
        return environmentChange(song, 6)

    def showEffect(self, effect: str) -> Any:
        if ServerConstants.调试输出封包:
            print("showEffect--------------------")
        return environmentChange(effect, 3)

    def playSound(self, sound: str) -> Any:
        if ServerConstants.调试输出封包:
            print("playSound--------------------")
        return environmentChange(sound, 4)

    def environmentChange(self, env: str, mode: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("environmentChange--------------------")
        mplew.writeShort(SendPacketOpcode.BOSS_ENV.getValue())
        mplew.write(mode)
        mplew.writeMapleAsciiString(env)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def startMapEffect(self, msg: str, itemid: int, active: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("startMapEffect--------------------")
        mplew.writeShort(SendPacketOpcode.MAP_EFFECT.getValue())
        mplew.write(active ? 0 : 1)
        mplew.writeInt(itemid)
        if active:
            mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeMapEffect(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeMapEffect--------------------")
        mplew.writeShort(SendPacketOpcode.MAP_EFFECT.getValue())
        mplew.write(0)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def fuckGuildInfo(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("fuckGuildInfo--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(26)
        Prefix = ""
        if c.getPrefix() == 1:
            Prefix = "[技术团队成员]"
        if c.getPrefix() == 2:
            Prefix = "[游戏管理成员]"
        if c.getPrefix() == 3:
            Prefix = "[活动办理成员]"
        mplew.write(1)
        mplew.writeInt(0)
        mplew.writeMapleAsciiString(Prefix)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showGuildInfo(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showGuildInfo--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(26)
        if c is None or c.getMGC() is None:
            mplew.write(0)
            return mplew.getPacket()
        g = World.Guild.getGuild(c.getGuildId())
        if g is None:
            mplew.write(0)
            return mplew.getPacket()
        mgc = g.getMGC(c.getId())
        c.setGuildRank(mgc.getGuildRank())
        mplew.write(1)
        getGuildInfo(mplew, g)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGuildInfo(self, mplew: Any, guild: Any) -> None:
        if ServerConstants.调试输出封包:
            print("getGuildInfo--------------------")
        mplew.writeInt(guild.getId())
        mplew.writeMapleAsciiString(guild.getName())
        for i in range(1, = 5):
            mplew.writeMapleAsciiString(guild.getRankTitle(i))
        guild.addMemberData(mplew)
        mplew.writeInt(guild.getCapacity())
        mplew.writeShort(guild.getLogoBG())
        mplew.write(guild.getLogoBGColor())
        mplew.writeShort(guild.getLogo())
        mplew.write(guild.getLogoColor())
        mplew.writeMapleAsciiString(guild.getNotice())
        mplew.writeInt(guild.getGP())
        mplew.writeInt((guild.getAllianceId() > 0) ? guild.getAllianceId() : 0)

    def getGuildInfo2(self, mplew: Any, guild: Any, chr: Any) -> None:
        if ServerConstants.调试输出封包:
            print("getGuildInfo2--------------------")
        mplew.writeInt(guild.getId())
        mplew.writeMapleAsciiString(guild.getName())
        for i in range(1, = 5):
            mplew.writeMapleAsciiString(guild.getRankTitle(i))
        guild.addMemberData(mplew)
        mplew.writeInt(guild.getCapacity())
        mplew.writeShort(guild.getLogoBG())
        mplew.write(guild.getLogoBGColor())
        mplew.writeShort(guild.getLogo())
        mplew.write(guild.getLogoColor())
        mplew.writeMapleAsciiString(guild.getNotice())
        mplew.writeInt(guild.getGP())
        mplew.writeInt((guild.getAllianceId() > 0) ? guild.getAllianceId() : 0)

    def guildMemberOnline(self, gid: int, cid: int, bOnline: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildMemberOnline--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(61)
        mplew.writeInt(gid)
        mplew.writeInt(cid)
        mplew.write(bOnline ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildInvite(self, gid: int, charName: str, levelFrom: int, jobFrom: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildInvite--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(5)
        mplew.writeInt(gid)
        mplew.writeMapleAsciiString(charName)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def denyGuildInvitation(self, charname: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("denyGuildInvitation--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(55)
        mplew.writeMapleAsciiString(charname)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def genericGuildMessage(self, code: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("genericGuildMessage--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(code)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def newGuildMember(self, mgc: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("newGuildMember--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(39)
        mplew.writeInt(mgc.getGuildId())
        mplew.writeInt(mgc.getId())
        mplew.writeAsciiString(StringUtil.getRightPaddedStr(mgc.getName(), '\0', 13))
        mplew.writeInt(mgc.getJobId())
        mplew.writeInt(mgc.getLevel())
        mplew.writeInt(mgc.getGuildRank())
        mplew.writeInt(mgc.isOnline() ? 1 : 0)
        mplew.writeInt(1)
        mplew.writeInt(mgc.getAllianceRank())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def memberLeft(self, mgc: Any, bExpelled: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("memberLeft--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(bExpelled ? 47 : 44)
        mplew.writeInt(mgc.getGuildId())
        mplew.writeInt(mgc.getId())
        mplew.writeMapleAsciiString(mgc.getName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeRank(self, mgc: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeRank--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(64)
        mplew.writeInt(mgc.getGuildId())
        mplew.writeInt(mgc.getId())
        mplew.write(mgc.getGuildRank())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildNotice(self, gid: int, notice: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildNotice--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(68)
        mplew.writeInt(gid)
        mplew.writeMapleAsciiString(notice)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildMemberLevelJobUpdate(self, mgc: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildMemberLevelJobUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(60)
        mplew.writeInt(mgc.getGuildId())
        mplew.writeInt(mgc.getId())
        mplew.writeInt(mgc.getLevel())
        mplew.writeInt(mgc.getJobId())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def rankTitleChange(self, gid: int, ranks: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("rankTitleChange--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(62)
        mplew.writeInt(gid)
        for r in ranks:
            mplew.writeMapleAsciiString(r)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildDisband(self, gid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildDisband--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(50)
        mplew.writeInt(gid)
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildEmblemChange(self, gid: int, bg: int, bgcolor: int, logo: int, logocolor: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildEmblemChange--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(66)
        mplew.writeInt(gid)
        mplew.writeShort(bg)
        mplew.write(bgcolor)
        mplew.writeShort(logo)
        mplew.write(logocolor)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def guildCapacityChange(self, gid: int, capacity: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("guildCapacityChange--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(58)
        mplew.writeInt(gid)
        mplew.write(capacity)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeGuildFromAlliance(self, alliance: Any, expelledGuild: Any, expelled: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeGuildFromAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(16)
        addAllianceInfo(mplew, alliance)
        getGuildInfo(mplew, expelledGuild)
        mplew.write(expelled ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeAlliance(self, alliance: Any, in: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(1)
        mplew.write(in ? 1 : 0)
        mplew.writeInt(in ? alliance.getId() : 0)
        noGuilds = alliance.getNoGuilds()
        g = new MapleGuild[noGuilds]
        for i in range(noGuilds):
            g[i] = World.Guild.getGuild(alliance.getGuildId(i))
            if g[i] is None:
                return enableActions()
        mplew.write(noGuilds)
        for i in range(noGuilds):
            mplew.writeInt(g[i].getId())
            members = g[i].getMembers()
            mplew.writeInt(members)
            for mgc in members:
                mplew.writeInt(mgc.getId())
                mplew.write((byte)(in ? mgc.getAllianceRank() : 0))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeAllianceLeader(self, allianceid: int, newLeader: int, oldLeader: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeAllianceLeaderA--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(2)
        mplew.writeInt(allianceid)
        mplew.writeInt(oldLeader)
        mplew.writeInt(newLeader)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAllianceLeader(self, allianceid: int, newLeader: int, oldLeader: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateAllianceLeaderB--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(25)
        mplew.writeInt(allianceid)
        mplew.writeInt(oldLeader)
        mplew.writeInt(newLeader)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendAllianceInvite(self, allianceName: str, inviter: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendAllianceInvite--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(3)
        mplew.writeInt(inviter.getGuildId())
        mplew.writeMapleAsciiString(inviter.getName())
        mplew.writeMapleAsciiString(allianceName)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeGuildInAlliance(self, alliance: Any, guild: Any, add: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeGuildInAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(4)
        mplew.writeInt(add ? alliance.getId() : 0)
        mplew.writeInt(guild.getId())
        members = guild.getMembers()
        mplew.writeInt(members)
        for mgc in members:
            mplew.writeInt(mgc.getId())
            mplew.write((byte)(add ? mgc.getAllianceRank() : 0))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeAllianceRank(self, allianceid: int, player: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeAllianceRank--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(5)
        mplew.writeInt(allianceid)
        mplew.writeInt(player.getId())
        mplew.writeInt(player.getAllianceRank())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def createGuildAlliance(self, alliance: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("createGuildAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(15)
        addAllianceInfo(mplew, alliance)
        noGuilds = alliance.getNoGuilds()
        g = new MapleGuild[noGuilds]
        for i in range(alliance.getNoGuilds()):
            g[i] = World.Guild.getGuild(alliance.getGuildId(i))
            if g[i] is None:
                return enableActions()
        for gg in g:
            getGuildInfo(mplew, gg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getAllianceInfo(self, alliance: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getAllianceInfo--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(12)
        mplew.write((alliance is not None) ? 1 : 0)
        if alliance is not None:
            addAllianceInfo(mplew, alliance)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getAllianceUpdate(self, alliance: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getAllianceUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(23)
        addAllianceInfo(mplew, alliance)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGuildAlliance(self, alliance: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getGuildAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(13)
        if alliance is None:
            mplew.writeInt(0)
            return mplew.getPacket()
        noGuilds = alliance.getNoGuilds()
        g = new MapleGuild[noGuilds]
        for i in range(alliance.getNoGuilds()):
            g[i] = World.Guild.getGuild(alliance.getGuildId(i))
            if g[i] is None:
                return enableActions()
        mplew.writeInt(noGuilds)
        for gg in g:
            getGuildInfo(mplew, gg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addGuildToAlliance(self, alliance: Any, newGuild: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addGuildToAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(18)
        addAllianceInfo(mplew, alliance)
        mplew.writeInt(newGuild.getId())
        getGuildInfo(mplew, newGuild)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addAllianceInfo(self, mplew: Any, alliance: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addAllianceInfo--------------------")
        mplew.writeInt(alliance.getId())
        mplew.writeMapleAsciiString(alliance.getName())
        for i in range(1, = 5):
            mplew.writeMapleAsciiString(alliance.getRank(i))
        mplew.write(alliance.getNoGuilds())
        for i in range(alliance.getNoGuilds()):
            mplew.writeInt(alliance.getGuildId(i))
        mplew.writeInt(alliance.getCapacity())
        mplew.writeMapleAsciiString(alliance.getNotice())

    def allianceMemberOnline(self, alliance: int, gid: int, id: int, online: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("allianceMemberOnline--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(14)
        mplew.writeInt(alliance)
        mplew.writeInt(gid)
        mplew.writeInt(id)
        mplew.write(online ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAlliance(self, mgc: Any, allianceid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(24)
        mplew.writeInt(allianceid)
        mplew.writeInt(mgc.getGuildId())
        mplew.writeInt(mgc.getId())
        mplew.writeInt(mgc.getLevel())
        mplew.writeInt(mgc.getJobId())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAllianceRank(self, allianceid: int, mgc: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateAllianceRank--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(27)
        mplew.writeInt(allianceid)
        mplew.writeInt(mgc.getId())
        mplew.writeInt(mgc.getAllianceRank())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def disbandAlliance(self, alliance: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("disbandAlliance--------------------")
        mplew.writeShort(SendPacketOpcode.ALLIANCE_OPERATION.getValue())
        mplew.write(29)
        mplew.writeInt(alliance)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def BBSThreadList(self, bbs: list, start: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("BBSThreadList--------------------")
        mplew.writeShort(SendPacketOpcode.BBS_OPERATION.getValue())
        mplew.write(6)
        if bbs is None:
            mplew.write(0)
            mplew.writeLong(0)
            return mplew.getPacket()
        threadCount = bbs
        notice = None
        for b in bbs:
            if b.isNotice():
                notice = b
                break
        ret = (notice is not None) ? 1 : 0
        mplew.write(ret)
        if notice is not None:
            addThread(mplew, notice)
            threadCount -= 1
        if threadCount < start:
            start = 0
        mplew.writeInt(threadCount)
        pages = min(10, threadCount - start)
        mplew.writeInt(pages)
        for i in range(pages):
            addThread(mplew, bbs.get(start + i + ret))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addThread(self, mplew: Any, rs: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addThread--------------------")
        mplew.writeInt(rs.localthreadID)
        mplew.writeInt(rs.ownerID)
        mplew.writeMapleAsciiString(rs.name)
        mplew.writeLong(PacketHelper.getKoreanTimestamp(rs.timestamp))
        mplew.writeInt(rs.icon)
        mplew.writeInt(rs.getReplyCount())

    def showThread(self, thread: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showThread--------------------")
        mplew.writeShort(SendPacketOpcode.BBS_OPERATION.getValue())
        mplew.write(7)
        mplew.writeInt(thread.localthreadID)
        mplew.writeInt(thread.ownerID)
        mplew.writeLong(PacketHelper.getKoreanTimestamp(thread.timestamp))
        mplew.writeMapleAsciiString(thread.name)
        mplew.writeMapleAsciiString(thread.text)
        mplew.writeInt(thread.icon)
        mplew.writeInt(thread.getReplyCount())
        for (final MapleBBSThread.MapleBBSReply reply : thread.replies.values())
            mplew.writeInt(reply.replyid)
            mplew.writeInt(reply.ownerID)
            mplew.writeLong(PacketHelper.getKoreanTimestamp(reply.timestamp))
            mplew.writeMapleAsciiString(reply.content)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showGuildRanks(self, npcid: int, all: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showGuildRanks--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        mplew.writeInt(all)
        for (final MapleGuildRanking.GuildRankingInfo info : all)
            mplew.writeMapleAsciiString(info.getName())
            mplew.writeInt(info.getGP())
            mplew.writeInt(info.getLogo())
            mplew.writeInt(info.getLogoColor())
            mplew.writeInt(info.getLogoBg())
            mplew.writeInt(info.getLogoBgColor())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showmesoRanks(self, npcid: int, all: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        mplew.writeInt(all)
        for (MapleGuildRanking.mesoRankingInfo info : all)
            mplew.writeMapleAsciiString(info.getName())
            mplew.writeInt(Long.valueOf(info.getMeso()))
            mplew.writeInt(info.getStr())
            mplew.writeInt(info.getDex())
            mplew.writeInt(info.getInt())
            mplew.writeInt(info.getLuk())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showlevelRanks(self, npcid: int, all: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        mplew.writeInt(all)
        for (final MapleGuildRanking.levelRankingInfo info : all)
            mplew.writeMapleAsciiString(info.getName())
            mplew.writeInt(info.getLevel())
            mplew.writeInt(info.getStr())
            mplew.writeInt(info.getDex())
            mplew.writeInt(info.getInt())
            mplew.writeInt(info.getLuk())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showGuildRanks_npcid_rs(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("GP"))
            mplew.writeInt(rs.getInt("logo"))
            mplew.writeInt(rs.getInt("logoColor"))
            mplew.writeInt(rs.getInt("logoBG"))
            mplew.writeInt(rs.getInt("logoBGColor"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showLevelRanks(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("level"))
            mplew.writeInt(rs.getInt("vip"))
            mplew.writeInt(rs.getInt("meso"))
            mplew.writeInt(0)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMesoRanks(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("meso"))
            mplew.writeInt(rs.getInt("vip"))
            mplew.writeInt(rs.getInt("level"))
            mplew.writeInt(0)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def MapleMSpvpdeaths(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("pvpdeaths"))
            mplew.writeInt(rs.getInt("str"))
            mplew.writeInt(rs.getInt("dex"))
            mplew.writeInt(rs.getInt("int"))
            mplew.writeInt(rs.getInt("luk"))
        return mplew.getPacket()

    def showCustomRanks(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("data"))
            mplew.writeInt(rs.getInt("level"))
            mplew.writeInt(rs.getInt("meso"))
            mplew.writeInt(0)
            mplew.writeInt(0)
        return mplew.getPacket()

    def MapleMSpvpkills(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("pvpkills"))
            mplew.writeInt(rs.getInt("str"))
            mplew.writeInt(rs.getInt("dex"))
            mplew.writeInt(rs.getInt("int"))
            mplew.writeInt(rs.getInt("luk"))
        return mplew.getPacket()

    def showRQRanks(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("fame"))
            mplew.writeInt(rs.getInt("level"))
            mplew.writeInt(rs.getInt("meso"))
            mplew.writeInt(0)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showVipRanks(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("vip"))
            mplew.writeInt(rs.getInt("level"))
            mplew.writeInt(rs.getInt("meso"))
            mplew.writeInt(0)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateGP(self, gid: int, GP: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateGP--------------------")
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(72)
        mplew.writeInt(gid)
        mplew.writeInt(GP)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def skillEffect(self, from: Any, skillId: int, level: int, flags: int, speed: int, unk: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("skillEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SKILL_EFFECT.getValue())
        mplew.writeInt(from.getId())
        mplew.writeInt(skillId)
        mplew.write(level)
        mplew.write(flags)
        mplew.write(speed)
        mplew.write(unk)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def skillCancel(self, from: Any, skillId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("skillCancel--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_SKILL_EFFECT.getValue())
        mplew.writeInt(from.getId())
        mplew.writeInt(skillId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMagnet(self, mobid: int, success: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showMagnet--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_MAGNET.getValue())
        mplew.writeInt(mobid)
        mplew.write(success)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendHint(self, hint: str, width: int, height: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendHint--------------------")
        if width < 1:
            width = hint * 10
            if width < 40:
                width = 40
        if height < 5:
            height = 5
        mplew.writeShort(SendPacketOpcode.PLAYER_HINT.getValue())
        mplew.writeMapleAsciiString(hint)
        mplew.writeShort(width)
        mplew.writeShort(height)
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def messengerInvite(self, from: str, messengerid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("messengerInvite--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(3)
        mplew.writeMapleAsciiString(from)
        mplew.write(5)
        mplew.writeInt(messengerid)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addMessengerPlayer(self, from: str, chr: Any, position: int, channel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addMessengerPlayer--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(0)
        mplew.write(position)
        PacketHelper.addCharLook(mplew, chr, True)
        mplew.writeMapleAsciiString(from)
        mplew.writeShort(channel)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeMessengerPlayer(self, position: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeMessengerPlayer--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(2)
        mplew.write(position)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateMessengerPlayer(self, from: str, chr: Any, position: int, channel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateMessengerPlayer--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(7)
        mplew.write(position)
        PacketHelper.addCharLook(mplew, chr, True)
        mplew.writeMapleAsciiString(from)
        mplew.writeShort(channel)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def joinMessenger(self, position: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("joinMessenger--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(1)
        mplew.write(position)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def messengerChat(self, text: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("messengerChat--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(6)
        mplew.writeMapleAsciiString(text)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def messengerNote(self, text: str, mode: int, mode2: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("messengerNote--------------------")
        mplew.writeShort(SendPacketOpcode.MESSENGER.getValue())
        mplew.write(mode)
        mplew.writeMapleAsciiString(text)
        mplew.write(mode2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getFindReplyWithCS(self, target: str, buddy: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFindReplyWithCS--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(buddy ? 72 : 9)
        mplew.writeMapleAsciiString(target)
        mplew.write(2)
        mplew.writeInt(-1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getFindReplyWithMTS(self, target: str, buddy: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFindReplyWithMTS--------------------")
        mplew.writeShort(SendPacketOpcode.WHISPER.getValue())
        mplew.write(buddy ? 72 : 9)
        mplew.writeMapleAsciiString(target)
        mplew.write(0)
        mplew.writeInt(-1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showEquipEffect(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showEquipEffectA--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_EQUIP_EFFECT.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showEquipEffect_team(self, team: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showEquipEffectB--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_EQUIP_EFFECT.getValue())
        mplew.writeShort(team)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def summonSkill(self, cid: int, summonSkillId: int, newStance: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("summonSkill--------------------")
        mplew.writeShort(SendPacketOpcode.SUMMON_SKILL.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(summonSkillId)
        mplew.write(newStance)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def skillCooldown(self, sid: int, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("skillCooldown--------------------")
        mplew.writeShort(SendPacketOpcode.COOLDOWN.getValue())
        mplew.writeInt(sid)
        mplew.writeShort(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def useSkillBook(self, chr: Any, skillid: int, maxlevel: int, canuse: bool, success: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("useSkillBook--------------------")
        mplew.writeShort(SendPacketOpcode.USE_SKILL_BOOK.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(1)
        mplew.writeInt(skillid)
        mplew.writeInt(maxlevel)
        mplew.write(canuse ? 1 : 0)
        mplew.write(success ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMacros(self, macros: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMacros--------------------")
        mplew.writeShort(SendPacketOpcode.SKILL_MACRO.getValue())
        count = 0
        for i in range(5):
            if macros[i] is not None:
                count += 1
        mplew.write(count)
        for i in range(5):
            macro = macros[i]
            if macro is not None:
                mplew.writeMapleAsciiString(macro.getName())
                mplew.write(macro.getShout())
                mplew.writeInt(macro.getSkill1())
                mplew.writeInt(macro.getSkill2())
                mplew.writeInt(macro.getSkill3())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAriantPQRanking(self, name: str, score: int, empty: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateAriantPQRanking--------------------")
        mplew.writeShort(SendPacketOpcode.ARIANT_SCORE_UPDATE.getValue())
        mplew.write(empty ? 0 : 1)
        if not empty:
            mplew.writeMapleAsciiString(name)
            mplew.writeInt(score)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def catchMonster(self, mobid: int, itemid: int, success: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("catchMonster--------------------")
        if (itemid == 2270002) {}
        mplew.writeShort(153)
        mplew.writeInt(mobid)
        mplew.writeInt(itemid)
        mplew.write(success)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showAriantScoreBoard(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showAriantScoreBoard--------------------")
        mplew.writeShort(SendPacketOpcode.ARIANT_SCOREBOARD.getValue())
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def boatPacket(self, type: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("boatPacket1--------------------")
        mplew.writeShort(SendPacketOpcode.BOAT_PACKET.getValue())
        mplew.writeShort(type ? 1 : 2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def boatPacket_effect(self, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("boatPacket2--------------------")
        mplew.writeShort(SendPacketOpcode.BOAT_PACKET.getValue())
        mplew.writeShort(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def boatEffect(self, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("boatEffect--------------------")
        mplew.writeShort(SendPacketOpcode.BOAT_EFFECT.getValue())
        mplew.writeShort(effect)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeItemFromDuey(self, remove: bool, Package: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeItemFromDuey--------------------")
        mplew.writeShort(SendPacketOpcode.DUEY.getValue())
        mplew.write(23)
        mplew.writeInt(Package)
        mplew.write(remove ? 3 : 4)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendDuey(self, operation: int, packages: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendDuey--------------------")
        mplew.writeShort(SendPacketOpcode.DUEY.getValue())
        mplew.write(operation)
        # switch (operation):
            # case 8:
                mplew.write(1)
                break
            # case 9:
                mplew.write(0)
                mplew.write(packages)
                for dp in packages:
                    mplew.writeInt(dp.getPackageId())
                    mplew.writeAsciiString(dp.getSender(), 15)
                    mplew.writeInt(dp.getMesos())
                    mplew.writeLong(KoreanDateUtil.getFileTimestamp(dp.getSentTime(), False))
                    mplew.writeZeroBytes(205)
                    if dp.getItem() is not None:
                        mplew.write(1)
                        PacketHelper.addItemInfo(mplew, dp.getItem(), True, True)
                    else:
                        mplew.write(0)
                mplew.write(0)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def Mulung_DojoUp2(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("Mulung_DojoUp2--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(7)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def dojoWarpUp(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.DOJO_WARP_UP.getValue())
        mplew.write(0)
        mplew.write(6)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showQuestMsg(self, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showQuestMsg--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(9)
        mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def HSText(self, m: str) -> Any:
        if ServerConstants.调试输出封包:
            print("Mulung_Pts--------------------")
        return showQuestMsg(m)

    def Mulung_Pts(self, recv: int, total: int) -> Any:
        if ServerConstants.调试输出封包:
            print("Mulung_Pts--------------------")
        return showQuestMsg("你获得 " + recv + " 修炼点数, 目前累计了 " + total + " 点修炼点数")

    def showOXQuiz(self, questionSet: int, questionId: int, askQuestion: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showOXQuiz--------------------")
        mplew.writeShort(SendPacketOpcode.OX_QUIZ.getValue())
        mplew.write(askQuestion ? 1 : 0)
        mplew.write(questionSet)
        mplew.writeShort(questionId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def leftKnockBack(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("leftKnockBack--------------------")
        mplew.writeShort(SendPacketOpcode.LEFT_KNOCK_BACK.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def rollSnowball(self, type: int, ball1: Any, ball2: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("rollSnowball--------------------")
        mplew.writeShort(SendPacketOpcode.ROLL_SNOWBALL.getValue())
        mplew.write(type)
        mplew.writeInt((ball1 is None) ? 0 : (ball1.getSnowmanHP() / 75))
        mplew.writeInt((ball2 is None) ? 0 : (ball2.getSnowmanHP() / 75))
        mplew.writeShort((ball1 is None) ? 0 : ball1.getPosition())
        mplew.write(0)
        mplew.writeShort((ball2 is None) ? 0 : ball2.getPosition())
        mplew.writeZeroBytes(11)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def enterSnowBall(self) -> Any:
        if ServerConstants.调试输出封包:
            print("enterSnowBall--------------------")
        return rollSnowball(0, None, None)

    def hitSnowBall(self, team: int, damage: int, distance: int, delay: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("hitSnowBall--------------------")
        mplew.writeShort(SendPacketOpcode.HIT_SNOWBALL.getValue())
        mplew.write(team)
        mplew.writeShort(damage)
        mplew.write(distance)
        mplew.write(delay)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def snowballMessage(self, team: int, message: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("snowballMessage--------------------")
        mplew.writeShort(SendPacketOpcode.SNOWBALL_MESSAGE.getValue())
        mplew.write(team)
        mplew.writeInt(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def finishedSort(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("finishedSort--------------------")
        mplew.writeShort(SendPacketOpcode.FINISH_SORT.getValue())
        mplew.write(1)
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def coconutScore(self, coconutscore: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("coconutScore--------------------")
        mplew.writeShort(SendPacketOpcode.COCONUT_SCORE.getValue())
        mplew.writeShort(coconutscore[0])
        mplew.writeShort(coconutscore[1])
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def hitCoconut(self, spawn: bool, id: int, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("hitCoconut--------------------")
        mplew.writeShort(SendPacketOpcode.HIT_COCONUT.getValue())
        if spawn:
            mplew.write(0)
            mplew.writeInt(128)
        else:
            mplew.writeInt(id)
            mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def finishedGather(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("finishedGather--------------------")
        mplew.writeShort(SendPacketOpcode.FINISH_GATHER.getValue())
        mplew.write(1)
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def yellowChat(self, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("yellowChat--------------------")
        mplew.writeShort(SendPacketOpcode.YELLOW_CHAT.getValue())
        mplew.write(-1)
        mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendLevelup(self, family: bool, level: int, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendLevelup--------------------")
        mplew.writeShort(SendPacketOpcode.LEVEL_UPDATE.getValue())
        mplew.write(family ? 1 : 2)
        mplew.writeInt(level)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendMarriage(self, family: bool, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendMarriage--------------------")
        mplew.writeShort(SendPacketOpcode.MARRIAGE_UPDATE.getValue())
        mplew.write(family ? 1 : 0)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendJobup(self, family: bool, jobid: int, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendJobup--------------------")
        mplew.writeShort(SendPacketOpcode.JOB_UPDATE.getValue())
        mplew.write(family ? 1 : 0)
        mplew.writeInt(jobid)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showZakumShrine(self, spawned: bool, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showZakumShrine--------------------")
        mplew.writeShort(SendPacketOpcode.ZAKUM_SHRINE.getValue())
        mplew.write(spawned ? 1 : 0)
        mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showHorntailShrine(self, spawned: bool, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showHorntailShrine--------------------")
        mplew.writeShort(SendPacketOpcode.HORNTAIL_SHRINE.getValue())
        mplew.write(spawned ? 1 : 0)
        mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showChaosZakumShrine(self, spawned: bool, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showChaosZakumShrine--------------------")
        mplew.writeShort(SendPacketOpcode.CHAOS_ZAKUM_SHRINE.getValue())
        mplew.write(spawned ? 1 : 0)
        mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showChaosHorntailShrine(self, spawned: bool, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showChaosHorntailShrine--------------------")
        mplew.writeShort(SendPacketOpcode.CHAOS_HORNTAIL_SHRINE.getValue())
        mplew.write(spawned ? 1 : 0)
        mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def stopClock(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("stopClock--------------------")
        mplew.writeShort(SendPacketOpcode.STOP_CLOCK.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addTutorialStats(self) -> Any:
        mplew = MaplePacketLittleEndianWriter(0)
        if ServerConstants.调试输出封包:
            print("addTutorialStats--------------------")
        mplew.writeShort(SendPacketOpcode.TEMP_STATS.getValue())
        mplew.writeInt(3871)
        mplew.writeShort(999)
        mplew.writeShort(999)
        mplew.writeShort(999)
        mplew.writeShort(999)
        mplew.writeShort(255)
        mplew.writeShort(999)
        mplew.writeShort(999)
        mplew.write(120)
        mplew.write(140)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def temporaryStats_Aran(self) -> Any:
        if ServerConstants.调试输出封包:
            print("temporaryStats_Aran--------------------")
        final List<Pair<MapleStat.Temp, Integer>> stats = new ArrayList<Pair<MapleStat.Temp, Integer>>()
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.STR, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.DEX, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.INT, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.LUK, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.WATK, 255))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.ACC, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.AVOID, 999))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.SPEED, 140))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.JUMP, 120))
        return temporaryStats(stats)

    def temporaryStats_Balrog(self, chr: Any) -> Any:
        if ServerConstants.调试输出封包:
            print("temporaryStats_Balrog--------------------")
        final List<Pair<MapleStat.Temp, Integer>> stats = new ArrayList<Pair<MapleStat.Temp, Integer>>()
        offset = 1 + (chr.getLevel() - 90) / 20
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.STR, chr.getStat().getTotalStr() / offset))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.DEX, chr.getStat().getTotalDex() / offset))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.INT, chr.getStat().getTotalInt() / offset))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.LUK, chr.getStat().getTotalLuk() / offset))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.WATK, chr.getStat().getTotalWatk() / offset))
        stats.add(new Pair<MapleStat.Temp, Integer>(MapleStat.Temp.MATK, chr.getStat().getTotalMagic() / offset))
        return temporaryStats(stats)

    def temporaryStats(self, stats: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("temporaryStats--------------------")
        mplew.writeShort(SendPacketOpcode.TEMP_STATS.getValue())
        updateMask = 0
        for (final Pair<MapleStat.Temp, Integer> statupdate : stats)
            updateMask |= statupdate.getLeft().getValue()
        final List<Pair<MapleStat.Temp, Integer>> mystats = stats
        if mystats > 1:
            Collections.sort(mystats, new Comparator<Pair<MapleStat.Temp, Integer>>()
                public int compare(final Pair<MapleStat.Temp, Integer> o1, final Pair<MapleStat.Temp, Integer> o2)
                    val1 = o1.getLeft().getValue()
                    val2 = o2.getLeft().getValue()
                    return (val1 < val2) ? -1 : ((val1 == val2) ? 0 : 1)
        mplew.writeInt(updateMask)
        for (final Pair<MapleStat.Temp, Integer> statupdate2 : mystats)
            value = statupdate2.getLeft().getValue()
            if value >= 1:
                if value <= 512:
                    mplew.writeShort(statupdate2.getRight().shortValue())
                else:
                    mplew.write(statupdate2.getRight().byteValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def compare_o1_o2(self, o1: Any, o2: Any) -> int:
        val1 = o1.getLeft().getValue()
        val2 = o2.getLeft().getValue()
        return (val1 < val2) ? -1 : ((val1 == val2) ? 0 : 1)

    def temporaryStats_Reset(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("temporaryStats_Reset--------------------")
        mplew.writeShort(SendPacketOpcode.TEMP_STATS_RESET.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showHpHealed(self, cid: int, amount: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showHpHealed--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(cid)
        mplew.write(6)
        mplew.writeInt(amount)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showOwnHpHealed(self, amount: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showOwnHpHealed--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(6)
        mplew.writeInt(amount)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendPyramidUpdate(self, amount: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendPyramidUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.PYRAMID_UPDATE.getValue())
        mplew.writeInt(amount)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendPyramidResult(self, rank: int, amount: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendPyramidResult--------------------")
        mplew.writeShort(SendPacketOpcode.PYRAMID_RESULT.getValue())
        mplew.write(rank)
        mplew.writeInt(amount)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendMarrageEffect(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendMarrageEffect--------------------")
        mplew.writeShort(71)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendPyramidEnergy(self, type: str, amount: str) -> Any:
        if ServerConstants.调试输出封包:
            print("sendPyramidEnergy--------------------")
        return sendString(1, type, amount)

    def sendString(self, type: int, object: str, amount: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
        print("sendString--------------------")
        # switch (type):
            # case 1:
            mplew.writeShort(SendPacketOpcode.ENERGY.getValue())
            break
            # case 2:
            mplew.writeShort(SendPacketOpcode.GHOST_POINT.getValue())
            break
            # case 3:
            mplew.writeShort(SendPacketOpcode.GHOST_STATUS.getValue())
            break
        mplew.writeMapleAsciiString(object)
        mplew.writeMapleAsciiString(amount)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendGhostPoint(self, type: str, amount: str) -> Any:
        if ServerConstants.调试输出封包:
            print("sendGhostPoint--------------------")
        return sendString(2, type, amount)

    def sendGhostStatus(self, type: str, amount: str) -> Any:
        if ServerConstants.调试输出封包:
            print("sendGhostStatus--------------------")
        return sendString(3, type, amount)

    def MulungEnergy(self, energy: int) -> Any:
        if ServerConstants.调试输出封包:
            print("MulungEnergy--------------------")
        return sendPyramidEnergy("energy", str(energy))

    def getEvanTutorial(self, data: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getEvanTutorial--------------------")
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.writeInt(8)
        mplew.write(0)
        mplew.write(1)
        mplew.write(1)
        mplew.write(1)
        mplew.writeMapleAsciiString(data)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showEventInstructions(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showEventInstructions--------------------")
        mplew.writeShort(SendPacketOpcode.GMEVENT_INSTRUCTIONS.getValue())
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getOwlOpen(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getOwlOpen--------------------")
        mplew.writeShort(SendPacketOpcode.OWL_OF_MINERVA.getValue())
        mplew.write(7)
        mplew.write(GameConstants.len(owlItems))
        for i in GameConstants.owlItems:
            mplew.writeInt(i)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getOwlSearched(self, itemSearch: int, hms: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getOwlSearched--------------------")
        mplew.writeShort(SendPacketOpcode.OWL_OF_MINERVA.getValue())
        mplew.write(6)
        mplew.writeInt(0)
        mplew.writeInt(itemSearch)
        size = 0
        for hm in hms:
            size += hm.searchItem(itemSearch)
        mplew.writeInt(size)
        for hm in hms:
            items = hm.searchItem(itemSearch)
            for item in items:
                mplew.writeMapleAsciiString(hm.getOwnerName())
                mplew.writeInt(hm.getMap().getId())
                mplew.writeMapleAsciiString(hm.getDescription())
                mplew.writeInt(item.item.getQuantity())
                mplew.writeInt(item.bundles)
                mplew.writeInt(item.price)
                # switch (InventoryHandler.OWL_ID):
                    # case 0:
                        mplew.writeInt(hm.getOwnerId())
                        break
                    # case 1:
                        mplew.writeInt(hm.getStoreId())
                        break
                    # default:
                        mplew.writeInt(hm.getObjectId())
                        break
                mplew.write((hm.getFreeSlot() == -1) ? 1 : 0)
                mplew.write(GameConstants.getInventoryType(itemSearch).getType())
                if GameConstants.getInventoryType(itemSearch) == MapleInventoryType.EQUIP:
                    PacketHelper.addItemInfo(mplew, item.item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getRPSMode(self, mode: int, mesos: int, selection: int, answer: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getRPSMode--------------------")
        mplew.writeShort(SendPacketOpcode.RPS_GAME.getValue())
        mplew.write(mode)
        # switch (mode):
            # case 6:
                if mesos != -1:
                    mplew.writeInt(mesos)
                    break
                break
            # case 8:
                mplew.writeInt(9000019)
                break
            # case 11:
                mplew.write(selection)
                mplew.write(answer)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getSlotUpdate(self, invType: int, newSlots: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getSlotUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_INVENTORY_SLOT.getValue())
        mplew.write(invType)
        mplew.write(newSlots)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMovingPlatforms(self, map: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMovingPlatforms--------------------")
        mplew.writeShort(SendPacketOpcode.MOVE_PLATFORM.getValue())
        mplew.writeInt(map.getPlatforms())
        for (final MapleNodes.MaplePlatform mp : map.getPlatforms())
            mplew.writeMapleAsciiString(mp.name)
            mplew.writeInt(mp.start)
            mplew.writeInt(mp.SN)
            for x in range(mp.SN):
                mplew.writeInt(mp.SN.get(x))
            mplew.writeInt(mp.speed)
            mplew.writeInt(mp.x1)
            mplew.writeInt(mp.x2)
            mplew.writeInt(mp.y1)
            mplew.writeInt(mp.y2)
            mplew.writeInt(mp.x1)
            mplew.writeInt(mp.y1)
            mplew.writeShort(mp.r)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getUpdateEnvironment(self, map: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getUpdateEnvironment--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_ENV.getValue())
        mplew.writeInt(map.getEnvironment())
        for (final Map.Entry<String, Integer> mp : map.getEnvironment().items())
            mplew.writeMapleAsciiString(mp.getKey())
            mplew.writeInt(mp.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendEngagementRequest(self, name: str, cid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendEngagementRequest--------------------")
        mplew.writeShort(SendPacketOpcode.ENGAGE_REQUEST.getValue())
        mplew.write(0)
        mplew.writeMapleAsciiString(name)
        mplew.writeInt(cid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def trembleEffect(self, type: int, delay: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("trembleEffect--------------------")
        mplew.writeShort(SendPacketOpcode.BOSS_ENV.getValue())
        mplew.write(1)
        mplew.write(type)
        mplew.writeInt(delay)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendEngagement(self, msg: int, item: int, male: Any, female: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendEngagement--------------------")
        mplew.writeShort(SendPacketOpcode.ENGAGE_RESULT.getValue())
        mplew.write(msg)
        # switch (msg):
            # case 11:
                mplew.writeInt(0)
                mplew.writeInt(male.getId())
                mplew.writeInt(female.getId())
                mplew.writeShort(1)
                mplew.writeInt(item)
                mplew.writeInt(item)
                mplew.writeAsciiString(male.getName(), 15)
                mplew.writeAsciiString(female.getName(), 15)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def englishQuizMsg(self, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("englishQuizMsg--------------------")
        mplew.writeShort(SendPacketOpcode.ENGLISH_QUIZ.getValue())
        mplew.writeInt(20)
        mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def openBeans(self, beansCount: int, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("openBeans--------------------")
        mplew.writeShort(SendPacketOpcode.BEANS_GAME1.getValue())
        mplew.writeInt(beansCount)
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateBeans(self, cid: int, beansCount: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateBeans--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_BEANS.getValue())
        mplew.writeInt(cid)
        mplew.writeInt(beansCount)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBeans(self, 力度: int, size: int, Pos: int, Type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBeans--------------------")
        mplew.writeShort(SendPacketOpcode.BEANS_GAME2.getValue())
        mplew.writeShort(力度)
        mplew.write(size)
        mplew.writeShort(Pos)
        mplew.writeInt(Type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showCharCash(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showCharCash--------------------")
        mplew.writeShort(SendPacketOpcode.CHAR_CASH.getValue())
        mplew.writeInt(chr.getId())
        mplew.writeInt(chr.getCSPoints(2))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnLove(self, oid: int, itemid: int, name: str, msg: str, pos: Any, ft: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnLove--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_LOVE.getValue())
        mplew.writeInt(oid)
        mplew.writeInt(itemid)
        mplew.writeMapleAsciiString(msg)
        mplew.writeMapleAsciiString(name)
        mplew.writeShort(pos.x)
        mplew.writeShort(ft)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeLove(self, oid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeLove--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_LOVE.getValue())
        mplew.writeInt(oid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def licenseRequest(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("licenseRequest--------------------")
        mplew.writeShort(SendPacketOpcode.LOGIN_STATUS.getValue())
        mplew.write(22)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def licenseResult(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("licenseResult--------------------")
        mplew.writeShort(SendPacketOpcode.LICENSE_RESULT.getValue())
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showForcedEquip(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showForcedEquip--------------------")
        mplew.writeShort(SendPacketOpcode.FORCED_MAP_EQUIP.getValue())
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeTutorialStats(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeTutorialStats--------------------")
        mplew.writeShort(SendPacketOpcode.TEMP_STATS_RESET.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnTutorialSummon(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnTutorialSummon--------------------")
        mplew.writeShort(SendPacketOpcode.TUTORIAL_SUMMON.getValue())
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def requestBuddylistAdd_cidFrom_nameFrom(self, cidFrom: int, nameFrom: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.BUDDYLIST.getValue())
        mplew.write(9)
        mplew.writeInt(cidFrom)
        mplew.writeMapleAsciiString(nameFrom)
        mplew.writeInt(cidFrom)
        mplew.writeAsciiString(StringUtil.getRightPaddedStr(nameFrom, '\0', 13))
        mplew.write(1)
        mplew.write(5)
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeAsciiString(StringUtil.getRightPaddedStr("群未定", '\0', 17))
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendAutoHpPot(self, itemId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.AUTO_HP_POT.getValue())
        mplew.writeInt(itemId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendAutoMpPot(self, itemId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.AUTO_MP_POT.getValue())
        mplew.writeInt(itemId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def testPacket(self, testmsg: bytes) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.write(testmsg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAriantScore(self, players: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.ARIANT_SCORE_UPDATE.getValue())
        mplew.write(players == 0 ? 0 : 1)
        if not players == 0:
            for i in players:
                mplew.writeMapleAsciiString(i.getName())
                mplew.writeInt(i.getAriantScore())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateAriantScore_name_score_empty(self, name: str, score: int, empty: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.ARIANT_SCORE_UPDATE.getValue())
        mplew.write(empty ? 0 : 1)
        if not empty:
            mplew.writeMapleAsciiString(name)
            mplew.writeInt(score)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def modifyInventory(self, updateTick: bool, mod: Any) -> Any:
        return modifyInventory(updateTick, Collections.singletonList(mod))

    def modifyInventory_updateTick_mods(self, updateTick: bool, mods: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(updateTick ? 1 : 0)
        mplew.write(mods)
        addMovement = -1
        for mod in mods:
            mplew.write(mod.getMode())
            mplew.write(mod.getInventoryType())
            mplew.writeShort((mod.getMode() == 2) ? mod.getOldPosition() : mod.getPosition())
            # switch (mod.getMode()):
                # case 0:
                    PacketHelper.addItemInfo(mplew, mod.getItem(), True, False)
                    break
                # case 1:
                    mplew.writeShort(mod.getQuantity())
                    break
                # case 2:
                    mplew.writeShort(mod.getPosition())
                    if mod.getPosition() < 0 or mod.getOldPosition() < 0:
                        addMovement = ((mod.getOldPosition() < 0) ? 1 : 2)
                        break
                    break
                # case 3:
                    if mod.getPosition() < 0:
                        addMovement = 2
                        break
                    break
            mod.clear()
        if addMovement > -1:
            mplew.write(addMovement)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def petAutoHP(self, itemId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.AUTO_HP_POT.getValue())
        mplew.writeInt(itemId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def petAutoMP(self, itemId: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.AUTO_MP_POT.getValue())
        mplew.writeInt(itemId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def catchMob(self, mobid: int, itemid: int, success: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(80)
        mplew.write(success)
        mplew.writeInt(itemid)
        mplew.writeInt(mobid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def serverMessagePopUp(self, message: str) -> Any:
        return serverMessage(1, 0, message, False)

    def updateEquipSlot(self, item: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateEquipSlot--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(0)
        mplew.write(HexTool.getByteArrayFromHexString("02 03 01"))
        mplew.writeShort(item.getPosition())
        mplew.write(0)
        mplew.write(item.getType())
        mplew.writeShort(item.getPosition())
        PacketHelper.addItemInfo(mplew, item, True, True)
        mplew.writeMapleAsciiString("wat")
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelBuffMONSTERS(self, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelBuffMONSTERS--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_BUFF.getValue())
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 01 00"))
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 00 00"))
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelForeignBuffMONSTERS(self, cid: int, statups: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelForeignBuffA--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_FOREIGN_BUFF.getValue())
        mplew.writeInt(cid)
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 01 00"))
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 00 00"))
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def displayGuide(self, guide: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.SUMMON_HINT_MSG.getValue())
        mplew.write(1)
        mplew.writeInt(guide)
        mplew.writeInt(12000)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def returnSerialNumber(self) -> str:
        cpu = getCPUSerial()
        disk = getHardDiskSerialNumber("C")
        newdisk = int(disk)
        s = cpu + newdisk
        newStr = s[8:s.__len__(])
        return newStr

    def getCPUSerial(self) -> str:
        result = ""
        try:
            file = File.createTempFile("tmp", ".vbs")
            file.deleteOnExit()
            fw = FileWriter(file)
            vbs = "Set objWMIService = GetObject(\"winmgmts:  # ./root/cimv2\")\nSet colItems = objWMIService.ExecQuery _ \n   (\"Select * from Win32_Processor\") \nFor Each objItem in colItems \n    Wscript.Echo objItem.ProcessorId \n    exit for  ' do the first cpu only! \nNext \n"
            fw.write(vbs)
            fw.close()
            p = Runtime.getRuntime().exec("cscript  # NoLogo " + file.getPath())
            input = BufferedReader(InputStreamReader(p.getInputStream()))
            line = None
            while (line = input.readLine()) is not None:
                result += line
            input.close()
            file.delete()
        except IOError as e:
            e.fillInStackTrace()
        if result.strip() < 1 or result is None:
            result = "无CPU_ID被读取"
        return result.strip()

    def getHardDiskSerialNumber(self, drive: str) -> str:
        result = ""
        try:
            file = File.createTempFile("realhowto", ".vbs")
            file.deleteOnExit()
            fw = FileWriter(file)
            vbs = "Set objFSO = CreateObject(\"Scripting.FileSystemObject\")\nSet colDrives = objFSO.Drives\nSet objDrive = colDrives.item(\"" + drive + "\")\nWscript.Echo objDrive.SerialNumber"
            fw.write(vbs)
            fw.close()
            p = Runtime.getRuntime().exec("cscript  # NoLogo " + file.getPath())
            input = BufferedReader(InputStreamReader(p.getInputStream()))
            line = None
            while (line = input.readLine()) is not None:
                result += line
            input.close()
        except IOException as ex:
            pass
        return result.strip()

    def isshowPacket(self) -> bool:
        return False

    @staticmethod
    def openWeb(web: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("openWeb--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_WEB.getValue())
        mplew.writeMapleAsciiString(web)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def LieDetectorResponse(self, msg: int) -> Any:
        return LieDetectorResponse(msg, 0)

    def LieDetectorResponse_msg_msg2(self, msg: int, msg2: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.LIE_DETECTOR.getValue())
        mplew.write(msg)
        mplew.write(msg2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendLieDetector(self, image: bytes, attempt: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.LIE_DETECTOR.getValue())
        mplew.write(9)
        mplew.write(1)
        mplew.write(1)
        mplew.write(attempt - 1)
        if image is None:
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(len(image))
        mplew.write(image)
        print("调用: " + Throwable().getStackTrace()[0] + " 测谎仪图片大小: " + len(image) + " 换图次数: " + (attempt - 1))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shenlong(self, i: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(i)
        mplew.write(HexTool.getByteArrayFromHexString("DC 05 00 00 90 5 01 00 DC 05 00 00 9B 00 00 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shenlong2(self, i: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(i)
        mplew.write(HexTool.getByteArrayFromHexString("02 CB 06 00 00 FB 44 00 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def DragonBall1(self, i: int, Zhaohuan: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeInt(0)
        mplew.write(1)
        if not Zhaohuan:
            mplew.writeShort(0)
            mplew.writeShort(i)
            mplew.writeShort(0)
        else:
            mplew.writeLong(512)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_杀怪排行榜(self, npcid: int, rs: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.GUILD_OPERATION.getValue())
        mplew.write(73)
        mplew.writeInt(npcid)
        if not rs.last():
            mplew.writeInt(0)
            return mplew.getPacket()
        mplew.writeInt(rs.getRow())
        rs.beforeFirst()
        while rs.next():
            mplew.writeMapleAsciiString(rs.getString("name"))
            mplew.writeInt(rs.getInt("shaguai"))
            mplew.writeInt(rs.getInt("str"))
            mplew.writeInt(rs.getInt("dex"))
            mplew.writeInt(rs.getInt("int"))
            mplew.writeInt(rs.getInt("luk"))
        return mplew.getPacket()

    def getCY1(self, npc: int, talk: str, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.write(13)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.write(type)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeMapleAsciiString(talk)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getCY2(self, npc: int, talk: str, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.NPC_TALK.getValue())
        mplew.write(4)
        mplew.writeInt(npc)
        mplew.write(16)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.write(type)
        mplew.writeShort(0)
        mplew.write(0)
        mplew.writeMapleAsciiString(talk)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def PVPdamagePlayer(self, chrId: int, type: int, monsteridfrom: int, damage: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.DAMAGE_PLAYER.getValue())
        mplew.writeInt(chrId)
        mplew.write(type)
        mplew.writeInt(damage)
        mplew.writeInt(monsteridfrom)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.writeInt(damage)
        return mplew.getPacket()

    def testCombo(self, value: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("testCombo--------------------")
        mplew.writeShort(SendPacketOpcode.ARAN_COMBO.getValue())
        mplew.writeInt(value)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR("testCombo-864：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getInventoryStatus(self) -> Any:
        return modifyInventory(False, Collections.EMPTY_LIST)

