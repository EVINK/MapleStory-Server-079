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
        return 0

    def getSubCategory(self) -> int:
        """方法 getSubCategory"""
        return 0

    def getParent(self) -> int:
        """方法 getParent"""
        return 0

    def getImage(self) -> str:
        """方法 getImage"""
        return ""

    def getSN(self) -> int:
        """方法 getSN"""
        return 0

    def getItemId(self) -> int:
        """方法 getItemId"""
        return 0

    def getFlag(self) -> int:
        """方法 getFlag"""
        return 0

    def getPrice(self) -> int:
        """方法 getPrice"""
        return 0

    def getDiscountPrice(self) -> int:
        """方法 getDiscountPrice"""
        return 0

    def getQuantity(self) -> int:
        """方法 getQuantity"""
        return 0

    def getExpire(self) -> int:
        """方法 getExpire"""
        return 0

    def getGender(self) -> int:
        """方法 getGender"""
        return 0

    def getLikes(self) -> int:
        """方法 getLikes"""
        return 0

