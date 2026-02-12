"""
AbstractMapleMapObject - Converted from Java source
Original: server/maps/AbstractMapleMapObject.java
Package: server.maps
"""

from typing import Optional, Any


class AbstractMapleMapObject(MapleMapObject, ABC):
    """
    Class AbstractMapleMapObject
    Implements: MapleMapObject
    """

    def __init__(self):
        self.position = None
        self.objectId = 0
        self.position = Point()


    def getTruePosition(self) -> Any:
        return self.position

    def getPosition(self) -> Any:
        return Point(self.position)

    def setPosition(self, position: Any) -> None:
        self.position.x = position.x
        self.position.y = position.y

    def getObjectId(self) -> int:
        return self.objectId

    def setObjectId(self, id: int) -> None:
        self.objectId = id

