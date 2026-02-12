"""
PacketErrorHandler - Converted from Java source
Original: handling/login/handler/PacketErrorHandler.java
Package: handling.login.handler
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class PacketErrorHandler:
    """
    Class PacketErrorHandler
    """


    def handlePacket(self, slea: Any, c: Any) -> None:
        if slea.available() >= 6:
            slea.skip(6)
            badPacketSize = slea.readShort()
            slea.skip(4)
            pHeader = slea.readShort()
            pHeaderStr = Integer.toHexString(pHeader).upper()
            pHeaderStr = StringUtil.getLeftPaddedStr(pHeaderStr, '0', 4)
            op = lookupRecv(pHeader)
            from = ""
            if c.getPlayer() is not None:
                from = "\r\n时间：" + FileoutputUtil.CurrentReadable_Time() + "  角色: " + c.getPlayer().getName() + "  等级(" + c.getPlayer().getLevel() + ") 职业: " + c.getPlayer().getJob() + " \r\n"
            Recv = "封包出错: \r\n" + op + " [" + pHeaderStr + "] (" + (badPacketSize - 6) + ")\r\n" + slea.toString(True)
            FileoutputUtil.packetLog("logs/封包出错.log", from + Recv)

    def lookupRecv(self, val: int) -> str:
        for op in SendPacketOpcode.values():
            if op.getValue() == val:
                return op.name()
        return "UNKNOWN"

