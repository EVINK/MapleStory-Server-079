"""
MaplePacketDecoder - Converted from Java source
Original: handling/mina/MaplePacketDecoder.java
Package: handling.mina
"""

from typing import Optional, Any
import asyncio
import logging

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.RecvPacketOpcode import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.MapleAESOFB import *  # TODO: import specific classes
# from tools.MapleCustomEncryption import *  # TODO: import specific classes
# from tools.data.input.ByteArrayByteStream import *  # TODO: import specific classes
# from tools.data.input.ByteInputStream import *  # TODO: import specific classes
# from tools.data.input.GenericLittleEndianAccessor import *  # TODO: import specific classes


class MaplePacketDecoder(CumulativeProtocolDecoder):
    """
    Class MaplePacketDecoder
    Extends: CumulativeProtocolDecoder
    """

    def __init__(self):
        self.packetlength = 0

    # Static initializer
    # MaplePacketDecoder.DECODER_STATE_KEY = MaplePacketDecoder.class.getName() + ".STATE"
    # log = LoggerFactory.getLogger(MaplePacketDecoder.class)


    @staticmethod
    def doDecode(session: Any, in: Any, out: Any) -> bool:
        decoderState = session.getAttribute(MaplePacketDecoder.DECODER_STATE_KEY)
        if decoderState is None:
            decoderState = DecoderState()
            session.setAttribute(MaplePacketDecoder.DECODER_STATE_KEY, decoderState)
        client = session.getAttribute(MapleClient.CLIENT_KEY)
        if decoderState.packetlength == -1:
            if in.remaining() >= 4:
                packetHeader = in.getInt()
                if not client.getReceiveCrypto().checkPacket(packetHeader):
                    session.close(True)
                    return False
                decoderState.packetlength = MapleAESOFB.getPacketLength(packetHeader)
            elif in.remaining() < 4 and decoderState.packetlength == -1:
                MaplePacketDecoder.log.trace("解码…没有足够的数据/就是所谓的包不完整")
                return False
        if in.remaining() >= decoderState.packetlength:
            decryptedPacket = new byte[decoderState.packetlength]
            in.get(decryptedPacket, 0, decoderState.packetlength)
            decoderState.packetlength = -1
            client.getReceiveCrypto().crypt(decryptedPacket)
            MapleCustomEncryption.decryptData(decryptedPacket)
            out.write(decryptedPacket)
            if ServerConstants.封包显示:
                packetLen = len(decryptedPacket)
                pHeader = self.readFirstShort(decryptedPacket)
                pHeaderStr = Integer.toHexString(pHeader).upper()
                op = self.lookupSend(pHeader)
                show = True
                s = op
                # switch (s):
                    # case "PONG":
                    # case "NPC_ACTION":
                    # case "MOVE_LIFE":
                    # case "MOVE_PLAYER":
                    # case "MOVE_ANDROID":
                    # case "MOVE_SUMMON":
                    # case "AUTO_AGGRO":
                    # case "HEAL_OVER_TIME":
                    # case "BUTTON_PRESSED":
                    # case "STRANGE_DATA":
                        show = False
                        break
                Send = "客户端发送 " + op + " [" + pHeaderStr + "] (" + packetLen + ")\r\n"
                if packetLen <= 3000:
                    SendTo = Send + HexTool.toString(decryptedPacket) + "\r\n" + HexTool.toStringFromAscii(decryptedPacket)
                    if show:
                        FileoutputUtil.packetLog("logs/客户端封包.log", SendTo)
                        print(SendTo)
                    SendTos = "\r\n时间：" + FileoutputUtil.CurrentReadable_Time() + " "
                    if op == ("UNKNOWN"):
                        FileoutputUtil.packetLog("logs/未知客服端封包.log", SendTos + SendTo)
                else:
                    MaplePacketDecoder.log.info(HexTool.toString(new byte[] { decryptedPacket[0], decryptedPacket[1] }) + "...")
            return True
        return False

    def lookupSend(self, val: int) -> str:
        for op in RecvPacketOpcode.values():
            if op.getValue() == val:
                return op.name()
        return "UNKNOWN"

    def readFirstShort(self, arr: bytes) -> int:
        return GenericLittleEndianAccessor(ByteArrayByteStream(arr)).readShort()


# Inner class from Java (originally nested)
class DecoderState:
    """
    Class DecoderState
    """

    def __init__(self):
        self.packetlength = 0
        self.packetlength = -1


