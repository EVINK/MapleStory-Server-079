"""
BanishInfo - Converted from Java source
Original: server/life/BanishInfo.java
Package: server.life
"""

from typing import Optional, Any


class BanishInfo:
    """
    Class BanishInfo
    """

    def __init__(self, msg: str, map: int, portal: str):
        self.map = None
        self.portal = None
        self.msg = None
        self.msg = msg
        self.map = map
        self.portal = portal


    def getMap(self) -> int:
        return self.map

    def getPortal(self) -> str:
        return self.portal

    def getMsg(self) -> str:
        return self.msg

