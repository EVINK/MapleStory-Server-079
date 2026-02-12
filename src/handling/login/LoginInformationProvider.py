"""
LoginInformationProvider - Converted from Java source
Original: handling/login/LoginInformationProvider.java
Package: handling.login
"""

from pathlib import Path
from typing import List
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes


class LoginInformationProvider:
    """
    Class LoginInformationProvider
    """

    def __init__(self):
        self.ForbiddenName = []
        self.ForbiddenName = []
        wzPath = os.environ.get("wzPath")
        nameData = MapleDataProviderFactory.getDataProvider(File(wzPath + "/Etc.wz")).getData("ForbiddenName.img")
        for data in nameData.getChildren():
            self.ForbiddenName.add(MapleDataTool.getString(data))

    # Static initializer
    # instance = LoginInformationProvider()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def isForbiddenName(self, in: str) -> bool:
        for name in self.ForbiddenName:
            if (name in in):
                return True
        return False

