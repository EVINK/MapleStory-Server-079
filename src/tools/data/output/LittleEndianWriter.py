"""
LittleEndianWriter - 从Java源文件转换而来
对应Java源文件: tools/data/output/LittleEndianWriter.java
包路径: tools.data.output
"""

from dataclasses import dataclass


from abc import ABC, abstractmethod

class LittleEndianWriter(ABC):
    """接口 LittleEndianWriter - 从Java接口转换"""

    @abstractmethod
    def write_zero_bytes(self, p0: int) -> Any:
        """抽象方法 writeZeroBytes"""
        pass

    @abstractmethod
    def write(self, p0: bytes) -> Any:
        """抽象方法 write"""
        pass

    @abstractmethod
    def write(self, p0: int) -> Any:
        """抽象方法 write"""
        pass

    @abstractmethod
    def write(self, p0: int) -> Any:
        """抽象方法 write"""
        pass

    @abstractmethod
    def write_int(self, p0: int) -> Any:
        """抽象方法 writeInt"""
        pass

    @abstractmethod
    def write_short(self, p0: int) -> Any:
        """抽象方法 writeShort"""
        pass

    @abstractmethod
    def write_short(self, p0: int) -> Any:
        """抽象方法 writeShort"""
        pass

    @abstractmethod
    def write_long(self, p0: int) -> Any:
        """抽象方法 writeLong"""
        pass

    @abstractmethod
    def write_ascii_string(self, p0: str) -> Any:
        """抽象方法 writeAsciiString"""
        pass

    @abstractmethod
    def write_ascii_string(self, p0: str, p1: int) -> Any:
        """抽象方法 writeAsciiString"""
        pass

    @abstractmethod
    def write_pos(self, p0: Any) -> Any:
        """抽象方法 writePos"""
        pass

    @abstractmethod
    def write_maple_ascii_string(self, p0: str) -> Any:
        """抽象方法 writeMapleAsciiString"""
        pass

