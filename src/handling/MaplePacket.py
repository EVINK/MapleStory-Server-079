"""
MaplePacket - 从Java源文件转换而来
对应Java源文件: handling/MaplePacket.java
包路径: handling
"""

import threading


from abc import ABC, abstractmethod

class MaplePacket(ABC):
    """接口 MaplePacket - 从Java接口转换"""

    @abstractmethod
    def get_on_send(self) -> Any:
        """抽象方法 getOnSend"""
        pass

    @abstractmethod
    def set_on_send(self, p0: Any) -> Any:
        """抽象方法 setOnSend"""
        pass

