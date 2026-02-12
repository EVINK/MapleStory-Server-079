"""
CheatingOffenseEntry - 从Java源文件转换而来
对应Java源文件: client/anticheat/CheatingOffenseEntry.java
包路径: client.anticheat
"""

from typing import Optional, Any
import time


class CheatingOffenseEntry:
    """
    类 CheatingOffenseEntry - 从Java类转换
    """

    def __init__(self, offense: Any, characterid: int):
        """初始化 CheatingOffenseEntry"""
        self.offense = None
        self.count = 0
        self.characterid = None
        self.lastOffense = 0
        self.firstOffense = None
        self.param = ""
        self.dbid = 0


    def getOffense(self) -> Any:
        """方法 getOffense"""
        raise NotImplementedError("方法 getOffense 尚未实现")

    def getCount(self) -> int:
        """方法 getCount"""
        return 0

    def getChrfor(self) -> int:
        """方法 getChrfor"""
        return 0

    def incrementCount(self) -> None:
        """方法 incrementCount"""
        pass

    def isExpired(self) -> bool:
        """方法 isExpired"""
        return False

    def getPoints(self) -> int:
        """方法 getPoints"""
        return 0

    def getParam(self) -> str:
        """方法 getParam"""
        return ""

    def setParam(self, param: str) -> None:
        """方法 setParam"""
        pass

    def getLastOffenseTime(self) -> int:
        """方法 getLastOffenseTime"""
        return 0

    def getDbId(self) -> int:
        """方法 getDbId"""
        return 0

    def setDbId(self, dbid: int) -> None:
        """方法 setDbId"""
        pass

