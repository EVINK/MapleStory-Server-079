"""
GenericSeekableLittleEndianAccessor - 从Java源文件转换而来
对应Java源文件: tools/data/input/GenericSeekableLittleEndianAccessor.java
包路径: tools.data.input
"""

import os


class GenericSeekableLittleEndianAccessor(GenericLittleEndianAccessor, SeekableLittleEndianAccessor):
    """
    类 GenericSeekableLittleEndianAccessor - 从Java类转换
    继承自: GenericLittleEndianAccessor
    实现接口: SeekableLittleEndianAccessor
    """

    def __init__(self, bs: Any):
        """初始化 GenericSeekableLittleEndianAccessor"""
        self.bs = None


    def seek(self, offset: int) -> None:
        """方法 seek"""
        pass

    def getPosition(self) -> int:
        """方法 getPosition"""
        return getattr(self, 'position', 0)

    def skip(self, num: int) -> None:
        """方法 skip"""
        pass

