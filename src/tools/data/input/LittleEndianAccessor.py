"""
LittleEndianAccessor - 从Java源文件转换而来
对应Java源文件: tools/data/input/LittleEndianAccessor.java
包路径: tools.data.input
"""

from dataclasses import dataclass


from abc import ABC, abstractmethod

class LittleEndianAccessor(ABC):
    """接口 LittleEndianAccessor - 从Java接口转换"""

    @abstractmethod
    def read_byte(self) -> Any:
        """抽象方法 readByte"""
        pass

    @abstractmethod
    def read_byte_as_int(self) -> Any:
        """抽象方法 readByteAsInt"""
        pass

    @abstractmethod
    def read_char(self) -> Any:
        """抽象方法 readChar"""
        pass

    @abstractmethod
    def read_short(self) -> Any:
        """抽象方法 readShort"""
        pass

    @abstractmethod
    def read_int(self) -> Any:
        """抽象方法 readInt"""
        pass

    @abstractmethod
    def read_long(self) -> Any:
        """抽象方法 readLong"""
        pass

    @abstractmethod
    def skip(self, p0: int) -> Any:
        """抽象方法 skip"""
        pass

    @abstractmethod
    def read_float(self) -> Any:
        """抽象方法 readFloat"""
        pass

    @abstractmethod
    def read_double(self) -> Any:
        """抽象方法 readDouble"""
        pass

    @abstractmethod
    def read_ascii_string(self, p0: int) -> Any:
        """抽象方法 readAsciiString"""
        pass

    @abstractmethod
    def read_maple_ascii_string(self) -> Any:
        """抽象方法 readMapleAsciiString"""
        pass

    @abstractmethod
    def read_pos(self) -> Any:
        """抽象方法 readPos"""
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

