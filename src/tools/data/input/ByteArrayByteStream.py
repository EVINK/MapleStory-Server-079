"""
ByteArrayByteStream - 从Java源文件转换而来
对应Java源文件: tools/data/input/ByteArrayByteStream.java
包路径: tools.data.input
"""

import os

# 内部模块导入 (Internal module imports)
# from tools.HexTool import *  # TODO: 根据实际需要导入具体类


class ByteArrayByteStream(SeekableInputStreamBytestream):
    """
    类 ByteArrayByteStream - 从Java类转换
    实现接口: SeekableInputStreamBytestream
    """

    def __init__(self, arr: bytes):
        """初始化 ByteArrayByteStream"""
        self.pos = 0
        self.bytesRead = 0


    def getPosition(self) -> int:
        """方法 getPosition"""
        return getattr(self, 'position', 0)

    def seek(self, offset: int) -> None:
        """方法 seek"""
        pass

    def getBytesRead(self) -> int:
        """方法 getBytesRead"""
        return getattr(self, 'bytes_read', 0)

    def readByte(self) -> int:
        """方法 readByte"""
        return 0

    def toString(self) -> str:
        """方法 toString"""
        return ""

    def toString(self, b: bool) -> str:
        """方法 toString"""
        return ""

    def available(self) -> int:
        """方法 available"""
        return 0

