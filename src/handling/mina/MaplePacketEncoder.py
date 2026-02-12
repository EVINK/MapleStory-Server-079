"""
MaplePacketEncoder - Converted from Java source
Original: handling/mina/MaplePacketEncoder.java
Package: handling.mina
"""

from threading import Lock
from typing import Optional, Any
import asyncio
import logging
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.MapleAESOFB import *  # TODO: import specific classes
# from tools.MapleCustomEncryption import *  # TODO: import specific classes
# from tools.data.input.ByteArrayByteStream import *  # TODO: import specific classes
# from tools.data.input.ByteInputStream import *  # TODO: import specific classes
# from tools.data.input.GenericLittleEndianAccessor import *  # TODO: import specific classes


class MaplePacketEncoder(ProtocolEncoder):
    """
    Class MaplePacketEncoder
    Implements: ProtocolEncoder
    """

    # Static initializer
    # log = LoggerFactory.getLogger(MaplePacketEncoder.class)


    @staticmethod
    def encode(session: Any, message: Any, out: Any) -> None:
        client = session.getAttribute(MapleClient.CLIENT_KEY)
        if client is not None:
            send_crypto = client.getSendCrypto()
            inputInitialPacket = (message).encode("utf-8")
            if ServerConstants.封包显示:
                packetLen = len(inputInitialPacket)
                pHeader = self.readFirstShort(inputInitialPacket)
                pHeaderStr = Integer.toHexString(pHeader).upper()
                op = self.lookupRecv(pHeader)
                show = True
                s = op
                # switch (s):
                    # case "WARP_TO_MAP":
                    # case "PING":
                    # case "NPC_ACTION":
                    # case "UPDATE_STATS":
                    # case "MOVE_PLAYER":
                    # case "SPAWN_NPC":
                    # case "SPAWN_NPC_REQUEST_CONTROLLER":
                    # case "REMOVE_NPC":
                    # case "MOVE_LIFE":
                    # case "MOVE_MONSTER":
                    # case "MOVE_MONSTER_RESPONSE":
                    # case "SPAWN_MONSTER":
                    # case "SPAWN_MONSTER_CONTROL":
                    # case "ANDROID_MOVE":
                        show = False
                        break
                Recv = "服务端发送 " + op + " [" + pHeaderStr + "] (" + packetLen + ")\r\n"
                if packetLen <= 50000:
                    RecvTo = Recv + HexTool.toString(inputInitialPacket) + "\r\n" + HexTool.toStringFromAscii(inputInitialPacket)
                    if show:
                        FileoutputUtil.packetLog("logs/服务端封包.log", RecvTo)
                        print(RecvTo)
                else:
                    MaplePacketEncoder.log.info(HexTool.toString(new byte[] { inputInitialPacket[0], inputInitialPacket[1] }) + " ...")
            unencrypted = new byte[len(inputInitialPacket)]
            System.arraycopy(inputInitialPacket, 0, unencrypted, 0, len(inputInitialPacket))
            ret = new byte[len(unencrypted) + 4]
            mutex = client.getLock()
            mutex.lock()
            try:
                header = send_crypto.getPacketHeader(len(unencrypted))
                MapleCustomEncryption.encryptData(unencrypted)
                send_crypto.crypt(unencrypted)
                System.arraycopy(header, 0, ret, 0, 4)
            finally:
                mutex.unlock()
            System.arraycopy(unencrypted, 0, ret, 4, len(unencrypted))
            out.write(IoBuffer.wrap(ret))
        else:
            out.write(IoBuffer.wrap((message).encode("utf-8")))

    def dispose(self, session: Any) -> None:
        pass

    def lookupRecv(self, val: int) -> str:
        for op in SendPacketOpcode.values():
            if op.getValue() == val:
                return op.name()
        return "UNKNOWN"

    def readFirstShort(self, arr: bytes) -> int:
        return GenericLittleEndianAccessor(ByteArrayByteStream(arr)).readShort()

