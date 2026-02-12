"""
Forum_Thread - Converted from Java source
Original: server/custom/forum/Forum_Thread.java
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


class Forum_Thread:
    """
    Class Forum_Thread
    """

    def __init__(self):
        self.ThreadId = 0
        self.sectionId = 0
        self.threadName = ""
        self.characterId = 0
        self.characterName = ""
        self.releaseTime = ""
        self.up = 0
        self.down = 0

    # Static initializer
    # Forum_Thread.allThread = []


    def getThreadId(self) -> int:
        return self.ThreadId

    def setThreadId(self, threadId: int) -> None:
        self.ThreadId = threadId

    def getSectionId(self) -> int:
        return self.sectionId

    def setSectionId(self, sectionId: int) -> None:
        self.sectionId = sectionId

    def getThreadName(self) -> str:
        return self.threadName

    def setThreadName(self, threadName: str) -> None:
        self.threadName = threadName

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

    def getUp(self) -> int:
        return self.up

    def setUp(self, up: int) -> None:
        self.up = up

    def getDown(self) -> int:
        return self.down

    def setDown(self, down: int) -> None:
        self.down = down

    def getAllThread(self) -> list:
        return Forum_Thread.allThread

    def setAllThread(self, allThread: list) -> None:
        Forum_Thread.allThread = allThread

    def getCurrentAllThread(self, sid: int) -> list:
        CurrentThread = []
        for ft in Forum_Thread.allThread:
            if ft.getSectionId() == sid:
                CurrentThread.add(ft)
        return CurrentThread

    def loadAllThread(self) -> list:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_thread")
            rs = ps.executeQuery()
            while rs.next():
                Forum_Thread.allThread.add(Forum_Thread(rs.getInt("tid"), rs.getInt("sid"), rs.getString("tname"), rs.getInt("cid"), rs.getString("cname"), rs.getString("time"), rs.getInt("up"), rs.getInt("down")))
            rs.close()
            ps.close()
            Forum_Reply.loadAllReply()
            return Forum_Thread.allThread
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return None

    def getThreadById(self, sid: int, tid: int) -> Any:
        for ft in Forum_Thread.allThread:
            if ft.getThreadId() == tid:
                return ft
        return None

    def getThreadByName(self, sid: int, name: str) -> Any:
        allThread = getCurrentAllThread(sid)
        for ft in allThread:
            if ft.getThreadName() == (name):
                return ft
        return None

    def getThreadByNameToSql(self, sid: int, name: str) -> Any:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_thread WHERE sid = ? AND tname = ?")
            ps.setInt(1, sid)
            ps.setString(2, name)
            rs = ps.executeQuery()
            if rs.next():
                return Forum_Thread(rs.getInt("tid"), rs.getInt("sid"), rs.getString("tname"), rs.getInt("cid"), rs.getString("cname"), rs.getString("time"), rs.getInt("up"), rs.getInt("down"))
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
        return None

    def addThread(self, sid: int, tname: str, cid: int, cname: str) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            if getThreadByName(sid, tname) is not None:
                return False
            query = ""
            query.append("INSERT INTO forum_thread(sid, tname, cid, cname) VALUES (?,?,?,?)")
            ps = con.prepareStatement(query)
            ps.setInt(1, sid)
            ps.setString(2, tname)
            ps.setInt(3, cid)
            ps.setString(4, cname)
            ps.executeUpdate()
            ps.close()
            Forum_Thread.allThread.add(getThreadByNameToSql(sid, tname))
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

    def deleteThread(self, sid: int, tid: int, isAll: bool) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            isExist = False
            if isAll:
                if getCurrentAllThread(sid) is not None:
                    for ft in Forum_Thread.allThread:
                        if ft.getSectionId() == sid:
                            Forum_Reply.deleteReply(ft.getThreadId(), 0, True)
                    Forum_Thread.allThread.removeAll(getCurrentAllThread(sid))
                    isExist = True
            elif getThreadById(sid, tid) is not None:
                Forum_Thread.allThread.remove(getThreadById(sid, tid))
                Forum_Reply.deleteReply(tid, 0, True)
                isExist = True
            if not isExist:
                return isExist
            query = ""
            if isAll:
                query.append("DELETE FROM forum_thread WHERE sid = ?")
            else:
                query.append("DELETE FROM forum_thread WHERE sid = ? AND tid = ?")
            ps = con.prepareStatement(query)
            ps.setInt(1, sid)
            if not isAll:
                ps.setInt(2, tid)
            ps.executeUpdate()
            ps.close()
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

