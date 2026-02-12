"""
ShutdownServer - Converted from Java source
Original: server/ShutdownServer.java
Package: server
"""

from pymysql import Error
from typing import Optional, Any
from typing import Set
import os
import pymysql
import sys
import threading
import time

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class ShutdownServer(Runnable):
    """
    Class ShutdownServer
    Implements: Runnable
    """

    def __init__(self):
        self.mode = 0
        self.mode = 0

    # Static initializer
    # instance = ShutdownServer()
    # ShutdownServer.running = False


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def shutdown(self) -> None:
        self.run()

    def run(self) -> None:
        Timer.WorldTimer.getInstance().stop()
        Timer.EtcTimer.getInstance().stop()
        Timer.MapTimer.getInstance().stop()
        Timer.MobTimer.getInstance().stop()
        Timer.CloneTimer.getInstance().stop()
        Timer.CheatTimer.getInstance().stop()
        Timer.EventTimer.getInstance().stop()
        Timer.BuffTimer.getInstance().stop()
        Timer.TimerManager.getInstance().stop()
        for cs in ChannelServer.getAllInstances():
            cs.closeAllMerchant()
        try:
            World.Guild.save()
            World.Alliance.save()
            World.Family.save()
        except Exception as ex:
            pass
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, " 游戏服务器将关闭维护，请玩家安全下线..."))
        for cs in ChannelServer.getAllInstances():
            try:
                cs.setServerMessage("游戏服务器将关闭维护，请玩家安全下线...")
            except Exception as ex2:
                pass
        channels = ChannelServer.getAllInstance()
        for channel in channels:
            try:
                cs2 = ChannelServer.getInstance(channel)
                cs2.saveAll()
                cs2.setFinishShutdown()
                cs2.shutdown()
            except Exception as e2:
                print("频道" + str(channel) + " 关闭错误.")
        print("服务端关闭事件 1 已完成.")
        print("服务端关闭事件 2 开始...")
        try:
            LoginServer.shutdown()
            print("登录伺服器关闭完成...")
        except Exception as ex3:
            pass
        try:
            CashShopServer.shutdown()
            print("商城伺服器关闭完成...")
        except Exception as ex4:
            pass
        try:
            DatabaseConnection.closeAll()
        except SQLException as ex5:
            pass
        Timer.PingTimer.getInstance().stop()
        print("服务端关闭事件 2 已完成.")
        try:
            Thread.sleep(1000)
        except InterruptedException as e:
            print("关闭服务端错误 - 2" + e)
        sys.exit(0)

