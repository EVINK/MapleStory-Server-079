"""
AbstractMapleMapObject - 从Java源文件转换而来
对应Java源文件: server/maps/AbstractMapleMapObject.java
包路径: server.maps
"""

from dataclasses import dataclass


class AbstractMapleMapObject(MapleMapObject, ABC):
    """
    类 AbstractMapleMapObject - 从Java类转换
    实现接口: MapleMapObject
    """

    def __init__(self):
        """初始化 AbstractMapleMapObject"""
        self.position = None
        self.objectId = 0


    def getTruePosition(self) -> Any:
        """方法 getTruePosition"""
        return getattr(self, 'true_position', None)

    def getPosition(self) -> Any:
        """方法 getPosition"""
        return getattr(self, 'position', None)

    def setPosition(self, position: Any) -> None:
        """方法 setPosition"""
        self.position = position
        return None

    def getObjectId(self) -> int:
        """方法 getObjectId"""
        return getattr(self, 'object_id', 0)

    def setObjectId(self, id: int) -> None:
        """方法 setObjectId"""
        self.object_id = id
        return None

