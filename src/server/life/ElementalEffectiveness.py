"""
ElementalEffectiveness - 从Java源文件转换而来
对应Java源文件: server/life/ElementalEffectiveness.java
包路径: server.life
"""

from enum import Enum, IntEnum


class ElementalEffectiveness(Enum):
    """枚举类 ElementalEffectiveness - 从Java枚举转换"""

    正常 = 0
    免疫 = 1
    增强 = 2
    虚弱 = 3
    NEUTRAL = 4

