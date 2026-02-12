"""
LifeMovement - 从Java源文件转换而来
对应Java源文件: server/movement/LifeMovement.java
包路径: server.movement
"""

from dataclasses import dataclass


from abc import ABC, abstractmethod

class LifeMovement(ABC):
    """接口 LifeMovement - 从Java接口转换"""

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

    @abstractmethod
    def get_newstate(self) -> Any:
        """抽象方法 getNewstate"""
        pass

    @abstractmethod
    def get_duration(self) -> Any:
        """抽象方法 getDuration"""
        pass

    @abstractmethod
    def get_type(self) -> Any:
        """抽象方法 getType"""
        pass

