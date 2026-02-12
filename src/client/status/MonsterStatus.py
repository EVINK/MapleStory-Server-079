"""
MonsterStatus - 从Java源文件转换而来
对应Java源文件: client/status/MonsterStatus.java
包路径: client.status
"""

from enum import Enum, IntEnum


class MonsterStatus(Enum):
    """枚举类 MonsterStatus - 从Java枚举转换"""

    NEUTRALISE = (2L)
    物攻 = (4294967296L)
    物防 = (8589934592L)
    魔攻 = (17179869184L)
    魔防 = (34359738368L)
    命中 = (68719476736L)
    回避 = (137438953472L)
    速度 = (274877906944L)
    眩晕 = (549755813888L)
    冻结 = (1099511627776L)
    中毒 = (2199023255552L)
    封印 = (4398046511104L)
    挑衅 = (8796093022208L)
    物理攻击提升 = (17592186044416L)
    物理防御提升 = (35184372088832L)
    魔法攻击提升 = (70368744177664L)
    魔法防御提升 = (140737488355328L)
    巫毒术 = (281474976710656L)
    影网术 = (562949953421312L)
    免疫物理攻击 = (1125899906842624L)
    免疫魔法攻击 = (2251799813685248L)
    免疫伤害 = (9007199254740992L)
    忍者伏击 = (18014398509481984L)
    烈焰喷射 = (72057594037927936L)
    DARKNESS = (144115188075855872L)
    空白BUFF = (576460752303423488L)
    心灵控制 = (1152921504606846976L)
    反射物理伤害 = (2305843009213693952L)
    反射魔法伤害 = (4611686018427387904L)
    召唤怪物 = (Long.MIN_VALUE)

    def __init__(self, i):
        """初始化枚举值"""
        self._i = i

    def isFirst(self) -> bool:
        """方法 isFirst"""
        return bool(getattr(self, 'first', False))

    def isEmpty(self) -> bool:
        """方法 isEmpty"""
        return bool(getattr(self, 'empty', False))

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)

