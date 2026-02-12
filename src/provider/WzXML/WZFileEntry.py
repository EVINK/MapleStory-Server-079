"""
WZFileEntry - Converted from Java source
Original: provider/WzXML/WZFileEntry.java
Package: provider.WzXML
"""

from typing import Optional, Any

# Internal module imports
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes


class WZFileEntry(WZEntry, MapleDataFileEntry):
    """
    Class WZFileEntry
    Extends: WZEntry
    Implements: MapleDataFileEntry
    """

    def __init__(self, name: str, size: int, checksum: int, parent: Any):
        self.offset = 0
        super(name, size, checksum, parent)


    def getOffset(self) -> int:
        return self.offset

    def setOffset(self, offset: int) -> None:
        self.offset = offset

