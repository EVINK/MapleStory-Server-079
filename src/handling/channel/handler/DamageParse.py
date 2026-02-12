"""
DamageParse - Converted from Java source
Original: handling/channel/handler/DamageParse.java
Package: handling.channel.handler
"""

from typing import Dict
from typing import List
from typing import Optional, Any
import math
import threading

# Internal module imports
# from KinMS.PvP.MaplePvp import *  # TODO: import specific classes
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.anticheat.CheatTracker import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.Element import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MapleMonsterStats import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapItem import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from tools.AttackPair import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.LittleEndianAccessor import *  # TODO: import specific classes


class DamageParse:
    """
    Class DamageParse
    """

    # Static initializer
    # charges = new int[] { 1211005, 1211006 }


    @staticmethod
    def applyAttack(attack: Any, theSkill: Any, player: Any, attackCount: int, maxDamagePerMonster: float, effect: Any, attack_type: Any) -> None:
        if not player.isAlive():
            player.getCheatTracker().registerOffense(CheatingOffense.人物死亡攻击)
            return
        if attack.real:
        if attack.skill != 0:
            ban = False
            lastReason = ""
            reason = ""
            if effect is None:
                player.getClient().getSession().write(MaplePacketCreator.enableActions())
                return
            if GameConstants.isMulungSkill(attack.skill):
                if player.getMapId() / 10000 != 92502:
                return
                player.mulung_EnergyModify(False)
            if GameConstants.isPyramidSkill(attack.skill):
                if player.getMapId() / 1000000 != 926:
                return
                if player.getPyramidSubway() is None or not player.getPyramidSubway().onSkillUse(player):
                return
        totDamage = 0
        map = player.getMap()
        if map.isPvpMap():
            MaplePvp.doPvP(player, map, attack, effect)
        elif map.isPartyPvpMap():
            MaplePvp.doPartyPvP(player, map, attack, effect)
        elif map.isGuildPvpMap():
            MaplePvp.doGuildPvP(player, map, attack, effect)
        if attack.skill == 4211006:
        for oned in attack.allDamage:
            if oned.attack is not None:
            continue
            mapobject = map.getMapObject(oned.objectid, MapleMapObjectType.ITEM)
            if mapobject is not None:
                mapitem = mapobject
                mapitem.getLock().lock()
                try:
                    if mapitem.getMeso() > 0:
                        if mapitem.isPickedUp():
                        return
                        map.removeMapObject(mapitem)
                        map.broadcastMessage(MaplePacketCreator.explodeDrop(mapitem.getObjectId()))
                        mapitem.setPickedUp(True)
                    else:
                        player.getCheatTracker().registerOffense(CheatingOffense.其他异常)
                        return
                finally:
                    mapitem.getLock().unlock()
                continue
            player.getCheatTracker().registerOffense(CheatingOffense.金钱炸弹_不存在道具)
            return
        totDamageToOneMonster = 0
        hpMob = 0
        stats = player.getStat()
        ShdowPartnerAttackPercentage = 0
        if attack_type == AttackType.RANGED_WITH_SHADOWPARTNER or attack_type == AttackType.NON_RANGED_WITH_MIRROR:
            shadowPartnerEffect = None
            if attack_type == AttackType.NON_RANGED_WITH_MIRROR:
                shadowPartnerEffect = player.getStatForBuff(MapleBuffStat.MIRROR_IMAGE)
            else:
                shadowPartnerEffect = player.getStatForBuff(MapleBuffStat.影分身)
            if shadowPartnerEffect is not None:
            if attack.skill != 0 and attack_type != AttackType.NON_RANGED_WITH_MIRROR:
                ShdowPartnerAttackPercentage = shadowPartnerEffect.getY()
            else:
                ShdowPartnerAttackPercentage = shadowPartnerEffect.getX()
            attackCount /= 2
        for oned in attack.allDamage:
            monster = map.getMonsterByOid(oned.objectid)
            if monster is not None:
                totDamageToOneMonster = 0
                hpMob = monster.getHp()
                monsterstats = monster.getStats()
                fixeddmg = monsterstats.getFixedDamage()
                Tempest = (monster.getStatusSourceID(MonsterStatus.冻结) == 21120006)
                overallAttackCount = 0
                for eachde in (Iterable<Pair<Integer, Boolean>>)oned.attack:
                    eachd = eachde.left
                    overallAttackCount = (byte)(overallAttackCount + 1)
                    if fixeddmg != -1:
                        if monsterstats.getOnlyNoramlAttack():
                            eachd = Integer.valueOf((attack.skill != 0) ? 0 : fixeddmg)
                        else:
                            eachd = Integer.valueOf(fixeddmg)
                    elif not monsterstats.getOnlyNoramlAttack():
                        if not player.isGM():
                    if player is None:
                    return
                    totDamageToOneMonster += eachd
                    if monster.getId() == 9300021 and player.getPyramidSubway() is not None:
                    player.getPyramidSubway().onMiss(player)
                totDamage += totDamageToOneMonster
                player.checkMonsterAggro(monster)
                if attack.skill == 2301002 and not monsterstats.getUndead():
                    player.ban("修改WZ", True, True, False)
                    FileoutputUtil.logToFile_chr(player, FileoutputUtil.ban_log, "使用群体治愈伤害怪物 " + monster.getId())
                    World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[封号系统] " + player.getName() + " 该玩家攻击异常被系统自动封号处理。").encode("utf-8"))
                    return
                Position_range = player.getPosition().distanceSq(monster.getPosition())
                Count_range = 7000000.0
                if Position_range > Count_range and (player.getJob() != 2000 or player.getJob() != 2100 or player.getJob() != 2111 or player.getJob() != 2112):
                    player.getCheatTracker().registerOffense(CheatingOffense.攻击范围过大, " 技能 " + attack.skill + " 范围 : " + Position_range + "正常范围 " + Count_range)
                    return
                if player.getBuffedValue(MapleBuffStat.敛财术) is not None:
                # switch (attack.skill):
                    # case 0:
                    # case 4001334:
                    # case 4201005:
                    # case 4211002:
                    # case 4211004:
                    # case 4221003:
                    # case 4221007:
                    handlePickPocket(player, monster, oned)
                    break
                ds = player.getStatForBuff(MapleBuffStat.隐身术)
                if (ds is not None and not player.isGM() and (
                ds.getSourceId() == 4221007 or not ds.makeChanceResult() or ds.getSourceId() == 0))
                player.cancelEffectFromBuffStat(MapleBuffStat.隐身术)
                if totDamageToOneMonster > 0:
                    remainingHP = None
                    skills = None
                    if attack.skill != 1221011 and attack.skill != 3221007:
                        monster.damage(player, totDamageToOneMonster, True, attack.skill)
                    else:
                        monster.damage(player, monster.getStats().isBoss() ? totDamageToOneMonster : monster.getHp(), True, attack.skill)
                    if monster.isBuffed(MonsterStatus.反射物理伤害):
                    player.addHP(-(3000 + Randomizer.nextInt(1500)))
                    if (stats.hpRecoverProp > 0 and
                    Randomizer.nextInt(100) <= stats.hpRecoverProp)
                    player.healHP(stats.hpRecover)
                    if (stats.mpRecoverProp > 0 and
                    Randomizer.nextInt(100) <= stats.mpRecoverProp)
                    player.healMP(stats.mpRecover)
                    if player.getBuffedValue(MapleBuffStat.连环吸血) is not None:
                        stats.setHp(stats.getHp() + min(monster.getMobMaxHp(), min((int)(totDamage * player.getStatForBuff(MapleBuffStat.连环吸血).getX() / 10.0), stats.getMaxHp() / 2)), True)
                        player.updateSingleStat(MapleStat.HP, player.getHp())
                    # switch (attack.skill):
                        # case 4101005:
                        # case 5111004:
                        # case 14101006:
                        # case 15111001:
                        stats.setHp(stats.getHp() + min(monster.getMobMaxHp(), min((int)(totDamage * theSkill.getEffect(player.getSkillLevel(theSkill)).getX() / 100.0), stats.getMaxHp() / 2)), True)
                        player.updateSingleStat(MapleStat.HP, player.getHp())
                        break
                        # case 5211006:
                        # case 5220011:
                        # case 22151002:
                        player.setLinkMid(monster.getObjectId())
                        break
                        # case 1311005:
                        remainingHP = stats.getHp() - totDamage * effect.getX() / 100
                        stats.setHp((remainingHP < 1) ? 1 : remainingHP)
                        player.updateSingleStat(MapleStat.HP, player.getHp())
                        break
                        # case 4001002:
                        # case 4001334:
                        # case 4001344:
                        # case 4111005:
                        # case 4121007:
                        # case 4201005:
                        # case 4211002:
                        # case 4221001:
                        # case 4221007:
                        # case 4301001:
                        # case 4311002:
                        # case 4311003:
                        # case 4331000:
                        # case 4331004:
                        # case 4331005:
                        # case 4341005:
                        skills = new int[] { 4120005, 4220005, 14110004 }
                        for i in skills:
                            skill = SkillFactory.getSkill(i)
                            if player.getSkillLevel(skill) > 0:
                                venomEffect = skill.getEffect(player.getSkillLevel(skill))
                                if not venomEffect.makeChanceResult():
                                break
                                monster.applyStatus(player, MonsterStatusEffect(MonsterStatus.中毒, Integer.valueOf(1), i, None, False), True, venomEffect.getDuration(), True)
                                break
                        break
                        # case 4201004:
                        monster.handleSteal(player)
                        break
                        # case 21000002:
                        # case 21100001:
                        # case 21100002:
                        # case 21100004:
                        # case 21110002:
                        # case 21110003:
                        # case 21110004:
                        # case 21110006:
                        # case 21110007:
                        # case 21110008:
                        # case 21120002:
                        # case 21120005:
                        # case 21120006:
                        # case 21120009:
                        # case 21120010:
                        if player.getBuffedValue(MapleBuffStat.属性攻击) is not None and not monster.getStats().isBoss():
                            eff = player.getStatForBuff(MapleBuffStat.属性攻击)
                            if eff is not None and eff.getSourceId() == 21111005:
                            monster.applyStatus(player, MonsterStatusEffect(MonsterStatus.速度, Integer.valueOf(eff.getX()), eff.getSourceId(), None, False), False, (eff.getY() * 1000), False)
                        if player.getBuffedValue(MapleBuffStat.战神抗压) is not None and not monster.getStats().isBoss():
                            eff = player.getStatForBuff(MapleBuffStat.战神抗压)
                            if eff is not None and eff.makeChanceResult() and not monster.isBuffed(MonsterStatus.NEUTRALISE):
                            monster.applyStatus(player, MonsterStatusEffect(MonsterStatus.NEUTRALISE, Integer.valueOf(1), eff.getSourceId(), None, False), False, (eff.getX() * 1000), False)
                        break
                    if totDamageToOneMonster > 0:
                        weapon_ = player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)-11)
                        if weapon_ is not None:
                            stat = GameConstants.getStatFromWeapon(weapon_.getItemId())
                            if stat is not None and Randomizer.nextInt(100) < GameConstants.getStatChance():
                                monsterStatusEffect = MonsterStatusEffect(stat, Integer.valueOf(GameConstants.getXForStat(stat)), GameConstants.getSkillForStat(stat), None, False)
                                monster.applyStatus(player, monsterStatusEffect, False, 10000, False, False)
                        if player.getBuffedValue(MapleBuffStat.刺眼箭) is not None:
                            eff = player.getStatForBuff(MapleBuffStat.刺眼箭)
                            if eff.makeChanceResult():
                                monsterStatusEffect = MonsterStatusEffect(MonsterStatus.命中, Integer.valueOf(eff.getX()), eff.getSourceId(), None, False)
                                monster.applyStatus(player, monsterStatusEffect, False, (eff.getY() * 1000), False)
                        if player.getBuffedValue(MapleBuffStat.击退箭) is not None:
                            skill = SkillFactory.getSkill(3121007)
                            eff = skill.getEffect(player.getSkillLevel(skill))
                            if eff.makeChanceResult():
                                monsterStatusEffect = MonsterStatusEffect(MonsterStatus.速度, Integer.valueOf(eff.getX()), 3121007, None, False)
                                monster.applyStatus(player, monsterStatusEffect, False, (eff.getY() * 1000), False)
                        if player.getJob() == 121:
                        for charge in charges:
                            skill = SkillFactory.getSkill(charge)
                            if player.isBuffFrom(MapleBuffStat.属性攻击, skill):
                                monsterStatusEffect = MonsterStatusEffect(MonsterStatus.冻结, Integer.valueOf(1), charge, None, False)
                                monster.applyStatus(player, monsterStatusEffect, False, (skill.getEffect(player.getSkillLevel(skill)).getY() * 2000), False)
                                break
                        if player.getJob() == 221:
                            冰咆哮 = { 2211002 }
                            int arrayOfInt1[] = 冰咆哮, i = len(arrayOfInt1)
                            b = 0
                            if b < i:
                                bing = arrayOfInt1[b]
                                skill = SkillFactory.getSkill(bing)
                                monsterStatusEffect = MonsterStatusEffect(MonsterStatus.冻结, Integer.valueOf(1), bing, None, False)
                                monster.applyStatus(player, monsterStatusEffect, False, (skill.getEffect(player.getSkillLevel(skill)).getY() * 2000), False)
                    if (effect is not None and effect.getMonsterStati() > 0 and
                    effect.makeChanceResult())
                    for (Map.Entry<MonsterStatus, Integer> z : (Iterable<Map.Entry<MonsterStatus, Integer>>)effect.getMonsterStati().items())
                    monster.applyStatus(player, MonsterStatusEffect(z.getKey(), z.getValue(), theSkill.getId(), None, False), effect.isPoison(), effect.getDuration(), False)
        (player.getStat()).mesoBuff = 100.0
        buff = player.getBuffedValue(MapleBuffStat.聚财术)
        if buff is not None:
        (player.getStat()).mesoBuff *= buff / 100.0
        buff = player.getBuffedValue(MapleBuffStat.金币_率)
        if buff is not None:
        (player.getStat()).mesoBuff *= buff / 100.0
        if attack.skill == 4331003 and totDamageToOneMonster < hpMob:
        return
        if attack.skill != 0 and (attack.targets > 0 or (attack.skill != 4331003 and attack.skill != 4341002)) and attack.skill != 21101003 and attack.skill != 5110001 and attack.skill != 15100004 and attack.skill != 11101002 and attack.skill != 13101002:
        effect.applyTo(player, attack.position)
        if totDamage > 1:
            tracker = player.getCheatTracker()
            tracker.setAttacksWithoutHit(True)
            if tracker.getAttacksWithoutHit() > 1000:
            tracker.registerOffense(CheatingOffense.人物无敌, Integer.toString(tracker.getAttacksWithoutHit()))

    def applyAttackMagic(self, attack: Any, theSkill: Any, player: Any, effect: Any) -> None:
        if not player.isAlive():
            player.getCheatTracker().registerOffense(CheatingOffense.人物死亡攻击)
            return
        if effect is None:
            player.getClient().getSession().write(MaplePacketCreator.enableActions())
            return
        if (attack.real) {}
        if GameConstants.isMulungSkill(attack.skill):
            if player.getMapId() / 10000 != 92502:
                return
            player.mulung_EnergyModify(False)
        if GameConstants.isPyramidSkill(attack.skill):
            if player.getMapId() / 1000000 != 926:
                return
            if player.getPyramidSubway() is None or not player.getPyramidSubway().onSkillUse(player):
                return
        stats = player.getStat()
        element = (player.getBuffedValue(MapleBuffStat.自然力重置) is not None) ? Element.NEUTRAL : theSkill.getElement()
        maxDamagePerHit = None
        if attack.skill == 1000 or attack.skill == 10001000 or attack.skill == 20001000 or attack.skill == 20011000 or attack.skill == 30001000:
            maxDamagePerHit = 40
        elif GameConstants.isPyramidSkill(attack.skill):
            maxDamagePerHit = 1
        else:
            v75 = (effect.getMatk() * 0.058)
            # minDamagePerHit = stats.getTotalMagic() * (stats.getInt() * 0.5 + (v75 * v75) + (effect.getMastery() * 0.9 * effect.getMatk()) * 3.3) / 100;
            maxDamagePerHit = stats.getTotalMagic() * (stats.getInt() * 0.5 + (v75 * v75) + effect.getMatk() * 3.3) / 100
        maxDamagePerHit *= 1.04  # Avoid any errors for now
        MaxDamagePerHit = 0
        totDamage = 0
        eaterSkill = SkillFactory.getSkill(GameConstants.getMPEaterForJob(player.getJob()))
        eaterLevel = player.getSkillLevel(eaterSkill)
        map = player.getMap()
        if map.isPvpMap():
            MaplePvp.doPvP(player, map, attack, effect)
        elif map.isPartyPvpMap():
            MaplePvp.doPartyPvP(player, map, attack, effect)
        elif map.isGuildPvpMap():
            MaplePvp.doGuildPvP(player, map, attack, effect)
        for oned in attack.allDamage:
            monster = map.getMonsterByOid(oned.objectid)
            if monster is not None:
                Tempest = monster.getStatusSourceID(MonsterStatus.冻结) == 21120006 and not monster.getStats().isBoss()
                totDamageToOneMonster = 0
                monsterstats = monster.getStats()
                fixeddmg = monsterstats.getFixedDamage()
                overallAttackCount = 0
                for eachde in oned.attack:
                    eachd = eachde.left
                    overallAttackCount += 1
                    if fixeddmg != -1:
                        eachd = (monsterstats.getOnlyNoramlAttack() ? 0 : fixeddmg)
                    elif monsterstats.getOnlyNoramlAttack():
                        eachd = 0
                    elif not player.isGM():
                        if Tempest:  # Buffed with Tempest
                            # In special case such as Chain lightning, the damage will be reduced from the maxMP.
                            if eachd > monster.getMobMaxHp():
                                eachd = min(monster.getMobMaxHp(), Integer.MAX_VALUE)
                                player.getCheatTracker().registerOffense(CheatingOffense.魔法伤害过高)
                        elif not monster.isBuffed(MonsterStatus.免疫伤害) and not monster.isBuffed(MonsterStatus.免疫魔法攻击) and not monster.isBuffed(MonsterStatus.反射物理伤害):
                            if eachd > maxDamagePerHit:
                                player.getCheatTracker().registerOffense(CheatingOffense.魔法伤害过高)
                                if eachd > MaxDamagePerHit * 2:
                                    # System.out.println("EXCEED!!! Client damage : " + eachd + " Server : " + MaxDamagePerHit);
                                    eachd = (int) (MaxDamagePerHit * 2)  # Convert to server calculated damage
                                    FileoutputUtil.logToFile_chr(player, FileoutputUtil.fixdam_ph, " 技能 " + attack.skill + " 怪物 " + monster.getId() + " 预计伤害:" + MaxDamagePerHit + " 实际" + eachd)
                                    player.getCheatTracker().registerOffense(CheatingOffense.魔法伤害过高2)
                        elif eachd > maxDamagePerHit * 2:
                            FileoutputUtil.logToFile_chr(player, FileoutputUtil.fixdam_ph, " 技能 " + attack.skill + " 怪物 " + monster.getId() + " 预计伤害:" + MaxDamagePerHit + " 实际" + eachd)
                            eachd = (int) (maxDamagePerHit)
                    totDamageToOneMonster += eachd
                totDamage += totDamageToOneMonster
                player.checkMonsterAggro(monster)
                Position_range = player.getPosition().distanceSq(monster.getPosition())
                Count_range = 7000000.0
                if Position_range > Count_range and (player.getJob() != 2000 or player.getJob() != 2100 or player.getJob() != 2111 or player.getJob() != 2112):
                    player.getCheatTracker().registerOffense(CheatingOffense.攻击范围过大, " 技能 " + attack.skill + " 范围 : " + Position_range + "正常范围 " + Count_range)
                    return
                if attack.skill == 2301002 and not monsterstats.getUndead():
                    player.getCheatTracker().registerOffense(CheatingOffense.治愈术攻击非不死系怪物)
                    return
                if totDamageToOneMonster <= 0:
                    continue
                monster.damage(player, totDamageToOneMonster, True, attack.skill)
                if monster.isBuffed(MonsterStatus.反射魔法伤害):
                    player.addHP(-(3000 + Randomizer.nextInt(1500)))
                # switch (attack.skill):
                    # case 2221003:
                        monster.setTempEffectiveness(Element.FIRE, theSkill.getEffect(player.getSkillLevel(theSkill)).getDuration())
                        break
                    # case 2121003:
                        monster.setTempEffectiveness(Element.ICE, theSkill.getEffect(player.getSkillLevel(theSkill)).getDuration())
                        break
                if effect is not None and effect.getMonsterStati() > 0 and effect.makeChanceResult():
                    for (final Map.Entry<MonsterStatus, Integer> z : effect.getMonsterStati().items())
                        monster.applyStatus(player, MonsterStatusEffect(z.getKey(), z.getValue(), theSkill.getId(), None, False), effect.isPoison(), effect.getDuration(), False)
                if eaterLevel <= 0:
                    continue
                eaterSkill.getEffect(eaterLevel).applyPassive(player, monster)
        if attack.skill != 2301002:
            effect.applyTo(player)
        player.getStat().mesoBuff = 100.0
        buff = player.getBuffedValue(MapleBuffStat.聚财术)
        if buff is not None:
            stat = player.getStat()
            stat.mesoBuff *= buff / 100.0
        buff = player.getBuffedValue(MapleBuffStat.金币_率)
        if buff is not None:
            stat2 = player.getStat()
            stat2.mesoBuff *= buff / 100.0
        if totDamage > 1:
            tracker = player.getCheatTracker()
            tracker.setAttacksWithoutHit(True)
            if tracker.getAttacksWithoutHit() > 1000:
                tracker.registerOffense(CheatingOffense.人物无敌, Integer.toString(tracker.getAttacksWithoutHit()))

    def CalculateMaxMagicDamagePerHit(self, chr: Any, skill: Any, monster: Any, mobstats: Any, stats: Any, elem: Any, sharpEye: int, maxDamagePerMonster: float) -> float:
        dLevel = max(mobstats.getLevel() - chr.getLevel(), 0)
        Accuracy = (int)(math.floor(stats.getTotalInt() / 10.0) + math.floor(stats.getTotalLuk() / 10.0))
        MinAccuracy = mobstats.getEva() * (dLevel * 2 + 51) / 120
        if MinAccuracy > Accuracy and skill.getId() != 1000 and skill.getId() != 10001000 and skill.getId() != 20001000 and skill.getId() != 20011000 and skill.getId() != 30001000 and not GameConstants.isPyramidSkill(skill.getId()):
            return 0.0
        elemMaxDamagePerMob = 0.0
        # switch (monster.getEffectiveness(elem)):
            # case 免疫:
                elemMaxDamagePerMob = 1.0
                break
            # case 正常:
                elemMaxDamagePerMob = ElementalStaffAttackBonus(elem, maxDamagePerMonster, stats)
                break
            # case 虚弱:
                elemMaxDamagePerMob = ElementalStaffAttackBonus(elem, maxDamagePerMonster * 1.5, stats)
                break
            # case 增强:
                elemMaxDamagePerMob = ElementalStaffAttackBonus(elem, maxDamagePerMonster * 0.5, stats)
                break
            # default:
                raise RuntimeError("Unknown enum constant")
        elemMaxDamagePerMob -= mobstats.getMagicDefense() * 0.5
        elemMaxDamagePerMob += elemMaxDamagePerMob / 100.0 * sharpEye
        elemMaxDamagePerMob += elemMaxDamagePerMob * (mobstats.isBoss() ? stats.bossdam_r : stats.dam_r) / 100.0
        # switch (skill.getId()):
            # case 1000:
            # case 10001000:
            # case 20001000:
            # case 20011000:
            # case 30001000:
                elemMaxDamagePerMob = 40.0
                break
            # case 1020:
            # case 10001020:
            # case 20001020:
            # case 20011020:
            # case 30001020:
                elemMaxDamagePerMob = 1.0
                break
        if skill.getId() == 2301002:
            elemMaxDamagePerMob *= 2.0
        if elemMaxDamagePerMob > 199999.0:
            elemMaxDamagePerMob = 199999.0
        elif elemMaxDamagePerMob < 0.0:
            elemMaxDamagePerMob = 1.0
        return elemMaxDamagePerMob

    def ElementalStaffAttackBonus(self, elem: Any, elemMaxDamagePerMob: float, stats: Any) -> float:
        # switch (elem):
            # case FIRE:
                return elemMaxDamagePerMob / 100.0 * stats.element_fire
            # case ICE:
                return elemMaxDamagePerMob / 100.0 * stats.element_ice
            # case LIGHTING:
                return elemMaxDamagePerMob / 100.0 * stats.element_light
            # case POISON:
                return elemMaxDamagePerMob / 100.0 * stats.element_psn
            # default:
                return elemMaxDamagePerMob / 100.0 * stats.def

    def handlePickPocket(self, player: Any, mob: Any, oned: Any) -> None:
        maxmeso = player.getBuffedValue(MapleBuffStat.敛财术)
        skill = SkillFactory.getSkill(4211003)
        s = skill.getEffect(player.getSkillLevel(skill))
        for eachde in oned.attack:
            eachd = eachde.left
            if s.makeChanceResult():
                player.getMap().spawnMesoDrop(min(max(eachd / 20000.0 * maxmeso, 1.0), maxmeso), Point((int)(mob.getTruePosition().getX() + Randomizer.nextInt(100) - 50.0), mob.getTruePosition().getY()), mob, player, False, 0)

    def CalculateMaxWeaponDamagePerHit(self, player: Any, monster: Any, attack: Any, theSkill: Any, attackEffect: Any, maximumDamageToMonster: float, CriticalDamagePercent: int) -> float:
        if player.getMapId() / 1000000 == 914:
            return 199999.0
        elements = []
        defined = False
        if theSkill is not None:
            elements.add(theSkill.getElement())
            # switch (theSkill.getId()):
                # case 3001004:
                # case 33101001:
                    defined = True
                    break
                # case 1000:
                # case 10001000:
                # case 20001000:
                # case 20011000:
                # case 30001000:
                    maximumDamageToMonster = 40.0
                    defined = True
                    break
                # case 1020:
                # case 10001020:
                # case 20001020:
                # case 20011020:
                # case 30001020:
                    maximumDamageToMonster = 1.0
                    defined = True
                    break
                # case 4331003:
                    maximumDamageToMonster = (double)(monster.getStats().isBoss() ? 199999 : monster.getHp())
                    defined = True
                    break
                # case 3221007:
                    maximumDamageToMonster = (double)(monster.getStats().isBoss() ? 199999 : monster.getMobMaxHp())
                    defined = True
                    break
                # case 1221011:
                    maximumDamageToMonster = (double)(monster.getStats().isBoss() ? 199999 : (monster.getHp() - 1))
                    defined = True
                    break
                # case 4211006:
                    maximumDamageToMonster = 750000.0
                    defined = True
                    break
                # case 1009:
                # case 10001009:
                # case 20001009:
                # case 20011009:
                # case 30001009:
                    defined = True
                    maximumDamageToMonster = (double)(monster.getStats().isBoss() ? (monster.getMobMaxHp() / 30 * 100) : monster.getMobMaxHp())
                    break
                # case 3211006:
                    if monster.getStatusSourceID(MonsterStatus.冻结) == 3211003:
                        defined = True
                        maximumDamageToMonster = monster.getHp()
                        break
                    break
        if player.getBuffedValue(MapleBuffStat.属性攻击) is not None:
            chargeSkillId = player.getBuffSource(MapleBuffStat.属性攻击)
            # switch (chargeSkillId):
                # case 1211003:
                # case 1211004:
                    elements.add(Element.FIRE)
                    break
                # case 1211005:
                # case 1211006:
                # case 21111005:
                    elements.add(Element.ICE)
                    break
                # case 1211007:
                # case 1211008:
                # case 15101006:
                    elements.add(Element.LIGHTING)
                    break
                # case 1221003:
                # case 1221004:
                # case 11111007:
                    elements.add(Element.HOLY)
                    break
                # case 12101005:
                    elements.clear()
                    break
        if player.getBuffedValue(MapleBuffStat.LIGHTNING_CHARGE) is not None:
            elements.add(Element.LIGHTING)
        elementalMaxDamagePerMonster = maximumDamageToMonster
        if elements > 0:
            elementalEffect = 0.0
            # switch (attack.skill):
                # case 3211003:
                    elementalEffect = attackEffect.getX() / 200.0
                    break
                # default:
                    elementalEffect = 0.5
                    break
            for element in elements:
                # switch (monster.getEffectiveness(element)):
                    # case 免疫:
                        elementalMaxDamagePerMonster = 1.0
                        continue
                    # case 虚弱:
                        elementalMaxDamagePerMonster *= 1.0 + elementalEffect
                        continue
                    # case 增强:
                        elementalMaxDamagePerMonster *= 1.0 - elementalEffect
                        continue
        moblevel = monster.getStats().getLevel()
        d = (short)((moblevel > player.getLevel()) ? ((short)(moblevel - player.getLevel())) : 0)
        elementalMaxDamagePerMonster = elementalMaxDamagePerMonster * (1.0 - 0.01 * d) - monster.getStats().getPhysicalDefense() * 0.5
        elementalMaxDamagePerMonster += elementalMaxDamagePerMonster / 100.0 * CriticalDamagePercent
        if theSkill is not None and theSkill.isChargeSkill() and player.getKeyDownSkill_Time() == 0:
            return 0.0
        homing = player.getStatForBuff(MapleBuffStat.导航辅助)
        if homing is not None and player.getLinkMid() == monster.getObjectId() and homing.getSourceId() == 5220011:
            elementalMaxDamagePerMonster += elementalMaxDamagePerMonster * homing.getX()
        stat = player.getStat()
        elementalMaxDamagePerMonster += elementalMaxDamagePerMonster * (monster.getStats().isBoss() ? stat.bossdam_r : stat.dam_r) / 100.0
        if player.getDebugMessage():
            player.dropMessage("[伤害计算] 属性伤害:" + elementalMaxDamagePerMonster)
        if elementalMaxDamagePerMonster > 199999.0:
            if not defined:
                elementalMaxDamagePerMonster = 199999.0
        elif elementalMaxDamagePerMonster < 0.0:
            elementalMaxDamagePerMonster = 1.0
        return elementalMaxDamagePerMonster

    def DivideAttack(self, attack: Any, rate: int) -> Any:
        attack.real = False
        if rate <= 1:
            return attack
        for p in attack.allDamage:
            if p.attack is not None:
                for pair in p.attack:
                    eachd = pair
                    pair.left /= rate
        return attack

    def Modify_AttackCrit(self, attack: Any, chr: Any, type: int) -> Any:
        CriticalRate = chr.getStat().passive_sharpeye_rate()
        shadow = (type == 2 and chr.getBuffedValue(MapleBuffStat.影分身) is not None) or (type == 1 and chr.getBuffedValue(MapleBuffStat.MIRROR_IMAGE) is not None)
        if attack.skill != 4211006 and attack.skill != 3211003 and attack.skill != 4111004 and (CriticalRate > 0 or attack.skill == 4221001 or attack.skill == 3221007):
            for p in attack.allDamage:
                if p.attack is not None:
                    hit = 0
                    mid_att = p.attack / 2
                    eachd_copy = new ArrayList<Pair<Integer, Boolean>>(p.attack)
                    for eachd in p.attack:
                        hit += 1
                        if not eachd.right:
                            if attack.skill == 4221001:
                                eachd.right = (hit == 4 and Randomizer.nextInt(100) < 90)
                            elif attack.skill == 3221007 or eachd.left > 199999:
                                eachd.right = True
                            elif shadow and hit > mid_att:
                                eachd.right = eachd_copy.get(hit - 1 - mid_att).right
                            else:
                                eachd.right = (Randomizer.nextInt(100) < CriticalRate)
                            eachd_copy.get(hit - 1).right = eachd.right
        return attack

    def parseDmgMa(self, lea: Any, chr: Any) -> Any:
        ret = AttackInfo()
        lea.skip(1)
        lea.skip(8)
        ret.tbyte = lea.readByte()
        ret.targets = (byte)(ret.tbyte >>> 4 & 0xF)
        ret.hits = (byte)(ret.tbyte & 0xF)
        lea.skip(8)
        ret.skill = lea.readInt()
        lea.skip(12)
        # switch (ret.skill):
            # case 2121001:
            # case 2221001:
            # case 2321001:
            # case 22121000:
            # case 22151001:
                ret.charge = lea.readInt()
                break
            # default:
                ret.charge = -1
                break
        lea.skip(1)
        ret.unk = 0
        ret.display = lea.readByte()
        ret.animation = lea.readByte()
        lea.skip(1)
        ret.speed = lea.readByte()
        ret.lastAttackTickCount = lea.readInt()
        ret.allDamage = []
        for i in range(ret.targets):
            oid = lea.readInt()
            lea.skip(14)
            allDamageNumbers = new ArrayList<Pair<Integer, Boolean>>()
            monster = chr.getMap().getMonsterByOid(oid)
            PGInfo = "#b#e[破攻伤害]\r\n"
            for j in range(ret.hits):
                PGInfo = ""
                damage = lea.readInt()
                maxdamage = 199999 + chr.getVip() * 10000
                show = False
                baoji = False
                pogong = False
                if chr.getStat().getTotalMagic() >= 1999 and damage > 1:
                    skill = SkillFactory.getSkill(ret.skill)
                    matk = skill.getEffect(chr.getSkillLevel(skill)).getMatk()
                    if Randomizer.nextInt(100) < chr.getStat().passive_sharpeye_rate():
                        matk += chr.getStat().passive_sharpeye_percent()
                        baoji = True
                    baseAttack = chr.getStat().getCurrentMaxBaseDamage()
                    tmpdamage = (int)(baseAttack / 100.0 * matk / 100.0 * (80 + Randomizer.nextInt(21)))
                    if monster is not None:
                        element = (chr.getBuffedValue(MapleBuffStat.自然力重置) is not None) ? Element.NEUTRAL : skill.getElement()
                        # switch (monster.getEffectiveness(element)):
                            # case 免疫:
                                tmpdamage = 1
                                break
                            # case 正常:
                                tmpdamage = ElementalStaffAttackBonus(element, tmpdamage, chr.getStat())
                                break
                            # case 虚弱:
                                tmpdamage = ElementalStaffAttackBonus(element, tmpdamage * 1.5, chr.getStat())
                                break
                            # case 增强:
                                tmpdamage = ElementalStaffAttackBonus(element, tmpdamage * 0.5, chr.getStat())
                                break
                            # default:
                                raise RuntimeError("Unknown enum constant")
                        moblevel = monster.getStats().getLevel()
                        d = ((moblevel > chr.getLevel()) ? ((short)(moblevel - chr.getLevel())) : 0)
                        tmpdamage = (int)(tmpdamage * (1.0 - 0.01 * d) - monster.getStats().getMagicDefense() * 0.5)
                        if tmpdamage < 0:
                            tmpdamage = 1
                        tmpdamage *= (monster.getStats().isBoss() ? chr.getStat().bossdam_r : chr.getStat().dam_r)
                    if tmpdamage > damage:
                        damage = tmpdamage
                        show = True
                damage = calcMonsterDecreaseDamage(damage, monster, chr, True)
                if show:
                    if baoji:
                        PGInfo = "#b#e[破攻伤害]\r\n#r" + damage + "\r\n"
                    else:
                        PGInfo = "#b#e[破攻伤害]\r\n#d" + damage + "\r\n"
                if damage > maxdamage:
                    damage = maxdamage
                    pogong = True
                if pogong:
                    PGInfo = PGInfo + "#b#e[已达上限]\r\n#r" + damage
                allDamageNumbers.add(new Pair<Integer, Boolean>(damage, False))
            if (PGInfo > 12) {}
            lea.skip(4)
            ret.allDamage.add(AttackPair(oid, allDamageNumbers))
        ret.position = lea.readPos()
        return ret

    def parseDmgM(self, lea: Any, chr: Any) -> Any:
        ret = AttackInfo()
        lea.skip(1)
        lea.skip(8)
        ret.tbyte = lea.readByte()
        ret.targets = (byte)(ret.tbyte >>> 4 & 0xF)
        ret.hits = (byte)(ret.tbyte & 0xF)
        lea.skip(8)
        ret.skill = lea.readInt()
        lea.skip(12)
        # switch (ret.skill):
            # case 4341002:
            # case 4341003:
            # case 5101004:
            # case 5201002:
            # case 14111006:
            # case 15101003:
                ret.charge = lea.readInt()
                break
            # default:
                ret.charge = 0
                break
        lea.skip(1)
        ret.unk = 0
        ret.display = lea.readByte()
        ret.animation = lea.readByte()
        lea.skip(1)
        ret.speed = lea.readByte()
        ret.lastAttackTickCount = lea.readInt()
        ret.allDamage = []
        if ret.skill == 4211006:
            return parseMesoExplosion(lea, ret, chr)
        for i in range(ret.targets):
            oid = lea.readInt()
            lea.skip(14)
            allDamageNumbers = new ArrayList<Pair<Integer, Boolean>>()
            monster = chr.getMap().getMonsterByOid(oid)
            PGInfo = "#b#e[破攻伤害]\r\n"
            for j in range(ret.hits):
                PGInfo = ""
                damage = lea.readInt()
                maxdamage = 199999 + chr.getVip() * 10000
                show = False
                pogong = False
                if chr.getStat().getTotalWatk() > 1999 and damage > 1:
                    damage = (int)(damage / 1999.0 * chr.getStat().getTotalWatk())
                    show = True
                if ret.skill == 1221011 or ret.skill == 3221007:
                    damage = 199999
                damage = calcMonsterDecreaseDamage(damage, monster, chr, True)
                if show:
                    PGInfo = "#b#e[破攻伤害]\r\n#d" + damage + "\r\n"
                if damage > maxdamage:
                    damage = maxdamage
                    pogong = True
                if pogong:
                    PGInfo = PGInfo + "#b#e[已达上限]\r\n#r" + damage
                allDamageNumbers.add(new Pair<Integer, Boolean>(damage, False))
            if (PGInfo > 12) {}
            lea.skip(4)
            ret.allDamage.add(AttackPair(oid, allDamageNumbers))
        ret.position = lea.readPos()
        return ret

    def parseDmgR(self, lea: Any, chr: Any) -> Any:
        ret = AttackInfo()
        lea.skip(1)
        lea.skip(8)
        ret.tbyte = lea.readByte()
        ret.targets = (byte)(ret.tbyte >>> 4 & 0xF)
        ret.hits = (byte)(ret.tbyte & 0xF)
        lea.skip(8)
        ret.skill = lea.readInt()
        lea.skip(12)
        # switch (ret.skill):
            # case 3121004:
            # case 3221001:
            # case 5221004:
            # case 13111002:
                lea.skip(4)
                break
        ret.charge = -1
        lea.skip(1)
        ret.unk = 0
        ret.display = lea.readByte()
        ret.animation = lea.readByte()
        lea.skip(1)
        ret.speed = lea.readByte()
        ret.lastAttackTickCount = lea.readInt()
        ret.starSlot = lea.readShort()
        ret.cashSlot = lea.readShort()
        ret.AOE = lea.readByte()
        ret.allDamage = []
        for i in range(ret.targets):
            oid = lea.readInt()
            lea.skip(14)
            monster = chr.getMap().getMonsterByOid(oid)
            allDamageNumbers = new ArrayList<Pair<Integer, Boolean>>()
            PGInfo = "#b#e[破攻伤害]\r\n"
            for j in range(ret.hits):
                PGInfo = ""
                damage = lea.readInt()
                maxdamage = 199999 + chr.getVip() * 10000
                show = False
                baoji = False
                pogong = False
                if damage > 1 and (ret.skill == 4121007 or ret.skill == 4001344 or ret.skill == 14001004 or ret.skill == 14111005):
                    skill = SkillFactory.getSkill(ret.skill)
                    watk = skill.getEffect(chr.getSkillLevel(skill)).getDamage()
                    if Randomizer.nextInt(100) < chr.getStat().passive_sharpeye_rate():
                        watk += chr.getStat().passive_sharpeye_percent()
                        baoji = True
                    baseAttack = chr.getStat().getCurrentMaxBaseDamage()
                    damage = (int)(baseAttack / 100.0 * watk / 100.0 * (80 + Randomizer.nextInt(21)))
                    if monster is not None:
                        element = (chr.getBuffedValue(MapleBuffStat.自然力重置) is not None) ? Element.NEUTRAL : skill.getElement()
                        # switch (monster.getEffectiveness(element)):
                            # case 免疫:
                                damage = 1
                                break
                            # case 虚弱:
                                damage *= 1.5
                                break
                            # case 增强:
                                damage *= 0.5
                                break
                        moblevel = monster.getStats().getLevel()
                        d = ((moblevel > chr.getLevel()) ? ((short)(moblevel - chr.getLevel())) : 0)
                        damage = (int)(damage * (1.0 - 0.01 * d) - monster.getStats().getPhysicalDefense() * 0.5)
                        if damage < 0:
                            damage = 1
                        damage *= (monster.getStats().isBoss() ? chr.getStat().bossdam_r : chr.getStat().dam_r)
                    show = True
                elif chr.getStat().getTotalWatk() > 1999 and damage > 1:
                    damage = (int)(damage / 1999.0 * chr.getStat().getTotalWatk())
                    show = True
                if ret.skill == 1221011 or ret.skill == 3221007:
                    damage = 199999
                damage = calcMonsterDecreaseDamage(damage, monster, chr, True)
                if show:
                    if baoji:
                        PGInfo = "#b#e[破攻伤害]\r\n#r" + damage + "\r\n"
                    else:
                        PGInfo = "#b#e[破攻伤害]\r\n#d" + damage + "\r\n"
                if damage > maxdamage:
                    damage = maxdamage
                    pogong = True
                if pogong:
                    PGInfo = PGInfo + "#b#e[已达上限]\r\n#r" + damage
                allDamageNumbers.add(new Pair<Integer, Boolean>(damage, False))
            if PGInfo > 12:
                chr.getClient().getSession().write(MaplePacketCreator.sendHint(PGInfo, 80, 5))
            lea.skip(4)
            ret.allDamage.add(AttackPair(oid, allDamageNumbers))
        lea.skip(4)
        ret.position = lea.readPos()
        return ret

    def parseMesoExplosion(self, lea: Any, ret: Any, chr: Any) -> Any:
        if ret.hits == 0:
            lea.skip(4)
            bullets = lea.readByte()
            for j in range(bullets):
                ret.allDamage.add(AttackPair(lea.readInt(), None))
                lea.skip(1)
            lea.skip(2)
            return ret
        for i in range(ret.targets):
            oid = lea.readInt()
            lea.skip(12)
            bullets = lea.readByte()
            allDamageNumbers = new ArrayList<Pair<Integer, Boolean>>()
            for k in range(bullets):
                damage = lea.readInt()
                allDamageNumbers.add(new Pair<Integer, Boolean>(damage, False))
            ret.allDamage.add(AttackPair(oid, allDamageNumbers))
            lea.skip(4)
        lea.skip(4)
        bullets = lea.readByte()
        for l in range(bullets):
            ret.allDamage.add(AttackPair(lea.readInt(), None))
            lea.skip(1)
        lea.skip(2)
        return ret

    def Damage_AttackCount(self, player: Any, effect: Any, attack: Any, attackCount: int) -> str:
        reason = "None"
        last = attackCount
        mirror_fix = False
        if player.getJob() >= 411 and player.getJob() <= 412:
            mirror_fix = True
        if mirror_fix:
            last *= 2
        if attack.hits > last:
            reason = "封包伤害次数 : " + last + " 封包伤害次数: " + attack.skill
        return reason

    def Damage_MobCount(self, player: Any, effect: Any, attack: Any) -> str:
        reason = "None"
        if attack.targets > effect.getMobCount():
            reason = "打怪数量过多， 封包数量: " + attack.targets + " 正确数量:" + effect.getMobCount()
        return reason

    def maxDamage(self, chr: Any, ret: Any, damage: int) -> int:
        VipCount = chr.getVip()
        maxdamage = 199999 + VipCount * 10000
        randomNum = Randomizer.nextInt(20) + 80
        tempDamage = 0
        for item in chr.getInventory(MapleInventoryType.EQUIPPED):
            ak = 0
            if item is not None and isinstance(item, Equip):
                ak = MapleItemInformationProvider.getInstance().getTotalStat(item)
            tempDamage += ak * 10
        if ret.skill != 14101006 and damage >= 199999:
            tempDamage += (chr.getStat().getInt() + chr.getStat().getStr() + chr.getStat().getDex() + chr.getStat().getLuk()) * 5
            damage = (tempDamage + 199999) * randomNum / 100
            if damage < 199999:
                damage = 199999
            damage = min(damage, 199999 + VipCount * 10000)
            chr.getClient().getSession().write(MaplePacketCreator.sendHint("#e[破攻伤害P]:#r" + damage + "#b ", 250, 5))
        if damage > maxdamage:
            damage = maxdamage
        tempDamage = 0
        return damage

    def calcMonsterDecreaseDamage(self, damage: int, monster: Any, chr: Any, show: bool) -> int:
        jianshang = False
        if monster is not None:
            # switch (monster.getId()):
                # case 9700002:
                    damage *= 1
                    jianshang = True
                    break
                # case 9700001:
                    damage *= 1
                    jianshang = True
                    break
                # case 9700006:
                    damage *= 1
                    jianshang = True
                    break
                # case 9700011:
                    damage *= 1
                    jianshang = True
                    break
                # case 8520000:
                    damage *= 1
                    jianshang = True
                    break
                # case 8510000:
                    damage *= 1
                    jianshang = True
                    break
                # case 9400593:
                    damage *= 1
                    jianshang = True
                    break
                # case 9400592:
                    damage *= 1
                    jianshang = True
                    break
                # case 9400591:
                    damage *= 1
                    jianshang = True
                    break
                # case 9400590:
                    damage *= 1
                    jianshang = True
                    break
                # case 9400589:
                    damage *= 1
                    jianshang = True
                    break
                # case 8500002:
                    damage *= 1
                    jianshang = True
                    break
                # case 9420522:
                    damage *= 1
                    jianshang = True
                    break
                # case 9420544:
                    damage *= 1
                    jianshang = True
                    break
                # case 9420549:
                    damage *= 1
                    jianshang = True
                    break
                # case 8810006:
                    damage *= 1
                    jianshang = True
                    break
                # case 8810001:
                    damage *= 1
                    jianshang = True
                    break
                # case 8810000:
                    damage *= 1
                    jianshang = True
                    break
                # case 8810005:
                    damage *= 0.3
                    jianshang = True
                    break
                # case 8800000:
                    damage *= 1
                    jianshang = True
                    break
                # case 8800001:
                    damage *= 1
                    jianshang = True
                    break
                # case 8800002:
                    damage *= 1
                    jianshang = True
                    break
                # case 8820001:
                    damage *= 1
                    jianshang = True
                    break
                # case 9600025:
                    damage *= 1
                    jianshang = True
                    break
                # case 9500363:
                    damage *= 1
                    jianshang = True
                    break
                # case 9300215:
                    damage *= 1
                    jianshang = True
                    break
        if (not jianshang or show) {}
        return damage

