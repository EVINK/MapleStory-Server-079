"""
PetDataFactory - Converted from Java source
Original: client/inventory/PetDataFactory.java
Package: client.inventory
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


class PetDataFactory:
    """
    Class PetDataFactory
    """

    dataRoot = MapleDataProviderFactory.getDataProvider(new File(System.getProperty("wzPath") + "/Item.wz"))
    petCommands = {}
    petHunger = {}


    @staticmethod
    def getPetCommand(petId: int, skillId: int) -> Any:
        ret = petCommands.get(Pair(Integer.valueOf(petId), Integer.valueOf(skillId)))
        if ret is not None:
        return ret
        skillData = dataRoot.getData("Pet/" + petId + ".img")
        prob = 0
        inc = 0
        if skillData is not None:
            prob = MapleDataTool.getInt("interact/" + skillId + "/prob", skillData, 0)
            inc = MapleDataTool.getInt("interact/" + skillId + "/inc", skillData, 0)
        ret = PetCommand(petId, skillId, prob, inc)
        petCommands.put(Pair(Integer.valueOf(petId), Integer.valueOf(skillId)), ret)
        return ret

    def getHunger(self, petId: int) -> int:
        ret = petHunger.get(Integer.valueOf(petId))
        if ret is not None:
        return ret
        hungerData = dataRoot.getData("Pet/" + petId + ".img").getChildByPath("info/hungry")
        ret = Integer.valueOf(MapleDataTool.getInt(hungerData, 1))
        petHunger.put(Integer.valueOf(petId), ret)
        return ret

