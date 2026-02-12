"""
RandomAccessByteStream - 从Java源文件转换而来
对应Java源文件: tools/data/input/RandomAccessByteStream.java
包路径: tools.data.input
"""

from io import open
import os


class RandomAccessByteStream(SeekableInputStreamBytestream):
    """
    类 RandomAccessByteStream - 从Java类转换
    实现接口: SeekableInputStreamBytestream
    """

    def __init__(self, raf: Any):
        """初始化 RandomAccessByteStream"""
        self.raf = None
        self.read = 0


    def readByte(self) -> int:
        """方法 readByte"""
        return 0

    def seek(self, offset: int) -> None:
        """方法 seek"""
        pass

    def getPosition(self) -> int:
        """方法 getPosition"""
        return getattr(self, 'position', 0)

    def getBytesRead(self) -> int:
        """方法 getBytesRead"""
        return getattr(self, 'bytes_read', 0)

    def available(self) -> int:
        """方法 available"""
        return 0

    def toString(self, b: bool) -> str:
        """方法 toString"""
        return ""

