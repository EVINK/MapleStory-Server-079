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
        return ""

    def getSize(self) -> int:
        """方法 getSize"""
        return 0

    def getChecksum(self) -> int:
        """方法 getChecksum"""
        return 0

    def getOffset(self) -> int:
        """方法 getOffset"""
        return 0

    def getParent(self) -> Any:
        """方法 getParent"""
        raise NotImplementedError("方法 getParent 尚未实现")

