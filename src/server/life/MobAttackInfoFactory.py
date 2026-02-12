"""
MobAttackInfoFactory - Converted from Java source
Original: server/life/MobAttackInfoFactory.java
Package: server.life
"""

from pathlib import Path
from typing import Dict
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class MobAttackInfoFactory:
    """
    Class MobAttackInfoFactory
    """

    # Static initializer
    # instance = MobAttackInfoFactory()
    # dataSource = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Mob.wz"))
    # mobAttacks = new HashMap<Pair<Integer, Integer>, MobAttackInfo>()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getMobAttackInfo(self, mob: Any, attack: int) -> Any:
        ret = MobAttackInfoFactory.mobAttacks.get(Pair(mob.getId(), attack))
        if ret is not None:
            return ret
        mobData = MobAttackInfoFactory.dataSource.getData(StringUtil.getLeftPaddedStr(Integer.toString(mob.getId()) + ".img", '0', 11))
        if mobData is not None:
            infoData = mobData.getChildByPath("info/link")
            if infoData is not None:
                linkedmob = MapleDataTool.getString("info/link", mobData)
                mobData = MobAttackInfoFactory.dataSource.getData(StringUtil.getLeftPaddedStr(linkedmob + ".img", '0', 11))
            attackData = mobData.getChildByPath("attack" + (attack + 1) + "/info")
            if attackData is not None:
                ret = MobAttackInfo()
                ret.setDeadlyAttack(attackData.getChildByPath("deadlyAttack") is not None)
                ret.setMpBurn(MapleDataTool.getInt("mpBurn", attackData, 0))
                ret.setDiseaseSkill(MapleDataTool.getInt("disease", attackData, 0))
                ret.setDiseaseLevel(MapleDataTool.getInt("level", attackData, 0))
                ret.setMpCon(MapleDataTool.getInt("conMP", attackData, 0))
        MobAttackInfoFactory.mobAttacks.put(new Pair<Integer, Integer>(mob.getId(), attack), ret)
        return ret

