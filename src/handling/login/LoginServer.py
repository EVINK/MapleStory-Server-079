"""
LoginServer - Converted from Java source
Original: handling/login/LoginServer.java
Package: handling.login
"""

from socket import socket
from typing import Dict
from typing import Optional, Any
from typing import Set
import asyncio
import os

# Internal module imports
# from handling.MapleServerHandler import *  # TODO: import specific classes
# from handling.mina.MapleCodecFactory import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from tools.Triple import *  # TODO: import specific classes


class LoginServer:
    """
    Class LoginServer
    """

    # Static initializer
    # LoginServer.PORT = 1314
    # LoginServer.load = {}
    # LoginServer.usersOn = 0
    # LoginServer.finishedShutdown = True
    # LoginServer.adminOnly = False
    # loginAuth = new HashMap<Integer, Triple<String, String, Integer>>()
    # loginIPAuth = set()
    # instance = LoginServer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def putLoginAuth(self, chrid: int, ip: str, tempIp: str, channel: int) -> None:
        LoginServer.loginAuth.put(chrid, new Triple<String, String, Integer>(ip, tempIp, channel))
        LoginServer.loginIPAuth.add(ip)

    def getLoginAuth(self, chrid: int) -> Any:
        return LoginServer.loginAuth.remove(chrid)

    def containsIPAuth(self, ip: str) -> bool:
        return (ip in LoginServer.loginIPAuth)

    def removeIPAuth(self, ip: str) -> None:
        LoginServer.loginIPAuth.remove(ip)

    def addIPAuth(self, ip: str) -> None:
        LoginServer.loginIPAuth.add(ip)

    def addChannel(self, channel: int) -> None:
        LoginServer.load.put(channel, 0)

    def removeChannel(self, channel: int) -> None:
        LoginServer.load.remove(channel)

    def run_startup_configurations(self) -> None:
        LoginServer.userLimit = Integer.valueOf(ServerProperties.getProperty("RoyMS.userLimit"))
        LoginServer.serverName = ServerProperties.getProperty("RoyMS.ServerName")
        LoginServer.eventMessage = ServerProperties.getProperty("RoyMS.EventMessage")
        LoginServer.flag = Byte.parseByte(ServerProperties.getProperty("RoyMS.Flag"))
        LoginServer.PORT = int(ServerProperties.getProperty("RoyMS.LPort"))
        LoginServer.adminOnly = bool(ServerProperties.getProperty("RoyMS.Admin", "False"))
        LoginServer.maxCharacters = int(ServerProperties.getProperty("RoyMS.MaxCharacters"))
        LoginServer.个人PK地图 = int(ServerProperties.getProperty("RoyMS.personPVP"))
        LoginServer.组队PK地图 = int(ServerProperties.getProperty("RoyMS.teamPVP"))
        LoginServer.家族PK地图 = int(ServerProperties.getProperty("RoyMS.familyPVP"))
        IoBuffer.setUseDirectBuffer(False)
        IoBuffer.setAllocator(SimpleBufferAllocator())
        LoginServer.acceptor = NioSocketAcceptor()
        LoginServer.acceptor.getFilterChain().addLast("codec", ProtocolCodecFilter(MapleCodecFactory()))
        LoginServer.acceptor.setHandler(MapleServerHandler(-1, False))
        (LoginServer.acceptor.getSessionConfig()).setTcpNoDelay(True)
        try:
            LoginServer.acceptor.bind(InetSocketAddress(LoginServer.PORT))
            print("登录服务器 : 启动端口 " + LoginServer.PORT)
        except IOError as e:
            print("Binding to port " + LoginServer.PORT + " failed" + e)

    def shutdown(self) -> None:
        if LoginServer.finishedShutdown:
            return
        print("正在关闭登录伺服器...")
        LoginServer.finishedShutdown = True

    def getServerName(self) -> str:
        return LoginServer.serverName

    def getEventMessage(self) -> str:
        return LoginServer.eventMessage

    def getFlag(self) -> int:
        return LoginServer.flag

    @staticmethod
    def getMaxCharacters() -> int:
        return LoginServer.maxCharacters

    def getLoad(self) -> dict:
        return LoginServer.load

    def setLoad(self, load_: dict, usersOn_: int) -> None:
        LoginServer.load = load_
        LoginServer.usersOn = usersOn_

    def setEventMessage(self, newMessage: str) -> None:
        LoginServer.eventMessage = newMessage

    def setFlag(self, newflag: int) -> None:
        LoginServer.flag = newflag

    def getUserLimit(self) -> int:
        return LoginServer.userLimit

    def getUsersOn(self) -> int:
        return LoginServer.usersOn

    @staticmethod
    def setUserLimit(newLimit: int) -> None:
        LoginServer.userLimit = newLimit

    def getNumberOfSessions(self) -> int:
        return LoginServer.acceptor.getManagedSessions()

    def isAdminOnly(self) -> bool:
        return LoginServer.adminOnly

    def isShutdown(self) -> bool:
        return LoginServer.finishedShutdown

    def setOn(self) -> None:
        LoginServer.finishedShutdown = False

    def translated_个人PK地图(self) -> int:
        return LoginServer.个人PK地图

    @staticmethod
    def translated_组队PK地图() -> int:
        return LoginServer.组队PK地图

    @staticmethod
    def translated_家族PK地图() -> int:
        return LoginServer.家族PK地图

    @staticmethod
    def closeConn(ip: str) -> None:
        count = 0
        for ss in LoginServer.acceptor.getManagedSessions().values():
            if ss.getRemoteAddress().split(":")[0] == (ip):
                ss.close(False)

