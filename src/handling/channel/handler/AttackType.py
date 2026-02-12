"""
AttackType - 从Java源文件转换而来
对应Java源文件: handling/channel/handler/AttackType.java
包路径: handling.channel.handler
"""

from enum import Enum, IntEnum


class AttackType(Enum):
    """枚举类 AttackType - 从Java枚举转换"""

    NON_RANGED = 0
    RANGED = 1
    RANGED_WITH_SHADOWPARTNER = 2
    NON_RANGED_WITH_MIRROR = 3

