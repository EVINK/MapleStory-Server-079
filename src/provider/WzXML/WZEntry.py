"""
WZEntry - Converted from Java source
Original: provider/WzXML/WZEntry.java
Package: provider.WzXML
"""

from typing import Optional, Any

# Internal module imports
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from provider.MapleDataEntry import *  # TODO: import specific classes


class WZEntry(MapleDataEntry):
    """
    Class WZEntry
    Implements: MapleDataEntry
    """

    def __init__(self, name: str, size: int, checksum: int, parent: Any):
        self.name = None
        self.size = None
        self.checksum = None
        self.offset = 0
        self.parent = None
        self.name = name
        self.size = size
        self.checksum = checksum
        self.parent = parent


    def getName(self) -> str:
        return self.name

    def getSize(self) -> int:
        return self.size

    def getChecksum(self) -> int:
        return self.checksum

    def getOffset(self) -> int:
        return self.offset

    def getParent(self) -> Any:
        return self.parent

