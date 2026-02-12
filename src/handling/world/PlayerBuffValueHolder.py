"""
PlayerBuffValueHolder - 从Java源文件转换而来
对应Java源文件: handling/world/PlayerBuffValueHolder.java
包路径: handling.world
"""

# 内部模块导入 (Internal module imports)
# from server.MapleStatEffect import *  # TODO: 根据实际需要导入具体类


class PlayerBuffValueHolder:
    """
    类 PlayerBuffValueHolder - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = 9179541993413738569

    def __init__(self, startTime: int, effect: Any):
        """初始化 PlayerBuffValueHolder"""
        self.startTime = 0
        self.effect = None


