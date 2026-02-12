"""
MapleDataProvider - 从Java源文件转换而来
对应Java源文件: provider/MapleDataProvider.java
包路径: provider
"""


from abc import ABC, abstractmethod

class MapleDataProvider(ABC):
    """接口 MapleDataProvider - 从Java接口转换"""

    @abstractmethod
    def get_data(self, p0: str) -> Any:
        """抽象方法 getData"""
        pass

    @abstractmethod
    def get_root(self) -> Any:
        """抽象方法 getRoot"""
        pass

