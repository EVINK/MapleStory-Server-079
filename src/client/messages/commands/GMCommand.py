"""
GMCommand - Converted from Java source
Original: client/messages/commands/GMCommand.java
Package: client.messages.commands
"""

from typing import Dict
from typing import Optional, Any
import os

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.ArrayMap import *  # TODO: import specific classes
# from tools.DateUtil import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class GMCommand:
    """
    Class GMCommand
    """

    def __init__(self):
        self.hellban = False


    def getPlayerLevelRequired(self) -> Any:
        return ServerConstants.PlayerGMRank.GM

    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        victim = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
        if victim is not None:
            victim.changeMap(c.getPlayer().getMap(), c.getPlayer().getMap().findClosestSpawnpoint(c.getPlayer().getPosition()))
        else:
            ch = World.Find.findChannel(splitted[1])
            if ch < 0:
                c.getPlayer().dropMessage(5, "角色不在线")
                return 1
            victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(splitted[1])
            c.getPlayer().dropMessage(5, "正在传送玩家到身边")
            victim.dropMessage(5, "GM正在传送你")
            if victim.getMapId() != c.getPlayer().getMapId():
                mapp = victim.getClient().getChannelServer().getMapFactory().getMap(c.getPlayer().getMapId())
                victim.changeMap(mapp, mapp.getPortal(0))
            victim.changeChannel(c.getChannel())
        return 1

    def getCommand(self) -> str:
        return "UnBan"

    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(6, "[Syntax] not " + self.getCommand() + " <原因>")
            return 0
        ret = None
        if self.hellban:
            ret = MapleClient.unHellban(splitted[1])
        else:
            ret = MapleClient.unban(splitted[1])
        if ret == -2:
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] SQL error.")
            return 0
        if ret == -1:
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] The character does not exist.")
            return 0
        c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] Successfully unbanned!")
        ret_ = MapleClient.unbanIPMacs(splitted[1])
        if ret_ == -2:
            c.getPlayer().dropMessage(6, "[UnbanIP] SQL error.")
        elif ret_ == -1:
            c.getPlayer().dropMessage(6, "[UnbanIP] The character does not exist.")
        elif ret_ == 0:
            c.getPlayer().dropMessage(6, "[UnbanIP] No IP or Mac with that character exists!")
        elif ret_ == 1:
            c.getPlayer().dropMessage(6, "[UnbanIP] IP/Mac -- one of them was found and unbanned.")
        elif ret_ == 2:
            c.getPlayer().dropMessage(6, "[UnbanIP] Both IP and Macs were unbanned.")
        return (ret_ > 0) ? 1 : 0

    @staticmethod
    def execute_c_splitted(c: Any, splitted: list) -> int:
        ChannelServer.forceRemovePlayerByCharName(splitted[1])
        c.getPlayer().dropMessage("解除卡号卡角成功")
        return 1

    def getMessage(self) -> str:
        return "".append("not exprate <倍率> - 更改经验倍率")


# Inner class from Java (originally nested)
class 拉(WarpHere):
    """
    Class 拉
    Extends: WarpHere
    """

    pass


# Inner class from Java (originally nested)
class 等级(Level):
    """
    Class 等级
    Extends: Level
    """

    pass


# Inner class from Java (originally nested)
class 转职(Job):
    """
    Class 转职
    Extends: Job
    """

    pass


# Inner class from Java (originally nested)
class 清空(ClearInv):
    """
    Class 清空
    Extends: ClearInv
    """

    pass


# Inner class from Java (originally nested)
class 踢人(DC):
    """
    Class 踢人
    Extends: DC
    """

    pass


# Inner class from Java (originally nested)
class 读取玩家(spy):
    """
    Class 读取玩家
    Extends: spy
    """

    pass


# Inner class from Java (originally nested)
class 解除封号(UnBan):
    """
    Class 解除封号
    Extends: UnBan
    """

    pass


# Inner class from Java (originally nested)
class 刷钱(GainMeso):
    """
    Class 刷钱
    Extends: GainMeso
    """

    pass


# Inner class from Java (originally nested)
class 给点卷(GainCash):
    """
    Class 给点卷
    Extends: GainCash
    """

    pass


# Inner class from Java (originally nested)
class WarpHere(CommandExecute):
    """
    Class WarpHere
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        victim = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
        if victim is not None:
            victim.changeMap(c.getPlayer().getMap(), c.getPlayer().getMap().findClosestSpawnpoint(c.getPlayer().getPosition()))
        else:
            ch = World.Find.findChannel(splitted[1])
            if ch < 0:
                c.getPlayer().dropMessage(5, "角色不在线")
                return 1
            victim = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(splitted[1])
            c.getPlayer().dropMessage(5, "正在传送玩家到身边")
            victim.dropMessage(5, "GM正在传送你")
            if victim.getMapId() != c.getPlayer().getMapId():
                mapp = victim.getClient().getChannelServer().getMapFactory().getMap(c.getPlayer().getMapId())
                victim.changeMap(mapp, mapp.getPortal(0))
            victim.changeChannel(c.getChannel())
        return 1


# Inner class from Java (originally nested)
class UnBan(CommandExecute):
    """
    Class UnBan
    Extends: CommandExecute
    """

    def __init__(self):
        self.hellban = False
        self.hellban = False


    def getCommand(self) -> str:
        return "UnBan"

    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(6, "[Syntax] not " + self.getCommand() + " <原因>")
            return 0
        ret = None
        if self.hellban:
            ret = MapleClient.unHellban(splitted[1])
        else:
            ret = MapleClient.unban(splitted[1])
        if ret == -2:
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] SQL error.")
            return 0
        if ret == -1:
            c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] The character does not exist.")
            return 0
        c.getPlayer().dropMessage(6, "[" + self.getCommand() + "] Successfully unbanned!")
        ret_ = MapleClient.unbanIPMacs(splitted[1])
        if ret_ == -2:
            c.getPlayer().dropMessage(6, "[UnbanIP] SQL error.")
        elif ret_ == -1:
            c.getPlayer().dropMessage(6, "[UnbanIP] The character does not exist.")
        elif ret_ == 0:
            c.getPlayer().dropMessage(6, "[UnbanIP] No IP or Mac with that character exists!")
        elif ret_ == 1:
            c.getPlayer().dropMessage(6, "[UnbanIP] IP/Mac -- one of them was found and unbanned.")
        elif ret_ == 2:
            c.getPlayer().dropMessage(6, "[UnbanIP] Both IP and Macs were unbanned.")
        return (ret_ > 0) ? 1 : 0


# Inner class from Java (originally nested)
class DC(CommandExecute):
    """
    Class DC
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        ChannelServer.forceRemovePlayerByCharName(splitted[1])
        c.getPlayer().dropMessage("解除卡号卡角成功")
        return 1


# Inner class from Java (originally nested)
class Job(CommandExecute):
    """
    Class Job
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().changeJob(int(splitted[1]))
        return 1


# Inner class from Java (originally nested)
class GainMeso(CommandExecute):
    """
    Class GainMeso
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().gainMeso(Integer.MAX_VALUE - c.getPlayer().getMeso(), True)
        return 1


# Inner class from Java (originally nested)
class Level(CommandExecute):
    """
    Class Level
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().setLevel(Short.parseShort(splitted[1]))
        c.getPlayer().levelUp()
        if c.getPlayer().getExp() < 0:
            c.getPlayer().gainExp(-c.getPlayer().getExp(), False, False, True)
        return 1


# Inner class from Java (originally nested)
class spy(CommandExecute):
    """
    Class spy
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            c.getPlayer().dropMessage(6, "使用规则: not spy <玩家名字>")
        else:
            victim = c.getChannelServer().getPlayerStorage().getCharacterByName(splitted[1])
            if victim.getGMLevel() > c.getPlayer().getGMLevel() and c.getPlayer().getId() != victim.getId():
                c.getPlayer().dropMessage(5, "你不能查看比你高权限的人!")
                return 0
            if victim is not None:
                c.getPlayer().dropMessage(5, "此玩家(" + victim.getId() + ")状态:")
                c.getPlayer().dropMessage(5, "等級: " + victim.getLevel() + "职业: " + victim.getJob() + "名声: " + victim.getFame())
                c.getPlayer().dropMessage(5, "地图: " + victim.getMapId() + " - " + victim.getMap().getMapName())
                c.getPlayer().dropMessage(5, "力量: " + victim.getStat().getStr() + " or 敏捷: " + victim.getStat().getDex() + " or 智力: " + victim.getStat().getInt() + " or 运气: " + victim.getStat().getLuk())
                c.getPlayer().dropMessage(5, "拥有 " + victim.getMeso() + " 金币.")
            else:
                c.getPlayer().dropMessage(5, "找不到此玩家.")
        return 1


# Inner class from Java (originally nested)
class ClearInv(CommandExecute):
    """
    Class ClearInv
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        eqs = new ArrayMap<Pair<Short, Short>, MapleInventoryType>()
        s = splitted[1]
        # switch (s):
            # case "全部":
                for type in MapleInventoryType.values():
                    for item in c.getPlayer().getInventory(type):
                        eqs.put(new Pair<Short, Short>(item.getPosition(), item.getQuantity()), type)
                break
            # case "已装备道具":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.EQUIPPED):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.EQUIPPED)
                break
            # case "武器":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.EQUIP):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.EQUIP)
                break
            # case "消耗":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.USE):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.USE)
                break
            # case "装饰":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.SETUP):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.SETUP)
                break
            # case "其他":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.ETC):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.ETC)
                break
            # case "特殊":
                for item2 in c.getPlayer().getInventory(MapleInventoryType.CASH):
                    eqs.put(new Pair<Short, Short>(item2.getPosition(), item2.getQuantity()), MapleInventoryType.CASH)
                break
            # default:
                c.getPlayer().dropMessage(6, "[全部/已装备道具/武器/消耗/装饰/其他/特殊]")
                break
        for (final Map.Entry<Pair<Short, Short>, MapleInventoryType> eq : eqs.items())
            MapleInventoryManipulator.removeFromSlot(c, eq.getValue(), eq.getKey().left, eq.getKey().right, False, False)
        return 1


# Inner class from Java (originally nested)
class ExpRate(CommandExecute):
    """
    Class ExpRate
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 1:
            rate = int(splitted[1])
            if len(splitted) > 2 and splitted[2].lower() == "all".lower():
                for cserv in ChannelServer.getAllInstances():
                    cserv.setExpRate(rate)
            else:
                c.getChannelServer().setExpRate(rate)
            c.getPlayer().dropMessage(6, "经验倍率已改变更为 " + rate + "x")
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not exprate <倍率> - 更改经验倍率")


# Inner class from Java (originally nested)
class GainCash(CommandExecute):
    """
    Class GainCash
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 3:
            return 0
        player = c.getPlayer()
        amount = 0
        name = ""
        try:
            amount = int(splitted[1])
            name = splitted[2]
        except NumberFormatException as ex:
            c.getPlayer().dropMessage("该玩家不在线")
            return 1
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage("该玩家不在线")
            return 1
        player = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if player is None:
            c.getPlayer().dropMessage("该玩家不在线")
            return 1
        player.modifyCSPoints(1, amount, True)
        player.dropMessage("已经收到点卷" + amount + "点")
        msg = "GM " + c.getPlayer().getName() + " 給了 " + player.getName() + " 点卷 " + amount + "点"
        for cserv2 in ChannelServer.getAllInstances():
            for mch2 in cserv2.getPlayerStorage().getAllCharacters():
                mch2.startMapEffect(msg, 5121009)
        FileoutputUtil.logToFile("logs/Data/给予点卷_"+ DateUtil.getCurrentDateStr2()+"_a.txt", "\r\n " + FileoutputUtil.NowTime() + " GM " + c.getPlayer().getName() + " 给了 " + player.getName() + " 点卷 " + amount + "点")
        return 1

    def getMessage(self) -> str:
        return "".append("not gaingash <數量> <玩家> - 取得Gash点数")


# Inner class from Java (originally nested)
class CheckGash(CommandExecute):
    """
    Class CheckGash
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        ch = World.Find.findChannel(name)
        if ch <= 0:
            c.getPlayer().dropMessage(6, "玩家必须在线")
            return 0
        chrs = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(name)
        if chrs is None:
            c.getPlayer().dropMessage(5, "找不到该角色")
        else:
            c.getPlayer().dropMessage(6, chrs.getName() + " 有 " + chrs.getCSPoints(1) + " 点数.")
        return 1

    def getMessage(self) -> str:
        return "".append("not checkgash <玩家名称> - 检查点数")


# Inner class from Java (originally nested)
class Say(CommandExecute):
    """
    Class Say
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if len(splitted) > 1:
            sb = ""
            sb.append("[")
            sb.append(c.getPlayer().getName())
            sb.append("] ")
            sb.append(StringUtil.joinStringFrom(splitted, 1))
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, sb).encode("utf-8"))
            return 1
        return 0

    def getMessage(self) -> str:
        return "".append("not say 讯息 - 服务器公告")

