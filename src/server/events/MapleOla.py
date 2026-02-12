"""
MapleOla - Converted from Java source
Original: server/events/MapleOla.java
Package: server.events
"""

from concurrent.futures import Future
from typing import Optional, Any
import sched
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleOla(MapleEvent):
    """
    Class MapleOla
    Extends: MapleEvent
    """

    serialVersionUID = 845748150824

    def __init__(self, channel: int, mapid: list):
        self.time = 600000
        self.timeStarted = 0
        super(channel, mapid)
        self.timeStarted = 0
        self.stages = new int[3]


    def finished(self, chr: Any) -> None:
        self.givePrize(chr)

    def onMapLoad(self, chr: Any) -> None:
        if self.isTimerStarted():
            chr.getClient().getSession().write(MaplePacketCreator.getClock((int)(self.getTimeLeft() / 1000)))

    def startEvent(self) -> None:
        self.unreset()
        super.reset()
        self.broadcast(MaplePacketCreator.getClock(600))
        self.timeStarted = int(time.time() * 1000)
        final Timer.EventTimer instance = Timer.EventTimer.getInstance()
        r = Runnable()
            public void run()
                for i in range(MapleOla.self.len(mapid)):
                    for chr in MapleOla.self.getMap(i).getCharactersThreadsafe():
                        MapleOla.self.warpBack(chr)
                    MapleOla.self.unreset()
        self.getClass()
        self.olaSchedule = instance.schedule(r, 600000)
        self.broadcast(MaplePacketCreator.serverNotice(0, "门已打开。按箭头↑键进入入口."))

    def run(self) -> None:
        for i in range(MapleOla.self.len(mapid)):
            for chr in MapleOla.self.getMap(i).getCharactersThreadsafe():
                MapleOla.self.warpBack(chr)
            MapleOla.self.unreset()

    def isTimerStarted(self) -> bool:
        return self.timeStarted > 0

    def getTime(self) -> int:
        return 600000

    def resetSchedule(self) -> None:
        self.timeStarted = 0
        if self.olaSchedule is not None:
            self.olaSchedule.cancel(False)
        self.olaSchedule = None

    def reset(self) -> None:
        super.reset()
        self.resetSchedule()
        self.getMap(0).getPortal("join00").setPortalState(False)
        self.stages = new int[] { 0, 0, 0 }

    def unreset(self) -> None:
        super.unreset()
        self.resetSchedule()
        self.getMap(0).getPortal("join00").setPortalState(True)
        self.stages = new int[] { Randomizer.nextInt(5), Randomizer.nextInt(8), Randomizer.nextInt(15) }

    def getTimeLeft(self) -> int:
        return 600000 - (int(time.time() * 1000) - self.timeStarted)

    def isCharCorrect(self, portalName: str, mapid: int) -> bool:
        st = self.stages[mapid % 10 - 1]
        return portalName == ("ch" + ((st < 10) ? "0" : "") + st)

