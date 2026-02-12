"""
CashItemInfo - Converted from Java source
Original: server/CashItemInfo.java
Package: server
"""

from typing import Optional, Any


class CashItemInfo:
    """
    Class CashItemInfo
    """

    def __init__(self, itemId: int, count: int, price: int, sn: int, expire: int, gender: int, sale: bool):
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
        self.itemId = itemId
        self.count = count
        self.price = price
        self.sn = sn
        self.expire = expire
        self.gender = gender
        self.onSale = sale


    def getId(self) -> int:
        return self.itemId

    def getOnSale(self) -> int:
        if self.onSale:
            return 1
        return 0

    def getExpire(self) -> int:
        return self.expire

    def getCount(self) -> int:
        return self.count

    def getPrice(self) -> int:
        return self.price

    def getSN(self) -> int:
        return self.sn

    def getPeriod(self) -> int:
        return self.expire

    def getGender(self) -> int:
        return self.gender

    def onSale(self) -> bool:
        return self.onSale or (CashItemFactory.getInstance().getModInfo(self.sn) is not None and CashItemFactory.getInstance().getModInfo(self.sn).showUp)

    def genderEquals(self, g: int) -> bool:
        return g == self.gender or self.gender == 2

    def toCItem(self, backup: Any) -> Any:
        if self.cii is not None:
            return self.cii
        item = None
        if self.itemid <= 0:
            item = ((backup is None) ? 0 : backup.getId())
        else:
            item = self.itemid
        c = None
        if self.count <= 0:
            c = ((backup is None) ? 0 : backup.getCount())
        else:
            c = self.count
        price = None
        if self.meso <= 0:
            if self.discountPrice <= 0:
                price = ((backup is None) ? 0 : backup.getPrice())
            else:
                price = self.discountPrice
        else:
            price = self.meso
        expire = None
        if self.period <= 0:
            expire = ((backup is None) ? 0 : backup.getPeriod())
        else:
            expire = self.period
        gen = None
        if self.gender < 0:
            gen = ((backup is None) ? 0 : backup.getGender())
        else:
            gen = self.gender
        onSale = None
        if not self.showUp:
            onSale = (backup is not None and backup.onSale())
        else:
            onSale = self.showUp
        return self.cii = CashItemInfo(item, c, price, self.sn, expire, gen, onSale)


# Inner class from Java (originally nested)
class CashModInfo:
    """
    Class CashModInfo
    """

    def __init__(self, sn: int, discount: int, mark: int, show: bool, itemid: int, priority: int, packagez: bool, period: int, gender: int, count: int, meso: int, unk_1: int, unk_2: int, unk_3: int, extra_flags: int):
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
        self.sn = sn
        self.itemid = itemid
        self.discountPrice = discount
        self.mark = mark
        self.showUp = show
        self.priority = priority
        self.packagez = packagez
        self.period = period
        self.gender = gender
        self.count = count
        self.meso = meso
        self.unk_1 = unk_1
        self.unk_2 = unk_2
        self.unk_3 = unk_3
        self.extra_flags = extra_flags
        self.flags = extra_flags
        if self.itemid > 0:
            self.flags |= 0x1
        if self.count > 0:
            self.flags |= 0x2
        if self.discountPrice > 0:
            self.flags |= 0x4
        if (self.unk_1 > 0) {}
        if self.priority >= 0:
            self.flags |= 0x10
        if self.period > 0:
            self.flags |= 0x20
        if self.meso > 0:
            self.flags |= 0x80
        if (self.unk_2 > 0) {}
        if self.gender >= 0:
            self.flags |= 0x200
        if self.showUp:
            self.flags |= 0x400
        if self.mark >= -1 or self.mark <= 3:
            self.flags |= 0x800
        if (self.unk_3 > 0) {}
        if self.packagez:
            self.flags |= 0x20000


    def toCItem(self, backup: Any) -> Any:
        if self.cii is not None:
            return self.cii
        item = None
        if self.itemid <= 0:
            item = ((backup is None) ? 0 : backup.getId())
        else:
            item = self.itemid
        c = None
        if self.count <= 0:
            c = ((backup is None) ? 0 : backup.getCount())
        else:
            c = self.count
        price = None
        if self.meso <= 0:
            if self.discountPrice <= 0:
                price = ((backup is None) ? 0 : backup.getPrice())
            else:
                price = self.discountPrice
        else:
            price = self.meso
        expire = None
        if self.period <= 0:
            expire = ((backup is None) ? 0 : backup.getPeriod())
        else:
            expire = self.period
        gen = None
        if self.gender < 0:
            gen = ((backup is None) ? 0 : backup.getGender())
        else:
            gen = self.gender
        onSale = None
        if not self.showUp:
            onSale = (backup is not None and backup.onSale())
        else:
            onSale = self.showUp
        return self.cii = CashItemInfo(item, c, price, self.sn, expire, gen, onSale)

