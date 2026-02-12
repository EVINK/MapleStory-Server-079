"""
PartyOperation - 从Java源文件转换而来
对应Java源文件: handling/world/PartyOperation.java
包路径: handling.world
"""

from enum import Enum, IntEnum


class PartyOperation(Enum):
    """枚举类 PartyOperation - 从Java枚举转换"""

    JOIN = 0
    LEAVE = 1
    EXPEL = 2
    DISBAND = 3
    SILENT_UPDATE = 4
    LOG_ONOFF = 5
    CHANGE_LEADER = 6
    CHANGE_LEADER_DC = 7

