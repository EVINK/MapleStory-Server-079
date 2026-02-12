"""
CopyItemInfo - Converted from Java source
Original: client/messages/CopyItemInfo.java
Package: client.messages
"""

from typing import Optional, Any


class CopyItemInfo:
    """
    Class CopyItemInfo
    """

    def __init__(self, itemId: int, chrId: int, name: str):
        self.itemId = 0
        self.chrId = 0
        self.name = ""
        self.first = False
        self.itemId = itemId
        self.chrId = chrId
        self.name = name
        self.first = True


    def isFirst(self) -> bool:
        return self.first

    def setFirst(self, f: bool) -> None:
        self.first = f

