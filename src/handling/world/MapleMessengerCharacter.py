"""
MapleMessengerCharacter - 从Java源文件转换而来
对应Java源文件: handling/world/MapleMessengerCharacter.java
包路径: handling.world
"""

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类


class MapleMessengerCharacter:
    """
    类 MapleMessengerCharacter - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, maplechar: Any):
        """初始化 MapleMessengerCharacter"""
        self.name = ""
        self.id = 0
        self.channel = 0
        self.online = False


    def getChannel(self) -> int:
        """方法 getChannel"""
        return getattr(self, 'channel', 0)

    def isOnline(self) -> bool:
        """方法 isOnline"""
        return bool(getattr(self, 'online', False))

    def setOnline(self, online: bool) -> None:
        """方法 setOnline"""
        self.online = online
        return None

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def hashCode(self) -> int:
        """方法 hashCode"""
        return hash(self)

    def equals(self, obj: Any) -> bool:
        """方法 equals"""
        return self is obj or getattr(self, '__eq__', lambda o: False)(obj)

