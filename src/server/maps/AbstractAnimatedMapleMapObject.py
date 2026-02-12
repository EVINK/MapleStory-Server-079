"""
AbstractAnimatedMapleMapObject - 从Java源文件转换而来
对应Java源文件: server/maps/AbstractAnimatedMapleMapObject.java
包路径: server.maps
"""


class AbstractAnimatedMapleMapObject(AbstractMapleMapObject, AnimatedMapleMapObject, ABC):
    """
    类 AbstractAnimatedMapleMapObject - 从Java类转换
    继承自: AbstractMapleMapObject
    实现接口: AnimatedMapleMapObject
    """

    def __init__(self):
        """初始化 AbstractAnimatedMapleMapObject"""
        self.stance = 0


    def getStance(self) -> int:
        """方法 getStance"""
        return 0

    def setStance(self, stance: int) -> None:
        """方法 setStance"""
        pass

    def isFacingLeft(self) -> bool:
        """方法 isFacingLeft"""
        return False

    def getFacingDirection(self) -> int:
        """方法 getFacingDirection"""
        return 0

