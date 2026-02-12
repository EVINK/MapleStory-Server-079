"""
AuctionPoint - 从Java源文件转换而来
对应Java源文件: server/custom/auction/AuctionPoint.java
包路径: server.custom.auction
"""


class AuctionPoint:
    """
    类 AuctionPoint - 从Java类转换
    """

    def __init__(self):
        """初始化 AuctionPoint"""
        self.characterid = 0
        self.point = 0
        self.point_sell = 0
        self.point_buy = 0


    def getCharacterid(self) -> int:
        """方法 getCharacterid"""
        return getattr(self, 'characterid', 0)

    def setCharacterid(self, characterid: int) -> None:
        """方法 setCharacterid"""
        self.characterid = characterid
        return None

    def getPoint(self) -> int:
        """方法 getPoint"""
        return getattr(self, 'point', 0)

    def setPoint(self, point: int) -> None:
        """方法 setPoint"""
        self.point = point
        return None

    def getPoint_sell(self) -> int:
        """方法 getPoint_sell"""
        return getattr(self, 'point_sell', 0)

    def setPoint_sell(self, point_sell: int) -> None:
        """方法 setPoint_sell"""
        self.point_sell = point_sell
        return None

    def getPoint_buy(self) -> int:
        """方法 getPoint_buy"""
        return getattr(self, 'point_buy', 0)

    def setPoint_buy(self, point_buy: int) -> None:
        """方法 setPoint_buy"""
        self.point_buy = point_buy
        return None

