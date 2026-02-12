"""
MapleOxQuizFactory - Converted from Java source
Original: server/events/MapleOxQuizFactory.java
Package: server.events
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleOxQuizFactory:
    """
    Class MapleOxQuizFactory
    """

    def __init__(self):
        self.initialized = False
        self.questionCache = None
        self.question = None
        self.answerText = None
        self.answer = None
        self.questionset = None
        self.questionid = None
        self.initialized = False
        self.questionCache = new HashMap<Pair<Integer, Integer>, MapleOxQuizEntry>()

    # Static initializer
    # instance = MapleOxQuizFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getOxEntry(self, questionSet: int, questionId: int) -> Any:
        return getInstance().getOxQuizEntry(new Pair<Integer, Integer>(questionSet, questionId))

    def getOxEntry_pair(self, pair: Any) -> Any:
        return getInstance().getOxQuizEntry(pair)

    def hasInitialized(self) -> bool:
        return self.initialized

    def grabRandomQuestion(self) -> Any:
        size = self.questionCache
        while True:
            for (Map.Entry<Pair<Integer, Integer>, MapleOxQuizEntry> oxquiz : self.questionCache.items())
                if Randomizer.nextInt(size) == 0:
                return oxquiz

    def initialize(self) -> None:
        if self.initialized:
            return
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM wz_oxdata")
            rs = ps.executeQuery()
            while rs.next():
                self.questionCache.put(new Pair<Integer, Integer>(rs.getInt("questionset"), rs.getInt("questionid")), self.get(rs))
            rs.close()
            ps.close()
        except Exception as e:
            e.printStackTrace()
        print("Done\r")
        self.initialized = True

    def getFromSQL(self, sql: str) -> Any:
        ret = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement(sql)
            rs = ps.executeQuery()
            if rs.next():
                ret = self.get(rs)
            rs.close()
            ps.close()
        except Exception as e:
            e.printStackTrace()
        return ret

    def getOxQuizEntry(self, pair: Any) -> Any:
        mooe = self.questionCache.get(pair)
        if mooe is None:
            if self.initialized:
                return None
            mooe = self.getFromSQL("SELECT * FROM wz_oxdata WHERE questionset = " + pair.getLeft() + " AND questionid = " + pair.getRight())
            self.questionCache.put(pair, mooe)
        return mooe

    def get(self, rs: Any) -> Any:
        return MapleOxQuizEntry(rs.getString("question"), rs.getString("display"), self.getAnswerByText(rs.getString("answer")), rs.getInt("questionset"), rs.getInt("questionid"))

    def getAnswerByText(self, text: str) -> int:
        if text.lower() == "x".lower():
            return 0
        if text.lower() == "o".lower():
            return 1
        return -1

    def getQuestion(self) -> str:
        return self.question

    def getAnswerText(self) -> str:
        return self.answerText

    def getAnswer(self) -> int:
        return self.answer

    def getQuestionSet(self) -> int:
        return self.questionset

    def getQuestionId(self) -> int:
        return self.questionid


# Inner class from Java (originally nested)
class MapleOxQuizEntry:
    """
    Class MapleOxQuizEntry
    """

    def __init__(self, question: str, answerText: str, answer: int, questionset: int, questionid: int):
        self.question = None
        self.answerText = None
        self.answer = None
        self.questionset = None
        self.questionid = None
        self.question = question
        self.answerText = answerText
        self.answer = answer
        self.questionset = questionset
        self.questionid = questionid


    def getQuestion(self) -> str:
        return self.question

    def getAnswerText(self) -> str:
        return self.answerText

    def getAnswer(self) -> int:
        return self.answer

    def getQuestionSet(self) -> int:
        return self.questionset

    def getQuestionId(self) -> int:
        return self.questionid

