"""
IEquip - 从Java源文件转换而来
对应Java源文件: client/inventory/IEquip.java
包路径: client.inventory
"""


from abc import ABC, abstractmethod

class IEquip(ABC):
    """接口 IEquip - 从Java接口转换"""

    @abstractmethod
    def get_upgrade_slots(self) -> Any:
        """抽象方法 getUpgradeSlots"""
        pass

    @abstractmethod
    def get_level(self) -> Any:
        """抽象方法 getLevel"""
        pass

    @abstractmethod
    def get_vicious_hammer(self) -> Any:
        """抽象方法 getViciousHammer"""
        pass

    @abstractmethod
    def get_item_exp(self) -> Any:
        """抽象方法 getItemEXP"""
        pass

    @abstractmethod
    def get_exp_percentage(self) -> Any:
        """抽象方法 getExpPercentage"""
        pass

    @abstractmethod
    def get_equip_level(self) -> Any:
        """抽象方法 getEquipLevel"""
        pass

    @abstractmethod
    def get_equip_levels(self) -> Any:
        """抽象方法 getEquipLevels"""
        pass

    @abstractmethod
    def get_equip_exp(self) -> Any:
        """抽象方法 getEquipExp"""
        pass

    @abstractmethod
    def get_equip_exp_for_level(self) -> Any:
        """抽象方法 getEquipExpForLevel"""
        pass

    @abstractmethod
    def get_base_level(self) -> Any:
        """抽象方法 getBaseLevel"""
        pass

    @abstractmethod
    def get_str(self) -> Any:
        """抽象方法 getStr"""
        pass

    @abstractmethod
    def get_dex(self) -> Any:
        """抽象方法 getDex"""
        pass

    @abstractmethod
    def get_int(self) -> Any:
        """抽象方法 getInt"""
        pass

    @abstractmethod
    def get_luk(self) -> Any:
        """抽象方法 getLuk"""
        pass

    @abstractmethod
    def get_hp(self) -> Any:
        """抽象方法 getHp"""
        pass

    @abstractmethod
    def get_mp(self) -> Any:
        """抽象方法 getMp"""
        pass

    @abstractmethod
    def get_watk(self) -> Any:
        """抽象方法 getWatk"""
        pass

    @abstractmethod
    def get_matk(self) -> Any:
        """抽象方法 getMatk"""
        pass

    @abstractmethod
    def get_wdef(self) -> Any:
        """抽象方法 getWdef"""
        pass

    @abstractmethod
    def get_mdef(self) -> Any:
        """抽象方法 getMdef"""
        pass

    @abstractmethod
    def get_acc(self) -> Any:
        """抽象方法 getAcc"""
        pass

    @abstractmethod
    def get_avoid(self) -> Any:
        """抽象方法 getAvoid"""
        pass

    @abstractmethod
    def get_hands(self) -> Any:
        """抽象方法 getHands"""
        pass

    @abstractmethod
    def get_speed(self) -> Any:
        """抽象方法 getSpeed"""
        pass

    @abstractmethod
    def get_jump(self) -> Any:
        """抽象方法 getJump"""
        pass

    @abstractmethod
    def get_durability(self) -> Any:
        """抽象方法 getDurability"""
        pass

    @abstractmethod
    def get_enhance(self) -> Any:
        """抽象方法 getEnhance"""
        pass

    @abstractmethod
    def get_state(self) -> Any:
        """抽象方法 getState"""
        pass

    @abstractmethod
    def get_potential1(self) -> Any:
        """抽象方法 getPotential1"""
        pass

    @abstractmethod
    def get_potential2(self) -> Any:
        """抽象方法 getPotential2"""
        pass

    @abstractmethod
    def get_potential3(self) -> Any:
        """抽象方法 getPotential3"""
        pass

    @abstractmethod
    def get_hp_r(self) -> Any:
        """抽象方法 getHpR"""
        pass

    @abstractmethod
    def get_mp_r(self) -> Any:
        """抽象方法 getMpR"""
        pass


class ScrollResult(Enum):
    """枚举类 ScrollResult - 从Java枚举转换"""

    SUCCESS = 0
    FAIL = 1
    CURSE = 2

