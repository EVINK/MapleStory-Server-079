"""
AbstractAnimatedMapleMapObject - Converted from Java source
Original: server/maps/AbstractAnimatedMapleMapObject.java
Package: server.maps
"""

from typing import Optional, Any


class AbstractAnimatedMapleMapObject(AbstractMapleMapObject, AnimatedMapleMapObject, ABC):
    """
    Class AbstractAnimatedMapleMapObject
    Extends: AbstractMapleMapObject
    Implements: AnimatedMapleMapObject
    """

    def __init__(self):
        self.stance = 0


    def getStance(self) -> int:
        return self.stance

    def setStance(self, stance: int) -> None:
        self.stance = stance

    def isFacingLeft(self) -> bool:
        return self.getStance() % 2 != 0

    def getFacingDirection(self) -> int:
        return self.getStance() % 2

