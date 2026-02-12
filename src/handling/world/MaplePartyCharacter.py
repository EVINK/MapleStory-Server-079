"""
MaplePartyCharacter - 从Java源文件转换而来
对应Java源文件: handling/world/MaplePartyCharacter.java
包路径: handling.world
"""

from dataclasses import dataclass
from typing import List
from typing import Optional, List, Dict, Any, Set

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类
# from server.maps.MapleDoor import *  # TODO: 根据实际需要导入具体类


class MaplePartyCharacter:
    """
    类 MaplePartyCharacter - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, maplechar: Any):
        """初始化 MaplePartyCharacter"""
        self.name = ""
        self.id = 0
        self.level = 0
        self.channel = 0
        self.jobid = 0
        self.mapid = 0
        self.doorTown = 0
        self.doorTarget = 0
        self.doorSkill = 0
        self.doorPosition = None
        self.online = False


    def getLevel(self) -> int:
        """方法 getLevel"""
        return getattr(self, 'level', 0)

    def getChannel(self) -> int:
        """方法 getChannel"""
        return getattr(self, 'channel', 0)

    def isOnline(self) -> bool:
        """方法 isOnline"""
        return bool(getattr(self, 'online', False))

    def setOnline(self, online: bool) -> None:
        """方法 setOnline"""
        self.online = online
        return None

    def getMapid(self) -> int:
        """方法 getMapid"""
        return getattr(self, 'mapid', 0)

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def getJobId(self) -> int:
        """方法 getJobId"""
        return getattr(self, 'job_id', 0)

    def getDoorTown(self) -> int:
        """方法 getDoorTown"""
        return getattr(self, 'door_town', 0)

    def getDoorTarget(self) -> int:
        """方法 getDoorTarget"""
        return getattr(self, 'door_target', 0)

    def getDoorSkill(self) -> int:
        """方法 getDoorSkill"""
        return getattr(self, 'door_skill', 0)

    def getDoorPosition(self) -> Any:
        """方法 getDoorPosition"""
        return getattr(self, 'door_position', None)

    def hashCode(self) -> int:
        """方法 hashCode"""
        return hash(self)

    def equals(self, obj: Any) -> bool:
        """方法 equals"""
        return self is obj or getattr(self, '__eq__', lambda o: False)(obj)

