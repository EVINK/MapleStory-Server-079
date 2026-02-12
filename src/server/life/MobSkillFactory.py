"""
MobSkillFactory - Converted from Java source
Original: server/life/MobSkillFactory.java
Package: server.life
"""

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MobSkillFactory:
    """
    Class MobSkillFactory
    """

    # Static initializer
    # mobSkills = new HashMap<Pair<Integer, Integer>, MobSkill>()
    # dataSource = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Skill.wz"))
    # skillRoot = MobSkillFactory.dataSource.getData("MobSkill.img")


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getMobSkill(self, skillId: int, level: int) -> Any:
        ret = MobSkillFactory.mobSkills.get(Pair(skillId, level))
        if ret is not None:
            return ret
        if MobSkillFactory.skillRoot is None || MobSkillFactory.skillRoot.getChildren() is None || MobSkillFactory.skillRoot.getChildByPath(str(skillId)) is None || MobSkillFactory.skillRoot.getChildByPath(str(skillId)).getChildren() is None || MobSkillFactory.skillRoot.getChildByPath(str(skillId)).getChildByPath("level") is None:
            return None
        skillData = MobSkillFactory.skillRoot.getChildByPath(skillId + "/level/" + level)
        if skillData is not None && skillData.getChildren() is not None:
            toSummon = []
            i = 0
            while i > -1 && skillData.getChildByPath(str(i)) is not None:
                toSummon.add(MapleDataTool.getInt(skillData.getChildByPath(str(i)), 0))
            ltd = skillData.getChildByPath("lt")
            lt = None
            rb = None
            if ltd is not None:
                lt = ltd.getData()
                rb = skillData.getChildByPath("rb").getData()
            ret = MobSkill(skillId, level)
            ret.addSummons(toSummon)
            ret.setCoolTime(MapleDataTool.getInt("interval", skillData, 0) * 1000)
            ret.setDuration(MapleDataTool.getInt("time", skillData, 1) * 1000)
            ret.setHp(MapleDataTool.getInt("hp", skillData, 100))
            ret.setMpCon(MapleDataTool.getInt(skillData.getChildByPath("mpCon"), 0))
            ret.setSpawnEffect(MapleDataTool.getInt("summonEffect", skillData, 0))
            ret.setX(MapleDataTool.getInt("x", skillData, 1))
            ret.setY(MapleDataTool.getInt("y", skillData, 1))
            ret.setProp(MapleDataTool.getInt("prop", skillData, 100) / 100.0)
            ret.setLimit(MapleDataTool.getInt("limit", skillData, 0))
            ret.setLtRb(lt, rb)
            MobSkillFactory.mobSkills.put(new Pair<Integer, Integer>(skillId, level), ret)
        return ret


# Inner class from Java (originally nested)
class SingletonHolder:
    """
    Class SingletonHolder
    """

    # Static initializer
    # instance = MobSkillFactory()

    pass

