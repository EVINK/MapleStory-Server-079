"""
SpawnPointAreaBoss - Converted from Java source
Original: server/life/SpawnPointAreaBoss.java
Package: server.life
"""

from typing import List
from typing import Optional, Any
import time

# Internal module imports
# from server.Randomizer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class SpawnPointAreaBoss(Spawns):
    """
    Class SpawnPointAreaBoss
    Extends: Spawns
    """

    def __init__(self, monster: Any, pos1: Any, pos2: Any, pos3: Any, mobTime: int, msg: str):
        self.monster = None
        self.pos1 = None
        self.pos2 = None
        self.pos3 = None
        self.nextPossibleSpawn = 0
        self.mobTime = None
        self.spawned = None
        self.msg = None
        self.spawned = AtomicBoolean(False)
        self.monster = monster
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.mobTime = ((mobTime < 0) ? -1 : (mobTime * 1000))
        self.msg = msg
        self.nextPossibleSpawn = int(time.time() * 1000)


    def getMonster(self) -> Any:
        return self.monster

    def getCarnivalTeam(self) -> int:
        return -1

    def getCarnivalId(self) -> int:
        return -1

    def shouldSpawn(self) -> bool:
        return self.mobTime >= 0 && !self.spawned.get() && self.nextPossibleSpawn <= int(time.time() * 1000)

    def getPosition(self) -> Any:
        rand = Randomizer.nextInt(3)
        return (rand == 0) ? self.pos1 : ((rand == 1) ? self.pos2 : self.pos3)

    def spawnMonster(self, map: Any) -> Any:
        mob = MapleMonster(self.monster)
        mob.setPosition(self.getPosition())
        self.spawned.set(True)
        mob.addListener(MonsterListener()
            public void monsterKilled()
                SpawnPointAreaBoss.self.nextPossibleSpawn = int(time.time() * 1000)
                if SpawnPointAreaBoss.self.mobTime > 0:
                    SpawnPointAreaBoss.self.nextPossibleSpawn += SpawnPointAreaBoss.self.mobTime
                SpawnPointAreaBoss.self.spawned.set(False)
        map.spawnMonster(mob, -2)
        if self.msg is not None:
            map.broadcastMessage(MaplePacketCreator.serverNotice(6, self.msg))
        return mob

    def monsterKilled(self) -> None:
        SpawnPointAreaBoss.self.nextPossibleSpawn = int(time.time() * 1000)
        if SpawnPointAreaBoss.self.mobTime > 0:
            SpawnPointAreaBoss.self.nextPossibleSpawn += SpawnPointAreaBoss.self.mobTime
        SpawnPointAreaBoss.self.spawned.set(False)

    def getMobTime(self) -> int:
        return self.mobTime

