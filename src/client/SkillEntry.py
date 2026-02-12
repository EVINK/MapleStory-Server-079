"""
SkillEntry - 从Java源文件转换而来
对应Java源文件: client/SkillEntry.java
包路径: client
"""


class SkillEntry:
    """
    类 SkillEntry - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = 9179541993413738569

    def __init__(self, skillevel: int, masterlevel: int, expiration: int):
        """初始化 SkillEntry"""
        self.skillevel = 0
        self.masterlevel = 0
        self.expiration = 0


