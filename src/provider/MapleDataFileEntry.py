"""
MapleDataFileEntry - 从Java源文件转换而来
对应Java源文件: provider/MapleDataFileEntry.java
包路径: provider
"""


from abc import ABC, abstractmethod

class MapleDataFileEntry(ABC):
    """接口 MapleDataFileEntry - 从Java接口转换"""

    @abstractmethod
    def set_offset(self, p0: int) -> Any:
        """抽象方法 setOffset"""
        pass

