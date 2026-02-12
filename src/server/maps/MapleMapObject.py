"""
MapleMapObject - 从Java源文件转换而来
对应Java源文件: server/maps/MapleMapObject.java
包路径: server.maps
"""

from dataclasses import dataclass

# 内部模块导入 (Internal module imports)
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class MapleMapObject(ABC):
    """接口 MapleMapObject - 从Java接口转换"""

    @abstractmethod
    def get_object_id(self) -> Any:
        """抽象方法 getObjectId"""
        pass

    @abstractmethod
    def set_object_id(self, p0: int) -> Any:
        """抽象方法 setObjectId"""
        pass

    @abstractmethod
    def get_type(self) -> Any:
        """抽象方法 getType"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

    @abstractmethod
    def set_position(self, p0: Any) -> Any:
        """抽象方法 setPosition"""
        pass

    @abstractmethod
    def send_spawn_data(self, p0: Any) -> Any:
        """抽象方法 sendSpawnData"""
        pass

    @abstractmethod
    def send_destroy_data(self, p0: Any) -> Any:
        """抽象方法 sendDestroyData"""
        pass

