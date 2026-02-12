"""
Forum_Reply - Converted from Java source
Original: server/custom/forum/Forum_Reply.java
Package: server.custom.forum
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import pymysql
import threading

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes


class Forum_Reply:
    """
    Class Forum_Reply
    """

    def __init__(self):
        self.replyId = 0
        self.threadId = 0
        self.characterId = 0
        self.characterName = ""
        self.releaseTime = ""
        self.news = ""

    # Static initializer
    # Forum_Reply.allReply = []


    def getReplyId(self) -> int:
        return self.replyId

    def setReplyId(self, replyId: int) -> None:
        self.replyId = replyId

    def getThreadId(self) -> int:
        return self.threadId

    def setThreadId(self, threadId: int) -> None:
        self.threadId = threadId

    def getCharacterId(self) -> int:
        return self.characterId

    def setCharacterId(self, characterId: int) -> None:
        self.characterId = characterId

    def getCharacterName(self) -> str:
        return self.characterName

    def setCharacterName(self, characterName: str) -> None:
        self.characterName = characterName

    def getReleaseTime(self) -> str:
        return self.releaseTime

    def setReleaseTime(self, releaseTime: str) -> None:
        self.releaseTime = releaseTime

    def getNews(self) -> str:
        return self.news

    def setNews(self, news: str) -> None:
        self.news = news

    def getAllReply(self) -> list:
        return Forum_Reply.allReply

    def setAllReply(self, allReply: list) -> None:
        Forum_Reply.allReply = allReply

    def getCurrentAllReply(self, tid: int) -> list:
        CurrentReply = []
        for fr in Forum_Reply.allReply:
            if fr.getThreadId() == tid:
                CurrentReply.add(fr)
        return CurrentReply

    def loadAllReply(self) -> list:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_reply")
            rs = ps.executeQuery()
            while rs.next():
                Forum_Reply.allReply.add(Forum_Reply(rs.getInt("rid"), rs.getInt("tid"), rs.getInt("cid"), rs.getString("cname"), rs.getString("time"), rs.getString("news")))
            rs.close()
            ps.close()
            return Forum_Reply.allReply
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return None

    def addReply(self, tid: int, cid: int, cname: str, news: str) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            query = ""
            query.append("INSERT INTO forum_reply(tid, cid, cname, news) VALUES (?,?,?,?)")
            ps = con.prepareStatement(query)
            ps.setInt(1, tid)
            ps.setInt(2, cid)
            ps.setString(3, cname)
            ps.setString(4, news)
            ps.executeUpdate()
            ps.close()
            Forum_Reply.allReply.add(getReplyByNameToSql(tid, news))
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

    def getReplyById(self, rid: int) -> Any:
        for fr in Forum_Reply.allReply:
            if fr.getReplyId() == rid:
                return fr
        return None

    def getReplyByNameToSql(self, tid: int, news: str) -> Any:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_reply WHERE tid = ? AND news = ?")
            ps.setInt(1, tid)
            ps.setString(2, news)
            rs = ps.executeQuery()
            if rs.next():
                return Forum_Reply(rs.getInt("rid"), rs.getInt("tid"), rs.getInt("cid"), rs.getString("cname"), rs.getString("time"), rs.getString("news"))
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
        return None

    def deleteReply(self, tid: int, rid: int, isAll: bool) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            isExist = False
            if isAll:
                if getCurrentAllReply(tid) is not None:
                    Forum_Reply.allReply.removeAll(getCurrentAllReply(tid))
                    isExist = True
            elif getReplyById(rid) is not None:
                Forum_Reply.allReply.remove(getReplyById(rid))
                isExist = True
            if not isExist:
                return isExist
            query = ""
            if isAll:
                query.append("DELETE FROM forum_reply WHERE tid = ?")
            else:
                query.append("DELETE FROM forum_reply WHERE tid = ? AND rid = ?")
            ps = con.prepareStatement(query)
            ps.setInt(1, tid)
            if not isAll:
                ps.setInt(2, rid)
            ps.executeUpdate()
            ps.close()
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

