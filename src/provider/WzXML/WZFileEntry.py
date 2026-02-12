"""
WZFileEntry - 从Java源文件转换而来
对应Java源文件: provider/WzXML/WZFileEntry.java
包路径: provider.WzXML
"""

# 内部模块导入 (Internal module imports)
# from provider.MapleDataEntity import *  # TODO: 根据实际需要导入具体类
# from provider.MapleDataFileEntry import *  # TODO: 根据实际需要导入具体类


class WZFileEntry(WZEntry, MapleDataFileEntry):
    """
    类 WZFileEntry - 从Java类转换
    继承自: WZEntry
    实现接口: MapleDataFileEntry
    """

    def __init__(self, name: str, size: int, checksum: int, parent: Any):
        """初始化 WZFileEntry"""
        self.offset = 0


    def getOffset(self) -> int:
        """方法 getOffset"""
        return getattr(self, 'offset', 0)

    def setOffset(self, offset: int) -> None:
        """方法 setOffset"""
        self.offset = offset
        return None

