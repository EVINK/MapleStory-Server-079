"""
CherryMSLottery - 从Java源文件转换而来
对应Java源文件: KinMS/db/CherryMSLottery.java
包路径: KinMS.db
"""

from typing import Collection
from typing import Optional, Any

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类
# from handling.channel.ChannelServer import *  # TODO: 根据实际需要导入具体类
# from server.maps.MapleMapFactory import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class CherryMSLottery(ABC):
    """接口 CherryMSLottery - 从Java接口转换"""

    @abstractmethod
    def add_char(self, p0: Any) -> Any:
        """抽象方法 addChar"""
        pass

    @abstractmethod
    def do_lottery(self) -> Any:
        """抽象方法 doLottery"""
        pass

    @abstractmethod
    def drawalottery(self) -> Any:
        """抽象方法 drawalottery"""
        pass

    @abstractmethod
    def get_allpeichu(self) -> Any:
        """抽象方法 getAllpeichu"""
        pass

    @abstractmethod
    def get_alltouzhu(self) -> Any:
        """抽象方法 getAlltouzhu"""
        pass

    @abstractmethod
    def get_channel_server(self) -> Any:
        """抽象方法 getChannelServer"""
        pass

    @abstractmethod
    def get_characters(self) -> Any:
        """抽象方法 getCharacters"""
        pass

    @abstractmethod
    def get_maple_map_factory(self) -> Any:
        """抽象方法 getMapleMapFactory"""
        pass

    @abstractmethod
    def get_tou_numby_type(self, p0: int) -> Any:
        """抽象方法 getTouNumbyType"""
        pass

    @abstractmethod
    def get_zj_num(self) -> Any:
        """抽象方法 getZjNum"""
        pass

    @abstractmethod
    def set_allpeichu(self, p0: int) -> Any:
        """抽象方法 setAllpeichu"""
        pass

    @abstractmethod
    def set_alltouzhu(self, p0: int) -> Any:
        """抽象方法 setAlltouzhu"""
        pass

    @abstractmethod
    def set_characters(self, p0: list) -> Any:
        """抽象方法 setCharacters"""
        pass

    @abstractmethod
    def set_zj_num(self, p0: int) -> Any:
        """抽象方法 setZjNum"""
        pass

    @abstractmethod
    def warp(self, p0: int, p1: Any) -> Any:
        """抽象方法 warp"""
        pass

