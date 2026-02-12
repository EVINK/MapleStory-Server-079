"""
CashShopServer - Converted from Java source
Original: handling/cashshop/CashShopServer.java
Package: handling.cashshop
"""

from socket import socket
from typing import Optional, Any
import asyncio
import os

# Internal module imports
# from handling.MapleServerHandler import *  # TODO: import specific classes
# from handling.channel.PlayerStorage import *  # TODO: import specific classes
# from handling.mina.MapleCodecFactory import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes


class CashShopServer:
    """
    Class CashShopServer
    """

    DEFAULT_PORT = 5200

    # Static initializer
    # CashShopServer.finishedShutdown = False


    @staticmethod
    def run_startup_configurations() -> None:
        CashShopServer.PORT = Short.parseShort(ServerProperties.getProperty("RoyMS.CSPort", str(DEFAULT_PORT)))
        CashShopServer.ip = ServerProperties.getProperty("RoyMS.IP") + ":" + CashShopServer.PORT
        IoBuffer.setUseDirectBuffer(False)
        IoBuffer.setAllocator(SimpleBufferAllocator())
        CashShopServer.acceptor = NioSocketAcceptor()
        CashShopServer.acceptor.getFilterChain().addLast("codec", ProtocolCodecFilter(MapleCodecFactory()))
        (CashShopServer.acceptor.getSessionConfig()).setTcpNoDelay(True)
        CashShopServer.players = PlayerStorage(-10)
        CashShopServer.playersMTS = PlayerStorage(-20)
        try:
            CashShopServer.acceptor.setHandler(MapleServerHandler(-1, True))
            CashShopServer.acceptor.bind(InetSocketAddress(CashShopServer.PORT))
            print("商城 1: 启动端口 " + CashShopServer.PORT)
        except IOError as e:
            print("Binding to port " + CashShopServer.PORT + " failed")
            e.printStackTrace()
            raise RuntimeError("Binding failed.", e)

    def getIP(self) -> str:
        return CashShopServer.ip

    @staticmethod
    def getPlayerStorage() -> Any:
        return CashShopServer.players

    def getPlayerStorageMTS(self) -> Any:
        return CashShopServer.playersMTS

    def shutdown(self) -> None:
        if CashShopServer.finishedShutdown:
            return
        print("正在断开商城内玩家...")
        CashShopServer.players.disconnectAll()
        CashShopServer.playersMTS.disconnectAll()
        print("正在关闭商城伺服器...")
        CashShopServer.finishedShutdown = True

    def isShutdown(self) -> bool:
        return CashShopServer.finishedShutdown

