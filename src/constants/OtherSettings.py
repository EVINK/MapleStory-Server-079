"""
OtherSettings - 从Java源文件转换而来
对应Java源文件: constants/OtherSettings.java
包路径: constants
"""

from configparser import ConfigParser
from io import TextIOWrapper
from io import open
import json
import logging
import os


class OtherSettings:
    """
    类 OtherSettings - 从Java类转换
    """

    def __init__(self):
        """初始化 OtherSettings"""
        self.itempb_cfg = None


    def getInstance(self) -> Any:
        """方法 getInstance"""
        return getattr(self, 'instance', None)

    def getItempb_id(self) -> list:
        """方法 getItempb_id"""
        return getattr(self, 'itempb_id', [])

    def getItemgy_id(self) -> list:
        """方法 getItemgy_id"""
        return getattr(self, 'itemgy_id', [])

    def getItemjy_id(self) -> list:
        """方法 getItemjy_id"""
        return getattr(self, 'itemjy_id', [])

    def getMappb_id(self) -> list:
        """方法 getMappb_id"""
        return getattr(self, 'mappb_id', [])

    def isCANLOG(self) -> bool:
        """方法 isCANLOG"""
        return bool(getattr(self, 'canlog', False))

    def setCANLOG(self, CANLOG: bool) -> None:
        """方法 setCANLOG"""
        self.canlog = CANLOG
        return None

