"""
AbstractLifeMovement - Converted from Java source
Original: server/movement/AbstractLifeMovement.java
Package: server.movement
"""

from typing import Optional, Any


class AbstractLifeMovement(LifeMovement, ABC):
    """
    Class AbstractLifeMovement
    Implements: LifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.position = None
        self.duration = 0
        self.newstate = 0
        self.type = 0
        self.type = type
        self.position = position
        self.duration = duration
        self.newstate = newstate


    def getType(self) -> int:
        return self.type

    def getDuration(self) -> int:
        return self.duration

    def getNewstate(self) -> int:
        return self.newstate

    def getPosition(self) -> Any:
        return self.position

