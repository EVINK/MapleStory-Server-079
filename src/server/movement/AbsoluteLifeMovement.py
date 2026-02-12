"""
AbsoluteLifeMovement - 从Java源文件转换而来
对应Java源文件: server/movement/AbsoluteLifeMovement.java
包路径: server.movement
"""

from dataclasses import dataclass

# 内部模块导入 (Internal module imports)
# from tools.data.output.LittleEndianWriter import *  # TODO: 根据实际需要导入具体类


class AbsoluteLifeMovement(AbstractLifeMovement):
    """
    类 AbsoluteLifeMovement - 从Java类转换
    继承自: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        """初始化 AbsoluteLifeMovement"""
        self.pixelsPerSecond = None
        self.offset = None
        self.unk = 0


    def getPixelsPerSecond(self) -> Any:
        """方法 getPixelsPerSecond"""
        return getattr(self, 'pixels_per_second', None)

    def setPixelsPerSecond(self, wobble: Any) -> None:
        """方法 setPixelsPerSecond"""
        self.pixels_per_second = wobble
        return None

    def getOffset(self) -> Any:
        """方法 getOffset"""
        return getattr(self, 'offset', None)

    def setOffset(self, wobble: Any) -> None:
        """方法 setOffset"""
        self.offset = wobble
        return None

    def getUnk(self) -> int:
        """方法 getUnk"""
        return getattr(self, 'unk', 0)

    def setUnk(self, unk: int) -> None:
        """方法 setUnk"""
        self.unk = unk
        return None

    def serialize(self, lew: Any) -> None:
        """方法 serialize"""
        pass

