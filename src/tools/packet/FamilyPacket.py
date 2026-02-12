"""
FamilyPacket - Converted from Java source
Original: tools/packet/FamilyPacket.java
Package: tools.packet
"""

from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamily import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyBuff import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyCharacter import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class FamilyPacket:
    """
    Class FamilyPacket
    """


    def getFamilyData(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFamilyData--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY.getValue())
        final List<MapleFamilyBuff.MapleFamilyBuffEntry> entries = MapleFamilyBuff.getBuffEntry()
        mplew.writeInt(entries)
        for (final MapleFamilyBuff.MapleFamilyBuffEntry entry : entries)
            mplew.write(entry.type)
            mplew.writeInt(entry.rep * 100)
            mplew.writeInt(entry.count)
            mplew.writeMapleAsciiString(entry.name)
            mplew.writeMapleAsciiString(entry.desc)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeRep(self, r: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeRep--------------------")
        mplew.writeShort(SendPacketOpcode.REP_INCREASE.getValue())
        mplew.writeInt(r)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getFamilyInfo(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFamilyInfo--------------------")
        mplew.writeShort(SendPacketOpcode.OPEN_FAMILY.getValue())
        mplew.writeInt(chr.getCurrentRep())
        mplew.writeInt(chr.getTotalRep())
        mplew.writeInt(chr.getTotalRep())
        mplew.writeShort(chr.getNoJuniors())
        mplew.writeShort(2)
        mplew.writeShort(chr.getNoJuniors())
        family = World.Family.getFamily(chr.getFamilyId())
        if family is not None:
            mplew.writeInt(family.getLeaderId())
            mplew.writeMapleAsciiString(family.getLeaderName())
            mplew.writeMapleAsciiString(family.getNotice())
        else:
            mplew.writeLong(0)
        b = chr.usedBuffs()
        mplew.writeInt(b)
        for ii in b:
            mplew.writeInt(ii.getLeft())
            mplew.writeInt(ii.getRight())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addFamilyCharInfo(self, ldr: Any, mplew: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addFamilyCharInfo--------------------")
        mplew.writeInt(ldr.getId())
        mplew.writeInt(ldr.getSeniorId())
        mplew.writeShort(ldr.getJobId())
        mplew.write(ldr.getLevel())
        mplew.write(ldr.isOnline() ? 1 : 0)
        mplew.writeInt(ldr.getCurrentRep())
        mplew.writeInt(ldr.getTotalRep())
        mplew.writeInt(ldr.getTotalRep())
        mplew.writeInt(ldr.getTotalRep())
        mplew.writeLong(max(ldr.getChannel(), 0))
        mplew.writeMapleAsciiString(ldr.getName())

    def getFamilyPedigree(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getFamilyPedigree--------------------")
        mplew.writeShort(SendPacketOpcode.SEND_PEDIGREE.getValue())
        mplew.writeInt(chr.getId())
        family = World.Family.getFamily(chr.getFamilyId())
        descendants = 2
        gens = 0
        generations = 0
        if family is None:
            mplew.writeInt(2)
            addFamilyCharInfo(MapleFamilyCharacter(chr, 0, 0, 0, 0), mplew)
        else:
            mplew.writeInt(family.getMFC(chr.getId()).getPedigree() + 1)
            addFamilyCharInfo(family.getMFC(family.getLeaderId()), mplew)
            if chr.getSeniorId() > 0:
                senior = family.getMFC(chr.getSeniorId())
                if senior.getSeniorId() > 0:
                    addFamilyCharInfo(family.getMFC(senior.getSeniorId()), mplew)
                addFamilyCharInfo(senior, mplew)
        addFamilyCharInfo((chr.getMFC() is None) ? MapleFamilyCharacter(chr, 0, 0, 0, 0) : chr.getMFC(), mplew)
        if family is not None:
            if chr.getSeniorId() > 0:
                senior = family.getMFC(chr.getSeniorId())
                if senior is not None:
                    if senior.getJunior1() > 0 && senior.getJunior1() != chr.getId():
                        addFamilyCharInfo(family.getMFC(senior.getJunior1()), mplew)
                    elif senior.getJunior2() > 0 && senior.getJunior2() != chr.getId():
                        addFamilyCharInfo(family.getMFC(senior.getJunior2()), mplew)
            if chr.getJunior1() > 0:
                addFamilyCharInfo(family.getMFC(chr.getJunior1()), mplew)
            if chr.getJunior2() > 0:
                addFamilyCharInfo(family.getMFC(chr.getJunior2()), mplew)
            if chr.getJunior1() > 0:
                junior = family.getMFC(chr.getJunior1())
                if junior.getJunior1() > 0:
                    descendants += 1
                    addFamilyCharInfo(family.getMFC(junior.getJunior1()), mplew)
                if junior.getJunior2() > 0:
                    descendants += 1
                    addFamilyCharInfo(family.getMFC(junior.getJunior2()), mplew)
            if chr.getJunior2() > 0:
                junior = family.getMFC(chr.getJunior2())
                if junior.getJunior1() > 0:
                    descendants += 1
                    addFamilyCharInfo(family.getMFC(junior.getJunior1()), mplew)
                if junior.getJunior2() > 0:
                    descendants += 1
                    addFamilyCharInfo(family.getMFC(junior.getJunior2()), mplew)
            gens = family.getGens()
            generations = family.getMemberSize()
        mplew.writeLong(descendants)
        mplew.writeInt(gens)
        mplew.writeInt(-1)
        mplew.writeInt(generations)
        if family is not None:
            if chr.getJunior1() > 0:
                junior = family.getMFC(chr.getJunior1())
                if junior.getJunior1() > 0:
                    mplew.writeInt(junior.getJunior1())
                    mplew.writeInt(family.getMFC(junior.getJunior1()).getDescendants())
                if junior.getJunior2() > 0:
                    mplew.writeInt(junior.getJunior2())
                    mplew.writeInt(family.getMFC(junior.getJunior2()).getDescendants())
            if chr.getJunior2() > 0:
                junior = family.getMFC(chr.getJunior2())
                if junior.getJunior1() > 0:
                    mplew.writeInt(junior.getJunior1())
                    mplew.writeInt(family.getMFC(junior.getJunior1()).getDescendants())
                if junior.getJunior2() > 0:
                    mplew.writeInt(junior.getJunior2())
                    mplew.writeInt(family.getMFC(junior.getJunior2()).getDescendants())
        b = chr.usedBuffs()
        mplew.writeInt(b)
        for ii in b:
            mplew.writeInt(ii.getLeft())
            mplew.writeInt(ii.getRight())
        mplew.writeShort(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendFamilyInvite(self, cid: int, otherLevel: int, otherJob: int, inviter: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendFamilyInvite--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY_INVITE.getValue())
        mplew.writeInt(cid)
        mplew.writeMapleAsciiString(inviter)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getSeniorMessage(self, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getSeniorMessage--------------------")
        mplew.writeShort(SendPacketOpcode.SENIOR_MESSAGE.getValue())
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendFamilyJoinResponse(self, accepted: bool, added: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendFamilyJoinResponse--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY_JUNIOR.getValue())
        mplew.write(accepted ? 1 : 0)
        mplew.writeMapleAsciiString(added)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def familyBuff(self, type: int, buffnr: int, amount: int, time: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("familyBuff--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY_BUFF.getValue())
        mplew.write(type)
        if type >= 2 && type <= 4:
            mplew.writeInt(buffnr)
            mplew.writeInt((type == 3) ? 0 : amount)
            mplew.writeInt((type == 2) ? 0 : amount)
            mplew.write(0)
            mplew.writeInt(time)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelFamilyBuff(self) -> Any:
        if ServerConstants.调试输出封包:
            print("cancelFamilyBuff--------------------")
        return familyBuff(0, 0, 0, 0)

    def familyLoggedIn(self, online: bool, name: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("familyLoggedIn--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY_LOGGEDIN.getValue())
        mplew.write(online ? 1 : 0)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def familySummonRequest(self, name: str, mapname: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("familySummonRequest--------------------")
        mplew.writeShort(SendPacketOpcode.FAMILY_USE_REQUEST.getValue())
        mplew.writeMapleAsciiString(name)
        mplew.writeMapleAsciiString(mapname)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

