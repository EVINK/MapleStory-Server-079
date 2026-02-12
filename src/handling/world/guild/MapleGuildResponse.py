"""
MapleGuildResponse - 从Java源文件转换而来
对应Java源文件: handling/world/guild/MapleGuildResponse.java
包路径: handling.world.guild
"""

from enum import Enum, IntEnum

# 内部模块导入 (Internal module imports)
# from handling.MaplePacket import *  # TODO: 根据实际需要导入具体类
# from tools.MaplePacketCreator import *  # TODO: 根据实际需要导入具体类


class MapleGuildResponse(Enum):
    """枚举类 MapleGuildResponse - 从Java枚举转换"""

    NOT_IN_CHANNEL = (42)
    ALREADY_IN_GUILD = (40)
    NOT_IN_GUILD = (45)

    def __init__(self, val):
        """初始化枚举值"""
        self._val = val

    def getValue(self) -> int:
        """方法 getValue"""
        return 0

    def getPacket(self) -> Any:
        """方法 getPacket"""
        raise NotImplementedError("方法 getPacket 尚未实现")

