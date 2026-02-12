"""
BossRankInfo - 从Java源文件转换而来
对应Java源文件: server/custom/bossrank/BossRankInfo.java
包路径: server.custom.bossrank
"""


class BossRankInfo:
    """
    类 BossRankInfo - 从Java类转换
    """

    def __init__(self):
        """初始化 BossRankInfo"""
        self.cid = 0
        self.cname = ""
        self.bossname = ""
        self.points = 0
        self.count = 0


    def getCid(self) -> int:
        """方法 getCid"""
        return getattr(self, 'cid', 0)

    def setCid(self, cid: int) -> None:
        """方法 setCid"""
        self.cid = cid
        return None

    def getCname(self) -> str:
        """方法 getCname"""
        return getattr(self, 'cname', "")

    def setCname(self, cname: str) -> None:
        """方法 setCname"""
        self.cname = cname
        return None

    def getBossname(self) -> str:
        """方法 getBossname"""
        return getattr(self, 'bossname', "")

    def setBossname(self, bossname: str) -> None:
        """方法 setBossname"""
        self.bossname = bossname
        return None

    def getPoints(self) -> int:
        """方法 getPoints"""
        return getattr(self, 'points', 0)

    def setPoints(self, points: int) -> None:
        """方法 setPoints"""
        self.points = points
        return None

    def getCount(self) -> int:
        """方法 getCount"""
        return getattr(self, 'count', 0)

    def setCount(self, count: int) -> None:
        """方法 setCount"""
        self.count = count
        return None

