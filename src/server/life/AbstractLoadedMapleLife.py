"""
AbstractLoadedMapleLife - 从Java源文件转换而来
对应Java源文件: server/life/AbstractLoadedMapleLife.java
包路径: server.life
"""

# 内部模块导入 (Internal module imports)
# from server.maps.AbstractAnimatedMapleMapObject import *  # TODO: 根据实际需要导入具体类


class AbstractLoadedMapleLife(AbstractAnimatedMapleMapObject, ABC):
    """
    类 AbstractLoadedMapleLife - 从Java类转换
    继承自: AbstractAnimatedMapleMapObject
    """

    def __init__(self, id: int):
        """初始化 AbstractLoadedMapleLife"""
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


    def getF(self) -> int:
        """方法 getF"""
        return getattr(self, 'f', 0)

    def setF(self, f: int) -> None:
        """方法 setF"""
        self.f = f
        return None

    def isHidden(self) -> bool:
        """方法 isHidden"""
        return bool(getattr(self, 'hidden', False))

    def setHide(self, hide: bool) -> None:
        """方法 setHide"""
        self.hide = hide
        return None

    def originFh(self) -> int:
        """方法 originFh"""
        return 0

    def getFh(self) -> int:
        """方法 getFh"""
        return getattr(self, 'fh', 0)

    def setFh(self, fh: int) -> None:
        """方法 setFh"""
        self.fh = fh
        return None

    def getCy(self) -> int:
        """方法 getCy"""
        return getattr(self, 'cy', 0)

    def setCy(self, cy: int) -> None:
        """方法 setCy"""
        self.cy = cy
        return None

    def getRx0(self) -> int:
        """方法 getRx0"""
        return getattr(self, 'rx0', 0)

    def setRx0(self, rx0: int) -> None:
        """方法 setRx0"""
        self.rx0 = rx0
        return None

    def getRx1(self) -> int:
        """方法 getRx1"""
        return getattr(self, 'rx1', 0)

    def setRx1(self, rx1: int) -> None:
        """方法 setRx1"""
        self.rx1 = rx1
        return None

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def getMTime(self) -> int:
        """方法 getMTime"""
        return getattr(self, 'm_time', 0)

    def setMTime(self, mtime: int) -> None:
        """方法 setMTime"""
        self.m_time = mtime
        return None

    def getCType(self) -> str:
        """方法 getCType"""
        return getattr(self, 'c_type', "")

    def setCType(self, type: str) -> None:
        """方法 setCType"""
        self.c_type = type
        return None

