"""
MaplePvp - Converted from Java source
Original: KinMS/PvP/MaplePvp.java
Package: KinMS.PvP
"""

from typing import List
from typing import Optional, Any
import math
import threading

# Internal module imports
# from handling.channel.handler import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from server.maps import *  # TODO: import specific classes
# from server import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes
# from handling.world import *  # TODO: import specific classes
# from server.life import *  # TODO: import specific classes
# from handling import *  # TODO: import specific classes


class MaplePvp:
    """
    Class MaplePvp
    """


    def parsePvpAttack(self, attack: Any, player: Any, effect: Any) -> Any:
        ret = PvpAttackInfo()
        maxdamage = player.getLevel() + 100.0
        skillId = attack.skill
        ret.skillId = skillId
        ret.critRate = 8
        ret.ignoreDef = 0
        ret.skillDamage = 1000
        ret.mobCount = 3
        ret.attackCount = 1
        pvpRange = attack.isCloseRangeAttack ? 35 : 70
        ret.facingLeft = (attack.animation < 0)
        if skillId != 0 and effect is not None:
            ret.skillDamage = effect.getDamage()
            ret.mobCount = max(1, effect.getMobCount())
            ret.attackCount = max(effect.getBulletCount(), effect.getAttackCount())
            ret.box = effect.calculateBoundingBox(player.getTruePosition(), ret.facingLeft, pvpRange)
        else:
            ret.box = calculateBoundingBox(player.getTruePosition(), ret.facingLeft, pvpRange)
        mirror = player.getBuffedValue(MapleBuffStat.影分身) is not None
        pvpAttackInfo = ret
        pvpAttackInfo.attackCount *= (mirror ? 2 : 1)
        maxdamage *= ret.skillDamage / 100.0
        ret.maxDamage = maxdamage * ret.attackCount
        if player.isGM():
            player.dropMessage(6, "Pvp伤害解析 - 最大攻击: " + maxdamage + " 数量: " + ret.mobCount + " 次数: " + ret.attackCount + " 爆击: " + ret.critRate + " 无视: " + ret.ignoreDef + " 技能伤害: " + ret.skillDamage)
        return ret

    def calculateBoundingBox(self, posFrom: Any, facingLeft: bool, range: int) -> Any:
        lt = Point(-70, -30)
        rb = Point(-10, 0)
        mylt = None
        myrb = None
        if facingLeft:
            mylt = Point(lt.x + posFrom.x - range, lt.y + posFrom.y)
            myrb = Point(rb.x + posFrom.x, rb.y + posFrom.y)
        else:
            myrb = Point(lt.x * -1 + posFrom.x + range, rb.y + posFrom.y)
            mylt = Point(rb.x * -1 + posFrom.x, lt.y + posFrom.y)
        return Rectangle(mylt.x, mylt.y, myrb.x - mylt.x, myrb.y - mylt.y)

    def inArea(self, chr: Any) -> bool:
        for rect in chr.getMap().getAreas():
            if (chr.getTruePosition( in rect)):
                return True
        return False

    def monsterBomb(self, player: Any, attacked: Any, map: Any, attack: Any) -> None:
        if player is None or attacked is None or map is None:
            return
        maxDamage = attack.maxDamage
        isCritDamage = False
        if player.getLevel() > attacked.getLevel() + 10:
            maxDamage *= 1.05
        elif player.getLevel() < attacked.getLevel() - 10:
            maxDamage /= 1.05
        elif player.getLevel() > attacked.getLevel() + 20:
            maxDamage *= 1.1
        elif player.getLevel() < attacked.getLevel() - 20:
            maxDamage /= 1.1
        elif player.getLevel() > attacked.getLevel() + 30:
            maxDamage *= 1.15
        elif player.getLevel() < attacked.getLevel() - 30:
            maxDamage /= 1.15
        if Randomizer.nextInt(100) < attack.critRate:
            maxDamage *= 1.5
            isCritDamage = True
        attackedDamage = math.floor(random.random() * (maxDamage * 0.35) + maxDamage * 0.65)
        MAX_PVP_DAMAGE = (int)(player.getStat().getLimitBreak(player) / 100.0)
        MIN_PVP_DAMAGE = 100
        if attackedDamage > MAX_PVP_DAMAGE:
            attackedDamage = MAX_PVP_DAMAGE
        if attackedDamage < MIN_PVP_DAMAGE:
            attackedDamage = MIN_PVP_DAMAGE
        hploss = attackedDamage
        mploss = 0
        if attackedDamage > 0:
            if attacked.getBuffedValue(MapleBuffStat.魔法盾) is not None:
                mploss = (int)(attackedDamage * (attacked.getBuffedValue(MapleBuffStat.魔法盾) / 100.0))
                hploss -= mploss
                if attacked.getBuffedValue(MapleBuffStat.终极无限) is not None:
                    mploss = 0
                elif mploss > attacked.getStat().getMp():
                    mploss = attacked.getStat().getMp()
                    hploss -= mploss
                attacked.addMPHP(-hploss, -mploss)
            else:
                attacked.addHP(-hploss)
        pvpMob = MapleLifeFactory.getMonster(9400711)
        map.spawnMonsterOnGroundBelow(pvpMob, attacked.getPosition())
        map.broadcastMessage(MaplePacketCreator.PVPdamagePlayer(attacked.getId(), 2, pvpMob.getId(), hploss))
        if isCritDamage:
            player.dropMessage(6, "你对玩家 " + attacked.getName() + " 造成了 " + hploss + " 点爆击伤害! 对方血量: " + attacked.getStat().getHp() + "/" + attacked.getStat().getCurrentMaxHp())
            attacked.dropMessage(6, "玩家 " + player.getName() + " 对你造成了 " + hploss + " 点爆击伤害!")
        else:
            player.dropTopMsg("你对玩家 " + attacked.getName() + " 造成了 " + hploss + " 点伤害! 对方血量: " + attacked.getStat().getHp() + "/" + attacked.getStat().getCurrentMaxHp())
            attacked.dropTopMsg("玩家 " + player.getName() + " 对你造成了 " + hploss + " 点伤害!")
        map.killMonster(pvpMob, player, False, False, 1)
        if attacked.getStat().getHp() <= 0 and not attacked.isAlive():
            expReward = attacked.getLevel() * 10 * (attacked.getLevel() / player.getLevel())
            gpReward = math.floor(random.random() * 10.0 + 10.0)
            if player.getPvpKills() * 0.25 >= player.getPvpDeaths():
                expReward *= 2
            player.gainExp(expReward, True, False, True)
            if player.getGuildId() > 0 and player.getGuildId() != attacked.getGuildId():
                World.Guild.gainGP(player.getGuildId(), gpReward)
            player.gainPvpKill()
            player.dropMessage(6, "你击败了玩家 " + attacked.getName() + "not not ")
            pvpVictory = attacked.getPvpVictory()
            attacked.gainPvpDeath()
            attacked.dropMessage(6, player.getName() + " 将你击败!")
            packet = MaplePacketCreator.serverNotice(10, "[Pvp] 玩家 " + player.getName() + " 终结了 " + attacked.getName() + " 的 " + pvpVictory + " 连斩。")
            if pvpVictory >= 5 and pvpVictory < 10:
                map.broadcastMessage(packet)
            elif pvpVictory >= 10 and pvpVictory < 20:
                player.getClient().getChannelServer().broadcastMessage(packet)
            elif pvpVictory >= 20:
                World.Broadcast.broadcastMessage(packet)

    def doPvP(self, player: Any, map: Any, attack: Any, effect: Any) -> None:
        pvpAttack = parsePvpAttack(attack, player, effect)
        mobCount = 0
        for attacked in player.getMap().getCharactersIntersect(pvpAttack.box):
            if attacked.getId() != player.getId() and attacked.isAlive() and not attacked.isHidden() and mobCount < pvpAttack.mobCount:
                mobCount += 1
                monsterBomb(player, attacked, map, pvpAttack)

    def doPartyPvP(self, player: Any, map: Any, attack: Any, effect: Any) -> None:
        pvpAttack = parsePvpAttack(attack, player, effect)
        mobCount = 0
        for attacked in player.getMap().getCharactersIntersect(pvpAttack.box):
            if attacked.getId() != player.getId() and attacked.isAlive() and not attacked.isHidden() and (player.getParty() is None or player.getParty() != attacked.getParty()) and mobCount < pvpAttack.mobCount:
                mobCount += 1
                monsterBomb(player, attacked, map, pvpAttack)

    def doGuildPvP(self, player: Any, map: Any, attack: Any, effect: Any) -> None:
        pvpAttack = parsePvpAttack(attack, player, effect)
        mobCount = 0
        for attacked in player.getMap().getCharactersIntersect(pvpAttack.box):
            if attacked.getId() != player.getId() and attacked.isAlive() and not attacked.isHidden() and (player.getGuildId() == 0 or player.getGuildId() != attacked.getGuildId()) and mobCount < pvpAttack.mobCount:
                mobCount += 1
                monsterBomb(player, attacked, map, pvpAttack)

