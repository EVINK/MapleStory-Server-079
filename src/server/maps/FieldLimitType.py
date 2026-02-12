"""
FieldLimitType - 从Java源文件转换而来
对应Java源文件: server/maps/FieldLimitType.java
包路径: server.maps
"""

from enum import Enum, IntEnum


class FieldLimitType(Enum):
    """枚举类 FieldLimitType - 从Java枚举转换"""

    Jump = (1)
    MovementSkills = (2)
    SummoningBag = (4)
    MysticDoor = (8)
    ChannelSwitch = (16)
    RegularExpLoss = (32)
    VipRock = (64)
    Minigames = (128)
    NoClue1 = (256)
    Mount = (512)
    PotionUse = (1024)
    Event = (8192)
    Pet = (32768)
    Event2 = (65536)
    DropDown = (131072)

    def __init__(self, i):
        """初始化枚举值"""
        self._i = i

    def getValue(self) -> int:
        """方法 getValue"""
        return 0

    def check(self, fieldlimit: int) -> bool:
        """方法 check"""
        return False

