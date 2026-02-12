"""
CharacterIdChannelPair - 从Java源文件转换而来
对应Java源文件: handling/world/CharacterIdChannelPair.java
包路径: handling.world
"""

from typing import Optional, Any
import os


class CharacterIdChannelPair(Externalizable):
    """
    类 CharacterIdChannelPair - 从Java类转换
    实现接口: Externalizable, Comparable<CharacterIdChannelPair>
    """

    def __init__(self):
        """初始化 CharacterIdChannelPair"""
        self.charid = 0
        self.channel = 0


    def getCharacterId(self) -> int:
        """方法 getCharacterId"""
        return 0

    def getChannel(self) -> int:
        """方法 getChannel"""
        return 0

    def readExternal(self, in: Any) -> None:
        """方法 readExternal"""
        pass

    def writeExternal(self, out: Any) -> None:
        """方法 writeExternal"""
        pass

    def compareTo(self, o: Any) -> int:
        """方法 compareTo"""
        return 0

