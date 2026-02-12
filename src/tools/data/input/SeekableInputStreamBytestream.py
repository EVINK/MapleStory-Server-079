"""
SeekableInputStreamBytestream - 从Java源文件转换而来
对应Java源文件: tools/data/input/SeekableInputStreamBytestream.java
包路径: tools.data.input
"""

import os


from abc import ABC, abstractmethod

class SeekableInputStreamBytestream(ABC):
    """接口 SeekableInputStreamBytestream - 从Java接口转换"""

    @abstractmethod
    def seek(self, p0: int) -> Any:
        """抽象方法 seek"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

    @abstractmethod
    def to_string(self, p0: bool) -> Any:
        """抽象方法 toString"""
        pass

