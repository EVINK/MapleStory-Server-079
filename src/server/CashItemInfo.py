"""
CashItemInfo - 从Java源文件转换而来
对应Java源文件: server/CashItemInfo.java
包路径: server
"""

from typing import Optional, Any


class CashItemInfo:
    """
    类 CashItemInfo - 从Java类转换
    """

    def __init__(self, itemId: int, count: int, price: int, sn: int, expire: int, gender: int, sale: bool):
        """初始化 CashItemInfo"""
        self.itemId = 0
        self.count = 0
        self.price = 0
        self.sn = 0
        self.expire = 0
        self.gender = 0
        self.onSale = False
        self.name = ""
        self.discountPrice = 0
        self.mark = 0
        self.priority = 0
        self.sn = 0
        self.itemid = 0
        self.flags = 0
        self.period = 0
        self.gender = 0
        self.count = 0
        self.meso = 0
        self.unk_1 = 0
        self.unk_2 = 0
        self.unk_3 = 0
        self.extra_flags = 0
        self.showUp = False
        self.packagez = False
        self.cii = None


    def getId(self) -> int:
        """方法 getId"""
        return 0

    def getOnSale(self) -> int:
        """方法 getOnSale"""
        return 0

    def getExpire(self) -> int:
        """方法 getExpire"""
        return 0

    def getCount(self) -> int:
        """方法 getCount"""
        return 0

    def getPrice(self) -> int:
        """方法 getPrice"""
        return 0

    def getSN(self) -> int:
        """方法 getSN"""
        return 0

    def getPeriod(self) -> int:
        """方法 getPeriod"""
        return 0

    def getGender(self) -> int:
        """方法 getGender"""
        return 0

    def onSale(self) -> bool:
        """方法 onSale"""
        return False

    def genderEquals(self, g: int) -> bool:
        """方法 genderEquals"""
        return False

    def toCItem(self, backup: Any) -> Any:
        """方法 toCItem"""
        raise NotImplementedError("方法 toCItem 尚未实现")


class CashModInfo:
    """
    类 CashModInfo - 从Java类转换
    """

    def __init__(self, sn: int, discount: int, mark: int, show: bool, itemid: int, priority: int, packagez: bool, period: int, gender: int, count: int, meso: int, unk_1: int, unk_2: int, unk_3: int, extra_flags: int):
        """初始化 CashModInfo"""
        self.itemId = 0
        self.count = 0
        self.price = 0
        self.sn = 0
        self.expire = 0
        self.gender = 0
        self.onSale = False
        self.name = ""
        self.discountPrice = 0
        self.mark = 0
        self.priority = 0
        self.sn = 0
        self.itemid = 0
        self.flags = 0
        self.period = 0
        self.gender = 0
        self.count = 0
        self.meso = 0
        self.unk_1 = 0
        self.unk_2 = 0
        self.unk_3 = 0
        self.extra_flags = 0
        self.showUp = False
        self.packagez = False
        self.cii = None


    def getId(self) -> int:
        """方法 getId"""
        return 0

    def getOnSale(self) -> int:
        """方法 getOnSale"""
        return 0

    def getExpire(self) -> int:
        """方法 getExpire"""
        return 0

    def getCount(self) -> int:
        """方法 getCount"""
        return 0

    def getPrice(self) -> int:
        """方法 getPrice"""
        return 0

    def getSN(self) -> int:
        """方法 getSN"""
        return 0

    def getPeriod(self) -> int:
        """方法 getPeriod"""
        return 0

    def getGender(self) -> int:
        """方法 getGender"""
        return 0

    def onSale(self) -> bool:
        """方法 onSale"""
        return False

    def genderEquals(self, g: int) -> bool:
        """方法 genderEquals"""
        return False

    def toCItem(self, backup: Any) -> Any:
        """方法 toCItem"""
        raise NotImplementedError("方法 toCItem 尚未实现")

