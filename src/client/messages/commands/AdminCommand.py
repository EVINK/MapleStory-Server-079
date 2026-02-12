"""
AdminCommand - Converted from Java source
Original: client/messages/commands/AdminCommand.java
Package: client.messages.commands
"""

from concurrent.futures import Future
from datetime import datetime
from datetime import datetime, timezone, timedelta
from io import open
from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import asyncio
import math
import os
import pymysql
import sched
import threading

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.LoginCrypto import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from client.messages.CommandProcessorUtil import *  # TODO: import specific classes
# from client.messages.CopyItemInfo import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.handler.AutoRegister import *  # TODO: import specific classes
# from handling.world.CheaterData import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamily import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from scripting.EventManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from scripting.PortalScriptManager import *  # TODO: import specific classes
# from scripting.ReactorScriptManager import *  # TODO: import specific classes
# from server.CashItemFactory import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.MapleShopFactory import *  # TODO: import specific classes
# from server.ShutdownServer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.events.MapleEvent import *  # TODO: import specific classes
# from server.events.MapleEventType import *  # TODO: import specific classes
# from server.events.MapleOxQuizFactory import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MapleMonsterInformationProvider import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes
# from server.life.OverrideMonsterStats import *  # TODO: import specific classes
# from server.life.PlayerNPC import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.maps.MapleReactorFactory import *  # TODO: import specific classes
# from server.maps.MapleReactorStats import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.ArrayMap import *  # TODO: import specific classes
# from tools.CPUSampler import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.MockIOSession import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes


class AdminCommand:
    """
    Class AdminCommand
    """

    def __init__(self):
        self.minutesLeft = 0
        self.p = 0
        self.min = 0

    # Static initializer
    # Shutdown.t = None


    def getPlayerLevelRequired(self) -> Any:
        return ServerConstants.PlayerGMRank.ADMIN

    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        c.getPlayer().setDebugMessage(not c.getPlayer().getDebugMessage())
        return 1

    @staticmethod
    def execute_c_splitted(c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        mac = ""
        ip = ""
        acid = 0
        Systemban = False
        ACbanned = False
        IPbanned = False
        MACbanned = False
        reason = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select accountid from characters where name = ?")
            ps.setString(1, name)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    acid = rs.getInt("accountid")
            ps = con.prepareStatement("select banned, banreason, macs, Sessionip from accounts where id = ?")
            ps.setInt(1, acid)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    Systemban = (rs.getInt("banned") == 2)
                    ACbanned = (rs.getInt("banned") == 1 or rs.getInt("banned") == 2)
                    reason = rs.getString("banreason")
                    mac = rs.getString("macs")
                    ip = rs.getString("Sessionip")
            ps.close()
        except SQLException as ex:
        if reason is None or reason == "":
            reason = "?"
        if c.isBannedIP(ip):
            IPbanned = True
        if c.isBannedMac(mac):
            MACbanned = True
        c.getPlayer().dropMessage("玩家[" + name + "] 帐号ID[" + acid + "]是否被封锁: " + (ACbanned ? "是" : "否") + (Systemban ? "(系统自动封锁)" : "") + ", 原因: " + reason)
        c.getPlayer().dropMessage("IP: " + ip + " 是否在封锁IP名单: " + (IPbanned ? "是" : "否"))
        c.getPlayer().dropMessage("MAC: " + mac + " 是否在封锁MAC名单: " + (MACbanned ? "是" : "否"))
        return 1

    def getMessage(self) -> str:
        return "".append("not BanStatus <產嘿> - 琩產琌砆玛の")

    def execute(self, c: Any, splitted: list) -> int:
        def _task_1():
            if ShutdownTime.self.minutesLeft == 0:
                ShutdownServer.getInstance().run()
                ShutdownTime.t.start()
                ShutdownTime.ts.cancel(False)
                return
            message = ""
            message.append("[冒险岛公告] 服务器将在 ")
            message.append(ShutdownTime.self.minutesLeft)
            message.append("分钟后关闭. 请尽速关闭精灵商人 并下线.")
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, message).encode("utf-8"))
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage(message).encode("utf-8"))
            for cs in ChannelServer.getAllInstances():
                cs.setServerMessage("服务器将于 " + ShutdownTime.self.minutesLeft + " 分钟后开启")
            ShutdownTime.self.minutesLeft -= 1

        if len(splitted) < 2:
            return 0
        self.minutesLeft = int(splitted[1])
        c.getPlayer().dropMessage(6, "服务器将在 " + self.minutesLeft + "分钟后关闭. 请尽速关闭精灵商人 并下线.")
        if ShutdownTime.ts is None and (ShutdownTime.t is None or not ShutdownTime.t.isAlive()):
            ShutdownTime.t = Thread(ShutdownServer.getInstance())
            ShutdownTime.ts = Timer.EventTimer.getInstance().register(_task_1, 60000)
        else:
            c.getPlayer().dropMessage(6, "服务器关闭时间修改为 " + self.minutesLeft + "分钟后，请稍等服务器关闭")
        return 1

    def run(self) -> None:
        if ShutdownTime.self.minutesLeft == 0:
            ShutdownServer.getInstance().run()
            ShutdownTime.t.start()
            ShutdownTime.ts.cancel(False)
            return
        message = ""
        message.append("[冒险岛公告] 服务器将在 ")
        message.append(ShutdownTime.self.minutesLeft)
        message.append("分钟后关闭. 请尽速关闭精灵商人 并下线.")
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, message).encode("utf-8"))
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage(message).encode("utf-8"))
        for cs in ChannelServer.getAllInstances():
            cs.setServerMessage("服务器将于 " + ShutdownTime.self.minutesLeft + " 分钟后开启")
        ShutdownTime.self.minutesLeft -= 1

    def execute_c_splitted(self, c: Any, splitted: list) -> int:
        for cserv in ChannelServer.getAllInstances():
            chrs = cserv.getPlayerStorage().getAllCharactersThreadSafe()
            for chr in chrs:
                self.p += 1
                chr.saveToDB(False, False)
        c.getPlayer().dropMessage("[保存] " + self.p + "个玩家数据保存到数据中.")
        self.p = 0
        return 1


# Inner class from Java (originally nested)
class 开放地图(openmap):
    """
    Class 开放地图
    Extends: openmap
    """

    pass


# Inner class from Java (originally nested)
class 关闭地图(closemap):
    """
    Class 关闭地图
    Extends: closemap
    """

    pass


# Inner class from Java (originally nested)
class 注册(register):
    """
    Class 注册
    Extends: register
    """

    pass


# Inner class from Java (originally nested)
class 满属性(maxstats):
    """
    Class 满属性
    Extends: maxstats
    """

    pass


# Inner class from Java (originally nested)
class 最小属性(Minimumstats):
    """
    Class 最小属性
    Extends: Minimumstats
    """

    pass


# Inner class from Java (originally nested)
class 满技能(maxSkills):
    """
    Class 满技能
    Extends: maxSkills
    """

    pass


# Inner class from Java (originally nested)
class 拉全部(WarpAllHere):
    """
    Class 拉全部
    Extends: WarpAllHere
    """

    pass


# Inner class from Java (originally nested)
class 给金币(mesoEveryone):
    """
    Class 给金币
    Extends: mesoEveryone
    """

    pass


# Inner class from Java (originally nested)
class 给经验(ExpEveryone):
    """
    Class 给经验
    Extends: ExpEveryone
    """

    pass


# Inner class from Java (originally nested)
class 给所有人点卷(CashEveryone):
    """
    Class 给所有人点卷
    Extends: CashEveryone
    """

    pass


# Inner class from Java (originally nested)
class 刷新地图(ReloadMap):
    """
    Class 刷新地图
    Extends: ReloadMap
    """

    pass


# Inner class from Java (originally nested)
class 祝福(buff):
    """
    Class 祝福
    Extends: buff
    """

    pass


# Inner class from Java (originally nested)
class 倍率设置(setRate):
    """
    Class 倍率设置
    Extends: setRate
    """

    pass


# Inner class from Java (originally nested)
class 地图代码(WhereAmI):
    """
    Class 地图代码
    Extends: WhereAmI
    """

    pass


# Inner class from Java (originally nested)
class 刷(Item):
    """
    Class 刷
    Extends: Item
    """

    pass


# Inner class from Java (originally nested)
class 丢(Drop):
    """
    Class 丢
    Extends: Drop
    """

    pass


# Inner class from Java (originally nested)
class 全部复活(HealMap):
    """
    Class 全部复活
    Extends: HealMap
    """

    pass


# Inner class from Java (originally nested)
class 清怪(KillAll):
    """
    Class 清怪
    Extends: KillAll
    """

    pass


# Inner class from Java (originally nested)
class 设置人气(Fame):
    """
    Class 设置人气
    Extends: Fame
    """

    pass


# Inner class from Java (originally nested)
class 清除地板(cleardrops):
    """
    Class 清除地板
    Extends: cleardrops
    """

    pass


# Inner class from Java (originally nested)
class 召唤怪物(Spawn):
    """
    Class 召唤怪物
    Extends: Spawn
    """

    pass


# Inner class from Java (originally nested)
class 计时器(Clock):
    """
    Class 计时器
    Extends: Clock
    """

    pass


# Inner class from Java (originally nested)
class 自动注册(autoreg):
    """
    Class 自动注册
    Extends: autoreg
    """

    pass


# Inner class from Java (originally nested)
class 怪物代码(mob):
    """
    Class 怪物代码
    Extends: mob
    """

    pass


# Inner class from Java (originally nested)
class 封号状态(BanStatus):
    """
    Class 封号状态
    Extends: BanStatus
    """

    pass


# Inner class from Java (originally nested)
class 打开NPC(OpenNpc):
    """
    Class 打开NPC
    Extends: OpenNpc
    """

    pass


# Inner class from Java (originally nested)
class 打开商店(OpenShop):
    """
    Class 打开商店
    Extends: OpenShop
    """

    pass


# Inner class from Java (originally nested)
class Debug(CommandExecute):
    """
    Class Debug
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().setDebugMessage(not c.getPlayer().getDebugMessage())
        return 1


# Inner class from Java (originally nested)
class BanStatus(CommandExecute):
    """
    Class BanStatus
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        mac = ""
        ip = ""
        acid = 0
        Systemban = False
        ACbanned = False
        IPbanned = False
        MACbanned = False
        reason = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select accountid from characters where name = ?")
            ps.setString(1, name)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    acid = rs.getInt("accountid")
            ps = con.prepareStatement("select banned, banreason, macs, Sessionip from accounts where id = ?")
            ps.setInt(1, acid)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    Systemban = (rs.getInt("banned") == 2)
                    ACbanned = (rs.getInt("banned") == 1 or rs.getInt("banned") == 2)
                    reason = rs.getString("banreason")
                    mac = rs.getString("macs")
                    ip = rs.getString("Sessionip")
            ps.close()
        except SQLException as ex:
        if reason is None or reason == "":
            reason = "?"
        if c.isBannedIP(ip):
            IPbanned = True
        if c.isBannedMac(mac):
            MACbanned = True
        c.getPlayer().dropMessage("玩家[" + name + "] 帐号ID[" + acid + "]是否被封锁: " + (ACbanned ? "是" : "否") + (Systemban ? "(系统自动封锁)" : "") + ", 原因: " + reason)
        c.getPlayer().dropMessage("IP: " + ip + " 是否在封锁IP名单: " + (IPbanned ? "是" : "否"))
        c.getPlayer().dropMessage("MAC: " + mac + " 是否在封锁MAC名单: " + (MACbanned ? "是" : "否"))
        return 1

    def getMessage(self) -> str:
        return "".append("not BanStatus <產嘿> - 琩產琌砆玛の")


# Inner class from Java (originally nested)
class OpenNpc(CommandExecute):
    """
    Class OpenNpc
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().start(c, int(splitted[1]))
        return 1


# Inner class from Java (originally nested)
class OpenShop(CommandExecute):
    """
    Class OpenShop
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleShopFactory.getInstance().getShop(int(splitted[1]))
        return 1


# Inner class from Java (originally nested)
class SavePlayerShops(CommandExecute):
    """
    Class SavePlayerShops
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for cserv in ChannelServer.getAllInstances():
            cserv.closeAllMerchant()
        c.getPlayer().dropMessage(6, "雇佣商人储存完毕.")
        return 1


# Inner class from Java (originally nested)
class Shutdown(CommandExecute):
    """
    Class Shutdown
    Extends: CommandExecute
    """

    # Static initializer
    # Shutdown.t = None


    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(6, "关闭服务器...")
        if Shutdown.t is None or not Shutdown.t.isAlive():
            (Shutdown.t = Thread(ShutdownServer.getInstance())).start()
        else:
            c.getPlayer().dropMessage(6, "已在执行中...")
        return 1

    def getMessage(self) -> str:
        return "".append("not shutdown - 关闭服务器")


# Inner class from Java (originally nested)
class ShutdownTime(CommandExecute):
    """
    Class ShutdownTime
    Extends: CommandExecute
    """

    def __init__(self):
        self.minutesLeft = 0
        self.minutesLeft = 0

    # Static initializer
    # ShutdownTime.ts = None
    # ShutdownTime.t = None


    def execute(self, c: Any, splitted: list) -> int:
        def _task_1():
            if ShutdownTime.self.minutesLeft == 0:
                ShutdownServer.getInstance().run()
                ShutdownTime.t.start()
                ShutdownTime.ts.cancel(False)
                return
            message = ""
            message.append("[冒险岛公告] 服务器将在 ")
            message.append(ShutdownTime.self.minutesLeft)
            message.append("分钟后关闭. 请尽速关闭精灵商人 并下线.")
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, message).encode("utf-8"))
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage(message).encode("utf-8"))
            for cs in ChannelServer.getAllInstances():
                cs.setServerMessage("服务器将于 " + ShutdownTime.self.minutesLeft + " 分钟后开启")
            ShutdownTime.self.minutesLeft -= 1

        if len(splitted) < 2:
            return 0
        self.minutesLeft = int(splitted[1])
        c.getPlayer().dropMessage(6, "服务器将在 " + self.minutesLeft + "分钟后关闭. 请尽速关闭精灵商人 并下线.")
        if ShutdownTime.ts is None and (ShutdownTime.t is None or not ShutdownTime.t.isAlive()):
            ShutdownTime.t = Thread(ShutdownServer.getInstance())
            ShutdownTime.ts = Timer.EventTimer.getInstance().register(_task_1, 60000)
        else:
            c.getPlayer().dropMessage(6, "服务器关闭时间修改为 " + self.minutesLeft + "分钟后，请稍等服务器关闭")
        return 1

    def run(self) -> None:
        if ShutdownTime.self.minutesLeft == 0:
            ShutdownServer.getInstance().run()
            ShutdownTime.t.start()
            ShutdownTime.ts.cancel(False)
            return
        message = ""
        message.append("[冒险岛公告] 服务器将在 ")
        message.append(ShutdownTime.self.minutesLeft)
        message.append("分钟后关闭. 请尽速关闭精灵商人 并下线.")
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, message).encode("utf-8"))
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage(message).encode("utf-8"))
        for cs in ChannelServer.getAllInstances():
            cs.setServerMessage("服务器将于 " + ShutdownTime.self.minutesLeft + " 分钟后开启")
        ShutdownTime.self.minutesLeft -= 1

    def getMessage(self) -> str:
        return "".append("not shutdowntime <秒数> - 关闭服务器")


# Inner class from Java (originally nested)
class SaveAll(CommandExecute):
    """
    Class SaveAll
    Extends: CommandExecute
    """

    def __init__(self):
        self.p = 0
        self.p = 0


    def execute(self, c: Any, splitted: list) -> int:
        for cserv in ChannelServer.getAllInstances():
            chrs = cserv.getPlayerStorage().getAllCharactersThreadSafe()
            for chr in chrs:
                self.p += 1
                chr.saveToDB(False, False)
        c.getPlayer().dropMessage("[保存] " + self.p + "个玩家数据保存到数据中.")
        self.p = 0
        return 1

    def getMessage(self) -> str:
        return "".append("not saveall - 保存所有角色資料")


# Inner class from Java (originally nested)
class LowHP(CommandExecute):
    """
    Class LowHP
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getStat().setHp(1)
        c.getPlayer().getStat().setMp(1)
        c.getPlayer().updateSingleStat(MapleStat.HP, 1)
        c.getPlayer().updateSingleStat(MapleStat.MP, 1)
        return 1

    def getMessage(self) -> str:
        return "".append("not lowhp - 血魔归ㄧ")


# Inner class from Java (originally nested)
class Heal(CommandExecute):
    """
    Class Heal
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getStat().setHp(c.getPlayer().getStat().getCurrentMaxHp())
        c.getPlayer().getStat().setMp(c.getPlayer().getStat().getCurrentMaxMp())
        c.getPlayer().updateSingleStat(MapleStat.HP, c.getPlayer().getStat().getCurrentMaxHp())
        c.getPlayer().updateSingleStat(MapleStat.MP, c.getPlayer().getStat().getCurrentMaxMp())
        c.getPlayer().dispelDebuffs()
        return 1

    def getMessage(self) -> str:
        return "".append("not heal - 补满血魔")


# Inner class from Java (originally nested)
class UnbanIP(CommandExecute):
    """
    Class UnbanIP
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        ret_ = MapleClient.unbanIPMacs(splitted[1])
        if ret_ == -2:
            c.getPlayer().dropMessage(6, "[unbanip] SQL 错误.")
        elif ret_ == -1:
            c.getPlayer().dropMessage(6, "[unbanip] 角色不存在.")
        elif ret_ == 0:
            c.getPlayer().dropMessage(6, "[unbanip] No IP or Mac with that character exists!")
        elif ret_ == 1:
            c.getPlayer().dropMessage(6, "[unbanip] IP或Mac已解锁其中一個.")
        elif ret_ == 2:
            c.getPlayer().dropMessage(6, "[unbanip] IP以及Mac已成功解锁.")
        return 1

    def getMessage(self) -> str:
        return "".append("not unbanip <玩家名称> - 解锁玩家")


# Inner class from Java (originally nested)
class TempBan(CommandExecute):
    """
    Class TempBan
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        reason = int(splitted[2])
        numDay = int(splitted[3])
        cal = Calendar.getInstance()
        cal.add(5, numDay)
        df = DateFormat.getInstance()
        if victim is None:
            c.getPlayer().dropMessage(6, "[tempban] 找不到目标角色")
        else:
            victim.tempban("由" + c.getPlayer().getName() + "暂时锁定了", cal, reason, True)
            c.getPlayer().dropMessage(6, "[tempban] " + splitted[1] + " 已成功被暂时锁定至 " + df.format(cal.getTime()))
        return 1

    def getMessage(self) -> str:
        return "".append("not tempban <玩家名称> - 暂时锁定玩家")


# Inner class from Java (originally nested)
class Kill(CommandExecute):
    """
    Class Kill
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        if len(splitted) < 2:
            return 0
        for i in range(1, len(splitted)):
            name = splitted[1]
            ch = World.Find.findChannel(name)
            if ch <= 0:
                return 0
            victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
            if victim is None:
                c.getPlayer().dropMessage(6, "[kill] 玩家 " + splitted[i] + " 不存在.")
            elif player.allowedToTarget(victim):
                victim.getStat().setHp(0)
                victim.getStat().setMp(0)
                victim.updateSingleStat(MapleStat.HP, 0)
                victim.updateSingleStat(MapleStat.MP, 0)
        return 1

    def getMessage(self) -> str:
        return "".append("not kill <玩家名称1> <玩家名称2> ... - 杀掉玩家")


# Inner class from Java (originally nested)
class Skill(CommandExecute):
    """
    Class Skill
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        skill = SkillFactory.getSkill(int(splitted[1]))
        level = CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1)
        masterlevel = CommandProcessorUtil.getOptionalIntArg(splitted, 3, 1)
        if level > skill.getMaxLevel():
            level = skill.getMaxLevel()
        c.getPlayer().changeSkillLevel(skill, level, masterlevel)
        return 1

    def getMessage(self) -> str:
        return "".append("not skill <技能ID> [技能等級] [技能最大等級] ... - 学习技能")


# Inner class from Java (originally nested)
class Fame(CommandExecute):
    """
    Class Fame
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        if len(splitted) < 2:
            c.getPlayer().dropMessage("not fame <角色名称> <名声> ... - 名声")
            return 0
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        fame = None
        try:
            fame = Short.parseShort(splitted[2])
        except NumberFormatException as nfe:
            c.getPlayer().dropMessage(6, "不合法的数字")
            return 0
        if victim is not None and player.allowedToTarget(victim):
            victim.addFame(fame)
            victim.updateSingleStat(MapleStat.FAME, victim.getFame())
        else:
            c.getPlayer().dropMessage(6, "[fame] 角色不存在")
        return 1

    def getMessage(self) -> str:
        return "".append("not fame <角色名称> <名声> ... - 名声")


# Inner class from Java (originally nested)
class autoreg(CommandExecute):
    """
    Class autoreg
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage("目前自动注册已经 " + ServerConstants.ChangeAutoReg())
        return 1

    def getMessage(self) -> str:
        return "".append("not autoreg - 自动注册开关")


# Inner class from Java (originally nested)
class HealMap(CommandExecute):
    """
    Class HealMap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        for mch in player.getMap().getCharacters():
            if mch is not None:
                mch.getStat().setHp(mch.getStat().getMaxHp())
                mch.updateSingleStat(MapleStat.HP, mch.getStat().getMaxHp())
                mch.getStat().setMp(mch.getStat().getMaxMp())
                mch.updateSingleStat(MapleStat.MP, mch.getStat().getMaxMp())
                mch.dispelDebuffs()
        return 1

    def getMessage(self) -> str:
        return "not healmap - 治愈地图上所有的人"


# Inner class from Java (originally nested)
class GodMode(CommandExecute):
    """
    Class GodMode
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        if player.isInvincible():
            player.setInvincible(False)
            player.dropMessage(6, "无敌已经关闭")
        else:
            player.setInvincible(True)
            player.dropMessage(6, "无敌已经开启.")
        return 1

    def getMessage(self) -> str:
        return "".append("not godmode - 无敌开关")


# Inner class from Java (originally nested)
class GiveSkill(CommandExecute):
    """
    Class GiveSkill
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        skill = SkillFactory.getSkill(int(splitted[2]))
        level = CommandProcessorUtil.getOptionalIntArg(splitted, 3, 1)
        masterlevel = CommandProcessorUtil.getOptionalIntArg(splitted, 4, 1)
        if level > skill.getMaxLevel():
            level = skill.getMaxLevel()
        victim.changeSkillLevel(skill, level, masterlevel)
        return 1

    def getMessage(self) -> str:
        return "".append("not giveskill <玩家名称> <技能ID> [技能等級] [技能最大等級] - 给予技能")


# Inner class from Java (originally nested)
class SP(CommandExecute):
    """
    Class SP
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().setRemainingSp(CommandProcessorUtil.getOptionalIntArg(splitted, 1, 1))
        c.sendPacket(MaplePacketCreator.updateSp(c.getPlayer(), False))
        return 1

    def getMessage(self) -> str:
        return "".append("not sp [数量] - 增加SP")


# Inner class from Java (originally nested)
class AP(CommandExecute):
    """
    Class AP
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().setRemainingAp(CommandProcessorUtil.getOptionalIntArg(splitted, 1, 1))
        c.getPlayer().updateSingleStat(MapleStat.AVAILABLEAP, CommandProcessorUtil.getOptionalIntArg(splitted, 1, 1))
        return 1

    def getMessage(self) -> str:
        return "".append("not ap [数量] - 增加AP")


# Inner class from Java (originally nested)
class Shop(CommandExecute):
    """
    Class Shop
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        shop = MapleShopFactory.getInstance()
        shopId = None
        try:
            shopId = int(splitted[1])
        except NumberFormatException as ex:
            return 0
        if shop.getShop(shopId) is not None:
            shop.getShop(shopId).sendShop(c)
        else:
            c.getPlayer().dropMessage(5, "此商店ID不存在")
        return 1

    def getMessage(self) -> str:
        return "".append("not shop - 开启商店")


# Inner class from Java (originally nested)
class 关键时刻(CommandExecute):
    """
    Class 关键时刻
    Extends: CommandExecute
    """

    # Static initializer
    # 关键时刻.ts = None


    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        def _task_1():
            for cserv in ChannelServer.getAllInstances():
                for mch in cserv.getPlayerStorage().getAllCharacters():
                    if not c.getPlayer().isGM():
                        NPCScriptManager.getInstance().start(mch.getClient(), 9010010)
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "关键时刻已经开始了!not not ").encode("utf-8"))
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage("关键时刻已经开始了!not not ").encode("utf-8"))
            关键时刻.ts.cancel(False)
            关键时刻.ts = None

        if len(splitted) < 1:
            return 0
        if 关键时刻.ts is not None:
            关键时刻.ts.cancel(False)
            c.getPlayer().dropMessage(0, "原定的关键时刻已取消")
        minutesLeft = None
        try:
            minutesLeft = int(splitted[1])
        except NumberFormatException as ex:
            return 0
        if minutesLeft > 0:
            关键时刻.ts = Timer.EventTimer.getInstance().schedule(_task_1, minutesLeft * 60 * 1000)
            c.getPlayer().dropMessage(0, "关键时刻预定已完成")
        else:
            c.getPlayer().dropMessage(0, "设定的时间必须 > 0。")
        return 1

    def run(self) -> None:
        for cserv in ChannelServer.getAllInstances():
            for mch in cserv.getPlayerStorage().getAllCharacters():
                if not c.getPlayer().isGM():
                    NPCScriptManager.getInstance().start(mch.getClient(), 9010010)
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "关键时刻已经开始了!not not ").encode("utf-8"))
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage("关键时刻已经开始了!not not ").encode("utf-8"))
        关键时刻.ts.cancel(False)
        关键时刻.ts = None

    def getMessage(self) -> str:
        return "".append("not 关键时刻 <时间:分钟> - 关键时刻")


# Inner class from Java (originally nested)
class GainMaplePoint(CommandExecute):
    """
    Class GainMaplePoint
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        amount = int(splitted[1])
        name = splitted[2]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            return 0
        player = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if player is None:
            return 0
        player.modifyCSPoints(2, amount, True)
        msg = "[GM 密语] GM " + c.getPlayer().getName() + " 给了 " + player.getName() + " 枫叶点数 " + amount + "点"
        World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, msg).encode("utf-8"))
        return 1

    def getMessage(self) -> str:
        return "".append("not gainmaplepoint <數量> <玩家> - 取得枫叶点数")


# Inner class from Java (originally nested)
class GainPoint(CommandExecute):
    """
    Class GainPoint
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        amount = int(splitted[1])
        name = splitted[2]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            return 0
        player = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if player is None:
            return 0
        player.setPoints(player.getPoints() + amount)
        return 1

    def getMessage(self) -> str:
        return "".append("not gainpoint <數量> <玩家> - 取得Point")


# Inner class from Java (originally nested)
class GainVP(GainPoint):
    """
    Class GainVP
    Extends: GainPoint
    """

    pass


# Inner class from Java (originally nested)
class LevelUp(CommandExecute):
    """
    Class LevelUp
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().levelUp()
        else:
            up = 0
            try:
                up = int(splitted[1])
            except NumberFormatException as ex:
            for i in range(up):
                c.getPlayer().levelUp()
        c.getPlayer().setExp(0)
        c.getPlayer().updateSingleStat(MapleStat.EXP, 0)
        return 1

    def getMessage(self) -> str:
        return "".append("not levelup - 等級上升")


# Inner class from Java (originally nested)
class UnlockInv(CommandExecute):
    """
    Class UnlockInv
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        arrayMap = ArrayMap()
        add = False
        if len(splitted) < 2 or splitted[1] == ("全部"):
            for type in MapleInventoryType.values():
                for item in c.getPlayer().getInventory(type):
                    if ItemFlag.LOCK.check(item.getFlag()):
                        item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                        add = True
                        c.getPlayer().reloadC()
                        c.getPlayer().dropMessage(5, "已经解锁")
                    if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                        item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                        add = True
                        c.getPlayer().reloadC()
                        c.getPlayer().dropMessage(5, "已经解锁")
                    if add:
                    arrayMap.put(item, type)
                    add = False
        elif splitted[1] == ("已装备道具"):
            for item in c.getPlayer().getInventory(MapleInventoryType.EQUIPPED):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已經解鎖")
                if add:
                arrayMap.put(item, MapleInventoryType.EQUIP)
                add = False
        elif splitted[1] == ("武器"):
            for item in c.getPlayer().getInventory(MapleInventoryType.EQUIP):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if add:
                arrayMap.put(item, MapleInventoryType.EQUIP)
                add = False
        elif splitted[1] == ("消耗"):
            for item in c.getPlayer().getInventory(MapleInventoryType.USE):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if add:
                arrayMap.put(item, MapleInventoryType.USE)
                add = False
        elif splitted[1] == ("装饰"):
            for item in c.getPlayer().getInventory(MapleInventoryType.SETUP):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if add:
                arrayMap.put(item, MapleInventoryType.SETUP)
                add = False
        elif splitted[1] == ("其他"):
            for item in c.getPlayer().getInventory(MapleInventoryType.ETC):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if add:
                arrayMap.put(item, MapleInventoryType.ETC)
                add = False
        elif splitted[1] == ("特殊"):
            for item in c.getPlayer().getInventory(MapleInventoryType.CASH):
                if ItemFlag.LOCK.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.LOCK.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if ItemFlag.UNTRADEABLE.check(item.getFlag()):
                    item.setFlag((byte) (item.getFlag() - ItemFlag.UNTRADEABLE.getValue()))
                    add = True
                    c.getPlayer().reloadC()
                    c.getPlayer().dropMessage(5, "已经解锁")
                if add:
                arrayMap.put(item, MapleInventoryType.CASH)
                add = False
        else:
            return 0
        for (java.util.Map.Entry<IItem, MapleInventoryType> eq : arrayMap.items())
        c.getPlayer().forceReAddItem_NoUpdate((eq.getKey()).copy(), eq.getValue())
        return 1

    def getMessage(self) -> str:
        return "not unlockinv <全部/已装备道具/武器/消耗/装饰/其他/特殊> - 解锁道具"


# Inner class from Java (originally nested)
class Item(CommandExecute):
    """
    Class Item
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        itemId = 0
        try:
            itemId = int(splitted[1])
        except NumberFormatException as ex:
        quantity = CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1)
        ii = MapleItemInformationProvider.getInstance()
        if GameConstants.isPet(itemId):
            pet = MaplePet.createPet(itemId, MapleInventoryIdentifier.getInstance())
            if pet is not None:
                MapleInventoryManipulator.addById(c, itemId, 1, c.getPlayer().getName(), pet, 90, 0)
        elif not ii.itemExists(itemId):
            c.getPlayer().dropMessage(5, itemId + " - 物品不存在")
        else:
            flag = 0
            flag |= ItemFlag.LOCK.getValue()
            item = None
            if GameConstants.getInventoryType(itemId) == MapleInventoryType.EQUIP:
                item = ii.randomizeStats(ii.getEquipById(itemId))
            else:
                item = new client.inventory.Item(itemId, 0, quantity, 0)
                if GameConstants.getInventoryType(itemId) != MapleInventoryType.USE:
            item.setOwner(c.getPlayer().getName())
            item.setGMLog(c.getPlayer().getName())
            MapleInventoryManipulator.addbyItem(c, item)
        return 1

    def getMessage(self) -> str:
        return "".append("not item <道具ID> - 取得道具")


# Inner class from Java (originally nested)
class serverMsg(CommandExecute):
    """
    Class serverMsg
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 1:
            sb = ""
            sb.append(StringUtil.joinStringFrom(splitted, 1))
            for ch in ChannelServer.getAllInstances():
                ch.setServerMessage(sb)
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverMessage(sb).encode("utf-8"))
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not servermsg 讯息 - 更改上方黃色公告")


# Inner class from Java (originally nested)
class Letter(CommandExecute):
    """
    Class Letter
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        nstart = None
        if len(splitted) < 3:
            c.getPlayer().dropMessage(6, "指令规则: ")
            return 0
        if splitted[1].lower() == "green".lower():
            start = 3991026
            nstart = 3990019
        elif splitted[1].lower() == "red".lower():
            start = 3991000
            nstart = 3990009
        else:
            c.getPlayer().dropMessage(6, "未知的顏色!")
            return 1
        splitString = StringUtil.joinStringFrom(splitted, 2)
        chars = []
        splitString = splitString.upper()
        for i in range(splitString):
            chr = splitString[i]
            if chr == ' ':
                chars.add(Integer.valueOf(-1))
            elif chr >= 'A' and chr <= 'Z':
                chars.add(Integer.valueOf(chr))
            elif chr >= '0' and chr <= '9':
                chars.add(Integer.valueOf(chr + 200))
        w = 32
        dStart = (c.getPlayer().getPosition()).x - splitString / 2 * w
        for integer in chars:
            if integer == -1:
                dStart += w
                continue
            if integer < 200:
                val = start + integer - 65
                client.inventory.Item item = new client.inventory.Item(val, 0, 1)
                c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), item, Point(dStart, (c.getPlayer().getPosition()).y), False, False)
                dStart += w
                continue
            if integer >= 200 and integer <= 300:
                val = nstart + integer - 48 - 200
                client.inventory.Item item = new client.inventory.Item(val, 0, 1)
                c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), item, Point(dStart, (c.getPlayer().getPosition()).y), False, False)
                dStart += w
        return 1

    def getMessage(self) -> str:
        return " not letter <color (green/red)> <word> - 送信"


# Inner class from Java (originally nested)
class Marry(CommandExecute):
    """
    Class Marry
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
        return 0
        itemId = int(splitted[2])
        if not GameConstants.isEffectRing(itemId):
            c.getPlayer().dropMessage(6, "错误的戒指ID.")
        else:
            name = splitted[1]
            ch = World.Find.findChannel(name)
            if ch <= 0:
                c.getPlayer().dropMessage(6, "玩家必须在线")
                return 0
            fff = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
            if fff is None:
                c.getPlayer().dropMessage(6, "玩家必须在线")
            else:
                ringID = {MapleInventoryIdentifier.getInstance(), MapleInventoryIdentifier.getInstance()}
                try:
                    chrz = {fff, c.getPlayer()}
                    for i in range(len(chrz)):
                        eq = MapleItemInformationProvider.getInstance().getEquipById(itemId)
                        if eq is None:
                            c.getPlayer().dropMessage(6, "错误的戒指ID.")
                            return 1
                        eq.setUniqueId(ringID[i])
                        MapleInventoryManipulator.addbyItem(chrz[i].getClient(), eq.copy())
                        chrz[i].dropMessage(6, "成功与 " + chrz[(i == 0) ? 1 : 0].getName() + " 结婚")
                    MapleRing.addToDB(itemId, c.getPlayer(), fff.getName(), fff.getId(), ringID)
                except SQLException as sQLException:
                    sQLException.printStackTrace()
        return 1

    def getMessage(self) -> str:
        return "not marry <玩家名称> <戒指代码> - 结婚"


# Inner class from Java (originally nested)
class ItemCheck(CommandExecute):
    """
    Class ItemCheck
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3 or splitted[1] is None or splitted[1] == ("") or splitted[2] is None or splitted[2] == (""):
            return 0
        item = int(splitted[2])
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        itemamount = chr.getItemQuantity(item, True)
        if itemamount > 0:
            c.getPlayer().dropMessage(6, chr.getName() + " 有 " + itemamount + " (" + item + ").")
        else:
            c.getPlayer().dropMessage(6, chr.getName() + " 并沒有 (" + item + ")")
        return 1

    def getMessage(self) -> str:
        return "".append("not itemcheck <playername> <itemid> - 检查物品")


# Inner class from Java (originally nested)
class MobVac(CommandExecute):
    """
    Class MobVac
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for mmo in c.getPlayer().getMap().getAllMonstersThreadsafe():
            monster = mmo
            c.getPlayer().getMap().broadcastMessage(MobPacket.moveMonster(False, -1, 0, 0, 0, 0, monster.getObjectId(), monster.getPosition(), c.getPlayer().getPosition(), c.getPlayer().getLastRes()))
            monster.setPosition(c.getPlayer().getPosition())
        return 1

    def getMessage(self) -> str:
        return "".append("not mobvac - 全图吸怪")


# Inner class from Java (originally nested)
class Song(CommandExecute):
    """
    Class Song
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.musicChange(splitted[1]))
        return 1

    def getMessage(self) -> str:
        return "".append("not song - 播放音乐")


# Inner class from Java (originally nested)
class 开启自动活动(CommandExecute):
    """
    Class 开启自动活动
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        em = c.getChannelServer().getEventSM().getEventManager("AutomatedEvent")
        if em is not None:
            em.scheduleRandomEvent()
        return 1

    def getMessage(self) -> str:
        return "".append("not 开启自动活动 - 开启自动活动")


# Inner class from Java (originally nested)
class 活动开始(CommandExecute):
    """
    Class 活动开始
    Extends: CommandExecute
    """

    def __init__(self):
        self.min = 0
        self.min = 1

    # Static initializer
    # 活动开始.ts = None


    def execute(self, c: Any, splitted: list) -> int:
        def _task_1():
            if 活动开始.self.min == 0:
                MapleEvent.onStartEvent(c.getPlayer())
                活动开始.ts.cancel(False)
                return
            活动开始.self.min -= 1

        if c.getChannelServer().getEvent() == c.getPlayer().getMapId():
            MapleEvent.setEvent(c.getChannelServer(), False)
            c.getPlayer().dropMessage(5, "已经关闭活动入口，可以使用 not 活动开始 來启动。")
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "頻道:" + c.getChannel() + "活动目前已经关闭大门口。").encode("utf-8"))
            c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.getClock(60))
            活动开始.ts = Timer.EventTimer.getInstance().register(_task_1, 60000)
            return 1
        c.getPlayer().dropMessage(5, "您必须先使用 not 选择活动 设定當前頻道的活动，并在当前頻道活动地图里使用。")
        return 1

    def run(self) -> None:
        if 活动开始.self.min == 0:
            MapleEvent.onStartEvent(c.getPlayer())
            活动开始.ts.cancel(False)
            return
        活动开始.self.min -= 1

    def getMessage(self) -> str:
        return "".append("not 活动开始 - 活动开始")


# Inner class from Java (originally nested)
class 关闭活动入口(CommandExecute):
    """
    Class 关闭活动入口
    Extends: CommandExecute
    """

    # Static initializer
    # 关闭活动入口.tt = False


    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        def _task_1():
            关闭活动入口.tt = True

        if c.getChannelServer().getEvent() == c.getPlayer().getMapId():
            MapleEvent.setEvent(c.getChannelServer(), False)
            c.getPlayer().dropMessage(5, "已经关闭活动入口，可以使用 not 活动开始 來启动。")
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "頻道:" + c.getChannel() + "活动目前已经关闭大门口。").encode("utf-8"))
            c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.getClock(60))
            Timer.EventTimer.getInstance().register(_task_1, 60000)
            if 关闭活动入口.tt:
                MapleEvent.onStartEvent(c.getPlayer())
            return 1
        c.getPlayer().dropMessage(5, "您必须先使用 not 选择活动 设定当前頻道的活动，并在当前頻道活动地图里使用。")
        return 1

    def run(self) -> None:
        关闭活动入口.tt = True

    def getMessage(self) -> str:
        return "".append("not 关闭活动入口 -关闭活动入口")


# Inner class from Java (originally nested)
class 选择活动(CommandExecute):
    """
    Class 选择活动
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        type = MapleEventType.getByString(splitted[1])
        if type is None:
            sb = ""
            for t in MapleEventType.values():
                sb.append(t.name()).append(",")
            c.getPlayer().dropMessage(5, sb[0:sb.__len__(] - 1))
        msg = MapleEvent.scheduleEvent(type, c.getChannelServer())
        if msg > 0:
            c.getPlayer().dropMessage(5, msg)
        return 1

    def getMessage(self) -> str:
        return "".append("not 选择活动 - 选择活动")


# Inner class from Java (originally nested)
class RemoveItem(CommandExecute):
    """
    Class RemoveItem
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        name = splitted[1]
        id = int(splitted[2])
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        chr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if chr is None:
            c.getPlayer().dropMessage(6, "此玩家并不存在")
        else:
            chr.removeAll(id)
            c.getPlayer().dropMessage(6, "所有ID为 " + id + " 的道具已经从 " + name + " 身上被移除了")
        return 1

    def getMessage(self) -> str:
        return "".append("not removeitem <角色名称> <物品ID> - 移除玩家身上的道具")


# Inner class from Java (originally nested)
class KillMap(CommandExecute):
    """
    Class KillMap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for map in c.getPlayer().getMap().getCharactersThreadsafe():
            if map is not None and not map.isGM():
                map.getStat().setHp(0)
                map.getStat().setMp(0)
                map.updateSingleStat(MapleStat.HP, 0)
                map.updateSingleStat(MapleStat.MP, 0)
        return 1

    def getMessage(self) -> str:
        return "".append("not killmap - 杀掉所有玩家")


# Inner class from Java (originally nested)
class SpeakMega(CommandExecute):
    """
    Class SpeakMega
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        victim = None
        if len(splitted) >= 2:
            victim = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
        try:
            World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(3, (victim is None) ? c.getChannel() : victim.getClient().getChannel(), (victim is None) ? splitted[1] : (victim.getName() + " : " + StringUtil.joinStringFrom(splitted, 2)), True).encode("utf-8"))
        except Exception as e:
            return 0
        return 1

    def getMessage(self) -> str:
        return "".append("not speakmega [玩家名称] <讯息> - 对某个玩家的頻道进行广播")


# Inner class from Java (originally nested)
class Speak(CommandExecute):
    """
    Class Speak
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if victim is None:
            c.getPlayer().dropMessage(5, "找不到 '" + splitted[1])
            return 0
        victim.getMap().broadcastMessage(MaplePacketCreator.getChatText(victim.getId(), StringUtil.joinStringFrom(splitted, 2), victim.isGM(), 0))
        return 1

    def getMessage(self) -> str:
        return "".append("not speak <玩家名称> <讯息> - 对某个玩家发信息")


# Inner class from Java (originally nested)
class SpeakMap(CommandExecute):
    """
    Class SpeakMap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for victim in c.getPlayer().getMap().getCharactersThreadsafe():
            if victim.getId() != c.getPlayer().getId():
                victim.getMap().broadcastMessage(MaplePacketCreator.getChatText(victim.getId(), StringUtil.joinStringFrom(splitted, 1), victim.isGM(), 0))
        return 1

    def getMessage(self) -> str:
        return "".append("not speakmap <讯息> - 对目前地图进行发送信息")


# Inner class from Java (originally nested)
class SpeakChannel(CommandExecute):
    """
    Class SpeakChannel
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for victim in c.getChannelServer().getPlayerStorage().getAllCharacters():
            if victim.getId() != c.getPlayer().getId():
                victim.getMap().broadcastMessage(MaplePacketCreator.getChatText(victim.getId(), StringUtil.joinStringFrom(splitted, 1), victim.isGM(), 0))
        return 1

    def getMessage(self) -> str:
        return "".append("not speakchannel <讯息> - 对目前频道进行发送信息")


# Inner class from Java (originally nested)
class SpeakWorld(CommandExecute):
    """
    Class SpeakWorld
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for cserv in ChannelServer.getAllInstances():
            for victim in cserv.getPlayerStorage().getAllCharacters():
                if victim.getId() != c.getPlayer().getId():
                    victim.getMap().broadcastMessage(MaplePacketCreator.getChatText(victim.getId(), StringUtil.joinStringFrom(splitted, 1), victim.isGM(), 0))
        return 1

    def getMessage(self) -> str:
        return "".append("not speakchannel <讯息> - 对目前服务器进行传送信息")


# Inner class from Java (originally nested)
class Disease(CommandExecute):
    """
    Class Disease
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        type = None
        if len(splitted) < 3:
        return 0
        if splitted[1].lower() == "SEAL".lower():
            type = 120
        elif splitted[1].lower() == "DARKNESS".lower():
            type = 121
        elif splitted[1].lower() == "WEAKEN".lower():
            type = 122
        elif splitted[1].lower() == "STUN".lower():
            type = 123
        elif splitted[1].lower() == "CURSE".lower():
            type = 124
        elif splitted[1].lower() == "POISON".lower():
            type = 125
        elif splitted[1].lower() == "SLOW".lower():
            type = 126
        elif splitted[1].lower() == "SEDUCE".lower():
            type = 128
        elif splitted[1].lower() == "REVERSE".lower():
            type = 132
        elif splitted[1].lower() == "ZOMBIFY".lower():
            type = 133
        elif splitted[1].lower() == "POTION".lower():
            type = 134
        elif splitted[1].lower() == "SHADOW".lower():
            type = 135
        elif splitted[1].lower() == "BLIND".lower():
            type = 136
        elif splitted[1].lower() == "FREEZE".lower():
            type = 137
        else:
            return 0
        dis = MapleDisease.getBySkill(type)
        if len(splitted) == 4:
            name = splitted[2]
            ch = World.Find.findChannel(name)
            if ch <= 0:
                c.getPlayer().dropMessage(6, "玩家必须在线")
                return 0
            victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
            if victim is None:
                c.getPlayer().dropMessage(5, "找不到此玩家")
            else:
                victim.setChair(0)
                victim.getClient().sendPacket(MaplePacketCreator.cancelChair(-1))
                victim.getMap().broadcastMessage(victim, MaplePacketCreator.showChair(c.getPlayer().getId(), 0), False)
                victim.giveDebuff(dis, MobSkillFactory.getMobSkill(type, CommandProcessorUtil.getOptionalIntArg(splitted, 3, 1)))
        else:
            for victim in c.getPlayer().getMap().getCharactersThreadsafe():
                victim.setChair(0)
                victim.getClient().sendPacket(MaplePacketCreator.cancelChair(-1))
                victim.getMap().broadcastMessage(victim, MaplePacketCreator.showChair(c.getPlayer().getId(), 0), False)
                victim.giveDebuff(dis, MobSkillFactory.getMobSkill(type, CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1)))
        return 1

    def getMessage(self) -> str:
        return "not disease <SEAL/DARKNESS/WEAKEN/STUN/CURSE/POISON/SLOW/SEDUCE/REVERSE/ZOMBIFY/POTION/SHADOW/BLIND/FREEZE> [角色名称] <状态等级> - 让人得到特殊状态"


# Inner class from Java (originally nested)
class SendAllNote(CommandExecute):
    """
    Class SendAllNote
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) >= 1:
            text = StringUtil.joinStringFrom(splitted, 1)
            for mch in c.getChannelServer().getPlayerStorage().getAllCharacters():
                c.getPlayer().sendNote(mch.getName(), text)
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not sendallnote <文字> 传送Note給目前頻道的所有人")


# Inner class from Java (originally nested)
class giveMeso(CommandExecute):
    """
    Class giveMeso
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        gain = int(splitted[2])
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if victim is None:
            c.getPlayer().dropMessage(5, "找不到 '" + name)
        else:
            victim.gainMeso(gain, True)
            msg = "[GM 密语] GM " + c.getPlayer().getName() + " 给了 " + victim.getName() + " 金币 " + gain + "点"
            World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, msg).encode("utf-8"))
        return 1

    def getMessage(self) -> str:
        return "".append("not gainmeso <名字> <数量> - 給玩家金币")


# Inner class from Java (originally nested)
class CloneMe(CommandExecute):
    """
    Class CloneMe
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().cloneLook()
        return 1

    def getMessage(self) -> str:
        return "".append("not cloneme - 产生克隆体")


# Inner class from Java (originally nested)
class DisposeClones(CommandExecute):
    """
    Class DisposeClones
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(6, c.getPlayer().getCloneSize() + "个克隆体消失了.")
        c.getPlayer().disposeClones()
        return 1

    def getMessage(self) -> str:
        return "".append("not disposeclones - 摧毁克隆体")


# Inner class from Java (originally nested)
class Monitor(CommandExecute):
    """
    Class Monitor
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        target = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
        if target is not None:
            if target.getClient().isMonitored():
                target.getClient().setMonitored(False)
                c.getPlayer().dropMessage(5, "Not monitoring " + target.getName() + " anymore.")
            else:
                target.getClient().setMonitored(True)
                c.getPlayer().dropMessage(5, "Monitoring " + target.getName() + ".")
        else:
            c.getPlayer().dropMessage(5, "找不到该玩家")
        return 1

    def getMessage(self) -> str:
        return "".append("not monitor <玩家> - 记录玩家资讯")


# Inner class from Java (originally nested)
class PermWeather(CommandExecute):
    """
    Class PermWeather
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if c.getPlayer().getMap().getPermanentWeather() > 0:
            c.getPlayer().getMap().setPermanentWeather(0)
            c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.removeMapEffect())
            c.getPlayer().dropMessage(5, "地图天气已被禁用.")
        else:
            weather = CommandProcessorUtil.getOptionalIntArg(splitted, 1, 5120000)
            if not MapleItemInformationProvider.getInstance().itemExists(weather) or weather / 10000 != 512:
                c.getPlayer().dropMessage(5, "无效的ID.")
            else:
                c.getPlayer().getMap().setPermanentWeather(weather)
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.startMapEffect("", weather, False))
                c.getPlayer().dropMessage(5, "地图天气已启用.")
        return 1

    def getMessage(self) -> str:
        return "".append("not permweather - 设定天气")


# Inner class from Java (originally nested)
class CharInfo(CommandExecute):
    """
    Class CharInfo
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        builder = ""
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        other = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if other is None:
            builder.append("角色不存在")
            c.getPlayer().dropMessage(6, builder)
        else:
            if other.getClient().getLastPing() <= 0:
                other.getClient().sendPing()
            builder.append(MapleClient.getLogMessage(other, ""))
            builder.append(" 在 ").append(other.getPosition().x)
            builder.append(" /").append(other.getPosition().y)
            builder.append(" or 血量 : ")
            builder.append(other.getStat().getHp())
            builder.append(" /")
            builder.append(other.getStat().getCurrentMaxHp())
            builder.append(" or 魔量 : ")
            builder.append(other.getStat().getMp())
            builder.append(" /")
            builder.append(other.getStat().getCurrentMaxMp())
            builder.append(" or 物理攻擊力 : ")
            builder.append(other.getStat().getTotalWatk())
            builder.append(" or 魔法攻擊力 : ")
            builder.append(other.getStat().getTotalMagic())
            builder.append(" or 最高攻擊 : ")
            builder.append(other.getStat().getCurrentMaxBaseDamage())
            builder.append(" or 攻擊%數 : ")
            builder.append(other.getStat().dam_r)
            builder.append(" or BOSS攻擊%數 : ")
            builder.append(other.getStat().bossdam_r)
            builder.append(" or 力量 : ")
            builder.append(other.getStat().getStr())
            builder.append(" or 敏捷 : ")
            builder.append(other.getStat().getDex())
            builder.append(" or 智力 : ")
            builder.append(other.getStat().getInt())
            builder.append(" or 幸運 : ")
            builder.append(other.getStat().getLuk())
            builder.append(" or 全部力量 : ")
            builder.append(other.getStat().getTotalStr())
            builder.append(" or 全部敏捷 : ")
            builder.append(other.getStat().getTotalDex())
            builder.append(" or 全部智力 : ")
            builder.append(other.getStat().getTotalInt())
            builder.append(" or 全部幸運 : ")
            builder.append(other.getStat().getTotalLuk())
            builder.append(" or 經驗值 : ")
            builder.append(other.getExp())
            builder.append(" or 組隊狀態 : ")
            builder.append(other.getParty() is not None)
            builder.append(" or 交易狀態: ")
            builder.append(other.getTrade() is not None)
            builder.append(" or Latency: ")
            builder.append(other.getClient().getLatency())
            builder.append(" or 最後PING: ")
            builder.append(other.getClient().getLastPing())
            builder.append(" or 最後PONG: ")
            builder.append(other.getClient().getLastPong())
            builder.append(" or IP: ")
            builder.append(other.getClient().getSessionIPAddress())
            other.getClient().DebugMessage(builder)
            c.getPlayer().dropMessage(6, builder)
        return 1

    def getMessage(self) -> str:
        return "".append("not charinfo <角色名称> - 查看角色状态")


# Inner class from Java (originally nested)
class whoishere(CommandExecute):
    """
    Class whoishere
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        builder = ""
        for chr in c.getPlayer().getMap().getCharactersThreadsafe():
            if builder > 150:
                builder.setLength(builder - 2)
                c.getPlayer().dropMessage(6, builder)
                builder = ""
            builder.append(MapleCharacterUtil.makeMapleReadable(chr.getName()))
            builder.append(", ")
        builder.setLength(builder - 2)
        c.getPlayer().dropMessage(6, builder)
        return 1

    def getMessage(self) -> str:
        return "".append("not whoishere - 查看目前地图上的玩家")


# Inner class from Java (originally nested)
class Cheaters(CommandExecute):
    """
    Class Cheaters
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        cheaters = World.getCheaters()
        x = cheaters - 1
        while x >= 0:
            cheater = cheaters.get(x)
            c.getPlayer().dropMessage(6, cheater.getInfo())
        return 1

    def getMessage(self) -> str:
        return "".append("not cheaters - 查看作弊角色")


# Inner class from Java (originally nested)
class Connected(CommandExecute):
    """
    Class Connected
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        final java.util.Map<Integer, Integer> connected = World.getConnected()
        conStr = ""
        first = True
        for i in connected.keys():
            if not first:
                conStr.append(", ")
            else:
                first = False
            if i == 0:
                conStr.append("所有: ")
                conStr.append(connected.get(i))
            else:
                conStr.append("頻道 ")
                conStr.append(i)
                conStr.append(": ")
                conStr.append(connected.get(i))
        c.getPlayer().dropMessage(6, conStr)
        return 1

    def getMessage(self) -> str:
        return "".append("not connected - 查看已连线的客戶端")


# Inner class from Java (originally nested)
class ResetQuest(CommandExecute):
    """
    Class ResetQuest
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        MapleQuest.getInstance(int(splitted[1])).forfeit(c.getPlayer())
        return 1

    def getMessage(self) -> str:
        return "".append("not resetquest <任务ID> - 重置任务")


# Inner class from Java (originally nested)
class StartQuest(CommandExecute):
    """
    Class StartQuest
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        MapleQuest.getInstance(int(splitted[1])).start(c.getPlayer(), int(splitted[2]))
        return 1

    def getMessage(self) -> str:
        return "".append("not startquest <任务ID> - 开始任务")


# Inner class from Java (originally nested)
class CompleteQuest(CommandExecute):
    """
    Class CompleteQuest
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        MapleQuest.getInstance(int(splitted[1])).complete(c.getPlayer(), int(splitted[2]), int(splitted[3]))
        return 1

    def getMessage(self) -> str:
        return "".append("not completequest <任务ID> - 完成任务")


# Inner class from Java (originally nested)
class FStartQuest(CommandExecute):
    """
    Class FStartQuest
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        MapleQuest.getInstance(int(splitted[1])).forceStart(c.getPlayer(), int(splitted[2]), (len(splitted) >= 4) ? splitted[3] : None)
        return 1

    def getMessage(self) -> str:
        return "".append("not fstartquest <任务ID> - 强制开始任务")


# Inner class from Java (originally nested)
class FCompleteQuest(CommandExecute):
    """
    Class FCompleteQuest
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        MapleQuest.getInstance(int(splitted[1])).forceComplete(c.getPlayer(), int(splitted[2]))
        return 1

    def getMessage(self) -> str:
        return "".append("not fcompletequest <任务ID> - 强制完成任务")


# Inner class from Java (originally nested)
class FStartOther(CommandExecute):
    """
    Class FStartOther
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleQuest.getInstance(int(splitted[2])).forceStart(c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1]), int(splitted[3]), (len(splitted) >= 4) ? splitted[4] : None)
        return 1

    def getMessage(self) -> str:
        return "".append("not fstartother - 不知道啥")


# Inner class from Java (originally nested)
class FCompleteOther(CommandExecute):
    """
    Class FCompleteOther
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleQuest.getInstance(int(splitted[2])).forceComplete(c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1]), int(splitted[3]))
        return 1

    def getMessage(self) -> str:
        return "".append("not fcompleteother - 不知道啥")


# Inner class from Java (originally nested)
class NearestPortal(CommandExecute):
    """
    Class NearestPortal
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        portal = c.getPlayer().getMap().findClosestSpawnpoint(c.getPlayer().getPosition())
        c.getPlayer().dropMessage(6, portal.getName() + " id: " + portal.getId() + " script: " + portal.getScriptName())
        return 1

    def getMessage(self) -> str:
        return "".append("not nearestportal - 不知道啥")


# Inner class from Java (originally nested)
class SpawnDebug(CommandExecute):
    """
    Class SpawnDebug
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(6, c.getPlayer().getMap().spawnDebug())
        return 1

    def getMessage(self) -> str:
        return "".append("not spawndebug - debug怪物出生")


# Inner class from Java (originally nested)
class Threads(CommandExecute):
    """
    Class Threads
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        threads = new Thread[Thread.activeCount()]
        Thread.enumerate(threads)
        filter = ""
        if len(splitted) > 1:
            filter = splitted[1]
        for i in range(len(threads)):
            tstring = threads[i]
            if tstring.lower().__contains__(filter.lower()):
                c.getPlayer().dropMessage(6, i + ": " + tstring)
        return 1

    def getMessage(self) -> str:
        return "".append("not threads - 查看Threads资讯")


# Inner class from Java (originally nested)
class ShowTrace(CommandExecute):
    """
    Class ShowTrace
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        threads = new Thread[Thread.activeCount()]
        Thread.enumerate(threads)
        t = threads[int(splitted[1])]
        c.getPlayer().dropMessage(6, t + ":")
        for elem in t.getStackTrace():
            c.getPlayer().dropMessage(6, elem)
        return 1

    def getMessage(self) -> str:
        return "".append("not showtrace - show trace info")


# Inner class from Java (originally nested)
class FakeRelog(CommandExecute):
    """
    Class FakeRelog
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        c.sendPacket(MaplePacketCreator.getCharInfo(player))
        player.getMap().removePlayer(player)
        player.getMap().addPlayer(player)
        return 1

    def getMessage(self) -> str:
        return "".append("not fakerelog - 假登出再登入")


# Inner class from Java (originally nested)
class ToggleOffense(CommandExecute):
    """
    Class ToggleOffense
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        try:
            co = CheatingOffense.valueOf(splitted[1])
            co.setEnabled(not co.isEnabled())
        except IllegalArgumentException as iae:
            c.getPlayer().dropMessage(6, "Offense " + splitted[1] + " not found")
        return 1

    def getMessage(self) -> str:
        return "".append("not toggleoffense <Offense> - 开启或关闭CheatOffense")


# Inner class from Java (originally nested)
class toggleDrop(CommandExecute):
    """
    Class toggleDrop
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().toggleDrops()
        return 1

    def getMessage(self) -> str:
        return "".append("not toggledrop - 开启或关闭掉落")


# Inner class from Java (originally nested)
class ToggleMegaphone(CommandExecute):
    """
    Class ToggleMegaphone
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        World.toggleMegaphoneMuteState()
        c.getPlayer().dropMessage(6, "广播是否封锁 : " + (c.getChannelServer().getMegaphoneMuteState() ? "是" : "否"))
        return 1

    def getMessage(self) -> str:
        return "".append("not togglemegaphone - 开启或者关闭广播")


# Inner class from Java (originally nested)
class SpawnReactor(CommandExecute):
    """
    Class SpawnReactor
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        id = 0
        try:
            id = int(splitted[1])
        except NumberFormatException as ex:
        reactorSt = MapleReactorFactory.getReactor(id)
        reactor = MapleReactor(reactorSt, id)
        reactor.setDelay(-1)
        reactor.setPosition(c.getPlayer().getPosition())
        c.getPlayer().getMap().spawnReactor(reactor)
        return 1

    def getMessage(self) -> str:
        return "".append("not spawnreactor - 设立Reactor")


# Inner class from Java (originally nested)
class HReactor(CommandExecute):
    """
    Class HReactor
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        c.getPlayer().getMap().getReactorByOid(int(splitted[1])).hitReactor(c)
        return 1

    def getMessage(self) -> str:
        return "".append("not hitreactor - 触碰Reactor")


# Inner class from Java (originally nested)
class DestroyReactor(CommandExecute):
    """
    Class DestroyReactor
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        map = c.getPlayer().getMap()
        reactors = map.getMapObjectsInRange(c.getPlayer().getPosition(), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.REACTOR))
        if splitted[1] == ("all"):
            for reactorL in reactors:
                reactor2l = reactorL
                c.getPlayer().getMap().destroyReactor(reactor2.getObjectId())
        else:
            c.getPlayer().getMap().destroyReactor(int(splitted[1]))
        return 1

    def getMessage(self) -> str:
        return "".append("not drstroyreactor - 移除Reactor")


# Inner class from Java (originally nested)
class ResetReactors(CommandExecute):
    """
    Class ResetReactors
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().resetReactors()
        return 1

    def getMessage(self) -> str:
        return "".append("not resetreactors - 重置此地图所有的Reactor")


# Inner class from Java (originally nested)
class SetReactor(CommandExecute):
    """
    Class SetReactor
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        c.getPlayer().getMap().setReactorState(Byte.parseByte(splitted[1]))
        return 1

    def getMessage(self) -> str:
        return "".append("not hitreactor - 触碰Reactor")


# Inner class from Java (originally nested)
class cleardrops(RemoveDrops):
    """
    Class cleardrops
    Extends: RemoveDrops
    """

    pass


# Inner class from Java (originally nested)
class RemoveDrops(CommandExecute):
    """
    Class RemoveDrops
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(5, "清除了 " + c.getPlayer().getMap().getNumItems() + " 个掉落物")
        c.getPlayer().getMap().removeDrops()
        return 1

    def getMessage(self) -> str:
        return "".append("not removedrops - 移除地上的物品")


# Inner class from Java (originally nested)
class DropRate(CommandExecute):
    """
    Class DropRate
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 1:
            rate = int(splitted[1])
            if len(splitted) > 2 and splitted[2].lower() == "all".lower():
                for cserv in ChannelServer.getAllInstances():
                    cserv.setDropRate(rate)
            else:
                c.getChannelServer().setDropRate(rate)
            c.getPlayer().dropMessage(6, "掉宝倍率已改变更为 " + rate + "x")
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not droprate <倍率> - 更改掉落倍率")


# Inner class from Java (originally nested)
class MesoRate(CommandExecute):
    """
    Class MesoRate
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 1:
            rate = int(splitted[1])
            if len(splitted) > 2 and splitted[2].lower() == "all".lower():
                for cserv in ChannelServer.getAllInstances():
                    cserv.setMesoRate(rate)
            else:
                c.getChannelServer().setMesoRate(rate)
            c.getPlayer().dropMessage(6, "金币爆率已改变更为 " + rate + "x")
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not mesorate <倍率> - 更改金钱倍率")


# Inner class from Java (originally nested)
class DCAll(CommandExecute):
    """
    Class DCAll
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        range = -1
        if len(splitted) < 2:
            return 0
        input = None
        try:
            input = splitted[1]
        except Exception as ex:
        s = splitted[1]
        # switch (s):
            # case "m":
                range = 0
                break
            # case "c":
                range = 1
                break
            # default:
                range = 2
                break
        if range == -1:
            range = 1
        # switch (range):
            # case 0:
                c.getPlayer().getMap().disconnectAll()
                break
            # case 1:
                c.getChannelServer().getPlayerStorage().disconnectAll()
                break
            # case 2:
                for cserv in ChannelServer.getAllInstances():
                    cserv.getPlayerStorage().disconnectAll(True)
                break
        show = ""
        # switch (range):
            # case 0:
                show = "地图"
                break
            # case 1:
                show = "頻道"
                break
            # case 2:
                show = "世界"
                break
        msg = "[GM 密语] GM " + c.getPlayer().getName() + " DC 了 " + show + "玩家"
        World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, msg).encode("utf-8"))
        return 1

    def getMessage(self) -> str:
        return "".append("not dcall [m|c|w] - 所有玩家断线")


# Inner class from Java (originally nested)
class GoTo(CommandExecute):
    """
    Class GoTo
    Extends: CommandExecute
    """

    # Static initializer
    # (gotomaps = {}).put("gmmap", 180000000)
    # GoTo.gotomaps.put("southperry", 2000000)
    # GoTo.gotomaps.put("amherst", 1010000)
    # GoTo.gotomaps.put("henesys", 100000000)
    # GoTo.gotomaps.put("ellinia", 101000000)
    # GoTo.gotomaps.put("perion", 102000000)
    # GoTo.gotomaps.put("kerning", 103000000)
    # GoTo.gotomaps.put("lithharbour", 104000000)
    # GoTo.gotomaps.put("sleepywood", 105040300)
    # GoTo.gotomaps.put("florina", 110000000)
    # GoTo.gotomaps.put("orbis", 200000000)
    # GoTo.gotomaps.put("happyville", 209000000)
    # GoTo.gotomaps.put("elnath", 211000000)
    # GoTo.gotomaps.put("ludibrium", 220000000)
    # GoTo.gotomaps.put("aquaroad", 230000000)
    # GoTo.gotomaps.put("leafre", 240000000)
    # GoTo.gotomaps.put("mulung", 250000000)
    # GoTo.gotomaps.put("herbtown", 251000000)
    # GoTo.gotomaps.put("omegasector", 221000000)
    # GoTo.gotomaps.put("koreanfolktown", 222000000)
    # GoTo.gotomaps.put("newleafcity", 600000000)
    # GoTo.gotomaps.put("sharenian", 990000000)
    # GoTo.gotomaps.put("pianus", 230040420)
    # GoTo.gotomaps.put("horntail", 240060200)
    # GoTo.gotomaps.put("chorntail", 240060201)
    # GoTo.gotomaps.put("mushmom", 100000005)
    # GoTo.gotomaps.put("griffey", 240020101)
    # GoTo.gotomaps.put("manon", 240020401)
    # GoTo.gotomaps.put("zakum", 280030000)
    # GoTo.gotomaps.put("czakum", 280030001)
    # GoTo.gotomaps.put("papulatus", 220080001)
    # GoTo.gotomaps.put("showatown", 801000000)
    # GoTo.gotomaps.put("zipangu", 800000000)
    # GoTo.gotomaps.put("ariant", 260000100)
    # GoTo.gotomaps.put("nautilus", 120000000)
    # GoTo.gotomaps.put("boatquay", 541000000)
    # GoTo.gotomaps.put("malaysia", 550000000)
    # GoTo.gotomaps.put("taiwan", 740000000)
    # GoTo.gotomaps.put("thailand", 500000000)
    # GoTo.gotomaps.put("erev", 130000000)
    # GoTo.gotomaps.put("ellinforest", 300000000)
    # GoTo.gotomaps.put("kampung", 551000000)
    # GoTo.gotomaps.put("singapore", 540000000)
    # GoTo.gotomaps.put("amoria", 680000000)
    # GoTo.gotomaps.put("timetemple", 270000000)
    # GoTo.gotomaps.put("pinkbean", 270050100)
    # GoTo.gotomaps.put("peachblossom", 700000000)
    # GoTo.gotomaps.put("fm", 910000000)
    # GoTo.gotomaps.put("freemarket", 910000000)
    # GoTo.gotomaps.put("oxquiz", 109020001)
    # GoTo.gotomaps.put("ola", 109030101)
    # GoTo.gotomaps.put("fitness", 109040000)
    # GoTo.gotomaps.put("snowball", 109060000)
    # GoTo.gotomaps.put("cashmap", 741010200)
    # GoTo.gotomaps.put("golden", 950100000)
    # GoTo.gotomaps.put("phantom", 610010000)
    # GoTo.gotomaps.put("cwk", 610030000)
    # GoTo.gotomaps.put("rien", 140000000)


    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(6, "Syntax: not goto <mapname>")
        elif (splitted[1] in GoTo.gotomaps):
            target = c.getChannelServer().getMapFactory().getMap(GoTo.gotomaps.get(splitted[1]))
            targetPortal = target.getPortal(0)
            c.getPlayer().changeMap(target, targetPortal)
        elif splitted[1] == ("locations"):
            c.getPlayer().dropMessage(6, "Use not goto <location>. Locations are as follows:")
            sb = ""
            for s in GoTo.gotomaps.keys():
                sb.append(s).append(", ")
            c.getPlayer().dropMessage(6, sb[0:sb.__len__(] - 2))
        else:
            c.getPlayer().dropMessage(6, "Invalid command 指令規則 - Use not goto <location>. For a list of locations, use not goto locations.")
        return 1

    def getMessage(self) -> str:
        return "".append("not goto <名称> - 到某个地图")


# Inner class from Java (originally nested)
class KillAll(CommandExecute):
    """
    Class KillAll
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        map = c.getPlayer().getMap()
        range = Double.POSITIVE_INFINITY
        drop = True
        if len(splitted) > 1:
            irange = 9999
            if len(splitted) < 2:
                range = irange * irange
            else:
                try:
                    map = c.getChannelServer().getMapFactory().getMap(int(splitted[1]))
                    range = int(splitted[2]) * int(splitted[2])
                except NumberFormatException as ex:
            if len(splitted) >= 3:
                drop = splitted[3].lower() == "True".lower()
        monsters = map.getMapObjectsInRange(c.getPlayer().getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER))
        for monstermo in map.getMapObjectsInRange(c.getPlayer().getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER)):
            mob = monstermo
            map.killMonster(mob, c.getPlayer(), drop, False, 1)
            mob.giveExpToCharacter(c.getPlayer(), mob.getExp(), False, 0, 0, 0, 0, 0)
        c.getPlayer().dropMessage("您总共杀了 " + monsters + " 怪物")
        return 1

    def getMessage(self) -> str:
        return "".append("not killall [range] [mapid] - 杀掉所有怪物")


# Inner class from Java (originally nested)
class ResetMobs(CommandExecute):
    """
    Class ResetMobs
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().killAllMonsters(False)
        return 1

    def getMessage(self) -> str:
        return "".append("not resetmobs - 重置地图上所有怪物")


# Inner class from Java (originally nested)
class KillMonster(CommandExecute):
    """
    Class KillMonster
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        map = c.getPlayer().getMap()
        range = Double.POSITIVE_INFINITY
        for monstermo in map.getMapObjectsInRange(c.getPlayer().getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER)):
            mob = monstermo
            if mob.getId() == int(splitted[1]):
                mob.damage(c.getPlayer(), mob.getHp(), False)
        return 1

    def getMessage(self) -> str:
        return "".append("not killmonster <mobid> - 杀掉地图上某个怪物")


# Inner class from Java (originally nested)
class KillMonsterByOID(CommandExecute):
    """
    Class KillMonsterByOID
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        map = c.getPlayer().getMap()
        targetId = int(splitted[1])
        monster = map.getMonsterByOid(targetId)
        if monster is not None:
            map.killMonster(monster, c.getPlayer(), False, False, 1)
        return 1

    def getMessage(self) -> str:
        return "".append("not killmonsterbyoid <moboid> - 杀掉地图上某个怪物")


# Inner class from Java (originally nested)
class HitMonsterByOID(CommandExecute):
    """
    Class HitMonsterByOID
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        map = c.getPlayer().getMap()
        targetId = int(splitted[1])
        damage = int(splitted[2])
        monster = map.getMonsterByOid(targetId)
        if monster is not None:
            map.broadcastMessage(MobPacket.damageMonster(targetId, damage))
            monster.damage(c.getPlayer(), damage, False)
        return 1

    def getMessage(self) -> str:
        return "".append("not hitmonsterbyoid <moboid> <damage> - 碰撞地图上某個怪物")


# Inner class from Java (originally nested)
class NPC(CommandExecute):
    """
    Class NPC
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        npcId = 0
        try:
            npcId = int(splitted[1])
        except NumberFormatException as ex:
        npc = MapleLifeFactory.getNPC(npcId)
        if npc is not None and not npc.getName() == ("MISSINGNO"):
            npc.setPosition(c.getPlayer().getPosition())
            npc.setCy(c.getPlayer().getPosition().y)
            npc.setRx0(c.getPlayer().getPosition().x + 50)
            npc.setRx1(c.getPlayer().getPosition().x - 50)
            npc.setFh(c.getPlayer().getMap().getFootholds().findBelow(c.getPlayer().getPosition()).getId())
            npc.setCustom(True)
            c.getPlayer().getMap().addMapObject(npc)
            c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.spawnNPC(npc, True))
        else:
            c.getPlayer().dropMessage(6, "找不到此代码为" + npcId + "的Npc")
        return 1

    def getMessage(self) -> str:
        return "".append("not npc <npcid> - 呼叫出NPC")


# Inner class from Java (originally nested)
class RemoveNPCs(CommandExecute):
    """
    Class RemoveNPCs
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().resetNPCs()
        return 1

    def getMessage(self) -> str:
        return "".append("not removenpcs - 刪除所有NPC")


# Inner class from Java (originally nested)
class LookNPCs(CommandExecute):
    """
    Class LookNPCs
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for reactor1l in c.getPlayer().getMap().getAllNPCsThreadsafe():
            reactor2l = reactor1
            c.getPlayer().dropMessage(5, "NPC: oID: " + reactor2.getObjectId() + " npcID: " + reactor2.getId() + " Position: " + reactor2.getPosition() + " Name: " + reactor2.getName())
        return 1

    def getMessage(self) -> str:
        return "".append("not looknpcs - 查看所有NPC")


# Inner class from Java (originally nested)
class LookReactors(CommandExecute):
    """
    Class LookReactors
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for reactor1l in c.getPlayer().getMap().getAllReactorsThreadsafe():
            reactor2l = reactor1
            c.getPlayer().dropMessage(5, "Reactor: oID: " + reactor2.getObjectId() + " reactorID: " + reactor2.getReactorId() + " Position: " + reactor2.getPosition() + " State: " + reactor2.getState() + " Name: " + reactor2.getName())
        return 1

    def getMessage(self) -> str:
        return "".append("not lookreactors - 查看所有反应堆")


# Inner class from Java (originally nested)
class LookPortals(CommandExecute):
    """
    Class LookPortals
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for portal in c.getPlayer().getMap().getPortals():
            c.getPlayer().dropMessage(5, "Portal: ID: " + portal.getId() + " script: " + portal.getScriptName() + " name: " + portal.getName() + " pos: " + portal.getPosition().x + "," + portal.getPosition().y + " target: " + portal.getTargetMapId() + " / " + portal.getTarget())
        return 1

    def getMessage(self) -> str:
        return "".append("not 反应堆 - 查看所有反应堆")


# Inner class from Java (originally nested)
class MakePNPC(CommandExecute):
    """
    Class MakePNPC
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        try:
            c.getPlayer().dropMessage(6, "Making playerNPC...")
            name = splitted[1]
            ch = World.Find.findChannel(name)
            if ch <= 0:
                c.getPlayer().dropMessage(6, "玩家必须在线")
                return 1
            chhr = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
            if chhr is None:
                c.getPlayer().dropMessage(6, splitted[1] + " is not online")
            else:
                npcId = int(splitted[2])
                npc_c = MapleLifeFactory.getNPC(npcId)
                if npc_c is None or npc_c.getName() == ("MISSINGNO"):
                    c.getPlayer().dropMessage(6, "NPC不存在")
                    return 1
                npc = PlayerNPC(chhr, npcId, c.getPlayer().getMap(), c.getPlayer())
                npc.addToServer()
                c.getPlayer().dropMessage(6, "Done")
        except NumberFormatException as e:
            c.getPlayer().dropMessage(6, "NPC failed... : " + e.getMessage())
        return 1

    def getMessage(self) -> str:
        return "".append("not 玩家npc <playername> <npcid> - 创造玩家NPC")


# Inner class from Java (originally nested)
class MakeOfflineP(CommandExecute):
    """
    Class MakeOfflineP
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        try:
            c.getPlayer().dropMessage(6, "Making playerNPC...")
            cs = MapleClient(None, None, MockIOSession())
            chhr = MapleCharacter.loadCharFromDB(MapleCharacterUtil.getIdByName(splitted[1]), cs, False)
            if chhr is None:
                c.getPlayer().dropMessage(6, splitted[1] + " does not exist")
            else:
                npc = PlayerNPC(chhr, int(splitted[2]), c.getPlayer().getMap(), c.getPlayer())
                npc.addToServer()
                c.getPlayer().dropMessage(6, "Done")
        except NumberFormatException as e:
            c.getPlayer().dropMessage(6, "NPC failed... : " + e.getMessage())
        return 1

    def getMessage(self) -> str:
        return "".append("not 离线npc <charname> <npcid> - 创造离线PNPC")


# Inner class from Java (originally nested)
class DestroyPNPC(CommandExecute):
    """
    Class DestroyPNPC
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        try:
            c.getPlayer().dropMessage(6, "Destroying playerNPC...")
            npc = c.getPlayer().getMap().getNPCByOid(int(splitted[1]))
            if isinstance(npc, PlayerNPC):
                (npc).destroy(True)
                c.getPlayer().dropMessage(6, "Done")
            else:
                c.getPlayer().dropMessage(6, "not destroypnpc [objectid]")
        except NumberFormatException as e:
            c.getPlayer().dropMessage(6, "NPC failed... : " + e.getMessage())
        return 1

    def getMessage(self) -> str:
        return "".append("not destroypnpc [objectid] - 刪除PNPC")


# Inner class from Java (originally nested)
class MyPos(CommandExecute):
    """
    Class MyPos
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        pos = c.getPlayer().getPosition()
        c.getPlayer().dropMessage(6, "X: " + pos.x + " | Y: " + pos.y + " | RX0: " + (pos.x + 50) + " | RX1: " + (pos.x - 50) + " | FH: " + c.getPlayer().getFH() + "| CY:" + pos.y)
        return 1

    def getMessage(self) -> str:
        return "".append("not mypos - 我的位置")


# Inner class from Java (originally nested)
class ReloadDrops(CommandExecute):
    """
    Class ReloadDrops
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleMonsterInformationProvider.getInstance().clearDrops()
        ReactorScriptManager.getInstance().clearDrops()
        return 1

    def getMessage(self) -> str:
        return "".append("not 重新载入掉宝 - 重新載入掉宝")


# Inner class from Java (originally nested)
class ReloadPortals(CommandExecute):
    """
    Class ReloadPortals
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        PortalScriptManager.getInstance().clearScripts()
        return 1

    def getMessage(self) -> str:
        return "".append("not reloadportals - 重新载入进入点")


# Inner class from Java (originally nested)
class ReloadShops(CommandExecute):
    """
    Class ReloadShops
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleShopFactory.getInstance().clear()
        return 1

    def getMessage(self) -> str:
        return "".append("not 重新载入商店 - 重新载入商店")


# Inner class from Java (originally nested)
class ReloadEvents(CommandExecute):
    """
    Class ReloadEvents
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for instance in ChannelServer.getAllInstances():
            instance.reloadEvents()
        return 1


# Inner class from Java (originally nested)
class ReloadQuests(CommandExecute):
    """
    Class ReloadQuests
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        MapleQuest.clearQuests()
        return 1

    def getMessage(self) -> str:
        return "".append("not 重新载入任务 - 重新载入任务")


# Inner class from Java (originally nested)
class 召唤永久的怪物(CommandExecute):
    """
    Class 召唤永久的怪物
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        npcId = int(splitted[1])
        npc = MapleLifeFactory.getNPC(npcId)
        if npc is not None and not npc.getName() == ("MISSINGNO"):
            xpos = c.getPlayer().getPosition().x
            ypos = c.getPlayer().getPosition().y
            fh = c.getPlayer().getMap().getFootholds().findBelow(c.getPlayer().getPosition()).getId()
            npc.setPosition(c.getPlayer().getPosition())
            npc.setCy(ypos)
            npc.setRx0(xpos)
            npc.setRx1(xpos)
            npc.setFh(fh)
            npc.setCustom(True)
            try:
                final com.mysql.jdbc.Connection con = (com.mysql.jdbc.Connection) DatabaseConnection.getConnection()
                # try-with-resources: final PreparedStatement ps = con.prepareStatement("INSERT INTO wz_customlife (dataid, f, hide, fh, cy, rx0, rx1, type, x, y, mid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                try:
                    ps.setInt(1, npcId)
                    ps.setInt(2, 0)
                    ps.setInt(3, 0)
                    ps.setInt(4, fh)
                    ps.setInt(5, ypos)
                    ps.setInt(6, xpos)
                    ps.setInt(7, xpos)
                    ps.setString(8, "n")
                    ps.setInt(9, xpos)
                    ps.setInt(10, ypos)
                    ps.setInt(11, c.getPlayer().getMapId())
                    ps.executeUpdate()
            except SQLException as e:
                c.getPlayer().dropMessage(6, "Failed to save NPC to the database")
            for cserv in ChannelServer.getAllInstances():
                cserv.getMapFactory().getMap(c.getPlayer().getMapId()).addMapObject(npc)
                cserv.getMapFactory().getMap(c.getPlayer().getMapId()).broadcastMessage(MaplePacketCreator.spawnNPC(npc, True))
            c.getPlayer().dropMessage(6, "Please do not reload this map or else the NPC will disappear till the next restart.")
        else:
            c.getPlayer().dropMessage(6, "查无此 Npc ")
        return 1

    def getMessage(self) -> str:
        return "".append("not 永久npc - 建立永久NPC")


# Inner class from Java (originally nested)
class Spawn(CommandExecute):
    """
    Class Spawn
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        mid = 0
        try:
            mid = int(splitted[1])
        except NumberFormatException as ex:
        num = min(CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1), 500)
        if num > 1000:
            num = 1000
        hp = CommandProcessorUtil.getNamedLongArg(splitted, 1, "hp")
        exp = CommandProcessorUtil.getNamedIntArg(splitted, 1, "exp")
        php = CommandProcessorUtil.getNamedDoubleArg(splitted, 1, "php")
        pexp = CommandProcessorUtil.getNamedDoubleArg(splitted, 1, "pexp")
        onemob = None
        try:
            onemob = MapleLifeFactory.getMonster(mid)
        except Exception as e:
            c.getPlayer().dropMessage(5, "错误: " + e.getMessage())
            return 1
        newhp = None
        if hp is not None:
            newhp = hp
        elif php is not None:
            newhp = (long) (onemob.getMobMaxHp() * (php / 100.0))
        else:
            newhp = onemob.getMobMaxHp()
        newexp = None
        if exp is not None:
            newexp = exp
        elif pexp is not None:
            newexp = (int) (onemob.getMobExp() * (pexp / 100.0))
        else:
            newexp = onemob.getMobExp()
        if newhp < 1:
            newhp = 1
        overrideStats = OverrideMonsterStats(newhp, onemob.getMobMaxMp(), newexp, False)
        for i in range(num):
            mob = MapleLifeFactory.getMonster(mid)
            mob.setHp(newhp)
            mob.setOverrideStats(overrideStats)
            c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, c.getPlayer().getPosition())
        return 1

    def getMessage(self) -> str:
        return "".append("not spawn <怪物ID> <hp|exp|php or pexp = ?> - 召唤怪物")


# Inner class from Java (originally nested)
class Clock(CommandExecute):
    """
    Class Clock
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.getClock(CommandProcessorUtil.getOptionalIntArg(splitted, 1, 60)))
        return 1

    def getMessage(self) -> str:
        return "".append("not clock <time> 时钟")


# Inner class from Java (originally nested)
class WarpPlayersTo(CommandExecute):
    """
    Class WarpPlayersTo
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        try:
            target = c.getChannelServer().getMapFactory().getMap(int(splitted[1]))
            from = c.getPlayer().getMap()
            for chr in from.getCharactersThreadsafe():
                chr.changeMap(target, target.getPortal(0))
        except NumberFormatException as e:
            return 0
        return 1

    def getMessage(self) -> str:
        return "".append("not WarpPlayersTo <maipid> 把所有玩家传送到某个地图")


# Inner class from Java (originally nested)
class LOLCastle(CommandExecute):
    """
    Class LOLCastle
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) != 2:
            return 0
        target = c.getChannelServer().getEventSM().getEventManager("lolcastle").getInstance("lolcastle" + splitted[1]).getMapFactory().getMap(990000300, False, False)
        c.getPlayer().changeMap(target, target.getPortal(0))
        return 1

    def getMessage(self) -> str:
        return "".append("not lolcastle level (level = 1-5) - 不知道是啥")


# Inner class from Java (originally nested)
class Map(CommandExecute):
    """
    Class Map
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        try:
            target = c.getChannelServer().getMapFactory().getMap(int(splitted[1]))
            if target is None:
                c.getPlayer().dropMessage(5, "地图不存在.")
                return 1
            targetPortal = None
            if len(splitted) > 2:
                try:
                    targetPortal = target.getPortal(int(splitted[2]))
                except IndexOutOfBoundsException as e2:
                    c.getPlayer().dropMessage(5, "传送点错误.")
                except NumberFormatException as ex:
            if targetPortal is None:
                targetPortal = target.getPortal(0)
            c.getPlayer().changeMap(target, targetPortal)
        except NumberFormatException as e:
            c.getPlayer().dropMessage(5, "Error: " + e.getMessage())
        return 1

    def getMessage(self) -> str:
        return "".append("not map <mapid|charname> [portal] - 传送到某地图/人")


# Inner class from Java (originally nested)
class StartProfiling(CommandExecute):
    """
    Class StartProfiling
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        sampler = CPUSampler.getInstance()
        sampler.addIncluded("client")
        sampler.addIncluded("constants")
        sampler.addIncluded("database")
        sampler.addIncluded("handling")
        sampler.addIncluded("provider")
        sampler.addIncluded("scripting")
        sampler.addIncluded("server")
        sampler.addIncluded("tools")
        sampler.start()
        return 1

    def getMessage(self) -> str:
        return "".append("not startprofiling 开始记录JVM资讯")


# Inner class from Java (originally nested)
class StopProfiling(CommandExecute):
    """
    Class StopProfiling
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        sampler = CPUSampler.getInstance()
        try:
            filename = "odinprofile.txt"
            if len(splitted) > 1:
                filename = splitted[1]
            file = File(filename)
            if file.exists():
                c.getPlayer().dropMessage(6, "The entered filename already exists, choose a different one")
                return 1
            sampler.stop()
            # try-with-resources: final FileWriter fw = FileWriter(file)
            try:
                sampler.save(fw, 1, 10)
        except IOException as e:
            print("Error saving profile" + e)
        sampler.reset()
        return 1

    def getMessage(self) -> str:
        return "".append("not stopprofiling <filename> - 取消记录JVM资讯并保存到档案")


# Inner class from Java (originally nested)
class ReloadMap(CommandExecute):
    """
    Class ReloadMap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        if len(splitted) < 2:
            return 0
        custMap = len(splitted) >= 2
        mapid = custMap ? int(splitted[1]) : player.getMapId()
        map = custMap ? player.getClient().getChannelServer().getMapFactory().getMap(mapid) : player.getMap()
        if player.getClient().getChannelServer().getMapFactory().destroyMap(mapid):
            newMap = player.getClient().getChannelServer().getMapFactory().getMap(mapid)
            newPor = newMap.getPortal(0)
            mcs = new LinkedHashSet<MapleCharacter>(map.getCharacters())
            Label_0139:
            for m in mcs:
                x = 0
                while x < 5:
                    try:
                        m.changeMap(newMap, newPor)
                        Label_0139 = None
                    except Exception as t:
                        x += 1
                        continue
                player.dropMessage("Failed warping " + m.getName() + " to the new map. Skipping...")
            player.dropMessage("地图刷新完毕，如还出现NPC不见请使用此命令.")
            return 1
        player.dropMessage("Unsuccessful reset!")
        return 1

    def getMessage(self) -> str:
        return "".append("not reloadmap <maipid> - 重置某个地图")


# Inner class from Java (originally nested)
class Respawn(CommandExecute):
    """
    Class Respawn
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().respawn(True)
        return 1

    def getMessage(self) -> str:
        return "".append("not respawn - 重新载入地图")


# Inner class from Java (originally nested)
class ResetMap(CommandExecute):
    """
    Class ResetMap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().resetFully()
        return 1

    def getMessage(self) -> str:
        return "".append("not resetmap - 重置这个地图")


# Inner class from Java (originally nested)
class Reloadall(CommandExecute):
    """
    Class Reloadall
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for instance in ChannelServer.getAllInstances():
            instance.reloadEvents()
        MapleShopFactory.getInstance().clear()
        PortalScriptManager.getInstance().clearScripts()
        MapleItemInformationProvider.getInstance().load()
        CashItemFactory.getInstance().initialize()
        MapleMonsterInformationProvider.getInstance().clearDrops()
        MapleGuild.loadAll()
        MapleFamily.loadAll()
        MapleLifeFactory.loadQuestCounts()
        MapleQuest.initQuests()
        MapleOxQuizFactory.getInstance()
        ReactorScriptManager.getInstance().clearDrops()
        return 1

    def getMessage(self) -> str:
        return "".append("not Reloadall - 重置全服务器")


# Inner class from Java (originally nested)
class PNPC(CommandExecute):
    """
    Class PNPC
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        npcId = int(splitted[1])
        npc = MapleLifeFactory.getNPC(npcId)
        if npc is not None and not npc.getName() == ("MISSINGNO"):
            xpos = c.getPlayer().getPosition().x
            ypos = c.getPlayer().getPosition().y
            fh = c.getPlayer().getMap().getFootholds().findBelow(c.getPlayer().getPosition()).getId()
            npc.setPosition(c.getPlayer().getPosition())
            npc.setCy(ypos)
            npc.setRx0(xpos)
            npc.setRx1(xpos)
            npc.setFh(fh)
            npc.setCustom(True)
            try:
                final com.mysql.jdbc.Connection con = (com.mysql.jdbc.Connection) DatabaseConnection.getConnection()
                # try-with-resources: PreparedStatement ps = con.prepareStatement("INSERT INTO wz_customlife (dataid, f, hide, fh, cy, rx0, rx1, type, x, y, mid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                try:
                    ps.setInt(1, npcId)
                    ps.setInt(2, 0)
                    ps.setInt(3, 0)
                    ps.setInt(4, fh)
                    ps.setInt(5, ypos)
                    ps.setInt(6, xpos)
                    ps.setInt(7, xpos)
                    ps.setString(8, "n")
                    ps.setInt(9, xpos)
                    ps.setInt(10, ypos)
                    ps.setInt(11, c.getPlayer().getMapId())
                    ps.executeUpdate()
            except SQLException as e:
                c.getPlayer().dropMessage(6, "Failed to save NPC to the database")
            for cserv in ChannelServer.getAllInstances():
                cserv.getMapFactory().getMap(c.getPlayer().getMapId()).addMapObject(npc)
                cserv.getMapFactory().getMap(c.getPlayer().getMapId()).broadcastMessage(MaplePacketCreator.spawnNPC(npc, True))
            c.getPlayer().dropMessage(6, "Please do not reload this map or else the NPC will disappear till the next restart.")
        else:
            c.getPlayer().dropMessage(6, "查无此 Npc ")
        return 1

    def getMessage(self) -> str:
        return "".append("not 永久npc - 建立永久NPC")


# Inner class from Java (originally nested)
class copyInv(CommandExecute):
    """
    Class copyInv
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        type = 1
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if victim is None:
            player.dropMessage("找不到该玩家")
            return 1
        try:
            type = int(splitted[2])
        except NumberFormatException as ex:
        if type == 0:
            for ii in victim.getInventory(MapleInventoryType.EQUIPPED).list():
                n = ii.copy()
                player.getInventory(MapleInventoryType.EQUIP).addItem(n)
            player.fakeRelog()
        else:
            types = None
            # switch (type):
                # case 1:
                    types = MapleInventoryType.EQUIP
                    break
                # case 2:
                    types = MapleInventoryType.USE
                    break
                # case 3:
                    types = MapleInventoryType.ETC
                    break
                # case 4:
                    types = MapleInventoryType.SETUP
                    break
                # case 5:
                    types = MapleInventoryType.CASH
                    break
                # default:
                    types = None
                    break
            if types is None:
                c.getPlayer().dropMessage("发生错误")
                return 1
            equip = new int[97]
            for i in range(1, 97):
                if victim.getInventory(types).getItem(i) is not None:
                    equip[i] = i
            for i in range(len(equip)):
                if equip[i] != 0:
                    n2 = victim.getInventory(types).getItem(equip[i]).copy()
                    player.getInventory(types).addItem(n2)
            player.fakeRelog()
        return 1

    def getMessage(self) -> str:
        return "".append("not copyinv 玩家名称 装备栏位(0 = 装备中 1=装备栏 2=消耗栏 3=其他栏 4=装饰栏 5=点数栏)(预设装备栏) - 复制玩家道具")


# Inner class from Java (originally nested)
class RemoveItemOff(CommandExecute):
    """
    Class RemoveItemOff
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        final com.mysql.jdbc.Connection dcon = (com.mysql.jdbc.Connection) DatabaseConnection.getConnection()
        try:
            id = 0
            quantity = 0
            name = splitted[2]
            ps = dcon.prepareStatement("select * from characters where name = ?")
            ps.setString(1, name)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    id = rs.getInt("id")
            if id == 0:
                c.getPlayer().dropMessage(5, "角色不存在资料库。")
                return 0
            ps2 = dcon.prepareStatement("delete from inventoryitems WHERE itemid = ? and characterid = ?")
            ps2.setInt(1, int(splitted[1]))
            ps2.setInt(2, id)
            ps2.executeUpdate()
            c.getPlayer().dropMessage(6, "所有ID为 " + splitted[1] + " 的道具" + quantity + "已经从 " + name + " 身上被移除了")
            ps.close()
            ps2.close()
            return 1
        except SQLException as e:
            return 0

    def getMessage(self) -> str:
        return "".append("not removeitem <物品ID> <角色名稱> - 移除玩家身上的道具")


# Inner class from Java (originally nested)
class ExpEveryone(CommandExecute):
    """
    Class ExpEveryone
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(splitted[0] + " <经验量>")
            return 0
        gain = int(splitted[1])
        ret = 0
        for cserv in ChannelServer.getAllInstances():
            for mch in cserv.getPlayerStorage().getAllCharacters():
                mch.gainExp(gain, True, True, True)
                ret += 1
        for cserv2 in ChannelServer.getAllInstances():
            for mch in cserv2.getPlayerStorage().getAllCharacters():
                mch.startMapEffect("管理员发放" + gain + "经验给在线的所有玩家！祝您玩的开心玩的快乐", 5121009)
        c.getPlayer().dropMessage(6, "命令使用成功，当前共有: " + ret + " 个玩家获得: " + gain + " 点的" + " 经验 " + " 总计: " + ret * gain)
        return 1


# Inner class from Java (originally nested)
class CashEveryone(CommandExecute):
    """
    Class CashEveryone
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 2:
            type = int(splitted[1])
            quantity = int(splitted[2])
            # switch (type):
                # case 1:
                    type = 1
                    break
                # case 2:
                    type = 2
                    break
                # default:
                    c.getPlayer().dropMessage(6, "用法: not 给所有人点卷 [点卷类型1-2] [点卷数量][1是点卷.2是抵用卷]")
                    return 0
            if quantity > 10000:
                quantity = 10000
            ret = 0
            for cserv in ChannelServer.getAllInstances():
                for mch in cserv.getPlayerStorage().getAllCharacters():
                    mch.modifyCSPoints(type, quantity)
                    ret += 1
            show = (type == 1) ? "点卷" : "抵用卷"
            for cserv2 in ChannelServer.getAllInstances():
                for mch2 in cserv2.getPlayerStorage().getAllCharacters():
                    mch2.startMapEffect("管理员发放" + quantity + show + "点卷给在线的所有玩家！祝您的开心玩的快乐", 5121009)
            c.getPlayer().dropMessage(6, "命令使用成功，当前共有: " + ret + " 个玩家获得: " + quantity + " 点的" + ((type == 1) ? "点券 " : " 抵用券 ") + " 总计: " + ret * quantity)
        else:
            c.getPlayer().dropMessage(6, "用法: not 给所有人点卷 [点卷类型1-2] [点卷数量][1是点卷.2是抵用卷]")
        return 1


# Inner class from Java (originally nested)
class mesoEveryone(CommandExecute):
    """
    Class mesoEveryone
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(splitted[0] + " <金币量>")
            return 0
        ret = 0
        gain = int(splitted[1])
        for mch in c.getChannelServer().getPlayerStorage().getAllCharactersThreadSafe():
            mch.gainMeso(gain, True)
            ret += 1
        for cserv1 in ChannelServer.getAllInstances():
            for mch2 in cserv1.getPlayerStorage().getAllCharacters():
                mch2.startMapEffect("管理员发放" + gain + "冒险币给在线的所有玩家！祝您玩的开心玩的快乐", 5121009)
        c.getPlayer().dropMessage(6, "命令使用成功，当前共有: " + ret + " 个玩家获得: " + gain + " 冒险币 " + " 总计: " + ret * gain)
        return 1


# Inner class from Java (originally nested)
class setRate(CommandExecute):
    """
    Class setRate
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        mc = None
        player = mc = c.getPlayer()
        if len(splitted) > 2:
            arg = int(splitted[2])
            seconds = int(splitted[3])
            mins = int(splitted[4])
            hours = int(splitted[5])
            time = seconds + mins * 60 + hours * 60 * 60
            bOk = True
            if splitted[1] == ("经验"):
                if arg <= 50:
                    for cservs in ChannelServer.getAllInstances():
                        cservs.setExpRate(arg)
                        cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, "经验倍率已经成功修改为 " + arg + "倍。祝大家游戏开心.经验倍率将在时间到后自动更正！"))
                else:
                    mc.dropMessage("操作已被系统限制。")
            elif splitted[1] == ("爆率"):
                if arg <= 5:
                    for cservs in ChannelServer.getAllInstances():
                        cservs.setDropRate(arg)
                        cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, "爆率倍率已经成功修改为 " + arg + "倍。祝大家游戏开心.经验倍率将在时间到后自动更正！！"))
                else:
                    mc.dropMessage("操作已被系统限制。")
            elif splitted[1] == ("金币"):
                if arg <= 5:
                    for cservs in ChannelServer.getAllInstances():
                        cservs.setMesoRate(arg)
                        cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, "金币倍率已经成功修改为 " + arg + "倍。祝大家游戏开心.经验倍率将在时间到后自动更正！！"))
                else:
                    mc.dropMessage("操作已被系统限制。")
            elif splitted[1].lower() == "boss爆率".lower():
                if arg <= 5:
                    for cservs in ChannelServer.getAllInstances():
                        cservs.setBossDropRate(arg)
                        cservs.broadcastPacket(MaplePacketCreator.serverNotice(6, "BOSS掉宝已经成功修改为 " + arg + "倍。祝大家游戏开心.经验倍率将在时间到后自动更正！！"))
                else:
                    mc.dropMessage("操作已被系统限制。")
            elif splitted[1] == ("宠物经验"):
                if arg > 5:
                    mc.dropMessage("操作已被系统限制。")
            else:
                bOk = False
            if bOk:
                rate = splitted[1]
                World.scheduleRateDelay(rate, time)
            else:
                mc.dropMessage("使用方法: not 倍率设置 <exp经验|drop爆率|meso金币|bossboss爆率|pet> <类> <秒> <分> <时>")
        else:
            mc.dropMessage("使用方法: not 倍率设置 <exp经验|drop爆率|meso金币|bossboss爆率|pet> <类> <秒> <分> <时>")
        return 1


# Inner class from Java (originally nested)
class WarpAllHere(CommandExecute):
    """
    Class WarpAllHere
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        for CS in ChannelServer.getAllInstances():
            for mch in CS.getPlayerStorage().getAllCharactersThreadSafe():
                if mch.getMapId() != c.getPlayer().getMapId():
                    mch.changeMap(c.getPlayer().getMap(), c.getPlayer().getPosition())
                if mch.getClient().getChannel() != c.getPlayer().getClient().getChannel():
                    mch.changeChannel(c.getPlayer().getClient().getChannel())
        return 1

    def getMessage(self) -> str:
        return "".append("not WarpAllHere 把所有玩家传送到这里")


# Inner class from Java (originally nested)
class maxSkills(CommandExecute):
    """
    Class maxSkills
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        player.maxSkills()
        return 1


# Inner class from Java (originally nested)
class Drop(CommandExecute):
    """
    Class Drop
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        itemId = 0
        try:
            itemId = int(splitted[1])
        except NumberFormatException as ex:
            ex.printStackTrace()
        quantity = CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1)
        ii = MapleItemInformationProvider.getInstance()
        if GameConstants.isPet(itemId):
            c.getPlayer().dropMessage(5, "宠物请到购物商城购买.")
        elif not ii.itemExists(itemId):
            c.getPlayer().dropMessage(5, itemId + " - 物品不存在")
        else:
            toDrop = None
            if GameConstants.getInventoryType(itemId) == MapleInventoryType.EQUIP:
                toDrop = ii.randomizeStats(ii.getEquipById(itemId))
            else:
                toDrop = new client.inventory.Item(itemId, 0, quantity, 0)
            toDrop.setGMLog(c.getPlayer().getName())
            c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), toDrop, c.getPlayer().getPosition(), True, True)
        return 1


# Inner class from Java (originally nested)
class buff(CommandExecute):
    """
    Class buff
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        SkillFactory.getSkill(9001002).getEffect(1).applyTo(player)
        SkillFactory.getSkill(9001003).getEffect(1).applyTo(player)
        SkillFactory.getSkill(9001008).getEffect(1).applyTo(player)
        SkillFactory.getSkill(9001001).getEffect(1).applyTo(player)
        return 1


# Inner class from Java (originally nested)
class maxstats(CommandExecute):
    """
    Class maxstats
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        player.getStat().setMaxHp(30000)
        player.getStat().setMaxMp(30000)
        player.getStat().setStr(32767)
        player.getStat().setDex(32767)
        player.getStat().setInt(32767)
        player.getStat().setLuk(32767)
        player.updateSingleStat(MapleStat.MAXHP, 30000)
        player.updateSingleStat(MapleStat.MAXMP, 30000)
        player.updateSingleStat(MapleStat.STR, 32767)
        player.updateSingleStat(MapleStat.DEX, 32767)
        player.updateSingleStat(MapleStat.INT, 32767)
        player.updateSingleStat(MapleStat.LUK, 32767)
        return 1


# Inner class from Java (originally nested)
class Minimumstats(CommandExecute):
    """
    Class Minimumstats
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        player = c.getPlayer()
        player.getStat().setMaxHp(50)
        player.getStat().setMaxMp(50)
        player.getStat().setStr(4)
        player.getStat().setDex(4)
        player.getStat().setInt(4)
        player.getStat().setLuk(4)
        player.updateSingleStat(MapleStat.MAXHP, 50)
        player.updateSingleStat(MapleStat.MAXMP, 50)
        player.updateSingleStat(MapleStat.STR, 4)
        player.updateSingleStat(MapleStat.DEX, 4)
        player.updateSingleStat(MapleStat.INT, 4)
        player.updateSingleStat(MapleStat.LUK, 4)
        return 1


# Inner class from Java (originally nested)
class WhereAmI(CommandExecute):
    """
    Class WhereAmI
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(5, "目前地图 " + c.getPlayer().getMap().getId() + "坐标 (" + str(c.getPlayer().getPosition().x) + " , " + str(c.getPlayer().getPosition().y) + ")")
        return 1


# Inner class from Java (originally nested)
class Packet(CommandExecute):
    """
    Class Packet
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        mplew = MaplePacketLittleEndianWriter()
        packetheader = int(splitted[1])
        packet_in = " 00 00 00 00 00 00 00 00 00 "
        if len(splitted) > 2:
            packet_in = StringUtil.joinStringFrom(splitted, 2)
        mplew.writeShort(packetheader)
        mplew.write(HexTool.getByteArrayFromHexString(packet_in))
        mplew.writeZeroBytes(20)
        c.getSession().write(mplew.getPacket())
        c.getPlayer().dropMessage(packetheader + "已传送封包[" + mplew.getPacket().encode("utf-8").length + "] : " + mplew)
        return 1


# Inner class from Java (originally nested)
class mob(CommandExecute):
    """
    Class mob
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        monster = None
        for monstermo in c.getPlayer().getMap().getMapObjectsInRange(c.getPlayer().getPosition(), 100000.0, Arrays.asList(MapleMapObjectType.MONSTER)):
            monster = monstermo
            if monster.isAlive():
                c.getPlayer().dropMessage(6, "怪物 " + monster)
        if monster is None:
            c.getPlayer().dropMessage(6, "找不到怪物")
        return 1


# Inner class from Java (originally nested)
class register(CommandExecute):
    """
    Class register
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        con = None
        acc = None
        password = None
        try:
            acc = splitted[1]
            password = splitted[2]
        except Exception as ex3:
            ex3.printStackTrace()
        if acc is None or password is None:
            c.getPlayer().dropMessage("账号或密码异常")
            return 0
        ACCexist = AutoRegister.getAccountExists(acc)
        if ACCexist:
            c.getPlayer().dropMessage("帐号已被使用")
            return 0
        if acc >= 12:
            c.getPlayer().dropMessage("密码长度过长")
            return 0
        try:
            con = DatabaseConnection.getConnection()
        except Exception as ex:
            print(ex)
            return 0
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("INSERT INTO accounts (name, password) VALUES (?, ?)")
        try:
            ps.setString(1, acc)
            ps.setString(2, LoginCrypto.hexSha1(password))
            ps.executeUpdate()
            ps.close()
        except SQLException as ex2:
            print(ex2)
            return 0
        c.getPlayer().dropMessage("[注册完成]账号: " + acc + " 密码: " + password)
        return 1


# Inner class from Java (originally nested)
class openmap(CommandExecute):
    """
    Class openmap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        mapid = 0
        input = None
        map = None
        if len(splitted) < 2:
            c.getPlayer().dropMessage(splitted[0] + " - 开放地图")
            return 0
        try:
            input = splitted[1]
            mapid = int(input)
        except NumberFormatException as ex:
        for cserv in ChannelServer.getAllInstances():
            cserv.getMapFactory().HealMap(mapid)
        return 1


# Inner class from Java (originally nested)
class closemap(CommandExecute):
    """
    Class closemap
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        mapid = 0
        input = None
        map = None
        if len(splitted) < 2:
            c.getPlayer().dropMessage(splitted[0] + " - 关闭地图")
            return 0
        try:
            input = splitted[1]
            mapid = int(input)
        except NumberFormatException as ex:
        if c.getChannelServer().getMapFactory().getMap(mapid) is None:
            c.getPlayer().dropMessage("地图不存在")
            return 0
        for cserv in ChannelServer.getAllInstances():
            cserv.getMapFactory().destroyMap(mapid, True)
        return 1


# Inner class from Java (originally nested)
class reloadcpq(CommandExecute):
    """
    Class reloadcpq
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().getMap().reloadCPQ()
        c.getPlayer().dropMessage("嘉年华地图更新成功")
        return 1


# Inner class from Java (originally nested)
class 检测复制(CommandExecute):
    """
    Class 检测复制
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        ii = MapleItemInformationProvider.getInstance()
        msgs = []
        final java.util.Map<Integer, CopyItemInfo> checkItems = {}
        for cserv in ChannelServer.getAllInstances():
            for player in cserv.getPlayerStorage().getAllCharacters():
                if player is not None and player.getMap() is not None:
                    equip = player.getInventory(MapleInventoryType.EQUIP)
                    for item in equip.list():
                        if item.getEquipOnlyId() > 0:
                            ret = CopyItemInfo(item.getItemId(), player.getId(), player.getName())
                            if (item.getEquipOnlyId( in checkItems)):
                                ret = checkItems.get(item.getEquipOnlyId())
                                if ret.itemId != item.getItemId():
                                    continue
                                if ret.isFirst():
                                    ret.setFirst(False)
                                    msgs.add("角色: " + StringUtil.getRightPaddedStr(ret.name, ' ', 13) + " 角色ID: " + StringUtil.getRightPaddedStr(str(ret.chrId), ' ', 6) + " 道具: " + ret.itemId + " - " + ii.getName(ret.itemId) + " 唯一ID: " + item.getEquipOnlyId())
                                else:
                                    msgs.add("角色: " + StringUtil.getRightPaddedStr(player.getName(), ' ', 13) + " 角色ID: " + StringUtil.getRightPaddedStr(str(player.getId()), ' ', 6) + " 道具: " + item.getItemId() + " - " + ii.getName(item.getItemId()) + " 唯一ID: " + item.getEquipOnlyId())
                            else:
                                checkItems.put(item.getEquipOnlyId(), ret)
                    equip = player.getInventory(MapleInventoryType.EQUIPPED)
                    for item in equip.list():
                        if item.getEquipOnlyId() > 0:
                            ret = CopyItemInfo(item.getItemId(), player.getId(), player.getName())
                            if (item.getEquipOnlyId( in checkItems)):
                                ret = checkItems.get(item.getEquipOnlyId())
                                if ret.itemId != item.getItemId():
                                    continue
                                if ret.isFirst():
                                    ret.setFirst(False)
                                    msgs.add("角色: " + StringUtil.getRightPaddedStr(ret.name, ' ', 13) + " 角色ID: " + StringUtil.getRightPaddedStr(str(ret.chrId), ' ', 6) + " 道具: " + ret.itemId + " - " + ii.getName(ret.itemId) + " 唯一ID: " + item.getEquipOnlyId())
                                else:
                                    msgs.add("角色: " + StringUtil.getRightPaddedStr(player.getName(), ' ', 13) + " 角色ID: " + StringUtil.getRightPaddedStr(str(player.getId()), ' ', 6) + " 道具: " + item.getItemId() + " - " + ii.getName(item.getItemId()) + " 唯一ID: " + item.getEquipOnlyId())
                            else:
                                checkItems.put(item.getEquipOnlyId(), ret)
        checkItems.clear()
        if msgs > 0:
            c.getPlayer().dropMessage(5, "检测完成，共有: " + msgs + " 个复制信息")
            FileoutputUtil.log("装备复制.txt", "检测完成，共有: " + msgs + " 个复制信息")
            for s in msgs:
                c.getPlayer().dropMessage(5, s)
                FileoutputUtil.log("装备复制.txt", s)
            c.getPlayer().dropMessage(5, "以上信息为拥有复制道具的玩家.")
        else:
            c.getPlayer().dropMessage(5, "未检测到游戏中的角色有复制的道具信息.")
        return 1

