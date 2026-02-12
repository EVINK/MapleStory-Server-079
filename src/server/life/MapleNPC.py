"""
MapleNPC - 从Java源文件转换而来
对应Java源文件: server/life/MapleNPC.java
包路径: server.life
"""

from typing import Optional, Any

# 内部模块导入 (Internal module imports)
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类
# from server.MapleShopFactory import *  # TODO: 根据实际需要导入具体类
# from server.maps.MapleMapObjectType import *  # TODO: 根据实际需要导入具体类
# from tools.MaplePacketCreator import *  # TODO: 根据实际需要导入具体类


class MapleNPC(AbstractLoadedMapleLife):
    """
    类 MapleNPC - 从Java类转换
    继承自: AbstractLoadedMapleLife
    """

    def __init__(self, id: int, name: str):
        """初始化 MapleNPC"""
        self.name = ""
        self.custom = False


    def hasShop(self) -> bool:
        """方法 hasShop"""
        return bool(getattr(self, 'shop', False))

    def sendShop(self, c: Any) -> None:
        """方法 sendShop"""
        pass

    def sendSpawnData(self, client: Any) -> None:
        """方法 sendSpawnData"""
        pass

    def sendDestroyData(self, client: Any) -> None:
        """方法 sendDestroyData"""
        pass

    def getType(self) -> Any:
        """方法 getType"""
        return getattr(self, 'type', None)

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def setName(self, n: str) -> None:
        """方法 setName"""
        self.name = n
        return None

    def isCustom(self) -> bool:
        """方法 isCustom"""
        return bool(getattr(self, 'custom', False))

    def setCustom(self, custom: bool) -> None:
        """方法 setCustom"""
        self.custom = custom
        return None

