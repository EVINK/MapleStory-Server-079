"""
SummonHandler - Converted from Java source
Original: handling/channel/handler/SummonHandler.java
Package: handling.channel.handler
"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import threading

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.SummonSkillEntry import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.SummonAttackEntry import *  # TODO: import specific classes
# from server.maps.AnimatedMapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleSummon import *  # TODO: import specific classes
# from server.maps.SummonMovementType import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes


class SummonHandler:
    """
    Class SummonHandler
    """


    def MoveSummon(self, slea: Any, chr: Any) -> None:
        oid = slea.readInt()
        startPos = Point(slea.readShort(), slea.readShort())
        res = MovementParse.parseMovement(slea, 4)
        if chr is None:
            return
        for sum in chr.getSummons():
            if sum.getObjectId() == oid and sum.getMovementType() != SummonMovementType.不会移动:
                pos = sum.getPosition()
                MovementParse.updatePosition(res, sum, 0)
                if res > 0:
                    chr.getMap().broadcastMessage(chr, MaplePacketCreator.moveSummon(chr.getId(), oid, startPos, res), sum.getPosition())
                    break
                break

    def DamageSummon(self, slea: Any, chr: Any) -> None:
        if chr is None or not chr.isAlive() or chr.getMap() is None:
            return
        unkByte = slea.readByte()
        damage = slea.readInt()
        monsterIdFrom = slea.readInt()
        iter = chr.getSummonsReadLock().iterator()
        remove = False
        try:
            while iter.hasNext():
                summon = iter.next()
                if summon.is替身术() and summon.getOwnerId() == chr.getId() and damage > 0:
                    summon.addHP((short)(-damage))
                    if summon.getHP() <= 0:
                        remove = True
                    chr.getMap().broadcastMessage(chr, MaplePacketCreator.damageSummon(chr.getId(), summon.getSkill(), damage, unkByte, monsterIdFrom), summon.getTruePosition())
                    break
        finally:
            chr.unlockSummonsReadLock()
        if remove:
            chr.cancelEffectFromBuffStat(MapleBuffStat.替身术)

    def SummonAttack(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None or not chr.isAlive() or chr.getMap() is None:
            return
        map = chr.getMap()
        obj = map.getMapObject(slea.readInt(), MapleMapObjectType.SUMMON)
        if obj is None:
            return
        summon = obj
        if summon.getOwnerId() != chr.getId() or summon.getSkillLevel() <= 0:
            return
        sse = SkillFactory.getSummonData(summon.getSkill())
        if sse is None:
            return
        slea.skip(8)
        tick = slea.readInt()
        chr.updateTick(tick)
        summon.CheckSummonAttackFrequency(chr, tick)
        slea.skip(8)
        animation = slea.readByte()
        slea.skip(8)
        numAttacked = slea.readByte()
        if numAttacked > sse.mobCount:
            chr.getCheatTracker().registerOffense(CheatingOffense.召唤兽攻击怪物数量异常)
            chr.dropMessage(5, "[警告] 请不要使用非法程序。召唤兽攻击怪物数量错误.")
            return
        allDamage = []
        chr.getCheatTracker().checkSummonAttack()
        for i in range(numAttacked):
            mob = map.getMonsterByOid(slea.readInt())
            if mob is not None:
                if chr.getPosition().distanceSq(mob.getPosition()) > 400000.0:
                    chr.getCheatTracker().registerOffense(CheatingOffense.召唤兽攻击范围过大)
                    chr.dropMessage(5, "[警告] 请不要使用非法程序。召唤兽攻击范围过大.")
                slea.skip(14)
                damage = slea.readInt()
                allDamage.add(SummonAttackEntry(mob, damage))
        if (not summon.isChangedMap()) {}
        summonSkill = SkillFactory.getSkill(summon.getSkill())
        summonEffect = summonSkill.getEffect(summon.getSkillLevel())
        if summonEffect is None:
            chr.dropMessage(5, "召唤兽攻击出现错误 => 攻击效果为空.")
            return
        for attackEntry in allDamage:
            toDamage = attackEntry.getDamage()
            mob2 = attackEntry.getMonster()
            if toDamage > 0 and summonEffect.getMonsterStati() > 0 and summonEffect.makeChanceResult():
                for (final Map.Entry<MonsterStatus, Integer> z : summonEffect.getMonsterStati().items())
                    mob2.applyStatus(chr, MonsterStatusEffect(z.getKey(), z.getValue(), summonSkill.getId(), None, False), summonEffect.isPoison(), 4000, False)
            if not chr.isGM() and toDamage >= 199999:
                chr.getClient().getSession().write(MaplePacketCreator.serverNotice(1, "召唤兽攻击过高，你已被断开连接"))
                c.disconnect(True, True)
                return
            mob2.damage(chr, toDamage, True)
            chr.checkMonsterAggro(mob2)
            if mob2.isAlive():
                continue
            chr.getClient().getSession().write(MobPacket.killMonster(mob2.getObjectId(), 1))
        if summon.isGaviota():
            chr.getMap().broadcastMessage(MaplePacketCreator.removeSummon(summon, True))
            chr.getMap().removeMapObject(summon)
            chr.removeVisibleMapObject(summon)
            chr.cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
            chr.cancelEffectFromBuffStat(MapleBuffStat.REAPER)

