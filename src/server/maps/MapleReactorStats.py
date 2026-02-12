"""
MapleReactorStats - Converted from Java source
Original: server/maps/MapleReactorStats.java
Package: server.maps
"""

from typing import Dict
from typing import Optional, Any

# Internal module imports
# from tools.Pair import *  # TODO: import specific classes


class MapleReactorStats:
    """
    Class MapleReactorStats
    """

    def __init__(self):
        self.facingDirection = 0
        self.tl = None
        self.br = None
        self.stateInfo = None
        self.type = None
        self.timeOut = None
        self.reactItem = None
        self.nextState = None
        self.canTouch = None
        self.stateInfo = {}


    def setFacingDirection(self, facingDirection: int) -> None:
        self.facingDirection = facingDirection

    def getFacingDirection(self) -> int:
        return self.facingDirection

    def setTL(self, tl: Any) -> None:
        self.tl = tl

    def setBR(self, br: Any) -> None:
        self.br = br

    def getTL(self) -> Any:
        return self.tl

    def getBR(self) -> Any:
        return self.br

    def addState(self, state: int, type: int, reactItem: Any, nextState: int, timeOut: int, canTouch: int) -> None:
        newState = StateData(type, reactItem, nextState, timeOut, canTouch)
        self.stateInfo.put(state, newState)

    def getNextState(self, state: int) -> int:
        nextState = self.stateInfo.get(state)
        if nextState is not None:
            return nextState.getNextState()
        return -1

    def getType(self, state: int) -> int:
        nextState = self.stateInfo.get(state)
        if nextState is not None:
            return nextState.getType()
        return -1

    def getReactItem(self, state: int) -> Any:
        nextState = self.stateInfo.get(state)
        if nextState is not None:
            return nextState.getReactItem()
        return None

    def getTimeOut(self, state: int) -> int:
        nextState = self.stateInfo.get(state)
        if nextState is not None:
            return nextState.getTimeOut()
        return -1

    def canTouch(self, state: int) -> int:
        nextState = self.stateInfo.get(state)
        if nextState is not None:
            return nextState.canTouch()
        return 0


# Inner class from Java (originally nested)
class StateData:
    """
    Class StateData
    """

    def __init__(self, type: int, reactItem: Any, nextState: int, timeOut: int, canTouch: int):
        self.type = None
        self.timeOut = None
        self.reactItem = None
        self.nextState = None
        self.canTouch = None
        self.type = type
        self.reactItem = reactItem
        self.nextState = nextState
        self.timeOut = timeOut
        self.canTouch = canTouch


    def getType(self) -> int:
        return self.type

    def getNextState(self) -> int:
        return self.nextState

    def getReactItem(self) -> Any:
        return self.reactItem

    def getTimeOut(self) -> int:
        return self.timeOut

    def canTouch(self) -> int:
        return self.canTouch

