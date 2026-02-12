"""
MobHandler - Converted from Java source
Original: handling/channel/handler/MobHandler.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes
# from server.maps.AnimatedMapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes


class MobHandler:
    """
    Class MobHandler
    """


    def MoveMonster(self, slea: Any, c: Any, chr: Any) -> None:
        res = None
        if chr is None or chr.getMap() is None:
        return
        oid = slea.readInt()
        monster = chr.getMap().getMonsterByOid(oid)
        if monster is None:
            chr.addMoveMob(oid)
            return
        moveid = slea.readShort()
        useSkill = (slea.readByte() > 0)
        skill = slea.readByte()
        skill1 = slea.readByte() & 0xFF
        skill2 = slea.readByte()
        skill3 = slea.readByte()
        skill4 = slea.readByte()
        realskill = 0
        level = 0
        if useSkill:
            size = monster.getNoSkills()
            used = False
            if size > 0:
                skillToUse = monster.getSkills().get(Randomizer.nextInt(size))
                realskill = (skillToUse.getLeft())
                level = (skillToUse.getRight())
                mobSkill = MobSkillFactory.getMobSkill(realskill, level)
                if mobSkill is not None and not mobSkill.checkCurrentBuff(chr, monster):
                    now = int(time.time() * 1000)
                    ls = monster.getLastSkillUsed(realskill)
                    if ls == 0 or now - ls > mobSkill.getCoolTime():
                        monster.setLastSkillUsed(realskill, now, mobSkill.getCoolTime())
                        reqHp = (int)(monster.getHp() / monster.getMobMaxHp() * 100.0)
                        if reqHp <= mobSkill.getHP():
                            used = True
                            mobSkill.applyEffect(chr, monster, True)
            if not used:
                realskill = 0
                level = 0
        slea.readByte()
        slea.readInt()
        slea.readLong()
        startPos = slea.readPos()
        try:
            res = MovementParse.parseMovement(slea, 2)
        except ArrayIndexOutOfBoundsException as e:
            FileoutputUtil.outputFileError(FileoutputUtil.Movement_Log, e)
            FileoutputUtil.log(FileoutputUtil.Movement_Log, "怪物ID " + monster.getId() + ", AIOBE Type2:\r\n" + slea.toString(True))
            return
        c.getSession().write(MobPacket.moveMonsterResponse(monster.getObjectId(), moveid, monster.getMp(), monster.isControllerHasAggro(), realskill, level))
        if res is not None:
            map = chr.getMap()
            MovementParse.updatePosition(res, monster, -1)
            map.moveMonster(monster, monster.getPosition())
            map.broadcastMessage(chr, MobPacket.moveMonster(useSkill, skill, skill1, skill2, skill3, skill4, monster.getObjectId(), startPos, monster.getPosition(), res), monster.getPosition())
            if not chr.isGM():
            chr.getCheatTracker().checkMoveMonster(monster.getPosition(), chr)

    def FriendlyDamage(self, slea: Any, chr: Any) -> None:
        map = chr.getMap()
        if map is None:
            return
        mobfrom = map.getMonsterByOid(slea.readInt())
        slea.skip(4)
        mobto = map.getMonsterByOid(slea.readInt())
        if mobfrom is not None and mobto is not None and mobto.getStats().isFriendly():
            damage = mobto.getStats().getLevel() * Randomizer.nextInt(mobto.getStats().getLevel()) / 2
            mobto.damage(chr, damage, True)
            checkShammos(chr, mobto, map)

    def checkShammos(self, chr: Any, mobto: Any, map: Any) -> None:
        if not mobto.isAlive() and mobto.getId() == 9300275:
            for chrz in map.getCharactersThreadsafe():
                if chrz.getParty() is not None and chrz.getParty().getLeader().getId() == chrz.getId():
                    if chrz.haveItem(2022698):
                        MapleInventoryManipulator.removeById(chrz.getClient(), MapleInventoryType.USE, 2022698, 1, False, True)
                        mobto.heal(mobto.getMobMaxHp(), mobto.getMobMaxMp(), True)
                        return
                    break
            map.broadcastMessage(MaplePacketCreator.serverNotice(6, "未能保护好这个怪物."))
            mapp = chr.getClient().getChannelServer().getMapFactory().getMap(921120001)
            for chrz2 in map.getCharactersThreadsafe():
                chrz2.changeMap(mapp, mapp.getPortal(0))
        elif mobto.getId() == 9300275 and mobto.getEventInstance() is not None:
            mobto.getEventInstance().setProperty("HP", str(mobto.getHp()))

    def MonsterBomb(self, oid: int, chr: Any) -> None:
        monster = chr.getMap().getMonsterByOid(oid)
        if monster is None or not chr.isAlive() or chr.isHidden():
            return
        selfd = monster.getStats().getSelfD()
        if selfd != -1:
            chr.getMap().killMonster(monster, chr, False, False, selfd)

    def AutoAggro(self, monsteroid: int, chr: Any) -> None:
        if chr is None or chr.getMap() is None or chr.isHidden():
            return
        monster = chr.getMap().getMonsterByOid(monsteroid)
        if monster is not None and chr.getPosition().distanceSq(monster.getPosition()) < 200000.0:
            if monster.getController() is not None:
                if chr.getMap().getCharacterById(monster.getController().getId()) is None:
                    monster.switchController(chr, True)
                else:
                    monster.switchController(monster.getController(), True)
            else:
                monster.switchController(chr, True)

