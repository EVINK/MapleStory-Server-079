"""
MapleMiniGame - Converted from Java source
Original: server/shops/MapleMiniGame.java
Package: server.shops
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class MapleMiniGame(AbstractPlayerStore):
    """
    Class MapleMiniGame
    Extends: AbstractPlayerStore
    """

    slots = 2

    def __init__(self, owner: Any, itemId: int, description: str, pass: str, GameType: int):
        self.GameType = 0
        self.matchcards = None
        super(owner, itemId, description, pass, 1)
        self.GameType = 0
        self.piece = new int[15][15]
        self.matchcards = []
        self.loser = 0
        self.turn = 1
        self.piecetype = 0
        self.firstslot = 0
        self.tie = -1
        self.REDO = -1
        self.GameType = GameType
        self.points = new int[2]
        self.exitAfter = new boolean[2]
        self.ready = new boolean[2]
        self.reset()


    def reset(self) -> None:
        for i in range(2):
            self.points[i] = 0
            self.exitAfter[i] = False
            self.ready[i] = False

    def setFirstSlot(self, type: int) -> None:
        self.firstslot = type

    def getFirstSlot(self) -> int:
        return self.firstslot

    def setPoints(self, slot: int) -> None:
        points = self.points
        ++points[slot]
        self.checkWin()

    def getPoints(self) -> int:
        ret = 0
        for i in range(2):
            ret += self.points[i]
        return ret

    def checkWin(self) -> None:
        if self.getPoints() >= self.getMatchesToWin() && !self.isOpen():
            x = 0
            highest = 0
            tie = False
            REDO = False
            for i in range(2):
                if self.points[i] > highest:
                    x = i
                    highest = self.points[i]
                    tie = False
                    REDO = False
                elif self.points[i] == highest:
                    tie = True
                    REDO = True
                self.points[i] = 0
            self.broadcastToVisitors(PlayerShopPacket.getMiniGameResult(this, tie ? 1 : 2, x))
            self.setOpen(True)
            self.update()
            self.checkExitAfterGame()

    def getOwnerPoints(self, slot: int) -> int:
        return self.points[slot]

    def setPieceType(self, type: int) -> None:
        self.piecetype = type

    def getPieceType(self) -> int:
        return self.piecetype

    def setGameType(self) -> None:
        if self.GameType == 2:
            self.matchcards.clear()
            for i in range(self.getMatchesToWin()):
                self.matchcards.add(i)
                self.matchcards.add(i)

    def shuffleList(self) -> None:
        if self.GameType == 2:
            Collections.shuffle(self.matchcards)
        else:
            self.piece = new int[15][15]

    def getCardId(self, slot: int) -> int:
        return self.matchcards.get(slot - 1)

    def getMatchesToWin(self) -> int:
        return (self.getPieceType() == 0) ? 6 : ((self.getPieceType() == 1) ? 10 : 15)

    def setLoser(self, type: int) -> None:
        self.loser = type

    def getLoser(self) -> int:
        return self.loser

    def send(self, c: Any) -> None:
        if self.getMCOwner() is None:
            self.closeShop(False, False)
            return
        c.getSession().write(PlayerShopPacket.getMiniGame(c, this))

    def setReady(self, slot: int) -> None:
        self.ready[slot] = !self.ready[slot]

    def isReady(self, slot: int) -> bool:
        return self.ready[slot]

    def setPiece(self, move1: int, move2: int, type: int, chr: Any) -> None:
        if self.piece[move1][move2] == 0 && !self.isOpen():
            self.piece[move1][move2] = type
            self.broadcastToVisitors(PlayerShopPacket.getMiniGameMoveOmok(move1, move2, type))
            found = False
            for y in range(15):
                for x in range(15):
                    if !found && self.searchCombo(x, y, type):
                        self.broadcastToVisitors(PlayerShopPacket.getMiniGameResult(this, 2, self.getVisitorSlot(chr)))
                        self.setOpen(True)
                        self.update()
                        self.checkExitAfterGame()
                        found = True
            self.nextLoser()

    def nextLoser(self) -> None:
        self.loser += 1
        if self.loser > 1:
            self.loser = 0

    def exit(self, player: Any) -> None:
        if player is None:
            return
        player.setPlayerShop(None)
        if self.isOwner(player):
            self.update()
            self.removeAllVisitors(3, 1)
        else:
            self.removeVisitor(player)

    def isExitAfter(self, player: Any) -> bool:
        return self.getVisitorSlot(player) > -1 && self.exitAfter[self.getVisitorSlot(player)]

    def setExitAfter(self, player: Any) -> None:
        if self.getVisitorSlot(player) > -1:
            self.exitAfter[self.getVisitorSlot(player)] = !self.exitAfter[self.getVisitorSlot(player)]

    def checkExitAfterGame(self) -> None:
        for i in range(2):
            if self.exitAfter[i]:
                self.exitAfter[i] = False
                self.exit((i == 0) ? self.getMCOwner() : self.chrs[i - 1].get())

    def searchCombo(self, x: int, y: int, type: int) -> bool:
        ret = False
        if !ret && x < 11:
            ret = True
            for i in range(5):
                if self.piece[x + i][y] != type:
                    ret = False
                    break
        if !ret && y < 11:
            ret = True
            for i in range(5):
                if self.piece[x][y + i] != type:
                    ret = False
                    break
        if !ret && x < 11 && y < 11:
            ret = True
            for i in range(5):
                if self.piece[x + i][y + i] != type:
                    ret = False
                    break
        if !ret && x > 3 && y < 11:
            ret = True
            for i in range(5):
                if self.piece[x - i][y + i] != type:
                    ret = False
                    break
        return ret

    def getScore(self, chr: Any) -> int:
        score = 2000
        wins = self.getWins(chr)
        ties = self.getTies(chr)
        losses = self.getLosses(chr)
        if wins + ties + losses > 0:
            score += wins * 2
            score += ties
            score -= losses * 2
        return score

    def getShopType(self) -> int:
        return (byte)((self.GameType == 1) ? 3 : 4)

    def getWins(self, chr: Any) -> int:
        return int(self.getData(chr).split(",")[2])

    def getTies(self, chr: Any) -> int:
        return int(self.getData(chr).split(",")[1])

    def getLosses(self, chr: Any) -> int:
        return int(self.getData(chr).split(",")[0])

    def setPoints_i_type(self, i: int, type: int) -> None:
        z = None
        if i == 0:
            z = self.getMCOwner()
        else:
            z = self.getVisitor(i - 1)
        if z is not None:
            data = self.getData(z).split(",")
            data[type] = str(int(data[type]) + 1)
            newData = ""
            for s in range(len(data)):
                newData.append(data[s])
                newData.append(",")
            newDat = newData
            z.getQuestNAdd(MapleQuest.getInstance((self.GameType == 1) ? GameConstants.OMOK_SCORE : GameConstants.MATCH_SCORE)).setCustomData(newDat[0:newDat.__len__(] - 1))

    def getData(self, chr: Any) -> str:
        quest = MapleQuest.getInstance((self.GameType == 1) ? GameConstants.OMOK_SCORE : GameConstants.MATCH_SCORE)
        record = None
        if chr.getQuestNoAdd(quest) is None:
            record = chr.getQuestNAdd(quest)
            record.setCustomData("0,0,0")
        else:
            record = chr.getQuestNoAdd(quest)
            if record.getCustomData() is None || record.getCustomData() < 5 || record.getCustomData().find(",") == -1:
                record.setCustomData("0,0,0")
        return record.getCustomData()

    def getRequestedTie(self) -> int:
        return self.tie

    def setRequestedTie(self, t: int) -> None:
        self.tie = t

    def getRequestedREDO(self) -> int:
        return self.REDO

    def setRequestedREDO(self, t: int) -> None:
        self.REDO = t

    def getTurn(self) -> int:
        return self.turn

    def setTurn(self, t: int) -> None:
        self.turn = t

    def closeShop(self, s: bool, z: bool) -> None:
        self.removeAllVisitors(3, 1)
        if self.getMCOwner() is not None:
            self.getMCOwner().setPlayerShop(None)
        self.update()
        self.getMap().removeMapObject(this)

    def buy(self, c: Any, z: int, i: int) -> None:
        pass

