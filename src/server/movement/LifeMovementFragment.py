"""
LifeMovementFragment - 从Java源文件转换而来
对应Java源文件: server/movement/LifeMovementFragment.java
包路径: server.movement
"""

from dataclasses import dataclass

# 内部模块导入 (Internal module imports)
# from tools.data.output.LittleEndianWriter import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class LifeMovementFragment(ABC):
    """接口 LifeMovementFragment - 从Java接口转换"""

    @abstractmethod
    def serialize(self, p0: Any) -> Any:
        """抽象方法 serialize"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

