"""
AnimatedMapleMapObject - 从Java源文件转换而来
对应Java源文件: server/maps/AnimatedMapleMapObject.java
包路径: server.maps
"""


from abc import ABC, abstractmethod

class AnimatedMapleMapObject(ABC):
    """接口 AnimatedMapleMapObject - 从Java接口转换"""

    @abstractmethod
    def get_stance(self) -> Any:
        """抽象方法 getStance"""
        pass

    @abstractmethod
    def set_stance(self, p0: int) -> Any:
        """抽象方法 setStance"""
        pass

    @abstractmethod
    def is_facing_left(self) -> Any:
        """抽象方法 isFacingLeft"""
        pass

