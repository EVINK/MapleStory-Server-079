"""
MapleDataEntry - 从Java源文件转换而来
对应Java源文件: provider/MapleDataEntry.java
包路径: provider
"""


from abc import ABC, abstractmethod

class MapleDataEntry(ABC):
    """接口 MapleDataEntry - 从Java接口转换"""

    @abstractmethod
    def get_name(self) -> Any:
        """抽象方法 getName"""
        pass

    @abstractmethod
    def get_size(self) -> Any:
        """抽象方法 getSize"""
        pass

    @abstractmethod
    def get_checksum(self) -> Any:
        """抽象方法 getChecksum"""
        pass

    @abstractmethod
    def get_offset(self) -> Any:
        """抽象方法 getOffset"""
        pass

