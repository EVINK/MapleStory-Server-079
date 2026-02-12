"""
RockPaperScissors - Converted from Java source
Original: client/RockPaperScissors.java
Package: client
"""

from typing import Optional, Any

# Internal module imports
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class RockPaperScissors:
    """
    Class RockPaperScissors
    """

    def __init__(self, c: Any, mode: int):
        self.round = 0
        self.ableAnswer = False
        self.win = False
        self.round = 0
        self.ableAnswer = True
        self.win = False
        c.getSession().write(MaplePacketCreator.getRPSMode((byte)(9 + mode), -1, -1, -1))
        if mode == 0:
            c.getPlayer().gainMeso(-1000, True, True, True)


    def answer(self, c: Any, answer: int) -> bool:
        if self.ableAnswer && !self.win && answer >= 0 && answer <= 2:
            response = Randomizer.nextInt(3)
            if response == answer:
                c.getSession().write(MaplePacketCreator.getRPSMode(11, -1, response, self.round))
            elif (answer == 0 && response == 2) || (answer == 1 && response == 0) || (answer == 2 && response == 1):
                c.getSession().write(MaplePacketCreator.getRPSMode(11, -1, response, (byte)(self.round + 1)))
                self.ableAnswer = False
                self.win = True
            else:
                c.getSession().write(MaplePacketCreator.getRPSMode(11, -1, response, -1))
                self.ableAnswer = False
            return True
        self.reward(c)
        return False

    def timeOut(self, c: Any) -> bool:
        if self.ableAnswer && !self.win:
            self.ableAnswer = False
            c.getSession().write(MaplePacketCreator.getRPSMode(10, -1, -1, -1))
            return True
        self.reward(c)
        return False

    def nextRound(self, c: Any) -> bool:
        if self.win:
            self.round += 1
            if self.round < 10:
                self.win = False
                self.ableAnswer = True
                c.getSession().write(MaplePacketCreator.getRPSMode(12, -1, -1, -1))
                return True
        self.reward(c)
        return False

    def reward(self, c: Any) -> None:
        if self.win:
            MapleInventoryManipulator.addById(c, 4031332 + self.round, 1, "", None, 0, 0)
        elif self.round == 0:
            c.getPlayer().gainMeso(500, True, True, True)
        c.getPlayer().setRPS(None)

    def dispose(self, c: Any) -> None:
        self.reward(c)
        c.getSession().write(MaplePacketCreator.getRPSMode(13, -1, -1, -1))

