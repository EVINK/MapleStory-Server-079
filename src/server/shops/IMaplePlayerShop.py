"""
IMaplePlayerShop - 从Java源文件转换而来
对应Java源文件: server/shops/IMaplePlayerShop.java
包路径: server.shops
"""

from typing import List
from typing import Optional, List, Dict, Any, Set

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类
# from handling.MaplePacket import *  # TODO: 根据实际需要导入具体类
# from tools.Pair import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class IMaplePlayerShop(ABC):
    """接口 IMaplePlayerShop - 从Java接口转换"""

    @abstractmethod
    def get_owner_name(self) -> Any:
        """抽象方法 getOwnerName"""
        pass

    @abstractmethod
    def get_description(self) -> Any:
        """抽象方法 getDescription"""
        pass

    @abstractmethod
    def get_visitors(self) -> Any:
        """抽象方法 getVisitors"""
        pass

    @abstractmethod
    def get_items(self) -> Any:
        """抽象方法 getItems"""
        pass

    @abstractmethod
    def is_open(self) -> Any:
        """抽象方法 isOpen"""
        pass

    @abstractmethod
    def remove_item(self, p0: int) -> Any:
        """抽象方法 removeItem"""
        pass

    @abstractmethod
    def is_owner(self, p0: Any) -> Any:
        """抽象方法 isOwner"""
        pass

    @abstractmethod
    def get_shop_type(self) -> Any:
        """抽象方法 getShopType"""
        pass

    @abstractmethod
    def get_visitor_slot(self, p0: Any) -> Any:
        """抽象方法 getVisitorSlot"""
        pass

    @abstractmethod
    def get_free_slot(self) -> Any:
        """抽象方法 getFreeSlot"""
        pass

    @abstractmethod
    def get_item_id(self) -> Any:
        """抽象方法 getItemId"""
        pass

    @abstractmethod
    def get_meso(self) -> Any:
        """抽象方法 getMeso"""
        pass

    @abstractmethod
    def get_owner_id(self) -> Any:
        """抽象方法 getOwnerId"""
        pass

    @abstractmethod
    def get_owner_acc_id(self) -> Any:
        """抽象方法 getOwnerAccId"""
        pass

    @abstractmethod
    def set_open(self, p0: bool) -> Any:
        """抽象方法 setOpen"""
        pass

    @abstractmethod
    def set_meso(self, p0: int) -> Any:
        """抽象方法 setMeso"""
        pass

    @abstractmethod
    def add_item(self, p0: Any) -> Any:
        """抽象方法 addItem"""
        pass

    @abstractmethod
    def remove_from_slot(self, p0: int) -> Any:
        """抽象方法 removeFromSlot"""
        pass

    @abstractmethod
    def broadcast_to_visitors(self, p0: Any) -> Any:
        """抽象方法 broadcastToVisitors"""
        pass

    @abstractmethod
    def add_visitor(self, p0: Any) -> Any:
        """抽象方法 addVisitor"""
        pass

    @abstractmethod
    def remove_visitor(self, p0: Any) -> Any:
        """抽象方法 removeVisitor"""
        pass

    @abstractmethod
    def remove_all_visitors(self, p0: int, p1: int) -> Any:
        """抽象方法 removeAllVisitors"""
        pass

    @abstractmethod
    def buy(self, p0: Any, p1: int, p2: int) -> Any:
        """抽象方法 buy"""
        pass

    @abstractmethod
    def close_shop(self, p0: bool, p1: bool) -> Any:
        """抽象方法 closeShop"""
        pass

    @abstractmethod
    def get_password(self) -> Any:
        """抽象方法 getPassword"""
        pass

    @abstractmethod
    def get_map_id(self) -> Any:
        """抽象方法 getMapId"""
        pass

    @abstractmethod
    def get_channel(self) -> Any:
        """抽象方法 getChannel"""
        pass

    @abstractmethod
    def get_max_size(self) -> Any:
        """抽象方法 getMaxSize"""
        pass

    @abstractmethod
    def get_size(self) -> Any:
        """抽象方法 getSize"""
        pass

    @abstractmethod
    def get_game_type(self) -> Any:
        """抽象方法 getGameType"""
        pass

    @abstractmethod
    def update(self) -> Any:
        """抽象方法 update"""
        pass

    @abstractmethod
    def set_available(self, p0: bool) -> Any:
        """抽象方法 setAvailable"""
        pass

    @abstractmethod
    def is_available(self) -> Any:
        """抽象方法 isAvailable"""
        pass

    @abstractmethod
    def get_bought_items(self) -> Any:
        """抽象方法 getBoughtItems"""
        pass

