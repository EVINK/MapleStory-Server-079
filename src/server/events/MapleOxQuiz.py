"""
MapleOxQuiz - Converted from Java source
Original: server/events/MapleOxQuiz.java
Package: server.events
"""

from concurrent.futures import Future
from typing import Dict
from typing import Optional, Any
import sched
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleOxQuiz(MapleEvent):
    """
    Class MapleOxQuiz
    Extends: MapleEvent
    """

    def __init__(self, channel: int, mapid: list):
        self.timesAsked = 0
        super(channel, mapid)
        self.timesAsked = 0


    def resetSchedule(self) -> None:
        if self.oxSchedule is not None:
            self.oxSchedule.cancel(False)
            self.oxSchedule = None
        if self.oxSchedule2 is not None:
            self.oxSchedule2.cancel(False)
            self.oxSchedule2 = None

    def onMapLoad(self, chr: Any) -> None:
        if chr.getMapId() == self.mapid[0] && !chr.isGM():
            chr.canTalk(False)

    def reset(self) -> None:
        super.reset()
        self.getMap(0).getPortal("join00").setPortalState(False)
        self.resetSchedule()
        self.timesAsked = 0

    def unreset(self) -> None:
        super.unreset()
        self.getMap(0).getPortal("join00").setPortalState(True)
        self.resetSchedule()

    def startEvent(self) -> None:
        self.sendQuestion()

    def sendQuestion(self) -> None:
        self.sendQuestion(self.getMap(0))

    def sendQuestion_toSend(self, toSend: Any) -> None:
        if self.oxSchedule2 is not None:
            self.oxSchedule2.cancel(False)
        self.oxSchedule2 = Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                number = 0
                for mc in toSend.getCharactersThreadsafe():
                    if mc.isGM() || !mc.isAlive():
                        number += 1
                if toSend.getCharactersSize() - number <= 1 || MapleOxQuiz.self.timesAsked == 10:
                    toSend.broadcastMessage(MaplePacketCreator.serverNotice(6, "人数不足！活动自动结束！"))
                    MapleOxQuiz.self.unreset()
                    for chr in toSend.getCharactersThreadsafe():
                        if chr is not None && !chr.isGM() && chr.isAlive():
                            chr.canTalk(True)
                            MapleOxQuiz.self.givePrize(chr)
                            MapleOxQuiz.self.warpBack(chr)
                    return
                final Map.Entry<Pair<Integer, Integer>, MapleOxQuizFactory.MapleOxQuizEntry> question = MapleOxQuizFactory.getInstance().grabRandomQuestion()
                toSend.broadcastMessage(MaplePacketCreator.showOXQuiz(question.getKey().left, question.getKey().right, True))
                toSend.broadcastMessage(MaplePacketCreator.getClock(12))
                if MapleOxQuiz.self.oxSchedule is not None:
                    MapleOxQuiz.self.oxSchedule.cancel(False)
                MapleOxQuiz.self.oxSchedule = Timer.EventTimer.getInstance().schedule(Runnable()
                    public void run()
                        toSend.broadcastMessage(MaplePacketCreator.showOXQuiz(question.getKey().left, question.getKey().right, False))
                        MapleOxQuiz.self.timesAsked += 1
                        for chr in toSend.getCharactersThreadsafe():
                            if chr is not None && !chr.isGM() && chr.isAlive():
                                if !MapleOxQuiz.self.isCorrectAnswer(chr, question.getValue().getAnswer()):
                                    chr.getStat().setHp(0)
                                    chr.updateSingleStat(MapleStat.HP, 0)
                                else:
                                    chr.gainExp(3000, True, True, False)
                        MapleOxQuiz.self.sendQuestion()

    def run(self) -> None:
        number = 0
        for mc in toSend.getCharactersThreadsafe():
            if mc.isGM() || !mc.isAlive():
                number += 1
        if toSend.getCharactersSize() - number <= 1 || MapleOxQuiz.self.timesAsked == 10:
            toSend.broadcastMessage(MaplePacketCreator.serverNotice(6, "人数不足！活动自动结束！"))
            MapleOxQuiz.self.unreset()
            for chr in toSend.getCharactersThreadsafe():
                if chr is not None && !chr.isGM() && chr.isAlive():
                    chr.canTalk(True)
                    MapleOxQuiz.self.givePrize(chr)
                    MapleOxQuiz.self.warpBack(chr)
            return
        final Map.Entry<Pair<Integer, Integer>, MapleOxQuizFactory.MapleOxQuizEntry> question = MapleOxQuizFactory.getInstance().grabRandomQuestion()
        toSend.broadcastMessage(MaplePacketCreator.showOXQuiz(question.getKey().left, question.getKey().right, True))
        toSend.broadcastMessage(MaplePacketCreator.getClock(12))
        if MapleOxQuiz.self.oxSchedule is not None:
            MapleOxQuiz.self.oxSchedule.cancel(False)
        MapleOxQuiz.self.oxSchedule = Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                toSend.broadcastMessage(MaplePacketCreator.showOXQuiz(question.getKey().left, question.getKey().right, False))
                MapleOxQuiz.self.timesAsked += 1
                for chr in toSend.getCharactersThreadsafe():
                    if chr is not None && !chr.isGM() && chr.isAlive():
                        if !MapleOxQuiz.self.isCorrectAnswer(chr, question.getValue().getAnswer()):
                            chr.getStat().setHp(0)
                            chr.updateSingleStat(MapleStat.HP, 0)
                        else:
                            chr.gainExp(3000, True, True, False)
                MapleOxQuiz.self.sendQuestion()

    def isCorrectAnswer(self, chr: Any, answer: int) -> bool:
        x = chr.getPosition().getX()
        y = chr.getPosition().getY()
        if (x > -234.0 && y > -26.0 && answer == 0) || (x < -234.0 && y > -26.0 && answer == 1):
            chr.dropMessage(6, "[OX答题活动] 恭喜答对!")
            return True
        chr.dropMessage(6, "[OX答题活动] 你答错了!")
        return False

