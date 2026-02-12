"""
PlayerCommand - Converted from Java source
Original: client/messages/commands/PlayerCommand.java
Package: client.messages.commands
"""

from typing import List
from typing import Optional, Any
import math
import time

# Internal module imports
# from client.messages.CommandProcessorUtil import *  # TODO: import specific classes
# from constants import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from scripting import *  # TODO: import specific classes
# from server.maps import *  # TODO: import specific classes
# from server.life import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes
# from handling.world import *  # TODO: import specific classes


class PlayerCommand:
    """
    Class PlayerCommand
    """


    def getPlayerLevelRequired(self) -> Any:
        return ServerConstants.PlayerGMRank.NORMAL

    @staticmethod
    def execute(c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        c.getPlayer().dropMessage(1, "假死已处理完毕.")
        c.getPlayer().dropMessage(6, "当前时间是" + FileoutputUtil.CurrentReadable_Time() + " GMT+8 | 经验值倍率 " + (int)(c.getPlayer().getEXPMod() * 100 * (c.getPlayer().getStat().expBuff / 100.0)) + "%, 怪物倍率 " + (int)(c.getPlayer().getDropMod() * 100 * (c.getPlayer().getStat().dropBuff / 100.0)) + "%, 金币倍率 " + (int)(c.getPlayer().getStat().mesoBuff / 100.0 * 100.0) + "%")
        c.getPlayer().dropMessage(6, "当前延迟 " + c.getPlayer().getClient().getLatency() + " 毫秒")
        if c.getPlayer().isAdmin():
            c.sendPacket(MaplePacketCreator.sendPyramidEnergy("massacre_hit", str(50)))
        return 1

    @staticmethod
    def execute_c_splitted(c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        npc = NPCScriptManager.getInstance()
        npc.start(c, 9900007, 86)
        if c.getPlayer().getBossLog("狮熊Boss") > 0:
            c.getPlayer().resetBossLog("狮熊Boss")
        if c.getPlayer().getBossLog("普通黑龙") > 0:
            c.getPlayer().resetBossLog("普通黑龙")
        if c.getPlayer().getBossLog("树精Boss") > 0:
            c.getPlayer().resetBossLog("树精Boss")
        if c.getPlayer().getBossLog("普通扎昆") > 0:
            c.getPlayer().resetBossLog("普通扎昆")
        return 1

    def getMessage(self) -> str:
        return "".append("not abc <怪物ID> - 召唤怪物")


# Inner class from Java (originally nested)
class 帮助(help):
    """
    Class 帮助
    Extends: help
    """

    pass


# Inner class from Java (originally nested)
class 自由(zy):
    """
    Class 自由
    Extends: zy
    """

    pass


# Inner class from Java (originally nested)
class 怪物(Mob):
    """
    Class 怪物
    Extends: Mob
    """

    pass


# Inner class from Java (originally nested)
class 万能(wn):
    """
    Class 万能
    Extends: wn
    """

    pass


# Inner class from Java (originally nested)
class 爆率(Mobdrop):
    """
    Class 爆率
    Extends: Mobdrop
    """

    pass


# Inner class from Java (originally nested)
class ea(查看):
    """
    Class ea
    Extends: 查看
    """

    pass


# Inner class from Java (originally nested)
class 解卡(查看):
    """
    Class 解卡
    Extends: 查看
    """

    pass


# Inner class from Java (originally nested)
class 破攻(pg):
    """
    Class 破攻
    Extends: pg
    """

    pass


# Inner class from Java (originally nested)
class 查看(CommandExecute):
    """
    Class 查看
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        c.getPlayer().dropMessage(1, "假死已处理完毕.")
        c.getPlayer().dropMessage(6, "当前时间是" + FileoutputUtil.CurrentReadable_Time() + " GMT+8 | 经验值倍率 " + (int)(c.getPlayer().getEXPMod() * 100 * (c.getPlayer().getStat().expBuff / 100.0)) + "%, 怪物倍率 " + (int)(c.getPlayer().getDropMod() * 100 * (c.getPlayer().getStat().dropBuff / 100.0)) + "%, 金币倍率 " + (int)(c.getPlayer().getStat().mesoBuff / 100.0 * 100.0) + "%")
        c.getPlayer().dropMessage(6, "当前延迟 " + c.getPlayer().getClient().getLatency() + " 毫秒")
        if c.getPlayer().isAdmin():
            c.sendPacket(MaplePacketCreator.sendPyramidEnergy("massacre_hit", str(50)))
        return 1


# Inner class from Java (originally nested)
class zy(CommandExecute):
    """
    Class zy
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        npc = NPCScriptManager.getInstance()
        npc.start(c, 9900007, 86)
        if c.getPlayer().getBossLog("狮熊Boss") > 0:
            c.getPlayer().resetBossLog("狮熊Boss")
        if c.getPlayer().getBossLog("普通黑龙") > 0:
            c.getPlayer().resetBossLog("普通黑龙")
        if c.getPlayer().getBossLog("树精Boss") > 0:
            c.getPlayer().resetBossLog("树精Boss")
        if c.getPlayer().getBossLog("普通扎昆") > 0:
            c.getPlayer().resetBossLog("普通扎昆")
        return 1


# Inner class from Java (originally nested)
class wn(CommandExecute):
    """
    Class wn
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        npc = NPCScriptManager.getInstance()
        npc.start(c, 9900004, 0)
        return 1


# Inner class from Java (originally nested)
class Mobdrop(CommandExecute):
    """
    Class Mobdrop
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        NPCScriptManager.getInstance().dispose(c)
        c.getSession().write(MaplePacketCreator.enableActions())
        npc = NPCScriptManager.getInstance()
        npc.start(c, 2000)
        return 1


# Inner class from Java (originally nested)
class Mob(CommandExecute):
    """
    Class Mob
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        mob = None
        for monstermo in c.getPlayer().getMap().getMapObjectsInRange(c.getPlayer().getPosition(), 100000.0, Arrays.asList(MapleMapObjectType.MONSTER)):
            mob = monstermo
            if mob.isAlive():
                c.getPlayer().dropMessage(6, "怪物: " + mob)
                break
        if mob is None:
            c.getPlayer().dropMessage(6, "查看失败: 1.没有找到需要查看的怪物信息. 2.你周围没有怪物出现. 3.有些怪物禁止查看.")
        return 1


# Inner class from Java (originally nested)
class CGM(CommandExecute):
    """
    Class CGM
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if splitted[1] is None:
            c.getPlayer().dropMessage(6, "请打字谢谢.")
            return 1
        if c.getPlayer().isGM():
            c.getPlayer().dropMessage(6, "因为你自己是GM无法使用此命令,可以尝试!cngm <讯息> 來建立GM聊天頻道~")
            return 1
        if not c.getPlayer().getCheatTracker().GMSpam(100000, 1):
            World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "頻道 " + c.getPlayer().getClient().getChannel() + " 玩家 [" + c.getPlayer().getName() + "] : " + StringUtil.joinStringFrom(splitted, 1)).encode("utf-8"))
            c.getPlayer().dropMessage(6, "讯息已经发给GM了!")
        else:
            c.getPlayer().dropMessage(6, "为了防止对GM刷屏所以每1分鐘只能发一次.")
        return 1


# Inner class from Java (originally nested)
class pg(CommandExecute):
    """
    Class pg
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        VipCount = c.getPlayer().getVip()
        maxdamage = 199999 + VipCount * 10000
        if maxdamage >= 2147483647 or maxdamage < 0:
            maxdamage = 2147483647
        c.getPlayer().refreshPGDamage()
        mds = "您当前的伤害上限为：" + maxdamage + " 当前破攻伤害为：" + c.getPlayer().curPGDamage
        c.getPlayer().dropMessage(5, "伤害上限计算公式： 基础伤害(199999) + 您的破功等级*10000 ")
        c.getPlayer().dropMessage(-1, mds)
        c.getPlayer().dropMessage(5, mds)
        return 1


# Inner class from Java (originally nested)
class help(CommandExecute):
    """
    Class help
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        c.getPlayer().dropMessage(5, "指令列表 :")
        c.getPlayer().dropMessage(5, "@解卡/@查看/@ea <解除异常+查看当前状态>")
        c.getPlayer().dropMessage(5, "@爆率 爆率 <查询当前地图怪物爆率>")
        c.getPlayer().dropMessage(5, "@自由/@zy < 立即回到自于市场 >")
        c.getPlayer().dropMessage(5, "@万能/@wn < 打开多功能NPC >")
        c.getPlayer().dropMessage(5, "@怪物/@Mob <查看身边怪物信息/血量>")
        c.getPlayer().dropMessage(5, "@pg 查看自己的破攻上限(也可以使用 @破攻 )")
        c.getPlayer().dropMessage(5, "@abc 召唤怪物\n(蜗牛、黑木妖、火独眼兽、小石球、海胆、鲨鱼、骷髅龙、小铜人、银人、小金人)\n最高可召唤100只 每天召唤10次")
        return 1


# Inner class from Java (originally nested)
class abc(CommandExecute):
    """
    Class abc
    Extends: CommandExecute
    """


    def execute(self, c: Any, splitted: list) -> int:
        if c.getPlayer().getVipexpired() < int(time.time() * 1000):
            c.getPlayer().dropMessage("你不是VIP玩家或者VIP过期，请联系管理员")
            return 0
        if len(splitted) < 2:
            return 0
        name = splitted[1]
        mid = 0
        if "小金人" == (name):
            mid = 9600019
        elif "银人" == (name):
            mid = 9600024
        elif "小铜人" == (name):
            mid = 9600020
        elif "骷髅龙" == (name):
            mid = 8190003
        elif "鲨鱼" == (name):
            mid = 8150100
        elif "海胆" == (name):
            mid = 2230108
        elif "小石球" == (name):
            mid = 5200000
        elif "火独眼兽" == (name):
            mid = 2230100
        elif "黑木妖" == (name):
            mid = 1110101
        elif "蜗牛" == (name):
            mid = 100100
        else:
            c.getPlayer().dropMessage("暂不支持召唤: "+name)
            return 0
        if c.getPlayer().getBossLog(name) > 9:
            c.getPlayer().dropMessage(6,"今日召唤已超过10次，请明天再来吧")
            return 0
        c.getPlayer().setBossLog(name)
        num = min(CommandProcessorUtil.getOptionalIntArg(splitted, 2, 1), 500)
        if num > 100:
            num = 100
        for i in range(num):
            mob = MapleLifeFactory.getMonster(mid)
            c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, c.getPlayer().getPosition())
        return 1

    def getMessage(self) -> str:
        return "".append("not abc <怪物ID> - 召唤怪物")

