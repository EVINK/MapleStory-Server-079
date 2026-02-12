"""
CashItem - 从Java源文件转换而来
对应Java源文件: server/CashItem.java
包路径: server
"""


class CashItem:
    """
    类 CashItem - 从Java类转换
    """

    def __init__(self, category: int, subcategory: int, parent: int, image: str, sn: int, itemid: int, flag: int, price: int, discountPrice: int, quantity: int, expire: int, gender: int, likes: int):
        """初始化 CashItem"""
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


    def getCategory(self) -> int:
        """方法 getCategory"""
        return getattr(self, 'category', 0)

    def getSubCategory(self) -> int:
        """方法 getSubCategory"""
        return getattr(self, 'sub_category', 0)

    def getParent(self) -> int:
        """方法 getParent"""
        return getattr(self, 'parent', 0)

    def getImage(self) -> str:
        """方法 getImage"""
        return getattr(self, 'image', "")

    def getSN(self) -> int:
        """方法 getSN"""
        return getattr(self, 'sn', 0)

    def getItemId(self) -> int:
        """方法 getItemId"""
        return getattr(self, 'item_id', 0)

    def getFlag(self) -> int:
        """方法 getFlag"""
        return getattr(self, 'flag', 0)

    def getPrice(self) -> int:
        """方法 getPrice"""
        return getattr(self, 'price', 0)

    def getDiscountPrice(self) -> int:
        """方法 getDiscountPrice"""
        return getattr(self, 'discount_price', 0)

    def getQuantity(self) -> int:
        """方法 getQuantity"""
        return getattr(self, 'quantity', 0)

    def getExpire(self) -> int:
        """方法 getExpire"""
        return getattr(self, 'expire', 0)

    def getGender(self) -> int:
        """方法 getGender"""
        return getattr(self, 'gender', 0)

    def getLikes(self) -> int:
        """方法 getLikes"""
        return getattr(self, 'likes', 0)

