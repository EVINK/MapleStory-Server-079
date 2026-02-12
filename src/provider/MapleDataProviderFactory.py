"""
MapleDataProviderFactory - Converted from Java source
Original: provider/MapleDataProviderFactory.java
Package: provider
"""

from pathlib import Path
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.WzXML.XMLWZFile import *  # TODO: import specific classes


class MapleDataProviderFactory:
    """
    Class MapleDataProviderFactory
    """

    # Static initializer
    # wzPath = os.environ.get("wzPath", "wz")


    @staticmethod
    def getWZ(in: Any, provideImages: bool) -> Any:
        if isinstance(in, File):
            fileIn = in
            return XMLWZFile(fileIn)
        raise ValueError("Can't create data provider for input " + in)

    def getDataProvider(self, in: Any) -> Any:
        return getWZ(in, False)

    def getImageProvidingDataProvider(self, in: Any) -> Any:
        return getWZ(in, True)

    def fileInwzPath(self, filename: str) -> Any:
        return File(MapleDataProviderFactory.wzPath, filename)

