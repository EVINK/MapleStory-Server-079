"""
UIPacket - Converted from Java source
Original: tools/packet/UIPacket.java
Package: tools.packet
"""

from typing import Optional, Any
import threading

# Internal module imports
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class UIPacket:
    """
    Class UIPacket
    """


    def getSPMsg(self, sp: int, job: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getSPMsg--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(3)
        mplew.writeShort(job)
        mplew.write(sp)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getGPMsg(self, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getGPMsg--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(6)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getTopMsg(self, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getTopMsg--------------------")
        mplew.writeShort(SendPacketOpcode.TOP_MSG.getValue())
        mplew.writeMapleAsciiString(msg)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getStatusMsg(self, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getStatusMsg--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_STATUS_INFO.getValue())
        mplew.write(7)
        mplew.writeInt(itemid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def MapEff(self, path: str) -> Any:
        if ServerConstants.调试输出封包:
            print("MapEff--------------------")
        return MaplePacketCreator.environmentChange(path, 3)

    def MapNameDisplay(self, mapid: int) -> Any:
        if ServerConstants.调试输出封包:
            print("MapNameDisplay--------------------")
        return MaplePacketCreator.environmentChange("maplemap/enter/" + mapid, 3)

    def Aran_Start(self) -> Any:
        if ServerConstants.调试输出封包:
            print("Aran_Start--------------------")
        return MaplePacketCreator.environmentChange("Aran/balloon", 4)

    def AranTutInstructionalBalloon(self, data: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("AranTutInstructionalBalloon--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(35)
        mplew.writeMapleAsciiString(data)
        mplew.writeInt(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def ShowWZEffect(self, data: str, info: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("ShowWZEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        if info == -1:
            mplew.write(18)
        else:
            mplew.write(23)
        mplew.writeMapleAsciiString(data)
        if info > -1:
            mplew.writeInt(info)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def ShowWZEffectS(self, data: str, info: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(20)
        mplew.writeMapleAsciiString(data)
        if info > -1:
            mplew.writeInt(info)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def summonHelper(self, summon: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("summonHelper--------------------")
        mplew.writeShort(SendPacketOpcode.SUMMON_HINT.getValue())
        mplew.write(summon ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def summonMessage(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("summonMessageA--------------------")
        mplew.writeShort(SendPacketOpcode.SUMMON_HINT_MSG.getValue())
        mplew.write(1)
        mplew.writeInt(type)
        mplew.writeInt(7000)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def summonMessage_message(self, message: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("summonMessageB--------------------")
        mplew.writeShort(SendPacketOpcode.SUMMON_HINT_MSG.getValue())
        mplew.write(0)
        mplew.writeMapleAsciiString(message)
        mplew.writeInt(200)
        mplew.writeShort(0)
        mplew.writeInt(10000)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def IntroLock(self, enable: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("IntroLock--------------------")
        mplew.writeShort(SendPacketOpcode.CYGNUS_INTRO_LOCK.getValue())
        mplew.write(enable ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def IntroDisableUI(self, enable: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("IntroDisableUI--------------------")
        mplew.writeShort(SendPacketOpcode.CYGNUS_INTRO_DISABLE_UI.getValue())
        mplew.write(enable ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def fishingUpdate(self, type: int, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("fishingUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.FISHING_BOARD_UPDATE.getValue())
        mplew.write(type)
        mplew.writeInt(id)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def fishingCaught(self, chrid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("fishingCaught--------------------")
        mplew.writeShort(SendPacketOpcode.FISHING_CAUGHT.getValue())
        mplew.writeInt(chrid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

