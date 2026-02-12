"""
MonsterCarnivalPacket - Converted from Java source
Original: tools/packet/MonsterCarnivalPacket.java
Package: tools.packet
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from server.MapleCarnivalParty import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class MonsterCarnivalPacket:
    """
    Class MonsterCarnivalPacket
    """


    def startMonsterCarnival(self, chr: Any, enemyavailable: int, enemytotal: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("startMonsterCarnival--------------------")
        mplew.writeShort(SendPacketOpcode.MONSTER_CARNIVAL_START.getValue())
        friendly = chr.getCarnivalParty()
        mplew.write(friendly.getTeam())
        mplew.writeShort(chr.getAvailableCP())
        mplew.writeShort(chr.getTotalCP())
        mplew.writeShort(friendly.getAvailableCP())
        mplew.writeShort(friendly.getTotalCP())
        mplew.writeShort(enemyavailable)
        mplew.writeShort(enemytotal)
        mplew.writeLong(0)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def playerDiedMessage(self, name: str, lostCP: int, team: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("playerDiedMessage--------------------")
        mplew.writeShort(SendPacketOpcode.MONSTER_CARNIVAL_DIED.getValue())
        mplew.write(team)
        mplew.write(lostCP)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def CPUpdate(self, party: bool, curCP: int, totalCP: int, team: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("CPUpdate--------------------")
        if !party:
            mplew.writeShort(SendPacketOpcode.MONSTER_CARNIVAL_OBTAINED_CP.getValue())
        else:
            mplew.writeShort(SendPacketOpcode.MONSTER_CARNIVAL_PARTY_CP.getValue())
            mplew.write(team)
        mplew.writeShort(curCP)
        mplew.writeShort(totalCP)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def playerSummoned(self, name: str, tab: int, number: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("playerSummoned--------------------")
        mplew.writeShort(SendPacketOpcode.MONSTER_CARNIVAL_SUMMON.getValue())
        mplew.write(tab)
        mplew.write(number)
        mplew.writeMapleAsciiString(name)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

