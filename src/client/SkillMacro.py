"""
SkillMacro - 从Java源文件转换而来
对应Java源文件: client/SkillMacro.java
包路径: client
"""


class SkillMacro:
    """
    类 SkillMacro - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = -63413738569

    def __init__(self, skill1: int, skill2: int, skill3: int, name: str, shout: int, position: int):
        """初始化 SkillMacro"""
        self.macroId = 0
        self.skill1 = 0
        self.skill2 = 0
        self.skill3 = 0
        self.name = ""
        self.shout = 0
        self.position = 0


    def getMacroId(self) -> int:
        """方法 getMacroId"""
        return getattr(self, 'macro_id', 0)

    def getSkill1(self) -> int:
        """方法 getSkill1"""
        return getattr(self, 'skill1', 0)

    def getSkill2(self) -> int:
        """方法 getSkill2"""
        return getattr(self, 'skill2', 0)

    def getSkill3(self) -> int:
        """方法 getSkill3"""
        return getattr(self, 'skill3', 0)

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getShout(self) -> int:
        """方法 getShout"""
        return getattr(self, 'shout', 0)

    def getPosition(self) -> int:
        """方法 getPosition"""
        return getattr(self, 'position', 0)

    def setMacroId(self, macroId: int) -> None:
        """方法 setMacroId"""
        self.macro_id = macroId
        return None

    def setSkill1(self, skill1: int) -> None:
        """方法 setSkill1"""
        self.skill1 = skill1
        return None

    def setSkill2(self, skill2: int) -> None:
        """方法 setSkill2"""
        self.skill2 = skill2
        return None

    def setSkill3(self, skill3: int) -> None:
        """方法 setSkill3"""
        self.skill3 = skill3
        return None

    def setName(self, name: str) -> None:
        """方法 setName"""
        self.name = name
        return None

    def setShout(self, shout: int) -> None:
        """方法 setShout"""
        self.shout = shout
        return None

    def setPosition(self, position: int) -> None:
        """方法 setPosition"""
        self.position = position
        return None

