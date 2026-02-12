"""
ByteBufferLittleEndianWriter - 从Java源文件转换而来
对应Java源文件: tools/data/output/ByteBufferLittleEndianWriter.java
包路径: tools.data.output
"""

from io import BytesIO
import asyncio
import struct


class ByteBufferLittleEndianWriter(GenericLittleEndianWriter):
    """
    类 ByteBufferLittleEndianWriter - 从Java类转换
    继承自: GenericLittleEndianWriter
    """

    def __init__(self):
        """初始化 ByteBufferLittleEndianWriter"""
        self.bb = None


    def getFlippedBB(self) -> Any:
        """方法 getFlippedBB"""
        raise NotImplementedError("方法 getFlippedBB 尚未实现")

    def getByteBuffer(self) -> Any:
        """方法 getByteBuffer"""
        raise NotImplementedError("方法 getByteBuffer 尚未实现")

