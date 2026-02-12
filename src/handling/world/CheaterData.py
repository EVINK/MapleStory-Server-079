"""
CheaterData - 从Java源文件转换而来
对应Java源文件: handling/world/CheaterData.java
包路径: handling.world
"""

from typing import Optional, Any


class CheaterData:
    """
    类 CheaterData - 从Java类转换
    实现接口: Serializable, Comparable<CheaterData>
    """

    # 静态字段 (Static fields)
    serialVersionUID = -8733673311051249885

    def __init__(self, points: int, info: str):
        """初始化 CheaterData"""
        self.points = None
        self.info = None


    def getInfo(self) -> str:
        """方法 getInfo"""
        return getattr(self, 'info', "")

    def getPoints(self) -> int:
        """方法 getPoints"""
        return getattr(self, 'points', 0)

    def compareTo(self, o: Any) -> int:
        """方法 compareTo"""
        return 0

    def equals(self, oth: Any) -> bool:
        """方法 equals"""
        return self is oth or getattr(self, '__eq__', lambda o: False)(oth)

