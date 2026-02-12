"""
InputStreamByteStream - 从Java源文件转换而来
对应Java源文件: tools/data/input/InputStreamByteStream.java
包路径: tools.data.input
"""

from io import IOBase
import os


class InputStreamByteStream(ByteInputStream):
    """
    类 InputStreamByteStream - 从Java类转换
    实现接口: ByteInputStream
    """

    def __init__(self, is: Any):
        """初始化 InputStreamByteStream"""
        self.is = None
        self.read = 0


    def readByte(self) -> int:
        """方法 readByte"""
        return 0

    def getBytesRead(self) -> int:
        """方法 getBytesRead"""
        return getattr(self, 'bytes_read', 0)

    def available(self) -> int:
        """方法 available"""
        return 0

    def toString(self, b: bool) -> str:
        """方法 toString"""
        return ""

