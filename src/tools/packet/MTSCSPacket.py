"""
MTSCSPacket - Converted from Java source
Original: tools/packet/MTSCSPacket.java
Package: tools.packet
"""

from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql
import time

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillEntry import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from server.CashItemFactory import *  # TODO: import specific classes
# from server.CashItemInfo import *  # TODO: import specific classes
# from server.CashShop import *  # TODO: import specific classes
# from server.MTSStorage import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.KoreanDateUtil import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class MTSCSPacket:
    """
    Class MTSCSPacket
    """

    # Static initializer
    # MTSCSPacket.warpCS = HexTool.getByteArrayFromHexString("00 00 00 63 00 74 00 65 00 64 00 2 00 32 00 00 00 00 00 02 00 11 00 AD 01 08 06 02 00 00 00 33 00 00 00 05 00 13 00 AF 00 08 06 A0 01 14 00 30 E1 7B 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 18 00 B2 01 08 06 02 00 00 00 33 00 00 00 08 00 1A 00 B4 00 0A 06 B8 01 14 00 A8 10 88 06 69 00 6C 00 6C 00 2 00 39 00 30 00 30 00 31 00")
    # MTSCSPacket.CHAR_INFO_MAGIC = new byte[] { -1, -55, -102, 59 }


    @staticmethod
    def warpCS(c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        chr = c.getPlayer()
        if ServerConstants.调试输出封包:
            print("warpCS--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPEN.getValue())
        mplew.writeLong(-1)
        mplew.write(0)
        PacketHelper.addCharStats(mplew, chr)
        mplew.write(20)
        mplew.write(0)
        mplew.writeInt(chr.getMeso())
        mplew.writeInt(chr.getId())
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.write(chr.getInventory(MapleInventoryType.EQUIP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.USE).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.SETUP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.ETC).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.CASH).getSlotLimit())
        mplew.writeLong(PacketHelper.getTime(int(time.time() * 1000)))
        iv = chr.getInventory(MapleInventoryType.EQUIPPED)
        equippedC = iv.list()
        equipped = [])
        for item in equippedC:
            equipped.add(item)
        Collections.sort(equipped)
        for item2 in equipped:
            if item2.getPosition() < 0 and item2.getPosition() > -100:
                PacketHelper.addItemInfo(mplew, item2, False, False)
        mplew.write(0)
        for item2 in equipped:
            if item2.getPosition() <= -100 and item2.getPosition() > -1000:
                PacketHelper.addItemInfo(mplew, item2, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.EQUIP)
        for item in iv.list():
            PacketHelper.addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.USE)
        for item in iv.list():
            PacketHelper.addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.SETUP)
        for item in iv.list():
            PacketHelper.addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.ETC)
        for item in iv.list():
            PacketHelper.addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.CASH)
        for item in iv.list():
            PacketHelper.addItemInfo(mplew, item, False, False)
        mplew.write(0)
        skills = chr.getSkills()
        mplew.writeShort(skills)
        for (final Map.Entry<ISkill, SkillEntry> skill : skills.items())
            mplew.writeInt(skill.getKey().getId())
            mplew.writeInt(skill.getValue().skillevel)
            if skill.getKey().isFourthJob():
                mplew.writeInt(skill.getValue().masterlevel)
        mplew.writeShort(0)
        mplew.writeShort(3)
        mplew.writeInt(662990)
        mplew.write(HexTool.getByteArrayFromHexString("5A 5A 5A 5A 45 46 47 48 49 5A B0 1 01 00 34 95 08 00 00 11 00 F0 03 00 4 CE 43 44 63 CA 01 08 04 00 05 05 49 70 FD C9 01 F1 03 00 07 0B 20 44 63 CA 01 09 04 00 E6 FA 4E 70 FD C9 01 F2 03 80 F7 05 23 44 63 CA 01 0A 04 00 F4 21 56 70 FD C9 01 F3 03 80 51 68 25 44 63 CA 01 0B 04 00 F0 C7 CB E1 00 CA 01 39 20 00 7 C1 6 C3 5A CA 01 F4 03 80 AB CA 27 44 63 CA 01 0C 04 00 DD 95 0A 44 63 CA 01 FC 03 80 6A FA 47 44 63 CA 01 B0 1 80 28 6 6 80 63 CA 01 F5 03 00 9C C5 2A 44 63 CA 01 F6 03 00 F6 27 2 44 63 CA 01 98 12 80 C4 5C 4A 44 63 CA 01 F7 03 80 40 85 32 44 63 CA 01"))
        mplew.writeLong(0)
        for i in range(15):
            mplew.write(MTSCSPacket.CHAR_INFO_MAGIC)
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"))
        mplew.writeMapleAsciiString(chr.getClient().getAccountName())
        mplew.write(HexTool.getByteArrayFromHexString("46 00 00 00 07 A5 9B 00 08 A5 9B 00 09 A5 9B 00 0A A5 9B 00 0B A5 9B 00 0C A5 9B 00 0 A5 9B 00 0E A5 9B 00 0 A5 9B 00 10 A5 9B 00 11 A5 9B 00 12 A5 9B 00 13 A5 9B 00 14 A5 9B 00 15 A5 9B 00 16 A5 9B 00 17 A5 9B 00 18 A5 9B 00 19 A5 9B 00 1A A5 9B 00 1B A5 9B 00 1C A5 9B 00 1 A5 9B 00 1E A5 9B 00 1 A5 9B 00 20 A5 9B 00 21 A5 9B 00 22 A5 9B 00 23 A5 9B 00 24 A5 9B 00 25 A5 9B 00 26 A5 9B 00 27 A5 9B 00 28 A5 9B 00 29 A5 9B 00 2A A5 9B 00 2B A5 9B 00 2C A5 9B 00 2 A5 9B 00 2E A5 9B 00 2 A5 9B 00 30 A5 9B 00 31 A5 9B 00 32 A5 9B 00 33 A5 9B 00 34 A5 9B 00 35 A5 9B 00 36 A5 9B 00 37 A5 9B 00 38 A5 9B 00 39 A5 9B 00 3A A5 9B 00 3B A5 9B 00 3C A5 9B 00 3 A5 9B 00 3E A5 9B 00 3 A5 9B 00 40 A5 9B 00 41 A5 9B 00 42 A5 9B 00 43 A5 9B 00 44 A5 9B 00 45 A5 9B 00 46 A5 9B 00 47 A5 9B 00 48 A5 9B 00 49 A5 9B 00 4A A5 9B 00 4B A5 9B 00 4C A5 9B 00"))
        mplew.writeShort(0)
        mplew.writeZeroBytes(123)
        itemz = CashItemFactory.getInstance().getBestItems()
        for j in range(1, = 8):
            for k in range(= 1):
                for item3 in range(len(itemz)):
                    mplew.writeInt(j)
                    mplew.writeInt(k)
                    mplew.writeInt(itemz[item3])
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR("warpCS-201：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def warpCSS(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        chr = c.getPlayer()
        if ServerConstants.调试输出封包:
            print("warpCS--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPEN.getValue())
        mplew.writeLong(-1)
        mplew.write(0)
        PacketHelper.addCharStats(mplew, chr)
        mplew.write(20)
        mplew.write(0)
        mplew.writeInt(0)
        mplew.writeInt(chr.getId())
        mplew.writeInt(0)
        mplew.writeInt(0)
        mplew.write(chr.getInventory(MapleInventoryType.EQUIP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.USE).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.SETUP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.ETC).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.CASH).getSlotLimit())
        mplew.writeLong(0)
        mplew.write(0)
        mplew.write(0)
        mplew.write(0)
        mplew.write(0)
        mplew.write(0)
        mplew.write(0)
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeShort(0)
        mplew.writeShort(3)
        mplew.writeInt(662990)
        mplew.write(HexTool.getByteArrayFromHexString("5A 5A 5A 5A 45 46 47 48 49 5A B0 1 01 00 34 95 08 00 00 11 00 F0 03 00 4 CE 43 44 63 CA 01 08 04 00 05 05 49 70 FD C9 01 F1 03 00 07 0B 20 44 63 CA 01 09 04 00 E6 FA 4E 70 FD C9 01 F2 03 80 F7 05 23 44 63 CA 01 0A 04 00 F4 21 56 70 FD C9 01 F3 03 80 51 68 25 44 63 CA 01 0B 04 00 F0 C7 CB E1 00 CA 01 39 20 00 7 C1 6 C3 5A CA 01 F4 03 80 AB CA 27 44 63 CA 01 0C 04 00 DD 95 0A 44 63 CA 01 FC 03 80 6A FA 47 44 63 CA 01 B0 1 80 28 6 6 80 63 CA 01 F5 03 00 9C C5 2A 44 63 CA 01 F6 03 00 F6 27 2 44 63 CA 01 98 12 80 C4 5C 4A 44 63 CA 01 F7 03 80 40 85 32 44 63 CA 01"))
        mplew.writeLong(0)
        for i in range(15):
            mplew.write(MTSCSPacket.CHAR_INFO_MAGIC)
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"))
        mplew.writeMapleAsciiString(chr.getClient().getAccountName())
        mplew.write(HexTool.getByteArrayFromHexString("46 00 00 00 07 A5 9B 00 08 A5 9B 00 09 A5 9B 00 0A A5 9B 00 0B A5 9B 00 0C A5 9B 00 0 A5 9B 00 0E A5 9B 00 0 A5 9B 00 10 A5 9B 00 11 A5 9B 00 12 A5 9B 00 13 A5 9B 00 14 A5 9B 00 15 A5 9B 00 16 A5 9B 00 17 A5 9B 00 18 A5 9B 00 19 A5 9B 00 1A A5 9B 00 1B A5 9B 00 1C A5 9B 00 1 A5 9B 00 1E A5 9B 00 1 A5 9B 00 20 A5 9B 00 21 A5 9B 00 22 A5 9B 00 23 A5 9B 00 24 A5 9B 00 25 A5 9B 00 26 A5 9B 00 27 A5 9B 00 28 A5 9B 00 29 A5 9B 00 2A A5 9B 00 2B A5 9B 00 2C A5 9B 00 2 A5 9B 00 2E A5 9B 00 2 A5 9B 00 30 A5 9B 00 31 A5 9B 00 32 A5 9B 00 33 A5 9B 00 34 A5 9B 00 35 A5 9B 00 36 A5 9B 00 37 A5 9B 00 38 A5 9B 00 39 A5 9B 00 3A A5 9B 00 3B A5 9B 00 3C A5 9B 00 3 A5 9B 00 3E A5 9B 00 3 A5 9B 00 40 A5 9B 00 41 A5 9B 00 42 A5 9B 00 43 A5 9B 00 44 A5 9B 00 45 A5 9B 00 46 A5 9B 00 47 A5 9B 00 48 A5 9B 00 49 A5 9B 00 4A A5 9B 00 4B A5 9B 00 4C A5 9B 00"))
        final Collection<CashItemInfo.CashModInfo> cmi = CashItemFactory.getInstance().getAllModInfo()
        mplew.writeShort(cmi)
        for (final CashItemInfo.CashModInfo cm : cmi)
            addModCashItemInfo(mplew, cm)
        mplew.writeZeroBytes(123)
        itemz = CashItemFactory.getInstance().getBestItems()
        for j in range(1, = 8):
            for k in range(= 1):
                for item in range(len(itemz)):
                    mplew.writeInt(j)
                    mplew.writeInt(k)
                    mplew.writeInt(itemz[item])
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addModCashItemInfo(self, mplew: Any, item: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addModCashItemInfo--------------------")
        flags = item.flags
        mplew.writeInt(item.sn)
        mplew.writeInt(flags)
        if (flags & 0x1) != 0x0:
            mplew.writeInt(item.itemid)
        if (flags & 0x2) != 0x0:
            mplew.writeShort(item.count)
        if (flags & 0x10) != 0x0:
            mplew.write(item.priority)
        if (flags & 0x4) != 0x0:
            mplew.writeInt(item.discountPrice)
        if (flags & 0x20) != 0x0:
            mplew.writeShort(item.period)
        if (flags & 0x200) != 0x0:
            mplew.write(item.gender)
        if (flags & 0x400) != 0x0:
            mplew.write(item.showUp ? 1 : 0)
        if (flags & 0x800) != 0x0:
            mplew.write(item.mark)
        if (flags & 0x10000) != 0x0:
            pack = CashItemFactory.getInstance().getPackageItems(item.sn)
            if pack is None:
                mplew.write(0)
            else:
                mplew.write(pack)
                for i in range(pack):
                    mplew.writeInt(pack.get(i).getSN())

    def sendBlockedMessage(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendBlockedMessage--------------------")
        mplew.writeShort(SendPacketOpcode.BLOCK_MSG.getValue())
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def playCashSong(self, itemid: int, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("playCashSong--------------------")
        mplew.writeShort(SendPacketOpcode.CASH_SONG.getValue())
        mplew.writeInt(itemid)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_show塔罗牌(self, name: str, otherName: str, love: int, cardId: int, commentId: int) -> Any:
        if ServerConstants.调试输出封包:
            print("playCashSong--------------------")
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.SHOW_PREDICT_CARD.getValue())
        mplew.writeMapleAsciiString(name)
        mplew.writeMapleAsciiString(otherName)
        mplew.writeInt(love)
        mplew.writeInt(cardId)
        mplew.writeInt(commentId)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def useCharm(self, charmsleft: int, daysleft: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("useCharm--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(6)
        mplew.write(1)
        mplew.write(charmsleft)
        mplew.write(daysleft)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def useWheel(self, charmsleft: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("useWheel--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(21)
        mplew.writeLong(charmsleft)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def itemExpired(self, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("itemExpired--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(2)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def ViciousHammer(self, start: bool, hammered: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("ViciousHammer--------------------")
        mplew.writeShort(SendPacketOpcode.VICIOUS_HAMMER.getValue())
        if start:
            mplew.write(49)
            mplew.writeInt(0)
            mplew.writeInt(hammered)
        else:
            mplew.write(53)
            mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changePetFlag(self, uniqueId: int, added: bool, flagAdded: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changePetFlag--------------------")
        mplew.writeShort(SendPacketOpcode.PET_FLAG_CHANGE.getValue())
        mplew.writeLong(uniqueId)
        mplew.write(added ? 1 : 0)
        mplew.writeShort(flagAdded)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changePetName(self, chr: Any, newname: str, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changePetName--------------------")
        mplew.writeShort(SendPacketOpcode.PET_NAMECHANGE.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(0)
        mplew.writeMapleAsciiString(newname)
        mplew.write(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showNotes(self, notes: Any, count: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showNotes--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_NOTES.getValue())
        mplew.write(3)
        mplew.write(count)
        for i in range(count):
            mplew.writeInt(notes.getInt("id"))
            mplew.writeMapleAsciiString(notes.getString("from"))
            mplew.writeMapleAsciiString(notes.getString("message"))
            mplew.writeLong(PacketHelper.getKoreanTimestamp(notes.getLong("timestamp")))
            mplew.write(notes.getInt("gift"))
            notes.next()
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def useChalkboard(self, charid: int, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("useChalkboard--------------------")
        mplew.writeShort(SendPacketOpcode.CHALKBOARD.getValue())
        mplew.writeInt(charid)
        if msg is None or msg <= 0:
            mplew.write(0)
        else:
            mplew.write(1)
            mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTrockRefresh(self, chr: Any, vip: bool, delete: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTrockRefresh--------------------")
        mplew.writeShort(SendPacketOpcode.TROCK_LOCATIONS.getValue())
        mplew.write(delete ? 2 : 3)
        mplew.write(vip ? 1 : 0)
        if vip:
            map = chr.getRocks()
            for i in range(10):
                mplew.writeInt(map[i])
        else:
            map = chr.getRegRocks()
            for i in range(5):
                mplew.writeInt(map[i])
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendWishList(self, chr: Any, update: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendWishList--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(70)
        con = DatabaseConnection.getConnection()
        i = 10
        try:
            ps = con.prepareStatement("SELECT sn FROM wishlist WHERE characterid = ? LIMIT 10")
            ps.setInt(1, chr.getAccountID())
            rs = ps.executeQuery()
            while rs.next():
                mplew.writeInt(rs.getInt("sn"))
                i -= 1
            rs.close()
            ps.close()
        except Exception as se:
            print("Error getting wishlist data:" + se)
        while i > 0:
            mplew.writeInt(0)
            i -= 1
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showCashInventory(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(66)
        mci = c.getPlayer().getCashInventory()
        mplew.writeShort(mci.getItemsSize())
        for itemz in mci.getInventory():
            addCashItemInfo(mplew, itemz, c.getAccID(), 0)
        mplew.writeShort(c.getPlayer().getStorage().getSlots())
        mplew.writeShort(c.getCharacterSlots())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showNXMapleTokens(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showNXMapleTokens--------------------")
        mplew.writeShort(SendPacketOpcode.CS_UPDATE.getValue())
        mplew.writeInt(chr.getCSPoints(1))
        mplew.writeInt(chr.getCSPoints(2))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBoughtCSPackage(self, ccc: dict, accid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBoughtCSPackage--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(126)
        mplew.write(ccc)
        for (final Map.Entry<Integer, IItem> sn : ccc.items())
            addCashItemInfo(mplew, sn.getValue(), accid, sn.getKey())
        mplew.writeShort(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBoughtCSItem(self, itemid: int, sn: int, uniqueid: int, accid: int, quantity: int, giftFrom: str, expire: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBoughtCSItemA--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(76)
        addCashItemInfo(mplew, uniqueid, accid, itemid, sn, quantity, giftFrom, expire)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBoughtCSItem_item_sn_accid(self, item: Any, sn: int, accid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBoughtCSItemB--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(76)
        addCashItemInfo(mplew, item, accid, sn)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addCashItemInfo(self, mplew: Any, item: Any, accId: int, sn: int) -> None:
        if ServerConstants.调试输出封包:
            print("addCashItemInfoA--------------------")
        addCashItemInfo(mplew, item, accId, sn, True)

    def addCashItemInfo_mplew_item_accId_sn_isFirst(self, mplew: Any, item: Any, accId: int, sn: int, isFirst: bool) -> None:
        if ServerConstants.调试输出封包:
            print("addCashItemInfoB--------------------")
        addCashItemInfo(mplew, item.getUniqueId(), accId, item.getItemId(), sn, item.getQuantity(), item.getGiftFrom(), item.getExpiration(), isFirst)

    def addCashItemInfo_mplew_uniqueid_accId_itemid_sn_quantity_sender_expire(self, mplew: Any, uniqueid: int, accId: int, itemid: int, sn: int, quantity: int, sender: str, expire: int) -> None:
        if ServerConstants.调试输出封包:
            print("addCashItemInfoC--------------------")
        addCashItemInfo(mplew, uniqueid, accId, itemid, sn, quantity, sender, expire, True)

    def addCashItemInfo_mplew_uniqueid_accId_itemid_sn_quantity_sender_expire_isFirst(self, mplew: Any, uniqueid: int, accId: int, itemid: int, sn: int, quantity: int, sender: str, expire: int, isFirst: bool) -> None:
        if ServerConstants.调试输出封包:
            print("addCashItemInfoD--------------------")
        mplew.writeLong((uniqueid > 0) ? (uniqueid) : 0)
        mplew.writeLong(accId)
        mplew.writeInt(itemid)
        mplew.writeInt(isFirst ? sn : 0)
        mplew.writeShort(quantity)
        mplew.writeAsciiString(sender, 13)
        PacketHelper.addExpirationTime(mplew, expire)
        mplew.writeLong(0)

    def showBoughtCSQuestItem(self, price: int, quantity: int, position: int, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBoughtCSQuestItem--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(111)
        mplew.writeInt(price)
        mplew.writeShort(quantity)
        mplew.writeShort(position)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendCSFail(self, err: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendCSFail--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(106)
        mplew.write(err)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showCouponRedeemedItem(self, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showCouponRedeemedItemA--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.writeShort(60)
        mplew.writeInt(0)
        mplew.writeInt(1)
        mplew.writeShort(1)
        mplew.writeShort(26)
        mplew.writeInt(itemid)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showCouponRedeemedItem_items_mesos_maplePoints_c(self, items: dict, mesos: int, maplePoints: int, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showCouponRedeemedItemB--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(60)
        mplew.write(items)
        for (final Map.Entry<Integer, IItem> item : items.items())
            addCashItemInfo(mplew, item.getValue(), c.getAccID(), item.getKey())
        mplew.writeLong(maplePoints)
        mplew.writeInt(mesos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def enableCSorMTS(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("enableCSorMTS--------------------")
        mplew.write(HexTool.getByteArrayFromHexString("15 00 01 00 00 00 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def enableCSUse(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("enableCSUse--------------------")
        mplew.writeShort(18)
        mplew.writeInt(0)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getCSInventory(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(66)
        mci = c.getPlayer().getCashInventory()
        mplew.writeShort(mci.getItemsSize())
        for itemz in mci.getInventory():
            sn = None
            try:
                sn = CashItemFactory.getInstance().getSnFromId(itemz.getItemId())
            except Exception as ex:
                pass
            mplew.writeLong(itemz.getUniqueId())
            mplew.writeLong(c.getAccID())
            mplew.writeInt(itemz.getItemId())
            mplew.writeInt((sn is None) ? 0 : (sn))
            mplew.writeShort(itemz.getQuantity())
            mplew.writeAsciiString(itemz.getGiftFrom())
            i = itemz.getGiftFrom().encode("utf-8").length
            while i < 13:
                mplew.write(0)
            PacketHelper.addExpirationTime(mplew, itemz.getExpiration())
            mplew.writeLong(0)
        mplew.writeShort(4)
        mplew.writeShort(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getCSGifts(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getCSGifts--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(68)
        mci = c.getPlayer().getCashInventory().loadGifts()
        mplew.writeShort(mci)
        for mcz in mci:
            mplew.writeLong(mcz.getLeft().getUniqueId())
            mplew.writeInt(mcz.getLeft().getItemId())
            mplew.writeAsciiString(mcz.getLeft().getGiftFrom(), 13)
            mplew.writeAsciiString(mcz.getRight(), 73)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cashItemExpired(self, uniqueid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cashItemExpired--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(82)
        mplew.writeLong(uniqueid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendGift(self, itemid: int, quantity: int, receiver: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendGift--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(83)
        mplew.writeMapleAsciiString(receiver)
        mplew.writeInt(itemid)
        mplew.writeShort(quantity)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def increasedInvSlots(self, inv: int, slots: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("increasedInvSlots--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(101)
        mplew.write(inv)
        mplew.writeShort(slots)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def increasedStorageSlots(self, slots: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("increasedStorageSlots--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(103)
        mplew.writeShort(slots)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def confirmToCSInventory(self, item: Any, accId: int, sn: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("confirmToCSInventory--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(95)
        mplew.writeLong(item.getUniqueId())
        mplew.writeLong(accId)
        mplew.writeInt(item.getItemId())
        mplew.writeInt(sn)
        mplew.writeShort(item.getQuantity())
        mplew.writeAsciiString(item.getGiftFrom(), 13)
        PacketHelper.addExpirationTime(mplew, item.getExpiration())
        mplew.writeLong(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def confirmFromCSInventory(self, item: Any, pos: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("confirmFromCSInventory--------------------")
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.write(93)
        mplew.writeShort(pos)
        PacketHelper.addItemInfo(mplew, item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendMesobagFailed(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendMesobagFailed--------------------")
        mplew.writeShort(SendPacketOpcode.MESOBAG_FAILURE.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendMesobagSuccess(self, mesos: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendMesobagSuccess--------------------")
        mplew.writeShort(SendPacketOpcode.MESOBAG_SUCCESS.getValue())
        mplew.writeInt(mesos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def startMTS(self, chr: Any, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("startMTS--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPEN.getValue())
        PacketHelper.addCharacterInfo(mplew, chr)
        mplew.writeMapleAsciiString(c.getAccountName())
        mplew.writeInt(ServerConstants.MTS_MESO)
        mplew.writeInt(ServerConstants.MTS_TAX)
        mplew.writeInt(ServerConstants.MTS_BASE)
        mplew.writeInt(24)
        mplew.writeInt(168)
        mplew.writeLong(PacketHelper.getTime(int(time.time() * 1000)))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendMTS(self, items: list, tab: int, type: int, page: int, pages: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendMTS--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(21)
        mplew.writeInt(pages * 10)
        mplew.writeInt(items)
        mplew.writeInt(tab)
        mplew.writeInt(type)
        mplew.writeInt(page)
        mplew.write(1)
        mplew.write(1)
        for (final MTSStorage.MTSItemInfo item : items)
            addMTSItemInfo(mplew, item)
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMTSCash(self, p: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showMTSCash--------------------")
        mplew.writeShort(SendPacketOpcode.GET_MTS_TOKENS.getValue())
        mplew.writeInt(p.getCSPoints(2))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSWantedListingOver(self, nx: int, items: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSWantedListingOver--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(61)
        mplew.writeInt(nx)
        mplew.writeInt(items)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSConfirmSell(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSConfirmSell--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(29)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSFailSell(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSFailSell--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(30)
        mplew.write(66)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSConfirmBuy(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSConfirmBuy--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(51)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSFailBuy(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSFailBuy--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(52)
        mplew.write(66)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSConfirmCancel(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSConfirmCancel--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(37)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSFailCancel(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSFailCancel--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(38)
        mplew.write(66)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMTSConfirmTransfer(self, quantity: int, pos: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMTSConfirmTransfer--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(39)
        mplew.writeInt(quantity)
        mplew.writeInt(pos)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addMTSItemInfo(self, mplew: Any, item: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addMTSItemInfo--------------------")
        PacketHelper.addItemInfo(mplew, item.getItem(), True, True)
        mplew.writeInt(item.getId())
        mplew.writeInt(item.getTaxes())
        mplew.writeInt(item.getPrice())
        mplew.writeInt(0)
        mplew.writeInt(KoreanDateUtil.getQuestTimestamp(item.getEndingDate()))
        mplew.writeInt(KoreanDateUtil.getQuestTimestamp(item.getEndingDate()))
        mplew.writeMapleAsciiString(item.getSeller())
        mplew.writeMapleAsciiString(item.getSeller())
        mplew.writeZeroBytes(28)

    def getNotYetSoldInv(self, items: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getNotYetSoldInv--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(35)
        mplew.writeInt(items)
        for (final MTSStorage.MTSItemInfo item : items)
            addMTSItemInfo(mplew, item)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTransferInventory(self, items: list, changed: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTransferInventory--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        mplew.write(33)
        mplew.writeInt(items)
        i = 0
        for item in items:
            PacketHelper.addItemInfo(mplew, item, True, True)
            mplew.writeInt(Integer.MAX_VALUE - i)
            mplew.writeInt(110)
            mplew.writeInt(1011)
            mplew.writeZeroBytes(48)
            i += 1
        mplew.writeInt(-47 + i - 1)
        mplew.write(changed ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addToCartMessage(self, fail: bool, remove: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addToCartMessage--------------------")
        mplew.writeShort(SendPacketOpcode.MTS_OPERATION.getValue())
        if remove:
            if fail:
                mplew.write(44)
                mplew.writeInt(-1)
            else:
                mplew.write(43)
        elif fail:
            mplew.write(42)
            mplew.writeInt(-1)
        else:
            mplew.write(41)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def translated_商城送礼物(self, itemid: int, quantity: int, receiver: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.CS_OPERATION.getValue())
        mplew.writeMapleAsciiString(receiver)
        mplew.writeInt(itemid)
        mplew.writeShort(quantity)
        return mplew.getPacket()

