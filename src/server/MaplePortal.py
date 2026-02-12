"""
MaplePortal - 从Java源文件转换而来
对应Java源文件: server/MaplePortal.java
包路径: server
"""

from dataclasses import dataclass

# 内部模块导入 (Internal module imports)
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class MaplePortal(ABC):
    """接口 MaplePortal - 从Java接口转换"""

    @abstractmethod
    def get_type(self) -> Any:
        """抽象方法 getType"""
        pass

    @abstractmethod
    def get_id(self) -> Any:
        """抽象方法 getId"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

    @abstractmethod
    def get_name(self) -> Any:
        """抽象方法 getName"""
        pass

    @abstractmethod
    def get_target(self) -> Any:
        """抽象方法 getTarget"""
        pass

    @abstractmethod
    def get_script_name(self) -> Any:
        """抽象方法 getScriptName"""
        pass

    @abstractmethod
    def set_script_name(self, p0: str) -> Any:
        """抽象方法 setScriptName"""
        pass

    @abstractmethod
    def get_target_map_id(self) -> Any:
        """抽象方法 getTargetMapId"""
        pass

    @abstractmethod
    def enter_portal(self, p0: Any) -> Any:
        """抽象方法 enterPortal"""
        pass

    @abstractmethod
    def set_portal_state(self, p0: bool) -> Any:
        """抽象方法 setPortalState"""
        pass

    @abstractmethod
    def get_portal_state(self) -> Any:
        """抽象方法 getPortalState"""
        pass

