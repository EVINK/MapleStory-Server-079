"""
CashItem - Converted from Java source
Original: server/CashItem.java
Package: server
"""

from typing import Optional, Any


class CashItem:
    """
    Class CashItem
    """

    def __init__(self, category: int, subcategory: int, parent: int, image: str, sn: int, itemid: int, flag: int, price: int, discountPrice: int, quantity: int, expire: int, gender: int, likes: int):
        self.category = None
        self.subcategory = None
        self.parent = None
        self.sn = None
        self.itemid = None
        self.flag = None
        self.price = None
        self.discountPrice = None
        self.quantity = None
        self.expire = None
        self.gender = None
        self.likes = None
        self.image = None
        self.category = category
        self.subcategory = subcategory
        self.parent = parent
        self.image = image
        self.sn = sn
        self.itemid = itemid
        self.flag = flag
        self.price = price
        self.discountPrice = discountPrice
        self.quantity = quantity
        self.expire = expire
        self.gender = gender
        self.likes = likes


    def getCategory(self) -> int:
        return self.category

    def getSubCategory(self) -> int:
        return self.subcategory

    def getParent(self) -> int:
        return self.parent

    def getImage(self) -> str:
        return self.image

    def getSN(self) -> int:
        return self.sn

    def getItemId(self) -> int:
        return self.itemid

    def getFlag(self) -> int:
        return self.flag

    def getPrice(self) -> int:
        return self.price

    def getDiscountPrice(self) -> int:
        return self.discountPrice

    def getQuantity(self) -> int:
        return self.quantity

    def getExpire(self) -> int:
        return self.expire

    def getGender(self) -> int:
        return self.gender

    def getLikes(self) -> int:
        return self.likes

