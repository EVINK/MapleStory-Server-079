"""
MapleGuildSummary - Converted from Java source
Original: handling/world/guild/MapleGuildSummary.java
Package: handling.world.guild
"""

from typing import Optional, Any


class MapleGuildSummary:
    """
    Class MapleGuildSummary
    Implements: Serializable
    """

    def __init__(self, g: Any):
        self.name = None
        self.logoBG = None
        self.logoBGColor = None
        self.logo = None
        self.logoColor = None
        self.allianceid = None
        self.name = g.getName()
        self.logoBG = g.getLogoBG()
        self.logoBGColor = g.getLogoBGColor()
        self.logo = g.getLogo()
        self.logoColor = g.getLogoColor()
        self.allianceid = g.getAllianceId()

    # Static initializer
    # MapleGuildSummary.serialVersionUID = 3565477792085301248


    def getName(self) -> str:
        return self.name

    def getLogoBG(self) -> int:
        return self.logoBG

    def getLogoBGColor(self) -> int:
        return self.logoBGColor

    def getLogo(self) -> int:
        return self.logo

    def getLogoColor(self) -> int:
        return self.logoColor

    def getAllianceId(self) -> int:
        return self.allianceid

