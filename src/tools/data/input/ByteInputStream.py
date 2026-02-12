"""
ByteInputStream - 从Java源文件转换而来
对应Java源文件: tools/data/input/ByteInputStream.java
包路径: tools.data.input
"""


from abc import ABC, abstractmethod

class ByteInputStream(ABC):
    """接口 ByteInputStream - 从Java接口转换"""

    @abstractmethod
    def read_byte(self) -> Any:
        """抽象方法 readByte"""
        pass

    @abstractmethod
    def get_bytes_read(self) -> Any:
        """抽象方法 getBytesRead"""
        pass

    @abstractmethod
    def available(self) -> Any:
        """抽象方法 available"""
        pass

    @abstractmethod
    def to_string(self, p0: bool) -> Any:
        """抽象方法 toString"""
        pass

