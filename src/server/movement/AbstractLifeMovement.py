"""
AbstractLifeMovement - 从Java源文件转换而来
对应Java源文件: server/movement/AbstractLifeMovement.java
包路径: server.movement
"""

from dataclasses import dataclass


class AbstractLifeMovement(LifeMovement, ABC):
    """
    类 AbstractLifeMovement - 从Java类转换
    实现接口: LifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        """初始化 AbstractLifeMovement"""
        self.position = None
        self.duration = 0
        self.newstate = 0
        self.type = 0


    def getType(self) -> int:
        """方法 getType"""
        return getattr(self, 'type', 0)

    def getDuration(self) -> int:
        """方法 getDuration"""
        return getattr(self, 'duration', 0)

    def getNewstate(self) -> int:
        """方法 getNewstate"""
        return getattr(self, 'newstate', 0)

    def getPosition(self) -> Any:
        """方法 getPosition"""
        return getattr(self, 'position', None)

