"""
PetCommand - 从Java源文件转换而来
对应Java源文件: client/inventory/PetCommand.java
包路径: client.inventory
"""


class PetCommand:
    """
    类 PetCommand - 从Java类转换
    """

    def __init__(self, petId: int, skillId: int, prob: int, inc: int):
        """初始化 PetCommand"""
        self.petId = None
        self.skillId = None
        self.prob = None
        self.inc = None


    def getPetId(self) -> int:
        """方法 getPetId"""
        return getattr(self, 'pet_id', 0)

    def getSkillId(self) -> int:
        """方法 getSkillId"""
        return getattr(self, 'skill_id', 0)

    def getProbability(self) -> int:
        """方法 getProbability"""
        return getattr(self, 'probability', 0)

    def getIncrease(self) -> int:
        """方法 getIncrease"""
        return getattr(self, 'increase', 0)

