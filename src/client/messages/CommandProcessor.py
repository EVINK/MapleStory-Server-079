"""
CommandProcessor - Converted from Java source
Original: client/messages/CommandProcessor.java
Package: client.messages
"""

from pymysql import Connection
from typing import List
from typing import Optional, Any
from weakref import ref
import pymysql

# Internal module imports
# from constants import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from database import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes
# from client.messages.commands import *  # TODO: import specific classes


class CommandProcessor:
    """
    Class CommandProcessor
    """

    # Static initializer
    # CommandProcessor.commands = {}
    # CommandProcessor.commandList = new HashMap<Integer, ArrayList<String>>()
    # array = None
    # CommandFiles = array = new Class[]{PlayerCommand.class, GMCommand.class, InternCommand.class, AdminCommand.class}
    # for clasz in array:
    # try:
    # final ServerConstants.PlayerGMRank rankNeeded = (ServerConstants.PlayerGMRank) clasz.getMethod("getPlayerLevelRequired", (Class[]) new Class[0]).invoke(None, (Object[]) None)
    # a = clasz.getDeclaredClasses()
    # cL = []
    # for c in a:
    # try:
    # if !Modifier.isAbstract(c.getModifiers()) && !c.isSynthetic():
    # o = c.newInstance()
    # enabled = None
    # try:
    # enabled = c.getDeclaredField("enabled").getBoolean(c.getDeclaredField("enabled"))
    # except NoSuchFieldException as ex3:
    # enabled = True
    # if isinstance(o, CommandExecute) && enabled:
    # cL.add(rankNeeded.getCommandPrefix() + c.getSimpleName().lower())
    # CommandProcessor.commands.put(rankNeeded.getCommandPrefix() + c.getSimpleName().lower(), CommandObject(rankNeeded.getCommandPrefix() + c.getSimpleName().lower(), o, rankNeeded.getLevel()))
    # except Exception:
    # ex6.printStackTrace()
    # FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex6)
    # Collections.sort(cL)
    # CommandProcessor.commandList.put(rankNeeded.getLevel(), cL)
    # except Exception:
    # ex7.printStackTrace()
    # FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex7)


    @staticmethod
    def sendDisplayMessage(c: Any, msg: str, type: Any) -> None:
        if c.getPlayer() is None:
            return
        # switch (type):
            # case NORMAL:
                c.getPlayer().dropMessage(6, msg)
                break
            # case TRADE:
                c.getPlayer().dropMessage(-2, "錯誤 : " + msg)
                break

    def processCommand(self, c: Any, line: str, type: Any) -> bool:
        if line[0] != ServerConstants.PlayerGMRank.NORMAL.getCommandPrefix():  # 管理员命令
            if c.getPlayer().getGMLevel() > ServerConstants.PlayerGMRank.NORMAL.getLevel() && (line[0] == ServerConstants.PlayerGMRank.GM.getCommandPrefix() || line[0] == ServerConstants.PlayerGMRank.ADMIN.getCommandPrefix() || line[0] == ServerConstants.PlayerGMRank.INTERN.getCommandPrefix()):
                splitted = line.split(" ")
                splitted[0] = splitted[0].lower()
                if line[0] == '!':
                    co = CommandProcessor.commands.get(splitted[0])
                    if splitted[0] == ("!help"):
                        dropHelp(c, 0)
                        return True
                    if co is None || co.getType() != type:
                        sendDisplayMessage(c, "输入的命令不存在.", type)
                        return True
                    if c.getPlayer().getGMLevel() >= co.getReqGMLevel():
                        ret = co.execute(c, splitted)
                        if ret > 0 && c.getPlayer() is not None:
                            logGMCommandToDB(c.getPlayer(), line)
                            print("[ " + c.getPlayer().getName() + " ] 使用了指令: " + line)
                    else:
                        sendDisplayMessage(c, "您的权限等级不足以使用次命令.", type)
                    return True
            return False
        else:
            splitted = line.split(" ")
            splitted[0] = splitted[0].lower()
            co = CommandProcessor.commands.get(splitted[0])
            if co is None || co.getType() != type:
                sendDisplayMessage(c, "输入的玩家命令不存在,可以使用 @帮助/@help 来查看指令.", type)
                return True
            try:
                co.execute(c, splitted)
            except Exception as e:
                sendDisplayMessage(c, "有错误.", type)
                if c.getPlayer().isGM():
                    sendDisplayMessage(c, "错误: " + e, type)
            return True

    def logGMCommandToDB(self, player: Any, command: str) -> None:
        ps = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO gmlog (cid, name, command, mapid, ip) VALUES (?, ?, ?, ?, ?)")
            ps.setInt(1, player.getId())
            ps.setString(2, player.getName())
            ps.setString(3, command)
            ps.setInt(4, player.getMap().getId())
            ps.setString(5, player.getClient().getSessionIPAddress())
            ps.executeUpdate()
        except SQLException as ex:
            FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, ex)
            ex.printStackTrace()
        finally:
            try:
                ps.close()
            except SQLException as ex2:

    def dropHelp(self, c: Any, type: int) -> None:
        sb = ""
        check = 0
        if type == 0:
            check = c.getPlayer().getGMLevel()
        for i in range(= check):
            if (i in CommandProcessor.commandList):
                sb.append((type == 1) ? "VIP" : "").append("权限等級： ").append(i).append("\r\n")
                for s in CommandProcessor.commandList.get(i):
                    sb.append(s)
                    sb.append(" \r\n")
        c.getSession().write(MaplePacketCreator.getNPCTalk(9010000, 0, sb, "00 00", 0))

