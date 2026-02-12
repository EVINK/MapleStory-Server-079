"""
LoginWorker - Converted from Java source
Original: handling/login/LoginWorker.java
Package: handling.login
"""

from typing import Dict
from typing import Optional, Any
import math
import threading
import time

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.LoginPacket import *  # TODO: import specific classes


class LoginWorker:
    """
    Class LoginWorker
    """

    # Static initializer
    # LoginWorker.lastUpdate = 0


    @staticmethod
    def registerClient(c: Any) -> None:
        def _task_1():
            pass

        if LoginServer.isAdminOnly() and not c.isGm():
            c.getSession().write(MaplePacketCreator.serverNotice(1, "管管已设置仅管理员登录。\r\n我们目前正在修复几个问题，\r\n请耐心等待"))
            c.getSession().write(LoginPacket.getLoginFailed(7))
            return
        if int(time.time() * 1000) - LoginWorker.lastUpdate > 600000:
            LoginWorker.lastUpdate = int(time.time() * 1000)
            load = ChannelServer.getChannelLoad()
            usersOn = 0
            if load is None or load <= 0:
                LoginWorker.lastUpdate = 0
                c.getSession().write(LoginPacket.getLoginFailed(7))
                return
            loadFactor = 1200.0 / (LoginServer.getUserLimit() / load)
            for (final Map.Entry<Integer, Integer> entry : load.items())
                usersOn += entry.getValue()
                load.put(entry.getKey(), min(1200, (int)(entry.getValue() * loadFactor)))
            LoginServer.setLoad(load, usersOn)
            LoginWorker.lastUpdate = int(time.time() * 1000)
        if c.finishLogin() == 0:
            if c.getGender() == 10:
                c.getSession().write(LoginPacket.getGenderNeeded(c))
            else:
                c.getSession().write(LoginPacket.getAuthSuccessRequest(c))
                c.getSession().write(LoginPacket.getServerList(0, LoginServer.getServerName(), LoginServer.getLoad()))
                c.getSession().write(LoginPacket.getEndOfServerList())
            c.setIdleTask(Timer.PingTimer.getInstance().schedule(_task_1, 6000000))
        elif c.getGender() == 10:
            c.getSession().write(LoginPacket.getGenderNeeded(c))
        else:
            c.getSession().write(LoginPacket.getAuthSuccessRequest(c))
            c.getSession().write(LoginPacket.getServerList(0, LoginServer.getServerName(), LoginServer.getLoad()))
            c.getSession().write(LoginPacket.getEndOfServerList())

    def run(self) -> None:
        pass

