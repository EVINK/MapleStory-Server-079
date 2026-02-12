"""
MonsterListener - 从Java源文件转换而来
对应Java源文件: server/life/MonsterListener.java
包路径: server.life
"""


from abc import ABC, abstractmethod

class MonsterListener(ABC):
    """接口 MonsterListener - 从Java接口转换"""

    @abstractmethod
    def monster_killed(self) -> Any:
        """抽象方法 monsterKilled"""
        pass

