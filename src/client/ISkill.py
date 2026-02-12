"""
ISkill - 从Java源文件转换而来
对应Java源文件: client/ISkill.java
包路径: client
"""

# 内部模块导入 (Internal module imports)
# from server import *  # TODO: 根据实际需要导入具体类
# from server.life import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class ISkill(ABC):
    """接口 ISkill - 从Java接口转换"""

    @abstractmethod
    def get_id(self) -> Any:
        """抽象方法 getId"""
        pass

    @abstractmethod
    def get_effect(self, p0: int) -> Any:
        """抽象方法 getEffect"""
        pass

    @abstractmethod
    def get_max_level(self) -> Any:
        """抽象方法 getMaxLevel"""
        pass

    @abstractmethod
    def get_animation_time(self) -> Any:
        """抽象方法 getAnimationTime"""
        pass

    @abstractmethod
    def can_be_learned_by(self, p0: int) -> Any:
        """抽象方法 canBeLearnedBy"""
        pass

    @abstractmethod
    def is_fourth_job(self) -> Any:
        """抽象方法 isFourthJob"""
        pass

    @abstractmethod
    def get_action(self) -> Any:
        """抽象方法 getAction"""
        pass

    @abstractmethod
    def is_time_limited(self) -> Any:
        """抽象方法 isTimeLimited"""
        pass

    @abstractmethod
    def get_master_level(self) -> Any:
        """抽象方法 getMasterLevel"""
        pass

    @abstractmethod
    def get_element(self) -> Any:
        """抽象方法 getElement"""
        pass

    @abstractmethod
    def is_beginner_skill(self) -> Any:
        """抽象方法 isBeginnerSkill"""
        pass

    @abstractmethod
    def has_required_skill(self) -> Any:
        """抽象方法 hasRequiredSkill"""
        pass

    @abstractmethod
    def is_invisible(self) -> Any:
        """抽象方法 isInvisible"""
        pass

    @abstractmethod
    def is_charge_skill(self) -> Any:
        """抽象方法 isChargeSkill"""
        pass

    @abstractmethod
    def get_required_skill_level(self) -> Any:
        """抽象方法 getRequiredSkillLevel"""
        pass

    @abstractmethod
    def get_required_skill_id(self) -> Any:
        """抽象方法 getRequiredSkillId"""
        pass

    @abstractmethod
    def get_name(self) -> Any:
        """抽象方法 getName"""
        pass

