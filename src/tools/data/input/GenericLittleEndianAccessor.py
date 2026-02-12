"""
GenericLittleEndianAccessor - 从Java源文件转换而来
对应Java源文件: tools/data/input/GenericLittleEndianAccessor.java
包路径: tools.data.input
"""

from dataclasses import dataclass
from typing import Optional, Any


class GenericLittleEndianAccessor(LittleEndianAccessor):
    """
    类 GenericLittleEndianAccessor - 从Java类转换
    实现接口: LittleEndianAccessor
    """

    def __init__(self, bs: Any):
        """初始化 GenericLittleEndianAccessor"""
        self.bs = None


    def readByteAsInt(self) -> int:
        """方法 readByteAsInt"""
        return 0

    def readByte(self) -> int:
        """方法 readByte"""
        return 0

    def readInt(self) -> int:
        """方法 readInt"""
        return 0

    def readShort(self) -> int:
        """方法 readShort"""
        return 0

    def readChar(self) -> str:
        """方法 readChar"""
        return ""

    def readLong(self) -> int:
        """方法 readLong"""
        return 0

    def readFloat(self) -> float:
        """方法 readFloat"""
        return 0

    def readDouble(self) -> float:
        """方法 readDouble"""
        return 0

    def readAsciiString(self, n: int) -> str:
        """方法 readAsciiString"""
        return ""

    def getBytesRead(self) -> int:
        """方法 getBytesRead"""
        return 0

    def readMapleAsciiString(self) -> str:
        """方法 readMapleAsciiString"""
        return ""

    def readPos(self) -> Any:
        """方法 readPos"""
        raise NotImplementedError("方法 readPos 尚未实现")

    def read(self, num: int) -> bytes:
        """方法 read"""
        return b""

    def skip(self, num: int) -> None:
        """方法 skip"""
        pass

    def available(self) -> int:
        """方法 available"""
        return 0

    def toString(self) -> str:
        """方法 toString"""
        return ""

    def toString(self, b: bool) -> str:
        """方法 toString"""
        return ""

