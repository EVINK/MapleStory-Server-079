"""
MapleCustomQuestData - Converted from Java source
Original: server/quest/MapleCustomQuestData.java
Package: server.quest
"""

from typing import Iterator
from typing import List
from typing import Optional, Any

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from provider.WzXML.MapleDataType import *  # TODO: import specific classes


class MapleCustomQuestData(MapleData):
    """
    Class MapleCustomQuestData
    Implements: MapleData, Serializable
    """

    serialVersionUID = -8600005891655365066

    def __init__(self, name: str, data: Any, parent: Any):
        self.children = None
        self.name = None
        self.data = None
        self.parent = None
        self.children = []
        self.name = name
        self.data = data
        self.parent = parent


    def addChild(self, child: Any) -> None:
        self.children.add(child)

    def getName(self) -> str:
        return self.name

    def getType(self) -> Any:
        return MapleDataType.UNKNOWN_TYPE

    def getChildren(self) -> list:
        ret = new MapleData[self.children]
        ret = self.children
        return [])

    def getChildByPath(self, name: str) -> Any:
        if name == (self.name):
            return this
        lookup = None
        nextName = None
        if name.find("/") == -1:
            lookup = name
            nextName = name
        else:
            lookup = name[0:name.find("/"])
            nextName = name[name.find("/":] + 1)
        for child in self.children:
            if child.getName() == (lookup):
                return child.getChildByPath(nextName)
        return None

    def getData(self) -> Any:
        return self.data

    def iterator(self) -> iter:
        return self.getChildren().iterator()

    def getParent(self) -> Any:
        return self.parent

