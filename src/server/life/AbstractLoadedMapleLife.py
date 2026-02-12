"""
AbstractLoadedMapleLife - Converted from Java source
Original: server/life/AbstractLoadedMapleLife.java
Package: server.life
"""

from typing import Optional, Any

# Internal module imports
# from server.maps.AbstractAnimatedMapleMapObject import *  # TODO: import specific classes


class AbstractLoadedMapleLife(AbstractAnimatedMapleMapObject, ABC):
    """
    Class AbstractLoadedMapleLife
    Extends: AbstractAnimatedMapleMapObject
    """

    def __init__(self, id: int):
        self.id = 0
        self.f = 0
        self.hide = False
        self.fh = 0
        self.originFh = 0
        self.cy = 0
        self.rx0 = 0
        self.rx1 = 0
        self.ctype = ""
        self.mtime = 0
        self.id = id


    def getF(self) -> int:
        return self.f

    def setF(self, f: int) -> None:
        self.f = f

    def isHidden(self) -> bool:
        return self.hide

    def setHide(self, hide: bool) -> None:
        self.hide = hide

    def originFh(self) -> int:
        return self.originFh

    def getFh(self) -> int:
        return self.fh

    def setFh(self, fh: int) -> None:
        self.fh = fh

    def getCy(self) -> int:
        return self.cy

    def setCy(self, cy: int) -> None:
        self.cy = cy

    def getRx0(self) -> int:
        return self.rx0

    def setRx0(self, rx0: int) -> None:
        self.rx0 = rx0

    def getRx1(self) -> int:
        return self.rx1

    def setRx1(self, rx1: int) -> None:
        self.rx1 = rx1

    def getId(self) -> int:
        return self.id

    def getMTime(self) -> int:
        return self.mtime

    def setMTime(self, mtime: int) -> None:
        self.mtime = mtime

    def getCType(self) -> str:
        return self.ctype

    def setCType(self, type: str) -> None:
        self.ctype = type

