"""
FishingConstants - 从Java源文件转换而来
对应Java源文件: constants/FishingConstants.java
包路径: constants
"""

from configparser import ConfigParser
from io import TextIOWrapper
from io import open
import json
import logging
import os


class FishingConstants:
    """
    类 FishingConstants - 从Java类转换
    """

    def __init__(self):
        """初始化 FishingConstants"""
        self.itempb_cfg = None
        self.FishingItemSJ = None
        self.FishingItemSL = None
        self.FishingItemSLS = None
        self.FishingVIPSJ = None
        self.FishingSJ = None
        self.FishingMeso = None
        self.FishingMesoS = None
        self.FishingExp = None
        self.FishingExpS = None


    def getInstance(self) -> Any:
        """方法 getInstance"""
        raise NotImplementedError("方法 getInstance 尚未实现")

    def getFishingItem(self) -> list:
        """方法 getFishingItem"""
        return []

    def getFishingItemS(self) -> list:
        """方法 getFishingItemS"""
        return []

    def getFishingItemSJ(self) -> int:
        """方法 getFishingItemSJ"""
        return 0

    def getFishingItemSLS(self) -> int:
        """方法 getFishingItemSLS"""
        return 0

    def getFishingItemSL(self) -> int:
        """方法 getFishingItemSL"""
        return 0

    def getFishingVIPSJ(self) -> int:
        """方法 getFishingVIPSJ"""
        return 0

    def getFishingSJ(self) -> int:
        """方法 getFishingSJ"""
        return 0

    def getFishingMeso(self) -> int:
        """方法 getFishingMeso"""
        return 0

    def getFishingMesoS(self) -> int:
        """方法 getFishingMesoS"""
        return 0

    def getFishingExp(self) -> int:
        """方法 getFishingExp"""
        return 0

    def getFishingExpS(self) -> int:
        """方法 getFishingExpS"""
        return 0

    def isCANLOG(self) -> bool:
        """方法 isCANLOG"""
        return False

    def setCANLOG(self, CANLOG: bool) -> None:
        """方法 setCANLOG"""
        pass

