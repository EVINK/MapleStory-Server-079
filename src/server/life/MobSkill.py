"""
MobSkill - Converted from Java source
Original: server/life/MobSkill.java
Package: server.life
"""

from enum import Enum
from typing import Dict
from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleMist import *  # TODO: import specific classes


class MobSkill:
    """
    Class MobSkill
    """

    def __init__(self, skillId: int, level: int):
        self.skillId = None
        self.skillLevel = None
        self.mpCon = 0
        self.spawnEffect = 0
        self.hp = 0
        self.x = 0
        self.y = 0
        self.duration = 0
        self.cooltime = 0
        self.prop = 0.0
        self.limit = 0
        self.toSummon = []
        self.lt = None
        self.rb = None
        self.toSummon = []
        self.skillId = skillId
        self.skillLevel = level


    def setMpCon(self, mpCon: int) -> None:
        self.mpCon = mpCon

    def addSummons(self, toSummon: list) -> None:
        self.toSummon = toSummon

    def setSpawnEffect(self, spawnEffect: int) -> None:
        self.spawnEffect = spawnEffect

    def setHp(self, hp: int) -> None:
        self.hp = hp

    def setX(self, x: int) -> None:
        self.x = x

    def setY(self, y: int) -> None:
        self.y = y

    def setDuration(self, duration: int) -> None:
        self.duration = duration

    def setCoolTime(self, cooltime: int) -> None:
        self.cooltime = cooltime

    def setProp(self, prop: float) -> None:
        self.prop = prop

    def setLtRb(self, lt: Any, rb: Any) -> None:
        self.lt = lt
        self.rb = rb

    def setLimit(self, limit: int) -> None:
        self.limit = limit

    def checkCurrentBuff(self, player: Any, monster: Any) -> bool:
        stop = False
        # switch (self.skillId):
            # case 100:
            # case 110:
            # case 150:
                stop = monster.isBuffed(MonsterStatus.物理攻击提升)
                break
            # case 101:
            # case 111:
            # case 151:
                stop = monster.isBuffed(MonsterStatus.魔法攻击提升)
                break
            # case 102:
            # case 112:
            # case 152:
                stop = monster.isBuffed(MonsterStatus.物理防御提升)
                break
            # case 103:
            # case 113:
            # case 153:
                stop = monster.isBuffed(MonsterStatus.魔法防御提升)
                break
            # case 140:
            # case 141:
            # case 142:
            # case 143:
            # case 144:
            # case 145:
                stop = (monster.isBuffed(MonsterStatus.免疫伤害) or monster.isBuffed(MonsterStatus.免疫魔法攻击) or monster.isBuffed(MonsterStatus.免疫物理攻击))
                break
            # case 200:
                stop = (player.getMap().getNumMonsters() >= self.limit)
                break
        return stop

    def applyEffect(self, player: Any, monster: Any, skill: bool) -> None:
        disease = None
        stats = new EnumMap<MonsterStatus, Integer>(MonsterStatus.class)
        reflection = []
        # switch (self.skillId):
            # case 100:
            # case 110:
            # case 150:
                stats.put(MonsterStatus.物理攻击提升, self.x)
                break
            # case 101:
            # case 111:
            # case 151:
                stats.put(MonsterStatus.魔法攻击提升, self.x)
                break
            # case 102:
            # case 112:
            # case 152:
                stats.put(MonsterStatus.物理防御提升, self.x)
                break
            # case 103:
            # case 113:
            # case 153:
                stats.put(MonsterStatus.魔法防御提升, self.x)
                break
            # case 154:
                stats.put(MonsterStatus.命中, self.x)
                break
            # case 155:
                stats.put(MonsterStatus.回避, self.x)
                break
            # case 156:
                stats.put(MonsterStatus.速度, self.x)
                break
            # case 157:
                stats.put(MonsterStatus.封印, self.x)
                break
            # case 114:
                if self.lt is not None and self.rb is not None and skill and monster is not None:
                    objects = self.getObjectsInRange(monster, MapleMapObjectType.MONSTER)
                    hp = self.getX() / 1000 * (int)(950.0 + 1050.0 * random.random())
                    for mons in objects:
                        if (mons).getStats().isBoss():
                            (mons).heal(hp, self.getY(), True)
                    break
                if monster is not None and monster.getStats().isBoss():
                    monster.heal(self.getX(), self.getY(), True)
                    break
                break
            # case 120:
            # case 121:
            # case 122:
            # case 123:
            # case 124:
            # case 125:
            # case 126:
            # case 128:
            # case 132:
            # case 133:
            # case 134:
            # case 135:
            # case 136:
            # case 137:
                disease = MapleDisease.getBySkill(self.skillId)
                break
            # case 127:
                if self.lt is not None and self.rb is not None and skill and monster is not None and player is not None:
                    for character in self.getPlayersInRange(monster, player):
                        character.dispel()
                    break
                if player is not None:
                    player.dispel()
                    break
                break
            # case 129:
                if monster is None:
                    break
                if monster.getEventInstance() is not None and monster.getEventInstance().getName().find("BossQuest") != -1:
                    break
                info = monster.getStats().getBanishInfo()
                if info is not None and info.getMap() != 0 and info.getPortal() is not None:
                    if self.lt is not None and self.rb is not None and skill and player is not None:
                        for chr in self.getPlayersInRange(monster, player):
                            chr.changeMapBanish(info.getMap(), info.getPortal(), info.getMsg())
                    elif player is not None:
                        player.changeMapBanish(info.getMap(), info.getPortal(), info.getMsg())
                break
            # case 131:
                if monster is not None:
                    monster.getMap().spawnMist(MapleMist(self.calculateBoundingBox(monster.getPosition(), True), monster, this), self.x * 10, False)
                    break
                break
            # case 140:
                stats.put(MonsterStatus.免疫物理攻击, self.x)
                break
            # case 141:
                stats.put(MonsterStatus.免疫魔法攻击, self.x)
                break
            # case 142:
                stats.put(MonsterStatus.免疫伤害, self.x)
                break
            # case 143:
                stats.put(MonsterStatus.反射物理伤害, self.x)
                stats.put(MonsterStatus.免疫物理攻击, self.x)
                reflection.add(self.x)
                break
            # case 144:
                stats.put(MonsterStatus.反射魔法伤害, self.x)
                stats.put(MonsterStatus.免疫魔法攻击, self.x)
                reflection.add(self.x)
                break
            # case 145:
                stats.put(MonsterStatus.反射物理伤害, self.x)
                stats.put(MonsterStatus.免疫物理攻击, self.x)
                stats.put(MonsterStatus.反射魔法伤害, self.x)
                stats.put(MonsterStatus.免疫魔法攻击, self.x)
                reflection.add(self.x)
                reflection.add(self.x)
                break
            # case 200:
                if monster is None:
                    return
                for mobId in self.getSummons():
                    toSpawn = None
                    try:
                        toSpawn = MapleLifeFactory.getMonster(GameConstants.getCustomSpawnID(monster.getId(), mobId))
                    except Exception as e:
                        continue
                    if toSpawn is None:
                        continue
                    toSpawn.setPosition(monster.getPosition())
                    ypos = monster.getPosition().getY()
                    xpos = monster.getPosition().getX()
                    # switch (mobId):
                        # case 8500003:
                            toSpawn.setFh(math.ceil(random.random() * 19.0))
                            ypos = -590
                            break
                        # case 8500004:
                            xpos = (int)(monster.getPosition().getX() + math.ceil(random.random() * 1000.0) - 500.0)
                            ypos = monster.getPosition().getY()
                            break
                        # case 8510100:
                            if math.ceil(random.random() * 5.0) == 1.0:
                                ypos = 78
                                xpos = (int)(0.0 + math.ceil(random.random() * 5.0)) + ((math.ceil(random.random() * 2.0) == 1.0) ? 180 : 0)
                                break
                            xpos = (int)(monster.getPosition().getX() + math.ceil(random.random() * 1000.0) - 500.0)
                            break
                        # case 8820007:
                            continue
                    # switch (monster.getMap().getId()):
                        # case 220080001:
                            if xpos < -890:
                                xpos = (int)(-890.0 + math.ceil(random.random() * 150.0))
                                break
                            if xpos > 230:
                                xpos = (int)(230.0 - math.ceil(random.random() * 150.0))
                                break
                            break
                        # case 230040420:
                            if xpos < -239:
                                xpos = (int)(-239.0 + math.ceil(random.random() * 150.0))
                                break
                            if xpos > 371:
                                xpos = (int)(371.0 - math.ceil(random.random() * 150.0))
                                break
                            break
                    monster.getMap().spawnMonsterWithEffect(toSpawn, self.getSpawnEffect(), monster.getMap().calcPointBelow(Point(xpos, ypos - 1)))
                break
        if stats > 0 and monster is not None:
            if self.lt is not None and self.rb is not None and skill:
                for mons2 in self.getObjectsInRange(monster, MapleMapObjectType.MONSTER):
                    (mons2).applyMonsterBuff(stats, self.getSkillId(), self.getDuration(), this, reflection)
            else:
                monster.applyMonsterBuff(stats, self.getSkillId(), self.getDuration(), this, reflection)
        if disease is not None and player is not None:
            if self.lt is not None and self.rb is not None and skill and monster is not None:
                for chr2 in self.getPlayersInRange(monster, player):
                    chr2.giveDebuff(disease, this)
            else:
                player.giveDebuff(disease, this)
        if monster is not None:
            monster.setMp(monster.getMp() - self.getMpCon())

    def getSkillId(self) -> int:
        return self.skillId

    def getSkillLevel(self) -> int:
        return self.skillLevel

    def getMpCon(self) -> int:
        return self.mpCon

    def getSummons(self) -> list:
        return Collections.unmodifiableList((List<? extends Integer>)self.toSummon)

    def getSpawnEffect(self) -> int:
        return self.spawnEffect

    def getHP(self) -> int:
        return self.hp

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getDuration(self) -> int:
        return self.duration

    def getCoolTime(self) -> int:
        return self.cooltime

    def getLt(self) -> Any:
        return self.lt

    def getRb(self) -> Any:
        return self.rb

    def getLimit(self) -> int:
        return self.limit

    def makeChanceResult(self) -> bool:
        return self.prop >= 1.0 or random.random() < self.prop

    def calculateBoundingBox(self, posFrom: Any, facingLeft: bool) -> Any:
        mylt = None
        myrb = None
        if facingLeft:
            mylt = Point(self.lt.x + posFrom.x, self.lt.y + posFrom.y)
            myrb = Point(self.rb.x + posFrom.x, self.rb.y + posFrom.y)
        else:
            myrb = Point(self.lt.x * -1 + posFrom.x, self.rb.y + posFrom.y)
            mylt = Point(self.rb.x * -1 + posFrom.x, self.lt.y + posFrom.y)
        bounds = Rectangle(mylt.x, mylt.y, myrb.x - mylt.x, myrb.y - mylt.y)
        return bounds

    def getPlayersInRange(self, monster: Any, player: Any) -> list:
        bounds = self.calculateBoundingBox(monster.getPosition(), monster.isFacingLeft())
        players = []
        players.add(player)
        return monster.getMap().getPlayersInRectAndInList(bounds, players)

    def getObjectsInRange(self, monster: Any, objectType: Any) -> list:
        bounds = self.calculateBoundingBox(monster.getPosition(), monster.isFacingLeft())
        objectTypes = []
        objectTypes.add(objectType)
        return monster.getMap().getMapObjectsInRect(bounds, objectTypes)

