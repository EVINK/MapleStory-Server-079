"""
MapleLieDetector - Converted from Java source
Original: client/MapleLieDetector.java
Package: client
"""

from typing import Optional, Any
import threading

# Internal module imports
# from scripting.LieDetectorScript import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleLieDetector:
    """
    Class MapleLieDetector
    """

    def __init__(self, c: Any):
        self.chr = None
        self.type = 0
        self.attempt = 0
        self.tester = ""
        self.answer = ""
        self.inProgress = False
        self.passed = False
        self.chr = c
        self.reset()


    def startLieDetector(self, tester: str, isItem: bool, anotherAttempt: bool) -> bool:
        if !anotherAttempt && (self.chr.isClone() || (isPassed() && isItem) || inProgress() || self.attempt == 3):
        return False
        captcha = LieDetectorScript.getImageBytes()
        if captcha is None:
        return False
        image = HexTool.getByteArrayFromHexString(captcha.getLeft())
        self.answer = captcha.getRight()
        self.tester = tester
        self.inProgress = True
        self.type = (byte)(isItem ? 0 : 1)
        self.attempt += 1
        self.chr.getClient().getSession().write(MaplePacketCreator.sendLieDetector(image, self.attempt))
        Timer.EtcTimer.getInstance().schedule(Runnable()
            public void run()
                if !MapleLieDetector.self.isPassed() && MapleLieDetector.self.chr is not None:
                if MapleLieDetector.self.attempt >= 3:
                    search_chr = MapleLieDetector.self.chr.getMap().getCharacterByName(tester)
                    if search_chr is not None && search_chr.getId() != MapleLieDetector.self.chr.getId():
                        search_chr.dropMessage(5, MapleLieDetector.self.chr.getName() + " 没用通过测谎仪的检测，恭喜你获得7000的金币.")
                        search_chr.gainMeso(7000, True)
                    MapleLieDetector.self.end()
                    MapleLieDetector.self.chr.getClient().getSession().write(MaplePacketCreator.LieDetectorResponse(8, 4))
                    map = MapleLieDetector.self.chr.getClient().getChannelServer().getMapFactory().getMap(180000001)
                    MapleLieDetector.self.chr.getQuestNAdd(MapleQuest.getInstance(123456)).setCustomData(str(1800))
                    MapleLieDetector.self.chr.changeMap(map, map.getPortal(0))
                else:
                    MapleLieDetector.self.startLieDetector(tester, isItem, True)
        return True

    def run(self) -> None:
        if !MapleLieDetector.self.isPassed() && MapleLieDetector.self.chr is not None:
        if MapleLieDetector.self.attempt >= 3:
            search_chr = MapleLieDetector.self.chr.getMap().getCharacterByName(tester)
            if search_chr is not None && search_chr.getId() != MapleLieDetector.self.chr.getId():
                search_chr.dropMessage(5, MapleLieDetector.self.chr.getName() + " 没用通过测谎仪的检测，恭喜你获得7000的金币.")
                search_chr.gainMeso(7000, True)
            MapleLieDetector.self.end()
            MapleLieDetector.self.chr.getClient().getSession().write(MaplePacketCreator.LieDetectorResponse(8, 4))
            map = MapleLieDetector.self.chr.getClient().getChannelServer().getMapFactory().getMap(180000001)
            MapleLieDetector.self.chr.getQuestNAdd(MapleQuest.getInstance(123456)).setCustomData(str(1800))
            MapleLieDetector.self.chr.changeMap(map, map.getPortal(0))
        else:
            MapleLieDetector.self.startLieDetector(tester, isItem, True)

    def getAttempt(self) -> int:
        return self.attempt

    def getLastType(self) -> int:
        return self.type

    def getTester(self) -> str:
        return self.tester

    def getAnswer(self) -> str:
        return self.answer

    def inProgress(self) -> bool:
        return self.inProgress

    def isPassed(self) -> bool:
        return self.passed

    def end(self) -> None:
        self.inProgress = False
        self.passed = True
        self.attempt = 0

    def reset(self) -> None:
        self.tester = ""
        self.answer = ""
        self.attempt = 0
        self.inProgress = False
        self.passed = False

