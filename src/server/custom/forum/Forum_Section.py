"""
Forum_Section - Converted from Java source
Original: server/custom/forum/Forum_Section.java
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


class Forum_Section:
    """
    Class Forum_Section
    """

    def __init__(self):
        self.Id = 0
        self.Name = ""

    # Static initializer
    # Forum_Section.AllSection = []


    def getAllSection(self) -> list:
        return Forum_Section.AllSection

    def setAllSection(self, allSection: list) -> None:
        Forum_Section.AllSection = allSection

    def getId(self) -> int:
        return self.Id

    def setId(self, id: int) -> None:
        self.Id = id

    def getName(self) -> str:
        return self.Name

    def setName(self, name: str) -> None:
        self.Name = name

    def loadAllSection(self) -> list:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_section")
            rs = ps.executeQuery()
            while rs.next():
                id = rs.getInt("id")
                name = rs.getString("name")
                Forum_Section.AllSection.add(Forum_Section(id, name))
            rs.close()
            ps.close()
            Forum_Thread.loadAllThread()
            return Forum_Section.AllSection
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return None

    def addSection(self, name: str) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            if getSectionByName(name) is not None:
                return False
            query = ""
            query.append("INSERT INTO forum_sectionVALUES (?)")
            ps = con.prepareStatement(query)
            ps.setString(1, name)
            ps.executeUpdate()
            ps.close()
            Forum_Section.AllSection.add(getSectionByNameToSql(name))
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

    def deleteSection(self, id: int) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            isExist = False
            if getSectionById(id) is not None:
                Forum_Section.AllSection.remove(getSectionById(id))
                isExist = True
            if not isExist:
                return isExist
            Forum_Thread.deleteThread(id, 0, True)
            query2 = ""
            query2.append("DELETE FROM forum_section WHERE id = ?")
            ps = con.prepareStatement(query2)
            ps.setInt(1, id)
            ps.executeUpdate()
            ps.close()
            return True
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return False

    def getSectionById(self, id: int) -> Any:
        allSection = getAllSection()
        for fs in allSection:
            if fs.getId() == id:
                return fs
        return None

    def getSectionByIdToSql(self, id: int) -> Any:
        name = ""
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_section WHERE id = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if rs.next():
                name = rs.getString("name")
            return Forum_Section(id, name)
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return None

    def getSectionByName(self, name: str) -> Any:
        allSection = getAllSection()
        for fs in allSection:
            if fs.getName() == (name):
                return fs
        return None

    def getSectionByNameToSql(self, name: str) -> Any:
        id = 0
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM forum_section WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if rs.next():
                id = rs.getInt("id")
            return Forum_Section(id, name)
        except Exception as ex:
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
            return None

