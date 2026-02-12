"""
MapleFoothold - 从Java源文件转换而来
对应Java源文件: server/maps/MapleFoothold.java
包路径: server.maps
"""

from dataclasses import dataclass
from typing import Optional, Any


class MapleFoothold:
    """
    类 MapleFoothold - 从Java类转换
    实现接口: Comparable<MapleFoothold>
    """

    def __init__(self, p1: Any, p2: Any, id: int):
        """初始化 MapleFoothold"""
        self.p1 = None
        self.p2 = None
        self.id = None
        self.next = 0
        self.prev = 0


    def isWall(self) -> bool:
        """方法 isWall"""
        return False

    def getX1(self) -> int:
        """方法 getX1"""
        return 0

    def getX2(self) -> int:
        """方法 getX2"""
        return 0

    def getY1(self) -> int:
        """方法 getY1"""
        return 0

    def getY2(self) -> int:
        """方法 getY2"""
        return 0

    def compareTo(self, o: Any) -> int:
        """方法 compareTo"""
        return 0

    def equals(self, o: Any) -> bool:
        """方法 equals"""
        return False

    def getId(self) -> int:
        """方法 getId"""
        return 0

    def getNext(self) -> int:
        """方法 getNext"""
        return 0

    def setNext(self, next: int) -> None:
        """方法 setNext"""
        pass

    def getPrev(self) -> int:
        """方法 getPrev"""
        return 0

    def setPrev(self, prev: int) -> None:
        """方法 setPrev"""
        pass

