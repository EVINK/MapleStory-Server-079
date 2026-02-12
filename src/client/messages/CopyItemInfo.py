"""
CopyItemInfo - 从Java源文件转换而来
对应Java源文件: client/messages/CopyItemInfo.java
包路径: client.messages
"""


class CopyItemInfo:
    """
    类 CopyItemInfo - 从Java类转换
    """

    def __init__(self, itemId: int, chrId: int, name: str):
        """初始化 CopyItemInfo"""
        self.itemId = 0
        self.chrId = 0
        self.name = ""
        self.first = False


    def isFirst(self) -> bool:
        """方法 isFirst"""
        return bool(getattr(self, 'first', False))

    def setFirst(self, f: bool) -> None:
        """方法 setFirst"""
        self.first = f
        return None

