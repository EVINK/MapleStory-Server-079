"""
CheatingOffense - Converted from Java source
Original: client/anticheat/CheatingOffense.java
Package: client.anticheat
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class CheatingOffense(Enum):
    """Enum CheatingOffense"""

    召唤兽快速攻击 = ((byte)5, 6000L, 10, (byte)1)
    快速攻击 = ((byte)5, 6000L, 50, (byte)2)
    快速攻击2 = ((byte)5, 9000L, 20, (byte)2)
    怪物移动 = ((byte)1, 30000L, 20, (byte)2)
    伤害相同 = ((byte)2, 30000L, 150, (byte)2)
    人物无敌 = ((byte)1, 30000L, 1200, (byte)0)
    魔法伤害过高 = ((byte)5, 30000L, -1, (byte)0)
    魔法伤害过高2 = ((byte)10, 30000L, -1, (byte)0)
    攻击力过高 = ((byte)5, 30000L, -1, (byte)0)
    怪物碰撞过快 = ((byte)1, 60000L, 100, (byte)2)
    攻击过高2 = ((byte)10, 30000L, -1, (byte)0)
    攻击范围过大 = ((byte)5, 60000L, 1500)
    召唤兽攻击范围过大 = ((byte)5, 60000L, 200)
    回复过多HP = ((byte)1, 30000L, 1000, (byte)0)
    回复过多MP = ((byte)1, 30000L, 1000, (byte)0)
    全图吸物_客户端 = ((byte)5, 5000L, 10)
    全图吸物_服务端 = ((byte)3, 5000L, 100)
    宠物全图吸物_客户端 = ((byte)5, 10000L, 20)
    宠物全图吸物_服务端 = ((byte)3, 10000L, 100, (byte)0)
    使用过远传送点 = ((byte)1, 60000L, 100, (byte)0)
    回避率过高 = ((byte)20, 180000L, 100, (byte)2)
    其他异常 = ((byte)1, 300000L)
    人物死亡攻击 = ((byte)1, 300000L, -1, (byte)0)
    使用不存在道具 = ((byte)1, 300000L)
    添加自己声望 = ((byte)1, 1000L, 1)
    声望十五级以下添加 = ((byte)1, 1000L, 1)
    金钱炸弹_不存在道具 = ((byte)1, 300000L)
    召唤兽攻击怪物数量异常 = ((byte)1, 10000L, 3)
    治愈术攻击非不死系怪物 = ((byte)20, 10000L, 3)
    吸怪 = ((byte)1, 7000L, 5)

    def __init__(self, points, validityDuration):
        self._points = points
        self._validityDuration = validityDuration

    def getPoints(self) -> int:
        return self.points

    def getValidityDuration(self) -> int:
        return self.validityDuration

    def shouldAutoban(self, count: int) -> bool:
        return self.autobancount != -1 && count >= self.autobancount

    def getBanType(self) -> int:
        return self.bantype

    def setEnabled(self, enabled: bool) -> None:
        self.bantype = (byte)(enabled ? 1 : 0)

    def isEnabled(self) -> bool:
        return self.bantype >= 1

