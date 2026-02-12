"""
MobPacket - Converted from Java source
Original: tools/packet/MobPacket.java
Package: tools.packet
"""

from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any

# Internal module imports
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class MobPacket:
    """
    Class MobPacket
    """


    def damageMonster(self, oid: int, damage: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("damageMonster--------------------")
        mplew.writeShort(SendPacketOpcode.DAMAGE_MONSTER.getValue())
        mplew.writeInt(oid)
        mplew.write(0)
        if damage > 2147483647:
            mplew.writeInt(Integer.MAX_VALUE)
        else:
            mplew.writeInt(damage)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def damageFriendlyMob(self, mob: Any, damage: int, display: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("damageFriendlyMob--------------------")
        mplew.writeShort(SendPacketOpcode.DAMAGE_MONSTER.getValue())
        mplew.writeInt(mob.getObjectId())
        mplew.write(display ? 1 : 2)
        mplew.writeInt((damage > 2147483647) ? Integer.MAX_VALUE : (damage))
        mplew.writeInt((mob.getHp() > 2147483647) ? ((int)(mob.getHp() / mob.getMobMaxHp() * 2.147483647E9)) : (mob.getHp()))
        mplew.writeInt((mob.getMobMaxHp() > 2147483647) ? Integer.MAX_VALUE : (mob.getMobMaxHp()))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def killMonster(self, oid: int, animation: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("killMonster--------------------")
        mplew.writeShort(SendPacketOpcode.KILL_MONSTER.getValue())
        mplew.writeInt(oid)
        mplew.write(animation)
        if animation == 4:
            mplew.writeInt(-1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def healMonster(self, oid: int, heal: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("healMonster--------------------")
        mplew.writeShort(SendPacketOpcode.DAMAGE_MONSTER.getValue())
        mplew.writeInt(oid)
        mplew.write(0)
        mplew.writeInt(-heal)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showMonsterHP(self, oid: int, remhppercentage: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showMonsterHP--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_MONSTER_HP.getValue())
        mplew.writeInt(oid)
        mplew.write(remhppercentage)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBossHP(self, mob: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBossHPA--------------------")
        mplew.writeShort(SendPacketOpcode.BOSS_ENV.getValue())
        mplew.write(5)
        mplew.writeInt(mob.getId())
        if mob.getHp() > 2147483647:
            mplew.writeInt((int)(mob.getHp() / mob.getMobMaxHp() * 2.147483647E9))
        else:
            mplew.writeInt(mob.getHp())
        if mob.getMobMaxHp() > 2147483647:
            mplew.writeInt(Integer.MAX_VALUE)
        else:
            mplew.writeInt(mob.getMobMaxHp())
        mplew.write(mob.getStats().getTagColor())
        mplew.write(mob.getStats().getTagBgColor())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showBossHP_monsterId_currentHp_maxHp(self, monsterId: int, currentHp: int, maxHp: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showBossHPB--------------------")
        mplew.writeShort(SendPacketOpcode.BOSS_ENV.getValue())
        mplew.write(5)
        mplew.writeInt(monsterId)
        if currentHp > 2147483647:
            mplew.writeInt((int)(currentHp / maxHp * 2.147483647E9))
        else:
            mplew.writeInt((int)((currentHp <= 0) ? -1 : currentHp))
        if maxHp > 2147483647:
            mplew.writeInt(Integer.MAX_VALUE)
        else:
            mplew.writeInt(maxHp)
        mplew.write(6)
        mplew.write(5)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveMonster(self, useskill: bool, skill: int, skill1: int, skill2: int, skill3: int, skill4: int, oid: int, startPos: Any, endPos: Any, moves: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveMonster--------------------")
        mplew.writeShort(SendPacketOpcode.MOVE_MONSTER.getValue())
        mplew.writeInt(oid)
        mplew.write(0)
        mplew.write(useskill ? 1 : 0)
        mplew.write(skill)
        mplew.write(skill1)
        mplew.write(skill2)
        mplew.write(skill3)
        mplew.write(skill4)
        mplew.writePos(startPos)
        serializeMovementList(mplew, moves)
        return mplew.getPacket()

    def serializeMovementList(self, lew: Any, moves: list) -> None:
        if ServerConstants.调试输出封包:
            print("serializeMovementList--------------------")
        lew.write(moves)
        for move in moves:
            move.serialize(lew)

    def spawnFakeMonster(self, life: Any, effect: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER_CONTROL.getValue())
        mplew.write(1)
        mplew.writeInt(life.getObjectId())
        mplew.write(1)
        mplew.writeInt(life.getId())
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeLong(0)
        mplew.writeInt(0)
        mplew.write(136)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.writeShort(life.getPosition().x)
        mplew.writeShort(life.getPosition().y)
        mplew.write(life.getStance())
        mplew.writeShort(life.getFh())
        mplew.writeShort(life.getFh())
        if effect > 0:
            mplew.write(effect)
            mplew.write(0)
            mplew.writeShort(0)
        mplew.writeShort(-2)
        mplew.writeInt(0)
        return mplew.getPacket()

    def spawnMonster(self, life: Any, newSpawn: bool) -> Any:
        return spawnMonsterInternal(life, False, newSpawn, False, 0, False)

    def spawnMonster_life_newSpawn_effect(self, life: Any, newSpawn: bool, effect: int) -> Any:
        return spawnMonsterInternal(life, False, newSpawn, False, effect, False)

    def addMonsterStatus(self, mplew: Any, life: Any) -> None:
        if ServerConstants.调试输出封包:
            print("addMonsterStatus--------------------")
        if life.getStati() <= 0:
            life.addEmpty()
        mplew.writeLong(getSpecialLongMask(life.getStati().keys()))
        mplew.writeLong(getLongMask_NoRef(life.getStati().keys()))
        ignore_imm = False
        for buff in life.getStati().values():
            if buff.getStati() == MonsterStatus.反射魔法伤害 or buff.getStati() == MonsterStatus.反射物理伤害:
                ignore_imm = True
                break
        for buff in life.getStati().values():
            if buff.getStati() != MonsterStatus.反射魔法伤害 and buff.getStati() != MonsterStatus.反射物理伤害:
                if ignore_imm:
                    if buff.getStati() == MonsterStatus.免疫魔法攻击:
                        continue
                    if buff.getStati() == MonsterStatus.免疫物理攻击:
                        continue
                mplew.writeShort(buff.getX().shortValue())
                if buff.getStati() == MonsterStatus.召唤怪物:
                    continue
                if buff.getMobSkill() is not None:
                    mplew.writeShort(buff.getMobSkill().getSkillId())
                    mplew.writeShort(buff.getMobSkill().getSkillLevel())
                elif buff.getSkill() > 0:
                    mplew.writeInt(buff.getSkill())
                mplew.writeShort(buff.getStati() == 0 ? 0 : 1)

    def controlMonster(self, life: Any, newSpawn: bool, aggro: bool) -> Any:
        return spawnMonsterInternal(life, True, newSpawn, aggro, 0, False)

    def spawnMonsterInternal(self, life: Any, requestController: bool, newSpawn: bool, aggro: bool, effect: int, makeInvis: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if makeInvis:
            mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER_CONTROL.getValue())
            mplew.write(0)
            mplew.writeInt(life.getObjectId())
            return mplew.getPacket()
        if requestController:
            mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER_CONTROL.getValue())
            if aggro:
                mplew.write(2)
            else:
                mplew.write(1)
        else:
            mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER.getValue())
        mplew.writeInt(life.getObjectId())
        mplew.write(1)
        mplew.writeInt(life.getId())
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeLong(0)
        mplew.writeInt(0)
        mplew.write(136)
        mplew.writeInt(0)
        mplew.writeShort(0)
        mplew.writeShort(life.getPosition().x)
        mplew.writeShort(life.getPosition().y)
        mplew.write(life.getStance())
        mplew.writeShort(0)
        mplew.writeShort(life.getFh())
        if effect > 0:
            mplew.write(effect)
            mplew.write(0)
            mplew.writeShort(0)
            if effect == 15:
                mplew.write(0)
        if newSpawn:
            mplew.write(-2)
        else:
            mplew.write(-1)
        mplew.write(life.getCarnivalTeam())
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def stopControllingMonster(self, oid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("stopControllingMonster--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER_CONTROL.getValue())
        mplew.write(0)
        mplew.writeInt(oid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def makeMonsterInvisible(self, life: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("makeMonsterInvisible--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER_CONTROL.getValue())
        mplew.write(0)
        mplew.writeInt(life.getObjectId())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def makeMonsterReal(self, life: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("makeMonsterReal--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_MONSTER.getValue())
        mplew.writeInt(life.getObjectId())
        mplew.write(1)
        mplew.writeInt(life.getId())
        addMonsterStatus(mplew, life)
        mplew.writeShort(life.getPosition().x)
        mplew.writeShort(life.getPosition().y)
        mplew.write(life.getStance())
        mplew.writeShort(0)
        mplew.writeShort(life.getFh())
        mplew.writeShort(-1)
        mplew.writeInt(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def moveMonsterResponse(self, objectid: int, moveid: int, currentMp: int, useSkills: bool, skillId: int, skillLevel: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("moveMonsterResponse--------------------")
        mplew.writeShort(SendPacketOpcode.MOVE_MONSTER_RESPONSE.getValue())
        mplew.writeInt(objectid)
        mplew.writeShort(moveid)
        mplew.write(useSkills ? 1 : 0)
        mplew.writeShort(currentMp)
        mplew.write(skillId)
        mplew.write(skillLevel)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getSpecialLongMask(self, statups: list) -> int:
        if ServerConstants.调试输出封包:
            print("getSpecialLongMask--------------------")
        mask = 0
        for statup in statups:
            if statup.isFirst():
                mask |= statup.getValue()
        return mask

    def getLongMask(self, statups: list) -> int:
        if ServerConstants.调试输出封包:
            print("getLongMask--------------------")
        mask = 0
        for statup in statups:
            if not statup.isFirst():
                mask |= statup.getValue()
        return mask

    def getLongMask_NoRef(self, statups: list) -> int:
        if ServerConstants.调试输出封包:
            print("getLongMask_NoRef--------------------")
        mask = 0
        ignore_imm = False
        for statup in statups:
            if statup == MonsterStatus.反射魔法伤害 or statup == MonsterStatus.反射物理伤害:
                ignore_imm = True
                break
        for statup in statups:
            if statup != MonsterStatus.反射魔法伤害 and statup != MonsterStatus.反射物理伤害:
                if ignore_imm:
                    if statup == MonsterStatus.免疫魔法攻击:
                        continue
                    if statup == MonsterStatus.免疫物理攻击:
                        continue
                if statup.isFirst():
                    continue
                mask |= statup.getValue()
        return mask

    def applyMonsterStatus(self, oid: int, mse: Any, x: int, skil: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("applyMonsterStatus--------------------")
        mplew.writeShort(SendPacketOpcode.APPLY_MONSTER_STATUS.getValue())
        mplew.writeInt(oid)
        mplew.writeLong(getSpecialLongMask(Collections.singletonList(mse)))
        mplew.writeLong(getLongMask(Collections.singletonList(mse)))
        mplew.writeShort(x)
        mplew.writeShort(skil.getSkillId())
        mplew.writeShort(skil.getSkillLevel())
        mplew.writeShort(mse == 0 ? 1 : 0)
        mplew.writeShort(0)
        mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def applyMonsterStatus_oid_mse(self, oid: int, mse: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("applyMonsterStatusA--------------------")
        mplew.writeShort(SendPacketOpcode.APPLY_MONSTER_STATUS.getValue())
        mplew.writeInt(oid)
        mplew.writeLong(getSpecialLongMask(Collections.singletonList(mse.getStati())))
        mplew.writeLong(getLongMask(Collections.singletonList(mse.getStati())))
        mplew.writeShort(mse.getX())
        if mse.isMonsterSkill():
            mplew.writeShort(mse.getMobSkill().getSkillId())
            mplew.writeShort(mse.getMobSkill().getSkillLevel())
        elif mse.getSkill() > 0:
            mplew.writeInt(mse.getSkill())
        mplew.writeShort(mse.getStati() == 0 ? 1 : 0)
        mplew.writeShort(0)
        mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def applyMonsterStatus_oid_stati_reflection_skil(self, oid: int, stati: dict, reflection: list, skil: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("applyMonsterStatusB--------------------")
        mplew.writeShort(SendPacketOpcode.APPLY_MONSTER_STATUS.getValue())
        mplew.writeInt(oid)
        mplew.writeLong(getSpecialLongMask(stati.keys()))
        mplew.writeLong(getLongMask(stati.keys()))
        for (final Map.Entry<MonsterStatus, Integer> mse : stati.items())
            mplew.writeShort(mse.getValue())
            mplew.writeShort(skil.getSkillId())
            mplew.writeShort(skil.getSkillLevel())
            mplew.writeShort(mse.getKey() == 0 ? 1 : 0)
        for ref in reflection:
            mplew.writeInt(ref)
        mplew.writeInt(0)
        mplew.writeShort(0)
        size = stati
        if reflection > 0:
            size /= 2
        mplew.write(size)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def cancelMonsterStatus(self, oid: int, stat: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("cancelMonsterStatus--------------------")
        mplew.writeShort(SendPacketOpcode.CANCEL_MONSTER_STATUS.getValue())
        mplew.writeInt(oid)
        mplew.writeLong(getSpecialLongMask(Collections.singletonList(stat)))
        mplew.writeLong(getLongMask(Collections.singletonList(stat)))
        mplew.write(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def talkMonster(self, oid: int, itemId: int, msg: str) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("talkMonster--------------------")
        mplew.writeShort(SendPacketOpcode.TALK_MONSTER.getValue())
        mplew.writeInt(oid)
        mplew.writeInt(500)
        mplew.writeInt(itemId)
        mplew.write((itemId > 0) ? 1 : 0)
        mplew.write((msg is not None and msg > 0) ? 1 : 0)
        if msg is not None and msg > 0:
            mplew.writeMapleAsciiString(msg)
        mplew.writeInt(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeTalkMonster(self, oid: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeTalkMonster--------------------")
        mplew.writeShort(SendPacketOpcode.REMOVE_TALK_MONSTER.getValue())
        mplew.writeInt(oid)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

