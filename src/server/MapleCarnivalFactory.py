"""
MapleCarnivalFactory - Converted from Java source
Original: server/MapleCarnivalFactory.java
Package: server
"""

from pathlib import Path
from typing import Dict
from typing import Optional, Any
import os
import sys

# Internal module imports
# from client.MapleDisease import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes


class MapleCarnivalFactory:
    """
    Class MapleCarnivalFactory
    """

    def __init__(self):
        self.skills = None
        self.guardians = None
        self.dataRoot = None
        self.cpLoss = 0
        self.skillid = 0
        self.level = 0
        self.targetsAll = False
        self.skills = {}
        self.guardians = {}
        self.dataRoot = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Skill.wz"))
        self.initialize()

    # Static initializer
    # instance = MapleCarnivalFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        if self.skills != 0:
            return
        for z in self.dataRoot.getData("MCSkill.img"):
            self.skills.put(int(z.getName()), MCSkill(MapleDataTool.getInt("spendCP", z, 0), MapleDataTool.getInt("mobSkillID", z, 0), MapleDataTool.getInt("level", z, 0), MapleDataTool.getInt("target", z, 1) > 1))
        for z in self.dataRoot.getData("MCGuardian.img"):
            self.guardians.put(int(z.getName()), MCSkill(MapleDataTool.getInt("spendCP", z, 0), MapleDataTool.getInt("mobSkillID", z, 0), MapleDataTool.getInt("level", z, 0), True))

    def getSkill(self, id: int) -> Any:
        return self.skills.get(id)

    def getGuardian(self, id: int) -> Any:
        return self.guardians.get(id)

    def getDisease(self) -> Any:
        if self.skillid <= 0:
            return MapleDisease.getRandom()
        return MapleDisease.getBySkill(self.skillid)


# Inner class from Java (originally nested)
class MCSkill:
    """
    Class MCSkill
    """

    def __init__(self, _cpLoss: int, _skillid: int, _level: int, _targetsAll: bool):
        self.cpLoss = 0
        self.skillid = 0
        self.level = 0
        self.targetsAll = False
        self.cpLoss = _cpLoss
        self.skillid = _skillid
        self.level = _level
        self.targetsAll = _targetsAll


    def getSkill(self) -> Any:
        return MobSkillFactory.getMobSkill(self.skillid, 1)

    def getDisease(self) -> Any:
        if self.skillid <= 0:
            return MapleDisease.getRandom()
        return MapleDisease.getBySkill(self.skillid)

