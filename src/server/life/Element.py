"""
Element - 从Java源文件转换而来
对应Java源文件: server/life/Element.java
包路径: server.life
"""

from enum import Enum, IntEnum


class Element(Enum):
    """枚举类 Element - 从Java枚举转换"""

    NEUTRAL = 0
    PHYSICAL = 1
    FIRE = 2
    ICE = 3
    LIGHTING = 4
    POISON = 5
    HOLY = 6
    DARKNESS = 7

