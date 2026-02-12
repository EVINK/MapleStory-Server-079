"""
IItem - 从Java源文件转换而来
对应Java源文件: client/inventory/IItem.java
包路径: client.inventory
"""

from typing import Optional, Any
import threading


from abc import ABC, abstractmethod

class IItem(ABC):
    """接口 IItem - 从Java接口转换"""

    @abstractmethod
    def get_type(self) -> Any:
        """抽象方法 getType"""
        pass

    @abstractmethod
    def get_position(self) -> Any:
        """抽象方法 getPosition"""
        pass

    @abstractmethod
    def get_flag(self) -> Any:
        """抽象方法 getFlag"""
        pass

    @abstractmethod
    def get_locked(self) -> Any:
        """抽象方法 getLocked"""
        pass

    @abstractmethod
    def get_quantity(self) -> Any:
        """抽象方法 getQuantity"""
        pass

    @abstractmethod
    def get_owner(self) -> Any:
        """抽象方法 getOwner"""
        pass

    @abstractmethod
    def get_gm_log(self) -> Any:
        """抽象方法 getGMLog"""
        pass

    @abstractmethod
    def get_item_id(self) -> Any:
        """抽象方法 getItemId"""
        pass

    @abstractmethod
    def get_pet(self) -> Any:
        """抽象方法 getPet"""
        pass

    @abstractmethod
    def get_unique_id(self) -> Any:
        """抽象方法 getUniqueId"""
        pass

    @abstractmethod
    def copy(self) -> Any:
        """抽象方法 copy"""
        pass

    @abstractmethod
    def get_expiration(self) -> Any:
        """抽象方法 getExpiration"""
        pass

    @abstractmethod
    def set_flag(self, p0: int) -> Any:
        """抽象方法 setFlag"""
        pass

    @abstractmethod
    def set_locked(self, p0: int) -> Any:
        """抽象方法 setLocked"""
        pass

    @abstractmethod
    def set_unique_id(self, p0: int) -> Any:
        """抽象方法 setUniqueId"""
        pass

    @abstractmethod
    def set_position(self, p0: int) -> Any:
        """抽象方法 setPosition"""
        pass

    @abstractmethod
    def set_expiration(self, p0: int) -> Any:
        """抽象方法 setExpiration"""
        pass

    @abstractmethod
    def set_owner(self, p0: str) -> Any:
        """抽象方法 setOwner"""
        pass

    @abstractmethod
    def set_gm_log(self, p0: str) -> Any:
        """抽象方法 setGMLog"""
        pass

    @abstractmethod
    def set_quantity(self, p0: int) -> Any:
        """抽象方法 setQuantity"""
        pass

    @abstractmethod
    def set_gift_from(self, p0: str) -> Any:
        """抽象方法 setGiftFrom"""
        pass

    @abstractmethod
    def set_equip_level(self, p0: int) -> Any:
        """抽象方法 setEquipLevel"""
        pass

    @abstractmethod
    def get_equip_level(self) -> Any:
        """抽象方法 getEquipLevel"""
        pass

    @abstractmethod
    def get_gift_from(self) -> Any:
        """抽象方法 getGiftFrom"""
        pass

    @abstractmethod
    def get_ring(self) -> Any:
        """抽象方法 getRing"""
        pass

    @abstractmethod
    def get_equip_only_id(self) -> Any:
        """抽象方法 getEquipOnlyId"""
        pass

    @abstractmethod
    def has_set_only_id(self) -> Any:
        """抽象方法 hasSetOnlyId"""
        pass

    @abstractmethod
    def set_equip_only_id(self, p0: int) -> Any:
        """抽象方法 setEquipOnlyId"""
        pass

