"""
FishingConstants - Converted from Java source
Original: constants/FishingConstants.java
Package: constants
"""

from configparser import ConfigParser
from io import TextIOWrapper
from io import open
from typing import Optional, Any
import json
import logging
import os
import sys


class FishingConstants:
    """
    Class FishingConstants
    """

    def __init__(self):
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
        self.itempb_cfg = Properties()
        try:
            path = os.environ.get("server_property_fish_path")
            is = FileReader(path)
            # final InputStreamReader is = new FileReader("HuaiMS_钓鱼设置.properties");
            localThrowable2 = None
            try:
                self.itempb_cfg.load(is)
            except IOError as localThrowable3:
                localThrowable2 = localThrowable3
                raise localThrowable3
            finally:
                if is is not None:
                    if localThrowable2 is not None:
                        try:
                            is.close()
                        except IOError as x2:
                            localThrowable2.addSuppressed(x2)
                    else:
                        is.close()
        except Exception as e:
            FishingConstants.log.error("Could not configuration", e)
        self.FishingItem = self.itempb_cfg.getProperty("FishingItem").split(",")
        self.FishingItemS = self.itempb_cfg.getProperty("FishingItemS").split(",")
        self.FishingItemSJ = int(self.itempb_cfg.getProperty("FishingItemSJ"))
        self.FishingItemSLS = int(self.itempb_cfg.getProperty("FishingItemSLS"))
        self.FishingItemSL = int(self.itempb_cfg.getProperty("FishingItemSL"))
        self.FishingVIPSJ = int(self.itempb_cfg.getProperty("FishingVIPSJ"))
        self.FishingSJ = int(self.itempb_cfg.getProperty("FishingSJ"))
        self.FishingMeso = int(self.itempb_cfg.getProperty("FishingMeso"))
        self.FishingMesoS = int(self.itempb_cfg.getProperty("FishingMesoS"))
        self.FishingExp = int(self.itempb_cfg.getProperty("FishingExp"))
        self.FishingExpS = int(self.itempb_cfg.getProperty("FishingExpS"))

    # Static initializer
    # FishingConstants.instance = None
    # log = LoggerFactory.getLogger(FishingConstants.class)


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getFishingItem(self) -> list:
        return self.FishingItem

    def getFishingItemS(self) -> list:
        return self.FishingItemS

    def getFishingItemSJ(self) -> int:
        return self.FishingItemSJ

    def getFishingItemSLS(self) -> int:
        return self.FishingItemSLS

    def getFishingItemSL(self) -> int:
        return self.FishingItemSL

    def getFishingVIPSJ(self) -> int:
        return self.FishingVIPSJ

    def getFishingSJ(self) -> int:
        return self.FishingSJ

    def getFishingMeso(self) -> int:
        return self.FishingMeso

    def getFishingMesoS(self) -> int:
        return self.FishingMesoS

    def getFishingExp(self) -> int:
        return self.FishingExp

    def getFishingExpS(self) -> int:
        return self.FishingExpS

    def isCANLOG(self) -> bool:
        return FishingConstants.CANLOG

    def setCANLOG(self, CANLOG: bool) -> None:
        FishingConstants.CANLOG = CANLOG

