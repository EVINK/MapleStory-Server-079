"""
AuctionPoint1 - 从Java源文件转换而来
对应Java源文件: server/custom/auction1/AuctionPoint1.java
包路径: server.custom.auction1
"""


class AuctionPoint1:
    """
    类 AuctionPoint1 - 从Java类转换
    """

    def __init__(self):
        """初始化 AuctionPoint1"""
        self.characterid = 0
        self.point1 = 0
        self.point1_sell = 0
        self.point1_buy = 0


    def getCharacterid(self) -> int:
        """方法 getCharacterid"""
        return getattr(self, 'characterid', 0)

    def setCharacterid(self, characterid: int) -> None:
        """方法 setCharacterid"""
        self.characterid = characterid
        return None

    def getPoint1(self) -> int:
        """方法 getPoint1"""
        return getattr(self, 'point1', 0)

    def setPoint(self, point: int) -> None:
        """方法 setPoint"""
        self.point = point
        return None

    def getPoint1_sell(self) -> int:
        """方法 getPoint1_sell"""
        return getattr(self, 'point1_sell', 0)

    def setPoint1_sell(self, point1_sell: int) -> None:
        """方法 setPoint1_sell"""
        self.point1_sell = point1_sell
        return None

    def getPoint1_buy(self) -> int:
        """方法 getPoint1_buy"""
        return getattr(self, 'point1_buy', 0)

    def setPoint1_buy(self, point1_buy: int) -> None:
        """方法 setPoint1_buy"""
        self.point1_buy = point1_buy
        return None

