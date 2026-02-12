"""
MapleMap - 从Java源文件转换而来
对应Java源文件: server/maps/MapleMap.java
包路径: server.maps
"""

from concurrent.futures import Future
from dataclasses import dataclass
from datetime import datetime
from datetime import datetime, timezone, timedelta
from enum import Enum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, List, Dict, Any, Set
from weakref import ref
import math
import pymysql
import sched
import threading
import time
import weakref

# 内部模块导入 (Internal module imports)
# from client.MapleBuffStat import *  # TODO: 根据实际需要导入具体类
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类
# from client.inventory.Equip import *  # TODO: 根据实际需要导入具体类
# from client.inventory.IItem import *  # TODO: 根据实际需要导入具体类
# from client.inventory.Item import *  # TODO: 根据实际需要导入具体类
# from client.inventory.MapleInventoryType import *  # TODO: 根据实际需要导入具体类
# from client.inventory.MaplePet import *  # TODO: 根据实际需要导入具体类
# from client.status.MonsterStatus import *  # TODO: 根据实际需要导入具体类
# from client.status.MonsterStatusEffect import *  # TODO: 根据实际需要导入具体类
# from constants.GameConstants import *  # TODO: 根据实际需要导入具体类
# from constants.ServerConstants import *  # TODO: 根据实际需要导入具体类
# from database.DatabaseConnection import *  # TODO: 根据实际需要导入具体类
# from handling.MaplePacket import *  # TODO: 根据实际需要导入具体类
# from handling.channel.ChannelServer import *  # TODO: 根据实际需要导入具体类
# from handling.login.LoginServer import *  # TODO: 根据实际需要导入具体类
# from handling.world.MaplePartyCharacter import *  # TODO: 根据实际需要导入具体类
# from handling.world.World import *  # TODO: 根据实际需要导入具体类
# from scripting.EventManager import *  # TODO: 根据实际需要导入具体类
# from server.MapleCarnivalFactory import *  # TODO: 根据实际需要导入具体类
# from server.MapleInventoryManipulator import *  # TODO: 根据实际需要导入具体类
# from server.MapleItemInformationProvider import *  # TODO: 根据实际需要导入具体类
# from server.MaplePortal import *  # TODO: 根据实际需要导入具体类
# from server.MapleSquad import *  # TODO: 根据实际需要导入具体类
# from server.MapleStatEffect import *  # TODO: 根据实际需要导入具体类
# from server.Randomizer import *  # TODO: 根据实际需要导入具体类
# from server.SpeedRunner import *  # TODO: 根据实际需要导入具体类
# from server.Timer import *  # TODO: 根据实际需要导入具体类
# from server.events.MapleEvent import *  # TODO: 根据实际需要导入具体类
# from server.life.MapleLifeFactory import *  # TODO: 根据实际需要导入具体类
# from server.life.MapleMonster import *  # TODO: 根据实际需要导入具体类
# from server.life.MapleMonsterInformationProvider import *  # TODO: 根据实际需要导入具体类
# from server.life.MapleNPC import *  # TODO: 根据实际需要导入具体类
# from server.life.MonsterDropEntry import *  # TODO: 根据实际需要导入具体类
# from server.life.MonsterGlobalDropEntry import *  # TODO: 根据实际需要导入具体类
# from server.life.OverrideMonsterStats import *  # TODO: 根据实际需要导入具体类
# from server.life.SpawnPoint import *  # TODO: 根据实际需要导入具体类
# from server.life.SpawnPointAreaBoss import *  # TODO: 根据实际需要导入具体类
# from server.life.Spawns import *  # TODO: 根据实际需要导入具体类
# from tools.FileoutputUtil import *  # TODO: 根据实际需要导入具体类
# from tools.MaplePacketCreator import *  # TODO: 根据实际需要导入具体类
# from tools.Pair import *  # TODO: 根据实际需要导入具体类
# from tools.StringUtil import *  # TODO: 根据实际需要导入具体类
# from tools.packet.MTSCSPacket import *  # TODO: 根据实际需要导入具体类
# from tools.packet.MobPacket import *  # TODO: 根据实际需要导入具体类
# from tools.packet.PetPacket import *  # TODO: 根据实际需要导入具体类


class MapleMap:
    """
    类 MapleMap - 从Java类转换
    """

    def __init__(self, mapid: int, channel: int, returnMapId: int, monsterRate: float):
        """初始化 MapleMap"""
        self.mapobjects = None
        self.mapobjectlocks = None
        self.characters = None
        self.charactersLock = None
        self.runningOid = 0
        self.runningOidLock = None
        self.monsterSpawn = None
        self.spawnedMonstersOnMap = None
        self.portals = None
        self.footholds = None
        self.monsterRate = 0.0
        self.recoveryRate = 0.0
        self.mapEffect = None
        self.channel = None
        self.decHP = 0
        self.createMobInterval = 0
        self.consumeItemCoolTime = 0
        self.protectItem = 0
        self.decHPInterval = 0
        self.mapid = None
        self.returnMapId = 0
        self.timeLimit = 0
        self.fieldLimit = 0
        self.maxRegularSpawn = 0
        self.fixedMob = 0
        self.forcedReturnMap = 0
        self.lvForceMove = 0
        self.lvLimit = 0
        self.permanentWeather = 0
        self.town = False


    def setSpawns(self, fm: bool) -> None:
        """方法 setSpawns"""
        self.spawns = fm
        return None

    def getSpawns(self) -> bool:
        """方法 getSpawns"""
        return getattr(self, 'spawns', False)

    def setFixedMob(self, fm: int) -> None:
        """方法 setFixedMob"""
        self.fixed_mob = fm
        return None

    def setForceMove(self, fm: int) -> None:
        """方法 setForceMove"""
        self.force_move = fm
        return None

    def getForceMove(self) -> int:
        """方法 getForceMove"""
        return getattr(self, 'force_move', 0)

    def setLevelLimit(self, fm: int) -> None:
        """方法 setLevelLimit"""
        self.level_limit = fm
        return None

    def getLevelLimit(self) -> int:
        """方法 getLevelLimit"""
        return getattr(self, 'level_limit', 0)

    def setReturnMapId(self, rmi: int) -> None:
        """方法 setReturnMapId"""
        self.return_map_id = rmi
        return None

    def setSoaring(self, b: bool) -> None:
        """方法 setSoaring"""
        self.soaring = b
        return None

    def canSoar(self) -> bool:
        """方法 canSoar"""
        return False

    def toggleDrops(self) -> None:
        """方法 toggleDrops"""
        pass

    def setDrops(self, b: bool) -> None:
        """方法 setDrops"""
        self.drops = b
        return None

    def toggleGDrops(self) -> None:
        """方法 toggleGDrops"""
        pass

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def getReturnMap(self) -> Any:
        """方法 getReturnMap"""
        return getattr(self, 'return_map', None)

    def getReturnMapId(self) -> int:
        """方法 getReturnMapId"""
        return getattr(self, 'return_map_id', 0)

    def getForcedReturnId(self) -> int:
        """方法 getForcedReturnId"""
        return getattr(self, 'forced_return_id', 0)

    def getForcedReturnMap(self) -> Any:
        """方法 getForcedReturnMap"""
        return getattr(self, 'forced_return_map', None)

    def setForcedReturnMap(self, map: int) -> None:
        """方法 setForcedReturnMap"""
        self.forced_return_map = map
        return None

    def getRecoveryRate(self) -> float:
        """方法 getRecoveryRate"""
        return getattr(self, 'recovery_rate', 0)

    def setRecoveryRate(self, recoveryRate: float) -> None:
        """方法 setRecoveryRate"""
        self.recovery_rate = recoveryRate
        return None

    def getFieldLimit(self) -> int:
        """方法 getFieldLimit"""
        return getattr(self, 'field_limit', 0)

    def setFieldLimit(self, fieldLimit: int) -> None:
        """方法 setFieldLimit"""
        self.field_limit = fieldLimit
        return None

    def setCreateMobInterval(self, createMobInterval: int) -> None:
        """方法 setCreateMobInterval"""
        self.create_mob_interval = createMobInterval
        return None

    def setTimeLimit(self, timeLimit: int) -> None:
        """方法 setTimeLimit"""
        self.time_limit = timeLimit
        return None

    def setMapName(self, mapName: str) -> None:
        """方法 setMapName"""
        self.map_name = mapName
        return None

    def getMapName(self) -> str:
        """方法 getMapName"""
        return getattr(self, 'map_name', "")

    def getStreetName(self) -> str:
        """方法 getStreetName"""
        return getattr(self, 'street_name', "")

    def setFirstUserEnter(self, onFirstUserEnter: str) -> None:
        """方法 setFirstUserEnter"""
        self.first_user_enter = onFirstUserEnter
        return None

    def setUserEnter(self, onUserEnter: str) -> None:
        """方法 setUserEnter"""
        self.user_enter = onUserEnter
        return None

    def setOnUserEnter(self, onUserEnter: str) -> None:
        """方法 setOnUserEnter"""
        self.on_user_enter = onUserEnter
        return None

    def hasClock(self) -> bool:
        """方法 hasClock"""
        return bool(getattr(self, 'clock', False))

    def setClock(self, hasClock: bool) -> None:
        """方法 setClock"""
        self.clock = hasClock
        return None

    def isTown(self) -> bool:
        """方法 isTown"""
        return bool(getattr(self, 'town', False))

    def setTown(self, town: bool) -> None:
        """方法 setTown"""
        self.town = town
        return None

    def allowPersonalShop(self) -> bool:
        """方法 allowPersonalShop"""
        return False

    def setPersonalShop(self, personalShop: bool) -> None:
        """方法 setPersonalShop"""
        self.personal_shop = personalShop
        return None

    def setStreetName(self, streetName: str) -> None:
        """方法 setStreetName"""
        self.street_name = streetName
        return None

    def setEverlast(self, everlast: bool) -> None:
        """方法 setEverlast"""
        self.everlast = everlast
        return None

    def getEverlast(self) -> bool:
        """方法 getEverlast"""
        return getattr(self, 'everlast', False)

    def getHPDec(self) -> int:
        """方法 getHPDec"""
        return getattr(self, 'hp_dec', 0)

    def setHPDec(self, delta: int) -> None:
        """方法 setHPDec"""
        self.hp_dec = delta
        return None

    def getHPDecInterval(self) -> int:
        """方法 getHPDecInterval"""
        return getattr(self, 'hp_dec_interval', 0)

    def setHPDecInterval(self, delta: int) -> None:
        """方法 setHPDecInterval"""
        self.hp_dec_interval = delta
        return None

    def getHPDecProtect(self) -> int:
        """方法 getHPDecProtect"""
        return getattr(self, 'hp_dec_protect', 0)

    def setHPDecProtect(self, delta: int) -> None:
        """方法 setHPDecProtect"""
        self.hp_dec_protect = delta
        return None

    def getCurrentPartyId(self) -> int:
        """方法 getCurrentPartyId"""
        return getattr(self, 'current_party_id', 0)

    def addMapObject(self, mapobject: Any) -> None:
        """方法 addMapObject"""
        pass

    def spawnAndAddRangedMapObject(self, mapobject: Any, packetbakery: Any, condition: Any) -> None:
        """方法 spawnAndAddRangedMapObject"""
        pass

    def removeMapObject(self, obj: Any) -> None:
        """方法 removeMapObject"""
        pass


class ActivateItemReactor(Runnable):
    """
    类 ActivateItemReactor - 从Java类转换
    实现接口: Runnable
    """

    def __init__(self, mapitem: Any, reactor: Any, c: Any):
        """初始化 ActivateItemReactor"""
        self.mapobjects = None
        self.mapobjectlocks = None
        self.characters = None
        self.charactersLock = None
        self.runningOid = 0
        self.runningOidLock = None
        self.monsterSpawn = None
        self.spawnedMonstersOnMap = None
        self.portals = None
        self.footholds = None
        self.monsterRate = 0.0
        self.recoveryRate = 0.0
        self.mapEffect = None
        self.channel = None
        self.decHP = 0
        self.createMobInterval = 0
        self.consumeItemCoolTime = 0
        self.protectItem = 0
        self.decHPInterval = 0
        self.mapid = None
        self.returnMapId = 0
        self.timeLimit = 0
        self.fieldLimit = 0
        self.maxRegularSpawn = 0
        self.fixedMob = 0
        self.forcedReturnMap = 0
        self.lvForceMove = 0
        self.lvLimit = 0
        self.permanentWeather = 0
        self.town = False


    def setSpawns(self, fm: bool) -> None:
        """方法 setSpawns"""
        self.spawns = fm
        return None

    def getSpawns(self) -> bool:
        """方法 getSpawns"""
        return getattr(self, 'spawns', False)

    def setFixedMob(self, fm: int) -> None:
        """方法 setFixedMob"""
        self.fixed_mob = fm
        return None

    def setForceMove(self, fm: int) -> None:
        """方法 setForceMove"""
        self.force_move = fm
        return None

    def getForceMove(self) -> int:
        """方法 getForceMove"""
        return getattr(self, 'force_move', 0)

    def setLevelLimit(self, fm: int) -> None:
        """方法 setLevelLimit"""
        self.level_limit = fm
        return None

    def getLevelLimit(self) -> int:
        """方法 getLevelLimit"""
        return getattr(self, 'level_limit', 0)

    def setReturnMapId(self, rmi: int) -> None:
        """方法 setReturnMapId"""
        self.return_map_id = rmi
        return None

    def setSoaring(self, b: bool) -> None:
        """方法 setSoaring"""
        self.soaring = b
        return None

    def canSoar(self) -> bool:
        """方法 canSoar"""
        return False

    def toggleDrops(self) -> None:
        """方法 toggleDrops"""
        pass

    def setDrops(self, b: bool) -> None:
        """方法 setDrops"""
        self.drops = b
        return None

    def toggleGDrops(self) -> None:
        """方法 toggleGDrops"""
        pass

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def getReturnMap(self) -> Any:
        """方法 getReturnMap"""
        return getattr(self, 'return_map', None)

    def getReturnMapId(self) -> int:
        """方法 getReturnMapId"""
        return getattr(self, 'return_map_id', 0)

    def getForcedReturnId(self) -> int:
        """方法 getForcedReturnId"""
        return getattr(self, 'forced_return_id', 0)

    def getForcedReturnMap(self) -> Any:
        """方法 getForcedReturnMap"""
        return getattr(self, 'forced_return_map', None)

    def setForcedReturnMap(self, map: int) -> None:
        """方法 setForcedReturnMap"""
        self.forced_return_map = map
        return None

    def getRecoveryRate(self) -> float:
        """方法 getRecoveryRate"""
        return getattr(self, 'recovery_rate', 0)

    def setRecoveryRate(self, recoveryRate: float) -> None:
        """方法 setRecoveryRate"""
        self.recovery_rate = recoveryRate
        return None

    def getFieldLimit(self) -> int:
        """方法 getFieldLimit"""
        return getattr(self, 'field_limit', 0)

    def setFieldLimit(self, fieldLimit: int) -> None:
        """方法 setFieldLimit"""
        self.field_limit = fieldLimit
        return None

    def setCreateMobInterval(self, createMobInterval: int) -> None:
        """方法 setCreateMobInterval"""
        self.create_mob_interval = createMobInterval
        return None

    def setTimeLimit(self, timeLimit: int) -> None:
        """方法 setTimeLimit"""
        self.time_limit = timeLimit
        return None

    def setMapName(self, mapName: str) -> None:
        """方法 setMapName"""
        self.map_name = mapName
        return None

    def getMapName(self) -> str:
        """方法 getMapName"""
        return getattr(self, 'map_name', "")

    def getStreetName(self) -> str:
        """方法 getStreetName"""
        return getattr(self, 'street_name', "")

    def setFirstUserEnter(self, onFirstUserEnter: str) -> None:
        """方法 setFirstUserEnter"""
        self.first_user_enter = onFirstUserEnter
        return None

    def setUserEnter(self, onUserEnter: str) -> None:
        """方法 setUserEnter"""
        self.user_enter = onUserEnter
        return None

    def setOnUserEnter(self, onUserEnter: str) -> None:
        """方法 setOnUserEnter"""
        self.on_user_enter = onUserEnter
        return None

    def hasClock(self) -> bool:
        """方法 hasClock"""
        return bool(getattr(self, 'clock', False))

    def setClock(self, hasClock: bool) -> None:
        """方法 setClock"""
        self.clock = hasClock
        return None

    def isTown(self) -> bool:
        """方法 isTown"""
        return bool(getattr(self, 'town', False))

    def setTown(self, town: bool) -> None:
        """方法 setTown"""
        self.town = town
        return None

    def allowPersonalShop(self) -> bool:
        """方法 allowPersonalShop"""
        return False

    def setPersonalShop(self, personalShop: bool) -> None:
        """方法 setPersonalShop"""
        self.personal_shop = personalShop
        return None

    def setStreetName(self, streetName: str) -> None:
        """方法 setStreetName"""
        self.street_name = streetName
        return None

    def setEverlast(self, everlast: bool) -> None:
        """方法 setEverlast"""
        self.everlast = everlast
        return None

    def getEverlast(self) -> bool:
        """方法 getEverlast"""
        return getattr(self, 'everlast', False)

    def getHPDec(self) -> int:
        """方法 getHPDec"""
        return getattr(self, 'hp_dec', 0)

    def setHPDec(self, delta: int) -> None:
        """方法 setHPDec"""
        self.hp_dec = delta
        return None

    def getHPDecInterval(self) -> int:
        """方法 getHPDecInterval"""
        return getattr(self, 'hp_dec_interval', 0)

    def setHPDecInterval(self, delta: int) -> None:
        """方法 setHPDecInterval"""
        self.hp_dec_interval = delta
        return None

    def getHPDecProtect(self) -> int:
        """方法 getHPDecProtect"""
        return getattr(self, 'hp_dec_protect', 0)

    def setHPDecProtect(self, delta: int) -> None:
        """方法 setHPDecProtect"""
        self.hp_dec_protect = delta
        return None

    def getCurrentPartyId(self) -> int:
        """方法 getCurrentPartyId"""
        return getattr(self, 'current_party_id', 0)

    def addMapObject(self, mapobject: Any) -> None:
        """方法 addMapObject"""
        pass

    def spawnAndAddRangedMapObject(self, mapobject: Any, packetbakery: Any, condition: Any) -> None:
        """方法 spawnAndAddRangedMapObject"""
        pass

    def removeMapObject(self, obj: Any) -> None:
        """方法 removeMapObject"""
        pass


from abc import ABC, abstractmethod

class SpawnCondition(ABC):
    """接口 SpawnCondition - 从Java接口转换"""

    @abstractmethod
    def maple_map(self, mapid: int, channel: int, returnMapId: int, monsterRate: float) -> Any:
        """抽象方法 MapleMap"""
        pass

    @abstractmethod
    def reentrant_read_write_lock(self) -> Any:
        """抽象方法 ReentrantReadWriteLock"""
        pass

    @abstractmethod
    def reentrant_lock(self) -> Any:
        """抽象方法 ReentrantLock"""
        pass

    @abstractmethod
    def atomic_integer(self, 0) -> Any:
        """抽象方法 AtomicInteger"""
        pass

    @abstractmethod
    def reentrant_read_write_lock(self) -> Any:
        """抽象方法 ReentrantReadWriteLock"""
        pass

    @abstractmethod
    def set_spawns(self, fm: bool) -> Any:
        """抽象方法 setSpawns"""
        pass

    @abstractmethod
    def get_spawns(self) -> Any:
        """抽象方法 getSpawns"""
        pass

    @abstractmethod
    def set_fixed_mob(self, fm: int) -> Any:
        """抽象方法 setFixedMob"""
        pass

    @abstractmethod
    def set_force_move(self, fm: int) -> Any:
        """抽象方法 setForceMove"""
        pass

    @abstractmethod
    def get_force_move(self) -> Any:
        """抽象方法 getForceMove"""
        pass

    @abstractmethod
    def set_level_limit(self, fm: int) -> Any:
        """抽象方法 setLevelLimit"""
        pass

    @abstractmethod
    def get_level_limit(self) -> Any:
        """抽象方法 getLevelLimit"""
        pass

    @abstractmethod
    def set_return_map_id(self, rmi: int) -> Any:
        """抽象方法 setReturnMapId"""
        pass

    @abstractmethod
    def set_soaring(self, b: bool) -> Any:
        """抽象方法 setSoaring"""
        pass

    @abstractmethod
    def can_soar(self) -> Any:
        """抽象方法 canSoar"""
        pass

    @abstractmethod
    def toggle_drops(self) -> Any:
        """抽象方法 toggleDrops"""
        pass

    @abstractmethod
    def set_drops(self, b: bool) -> Any:
        """抽象方法 setDrops"""
        pass

    @abstractmethod
    def toggle_g_drops(self) -> Any:
        """抽象方法 toggleGDrops"""
        pass

    @abstractmethod
    def get_id(self) -> Any:
        """抽象方法 getId"""
        pass

    @abstractmethod
    def get_return_map(self) -> Any:
        """抽象方法 getReturnMap"""
        pass

    @abstractmethod
    def get_return_map_id(self) -> Any:
        """抽象方法 getReturnMapId"""
        pass

    @abstractmethod
    def get_forced_return_id(self) -> Any:
        """抽象方法 getForcedReturnId"""
        pass

    @abstractmethod
    def get_forced_return_map(self) -> Any:
        """抽象方法 getForcedReturnMap"""
        pass

    @abstractmethod
    def set_forced_return_map(self, map: int) -> Any:
        """抽象方法 setForcedReturnMap"""
        pass

    @abstractmethod
    def get_recovery_rate(self) -> Any:
        """抽象方法 getRecoveryRate"""
        pass

    @abstractmethod
    def set_recovery_rate(self, recoveryRate: float) -> Any:
        """抽象方法 setRecoveryRate"""
        pass

    @abstractmethod
    def get_field_limit(self) -> Any:
        """抽象方法 getFieldLimit"""
        pass

    @abstractmethod
    def set_field_limit(self, fieldLimit: int) -> Any:
        """抽象方法 setFieldLimit"""
        pass

    @abstractmethod
    def set_create_mob_interval(self, createMobInterval: int) -> Any:
        """抽象方法 setCreateMobInterval"""
        pass

    @abstractmethod
    def set_time_limit(self, timeLimit: int) -> Any:
        """抽象方法 setTimeLimit"""
        pass

    @abstractmethod
    def set_map_name(self, mapName: str) -> Any:
        """抽象方法 setMapName"""
        pass

    @abstractmethod
    def get_map_name(self) -> Any:
        """抽象方法 getMapName"""
        pass

    @abstractmethod
    def get_street_name(self) -> Any:
        """抽象方法 getStreetName"""
        pass

    @abstractmethod
    def set_first_user_enter(self, onFirstUserEnter: str) -> Any:
        """抽象方法 setFirstUserEnter"""
        pass

    @abstractmethod
    def set_user_enter(self, onUserEnter: str) -> Any:
        """抽象方法 setUserEnter"""
        pass

    @abstractmethod
    def set_on_user_enter(self, onUserEnter: str) -> Any:
        """抽象方法 setOnUserEnter"""
        pass

    @abstractmethod
    def has_clock(self) -> Any:
        """抽象方法 hasClock"""
        pass

    @abstractmethod
    def set_clock(self, hasClock: bool) -> Any:
        """抽象方法 setClock"""
        pass

    @abstractmethod
    def is_town(self) -> Any:
        """抽象方法 isTown"""
        pass

    @abstractmethod
    def set_town(self, town: bool) -> Any:
        """抽象方法 setTown"""
        pass

    @abstractmethod
    def allow_personal_shop(self) -> Any:
        """抽象方法 allowPersonalShop"""
        pass

    @abstractmethod
    def set_personal_shop(self, personalShop: bool) -> Any:
        """抽象方法 setPersonalShop"""
        pass

    @abstractmethod
    def set_street_name(self, streetName: str) -> Any:
        """抽象方法 setStreetName"""
        pass

    @abstractmethod
    def set_everlast(self, everlast: bool) -> Any:
        """抽象方法 setEverlast"""
        pass

    @abstractmethod
    def get_everlast(self) -> Any:
        """抽象方法 getEverlast"""
        pass

    @abstractmethod
    def get_hp_dec(self) -> Any:
        """抽象方法 getHPDec"""
        pass

    @abstractmethod
    def set_hp_dec(self, delta: int) -> Any:
        """抽象方法 setHPDec"""
        pass

    @abstractmethod
    def get_hp_dec_interval(self) -> Any:
        """抽象方法 getHPDecInterval"""
        pass

    @abstractmethod
    def set_hp_dec_interval(self, delta: int) -> Any:
        """抽象方法 setHPDecInterval"""
        pass

    @abstractmethod
    def get_hp_dec_protect(self) -> Any:
        """抽象方法 getHPDecProtect"""
        pass

    @abstractmethod
    def set_hp_dec_protect(self, delta: int) -> Any:
        """抽象方法 setHPDecProtect"""
        pass

    @abstractmethod
    def get_current_party_id(self) -> Any:
        """抽象方法 getCurrentPartyId"""
        pass

    @abstractmethod
    def add_map_object(self, mapobject: Any) -> Any:
        """抽象方法 addMapObject"""
        pass

    @abstractmethod
    def spawn_and_add_ranged_map_object(self, mapobject: Any, packetbakery: Any, condition: Any) -> Any:
        """抽象方法 spawnAndAddRangedMapObject"""
        pass

    @abstractmethod
    def remove_map_object(self, obj: Any) -> Any:
        """抽象方法 removeMapObject"""
        pass

    @abstractmethod
    def calc_point_below(self, initial: Any) -> Any:
        """抽象方法 calcPointBelow"""
        pass

    @abstractmethod
    def point(self, initial.x, dropY) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def calc_drop_pos(self, initial: Any, fallback: Any) -> Any:
        """抽象方法 calcDropPos"""
        pass

    @abstractmethod
    def point(self, initial.x, 50: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def drop_from_monster(self, chr: Any, mob: Any) -> Any:
        """抽象方法 dropFromMonster"""
        pass

    @abstractmethod
    def drop_from_monster(self, chr: Any, mob: Any, instanced: bool) -> Any:
        """抽象方法 dropFromMonster"""
        pass

    @abstractmethod
    def point(self, 0, mob.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def item(self, de.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, de2.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def drop_from_monster2(self, chr: Any, mob: Any) -> Any:
        """抽象方法 dropFromMonster2"""
        pass

    @abstractmethod
    def point(self, 0, mob.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def item(self, de.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, 2370005, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, de2.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def remove_monster(self, monster: Any) -> Any:
        """抽象方法 removeMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int, lastSkill: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def if(self, 240060201: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 220080001: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000111: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000211: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000411: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000611: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000711: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000803: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000821: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 9420544: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 270050100: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 280030000: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 280030001: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8800010: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8800110: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8820014: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def get_all_reactor(self) -> Any:
        """抽象方法 getAllReactor"""
        pass

    @abstractmethod
    def get_all_reactors_threadsafe(self) -> Any:
        """抽象方法 getAllReactorsThreadsafe"""
        pass

    @abstractmethod
    def get_all_door(self) -> Any:
        """抽象方法 getAllDoor"""
        pass

    @abstractmethod
    def get_all_doors_threadsafe(self) -> Any:
        """抽象方法 getAllDoorsThreadsafe"""
        pass

    @abstractmethod
    def get_all_merchant(self) -> Any:
        """抽象方法 getAllMerchant"""
        pass

    @abstractmethod
    def get_all_hired_merchants_threadsafe(self) -> Any:
        """抽象方法 getAllHiredMerchantsThreadsafe"""
        pass

    @abstractmethod
    def get_all_monster(self) -> Any:
        """抽象方法 getAllMonster"""
        pass

    @abstractmethod
    def get_all_monsters_threadsafe(self) -> Any:
        """抽象方法 getAllMonstersThreadsafe"""
        pass

    @abstractmethod
    def kill_all_monsters(self, animate: bool) -> Any:
        """抽象方法 killAllMonsters"""
        pass

    @abstractmethod
    def kill_monster(self, monsId: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def map_debug__log(self) -> Any:
        """抽象方法 MapDebug_Log"""
        pass

    @abstractmethod
    def string_builder(self, ": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def limit_reactor(self, rid: int, num: int) -> Any:
        """抽象方法 limitReactor"""
        pass

    @abstractmethod
    def destroy_reactors(self, first: int, last: int) -> Any:
        """抽象方法 destroyReactors"""
        pass

    @abstractmethod
    def destroy_reactor(self, oid: int) -> Any:
        """抽象方法 destroyReactor"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def reload_reactors(self) -> Any:
        """抽象方法 reloadReactors"""
        pass

    @abstractmethod
    def reset_reactors(self) -> Any:
        """抽象方法 resetReactors"""
        pass

    @abstractmethod
    def set_reactor_state(self) -> Any:
        """抽象方法 setReactorState"""
        pass

    @abstractmethod
    def set_reactor_state(self, state: int) -> Any:
        """抽象方法 setReactorState"""
        pass

    @abstractmethod
    def shuffle_reactors(self) -> Any:
        """抽象方法 shuffleReactors"""
        pass

    @abstractmethod
    def shuffle_reactors(self, first: int, last: int) -> Any:
        """抽象方法 shuffleReactors"""
        pass

    @abstractmethod
    def update_monster_controller(self, monster: Any) -> Any:
        """抽象方法 updateMonsterController"""
        pass

    @abstractmethod
    def get_map_object(self, oid: int, type: Any) -> Any:
        """抽象方法 getMapObject"""
        pass

    @abstractmethod
    def contains_npc(self, npcid: int) -> Any:
        """抽象方法 containsNPC"""
        pass

    @abstractmethod
    def get_npc_by_id(self, id: int) -> Any:
        """抽象方法 getNPCById"""
        pass

    @abstractmethod
    def get_monster_by_id(self, id: int) -> Any:
        """抽象方法 getMonsterById"""
        pass

    @abstractmethod
    def count_monster_by_id(self, id: int) -> Any:
        """抽象方法 countMonsterById"""
        pass

    @abstractmethod
    def get_reactor_by_id(self, id: int) -> Any:
        """抽象方法 getReactorById"""
        pass

    @abstractmethod
    def get_monster_by_oid(self, oid: int) -> Any:
        """抽象方法 getMonsterByOid"""
        pass

    @abstractmethod
    def get_npc_by_oid(self, oid: int) -> Any:
        """抽象方法 getNPCByOid"""
        pass

    @abstractmethod
    def get_reactor_by_oid(self, oid: int) -> Any:
        """抽象方法 getReactorByOid"""
        pass

    @abstractmethod
    def get_reactor_by_name(self, name: str) -> Any:
        """抽象方法 getReactorByName"""
        pass

    @abstractmethod
    def spawn_npc(self, id: int, pos: Any) -> Any:
        """抽象方法 spawnNpc"""
        pass

    @abstractmethod
    def remove_npc(self, npcid: int) -> Any:
        """抽象方法 removeNpc"""
        pass

    @abstractmethod
    def spawn_monster_s_sack(self, mob: Any, pos: Any, spawnType: int) -> Any:
        """抽象方法 spawnMonster_sSack"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_monster_on_ground_below(self, mob: Any, pos: Any) -> Any:
        """抽象方法 spawnMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def spawn_monster_s_sack(self, mob: Any, pos: Any, spawnType: int, hp: int) -> Any:
        """抽象方法 spawnMonster_sSack"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_monster_on_ground_below(self, mob: Any, pos: Any, hp: int) -> Any:
        """抽象方法 spawnMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def spawn_monster_with_effect_below(self, mob: Any, pos: Any, effect: int) -> Any:
        """抽象方法 spawnMonsterWithEffectBelow"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_zakum(self, x: int, y: int) -> Any:
        """抽象方法 spawnZakum"""
        pass

    @abstractmethod
    def point(self, x, y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def get_all_mists_threadsafe(self) -> Any:
        """抽象方法 getAllMistsThreadsafe"""
        pass

    @abstractmethod
    def spawn_fake_monster_on_ground_below(self, mob: Any, pos: Any) -> Any:
        """抽象方法 spawnFakeMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def get_mobs_size(self) -> Any:
        """抽象方法 getMobsSize"""
        pass

    @abstractmethod
    def check_remove_after(self, monster: Any) -> Any:
        """抽象方法 checkRemoveAfter"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def spawn_revives(self, monster: Any, oid: int) -> Any:
        """抽象方法 spawnRevives"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_monster(self, monster: Any, spawnType: int) -> Any:
        """抽象方法 spawnMonster"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_monster_with_effect(self, monster: Any, effect: int, pos: Any) -> Any:
        """抽象方法 spawnMonsterWithEffect"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_fake_monster(self, monster: Any) -> Any:
        """抽象方法 spawnFakeMonster"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_reactor(self, reactor: Any) -> Any:
        """抽象方法 spawnReactor"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def respawn_reactor(self, reactor: Any) -> Any:
        """抽象方法 respawnReactor"""
        pass

    @abstractmethod
    def spawn_door(self, door: Any) -> Any:
        """抽象方法 spawnDoor"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def maple_party_character(self, c.getPlayer() -> Any:
        """抽象方法 MaplePartyCharacter"""
        pass

    @abstractmethod
    def can_spawn(self, chr: Any) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def spawn_summon(self, summon: Any) -> Any:
        """抽象方法 spawnSummon"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_dragon(self, summon: Any) -> Any:
        """抽象方法 spawnDragon"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mist(self, mist: Any, duration: int, fake: bool) -> Any:
        """抽象方法 spawnMist"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def monster_status_effect(self, MonsterStatus.中毒, Integer.valueOf(1) -> Any:
        """抽象方法 MonsterStatusEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def disappearing_item_drop(self, dropper: Any, owner: Any, item: Any, pos: Any) -> Any:
        """抽象方法 disappearingItemDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, item, droppos, dropper, owner, (byte) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def spawn_meso_drop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> Any:
        """抽象方法 spawnMesoDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, meso, droppos, dropper, owner, droptype, playerDrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mob_meso_drop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> Any:
        """抽象方法 spawnMobMesoDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, meso, position, dropper, owner, droptype, playerDrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mob_drop(self, idrop: Any, dropPos: Any, mob: Any, chr: Any, droptype: int, questid: int) -> Any:
        """抽象方法 spawnMobDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, idrop, dropPos, mob, chr, droptype, false, questid) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_rand_drop(self) -> Any:
        """抽象方法 spawnRandDrop"""
        pass

    @abstractmethod
    def spawn_auto_drop(self, itemid: int, pos: Any) -> Any:
        """抽象方法 spawnAutoDrop"""
        pass

    @abstractmethod
    def item(self, itemid, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def maple_map_item(self, pos, idrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_item_drop(self, dropper: Any, owner: Any, item: Any, pos: Any, ffaDrop: bool, playerDrop: bool) -> Any:
        """抽象方法 spawnItemDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, item, droppos, dropper, owner, (byte) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def delayed_packet_creation(self) -> Any:
        """抽象方法 DelayedPacketCreation"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def activate_item_reactors(self, drop: Any, c: Any) -> Any:
        """抽象方法 activateItemReactors"""
        pass

    @abstractmethod
    def activate_item_reactor(self, drop, react, c) -> Any:
        """抽象方法 ActivateItemReactor"""
        pass

    @abstractmethod
    def get_items_size(self) -> Any:
        """抽象方法 getItemsSize"""
        pass

    @abstractmethod
    def get_all_items(self) -> Any:
        """抽象方法 getAllItems"""
        pass

    @abstractmethod
    def get_all_items_threadsafe(self) -> Any:
        """抽象方法 getAllItemsThreadsafe"""
        pass

    @abstractmethod
    def return_ever_last_item(self, chr: Any) -> Any:
        """抽象方法 returnEverLastItem"""
        pass

    @abstractmethod
    def talk_monster(self, msg: str, itemId: int, objectid: int) -> Any:
        """抽象方法 talkMonster"""
        pass

    @abstractmethod
    def start_map_effect(self, msg: str, itemId: int) -> Any:
        """抽象方法 startMapEffect"""
        pass

    @abstractmethod
    def start_map_effect(self, msg: str, itemId: int, jukebox: bool) -> Any:
        """抽象方法 startMapEffect"""
        pass

    @abstractmethod
    def maple_map_effect(self, msg, itemId) -> Any:
        """抽象方法 MapleMapEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def start_extended_map_effect(self, msg: str, itemId: int) -> Any:
        """抽象方法 startExtendedMapEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def start_jukebox(self, msg: str, itemId: int) -> Any:
        """抽象方法 startJukebox"""
        pass

    @abstractmethod
    def add_player(self, chr: Any) -> Any:
        """抽象方法 addPlayer"""
        pass

    @abstractmethod
    def get_num_items(self) -> Any:
        """抽象方法 getNumItems"""
        pass

    @abstractmethod
    def has_forced_equip(self) -> Any:
        """抽象方法 hasForcedEquip"""
        pass

    @abstractmethod
    def set_field_type(self, fieldType: int) -> Any:
        """抽象方法 setFieldType"""
        pass

    @abstractmethod
    def get_num_monsters(self) -> Any:
        """抽象方法 getNumMonsters"""
        pass

    @abstractmethod
    def do_shrine(self, spawned: bool) -> Any:
        """抽象方法 doShrine"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def get_squad_by_map(self) -> Any:
        """抽象方法 getSquadByMap"""
        pass

    @abstractmethod
    def get_squad_begin(self) -> Any:
        """抽象方法 getSquadBegin"""
        pass

    @abstractmethod
    def get_em_by_map(self) -> Any:
        """抽象方法 getEMByMap"""
        pass

    @abstractmethod
    def remove_player(self, chr: Any) -> Any:
        """抽象方法 removePlayer"""
        pass

    @abstractmethod
    def get_all_players(self) -> Any:
        """抽象方法 getAllPlayers"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def broadcast_message(self, packet: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, repeatToSource: bool) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, packet: Any, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def send_object_placement(self, chr: Any) -> Any:
        """抽象方法 sendObjectPlacement"""
        pass

    @abstractmethod
    def get_map_objects_in_range(self, from: Any, rangeSq: float) -> Any:
        """抽象方法 getMapObjectsInRange"""
        pass

    @abstractmethod
    def get_items_in_range(self, from: Any, rangeSq: float) -> Any:
        """抽象方法 getItemsInRange"""
        pass

    @abstractmethod
    def get_map_objects_in_range(self, from: Any, rangeSq: float, MapObject_types: list) -> Any:
        """抽象方法 getMapObjectsInRange"""
        pass

    @abstractmethod
    def get_map_objects_in_rect(self, box: Any, MapObject_types: list) -> Any:
        """抽象方法 getMapObjectsInRect"""
        pass

    @abstractmethod
    def get_players_in_rect_and_in_list(self, box: Any, chrList: list) -> Any:
        """抽象方法 getPlayersInRectAndInList"""
        pass

    @abstractmethod
    def add_portal(self, myPortal: Any) -> Any:
        """抽象方法 addPortal"""
        pass

    @abstractmethod
    def get_portal(self, portalname: str) -> Any:
        """抽象方法 getPortal"""
        pass

    @abstractmethod
    def get_portal(self, portalid: int) -> Any:
        """抽象方法 getPortal"""
        pass

    @abstractmethod
    def reset_portals(self) -> Any:
        """抽象方法 resetPortals"""
        pass

    @abstractmethod
    def set_footholds(self, footholds: Any) -> Any:
        """抽象方法 setFootholds"""
        pass

    @abstractmethod
    def get_footholds(self) -> Any:
        """抽象方法 getFootholds"""
        pass

    @abstractmethod
    def load_monster_rate(self, first: bool) -> Any:
        """抽象方法 loadMonsterRate"""
        pass

    @abstractmethod
    def if(self, spawnSize: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def add_monster_spawn(self, monster: Any, mobTime: int, carnivalTeam: int, msg: str) -> Any:
        """抽象方法 addMonsterSpawn"""
        pass

    @abstractmethod
    def spawn_point(self, monster, newpos, mobTime, carnivalTeam, msg) -> Any:
        """抽象方法 SpawnPoint"""
        pass

    @abstractmethod
    def add_area_monster_spawn(self, monster: Any, pos1: Any, pos2: Any, pos3: Any, mobTime: int, msg: str) -> Any:
        """抽象方法 addAreaMonsterSpawn"""
        pass

    @abstractmethod
    def point(self, pos1) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos1) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def if(self, null: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def point(self, pos2) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos2) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def if(self, null: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def point(self, pos3) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos3) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_point_area_boss(self, monster, pos1, pos2, pos3, mobTime, msg) -> Any:
        """抽象方法 SpawnPointAreaBoss"""
        pass

    @abstractmethod
    def get_characters(self) -> Any:
        """抽象方法 getCharacters"""
        pass

    @abstractmethod
    def get_characters_threadsafe(self) -> Any:
        """抽象方法 getCharactersThreadsafe"""
        pass

    @abstractmethod
    def get_character_by_id__in_map(self, id: int) -> Any:
        """抽象方法 getCharacterById_InMap"""
        pass

    @abstractmethod
    def get_character_by_id(self, id: int) -> Any:
        """抽象方法 getCharacterById"""
        pass

    @abstractmethod
    def update_map_object_visibility(self, chr: Any, mo: Any) -> Any:
        """抽象方法 updateMapObjectVisibility"""
        pass

    @abstractmethod
    def if(self, mo.getType() -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, mo.getType() -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def move_monster(self, monster: Any, reportedPos: Any) -> Any:
        """抽象方法 moveMonster"""
        pass

    @abstractmethod
    def move_player(self, player: Any, newPosition: Any) -> Any:
        """抽象方法 movePlayer"""
        pass

    @abstractmethod
    def find_closest_spawnpoint(self, from: Any) -> Any:
        """抽象方法 findClosestSpawnpoint"""
        pass

    @abstractmethod
    def spawn_debug(self) -> Any:
        """抽象方法 spawnDebug"""
        pass

    @abstractmethod
    def string_builder(self, ": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def character_size(self) -> Any:
        """抽象方法 characterSize"""
        pass

    @abstractmethod
    def get_map_object_size(self) -> Any:
        """抽象方法 getMapObjectSize"""
        pass

    @abstractmethod
    def get_characters_size(self) -> Any:
        """抽象方法 getCharactersSize"""
        pass

    @abstractmethod
    def get_portals(self) -> Any:
        """抽象方法 getPortals"""
        pass

    @abstractmethod
    def get_spawned_monsters_on_map(self) -> Any:
        """抽象方法 getSpawnedMonstersOnMap"""
        pass

    @abstractmethod
    def spawn_love(self, love: Any) -> Any:
        """抽象方法 spawnLove"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def auto_nx(self, dy: int) -> Any:
        """抽象方法 AutoNx"""
        pass

    @abstractmethod
    def get_character_by_name(self, id: str) -> Any:
        """抽象方法 getCharacterByName"""
        pass

    @abstractmethod
    def hide_npc(self, npcid: int) -> Any:
        """抽象方法 hideNpc"""
        pass

    @abstractmethod
    def respawn(self, force: bool) -> Any:
        """抽象方法 respawn"""
        pass

    @abstractmethod
    def get_max_regular_spawn(self) -> Any:
        """抽象方法 getMaxRegularSpawn"""
        pass

    @abstractmethod
    def get_snowball_portal(self) -> Any:
        """抽象方法 getSnowballPortal"""
        pass

    @abstractmethod
    def is_disconnected(self, id: int) -> Any:
        """抽象方法 isDisconnected"""
        pass

    @abstractmethod
    def add_disconnected(self, id: int) -> Any:
        """抽象方法 addDisconnected"""
        pass

    @abstractmethod
    def reset_disconnected(self) -> Any:
        """抽象方法 resetDisconnected"""
        pass

    @abstractmethod
    def start_speed_run(self) -> Any:
        """抽象方法 startSpeedRun"""
        pass

    @abstractmethod
    def start_speed_run(self, leader: str) -> Any:
        """抽象方法 startSpeedRun"""
        pass

    @abstractmethod
    def end_speed_run(self) -> Any:
        """抽象方法 endSpeedRun"""
        pass

    @abstractmethod
    def get_rank_and_add(self, leader: str, time: str, type: Any, timz: int, squad: list) -> Any:
        """抽象方法 getRankAndAdd"""
        pass

    @abstractmethod
    def string_builder(self) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def speedruns(self, `type`, `leader`, `timestring`, `time`, `members`) -> Any:
        """抽象方法 speedruns"""
        pass

    @abstractmethod
    def string_builder(self, ".#k\r\n\r\n": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def get_speed_run_start(self) -> Any:
        """抽象方法 getSpeedRunStart"""
        pass

    @abstractmethod
    def disconnect_all(self) -> Any:
        """抽象方法 disconnectAll"""
        pass

    @abstractmethod
    def get_all_np_cs(self) -> Any:
        """抽象方法 getAllNPCs"""
        pass

    @abstractmethod
    def get_all_np_cs_threadsafe(self) -> Any:
        """抽象方法 getAllNPCsThreadsafe"""
        pass

    @abstractmethod
    def reset_np_cs(self) -> Any:
        """抽象方法 resetNPCs"""
        pass

    @abstractmethod
    def reset_fully(self) -> Any:
        """抽象方法 resetFully"""
        pass

    @abstractmethod
    def reset_fully(self, respawn: bool) -> Any:
        """抽象方法 resetFully"""
        pass

    @abstractmethod
    def cancel_squad_schedule(self) -> Any:
        """抽象方法 cancelSquadSchedule"""
        pass

    @abstractmethod
    def remove_drops(self) -> Any:
        """抽象方法 removeDrops"""
        pass

    @abstractmethod
    def remove_drops_delay(self) -> Any:
        """抽象方法 removeDropsDelay"""
        pass

    @abstractmethod
    def reset_all_spawn_point(self, mobid: int, mobTime: int) -> Any:
        """抽象方法 resetAllSpawnPoint"""
        pass

    @abstractmethod
    def point(self, oldMons.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def reset_spawns(self) -> Any:
        """抽象方法 resetSpawns"""
        pass

    @abstractmethod
    def make_carnival_spawn(self, team: int, newMons: Any, num: int) -> Any:
        """抽象方法 makeCarnivalSpawn"""
        pass

    @abstractmethod
    def point(self, mp.x, mp.y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, ret.x, ret.y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def make_carnival_reactor(self, team: int, num: int) -> Any:
        """抽象方法 makeCarnivalReactor"""
        pass

    @abstractmethod
    def maple_reactor(self, stats, team: Any) -> Any:
        """抽象方法 MapleReactor"""
        pass

    @abstractmethod
    def block_all_portal(self) -> Any:
        """抽象方法 blockAllPortal"""
        pass

    @abstractmethod
    def get_and_switch_team(self) -> Any:
        """抽象方法 getAndSwitchTeam"""
        pass

    @abstractmethod
    def set_squad(self, s: Any) -> Any:
        """抽象方法 setSquad"""
        pass

    @abstractmethod
    def get_channel(self) -> Any:
        """抽象方法 getChannel"""
        pass

    @abstractmethod
    def get_consume_item_cool_time(self) -> Any:
        """抽象方法 getConsumeItemCoolTime"""
        pass

    @abstractmethod
    def set_consume_item_cool_time(self, ciit: int) -> Any:
        """抽象方法 setConsumeItemCoolTime"""
        pass

    @abstractmethod
    def set_permanent_weather(self, pw: int) -> Any:
        """抽象方法 setPermanentWeather"""
        pass

    @abstractmethod
    def get_permanent_weather(self) -> Any:
        """抽象方法 getPermanentWeather"""
        pass

    @abstractmethod
    def check_states(self, chr: str) -> Any:
        """抽象方法 checkStates"""
        pass

    @abstractmethod
    def set_nodes(self, mn: Any) -> Any:
        """抽象方法 setNodes"""
        pass

    @abstractmethod
    def get_platforms(self) -> Any:
        """抽象方法 getPlatforms"""
        pass

    @abstractmethod
    def get_nodes(self) -> Any:
        """抽象方法 getNodes"""
        pass

    @abstractmethod
    def get_node(self, index: int) -> Any:
        """抽象方法 getNode"""
        pass

    @abstractmethod
    def get_areas(self) -> Any:
        """抽象方法 getAreas"""
        pass

    @abstractmethod
    def get_area(self, index: int) -> Any:
        """抽象方法 getArea"""
        pass

    @abstractmethod
    def change_environment(self, ms: str, type: int) -> Any:
        """抽象方法 changeEnvironment"""
        pass

    @abstractmethod
    def get_environment(self) -> Any:
        """抽象方法 getEnvironment"""
        pass

    @abstractmethod
    def get_num_players_in_area(self, index: int) -> Any:
        """抽象方法 getNumPlayersInArea"""
        pass

    @abstractmethod
    def broadcast_gm_message(self, source: Any, packet: Any, repeatToSource: bool) -> Any:
        """抽象方法 broadcastGMMessage"""
        pass

    @abstractmethod
    def broadcast_gm_message(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> Any:
        """抽象方法 broadcastGMMessage"""
        pass

    @abstractmethod
    def get_mobs_to_spawn(self) -> Any:
        """抽象方法 getMobsToSpawn"""
        pass

    @abstractmethod
    def get_skill_ids(self) -> Any:
        """抽象方法 getSkillIds"""
        pass

    @abstractmethod
    def can_spawn(self) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def can_hurt(self) -> Any:
        """抽象方法 canHurt"""
        pass

    @abstractmethod
    def get_all_unique_monsters(self) -> Any:
        """抽象方法 getAllUniqueMonsters"""
        pass

    @abstractmethod
    def array_list(self) -> Any:
        """抽象方法 ArrayList"""
        pass

    @abstractmethod
    def get_num_players_items_in_area(self, index: int) -> Any:
        """抽象方法 getNumPlayersItemsInArea"""
        pass

    @abstractmethod
    def get_num_players_items_in_rect(self, rect: Any) -> Any:
        """抽象方法 getNumPlayersItemsInRect"""
        pass

    @abstractmethod
    def get_num_players_in_rect(self, rect: Any) -> Any:
        """抽象方法 getNumPlayersInRect"""
        pass

    @abstractmethod
    def has_boat(self) -> Any:
        """抽象方法 hasBoat"""
        pass

    @abstractmethod
    def set_boat(self, hasBoat: bool) -> Any:
        """抽象方法 setBoat"""
        pass

    @abstractmethod
    def set_docked(self, isDocked: bool) -> Any:
        """抽象方法 setDocked"""
        pass

    @abstractmethod
    def spawn_rabbit(self, hp: int) -> Any:
        """抽象方法 spawnRabbit"""
        pass

    @abstractmethod
    def override_monster_stats(self, hp, onemob.getMobMaxMp() -> Any:
        """抽象方法 OverrideMonsterStats"""
        pass

    @abstractmethod
    def point(self, -183, -433) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def kill_fk(self, animate: bool) -> Any:
        """抽象方法 KillFk"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def mob_count(self) -> Any:
        """抽象方法 mobCount"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def player_count(self) -> Any:
        """抽象方法 playerCount"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def kill_monster_2(self, monster: Any) -> Any:
        """抽象方法 killMonster_2"""
        pass

    @abstractmethod
    def reload_cpq(self) -> Any:
        """抽象方法 reloadCPQ"""
        pass

    @abstractmethod
    def get_characters_intersect(self, box: Any) -> Any:
        """抽象方法 getCharactersIntersect"""
        pass

    @abstractmethod
    def array_list(self) -> Any:
        """抽象方法 ArrayList"""
        pass

    @abstractmethod
    def is_pvp_map(self) -> Any:
        """抽象方法 isPvpMap"""
        pass

    @abstractmethod
    def is_party_pvp_map(self) -> Any:
        """抽象方法 isPartyPvpMap"""
        pass

    @abstractmethod
    def is_guild_pvp_map(self) -> Any:
        """抽象方法 isGuildPvpMap"""
        pass

    @abstractmethod
    def is_boss_map(self) -> Any:
        """抽象方法 isBossMap"""
        pass

    @abstractmethod
    def activate_item_reactor(self, mapitem: Any, reactor: Any, c: Any) -> Any:
        """抽象方法 ActivateItemReactor"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def can_spawn(self, p0: Any) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def send_packets(self, p0: Any) -> Any:
        """抽象方法 sendPackets"""
        pass


from abc import ABC, abstractmethod

class DelayedPacketCreation(ABC):
    """接口 DelayedPacketCreation - 从Java接口转换"""

    @abstractmethod
    def maple_map(self, mapid: int, channel: int, returnMapId: int, monsterRate: float) -> Any:
        """抽象方法 MapleMap"""
        pass

    @abstractmethod
    def reentrant_read_write_lock(self) -> Any:
        """抽象方法 ReentrantReadWriteLock"""
        pass

    @abstractmethod
    def reentrant_lock(self) -> Any:
        """抽象方法 ReentrantLock"""
        pass

    @abstractmethod
    def atomic_integer(self, 0) -> Any:
        """抽象方法 AtomicInteger"""
        pass

    @abstractmethod
    def reentrant_read_write_lock(self) -> Any:
        """抽象方法 ReentrantReadWriteLock"""
        pass

    @abstractmethod
    def set_spawns(self, fm: bool) -> Any:
        """抽象方法 setSpawns"""
        pass

    @abstractmethod
    def get_spawns(self) -> Any:
        """抽象方法 getSpawns"""
        pass

    @abstractmethod
    def set_fixed_mob(self, fm: int) -> Any:
        """抽象方法 setFixedMob"""
        pass

    @abstractmethod
    def set_force_move(self, fm: int) -> Any:
        """抽象方法 setForceMove"""
        pass

    @abstractmethod
    def get_force_move(self) -> Any:
        """抽象方法 getForceMove"""
        pass

    @abstractmethod
    def set_level_limit(self, fm: int) -> Any:
        """抽象方法 setLevelLimit"""
        pass

    @abstractmethod
    def get_level_limit(self) -> Any:
        """抽象方法 getLevelLimit"""
        pass

    @abstractmethod
    def set_return_map_id(self, rmi: int) -> Any:
        """抽象方法 setReturnMapId"""
        pass

    @abstractmethod
    def set_soaring(self, b: bool) -> Any:
        """抽象方法 setSoaring"""
        pass

    @abstractmethod
    def can_soar(self) -> Any:
        """抽象方法 canSoar"""
        pass

    @abstractmethod
    def toggle_drops(self) -> Any:
        """抽象方法 toggleDrops"""
        pass

    @abstractmethod
    def set_drops(self, b: bool) -> Any:
        """抽象方法 setDrops"""
        pass

    @abstractmethod
    def toggle_g_drops(self) -> Any:
        """抽象方法 toggleGDrops"""
        pass

    @abstractmethod
    def get_id(self) -> Any:
        """抽象方法 getId"""
        pass

    @abstractmethod
    def get_return_map(self) -> Any:
        """抽象方法 getReturnMap"""
        pass

    @abstractmethod
    def get_return_map_id(self) -> Any:
        """抽象方法 getReturnMapId"""
        pass

    @abstractmethod
    def get_forced_return_id(self) -> Any:
        """抽象方法 getForcedReturnId"""
        pass

    @abstractmethod
    def get_forced_return_map(self) -> Any:
        """抽象方法 getForcedReturnMap"""
        pass

    @abstractmethod
    def set_forced_return_map(self, map: int) -> Any:
        """抽象方法 setForcedReturnMap"""
        pass

    @abstractmethod
    def get_recovery_rate(self) -> Any:
        """抽象方法 getRecoveryRate"""
        pass

    @abstractmethod
    def set_recovery_rate(self, recoveryRate: float) -> Any:
        """抽象方法 setRecoveryRate"""
        pass

    @abstractmethod
    def get_field_limit(self) -> Any:
        """抽象方法 getFieldLimit"""
        pass

    @abstractmethod
    def set_field_limit(self, fieldLimit: int) -> Any:
        """抽象方法 setFieldLimit"""
        pass

    @abstractmethod
    def set_create_mob_interval(self, createMobInterval: int) -> Any:
        """抽象方法 setCreateMobInterval"""
        pass

    @abstractmethod
    def set_time_limit(self, timeLimit: int) -> Any:
        """抽象方法 setTimeLimit"""
        pass

    @abstractmethod
    def set_map_name(self, mapName: str) -> Any:
        """抽象方法 setMapName"""
        pass

    @abstractmethod
    def get_map_name(self) -> Any:
        """抽象方法 getMapName"""
        pass

    @abstractmethod
    def get_street_name(self) -> Any:
        """抽象方法 getStreetName"""
        pass

    @abstractmethod
    def set_first_user_enter(self, onFirstUserEnter: str) -> Any:
        """抽象方法 setFirstUserEnter"""
        pass

    @abstractmethod
    def set_user_enter(self, onUserEnter: str) -> Any:
        """抽象方法 setUserEnter"""
        pass

    @abstractmethod
    def set_on_user_enter(self, onUserEnter: str) -> Any:
        """抽象方法 setOnUserEnter"""
        pass

    @abstractmethod
    def has_clock(self) -> Any:
        """抽象方法 hasClock"""
        pass

    @abstractmethod
    def set_clock(self, hasClock: bool) -> Any:
        """抽象方法 setClock"""
        pass

    @abstractmethod
    def is_town(self) -> Any:
        """抽象方法 isTown"""
        pass

    @abstractmethod
    def set_town(self, town: bool) -> Any:
        """抽象方法 setTown"""
        pass

    @abstractmethod
    def allow_personal_shop(self) -> Any:
        """抽象方法 allowPersonalShop"""
        pass

    @abstractmethod
    def set_personal_shop(self, personalShop: bool) -> Any:
        """抽象方法 setPersonalShop"""
        pass

    @abstractmethod
    def set_street_name(self, streetName: str) -> Any:
        """抽象方法 setStreetName"""
        pass

    @abstractmethod
    def set_everlast(self, everlast: bool) -> Any:
        """抽象方法 setEverlast"""
        pass

    @abstractmethod
    def get_everlast(self) -> Any:
        """抽象方法 getEverlast"""
        pass

    @abstractmethod
    def get_hp_dec(self) -> Any:
        """抽象方法 getHPDec"""
        pass

    @abstractmethod
    def set_hp_dec(self, delta: int) -> Any:
        """抽象方法 setHPDec"""
        pass

    @abstractmethod
    def get_hp_dec_interval(self) -> Any:
        """抽象方法 getHPDecInterval"""
        pass

    @abstractmethod
    def set_hp_dec_interval(self, delta: int) -> Any:
        """抽象方法 setHPDecInterval"""
        pass

    @abstractmethod
    def get_hp_dec_protect(self) -> Any:
        """抽象方法 getHPDecProtect"""
        pass

    @abstractmethod
    def set_hp_dec_protect(self, delta: int) -> Any:
        """抽象方法 setHPDecProtect"""
        pass

    @abstractmethod
    def get_current_party_id(self) -> Any:
        """抽象方法 getCurrentPartyId"""
        pass

    @abstractmethod
    def add_map_object(self, mapobject: Any) -> Any:
        """抽象方法 addMapObject"""
        pass

    @abstractmethod
    def spawn_and_add_ranged_map_object(self, mapobject: Any, packetbakery: Any, condition: Any) -> Any:
        """抽象方法 spawnAndAddRangedMapObject"""
        pass

    @abstractmethod
    def remove_map_object(self, obj: Any) -> Any:
        """抽象方法 removeMapObject"""
        pass

    @abstractmethod
    def calc_point_below(self, initial: Any) -> Any:
        """抽象方法 calcPointBelow"""
        pass

    @abstractmethod
    def point(self, initial.x, dropY) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def calc_drop_pos(self, initial: Any, fallback: Any) -> Any:
        """抽象方法 calcDropPos"""
        pass

    @abstractmethod
    def point(self, initial.x, 50: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def drop_from_monster(self, chr: Any, mob: Any) -> Any:
        """抽象方法 dropFromMonster"""
        pass

    @abstractmethod
    def drop_from_monster(self, chr: Any, mob: Any, instanced: bool) -> Any:
        """抽象方法 dropFromMonster"""
        pass

    @abstractmethod
    def point(self, 0, mob.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def item(self, de.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, de2.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def drop_from_monster2(self, chr: Any, mob: Any) -> Any:
        """抽象方法 dropFromMonster2"""
        pass

    @abstractmethod
    def point(self, 0, mob.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def item(self, de.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, 2370005, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def item(self, de2.itemId, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def remove_monster(self, monster: Any) -> Any:
        """抽象方法 removeMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def kill_monster(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int, lastSkill: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def if(self, 240060201: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 220080001: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000111: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000211: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000411: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000611: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000711: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000803: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 802000821: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 9420544: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 270050100: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 280030000: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 280030001: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8800010: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8800110: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, 8820014: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def get_all_reactor(self) -> Any:
        """抽象方法 getAllReactor"""
        pass

    @abstractmethod
    def get_all_reactors_threadsafe(self) -> Any:
        """抽象方法 getAllReactorsThreadsafe"""
        pass

    @abstractmethod
    def get_all_door(self) -> Any:
        """抽象方法 getAllDoor"""
        pass

    @abstractmethod
    def get_all_doors_threadsafe(self) -> Any:
        """抽象方法 getAllDoorsThreadsafe"""
        pass

    @abstractmethod
    def get_all_merchant(self) -> Any:
        """抽象方法 getAllMerchant"""
        pass

    @abstractmethod
    def get_all_hired_merchants_threadsafe(self) -> Any:
        """抽象方法 getAllHiredMerchantsThreadsafe"""
        pass

    @abstractmethod
    def get_all_monster(self) -> Any:
        """抽象方法 getAllMonster"""
        pass

    @abstractmethod
    def get_all_monsters_threadsafe(self) -> Any:
        """抽象方法 getAllMonstersThreadsafe"""
        pass

    @abstractmethod
    def kill_all_monsters(self, animate: bool) -> Any:
        """抽象方法 killAllMonsters"""
        pass

    @abstractmethod
    def kill_monster(self, monsId: int) -> Any:
        """抽象方法 killMonster"""
        pass

    @abstractmethod
    def map_debug__log(self) -> Any:
        """抽象方法 MapDebug_Log"""
        pass

    @abstractmethod
    def string_builder(self, ": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def limit_reactor(self, rid: int, num: int) -> Any:
        """抽象方法 limitReactor"""
        pass

    @abstractmethod
    def destroy_reactors(self, first: int, last: int) -> Any:
        """抽象方法 destroyReactors"""
        pass

    @abstractmethod
    def destroy_reactor(self, oid: int) -> Any:
        """抽象方法 destroyReactor"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def reload_reactors(self) -> Any:
        """抽象方法 reloadReactors"""
        pass

    @abstractmethod
    def reset_reactors(self) -> Any:
        """抽象方法 resetReactors"""
        pass

    @abstractmethod
    def set_reactor_state(self) -> Any:
        """抽象方法 setReactorState"""
        pass

    @abstractmethod
    def set_reactor_state(self, state: int) -> Any:
        """抽象方法 setReactorState"""
        pass

    @abstractmethod
    def shuffle_reactors(self) -> Any:
        """抽象方法 shuffleReactors"""
        pass

    @abstractmethod
    def shuffle_reactors(self, first: int, last: int) -> Any:
        """抽象方法 shuffleReactors"""
        pass

    @abstractmethod
    def update_monster_controller(self, monster: Any) -> Any:
        """抽象方法 updateMonsterController"""
        pass

    @abstractmethod
    def get_map_object(self, oid: int, type: Any) -> Any:
        """抽象方法 getMapObject"""
        pass

    @abstractmethod
    def contains_npc(self, npcid: int) -> Any:
        """抽象方法 containsNPC"""
        pass

    @abstractmethod
    def get_npc_by_id(self, id: int) -> Any:
        """抽象方法 getNPCById"""
        pass

    @abstractmethod
    def get_monster_by_id(self, id: int) -> Any:
        """抽象方法 getMonsterById"""
        pass

    @abstractmethod
    def count_monster_by_id(self, id: int) -> Any:
        """抽象方法 countMonsterById"""
        pass

    @abstractmethod
    def get_reactor_by_id(self, id: int) -> Any:
        """抽象方法 getReactorById"""
        pass

    @abstractmethod
    def get_monster_by_oid(self, oid: int) -> Any:
        """抽象方法 getMonsterByOid"""
        pass

    @abstractmethod
    def get_npc_by_oid(self, oid: int) -> Any:
        """抽象方法 getNPCByOid"""
        pass

    @abstractmethod
    def get_reactor_by_oid(self, oid: int) -> Any:
        """抽象方法 getReactorByOid"""
        pass

    @abstractmethod
    def get_reactor_by_name(self, name: str) -> Any:
        """抽象方法 getReactorByName"""
        pass

    @abstractmethod
    def spawn_npc(self, id: int, pos: Any) -> Any:
        """抽象方法 spawnNpc"""
        pass

    @abstractmethod
    def remove_npc(self, npcid: int) -> Any:
        """抽象方法 removeNpc"""
        pass

    @abstractmethod
    def spawn_monster_s_sack(self, mob: Any, pos: Any, spawnType: int) -> Any:
        """抽象方法 spawnMonster_sSack"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_monster_on_ground_below(self, mob: Any, pos: Any) -> Any:
        """抽象方法 spawnMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def spawn_monster_s_sack(self, mob: Any, pos: Any, spawnType: int, hp: int) -> Any:
        """抽象方法 spawnMonster_sSack"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_monster_on_ground_below(self, mob: Any, pos: Any, hp: int) -> Any:
        """抽象方法 spawnMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def spawn_monster_with_effect_below(self, mob: Any, pos: Any, effect: int) -> Any:
        """抽象方法 spawnMonsterWithEffectBelow"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_zakum(self, x: int, y: int) -> Any:
        """抽象方法 spawnZakum"""
        pass

    @abstractmethod
    def point(self, x, y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def get_all_mists_threadsafe(self) -> Any:
        """抽象方法 getAllMistsThreadsafe"""
        pass

    @abstractmethod
    def spawn_fake_monster_on_ground_below(self, mob: Any, pos: Any) -> Any:
        """抽象方法 spawnFakeMonsterOnGroundBelow"""
        pass

    @abstractmethod
    def point(self, pos.x, 1: Any) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def get_mobs_size(self) -> Any:
        """抽象方法 getMobsSize"""
        pass

    @abstractmethod
    def check_remove_after(self, monster: Any) -> Any:
        """抽象方法 checkRemoveAfter"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def spawn_revives(self, monster: Any, oid: int) -> Any:
        """抽象方法 spawnRevives"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_monster(self, monster: Any, spawnType: int) -> Any:
        """抽象方法 spawnMonster"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_monster_with_effect(self, monster: Any, effect: int, pos: Any) -> Any:
        """抽象方法 spawnMonsterWithEffect"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_fake_monster(self, monster: Any) -> Any:
        """抽象方法 spawnFakeMonster"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_reactor(self, reactor: Any) -> Any:
        """抽象方法 spawnReactor"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def respawn_reactor(self, reactor: Any) -> Any:
        """抽象方法 respawnReactor"""
        pass

    @abstractmethod
    def spawn_door(self, door: Any) -> Any:
        """抽象方法 spawnDoor"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def maple_party_character(self, c.getPlayer() -> Any:
        """抽象方法 MaplePartyCharacter"""
        pass

    @abstractmethod
    def spawn_condition(self) -> Any:
        """抽象方法 SpawnCondition"""
        pass

    @abstractmethod
    def can_spawn(self, chr: Any) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def spawn_summon(self, summon: Any) -> Any:
        """抽象方法 spawnSummon"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_dragon(self, summon: Any) -> Any:
        """抽象方法 spawnDragon"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mist(self, mist: Any, duration: int, fake: bool) -> Any:
        """抽象方法 spawnMist"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def monster_status_effect(self, MonsterStatus.中毒, Integer.valueOf(1) -> Any:
        """抽象方法 MonsterStatusEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def disappearing_item_drop(self, dropper: Any, owner: Any, item: Any, pos: Any) -> Any:
        """抽象方法 disappearingItemDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, item, droppos, dropper, owner, (byte) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def spawn_meso_drop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> Any:
        """抽象方法 spawnMesoDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, meso, droppos, dropper, owner, droptype, playerDrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mob_meso_drop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> Any:
        """抽象方法 spawnMobMesoDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, meso, position, dropper, owner, droptype, playerDrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_mob_drop(self, idrop: Any, dropPos: Any, mob: Any, chr: Any, droptype: int, questid: int) -> Any:
        """抽象方法 spawnMobDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, idrop, dropPos, mob, chr, droptype, false, questid) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_rand_drop(self) -> Any:
        """抽象方法 spawnRandDrop"""
        pass

    @abstractmethod
    def spawn_auto_drop(self, itemid: int, pos: Any) -> Any:
        """抽象方法 spawnAutoDrop"""
        pass

    @abstractmethod
    def item(self, itemid, (short) -> Any:
        """抽象方法 Item"""
        pass

    @abstractmethod
    def maple_map_item(self, pos, idrop) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def spawn_item_drop(self, dropper: Any, owner: Any, item: Any, pos: Any, ffaDrop: bool, playerDrop: bool) -> Any:
        """抽象方法 spawnItemDrop"""
        pass

    @abstractmethod
    def maple_map_item(self, item, droppos, dropper, owner, (byte) -> Any:
        """抽象方法 MapleMapItem"""
        pass

    @abstractmethod
    def send_packets(self, c: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

    @abstractmethod
    def activate_item_reactors(self, drop: Any, c: Any) -> Any:
        """抽象方法 activateItemReactors"""
        pass

    @abstractmethod
    def activate_item_reactor(self, drop, react, c) -> Any:
        """抽象方法 ActivateItemReactor"""
        pass

    @abstractmethod
    def get_items_size(self) -> Any:
        """抽象方法 getItemsSize"""
        pass

    @abstractmethod
    def get_all_items(self) -> Any:
        """抽象方法 getAllItems"""
        pass

    @abstractmethod
    def get_all_items_threadsafe(self) -> Any:
        """抽象方法 getAllItemsThreadsafe"""
        pass

    @abstractmethod
    def return_ever_last_item(self, chr: Any) -> Any:
        """抽象方法 returnEverLastItem"""
        pass

    @abstractmethod
    def talk_monster(self, msg: str, itemId: int, objectid: int) -> Any:
        """抽象方法 talkMonster"""
        pass

    @abstractmethod
    def start_map_effect(self, msg: str, itemId: int) -> Any:
        """抽象方法 startMapEffect"""
        pass

    @abstractmethod
    def start_map_effect(self, msg: str, itemId: int, jukebox: bool) -> Any:
        """抽象方法 startMapEffect"""
        pass

    @abstractmethod
    def maple_map_effect(self, msg, itemId) -> Any:
        """抽象方法 MapleMapEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def start_extended_map_effect(self, msg: str, itemId: int) -> Any:
        """抽象方法 startExtendedMapEffect"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def start_jukebox(self, msg: str, itemId: int) -> Any:
        """抽象方法 startJukebox"""
        pass

    @abstractmethod
    def add_player(self, chr: Any) -> Any:
        """抽象方法 addPlayer"""
        pass

    @abstractmethod
    def get_num_items(self) -> Any:
        """抽象方法 getNumItems"""
        pass

    @abstractmethod
    def has_forced_equip(self) -> Any:
        """抽象方法 hasForcedEquip"""
        pass

    @abstractmethod
    def set_field_type(self, fieldType: int) -> Any:
        """抽象方法 setFieldType"""
        pass

    @abstractmethod
    def get_num_monsters(self) -> Any:
        """抽象方法 getNumMonsters"""
        pass

    @abstractmethod
    def do_shrine(self, spawned: bool) -> Any:
        """抽象方法 doShrine"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def get_squad_by_map(self) -> Any:
        """抽象方法 getSquadByMap"""
        pass

    @abstractmethod
    def get_squad_begin(self) -> Any:
        """抽象方法 getSquadBegin"""
        pass

    @abstractmethod
    def get_em_by_map(self) -> Any:
        """抽象方法 getEMByMap"""
        pass

    @abstractmethod
    def remove_player(self, chr: Any) -> Any:
        """抽象方法 removePlayer"""
        pass

    @abstractmethod
    def get_all_players(self) -> Any:
        """抽象方法 getAllPlayers"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def broadcast_message(self, packet: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, repeatToSource: bool) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, packet: Any, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def broadcast_message(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> Any:
        """抽象方法 broadcastMessage"""
        pass

    @abstractmethod
    def send_object_placement(self, chr: Any) -> Any:
        """抽象方法 sendObjectPlacement"""
        pass

    @abstractmethod
    def get_map_objects_in_range(self, from: Any, rangeSq: float) -> Any:
        """抽象方法 getMapObjectsInRange"""
        pass

    @abstractmethod
    def get_items_in_range(self, from: Any, rangeSq: float) -> Any:
        """抽象方法 getItemsInRange"""
        pass

    @abstractmethod
    def get_map_objects_in_range(self, from: Any, rangeSq: float, MapObject_types: list) -> Any:
        """抽象方法 getMapObjectsInRange"""
        pass

    @abstractmethod
    def get_map_objects_in_rect(self, box: Any, MapObject_types: list) -> Any:
        """抽象方法 getMapObjectsInRect"""
        pass

    @abstractmethod
    def get_players_in_rect_and_in_list(self, box: Any, chrList: list) -> Any:
        """抽象方法 getPlayersInRectAndInList"""
        pass

    @abstractmethod
    def add_portal(self, myPortal: Any) -> Any:
        """抽象方法 addPortal"""
        pass

    @abstractmethod
    def get_portal(self, portalname: str) -> Any:
        """抽象方法 getPortal"""
        pass

    @abstractmethod
    def get_portal(self, portalid: int) -> Any:
        """抽象方法 getPortal"""
        pass

    @abstractmethod
    def reset_portals(self) -> Any:
        """抽象方法 resetPortals"""
        pass

    @abstractmethod
    def set_footholds(self, footholds: Any) -> Any:
        """抽象方法 setFootholds"""
        pass

    @abstractmethod
    def get_footholds(self) -> Any:
        """抽象方法 getFootholds"""
        pass

    @abstractmethod
    def load_monster_rate(self, first: bool) -> Any:
        """抽象方法 loadMonsterRate"""
        pass

    @abstractmethod
    def if(self, spawnSize: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def add_monster_spawn(self, monster: Any, mobTime: int, carnivalTeam: int, msg: str) -> Any:
        """抽象方法 addMonsterSpawn"""
        pass

    @abstractmethod
    def spawn_point(self, monster, newpos, mobTime, carnivalTeam, msg) -> Any:
        """抽象方法 SpawnPoint"""
        pass

    @abstractmethod
    def add_area_monster_spawn(self, monster: Any, pos1: Any, pos2: Any, pos3: Any, mobTime: int, msg: str) -> Any:
        """抽象方法 addAreaMonsterSpawn"""
        pass

    @abstractmethod
    def point(self, pos1) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos1) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def if(self, null: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def point(self, pos2) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos2) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def if(self, null: Any) -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def point(self, pos3) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, pos3) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def spawn_point_area_boss(self, monster, pos1, pos2, pos3, mobTime, msg) -> Any:
        """抽象方法 SpawnPointAreaBoss"""
        pass

    @abstractmethod
    def get_characters(self) -> Any:
        """抽象方法 getCharacters"""
        pass

    @abstractmethod
    def get_characters_threadsafe(self) -> Any:
        """抽象方法 getCharactersThreadsafe"""
        pass

    @abstractmethod
    def get_character_by_id__in_map(self, id: int) -> Any:
        """抽象方法 getCharacterById_InMap"""
        pass

    @abstractmethod
    def get_character_by_id(self, id: int) -> Any:
        """抽象方法 getCharacterById"""
        pass

    @abstractmethod
    def update_map_object_visibility(self, chr: Any, mo: Any) -> Any:
        """抽象方法 updateMapObjectVisibility"""
        pass

    @abstractmethod
    def if(self, mo.getType() -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def if(self, mo.getType() -> Any:
        """抽象方法 if"""
        pass

    @abstractmethod
    def move_monster(self, monster: Any, reportedPos: Any) -> Any:
        """抽象方法 moveMonster"""
        pass

    @abstractmethod
    def move_player(self, player: Any, newPosition: Any) -> Any:
        """抽象方法 movePlayer"""
        pass

    @abstractmethod
    def find_closest_spawnpoint(self, from: Any) -> Any:
        """抽象方法 findClosestSpawnpoint"""
        pass

    @abstractmethod
    def spawn_debug(self) -> Any:
        """抽象方法 spawnDebug"""
        pass

    @abstractmethod
    def string_builder(self, ": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def character_size(self) -> Any:
        """抽象方法 characterSize"""
        pass

    @abstractmethod
    def get_map_object_size(self) -> Any:
        """抽象方法 getMapObjectSize"""
        pass

    @abstractmethod
    def get_characters_size(self) -> Any:
        """抽象方法 getCharactersSize"""
        pass

    @abstractmethod
    def get_portals(self) -> Any:
        """抽象方法 getPortals"""
        pass

    @abstractmethod
    def get_spawned_monsters_on_map(self) -> Any:
        """抽象方法 getSpawnedMonstersOnMap"""
        pass

    @abstractmethod
    def spawn_love(self, love: Any) -> Any:
        """抽象方法 spawnLove"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def auto_nx(self, dy: int) -> Any:
        """抽象方法 AutoNx"""
        pass

    @abstractmethod
    def get_character_by_name(self, id: str) -> Any:
        """抽象方法 getCharacterByName"""
        pass

    @abstractmethod
    def hide_npc(self, npcid: int) -> Any:
        """抽象方法 hideNpc"""
        pass

    @abstractmethod
    def respawn(self, force: bool) -> Any:
        """抽象方法 respawn"""
        pass

    @abstractmethod
    def get_max_regular_spawn(self) -> Any:
        """抽象方法 getMaxRegularSpawn"""
        pass

    @abstractmethod
    def get_snowball_portal(self) -> Any:
        """抽象方法 getSnowballPortal"""
        pass

    @abstractmethod
    def is_disconnected(self, id: int) -> Any:
        """抽象方法 isDisconnected"""
        pass

    @abstractmethod
    def add_disconnected(self, id: int) -> Any:
        """抽象方法 addDisconnected"""
        pass

    @abstractmethod
    def reset_disconnected(self) -> Any:
        """抽象方法 resetDisconnected"""
        pass

    @abstractmethod
    def start_speed_run(self) -> Any:
        """抽象方法 startSpeedRun"""
        pass

    @abstractmethod
    def start_speed_run(self, leader: str) -> Any:
        """抽象方法 startSpeedRun"""
        pass

    @abstractmethod
    def end_speed_run(self) -> Any:
        """抽象方法 endSpeedRun"""
        pass

    @abstractmethod
    def get_rank_and_add(self, leader: str, time: str, type: Any, timz: int, squad: list) -> Any:
        """抽象方法 getRankAndAdd"""
        pass

    @abstractmethod
    def string_builder(self) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def speedruns(self, `type`, `leader`, `timestring`, `time`, `members`) -> Any:
        """抽象方法 speedruns"""
        pass

    @abstractmethod
    def string_builder(self, ".#k\r\n\r\n": Any) -> Any:
        """抽象方法 StringBuilder"""
        pass

    @abstractmethod
    def get_speed_run_start(self) -> Any:
        """抽象方法 getSpeedRunStart"""
        pass

    @abstractmethod
    def disconnect_all(self) -> Any:
        """抽象方法 disconnectAll"""
        pass

    @abstractmethod
    def get_all_np_cs(self) -> Any:
        """抽象方法 getAllNPCs"""
        pass

    @abstractmethod
    def get_all_np_cs_threadsafe(self) -> Any:
        """抽象方法 getAllNPCsThreadsafe"""
        pass

    @abstractmethod
    def reset_np_cs(self) -> Any:
        """抽象方法 resetNPCs"""
        pass

    @abstractmethod
    def reset_fully(self) -> Any:
        """抽象方法 resetFully"""
        pass

    @abstractmethod
    def reset_fully(self, respawn: bool) -> Any:
        """抽象方法 resetFully"""
        pass

    @abstractmethod
    def cancel_squad_schedule(self) -> Any:
        """抽象方法 cancelSquadSchedule"""
        pass

    @abstractmethod
    def remove_drops(self) -> Any:
        """抽象方法 removeDrops"""
        pass

    @abstractmethod
    def remove_drops_delay(self) -> Any:
        """抽象方法 removeDropsDelay"""
        pass

    @abstractmethod
    def reset_all_spawn_point(self, mobid: int, mobTime: int) -> Any:
        """抽象方法 resetAllSpawnPoint"""
        pass

    @abstractmethod
    def point(self, oldMons.getPosition() -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def reset_spawns(self) -> Any:
        """抽象方法 resetSpawns"""
        pass

    @abstractmethod
    def make_carnival_spawn(self, team: int, newMons: Any, num: int) -> Any:
        """抽象方法 makeCarnivalSpawn"""
        pass

    @abstractmethod
    def point(self, mp.x, mp.y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def point(self, ret.x, ret.y) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def make_carnival_reactor(self, team: int, num: int) -> Any:
        """抽象方法 makeCarnivalReactor"""
        pass

    @abstractmethod
    def maple_reactor(self, stats, team: Any) -> Any:
        """抽象方法 MapleReactor"""
        pass

    @abstractmethod
    def block_all_portal(self) -> Any:
        """抽象方法 blockAllPortal"""
        pass

    @abstractmethod
    def get_and_switch_team(self) -> Any:
        """抽象方法 getAndSwitchTeam"""
        pass

    @abstractmethod
    def set_squad(self, s: Any) -> Any:
        """抽象方法 setSquad"""
        pass

    @abstractmethod
    def get_channel(self) -> Any:
        """抽象方法 getChannel"""
        pass

    @abstractmethod
    def get_consume_item_cool_time(self) -> Any:
        """抽象方法 getConsumeItemCoolTime"""
        pass

    @abstractmethod
    def set_consume_item_cool_time(self, ciit: int) -> Any:
        """抽象方法 setConsumeItemCoolTime"""
        pass

    @abstractmethod
    def set_permanent_weather(self, pw: int) -> Any:
        """抽象方法 setPermanentWeather"""
        pass

    @abstractmethod
    def get_permanent_weather(self) -> Any:
        """抽象方法 getPermanentWeather"""
        pass

    @abstractmethod
    def check_states(self, chr: str) -> Any:
        """抽象方法 checkStates"""
        pass

    @abstractmethod
    def set_nodes(self, mn: Any) -> Any:
        """抽象方法 setNodes"""
        pass

    @abstractmethod
    def get_platforms(self) -> Any:
        """抽象方法 getPlatforms"""
        pass

    @abstractmethod
    def get_nodes(self) -> Any:
        """抽象方法 getNodes"""
        pass

    @abstractmethod
    def get_node(self, index: int) -> Any:
        """抽象方法 getNode"""
        pass

    @abstractmethod
    def get_areas(self) -> Any:
        """抽象方法 getAreas"""
        pass

    @abstractmethod
    def get_area(self, index: int) -> Any:
        """抽象方法 getArea"""
        pass

    @abstractmethod
    def change_environment(self, ms: str, type: int) -> Any:
        """抽象方法 changeEnvironment"""
        pass

    @abstractmethod
    def get_environment(self) -> Any:
        """抽象方法 getEnvironment"""
        pass

    @abstractmethod
    def get_num_players_in_area(self, index: int) -> Any:
        """抽象方法 getNumPlayersInArea"""
        pass

    @abstractmethod
    def broadcast_gm_message(self, source: Any, packet: Any, repeatToSource: bool) -> Any:
        """抽象方法 broadcastGMMessage"""
        pass

    @abstractmethod
    def broadcast_gm_message(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> Any:
        """抽象方法 broadcastGMMessage"""
        pass

    @abstractmethod
    def get_mobs_to_spawn(self) -> Any:
        """抽象方法 getMobsToSpawn"""
        pass

    @abstractmethod
    def get_skill_ids(self) -> Any:
        """抽象方法 getSkillIds"""
        pass

    @abstractmethod
    def can_spawn(self) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def can_hurt(self) -> Any:
        """抽象方法 canHurt"""
        pass

    @abstractmethod
    def get_all_unique_monsters(self) -> Any:
        """抽象方法 getAllUniqueMonsters"""
        pass

    @abstractmethod
    def array_list(self) -> Any:
        """抽象方法 ArrayList"""
        pass

    @abstractmethod
    def get_num_players_items_in_area(self, index: int) -> Any:
        """抽象方法 getNumPlayersItemsInArea"""
        pass

    @abstractmethod
    def get_num_players_items_in_rect(self, rect: Any) -> Any:
        """抽象方法 getNumPlayersItemsInRect"""
        pass

    @abstractmethod
    def get_num_players_in_rect(self, rect: Any) -> Any:
        """抽象方法 getNumPlayersInRect"""
        pass

    @abstractmethod
    def has_boat(self) -> Any:
        """抽象方法 hasBoat"""
        pass

    @abstractmethod
    def set_boat(self, hasBoat: bool) -> Any:
        """抽象方法 setBoat"""
        pass

    @abstractmethod
    def set_docked(self, isDocked: bool) -> Any:
        """抽象方法 setDocked"""
        pass

    @abstractmethod
    def spawn_rabbit(self, hp: int) -> Any:
        """抽象方法 spawnRabbit"""
        pass

    @abstractmethod
    def override_monster_stats(self, hp, onemob.getMobMaxMp() -> Any:
        """抽象方法 OverrideMonsterStats"""
        pass

    @abstractmethod
    def point(self, -183, -433) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def kill_fk(self, animate: bool) -> Any:
        """抽象方法 KillFk"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def mob_count(self) -> Any:
        """抽象方法 mobCount"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def player_count(self) -> Any:
        """抽象方法 playerCount"""
        pass

    @abstractmethod
    def point(self, 0, 0) -> Any:
        """抽象方法 Point"""
        pass

    @abstractmethod
    def kill_monster_2(self, monster: Any) -> Any:
        """抽象方法 killMonster_2"""
        pass

    @abstractmethod
    def reload_cpq(self) -> Any:
        """抽象方法 reloadCPQ"""
        pass

    @abstractmethod
    def get_characters_intersect(self, box: Any) -> Any:
        """抽象方法 getCharactersIntersect"""
        pass

    @abstractmethod
    def array_list(self) -> Any:
        """抽象方法 ArrayList"""
        pass

    @abstractmethod
    def is_pvp_map(self) -> Any:
        """抽象方法 isPvpMap"""
        pass

    @abstractmethod
    def is_party_pvp_map(self) -> Any:
        """抽象方法 isPartyPvpMap"""
        pass

    @abstractmethod
    def is_guild_pvp_map(self) -> Any:
        """抽象方法 isGuildPvpMap"""
        pass

    @abstractmethod
    def is_boss_map(self) -> Any:
        """抽象方法 isBossMap"""
        pass

    @abstractmethod
    def activate_item_reactor(self, mapitem: Any, reactor: Any, c: Any) -> Any:
        """抽象方法 ActivateItemReactor"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def runnable(self) -> Any:
        """抽象方法 Runnable"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """抽象方法 run"""
        pass

    @abstractmethod
    def can_spawn(self, p0: Any) -> Any:
        """抽象方法 canSpawn"""
        pass

    @abstractmethod
    def send_packets(self, p0: Any) -> Any:
        """抽象方法 sendPackets"""
        pass

