"""
PredictCardFactory - Converted from Java source
Original: server/PredictCardFactory.java
Package: server
"""

from pathlib import Path
from typing import Dict
from typing import Optional, Any
import os

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes


class PredictCardFactory:
    """
    Class PredictCardFactory
    """

    def __init__(self):
        self.etcData = None
        self.predictCard = {}
        self.predictCardComment = {}
        self.name = ""
        self.comment = ""
        self.score = 0
        self.effectType = 0
        self.worldmsg0 = ""
        self.worldmsg1 = ""
        self.etcData = MapleDataProviderFactory.getDataProvider(File("wz/Etc.wz"))
        self.predictCard = {}
        self.predictCardComment = {}

    # Static initializer
    # instance = PredictCardFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        if !self.predictCard == 0 || !self.predictCardComment == 0:
            return
        infoData = self.etcData.getData("PredictCard.img")
        for cardDat in infoData:
            if cardDat.getName() == ("comment"):
                continue
            card = PredictCard()
            card.name = MapleDataTool.getString("name", cardDat, "")
            card.comment = MapleDataTool.getString("comment", cardDat, "")
            self.predictCard.put(int(cardDat.getName()), card)
        commentData = infoData.getChildByPath("comment")
        for commentDat in commentData:
            comment = PredictCardComment()
            comment.worldmsg0 = MapleDataTool.getString("0", commentDat, "")
            comment.worldmsg1 = MapleDataTool.getString("1", commentDat, "")
            comment.score = MapleDataTool.getIntConvert("score", commentDat, 0)
            comment.effectType = MapleDataTool.getIntConvert("effectType", commentDat, 0)
            self.predictCardComment.put(int(commentDat.getName()), comment)

    def getPredictCard(self, id: int) -> Any:
        if !(id in self.predictCard):
            return None
        return self.predictCard.get(id)

    def getPredictCardComment(self, id: int) -> Any:
        if !(id in self.predictCardComment):
            return None
        return self.predictCardComment.get(id)

    def RandomCardComment(self) -> Any:
        return self.getPredictCardComment(Randomizer.nextInt(self.predictCardComment))

    def getCardCommentSize(self) -> int:
        return self.predictCardComment


# Inner class from Java (originally nested)
class PredictCard:
    """
    Class PredictCard
    """

    def __init__(self):
        self.name = ""
        self.comment = ""



# Inner class from Java (originally nested)
class PredictCardComment:
    """
    Class PredictCardComment
    """

    def __init__(self):
        self.score = 0
        self.effectType = 0
        self.worldmsg0 = ""
        self.worldmsg1 = ""


