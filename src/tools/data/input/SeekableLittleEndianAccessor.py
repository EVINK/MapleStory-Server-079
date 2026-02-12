"""
SeekableLittleEndianAccessor - 从Java源文件转换而来
对应Java源文件: tools/data/input/SeekableLittleEndianAccessor.java
包路径: tools.data.input
"""


from abc import ABC, abstractmethod

class SeekableLittleEndianAccessor(ABC):
    """接口 SeekableLittleEndianAccessor - 从Java接口转换"""

    @abstractmethod
    def seek(self, p0: int) -> Any:
        """抽象方法 seek"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

