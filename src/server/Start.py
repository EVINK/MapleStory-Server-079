"""
Start - Converted from Java source
Original: server/Start.java
Package: server
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from socket import socket
from typing import Dict
from typing import List
from typing import Optional, Any
import gc
import os
import pymysql
import socket
import sys
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.OtherSettings import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from gui.RoyMS import *  # TODO: import specific classes
# from handling.MapleServerHandler import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.channel.MapleGuildRanking import *  # TODO: import specific classes
# from handling.login.LoginInformationProvider import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyBuff import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from server.events.MapleOxQuizFactory import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonsterInformationProvider import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class Start:
    """
    Class Start
    """

    srvPort = 6350

    def __init__(self):
        self.c = None

    # Static initializer
    # Start.Check = True
    # Start.instance = Start()
    # Start.maxUsers = 0
    # Start.srvSocket = None


    @staticmethod
    def main(args: list) -> None:
        homePath = os.environ.get("homePath")
        scriptsPath = os.environ.get("scriptsPath")
        wzPath = os.environ.get("wzPath")
        os.environ["server_property_file_path"] = homePath + "server.properties"
        os.environ["server_property_db_path"] = homePath + "db.properties"
        os.environ["server_property_shop_path"] = homePath + "shop.properties"
        os.environ["server_property_fish_path"] = homePath + "fish.properties"
        os.environ["wzPath"] = wzPath
        os.environ["scripts_path"] = scriptsPath
        os.environ["server_name"] = "冒险岛"
        OtherSettings.getInstance()
        Start.instance.run()

    def run(self) -> None:
        start = int(time.time() * 1000)
        checkSingleInstance()
        if bool(ServerProperties.getProperty("RoyMS.Admin")):
            printSection("[not not not 已开启只能管理员登录模式 not not not ]")
        if bool(ServerProperties.getProperty("RoyMS.AutoRegister")):
            print("加载 自动注册完成 :::")
        try:
            # try-with-resources: final PreparedStatement ps = DatabaseConnection.getConnection().prepareStatement("UPDATE accounts SET loggedin = 0")
            try:
                ps.executeUpdate()
            # try-with-resources: final PreparedStatement ps = DatabaseConnection.getConnection().prepareStatement("UPDATE accounts SET lastGainHM = 0")
            try:
                ps.executeUpdate()
        except Exception as ex:
            raise RuntimeError("[数据库异常] 请检查数据库链接。目前无法连接到MySQL数据库.")
        print("服务端 开始启动...版本号：079")
        print("当前操作系统: " + os.environ.get("sun.desktop"))
        print("服务器地址: " + ServerProperties.getProperty("RoyMS.IP") + ":" + LoginServer.PORT)
        print("游戏版本: " + ServerConstants.MAPLE_TYPE + " v." + ServerConstants.MAPLE_VERSION + "." + ServerConstants.MAPLE_PATCH)
        print("主服务器: 蓝蜗牛")
        World.init()
        runThread()
        loadData()
        print("加载\"登入\"服务...")
        LoginServer.run_startup_configurations()
        print("正在加载频道...")
        ChannelServer.startChannel_Main()
        print("频道加载完成!\r\n")
        print("正在加载商城...")
        CashShopServer.run_startup_configurations()
        printSection("刷怪线程")
        World.registerRespawn()
        Timer.CheatTimer.getInstance().register(AutobanManager.getInstance(), 60000)
        onlineTime(1)
        memoryRecical(10)
        MapleServerHandler.registerMBean()
        LoginServer.setOn()
        print("\r\n经验倍率：" + int(ServerProperties.getProperty("RoyMS.Exp")) + " 物品倍率：" + int(ServerProperties.getProperty("RoyMS.Drop")) + " 金币倍率：" + int(ServerProperties.getProperty("RoyMS.Meso")) + " BOSS爆率：" + int(ServerProperties.getProperty("RoyMS.BDrop")))
        if bool(ServerProperties.getProperty("RoyMS.检测复制装备", "False")):
            checkCopyItemFromSql()
        if bool(ServerProperties.getProperty("RoyMS.防万能检测", "False")):
            print("启动防万能检测")
            startCheck()
        now = int(time.time() * 1000) - start
        seconds = now / 1000
        ms = now % 1000
        print("加载完成, 耗时: " + seconds + "秒" + ms + "毫秒\r\n")
        # CashGui();
        loadGui = Boolean.valueOf(ServerProperties.getProperty("RoyMS.loadGui","False"))
        if loadGui:
            print("加载GUI工具")
            CashGui()

    def runThread(self) -> None:
        print("\r\n正在加载线程")
        Timer.WorldTimer.getInstance().start()
        Timer.EtcTimer.getInstance().start()
        Timer.MapTimer.getInstance().start()
        Timer.MobTimer.getInstance().start()
        Timer.CloneTimer.getInstance().start()
        Timer.CheatTimer.getInstance().start()
        print(".")
        Timer.EventTimer.getInstance().start()
        Timer.BuffTimer.getInstance().start()
        Timer.TimerManager.getInstance().start()
        Timer.PingTimer.getInstance().start()
        Timer.PGTimer.getInstance().start()
        print("完成!\r\n")

    def loadData(self) -> None:
        print("载入数据(因为数据量大可能比较久而且内存消耗会飙升)")
        print("加载等级经验数据")
        GameConstants.LoadExp()
        print("加载排名信息数据")
        MapleGuildRanking.getInstance().RankingUpdate()
        print("加载公会数据并清理不存在公会")
        MapleGuild.loadAll()
        print("加载任务数据")
        MapleQuest.initQuests()
        MapleLifeFactory.loadQuestCounts()
        print("加载爆物数据")
        MapleMonsterInformationProvider.getInstance().retrieveGlobal()
        print("加载脏话检测系统")
        LoginInformationProvider.getInstance()
        print("加载道具数据")
        ItemMakerFactory.getInstance()
        MapleItemInformationProvider.getInstance().load()
        print("加载技能数据")
        SkillFactory.getSkill(99999999)
        MobSkillFactory.getInstance()
        MapleFamilyBuff.getBuffEntry()
        print("加载SpeedRunner")
        Runtime.getRuntime().addShutdownHook(Thread(Shutdown()))
        try:
            SpeedRunner.getInstance().loadSpeedRuns()
        except Exception as e:
            print("SpeedRunner错误:" + e)
        print("加载随机奖励系统")
        RandomRewards.getInstance()
        print("加载0X问答系统")
        MapleOxQuizFactory.getInstance().initialize()
        print("加载嘉年华数据")
        MapleCarnivalFactory.getInstance()
        print("加载角色类排名数据")
        print("加载商城道具数据，数据较为庞大，请耐心等待")
        CashItemFactory.getInstance().initialize()
        MapleMapFactory.loadCustomLife()

    def auto_save(self, time: int) -> None:
        def _task_1():
            ppl = 0
            try:
                for cserv in ChannelServer.getAllInstances():
                    for chr in cserv.getPlayerStorage().getAllCharacters():
                        if chr is None:
                            continue
                        ppl += 1
                        chr.saveToDB(False, False)
            except Exception as ex:
                pass

        print("服务端启用自动存档." + time + "分钟自动执行数据存档.")
        Timer.WorldTimer.getInstance().register(_task_1, 60000 * time)

    def onlineTime(self, time: int) -> None:
        def _task_1():
            try:
                for chan in ChannelServer.getAllInstances():
                    for chr in chan.getPlayerStorage().getAllCharacters():
                        if chr is None:
                            continue
                        chr.gainGamePoints(1)
                        if chr.getGamePoints() >= 5:
                            continue
                        chr.resetFBRW()
                        chr.resetFBRWA()
                        chr.resetSBOSSRW()
                        chr.resetSBOSSRWA()
                        chr.resetSGRW()
                        chr.resetSGRWA()
                        chr.resetSJRW()
                        chr.resetlb()
                        chr.setmrsjrw(0)
                        chr.setmrfbrw(0)
                        chr.setmrsgrw(0)
                        chr.setmrsbossrw(0)
                        chr.setmrfbrwa(0)
                        chr.setmrsgrwa(0)
                        chr.setmrsbossrwa(0)
                        chr.setmrfbrwas(0)
                        chr.setmrsgrwas(0)
                        chr.setmrsbossrwas(0)
                        chr.setmrfbrws(0)
                        chr.setmrsgrws(0)
                        chr.setmrsbossrws(0)
                        chr.resetGamePointsPS()
                        chr.resetGamePointsPD()
            except Exception as ex:
                pass

        print("服务端启用在线时间统计." + time + "分钟记录一次在线时间.")
        Timer.WorldTimer.getInstance().register(_task_1, 60000 * time)

    def checkSingleInstance(self) -> None:
        try:
            Start.srvSocket = ServerSocket(srvPort)
        except IOError as ex:
            if ex.getMessage().find("Address already in use: JVM_Bind") >= 0:
                print("在一台主机上同时只能启动一个进程(Only one instance allowed)。")
            sys.exit(0)

    def checkCopyItemFromSql(self) -> None:
        print("服务端启用 防复制系统，发现复制装备.进行删除处理功能")
        equipOnlyIds = []
        checkItems = {}
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM inventoryitems WHERE equipOnlyId > 0")
            rs = ps.executeQuery()
            while rs.next():
                itemId = rs.getInt("itemId")
                equipOnlyId = rs.getInt("equipOnlyId")
                if equipOnlyId > 0:
                    if (equipOnlyId in checkItems):
                        if checkItems.get(equipOnlyId) != itemId:
                            continue
                        equipOnlyIds.add(equipOnlyId)
                    else:
                        checkItems.put(equipOnlyId, itemId)
            rs.close()
            ps.close()
            Collections.sort(equipOnlyIds)
            for i in equipOnlyIds:
                ps = con.prepareStatement("DELETE FROM inventoryitems WHERE equipOnlyId = ?")
                ps.setInt(1, i)
                ps.executeUpdate()
                ps.close()
                print("发现复制装备 该装备的唯一ID: " + i + " 已进行删除处理..")
                FileoutputUtil.log("装备复制.txt", "发现复制装备 该装备的唯一ID: " + i + " 已进行删除处理..")
        except Exception as ex:
            print("[EXCEPTION] 清理复制装备出现错误." + ex)

    def startServer(self) -> None:
        start = int(time.time() * 1000)
        checkSingleInstance()
        print("======================================")
        print(ServerProperties.getProperty("RoyMS.Admin"))
        print("========================")
        if bool(ServerProperties.getProperty("RoyMS.Admin")):
            printSection("[not not not 已开启只能管理员登录模式 not not not ]")
        if bool(ServerProperties.getProperty("RoyMS.AutoRegister")):
            print("加载 自动注册完成 :::")
        # try-with-resources: final PreparedStatement ps = DatabaseConnection.getConnection().prepareStatement("UPDATE accounts SET loggedin = 0")
        try:
            ps.executeUpdate()
        except Exception as ex:
            raise RuntimeError("[数据库异常] 请检查数据库链接。目前无法连接到MySQL数据库.")
        print("服务端 开始启动...")
        print("当前操作系统: " + os.environ.get("sun.desktop"))
        print("服务器地址: " + ServerProperties.getProperty("RoyMS.IP") + ":" + LoginServer.PORT)
        print("游戏版本: " + ServerConstants.MAPLE_TYPE + " v." + ServerConstants.MAPLE_VERSION + "." + ServerConstants.MAPLE_PATCH)
        World.init()
        runThread()
        loadData()
        print("加载\"登入\"服务...")
        LoginServer.run_startup_configurations()
        print("正在加载频道...")
        ChannelServer.startChannel_Main()
        print("频道加载完成!\r\n")
        print("正在加载商城...")
        CashShopServer.run_startup_configurations()
        printSection("刷怪线程")
        World.registerRespawn()
        Timer.CheatTimer.getInstance().register(AutobanManager.getInstance(), 60000)
        onlineTime(1)
        memoryRecical(360)
        MapleServerHandler.registerMBean()
        LoginServer.setOn()
        print("\r\n经验倍率：" + int(ServerProperties.getProperty("RoyMS.Exp")) + " 物品倍率：" + int(ServerProperties.getProperty("RoyMS.Drop")) + " 金币倍率：" + int(ServerProperties.getProperty("RoyMS.Meso")) + " BOSS爆率：" + int(ServerProperties.getProperty("RoyMS.BDrop")))
        if bool(ServerProperties.getProperty("RoyMS.检测复制装备", "False")):
            checkCopyItemFromSql()
        if bool(ServerProperties.getProperty("RoyMS.防万能检测", "False")):
            print("启动防万能检测")
            startCheck()
        now = int(time.time() * 1000) - start
        seconds = now / 1000
        ms = now % 1000
        print("加载完成, 耗时: " + seconds + "秒" + ms + "毫秒\r\n")
        print("服务端开启完毕，可以登入游戏了！")

    def CashGui(self) -> None:
        if Start.CashGui is not None:
            Start.CashGui.dispose()
        (Start.CashGui = RoyMS()).setVisible(True)

    def onlineStatistics(self, time: int) -> None:
        def _task_1():
            connected = World.getConnected()
            conStr = "" + " 在线人数: ")
            for i in connected.keys():
                if i == 0:
                    users = connected.get(i)
                    conStr.append(StringUtil.getRightPaddedStr(str(users), ' ', 3))
                    if users > Start.maxUsers:
                        Start.maxUsers = users
                    conStr.append(" 最高在线: ")
                    conStr.append(Start.maxUsers)
                    break
            print(conStr)
            if Start.maxUsers > 0:
                FileoutputUtil.log("logs/在线统计.log", conStr)

        print("服务端启用在线统计." + time + "分钟统计一次在线的人数信息.")
        Timer.WorldTimer.getInstance().register(_task_1, 60000 * time)

    def printSection(self, s: str) -> None:
        for (s = "-[ " + s + " ]"; s.encode("utf-8").length < 79; s = "=" + s) {}
        print(s)

    def startCheck(self) -> None:
        def _task_1():
            for cserv_ in ChannelServer.getAllInstances():
                for chr in cserv_.getPlayerStorage().getAllCharacters():
                    if chr is not None:
                        chr.startCheck()

        print("服务端启用检测.30秒检测一次角色是否与登录器断开连接.")
        Timer.WorldTimer.getInstance().register(_task_1, 30000)

    def memoryRecical(self, time: int) -> None:
        def _task_1():
            gc.collect()

        Timer.WorldTimer.getInstance().register(_task_1, 60000 * time)

    @staticmethod
    def run() -> None:
        Thread(ShutdownServer.getInstance()).start()


# Inner class from Java (originally nested)
class Shutdown(Runnable):
    """
    Class Shutdown
    Implements: Runnable
    """


    def run(self) -> None:
        Thread(ShutdownServer.getInstance()).start()

