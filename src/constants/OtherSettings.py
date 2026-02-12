"""
OtherSettings - Converted from Java source
Original: constants/OtherSettings.java
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


class OtherSettings:
    """
    Class OtherSettings
    """

    def __init__(self):
        self.itempb_cfg = None
        self.itempb_cfg = Properties()
        try:
            path = os.environ.get("server_property_file_path")
            is = FileReader(path)
            # final InputStreamReader is = new FileReader("HuaiMS_服务端配置.properties");
            self.itempb_cfg.load(is)
            is.close()
            self.itempb_id = self.itempb_cfg.getProperty("cashban").split(",")
            self.itemjy_id = self.itempb_cfg.getProperty("cashjy", "0").split(",")
            self.itemgy_id = self.itempb_cfg.getProperty("gysj", "0").split(",")
        except IOError as e:
            OtherSettings.log.error("Could not configuration", e)

    # Static initializer
    # OtherSettings.instance = None
    # log = LoggerFactory.getLogger(OtherSettings.class)


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getItempb_id(self) -> list:
        return self.itempb_id

    def getItemgy_id(self) -> list:
        return self.itemgy_id

    def getItemjy_id(self) -> list:
        return self.itemjy_id

    def getMappb_id(self) -> list:
        return self.mappb_id

    def isCANLOG(self) -> bool:
        return OtherSettings.CANLOG

    def setCANLOG(self, CANLOG: bool) -> None:
        OtherSettings.CANLOG = CANLOG

