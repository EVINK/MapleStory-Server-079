"""
MapleReactor - Converted from Java source
Original: server/maps/MapleReactor.java
Package: server.maps
"""

from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from scripting.ReactorScriptManager import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleReactor(AbstractMapleMapObject):
    """
    Class MapleReactor
    Extends: AbstractMapleMapObject
    """

    def __init__(self, stats: Any, rid: int):
        self.rid = None
        self.stats = None
        self.state = 0
        self.delay = 0
        self.map = None
        self.name = ""
        self.timerActive = False
        self.alive = False
        self.name = ""
        self.stats = stats
        self.rid = rid
        self.alive = True


    def getFacingDirection(self) -> int:
        return self.stats.getFacingDirection()

    def setTimerActive(self, active: bool) -> None:
        self.timerActive = active

    def isTimerActive(self) -> bool:
        return self.timerActive

    def getReactorId(self) -> int:
        return self.rid

    def setState(self, state: int) -> None:
        self.state = state

    def getState(self) -> int:
        return self.state

    def isAlive(self) -> bool:
        return self.alive

    def setAlive(self, alive: bool) -> None:
        self.alive = alive

    def setDelay(self, delay: int) -> None:
        self.delay = delay

    def getDelay(self) -> int:
        return self.delay

    def getType(self) -> Any:
        return MapleMapObjectType.REACTOR

    def getReactorType(self) -> int:
        return self.stats.getType(self.state)

    def getTouch(self) -> int:
        return self.stats.canTouch(self.state)

    def setMap(self, map: Any) -> None:
        self.map = map

    def getMap(self) -> Any:
        return self.map

    def getReactItem(self) -> Any:
        return self.stats.getReactItem(self.state)

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.destroyReactor(this))

    def sendSpawnData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.spawnReactor(this))

    def forceStartReactor(self, c: Any) -> None:
        ReactorScriptManager.getInstance().act(c, this)

    def forceHitReactor(self, newState: int) -> None:
        self.setState(newState)
        self.setTimerActive(False)
        self.map.broadcastMessage(MaplePacketCreator.triggerReactor(this, 0))

    def hitReactor(self, c: Any) -> None:
        self.hitReactor(0, 0, c)

    def forceTrigger(self) -> None:
        self.map.broadcastMessage(MaplePacketCreator.triggerReactor(this, 0))

    def delayedDestroyReactor(self, delay: int) -> None:
        def _task_1():
            MapleReactor.self.map.destroyReactor(MapleReactor.self.getObjectId())

        Timer.MapTimer.getInstance().schedule(_task_1, delay)

    def run(self) -> None:
        MapleReactor.self.map.destroyReactor(MapleReactor.self.getObjectId())

    def hitReactor_charPos_stance_c(self, charPos: int, stance: int, c: Any) -> None:
        if self.stats.getType(self.state) < 999 and self.stats.getType(self.state) != -1:
            oldState = self.state
            pass = False
            pass = (self.getReactorId() == 1072000 or self.stats.getType(self.state) != 2)
            if pass or (charPos != 0 and charPos != 2):
                self.state = self.stats.getNextState(self.state)
                if self.stats.getNextState(self.state) == -1 or self.stats.getType(self.state) == 999:
                    if (self.stats.getType(self.state) < 100 or self.stats.getType(self.state) == 999) and self.delay > 0:
                        self.map.destroyReactor(self.getObjectId())
                    else:
                        self.map.broadcastMessage(MaplePacketCreator.triggerReactor(this, stance))
                    ReactorScriptManager.getInstance().act(c, this)
                else:
                    done = False
                    self.map.broadcastMessage(MaplePacketCreator.triggerReactor(this, stance))
                    if self.state == self.stats.getNextState(self.state) or self.rid == 2618000 or self.rid == 2309000:
                        if self.rid > 200011:
                            ReactorScriptManager.getInstance().act(c, this)
                        done = True
                    if self.stats.getTimeOut(self.state) > 0:
                        if not done and self.rid > 200011:
                            ReactorScriptManager.getInstance().act(c, this)
                        self.scheduleSetState(self.state, oldState, self.stats.getTimeOut(self.state))

    def getArea(self) -> Any:
        height = self.stats.getBR().y - self.stats.getTL().y
        width = self.stats.getBR().x - self.stats.getTL().x
        origX = self.getPosition().x + self.stats.getTL().x
        origY = self.getPosition().y + self.stats.getTL().y
        return Rectangle(origX, origY, width, height)

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def toString(self) -> str:
        return "Reactor " + self.getObjectId() + " of id " + self.rid + " at position " + self.getPosition() + " state" + self.state + " type " + self.stats.getType(self.state)

    def delayedHitReactor(self, c: Any, delay: int) -> None:
        def _task_1():
            MapleReactor.self.hitReactor(c)

        Timer.MapTimer.getInstance().schedule(_task_1, delay)

    def scheduleSetState(self, oldState: int, newState: int, delay: int) -> None:
        def _task_1():
            if MapleReactor.self.state == oldState:
                MapleReactor.self.forceHitReactor(newState)

        Timer.MapTimer.getInstance().schedule(_task_1, delay)

