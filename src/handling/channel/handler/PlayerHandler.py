"""
PlayerHandler - Converted from Java source
Original: handling/channel/handler/PlayerHandler.java
Package: handling.channel.handler
"""

from socket import socket
from typing import List
from typing import Optional, Any
from weakref import ref
import math
import threading
import time
import weakref

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.SkillMacro import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.MapConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.AutobanManager import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.events.MapleSnowball import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MobAttackInfo import *  # TODO: import specific classes
# from server.life.MobAttackInfoFactory import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes
# from server.maps.AnimatedMapleMapObject import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.LittleEndianAccessor import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes


class PlayerHandler:
    """
    Class PlayerHandler
    """


    def isFinisher(self, skillid: int) -> bool:
        # switch (skillid):
            # case 1111003:
            # case 1111004:
            # case 1111005:
            # case 1111006:
            # case 11111002:
            # case 11111003:
                return True
            # default:
                return False

    def ChangeMonsterBookCover(self, bookid: int, c: Any, chr: Any) -> None:
        if bookid == 0 || GameConstants.isMonsterCard(bookid):
            chr.setMonsterBookCover(bookid)
            chr.getMonsterBook().updateCard(c, bookid)

    def ChangeSkillMacro(self, slea: Any, chr: Any) -> None:
        num = slea.readByte(), i = 0
        while i < num:
            name = slea.readMapleAsciiString()
            shout = slea.readByte()
            skill1 = slea.readInt()
            skill2 = slea.readInt()
            skill3 = slea.readInt()
            macro = SkillMacro(skill1, skill2, skill3, name, shout, i)
            chr.updateMacros(i, macro)

    def ChangeKeymap(self, slea: Any, chr: Any) -> None:
        if slea.available() > 8 && chr is not None:
            chr.updateTick(slea.readInt())
            numChanges = slea.readInt(), i = 0
            while i < numChanges:
                chr.changeKeybinding(slea.readInt(), slea.readByte(), slea.readInt())
        elif chr is not None:
            type = slea.readInt()
            data = slea.readInt()
            # switch (type):
                # case 1:
                    if data <= 0:
                        chr.getQuestRemove(MapleQuest.getInstance(122221))
                        break
                    chr.getQuestNAdd(MapleQuest.getInstance(122221)).setCustomData(str(data))
                    break
                # case 2:
                    if data <= 0:
                        chr.getQuestRemove(MapleQuest.getInstance(122222))
                        break
                    chr.getQuestNAdd(MapleQuest.getInstance(122222)).setCustomData(str(data))
                    break
                # case 3:
                    if data <= 0:
                        chr.getQuestRemove(MapleQuest.getInstance(122224))
                        break
                    chr.getQuestNAdd(MapleQuest.getInstance(122224)).setCustomData(str(data))
                    break

    def UseChair(self, itemId: int, c: Any, chr: Any) -> None:
        if chr is None || chr.getMap() is None:
            return
        toUse = chr.getInventory(MapleInventoryType.SETUP).findById(itemId)
        if toUse is None:
            chr.getCheatTracker().registerOffense(CheatingOffense.使用不存在道具, Integer.toString(itemId))
            return
        if itemId == 3011000:
            haz = False
            for item in c.getPlayer().getInventory(MapleInventoryType.CASH).list():
                if item.getItemId() == 5340000:
                    haz = True
                else:
                    if item.getItemId() == 5340001:
                        haz = False
                        if chr.isGM():
                            chr.dropTopMsg("GM钓鱼，使用高级钓竿,每5秒一次。开始钓鱼")
                            chr.dropMessage(6, "GM钓鱼，使用高级钓竿,每5秒一次。开始钓鱼")
                        else:
                            chr.dropTopMsg("使用高级钓竿，每5秒一次。开始钓鱼")
                        chr.startFishingTask(True)
                        break
                    continue
            if haz:
                if chr.isGM():
                    chr.dropTopMsg("GM钓鱼，使用普通钓竿,每5秒一次。开始钓鱼")
                    chr.dropMessage(6, "GM钓鱼，使用普通钓竿,每5秒一次。开始钓鱼")
                else:
                    chr.dropTopMsg("使用普通钓竿，每5秒一次。开始钓鱼")
                chr.startFishingTask(False)
        chr.setChair(itemId)
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.showChair(chr.getId(), itemId), False)
        c.getSession().write(MaplePacketCreator.enableActions())

    def CancelChair(self, id: int, c: Any, chr: Any) -> None:
        if id == -1:
            if chr.getChair() == 3011000:
                chr.cancelFishingTask()
            chr.setChair(0)
            c.getSession().write(MaplePacketCreator.cancelChair(-1))
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.showChair(chr.getId(), 0), False)
        else:
            chr.setChair(id)
            c.getSession().write(MaplePacketCreator.cancelChair(id))

    def TrockAddMap(self, slea: Any, c: Any, chr: Any) -> None:
        addrem = slea.readByte()
        vip = slea.readByte()
        if vip == 1:
            if addrem == 0:
                chr.deleteFromRocks(slea.readInt())
            elif addrem == 1:
                if !FieldLimitType.VipRock.check(chr.getMap().getFieldLimit()):
                    chr.addRockMap()
                else:
                    chr.dropMessage(1, "你可能不能添加此地图.")
        elif addrem == 0:
            chr.deleteFromRegRocks(slea.readInt())
        elif addrem == 1:
            if !FieldLimitType.VipRock.check(chr.getMap().getFieldLimit()):
                chr.addRegRockMap()
            else:
                chr.dropMessage(1, "你可能不能添加此地图.")
        c.getSession().write(MTSCSPacket.getTrockRefresh(chr, vip == 1, addrem == 3))

    def CharInfoRequest(self, objectid: int, c: Any, chr: Any) -> None:
        if c.getPlayer() is None || c.getPlayer().getMap() is None:
            return
        player = c.getPlayer().getMap().getCharacterById(objectid)
        c.getSession().write(MaplePacketCreator.enableActions())
        if player is not None && !player.isClone() && (!player.isGM() || c.getPlayer().isGM()):
            c.getSession().write(MaplePacketCreator.charInfo(player, c.getPlayer().getId() == objectid))

    def resetAllBossLog(self, chr: Any) -> None:
        chr.resetBossLog("狮熊Boss")
        chr.resetBossLog("普通黑龙")
        chr.resetBossLog("树精Boss")
        chr.resetBossLog("普通扎昆")

    def TakeDamage(self, slea: Any, c: Any, chr: Any) -> None:
        chr.updateTick(slea.readInt())
        type = slea.readByte()
        slea.skip(1)
        damage = slea.readInt()
        oid = 0
        monsteridfrom = 0
        reflect = 0
        direction = 0
        pos_x = 0
        pos_y = 0
        fake = 0
        mpattack = 0
        is_pg = False
        isDeadlyAttack = False
        attacker = None
        if chr.isHidden() || chr.getMap() is None:
            return
        if chr.isGM() && chr.isInvincible():
            return
        stats = chr.getStat()
        if type != -2 && type != -3 && type != -4:
            monsteridfrom = slea.readInt()
            oid = slea.readInt()
            attacker = chr.getMap().getMonsterByOid(oid)
            direction = slea.readByte()
            if attacker is None:
                return
            if type != -1:
                attackInfo = MobAttackInfoFactory.getInstance().getMobAttackInfo(attacker, type)
                if attackInfo is not None:
                    if attackInfo.isDeadlyAttack():
                        isDeadlyAttack = True
                        mpattack = stats.getMp() - 1
                    else:
                        mpattack += attackInfo.getMpBurn()
                    skill = MobSkillFactory.getMobSkill(attackInfo.getDiseaseSkill(), attackInfo.getDiseaseLevel())
                    if skill is not None && (damage == -1 || damage > 0):
                        skill.applyEffect(chr, attacker, False)
                    attacker.setMp(attacker.getMp() - attackInfo.getMpCon())
        if damage == -1:
            fake = 4020002 + (chr.getJob() / 10 - 40) * 100000
        elif damage < -1 || damage > 60000:
            AutobanManager.getInstance().addPoints(c, 1000, 60000, "Taking abnormal amounts of damge from " + monsteridfrom + ": " + damage)
            return
        chr.getCheatTracker().checkTakeDamage(damage)
        if damage > 0:
            chr.getCheatTracker().setAttacksWithoutHit(False)
            if chr.getBuffedValue(MapleBuffStat.变身) is not None:
                chr.cancelMorphs()
            if slea.available() == 3:
                level = slea.readByte()
                if level > 0:
                    skill = MobSkillFactory.getMobSkill(slea.readShort(), level)
                    if skill is not None:
                        skill.applyEffect(chr, attacker, False)
            if type != -2 && type != -3 && type != -4:
                bouncedam_ = ((Randomizer.nextInt(100) < chr.getStat().DAMreflect_rate) ? chr.getStat().DAMreflect : 0) + ((type == -1 && chr.getBuffedValue(MapleBuffStat.伤害反击) is not None) ? chr.getBuffedValue(MapleBuffStat.伤害反击) : 0) + ((type == -1 && chr.getBuffedValue(MapleBuffStat.PERFECT_ARMOR) is not None) ? chr.getBuffedValue(MapleBuffStat.PERFECT_ARMOR) : 0)
                if bouncedam_ > 0 && attacker is not None:
                    bouncedamage = damage * bouncedam_ / 100
                    bouncedamage = min(bouncedamage, attacker.getMobMaxHp() / 10)
                    attacker.damage(chr, bouncedamage, True)
                    damage -= bouncedamage
                    chr.getMap().broadcastMessage(chr, MobPacket.damageMonster(oid, bouncedamage), chr.getPosition())
                    is_pg = True
            if type != -1 && type != -2 && type != -3 && type != -4:
                # switch (chr.getJob()):
                    # case 112:
                        skill2 = SkillFactory.getSkill(1120004)
                        if chr.getSkillLevel(skill2) > 0:
                            damage *= (int)(skill2.getEffect(chr.getSkillLevel(skill2)).getX() / 1000.0)
                            break
                        break
                    # case 122:
                        skill2 = SkillFactory.getSkill(1220005)
                        if chr.getSkillLevel(skill2) > 0:
                            damage *= (int)(skill2.getEffect(chr.getSkillLevel(skill2)).getX() / 1000.0)
                            break
                        break
                    # case 132:
                        skill2 = SkillFactory.getSkill(1320005)
                        if chr.getSkillLevel(skill2) > 0:
                            damage *= (int)(skill2.getEffect(chr.getSkillLevel(skill2)).getX() / 1000.0)
                            break
                        break
            if damage == -1:
                pguard = chr.getBuffedValue(MapleBuffStat.战神抗压)
                if pguard is not None:
                    attacker = chr.getMap().getMapObject(oid, None)
                    if attacker is not None:
                        反击伤害 = (int)(damage * (pguard / 100.0))
                        反击伤害 = min(反击伤害, attacker.getMobMaxHp() / 10)
                        attacker.damage(chr, damage, True)
                        damage -= 反击伤害
                        chr.getMap().broadcastMessage(chr, MobPacket.damageMonster(oid, damage), chr.getPosition())
                        chr.checkMonsterAggro(attacker)
                        c.getPlayer().setHp(c.getPlayer().getHp() - damage)
            zhanshenkangya = chr.getBuffedValue(MapleBuffStat.战神抗压)
            if zhanshenkangya is not None && damage > 0:
                attacker = chr.getMap().getMapObject(oid, MapleMapObjectType.MONSTER)
                if attacker is not None:
                    kangya = SkillFactory.getSkill(21101003)
                    kangyashanghai = (int)(kangya.getEffect(chr.getSkillLevel(21101003)).getDamage() / 100.0 * damage)
                    attacker.damage(chr, kangyashanghai, True)
                    damage -= kangyashanghai
                    chr.getMap().broadcastMessage(chr, MobPacket.damageMonster(oid, kangyashanghai), chr.getPosition())
                    chr.checkMonsterAggro(attacker)
                    c.getPlayer().setHp(c.getPlayer().getHp() - damage)
            bouncedam_A = chr.getStatForBuff(MapleBuffStat.战神抗压)
            if attacker is not None && bouncedam_A is not None && damage > 0:
                kangya2 = SkillFactory.getSkill(21101003)
                bouncedamage2 = (int)(kangya2.getEffect(chr.getSkillLevel(21101003)).getDamage() / 100.0 * damage)
                attacker.damage(chr, bouncedamage2, True)
                damage -= bouncedamage2
                chr.getMap().broadcastMessage(chr, MobPacket.damageMonster(oid, bouncedamage2), chr.getPosition())
                chr.checkMonsterAggro(attacker)
                chr.setHp(chr.getHp() - damage)
            magicShield = chr.getStatForBuff(MapleBuffStat.MAGIC_SHIELD)
            if magicShield is not None:
                damage -= (int)(magicShield.getX() / 100.0 * damage)
            blueAura = chr.getStatForBuff(MapleBuffStat.蓝色灵气)
            if blueAura is not None:
                damage -= (int)(blueAura.getY() / 100.0 * damage)
            if chr.getBuffedValue(MapleBuffStat.SATELLITESAFE_PROC) is not None && chr.getBuffedValue(MapleBuffStat.SATELLITESAFE_ABSORB) is not None:
                buff = chr.getBuffedValue(MapleBuffStat.SATELLITESAFE_PROC)
                buffz = chr.getBuffedValue(MapleBuffStat.SATELLITESAFE_ABSORB)
                if (int)(buff / 100.0 * chr.getStat().getMaxHp()) <= damage:
                    damage -= (int)(buffz / 100.0 * damage)
                    chr.cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
                    chr.cancelEffectFromBuffStat(MapleBuffStat.REAPER)
            if chr.getBuffedValue(MapleBuffStat.魔法盾) is not None:
                hploss = 0
                mploss = 0
                if isDeadlyAttack:
                    if stats.getHp() > 1:
                        hploss = stats.getHp() - 1
                    if stats.getMp() > 1:
                        mploss = stats.getMp() - 1
                    if chr.getBuffedValue(MapleBuffStat.终极无限) is not None:
                        mploss = 0
                    chr.addMPHP(-hploss, -mploss)
                else:
                    mploss = (int)(damage * (chr.getBuffedValue(MapleBuffStat.魔法盾) / 100.0)) + mpattack
                    hploss = damage - mploss
                    if chr.getBuffedValue(MapleBuffStat.终极无限) is not None:
                        mploss = 0
                    elif mploss > stats.getMp():
                        mploss = stats.getMp()
                        hploss = damage - mploss + mpattack
                    chr.addMPHP(-hploss, -mploss)
            elif chr.getBuffedValue(MapleBuffStat.金钱护盾) is not None:
                damage = ((damage % 2 == 0) ? (damage / 2) : (damage / 2 + 1))
                mesoloss = (int)(damage * (chr.getBuffedValue(MapleBuffStat.金钱护盾) / 100.0))
                if chr.getMeso() < mesoloss:
                    chr.gainMeso(-chr.getMeso(), False)
                    chr.cancelBuffStats(MapleBuffStat.金钱护盾)
                else:
                    chr.gainMeso(-mesoloss, False)
                if isDeadlyAttack && stats.getMp() > 1:
                    mpattack = stats.getMp() - 1
                chr.addMPHP(-damage, -mpattack)
            elif isDeadlyAttack:
                chr.addMPHP((stats.getHp() > 1) ? (-(stats.getHp() - 1)) : 0, (stats.getMp() > 1) ? (-(stats.getMp() - 1)) : 0)
            else:
                chr.addMPHP(-damage, -mpattack)
            chr.handleBattleshipHP(-damage)
        if !chr.isHidden():
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.damagePlayer(type, monsteridfrom, chr.getId(), damage, fake, direction, reflect, is_pg, oid, pos_x, pos_y), False)

    def AranCombo144(self, c: Any, chr: Any, toAdd: int) -> None:
        if chr is not None && chr.getJob() >= 2000 && chr.getJob() <= 2112:
            combo = chr.getCombo()
            curr = int(time.time() * 1000)
            if combo > 0 && curr - chr.getLastCombo() > 7000:
                combo = 0
            combo = min(30000, combo + toAdd)
            chr.setLastComboTime(curr)
            chr.setCombo(combo)
            c.getSession().write(MaplePacketCreator.testCombo(combo))
            # switch (combo):
                # case 10:
                # case 20:
                # case 30:
                # case 40:
                # case 50:
                # case 60:
                # case 70:
                # case 80:
                # case 90:
                # case 100:
                    if chr.getSkillLevel(21000000) < combo / 10:
                        break
                    SkillFactory.getSkill(21000000).getEffect(combo / 10).applyComboBuff(chr, combo)
                    break

    def AranCombo(self, c: Any, chr: Any) -> None:
        if chr is not None && chr.getJob() >= 2000 && chr.getJob() <= 2112:
            combo = chr.getCombo()
            curr = int(time.time() * 1000)
            if combo > 0 && curr - chr.getLastCombo() > 7000:
                combo = 0
                skill = SkillFactory.getSkill(21000000)
                if combo <= 1 && skill is not None:
                    SkillFactory.getSkill(21000000).getEffect(0).applyComboBuff(chr, 0)
            if combo < 30000:
                combo += 1
            # switch (combo):
                # case 10:
                # case 20:
                # case 30:
                # case 40:
                # case 50:
                # case 60:
                # case 70:
                # case 80:
                # case 90:
                # case 100:
                    if chr.getSkillLevel(21000000) >= combo / 10:
                        SkillFactory.getSkill(21000000).getEffect(combo / 10).applyComboBuff(chr, combo)
                        break
                    break
            chr.setCombo(combo)
            chr.setLastComboTime(curr)
            c.getSession().write(MaplePacketCreator.testCombo(combo))

    def UseItemEffect(self, itemId: int, c: Any, chr: Any) -> None:
        toUse = chr.getInventory(MapleInventoryType.CASH).findById(itemId)
        if toUse is None || toUse.getItemId() != itemId || toUse.getQuantity() < 1:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if itemId != 5510000:
            chr.setItemEffect(itemId)
        flag = toUse.getFlag()
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.itemEffects(chr.getId(), itemId), False)
        if ItemFlag.KARMA_EQ.check(flag):
            toUse.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
            c.getSession().write(MaplePacketCreator.getCharInfo(chr))
            chr.getMap().removePlayer(chr)
            chr.getMap().addPlayer(chr)
        elif ItemFlag.KARMA_USE.check(flag):
            toUse.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
            c.getSession().write(MaplePacketCreator.getCharInfo(chr))
            chr.getMap().removePlayer(chr)
            chr.getMap().addPlayer(chr)

    def CancelItemEffect(self, id: int, chr: Any) -> None:
        chr.cancelEffect(MapleItemInformationProvider.getInstance().getItemEffect(-id), False, -1)

    def CancelBuffHandler(self, sourceid: int, chr: Any) -> None:
        if chr is None:
            return
        skill = SkillFactory.getSkill1(sourceid)
        if skill.isChargeSkill():
            chr.setKeyDownSkill_Time(0)
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.skillCancel(chr, sourceid), False)
        else:
            chr.cancelEffect(skill.getEffect(1), False, -1)
            chr.getStat().recalcLocalStats()

    def SkillEffect(self, slea: Any, chr: Any) -> None:
        skillId = slea.readInt()
        level = slea.readByte()
        flags = slea.readByte()
        speed = slea.readByte()
        unk = slea.readByte()
        skill = SkillFactory.getSkill(skillId)
        if chr is None:
            return
        skilllevel_serv = chr.getSkillLevel(skill)
        if skilllevel_serv > 0 && skilllevel_serv == level && skill.isChargeSkill():
            chr.setKeyDownSkill_Time(int(time.time() * 1000))
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.skillEffect(chr, skillId, level, flags, speed, unk), False)

    def SpecialMove(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || !chr.isAlive() || chr.getMap() is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        slea.skip(4)
        skillid = slea.readInt()
        skillLevel = slea.readByte()
        skill = SkillFactory.getSkill(skillid)
        if chr.getSkillLevel(skill) <= 0 || chr.getSkillLevel(skill) != skillLevel:
            if !GameConstants.isMulungSkill(skillid) && !GameConstants.isPyramidSkill(skillid):
                return
            if GameConstants.isMulungSkill(skillid):
                if chr.getMapId() / 10000 != 92502:
                    return
                chr.mulung_EnergyModify(False)
            elif GameConstants.isPyramidSkill(skillid) && chr.getMapId() / 10000 != 92602:
                return
        effect = skill.getEffect(chr.getSkillLevel(GameConstants.getLinkedAranSkill(skillid)))
        if effect.getCooldown() > 0 && !chr.isGM():
            if chr.skillisCooling(skillid):
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            if skillid != 5221006:
                c.getSession().write(MaplePacketCreator.skillCooldown(skillid, effect.getCooldown()))
                chr.addCooldown(skillid, int(time.time() * 1000), effect.getCooldown() * 1000)
        chr.checkFollow()
        # switch (skillid):
            # case 1121001:
            # case 1221001:
            # case 1321001:
            # case 9001020:
                number_of_mobs = slea.readByte()
                slea.skip(3)
                for i in range(number_of_mobs):
                    mobId = slea.readInt()
                    mob = chr.getMap().getMonsterByOid(mobId)
                    if mob is not None:
                        mob.switchController(chr, mob.isControllerHasAggro())
                chr.getMap().broadcastMessage(chr, MaplePacketCreator.showBuffeffect(chr.getId(), skillid, 1, slea.readByte()), chr.getPosition())
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # default:
                pos = None
                if slea.available() == 7 || skill.getId() == 3111002 || skill.getId() == 3211002:
                    pos = slea.readPos()
                if effect.is时空门():
                    if !FieldLimitType.MysticDoor.check(chr.getMap().getFieldLimit()):
                        effect.applyTo(c.getPlayer(), pos)
                        break
                    c.getSession().write(MaplePacketCreator.enableActions())
                    break
                else:
                    mountid = MapleStatEffect.parseMountInfo(c.getPlayer(), skill.getId())
                    if mountid != 0 && mountid != GameConstants.getMountItem(skill.getId()) && !c.getPlayer().isGM() && c.getPlayer().getBuffedValue(MapleBuffStat.骑兽技能) is None && c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-118)) is None && !GameConstants.isMountItemAvailable(mountid, c.getPlayer().getJob()):
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    effect.applyTo(c.getPlayer(), pos)
                    break

    def closeRangeAttack(self, slea: Any, c: Any, chr: Any, energy: bool) -> None:
        if chr is None || (energy && chr.getBuffedValue(MapleBuffStat.能量获得) is None && chr.getBuffedValue(MapleBuffStat.战神抗压) is None && !GameConstants.isKOC(chr.getJob())):
            return
        if !chr.isAlive() || chr.getMap() is None:
            chr.getCheatTracker().registerOffense(CheatingOffense.人物死亡攻击)
            return
        隐身 = chr.getBuffedValue(MapleBuffStat.隐身术)
        attack = DamageParse.Modify_AttackCrit(DamageParse.parseDmgM(slea, chr), chr, 1)
        if 隐身 is not None:
            if attack.skill == 0:
                chr.cancelEffectFromBuffStat(MapleBuffStat.隐身术)
            if chr.getJob() == 1410 && attack.skill != 14100005 && attack.skill != 0:
                chr.dropMessage(5, "夜行者隐身状态除非使用驱逐技能。其他技能均无效！")
                return
            if (chr.getJob() != 400 || chr.getJob() != 410 || chr.getJob() != 411 || chr.getJob() != 412) && attack.skill != 4221001 && attack.skill != 4221007 && attack.skill != 0:
                chr.dropMessage(5, "隐身状态下除非使用刀飞的暗杀技能和一出双击技能。其他技能均无效！")
                return
        mirror = chr.getBuffedValue(MapleBuffStat.MIRROR_IMAGE) is not None
        maxdamage = chr.getStat().getCurrentMaxBaseDamage()
        attackCount = (chr.getJob() >= 430 && chr.getJob() <= 434) ? 2 : 1
        skillLevel = 0
        effect = None
        skill = None
        if attack.skill == 21100004 || attack.skill == 21100005 || attack.skill == 21110004 || attack.skill == 21120006 || attack.skill == 21120007:
            chr.setCombo(1)
        if attack.skill != 0:
            skill = SkillFactory.getSkill(GameConstants.getLinkedAranSkill(attack.skill))
            skillLevel = chr.getSkillLevel(skill)
            effect = attack.getAttackEffect(chr, skillLevel, skill)
            if effect is None:
                return
            maxdamage *= effect.getDamage() / 100.0
            attackCount = effect.getAttackCount()
            if effect.getCooldown() > 0 && !chr.isGM():
                if chr.skillisCooling(attack.skill):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                c.getSession().write(MaplePacketCreator.skillCooldown(attack.skill, effect.getCooldown()))
                chr.addCooldown(attack.skill, int(time.time() * 1000), effect.getCooldown() * 1000)
        attackCount *= (mirror ? 2 : 1)
        if !energy:
            if (chr.getMapId() == 109060000 || chr.getMapId() == 109060002 || chr.getMapId() == 109060004) && attack.skill == 0:
                MapleSnowball.MapleSnowballs.hitSnowball(chr)
            numFinisherOrbs = 0
            comboBuff = chr.getBuffedValue(MapleBuffStat.斗气集中)
            if isFinisher(attack.skill):
                if comboBuff is not None:
                    numFinisherOrbs = comboBuff - 1
                chr.handleOrbconsume()
            elif attack.targets > 0 && comboBuff is not None:
                # switch (chr.getJob()):
                    # case 111:
                    # case 112:
                    # case 1110:
                    # case 1111:
                        if attack.skill != 1111008:
                            chr.handleOrbgain()
                            break
                        break
            # switch (chr.getJob()):
                # case 511:
                # case 512:
                    chr.handleEnergyCharge(5110001, attack.targets * attack.hits)
                    break
                # case 1510:
                # case 1511:
                # case 1512:
                    chr.handleEnergyCharge(15100004, attack.targets * attack.hits)
                    break
            if numFinisherOrbs > 0:
                maxdamage *= numFinisherOrbs
            elif comboBuff is not None:
                combo = None
                if c.getPlayer().getJob() == 1110 || c.getPlayer().getJob() == 1111:
                    combo = SkillFactory.getSkill(11111001)
                else:
                    combo = SkillFactory.getSkill(1111002)
                if c.getPlayer().getSkillLevel(combo) > 0:
                    maxdamage *= 1.0 + (combo.getEffect(c.getPlayer().getSkillLevel(combo)).getDamage() / 100.0 - 1.0) * (comboBuff - 1)
            if isFinisher(attack.skill):
                if numFinisherOrbs == 0:
                    return
                maxdamage = 199999.0
        chr.checkFollow()
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.closeRangeAttack(chr.getId(), attack.tbyte, attack.skill, skillLevel, attack.display, attack.animation, attack.speed, attack.allDamage, energy, chr.getLevel(), chr.getStat().passive_mastery(), attack.unk, attack.charge), chr.getPosition())
        DamageParse.applyAttack(attack, skill, c.getPlayer(), attackCount, maxdamage, effect, mirror ? AttackType.NON_RANGED_WITH_MIRROR : AttackType.NON_RANGED)

    def rangedAttack(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        if !chr.isAlive() || chr.getMap() is None:
            chr.getCheatTracker().registerOffense(CheatingOffense.人物死亡攻击)
            return
        attack = DamageParse.Modify_AttackCrit(DamageParse.parseDmgR(slea, chr), chr, 2)
        bulletCount = 1
        skillLevel = 0
        effect = None
        skill = None
        if attack.skill != 0:
            skill = SkillFactory.getSkill(GameConstants.getLinkedAranSkill(attack.skill))
            skillLevel = chr.getSkillLevel(skill)
            effect = attack.getAttackEffect(chr, skillLevel, skill)
            if effect is None:
                return
            # switch (attack.skill):
                # case 14101006:
                # case 21110004:
                    bulletCount = effect.getAttackCount()
                    break
                # default:
                    bulletCount = effect.getBulletCount()
                    break
            if effect.getCooldown() > 0 && !chr.isGM():
                if chr.skillisCooling(attack.skill):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                c.getSession().write(MaplePacketCreator.skillCooldown(attack.skill, effect.getCooldown()))
                chr.addCooldown(attack.skill, int(time.time() * 1000), effect.getCooldown() * 1000)
        ShadowPartner = chr.getBuffedValue(MapleBuffStat.影分身)
        if ShadowPartner is not None:
            bulletCount *= 2
        projectile = 0
        visProjectile = 0
        if attack.AOE != 0 && chr.getBuffedValue(MapleBuffStat.无形箭弩) is None && attack.skill != 4111004:
            if chr.getInventory(MapleInventoryType.USE).getItem(attack.starSlot) is None:
                return
            projectile = chr.getInventory(MapleInventoryType.USE).getItem(attack.starSlot).getItemId()
            if attack.cashSlot > 0:
                if chr.getInventory(MapleInventoryType.CASH).getItem(attack.cashSlot) is None:
                    return
                visProjectile = chr.getInventory(MapleInventoryType.CASH).getItem(attack.cashSlot).getItemId()
            else:
                visProjectile = projectile
            if chr.getBuffedValue(MapleBuffStat.暗器伤人) is None:
                bulletConsume = bulletCount
                if effect is not None && effect.getBulletConsume() != 0:
                    bulletConsume = effect.getBulletConsume() * ((ShadowPartner is not None) ? 2 : 1)
                if !MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, projectile, bulletConsume, False, True):
                    chr.dropMessage(5, "您的箭/子弹/飞镖不足。")
                    return
        # switch (chr.getJob()):
            # case 511:
            # case 512:
                chr.handleEnergyCharge(5110001, attack.targets * attack.hits)
                break
            # case 1510:
            # case 1511:
            # case 1512:
                chr.handleEnergyCharge(15100004, attack.targets * attack.hits)
                break
        basedamage = 0.0
        projectileWatk = 0
        if projectile != 0:
            projectileWatk = MapleItemInformationProvider.getInstance().getWatkForProjectile(projectile)
        statst = chr.getStat()
        if effect is not None:
            money = effect.getMoneyCon()
            if money != 0:
                if money > chr.getMeso():
                    money = chr.getMeso()
                chr.gainMeso(-money, False)
        chr.checkFollow()
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.rangedAttack(chr.getId(), attack.tbyte, attack.skill, skillLevel, attack.display, attack.animation, attack.speed, visProjectile, attack.allDamage, attack.position, chr.getLevel(), chr.getStat().passive_mastery(), attack.unk), chr.getPosition())
        DamageParse.applyAttack(attack, skill, chr, bulletCount, basedamage, effect, (ShadowPartner is not None) ? AttackType.RANGED_WITH_SHADOWPARTNER : AttackType.RANGED)

    def MagicDamage(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        if !chr.isAlive() || chr.getMap() is None:
            chr.getCheatTracker().registerOffense(CheatingOffense.人物死亡攻击)
            return
        attack = DamageParse.Modify_AttackCrit(DamageParse.parseDmgMa(slea, chr), chr, 3)
        skill = SkillFactory.getSkill(GameConstants.getLinkedAranSkill(attack.skill))
        skillLevel = chr.getSkillLevel(skill)
        beforeMp = chr.getMp()
        effect = attack.getAttackEffect(chr, skillLevel, skill)
        if effect is None:
            return
        if effect.getCooldown() > 0 && !chr.isGM():
            if chr.skillisCooling(attack.skill):
                c.getSession().write(MaplePacketCreator.enableActions())
                return
            c.getSession().write(MaplePacketCreator.skillCooldown(attack.skill, effect.getCooldown()))
            chr.addCooldown(attack.skill, int(time.time() * 1000), effect.getCooldown() * 1000)
        chr.checkFollow()
        chr.getMap().broadcastMessage(chr, MaplePacketCreator.magicAttack(chr.getId(), attack.tbyte, attack.skill, skillLevel, attack.display, attack.animation, attack.speed, attack.allDamage, attack.charge, chr.getLevel(), attack.unk), chr.getPosition())
        DamageParse.applyAttackMagic(attack, skill, c.getPlayer(), effect)
        clones = chr.getClones()
        for i in range(len(clones)):
            if clones[i].get() is not None:
                clone = clones[i].get()
                skil2 = skill
                eff2 = effect
                skillLevel2 = skillLevel
                attack2 = DamageParse.DivideAttack(attack, chr.isGM() ? 1 : 4)
                Timer.CloneTimer.getInstance().schedule(Runnable()
                    public void run()
                        clone.getMap().broadcastMessage(MaplePacketCreator.magicAttack(clone.getId(), attack2.tbyte, attack2.skill, skillLevel2, attack2.display, attack2.animation, attack2.speed, attack2.allDamage, attack2.charge, clone.getLevel(), attack2.unk))
                        DamageParse.applyAttackMagic(attack2, skil2, chr, eff2)

    def run(self) -> None:
        clone.getMap().broadcastMessage(MaplePacketCreator.magicAttack(clone.getId(), attack2.tbyte, attack2.skill, skillLevel2, attack2.display, attack2.animation, attack2.speed, attack2.allDamage, attack2.charge, clone.getLevel(), attack2.unk))
        DamageParse.applyAttackMagic(attack2, skil2, chr, eff2)

    def DropMeso(self, meso: int, chr: Any) -> None:
        if !chr.isAlive() || meso < 10 || meso > 50000 || meso > chr.getMeso():
            chr.getClient().getSession().write(MaplePacketCreator.enableActions())
            return
        chr.gainMeso(-meso, False, True)
        chr.getMap().spawnMesoDrop(meso, chr.getPosition(), chr, chr, True, 0)
        chr.getCheatTracker().checkDrop(True)

    def ChangeEmotion(self, emote: int, chr: Any) -> None:
        if emote > 7:
            emoteid = 5159992 + emote
            type = GameConstants.getInventoryType(emoteid)
            if chr.getInventory(type).findById(emoteid) is None:
                chr.getCheatTracker().registerOffense(CheatingOffense.使用不存在道具, Integer.toString(emoteid))
                return
        if emote > 0 && chr is not None && chr.getMap() is not None:
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.facialExpression(chr, emote), False)
            clones = chr.getClones()
            for i in range(len(clones)):
                if clones[i].get() is not None:
                    clone = clones[i].get()
                    Timer.CloneTimer.getInstance().schedule(Runnable()
                        public void run()
                            clone.getMap().broadcastMessage(MaplePacketCreator.facialExpression(clone, emote))

    def Heal(self, slea: Any, chr: Any) -> None:
        if chr is None:
            return
        chr.updateTick(slea.readInt())
        healHP = slea.readShort()
        healMP = slea.readShort()
        stats = chr.getStat()
        check_hp = stats.getHealHP()
        check_mp = stats.getHealMP()
        if stats.getHp() <= 0:
            return
        if chr.canHP() && healHP != 0:
            if chr.getChair() != 0:
                check_hp += 150
            if healHP > check_hp * 2 && healHP > 20:
                chr.getCheatTracker().registerOffense(CheatingOffense.回复过多HP, str(healHP) + " 服务器:" + check_hp)
            chr.addHP(healHP)
        if chr.canMP() && healMP != 0:
            if healMP > check_mp * 2 && healMP > 20:
                chr.getCheatTracker().registerOffense(CheatingOffense.回复过多MP, str(healMP) + "服务器:" + check_mp)
            chr.addMP(healMP)

    def MovePlayer(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        Original_Pos = chr.getPosition()
        slea.skip(33)
        res = None
        try:
            res = MovementParse.parseMovement(slea, 1)
        except IndexError as e:
            print("AIOBE Type1:\n")
            # System.out.println("AIOBE Type1:\n" + slea.toString(true));
            return
        if res is not None && c.getPlayer().getMap() is not None:
            if slea.available() < 13 || slea.available() > 26:
                # System.out.println("slea.available != 13-26 (movement parsing error)\n" + slea.toString(true));
                print("slea.available != 13-26 (movement parsing error)\n")
                return
            res2 = []
            map = c.getPlayer().getMap()
            if chr.isHidden():
                chr.setLastRes(res2)
                c.getPlayer().getMap().broadcastGMMessage(chr, MaplePacketCreator.movePlayer(chr.getId(), res, Original_Pos), False)
            else:
                c.getPlayer().getMap().broadcastMessage(c.getPlayer(), MaplePacketCreator.movePlayer(chr.getId(), res, Original_Pos), False)
            MovementParse.updatePosition(res, chr, 0)
            pos = chr.getPosition()
            map.movePlayer(chr, pos)
            if chr.getFollowId() > 0 && chr.isFollowOn() && chr.isFollowInitiator():
                fol = map.getCharacterById(chr.getFollowId())
                if fol is not None:
                    original_pos = fol.getPosition()
                    MovementParse.updatePosition(res, fol, 0)
                    map.broadcastMessage(fol, MaplePacketCreator.movePlayer(fol.getId(), res, original_pos), False)
                else:
                    chr.checkFollow()
            clones = chr.getClones()
            for i in range(len(clones)):
                if clones[i].get() is not None:
                    clone = clones[i].get()
                    res3 = []
                    Timer.CloneTimer.getInstance().schedule(Runnable()
                        public void run()
                            try:
                                if clone.getMap() == map:
                                    if clone.isHidden():
                                        clone.setLastRes(res3)
                                    else:
                                        map.broadcastMessage(clone, MaplePacketCreator.movePlayer(clone.getId(), res3, Original_Pos), False)
                                    MovementParse.updatePosition(res3, clone, 0)
                                    map.movePlayer(clone, pos)
                            catch (Exception ex) {}
            count = c.getPlayer().getFallCounter()
            if map.getFootholds().findBelow(c.getPlayer().getPosition()) is None && c.getPlayer().getPosition().y > c.getPlayer().getOldPosition().y && c.getPlayer().getPosition().x == c.getPlayer().getOldPosition().x:
                if count > 10:
                    c.getPlayer().changeMap(map, map.getPortal(0))
                    c.getPlayer().setFallCounter(0)
                else:
                    c.getPlayer().setFallCounter(++count)
            elif count > 0:
                c.getPlayer().setFallCounter(0)
            c.getPlayer().setOldPosition(Point(c.getPlayer().getPosition()))

    def UpdateHandler(self, slea: Any, c: Any, chr: Any) -> None:
        chr.saveToDB(False, False)

    def ChangeMapSpecial(self, slea: Any, c: Any, chr: Any) -> None:
        slea.skip(1)
        portal_name = slea.readMapleAsciiString()
        portal = chr.getMap().getPortal(portal_name)
        slea.skip(2)
        if portal is not None:
            portal.enterPortal(c)
        else:
            c.getSession().write(MaplePacketCreator.enableActions())

    def ChangeMap(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || chr.getMap() is None:
            NPCScriptManager.getInstance().dispose(c)
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        startTime = int(time.time() * 1000)
        if slea.available() != 0:
            slea.readByte()
            targetid = slea.readInt()
            if targetid == 0:
                targetid = 1000000
            portal = chr.getMap().getPortal(slea.readMapleAsciiString())
            wheel = slea.readShort() > 0 && !MapConstants.isEventMap(chr.getMapId()) && chr.haveItem(5510000, 1, False, True)
            if targetid != -1 && !chr.isAlive():
                chr.setStance(0)
                if chr.getEventInstance() is not None && chr.getEventInstance().revivePlayer(chr) && chr.isAlive():
                    return
                if chr.getPyramidSubway() is not None:
                    chr.getStat().setHp(50)
                    chr.getPyramidSubway().fail(chr)
                    return
                if !wheel:
                    chr.getStat().setHp(50)
                    to = chr.getMap().getReturnMap()
                    resetAllBossLog(chr)
                    chr.changeMap(to, to.getPortal(0))
                else:
                    c.getSession().write(MTSCSPacket.useWheel((byte)(chr.getInventory(MapleInventoryType.CASH).countById(5510000) - 1)))
                    chr.getStat().setHp(chr.getStat().getMaxHp() / 100 * 40)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, 5510000, 1, True, False)
                    to = chr.getMap()
                    chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && chr.isGM():
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && !chr.isGM():
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                if c.getPlayer().isGM() || (chr.getMapId() == 0 && to.getId() == 10000) || (chr.getMapId() == 2010000 && to.getId() == 104000000) || (chr.getMapId() == 1020100 && to.getId() == 1020000) || (chr.getMapId() == 1020200 && to.getId() == 1020000) || (chr.getMapId() == 1020300 && to.getId() == 1020000) || (chr.getMapId() == 1020400 && to.getId() == 1020000) || (chr.getMapId() == 1020500 && to.getId() == 1020000) || (chr.getMapId() == 914090010 && to.getId() == 914090011) || (chr.getMapId() == 914090011 && to.getId() == 914090012) || (chr.getMapId() == 914090012 && to.getId() == 914090013) || (chr.getMapId() == 914090013 && to.getId() == 140090000) || (chr.getMapId() == 914090100 && to.getId() == 140000000):
                    pto = to.getPortal(0)
                    chr.changeMap(to, pto)
                else:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    print("[服务端]玩家[" + c.getPlayer().getName() + "]试图以非法形式切换地图！")
            elif portal is not None:
                portal.enterPortal(c)
            else:
                c.getSession().write(MaplePacketCreator.enableActions())

    def ChangeMap33(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None || chr.getMap() is None:
            NPCScriptManager.getInstance().dispose(c)
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if slea.available() == 0:
            socket = c.getChannelServer().getIP().split(":")
            chr.saveToDB(False, False)
            c.getChannelServer().removePlayer(c.getPlayer())
            c.updateLoginState(MapleClient.LOGIN_SERVER_TRANSITION)
            try:
                c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(socket[1])))
            except Exception as e:
                raise RuntimeError(e)
            return
        if slea.available() != 0:
            slea.readByte()
            targetid = slea.readInt()
            if targetid == 0:
                targetid = 1000000
            startwp = slea.readMapleAsciiString()
            portal = c.getPlayer().getMap().getPortal(startwp)
            wheel = slea.readShort() > 0 && !MapConstants.isEventMap(chr.getMapId()) && chr.haveItem(5510000, 1, False, True)
            if targetid != -1 && !chr.isAlive():
                chr.setStance(0)
                if chr.getEventInstance() is not None && chr.getEventInstance().revivePlayer(chr) && chr.isAlive():
                    return
                if chr.getPyramidSubway() is not None:
                    chr.getStat().setHp(50)
                    chr.getPyramidSubway().fail(chr)
                    return
                if !wheel:
                    chr.getStat().setHp(50)
                    to = chr.getMap().getReturnMap()
                    resetAllBossLog(chr)
                    chr.changeMap(to, to.getPortal(0))
                else:
                    c.getSession().write(MTSCSPacket.useWheel(chr.getInventory(MapleInventoryType.CASH).countById(5510000) - 1))
                    chr.getStat().setHp(chr.getStat().getMaxHp() / 100 * 40)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, 5510000, 1, True, False)
                    to = chr.getMap()
                    chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && chr.isGM():
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && !chr.isGM():
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                if c.getPlayer().isGM() || (chr.getMapId() == 0 && to.getId() == 10000) || (chr.getMapId() == 2010000 && to.getId() == 104000000) || (chr.getMapId() == 1020100 && to.getId() == 1020000) || (chr.getMapId() == 1020200 && to.getId() == 1020000) || (chr.getMapId() == 1020300 && to.getId() == 1020000) || (chr.getMapId() == 1020400 && to.getId() == 1020000) || (chr.getMapId() == 1020500 && to.getId() == 1020000) || (chr.getMapId() == 914090010 && to.getId() == 914090011) || (chr.getMapId() == 914090011 && to.getId() == 914090012) || (chr.getMapId() == 914090012 && to.getId() == 914090013) || (chr.getMapId() == 914090013 && to.getId() == 140090000) || (chr.getMapId() == 914090100 && to.getId() == 140000000):
                    pto = to.getPortal(0)
                    chr.changeMap(to, pto)
                else:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    print("[服务端]玩家[" + c.getPlayer().getName() + "]试图以非法形式切换地图！")
            elif portal is not None:
                portal.enterPortal(c)
            else:
                c.getSession().write(MaplePacketCreator.enableActions())

    def ChangeMap20(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            chr.dropMessage(5, "你現在不能攻擊或不能跟npc對話,請在對話框打 @解卡/@ea 來解除異常狀態")
            return
        if slea.available() == 0:
            socket = c.getChannelServer().getIP().split(":")
            chr.saveToDB(False, False)
            c.getChannelServer().removePlayer(c.getPlayer())
            c.updateLoginState(MapleClient.LOGIN_SERVER_TRANSITION)
            try:
                c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(socket[1])))
            except Exception as e:
                raise RuntimeError(e)
            return
        if slea.available() != 0:
            slea.readByte()
            targetid = slea.readInt()
            if targetid == 0:
                targetid = 1000000
            portal = chr.getMap().getPortal(slea.readMapleAsciiString())
            wheel = slea.readShort() > 0 && !MapConstants.isEventMap(chr.getMapId()) && chr.haveItem(5510000, 1, False, True)
            if targetid != -1 && !chr.isAlive():
                chr.setStance(0)
                if chr.getEventInstance() is not None && chr.getEventInstance().revivePlayer(chr) && chr.isAlive():
                    return
                if chr.getPyramidSubway() is not None:
                    chr.getStat().setHp(50)
                    chr.getPyramidSubway().fail(chr)
                    return
                if !wheel:
                    chr.getStat().setHp(50)
                    to = chr.getMap().getReturnMap()
                    resetAllBossLog(chr)
                    chr.changeMap(to, to.getPortal(0))
                else:
                    c.getSession().write(MTSCSPacket.useWheel((byte)(chr.getInventory(MapleInventoryType.CASH).countById(5510000) - 1)))
                    chr.getStat().setHp(chr.getStat().getMaxHp() / 100 * 40)
                    MapleInventoryManipulator.removeById(c, MapleInventoryType.CASH, 5510000, 1, True, False)
                    to = chr.getMap()
                    chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && chr.isGM():
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                chr.changeMap(to, to.getPortal(0))
            elif targetid != -1 && !chr.isGM():
                divi = chr.getMapId() / 100
                if divi == 9130401:
                    if targetid == 130000000 || targetid / 100 == 9130401:
                        to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                        chr.changeMap(to2, to2.getPortal(0))
                elif divi == 9140900:
                    if targetid == 914090011 || targetid == 914090012 || targetid == 914090013 || targetid == 140090000:
                        to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                        chr.changeMap(to2, to2.getPortal(0))
                elif divi == 9140901 && targetid == 140000000:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif divi == 9140902 && (targetid == 140030000 || targetid == 140000000):
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif divi == 9000900 && targetid / 100 == 9000900 && targetid > chr.getMapId():
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif divi / 1000 == 9000 && targetid / 100000 == 9000:
                    if targetid < 900090000 || targetid > 900090004:
                        c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif divi / 10 == 1020 && targetid == 1020000:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif chr.getMapId() == 900090101 && targetid == 100030100:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif chr.getMapId() == 2010000 && targetid == 104000000:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
                elif chr.getMapId() == 106020001 || chr.getMapId() == 106020502:
                    if targetid == chr.getMapId() - 1:
                        c.getSession().write(MaplePacketCreator.enableActions())
                        to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                        chr.changeMap(to2, to2.getPortal(0))
                elif chr.getMapId() == 0 && targetid == 10000:
                    c.getSession().write(MaplePacketCreator.enableActions())
                    to2 = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(targetid)
                    chr.changeMap(to2, to2.getPortal(0))
            elif portal is not None:
                portal.enterPortal(c)
            else:
                c.getSession().write(MaplePacketCreator.enableActions())

    def InnerPortal(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        portal = chr.getMap().getPortal(slea.readMapleAsciiString())
        Original_Pos = chr.getPosition()
        toX = slea.readShort()
        toY = slea.readShort()
        if portal is None:
            return
        if portal.getPosition().distanceSq(chr.getPosition()) > 22500.0:
            chr.getCheatTracker().registerOffense(CheatingOffense.使用过远传送点)
        chr.getMap().movePlayer(chr, Point(toX, toY))
        chr.checkFollow()

    def snowBall(self, slea: Any, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.enableActions())

    def leftKnockBack(self, slea: Any, c: Any) -> None:
        if c.getPlayer().getMapId() / 10000 == 10906:
            c.getSession().write(MaplePacketCreator.leftKnockBack())
            c.getSession().write(MaplePacketCreator.enableActions())

    def Rabbit(self, slea: Any, c: Any) -> None:
        arrackfrom = slea.readInt()
        damage = slea.readInt() + 100
        attackto = slea.readInt()
        mob = c.getPlayer().getMap().getMonsterByOid(attackto)
        if mob is not None && mob.getHp() > 0:
            mob.damage(c.getPlayer(), damage, True)

