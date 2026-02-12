"""
MapleGuildSummary - 从Java源文件转换而来
对应Java源文件: handling/world/guild/MapleGuildSummary.java
包路径: handling.world.guild
"""


class MapleGuildSummary:
    """
    类 MapleGuildSummary - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, g: Any):
        """初始化 MapleGuildSummary"""
        self.name = None
        self.logoBG = None
        self.logoBGColor = None
        self.logo = None
        self.logoColor = None
        self.allianceid = None


    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def getLogoBG(self) -> int:
        """方法 getLogoBG"""
        return getattr(self, 'logo_bg', 0)

    def getLogoBGColor(self) -> int:
        """方法 getLogoBGColor"""
        return getattr(self, 'logo_bg_color', 0)

    def getLogo(self) -> int:
        """方法 getLogo"""
        return getattr(self, 'logo', 0)

    def getLogoColor(self) -> int:
        """方法 getLogoColor"""
        return getattr(self, 'logo_color', 0)

    def getAllianceId(self) -> int:
        """方法 getAllianceId"""
        return getattr(self, 'alliance_id', 0)

