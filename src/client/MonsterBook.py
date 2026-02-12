"""
MonsterBook - Converted from Java source
Original: client/MonsterBook.java
Package: client
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Optional, Any
import pymysql

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes
# from tools.packet.MonsterBookPacket import *  # TODO: import specific classes


class MonsterBook:
    """
    Class MonsterBook
    Implements: Serializable
    """

    serialVersionUID = 7179541993413738569

    def __init__(self, cards: dict):
        self.changed = False
        self.SpecialCard = 0
        self.NormalCard = 0
        self.BookLevel = 0
        self.cards = None
        self.changed = False
        self.SpecialCard = 0
        self.NormalCard = 0
        self.BookLevel = 1
        self.cards = cards
        for (final Map.Entry<Integer, Integer> card : cards.items())
            if GameConstants.isSpecialCard(card.getKey()):
                self.SpecialCard += card.getValue()
            else:
                self.NormalCard += card.getValue()
        self.calculateLevel()


    def loadCards(self, charid: int) -> Any:
        ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM monsterbook WHERE charid = ? ORDER BY cardid ASC")
        ps.setInt(1, charid)
        rs = ps.executeQuery()
        cards = {}
        while rs.next():
            cards.put(rs.getInt("cardid"), rs.getInt("level"))
        rs.close()
        ps.close()
        return MonsterBook(cards)

    def getCards(self) -> dict:
        return self.cards

    def getTotalCards(self) -> int:
        return self.SpecialCard + self.NormalCard

    def getLevelByCard(self, cardid: int) -> int:
        return (self.cards.get(cardid) is None) ? 0 : self.cards.get(cardid)

    def saveCards(self, charid: int) -> None:
        if !self.changed || self.cards == 0:
            return
        con = DatabaseConnection.getConnection()
        ps = None
        rs = None
        ps = con.prepareStatement("SELECT * FROM monsterbook WHERE `charid` = ? AND `cardid` = ? LIMIT 1")
        ps.setInt(1, charid)
        for (final Map.Entry<Integer, Integer> all : self.cards.items())
            ps2 = None
            cardid = all.getKey()
            ps.setInt(2, cardid)
            rs = ps.executeQuery()
            if rs.next():
                ps2 = con.prepareStatement("UPDATE monsterbook SET `level` = ? WHERE `charid` = ? AND `cardid` = ?")
                ps2.setInt(1, all.getValue())
                ps2.setInt(2, charid)
                ps2.setInt(3, cardid)
                ps2.executeUpdate()
                ps2.close()
            else:
                ps2 = con.prepareStatement("INSERT INTO monsterbook (`charid`, `cardid`, `level`) VALUES (?, ?, ?)")
                ps2.setInt(1, charid)
                ps2.setInt(2, cardid)
                ps2.setInt(3, all.getValue())
                ps2.execute()
                ps2.close()
            rs.close()
        ps.close()

    def calculateLevel(self) -> None:
        Size = self.NormalCard + self.SpecialCard
        self.BookLevel = 8
        for i in range(8):
            if Size <= GameConstants.getBookLevel(i):
                self.BookLevel = i + 1
                break

    def addCardPacket(self, mplew: Any) -> None:
        mplew.writeShort(self.cards)
        for (final Map.Entry<Integer, Integer> all : self.cards.items())
            mplew.writeShort(GameConstants.getCardShortId(all.getKey()))
            mplew.write(all.getValue())

    def addCharInfoPacket(self, bookcover: int, mplew: Any) -> None:
        mplew.writeInt(self.BookLevel)
        mplew.writeInt(self.NormalCard)
        mplew.writeInt(self.SpecialCard)
        mplew.writeInt(self.NormalCard + self.SpecialCard)
        mplew.writeInt(MapleItemInformationProvider.getInstance().getCardMobId(bookcover))

    def updateCard(self, c: Any, cardid: int) -> None:
        c.getSession().write(MonsterBookPacket.changeCover(cardid))

    def addCard(self, c: Any, cardid: int) -> None:
        self.changed = True
        if (cardid in self.cards):
            levels = self.cards.get(cardid)
            if levels >= 5:
                c.getSession().write(MonsterBookPacket.addCard(True, cardid, levels))
            else:
                if GameConstants.isSpecialCard(cardid):
                    self.SpecialCard += 1
                else:
                    self.NormalCard += 1
                c.getSession().write(MonsterBookPacket.addCard(False, cardid, levels))
                c.getSession().write(MonsterBookPacket.showGainCard(cardid))
                self.cards.put(cardid, levels + 1)
                self.calculateLevel()
            return
        if GameConstants.isSpecialCard(cardid):
            self.SpecialCard += 1
        else:
            self.NormalCard += 1
        self.cards.put(cardid, 1)
        c.getSession().write(MonsterBookPacket.addCard(False, cardid, 1))
        c.getSession().write(MonsterBookPacket.showGainCard(cardid))
        self.calculateLevel()

