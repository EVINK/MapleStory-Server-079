"""
SpawnPoint - Converted from Java source
Original: server/life/SpawnPoint.java
Package: server.life
"""

from threading import Lock
from typing import Optional, Any
import threading
import time

# Internal module imports
# from server.MapleCarnivalFactory import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class SpawnPoint(Spawns):
    """
    Class SpawnPoint
    Extends: Spawns
    """

    def __init__(self, monster: Any, pos: Any, mobTime: int, carnivalTeam: int, msg: str):
        self.monster = None
        self.pos = None
        self.nextPossibleSpawn = 0
        self.mobTime = None
        self.carnival = 0
        self.spawnedMonsters = None
        self.immobile = None
        self.msg = None
        self.carnivalTeam = None
        self.carnival = -1
        self.spawnedMonsters = AtomicInteger(0)
        self.monster = monster
        self.pos = pos
        self.mobTime = ((mobTime < 0) ? -1 : (mobTime * 1000))
        self.carnivalTeam = carnivalTeam
        self.msg = msg
        self.immobile = !monster.getStats().getMobile()
        self.nextPossibleSpawn = int(time.time() * 1000)


    def setCarnival(self, c: int) -> None:
        self.carnival = c

    def getPosition(self) -> Any:
        return self.pos

    def getMonster(self) -> Any:
        return self.monster

    def getCarnivalTeam(self) -> int:
        return self.carnivalTeam

    def getCarnivalId(self) -> int:
        return self.carnival

    def shouldSpawn(self) -> bool:
        return self.mobTime >= 0 && ((self.mobTime == 0 && !self.immobile) || self.spawnedMonsters.get() <= 0) && self.spawnedMonsters.get() <= 1 && self.nextPossibleSpawn <= int(time.time() * 1000)

    def spawnMonster(self, map: Any) -> Any:
        mob = MapleMonster(self.monster)
        mob.setPosition(self.pos)
        mob.setCarnivalTeam(self.carnivalTeam)
        self.spawnedMonsters.incrementAndGet()
        mob.addListener(MonsterListener()
            public void monsterKilled()
                SpawnPoint.self.nextPossibleSpawn = int(time.time() * 1000)
                if SpawnPoint.self.mobTime > 0:
                    SpawnPoint.self.nextPossibleSpawn += SpawnPoint.self.mobTime
                SpawnPoint.self.spawnedMonsters.decrementAndGet()
        map.spawnMonster(mob, -2)
        if self.carnivalTeam > -1:
            for r in map.getAllReactorsThreadsafe():
                if r.getName().startswith(str(self.carnivalTeam)) && r.getReactorId() == 9980000 + self.carnivalTeam && r.getState() < 5:
                    num = int(r.getName()[1:2])
                    final MapleCarnivalFactory.MCSkill skil = MapleCarnivalFactory.getInstance().getGuardian(num)
                    if skil is None:
                        continue
                    skil.getSkill().applyEffect(None, mob, False)
        if self.msg is not None:
            map.broadcastMessage(MaplePacketCreator.serverNotice(6, self.msg))
        return mob

    def monsterKilled(self) -> None:
        SpawnPoint.self.nextPossibleSpawn = int(time.time() * 1000)
        if SpawnPoint.self.mobTime > 0:
            SpawnPoint.self.nextPossibleSpawn += SpawnPoint.self.mobTime
        SpawnPoint.self.spawnedMonsters.decrementAndGet()

    def getMobTime(self) -> int:
        return self.mobTime

