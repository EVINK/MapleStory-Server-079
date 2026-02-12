"""
PlayerBuffStorage - Converted from Java source
Original: handling/world/PlayerBuffStorage.java
Package: handling.world
"""

from threading import Lock
from typing import Dict
from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCoolDownValueHolder import *  # TODO: import specific classes
# from client.MapleDiseaseValueHolder import *  # TODO: import specific classes


class PlayerBuffStorage:
    """
    Class PlayerBuffStorage
    Implements: Serializable
    """

    # Static initializer
    # buffs = new ConcurrentHashMap<Integer, List<PlayerBuffValueHolder>>()
    # coolDowns = new ConcurrentHashMap<Integer, List<MapleCoolDownValueHolder>>()
    # diseases = new ConcurrentHashMap<Integer, List<MapleDiseaseValueHolder>>()


    @staticmethod
    def addBuffsToStorage(chrid: int, toStore: list) -> None:
        PlayerBuffStorage.buffs.put(chrid, toStore)

    def addCooldownsToStorage(self, chrid: int, toStore: list) -> None:
        PlayerBuffStorage.coolDowns.put(chrid, toStore)

    def addDiseaseToStorage(self, chrid: int, toStore: list) -> None:
        PlayerBuffStorage.diseases.put(chrid, toStore)

    def getBuffsFromStorage(self, chrid: int) -> list:
        return PlayerBuffStorage.buffs.remove(chrid)

    def getCooldownsFromStorage(self, chrid: int) -> list:
        return PlayerBuffStorage.coolDowns.remove(chrid)

    def getDiseaseFromStorage(self, chrid: int) -> list:
        return PlayerBuffStorage.diseases.remove(chrid)

