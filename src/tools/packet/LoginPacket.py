"""
LoginPacket - Converted from Java source
Original: tools/packet/LoginPacket.java
Package: tools.packet
"""

from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.login.handler.Balloon import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class LoginPacket:
    """
    Class LoginPacket
    """


    def getHello(self, mapleVersion: int, sendIv: bytes, recvIv: bytes) -> Any:
        mplew = MaplePacketLittleEndianWriter(16)
        if ServerConstants.调试输出封包:
            print("getHello--------------------")
        mplew.writeShort(13)
        mplew.writeShort(mapleVersion)
        mplew.write(new byte[] { 0, 0 })
        mplew.write(recvIv)
        mplew.write(sendIv)
        mplew.write(4)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPing(self) -> Any:
        mplew = MaplePacketLittleEndianWriter(16)
        if ServerConstants.调试输出封包:
            print("getPing--------------------")
        mplew.writeShort(SendPacketOpcode.PING.getValue())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def StrangeDATA(self) -> Any:
        mplew = MaplePacketLittleEndianWriter(16)
        if ServerConstants.调试输出封包:
            print("StrangeDATA--------------------")
        mplew.writeShort(18)
        mplew.writeMapleAsciiString("30819F300D06092A864886F70D010101050003818D0030818902818100994F4E66B003A7843C944E67BE4375203DAA203C676908E59839C9BADE95F53E848AAFE61DB9C09E80F48675CA2696F4E897B7F18CCB6398D221C4EC5823D11CA1FB9764A78F84711B8B6FCA9F01B171A51EC66C02CDA9308887CEE8E59C4FF0B146BF71F697EB11EDCEBFCE02FB0101A7076A3FEB64F6F6022C8417EB6B87270203010001")
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def genderNeeded(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter(3)
        if ServerConstants.调试输出封包:
            print("genderNeeded--------------------")
        mplew.writeShort(SendPacketOpcode.CHOOSE_GENDER.getValue())
        mplew.writeMapleAsciiString(c.getAccountName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getLoginFailed(self, reason: int) -> Any:
        mplew = MaplePacketLittleEndianWriter(16)
        if ServerConstants.调试输出封包:
            print("getLoginFailed--------------------")
        mplew.writeShort(SendPacketOpcode.LOGIN_STATUS.getValue())
        mplew.writeInt(reason)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPermBan(self, reason: int) -> Any:
        mplew = MaplePacketLittleEndianWriter(16)
        if ServerConstants.调试输出封包:
            print("getPermBan--------------------")
        mplew.writeShort(SendPacketOpcode.LOGIN_STATUS.getValue())
        mplew.writeShort(2)
        mplew.write(0)
        mplew.write(reason)
        mplew.write(HexTool.getByteArrayFromHexString("01 01 01 01 00"))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTempBan(self, timestampTill: int, reason: int) -> Any:
        mplew = MaplePacketLittleEndianWriter(17)
        if ServerConstants.调试输出封包:
            print("getTempBan--------------------")
        mplew.writeShort(SendPacketOpcode.LOGIN_STATUS.getValue())
        mplew.write(2)
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 00 00"))
        mplew.write(reason)
        mplew.writeLong(timestampTill)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGenderChanged(self, client: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getGenderChanged--------------------")
        mplew.writeShort(SendPacketOpcode.GENDER_SET.getValue())
        mplew.write(client.getGender())
        mplew.writeMapleAsciiString(client.getAccountName())
        mplew.writeMapleAsciiString(str(client.getAccID()))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGenderNeeded(self, client: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getGenderNeeded--------------------")
        mplew.writeShort(SendPacketOpcode.CHOOSE_GENDER.getValue())
        mplew.writeMapleAsciiString(client.getAccountName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getAuthSuccessRequest(self, client: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getAuthSuccessRequest--------------------")
        mplew.writeShort(SendPacketOpcode.LOGIN_STATUS.getValue())
        mplew.write(0)
        mplew.writeInt(client.getAccID())
        mplew.write(client.getGender())
        mplew.writeShort(client.isGm() ? 1 : 0)
        mplew.writeMapleAsciiString(client.getAccountName())
        mplew.write(HexTool.getByteArrayFromHexString("00 00 00 03 01 00 00 00 E2 ED A3 7A FA C9 01"))
        mplew.writeInt(0)
        mplew.writeLong(0)
        mplew.writeMapleAsciiString(str(client.getAccID()))
        mplew.writeMapleAsciiString(client.getAccountName())
        mplew.write(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getServerList(self, serverId: int, serverName: str, channelLoad: dict) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getServerList--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERLIST.getValue())
        mplew.write(serverId)
        mplew.writeMapleAsciiString(serverName)
        mplew.write(LoginServer.getFlag())
        mplew.writeMapleAsciiString(LoginServer.getEventMessage())
        mplew.writeShort(100)
        mplew.writeShort(100)
        lastChannel = 1
        channels = channelLoad.keys()
        i = 30
        while i > 0:
            if (i in channels):
                lastChannel = i
                break
        mplew.write(lastChannel)
        mplew.writeInt(500)
        for j in range(1, = lastChannel):
            load = None
            if (j in channels):
                load = channelLoad.get(j)
            else:
                load = 1200
            mplew.writeMapleAsciiString(serverName + "-" + j)
            mplew.writeInt(load)
            mplew.write(serverId)
            mplew.writeShort(j - 1)
        mplew.writeShort(GameConstants.getBalloons())
        for balloon in GameConstants.getBalloons():
            mplew.writeShort(balloon.nX)
            mplew.writeShort(balloon.nY)
            mplew.writeMapleAsciiString(balloon.sMessage)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getEndOfServerList(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getEndOfServerList--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERLIST.getValue())
        mplew.write(255)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getServerStatus(self, status: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getServerStatus--------------------")
        mplew.writeShort(SendPacketOpcode.SERVERSTATUS.getValue())
        mplew.writeShort(status)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getCharList(self, secondpw: bool, chars: list, charslots: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getCharList--------------------")
        mplew.writeShort(SendPacketOpcode.CHARLIST.getValue())
        mplew.write(0)
        mplew.writeInt(0)
        mplew.write(chars)
        for chr in chars:
            addCharEntry(mplew, chr, not chr.isGM() and chr.getLevel() >= 10, False)
        mplew.writeShort(3)
        mplew.writeInt(charslots)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addNewCharEntry(self, chr: Any, worked: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addNewCharEntry--------------------")
        mplew.writeShort(SendPacketOpcode.ADD_NEW_CHAR_ENTRY.getValue())
        mplew.write(worked ? 0 : 1)
        addCharEntry(mplew, chr, False, False)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def charNameResponse(self, charname: str, nameUsed: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("charNameResponse--------------------")
        mplew.writeShort(SendPacketOpcode.CHAR_NAME_RESPONSE.getValue())
        mplew.writeMapleAsciiString(charname)
        mplew.write(nameUsed ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addCharEntry(self, mplew: Any, chr: Any, ranking: bool, viewAll: bool) -> None:
        if ServerConstants.调试输出封包:
            print("addCharEntry--------------------")
        PacketHelper.addCharStats(mplew, chr)
        PacketHelper.addCharLook(mplew, chr, True, viewAll)
        mplew.write(0)
        if chr.getJob() == 900:
            mplew.write(2)

