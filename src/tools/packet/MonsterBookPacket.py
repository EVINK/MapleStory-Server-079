"""
MonsterBookPacket - Converted from Java source
Original: tools/packet/MonsterBookPacket.java
Package: tools.packet
"""

from typing import Optional, Any

# Internal module imports
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class MonsterBookPacket:
    """
    Class MonsterBookPacket
    """


    def addCard(self, full: bool, cardid: int, level: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addCard--------------------")
        mplew.writeShort(SendPacketOpcode.MONSTERBOOK_ADD.getValue())
        if !full:
            mplew.write(1)
            mplew.writeInt(cardid)
            mplew.writeInt(level)
        else:
            mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showGainCard(self, itemid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showGainCard--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(15)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showForeginCardEffect(self, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showForeginCardEffect--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(id)
        mplew.write(13)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def changeCover(self, cardid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("changeCover--------------------")
        mplew.writeShort(SendPacketOpcode.MONSTERBOOK_CHANGE_COVER.getValue())
        mplew.writeInt(cardid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

