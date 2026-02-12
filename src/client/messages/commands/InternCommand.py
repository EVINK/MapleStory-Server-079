"""
InternCommand - Converted from Java source
Original: client/messages/commands/InternCommand.java
Package: client.messages.commands
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from constants import *  # TODO: import specific classes
# from handling.channel import *  # TODO: import specific classes
# from handling.world import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from server.maps import *  # TODO: import specific classes


class InternCommand:
    """
    Class InternCommand
    """

    def __init__(self):
        self.hellban = False


    def getPlayerLevelRequired(self) -> Any:
        return ServerConstants.PlayerGMRank.INTERN

    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        total = 0
        curConnected = c.getChannelServer().getConnectedClients()
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        c.getPlayer().dropMessage(6, "頻道: " + c.getChannelServer().getChannel() + " 线上人数: " + curConnected)
        total += curConnected
        for chr in c.getChannelServer().getPlayerStorage().getAllCharacters():
            if chr is not None && c.getPlayer().getGMLevel() >= chr.getGMLevel():
                ret = ""
                ret.append(" 角色名称 ")
                ret.append(StringUtil.getRightPaddedStr(chr.getName(), ' ', 15))
                ret.append(" ID: ")
                ret.append(StringUtil.getRightPaddedStr(chr.getId() + "", ' ', 4))
                ret.append(" 等级: ")
                ret.append(StringUtil.getRightPaddedStr(str(chr.getLevel()), ' ', 4))
                ret.append(" 职业: ")
                ret.append(chr.getJob())
                if chr.getMap() is None:
                    continue
                ret.append(" 地图: ")
                ret.append(chr.getMapId())
                ret.append("(").append(chr.getMap().getMapName()).append(")")
                c.getPlayer().dropMessage(6, ret)
        c.getPlayer().dropMessage(6, "当前频道总计在线人数: " + total)
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        channelOnline = c.getChannelServer().getConnectedClients()
        totalOnline = 0
        for cserv in ChannelServer.getAllInstances():
            totalOnline += cserv.getConnectedClients()
        c.getPlayer().dropMessage(6, "当前服务器总计在线人数: " + totalOnline + "个")
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        return 1

    def getCommand(self) -> str:
        return "Ban"

    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            c.getPlayer().dropMessage(5, "[Syntax] !" + self.getCommand() + " <玩家> <原因>")
            return 0
        ch = World.Find.findChannel(splitted[1])
        sb = "".getName())
        sb.append(" banned ").append(splitted[1]).append(": ").append(StringUtil.joinStringFrom(splitted, 2))
        target = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(splitted[1])
        if target is None || ch < 1:
            if MapleCharacter.ban(splitted[1], sb, False, c.getPlayer().isAdmin() ? 250 : c.getPlayer().getGMLevel(), splitted[0] == ("!hellban")):
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 成功离线封锁 " + splitted[1] + ".")
                return 1
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 封锁失败 " + splitted[1])
            return 0
        else:
            if c.getPlayer().getGMLevel() <= target.getGMLevel():
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 不能封锁GM...")
                return 1
            sb.append(" (IP: ").append(target.getClient().getSessionIPAddress()).append(")")
            if target.ban(sb, c.getPlayer().isAdmin(), False, self.hellban):
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 成功封锁 " + splitted[1] + ".")
                FileoutputUtil.logToFile_chr(c.getPlayer(), FileoutputUtil.ban_log, sb)
                World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "[封号系统]" + target.getName() + " 因为使用非法软件而被永久封号。").encode("utf-8"))
                return 1
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 封锁失败.")
            return 0

    @staticmethod
    def execute_c_splitted(c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(6, "上线的角色 頻道-" + c.getChannel() + ":")
        c.getPlayer().dropMessage(6, c.getChannelServer().getPlayerStorage().getOnlinePlayers(True))
        return 1


# Inner class from Java (originally nested)
class 跟踪(Warp):
    """
    Class 跟踪
    Extends: Warp
    """

    pass


# Inner class from Java (originally nested)
class 封号(Ban):
    """
    Class 封号
    Extends: Ban
    """

    pass


# Inner class from Java (originally nested)
class 隐身(Hide):
    """
    Class 隐身
    Extends: Hide
    """

    pass


# Inner class from Java (originally nested)
class 解除隐身(UnHide):
    """
    Class 解除隐身
    Extends: UnHide
    """

    pass


# Inner class from Java (originally nested)
class 在线人数(online):
    """
    Class 在线人数
    Extends: online
    """

    pass


# Inner class from Java (originally nested)
class online(CommandExecute):
    """
    Class online
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        total = 0
        curConnected = c.getChannelServer().getConnectedClients()
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        c.getPlayer().dropMessage(6, "頻道: " + c.getChannelServer().getChannel() + " 线上人数: " + curConnected)
        total += curConnected
        for chr in c.getChannelServer().getPlayerStorage().getAllCharacters():
            if chr is not None && c.getPlayer().getGMLevel() >= chr.getGMLevel():
                ret = ""
                ret.append(" 角色名称 ")
                ret.append(StringUtil.getRightPaddedStr(chr.getName(), ' ', 15))
                ret.append(" ID: ")
                ret.append(StringUtil.getRightPaddedStr(chr.getId() + "", ' ', 4))
                ret.append(" 等级: ")
                ret.append(StringUtil.getRightPaddedStr(str(chr.getLevel()), ' ', 4))
                ret.append(" 职业: ")
                ret.append(chr.getJob())
                if chr.getMap() is None:
                    continue
                ret.append(" 地图: ")
                ret.append(chr.getMapId())
                ret.append("(").append(chr.getMap().getMapName()).append(")")
                c.getPlayer().dropMessage(6, ret)
        c.getPlayer().dropMessage(6, "当前频道总计在线人数: " + total)
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        channelOnline = c.getChannelServer().getConnectedClients()
        totalOnline = 0
        for cserv in ChannelServer.getAllInstances():
            totalOnline += cserv.getConnectedClients()
        c.getPlayer().dropMessage(6, "当前服务器总计在线人数: " + totalOnline + "个")
        c.getPlayer().dropMessage(6, "-------------------------------------------------------------------------------------")
        return 1


# Inner class from Java (originally nested)
class Ban(CommandExecute):
    """
    Class Ban
    Extends: CommandExecute
    """

    def __init__(self):
        self.hellban = False
        self.hellban = False


    def getCommand(self) -> str:
        return "Ban"

    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            c.getPlayer().dropMessage(5, "[Syntax] !" + self.getCommand() + " <玩家> <原因>")
            return 0
        ch = World.Find.findChannel(splitted[1])
        sb = "".getName())
        sb.append(" banned ").append(splitted[1]).append(": ").append(StringUtil.joinStringFrom(splitted, 2))
        target = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(splitted[1])
        if target is None || ch < 1:
            if MapleCharacter.ban(splitted[1], sb, False, c.getPlayer().isAdmin() ? 250 : c.getPlayer().getGMLevel(), splitted[0] == ("!hellban")):
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 成功离线封锁 " + splitted[1] + ".")
                return 1
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 封锁失败 " + splitted[1])
            return 0
        else:
            if c.getPlayer().getGMLevel() <= target.getGMLevel():
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 不能封锁GM...")
                return 1
            sb.append(" (IP: ").append(target.getClient().getSessionIPAddress()).append(")")
            if target.ban(sb, c.getPlayer().isAdmin(), False, self.hellban):
                c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 成功封锁 " + splitted[1] + ".")
                FileoutputUtil.logToFile_chr(c.getPlayer(), FileoutputUtil.ban_log, sb)
                World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "[封号系统]" + target.getName() + " 因为使用非法软件而被永久封号。").encode("utf-8"))
                return 1
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] 封锁失败.")
            return 0


# Inner class from Java (originally nested)
class online1(CommandExecute):
    """
    Class online1
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(6, "上线的角色 頻道-" + c.getChannel() + ":")
        c.getPlayer().dropMessage(6, c.getChannelServer().getPlayerStorage().getOnlinePlayers(True))
        return 1


# Inner class from Java (originally nested)
class CnGM(CommandExecute):
    """
    Class CnGM
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(5, "<GM聊天视窗>頻道" + c.getPlayer().getClient().getChannel() + " [" + c.getPlayer().getName() + "] : " + StringUtil.joinStringFrom(splitted, 1)).encode("utf-8"))
        return 1


# Inner class from Java (originally nested)
class Hide(CommandExecute):
    """
    Class Hide
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        SkillFactory.getSkill(9001004).getEffect(1).applyTo(c.getPlayer())
        c.getPlayer().dropMessage(6, "管理员隐藏 = 开启 \r\n 解除请输入!unhide")
        return 0


# Inner class from Java (originally nested)
class UnHide(CommandExecute):
    """
    Class UnHide
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dispelBuff(9001004)
        c.getPlayer().dropMessage(6, "管理员隐藏 = 关闭 \r\n 开启请输入!hide")
        return 1


# Inner class from Java (originally nested)
class Warp(CommandExecute):
    """
    Class Warp
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        victim = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
        if victim is not None:
            if len(splitted) == 2:
                c.getPlayer().changeMap(victim.getMap(), victim.getMap().findClosestSpawnpoint(victim.getPosition()))
            else:
                target = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(int(splitted[2]))
                victim.changeMap(target, target.getPortal(0))
        else:
            try:
                victim = c.getPlayer()
                ch = World.Find.findChannel(splitted[1])
                if ch < 0:
                    target2 = c.getChannelServer().getMapFactory().getMap(int(splitted[1]))
                    c.getPlayer().changeMap(target2, target2.getPortal(0))
                else:
                    victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(splitted[1])
                    c.getPlayer().dropMessage(6, "正在换频道,请等待.")
                    if victim.getMapId() != c.getPlayer().getMapId():
                        mapp = c.getChannelServer().getMapFactory().getMap(victim.getMapId())
                        c.getPlayer().changeMap(mapp, mapp.getPortal(0))
                    c.getPlayer().changeChannel(ch)
            except ValueError as e:
                c.getPlayer().dropMessage(6, "该玩家不在线 " + e.getMessage())
                return 0
        return 1

