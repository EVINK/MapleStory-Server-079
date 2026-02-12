"""
MapleCoconut - Converted from Java source
Original: server/events/MapleCoconut.java
Package: server.events
"""

from typing import List
from typing import Optional, Any
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleCoconut(MapleEvent):
    """
    Class MapleCoconut
    Extends: MapleEvent
    """

    def __init__(self, channel: int, mapid: list):
        self.coconuts = None
        self.countBombing = 0
        self.countFalling = 0
        self.countStopped = 0
        self.hits = 0
        self.hittable = False
        self.stopped = False
        self.hittime = 0
        super(channel, mapid)
        self.coconuts = []
        self.coconutscore = new int[2]
        self.countBombing = 0
        self.countFalling = 0
        self.countStopped = 0


    def reset(self) -> None:
        super.reset()
        self.resetCoconutScore()

    def unreset(self) -> None:
        super.unreset()
        self.resetCoconutScore()
        self.setHittable(False)

    def onMapLoad(self, chr: Any) -> None:
        chr.getClient().getSession().write(MaplePacketCreator.coconutScore(self.getCoconutScore()))

    def getCoconut(self, id: int) -> Any:
        return self.coconuts.get(id)

    def getAllCoconuts(self) -> list:
        return self.coconuts

    def setHittable(self, hittable: bool) -> None:
        for nut in self.coconuts:
            nut.setHittable(hittable)

    def getBombings(self) -> int:
        return self.countBombing

    def bombCoconut(self) -> None:
        self.countBombing -= 1

    def getFalling(self) -> int:
        return self.countFalling

    def fallCoconut(self) -> None:
        self.countFalling -= 1

    def getStopped(self) -> int:
        return self.countStopped

    def stopCoconut(self) -> None:
        self.countStopped -= 1

    def getCoconutScore(self) -> list:
        return self.coconutscore

    def getMapleScore(self) -> int:
        return self.coconutscore[0]

    def getStoryScore(self) -> int:
        return self.coconutscore[1]

    def addMapleScore(self) -> None:
        coconutscore = self.coconutscore
        n = 0
        ++coconutscore[n]

    def addStoryScore(self) -> None:
        coconutscore = self.coconutscore
        n = 1
        ++coconutscore[n]

    def resetCoconutScore(self) -> None:
        self.coconutscore[0] = 0
        self.coconutscore[1] = 0
        self.countBombing = 80
        self.countFalling = 1001
        self.countStopped = 20
        self.coconuts.clear()
        for i in range(506):
            self.coconuts.add(MapleCoconuts())

    def startEvent(self) -> None:
        def _task_1():
            if MapleCoconut.self.getMapleScore() == MapleCoconut.self.getStoryScore():
                MapleCoconut.self.bonusTime()
            elif MapleCoconut.self.getMapleScore() > MapleCoconut.self.getStoryScore():
                for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                    if chr.getCoconutTeam() == 0:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                    else:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
                MapleCoconut.self.warpOut()
            else:
                for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                    if chr.getCoconutTeam() == 1:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                    else:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
                MapleCoconut.self.warpOut()

        self.reset()
        self.setHittable(True)
        self.getMap(0).broadcastMessage(MaplePacketCreator.serverNotice(5, "活动开始!not "))
        self.getMap(0).broadcastMessage(MaplePacketCreator.hitCoconut(True, 0, 0))
        self.getMap(0).broadcastMessage(MaplePacketCreator.getClock(360))
        Timer.EventTimer.getInstance().schedule(_task_1, 360000)

    def run(self) -> None:
        if MapleCoconut.self.getMapleScore() == MapleCoconut.self.getStoryScore():
            MapleCoconut.self.bonusTime()
        elif MapleCoconut.self.getMapleScore() > MapleCoconut.self.getStoryScore():
            for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                if chr.getCoconutTeam() == 0:
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                    chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                else:
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                    chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
            MapleCoconut.self.warpOut()
        else:
            for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                if chr.getCoconutTeam() == 1:
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                    chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                else:
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                    chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
            MapleCoconut.self.warpOut()

    def bonusTime(self) -> None:
        def _task_1():
            if MapleCoconut.self.getMapleScore() == MapleCoconut.self.getStoryScore():
                for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                    chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
                MapleCoconut.self.warpOut()
            elif MapleCoconut.self.getMapleScore() > MapleCoconut.self.getStoryScore():
                for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                    if chr.getCoconutTeam() == 0:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                    else:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
                MapleCoconut.self.warpOut()
            else:
                for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                    if chr.getCoconutTeam() == 1:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/victory"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Victory"))
                    else:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("event/coconut/lose"))
                        chr.getClient().getSession().write(MaplePacketCreator.playSound("Coconut/Failed"))
                MapleCoconut.self.warpOut()

        self.getMap(0).broadcastMessage(MaplePacketCreator.getClock(120))
        Timer.EventTimer.getInstance().schedule(_task_1, 120000)

    def warpOut(self) -> None:
        def _task_1():
            for chr in MapleCoconut.self.getMap(0).getCharactersThreadsafe():
                if (MapleCoconut.self.getMapleScore() > MapleCoconut.self.getStoryScore() and chr.getCoconutTeam() == 0) or (MapleCoconut.self.getStoryScore() > MapleCoconut.self.getMapleScore() and chr.getCoconutTeam() == 1):
                    MapleCoconut.self.givePrize(chr)
                MapleCoconut.self.warpBack(chr)
            MapleCoconut.self.unreset()

        self.setHittable(False)
        Timer.EventTimer.getInstance().schedule(_task_1, 12000)

    def hit(self) -> None:
        self.hittime = int(time.time() * 1000) + 1000
        self.hits += 1

    def getHits(self) -> int:
        return self.hits

    def resetHits(self) -> None:
        self.hits = 0

    def isHittable(self) -> bool:
        return self.hittable

    def setHittable_hittable(self, hittable: bool) -> None:
        self.hittable = hittable

    def isStopped(self) -> bool:
        return self.stopped

    def setStopped(self, stopped: bool) -> None:
        self.stopped = stopped

    def getHitTime(self) -> int:
        return self.hittime


# Inner class from Java (originally nested)
class MapleCoconuts:
    """
    Class MapleCoconuts
    """

    def __init__(self):
        self.hits = 0
        self.hittable = False
        self.stopped = False
        self.hittime = 0
        self.hits = 0
        self.hittable = False
        self.stopped = False
        self.hittime = int(time.time() * 1000)


    def hit(self) -> None:
        self.hittime = int(time.time() * 1000) + 1000
        self.hits += 1

    def getHits(self) -> int:
        return self.hits

    def resetHits(self) -> None:
        self.hits = 0

    def isHittable(self) -> bool:
        return self.hittable

    def setHittable(self, hittable: bool) -> None:
        self.hittable = hittable

    def isStopped(self) -> bool:
        return self.stopped

    def setStopped(self, stopped: bool) -> None:
        self.stopped = stopped

    def getHitTime(self) -> int:
        return self.hittime

