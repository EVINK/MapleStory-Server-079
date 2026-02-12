"""
MapleCanvas - 从Java源文件转换而来
对应Java源文件: provider/MapleCanvas.java
包路径: provider
"""


from abc import ABC, abstractmethod

class MapleCanvas(ABC):
    """接口 MapleCanvas - 从Java接口转换"""

    @abstractmethod
    def get_height(self) -> Any:
        """抽象方法 getHeight"""
        pass

    @abstractmethod
    def get_width(self) -> Any:
        """抽象方法 getWidth"""
        pass

    @abstractmethod
    def get_image(self) -> Any:
        """抽象方法 getImage"""
        pass

