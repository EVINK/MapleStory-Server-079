"""
ItemMakerFactory - Converted from Java source
Original: server/ItemMakerFactory.java
Package: server
"""

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class ItemMakerFactory:
    """
    Class ItemMakerFactory
    """

    def __init__(self):
        self.createCache = {}
        self.gemCache = {}
        self.reqLevel = None
        self.reqMakerLevel = None
        self.cost = None
        self.quantity = None
        self.randomReward = None
        self.reqRecipe = None
        self.reqLevel = None
        self.cost = None
        self.quantity = None
        self.stimulator = None
        self.tuc = None
        self.reqMakerLevel = None
        self.reqItems = None
        self.reqEquips = None
        self.createCache = {}
        self.gemCache = {}
        info = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz")).getData("ItemMake.img")
        for dataType in info.getChildren():
            type = int(dataType.getName())
            # switch (type):
                # case 0:
                    for itemFolder in dataType.getChildren():
                        reqLevel = MapleDataTool.getInt("reqLevel", itemFolder, 0)
                        reqMakerLevel = MapleDataTool.getInt("reqSkillLevel", itemFolder, 0)
                        cost = MapleDataTool.getInt("meso", itemFolder, 0)
                        quantity = MapleDataTool.getInt("itemNum", itemFolder, 0)
                        ret = GemCreateEntry(cost, reqLevel, reqMakerLevel, quantity)
                        for rewardNRecipe in itemFolder.getChildren():
                            for ind in rewardNRecipe.getChildren():
                                if rewardNRecipe.getName() == ("randomReward"):
                                    ret.addRandomReward(MapleDataTool.getInt("item", ind, 0), MapleDataTool.getInt("prob", ind, 0))
                                else:
                                    if !rewardNRecipe.getName() == ("recipe"):
                                        continue
                                    ret.addReqRecipe(MapleDataTool.getInt("item", ind, 0), MapleDataTool.getInt("count", ind, 0))
                        self.gemCache.put(int(itemFolder.getName()), ret)
                    continue
                # case 1:
                # case 2:
                # case 4:
                # case 8:
                # case 16:
                    for itemFolder in dataType.getChildren():
                        reqLevel = MapleDataTool.getInt("reqLevel", itemFolder, 0)
                        reqMakerLevel = MapleDataTool.getInt("reqSkillLevel", itemFolder, 0)
                        cost = MapleDataTool.getInt("meso", itemFolder, 0)
                        quantity = MapleDataTool.getInt("itemNum", itemFolder, 0)
                        totalupgrades = MapleDataTool.getInt("tuc", itemFolder, 0)
                        stimulator = MapleDataTool.getInt("catalyst", itemFolder, 0)
                        imt = ItemMakerCreateEntry(cost, reqLevel, reqMakerLevel, quantity, totalupgrades, stimulator)
                        for Recipe in itemFolder.getChildren():
                            for ind in Recipe.getChildren():
                                if Recipe.getName() == ("recipe"):
                                    imt.addReqItem(MapleDataTool.getInt("item", ind, 0), MapleDataTool.getInt("count", ind, 0))
                        self.createCache.put(int(itemFolder.getName()), imt)
                    continue

    # Static initializer
    # instance = ItemMakerFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getGemInfo(self, itemid: int) -> Any:
        return self.gemCache.get(itemid)

    def getCreateInfo(self, itemid: int) -> Any:
        return self.createCache.get(itemid)

    def getRewardAmount(self) -> int:
        return self.quantity

    def getRandomReward(self) -> list:
        return self.randomReward

    def getReqRecipes(self) -> list:
        return self.reqRecipe

    def getReqLevel(self) -> int:
        return self.reqLevel

    def getReqSkillLevel(self) -> int:
        return self.reqMakerLevel

    def getCost(self) -> int:
        return self.cost

    def addRandomReward(self, itemId: int, prob: int) -> None:
        self.randomReward.add(new Pair<Integer, Integer>(itemId, prob))

    def addReqRecipe(self, itemId: int, count: int) -> None:
        self.reqRecipe.add(new Pair<Integer, Integer>(itemId, count))

    def getTUC(self) -> int:
        return self.tuc

    def getReqItems(self) -> list:
        return self.reqItems

    def getReqEquips(self) -> list:
        return self.reqEquips

    def getStimulator(self) -> int:
        return self.stimulator

    def addReqItem(self, itemId: int, amount: int) -> None:
        self.reqItems.add(new Pair<Integer, Integer>(itemId, amount))


# Inner class from Java (originally nested)
class GemCreateEntry:
    """
    Class GemCreateEntry
    """

    def __init__(self, cost: int, reqLevel: int, reqMakerLevel: int, quantity: int):
        self.reqLevel = None
        self.reqMakerLevel = None
        self.cost = None
        self.quantity = None
        self.randomReward = None
        self.reqRecipe = None
        self.randomReward = new ArrayList<Pair<Integer, Integer>>()
        self.reqRecipe = new ArrayList<Pair<Integer, Integer>>()
        self.cost = cost
        self.reqLevel = reqLevel
        self.reqMakerLevel = reqMakerLevel
        self.quantity = quantity


    def getRewardAmount(self) -> int:
        return self.quantity

    def getRandomReward(self) -> list:
        return self.randomReward

    def getReqRecipes(self) -> list:
        return self.reqRecipe

    def getReqLevel(self) -> int:
        return self.reqLevel

    def getReqSkillLevel(self) -> int:
        return self.reqMakerLevel

    def getCost(self) -> int:
        return self.cost

    def addRandomReward(self, itemId: int, prob: int) -> None:
        self.randomReward.add(new Pair<Integer, Integer>(itemId, prob))

    def addReqRecipe(self, itemId: int, count: int) -> None:
        self.reqRecipe.add(new Pair<Integer, Integer>(itemId, count))


# Inner class from Java (originally nested)
class ItemMakerCreateEntry:
    """
    Class ItemMakerCreateEntry
    """

    def __init__(self, cost: int, reqLevel: int, reqMakerLevel: int, quantity: int, tuc: int, stimulator: int):
        self.reqLevel = None
        self.cost = None
        self.quantity = None
        self.stimulator = None
        self.tuc = None
        self.reqMakerLevel = None
        self.reqItems = None
        self.reqEquips = None
        self.reqItems = new ArrayList<Pair<Integer, Integer>>()
        self.reqEquips = []
        self.cost = cost
        self.tuc = tuc
        self.reqLevel = reqLevel
        self.reqMakerLevel = reqMakerLevel
        self.quantity = quantity
        self.stimulator = stimulator


    def getTUC(self) -> int:
        return self.tuc

    def getRewardAmount(self) -> int:
        return self.quantity

    def getReqItems(self) -> list:
        return self.reqItems

    def getReqEquips(self) -> list:
        return self.reqEquips

    def getReqLevel(self) -> int:
        return self.reqLevel

    def getReqSkillLevel(self) -> int:
        return self.reqMakerLevel

    def getCost(self) -> int:
        return self.cost

    def getStimulator(self) -> int:
        return self.stimulator

    def addReqItem(self, itemId: int, amount: int) -> None:
        self.reqItems.add(new Pair<Integer, Integer>(itemId, amount))

