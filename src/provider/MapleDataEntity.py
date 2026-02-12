"""
MapleDataEntity - 从Java源文件转换而来
对应Java源文件: provider/MapleDataEntity.java
包路径: provider
"""


from abc import ABC, abstractmethod

class MapleDataEntity(ABC):
    """接口 MapleDataEntity - 从Java接口转换"""

    @abstractmethod
    def get_name(self) -> Any:
        """抽象方法 getName"""
        pass

    @abstractmethod
    def get_parent(self) -> Any:
        """抽象方法 getParent"""
        pass

