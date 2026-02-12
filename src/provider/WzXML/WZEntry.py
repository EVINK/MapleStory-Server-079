"""
WZEntry - 从Java源文件转换而来
对应Java源文件: provider/WzXML/WZEntry.java
包路径: provider.WzXML
"""

# 内部模块导入 (Internal module imports)
# from provider.MapleDataEntity import *  # TODO: 根据实际需要导入具体类
# from provider.MapleDataEntry import *  # TODO: 根据实际需要导入具体类


class WZEntry(MapleDataEntry):
    """
    类 WZEntry - 从Java类转换
    实现接口: MapleDataEntry
    """

    def __init__(self, name: str, size: int, checksum: int, parent: Any):
        """初始化 WZEntry"""
        self.name = None
        self.size = None
        self.checksum = None
        self.offset = 0
        self.parent = None


    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getSize(self) -> int:
        """方法 getSize"""
        return getattr(self, 'size', 0)

    def getChecksum(self) -> int:
        """方法 getChecksum"""
        return getattr(self, 'checksum', 0)

    def getOffset(self) -> int:
        """方法 getOffset"""
        return getattr(self, 'offset', 0)

    def getParent(self) -> Any:
        """方法 getParent"""
        return getattr(self, 'parent', None)

