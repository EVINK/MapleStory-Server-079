"""
RandomRewards - Converted from Java source
Original: server/RandomRewards.java
Package: server
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes


class RandomRewards:
    """
    Class RandomRewards
    """

    def __init__(self):
        self.compiledGold = []
        self.compiledSilver = []
        self.compiledFishing = []
        self.compiledEvent = []
        self.compiledEventC = []
        self.compiledEventB = []
        self.compiledEventA = []
        self.compiledGold = None
        self.compiledSilver = None
        self.compiledFishing = None
        self.compiledEvent = None
        self.compiledEventC = None
        self.compiledEventB = None
        self.compiledEventA = None
        print("加载 随机奖励 :::")
        returnArray = []
        self.processRewards(returnArray, GameConstants.goldrewards)
        self.compiledGold = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.silverrewards)
        self.compiledSilver = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.fishingReward)
        self.compiledFishing = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.eventCommonReward)
        self.compiledEventC = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.eventUncommonReward)
        self.compiledEventB = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.eventRareReward)
        self.compiledEventA = returnArray
        returnArray = []
        self.processRewards(returnArray, GameConstants.eventSuperReward)
        self.compiledEvent = returnArray

    # Static initializer
    # instance = RandomRewards()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def processRewards(self, returnArray: list, list: list) -> None:
        lastitem = 0
        for i in range(len(list)):
            if i % 2 == 0:
                lastitem = list[i]
            else:
                for j in range(list[i]):
                    returnArray.add(lastitem)
        Collections.shuffle(returnArray)

    def getGoldBoxReward(self) -> int:
        return self.compiledGold.get(Randomizer.nextInt(self.compiledGold))

    def getSilverBoxReward(self) -> int:
        return self.compiledSilver.get(Randomizer.nextInt(self.compiledSilver))

    def getFishingReward(self) -> int:
        return self.compiledFishing.get(Randomizer.nextInt(self.compiledFishing))

    def getEventReward(self) -> int:
        chance = Randomizer.nextInt(100)
        if chance < 50:
            return self.compiledEventC.get(Randomizer.nextInt(self.compiledEventC))
        if chance < 80:
            return self.compiledEventB.get(Randomizer.nextInt(self.compiledEventB))
        if chance < 95:
            return self.compiledEventA.get(Randomizer.nextInt(self.compiledEventA))
        return self.compiledEvent.get(Randomizer.nextInt(self.compiledEvent))

