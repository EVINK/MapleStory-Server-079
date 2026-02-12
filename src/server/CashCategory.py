"""
CashCategory - 从Java源文件转换而来
对应Java源文件: server/CashCategory.java
包路径: server
"""


class CashCategory:
    """
    类 CashCategory - 从Java类转换
    """

    def __init__(self, id: int, name: str, parent: int, flag: int, sold: int):
        """初始化 CashCategory"""
        self.id = None
        self.parent = None
        self.flag = None
        self.sold = None
        self.name = None
        self.value = None


    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getParentDirectory(self) -> int:
        """方法 getParentDirectory"""
        return getattr(self, 'parent_directory', 0)

    def getFlag(self) -> int:
        """方法 getFlag"""
        return getattr(self, 'flag', 0)

    def getSold(self) -> int:
        """方法 getSold"""
        return getattr(self, 'sold', 0)

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)


class CSFlag(Enum):
    """枚举类 CSFlag - 从Java枚举转换"""

    NORMAL = (0)
    NEW = (1)
    HOT = (2)

    def __init__(self, value):
        """初始化枚举值"""
        self._value = value

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)

