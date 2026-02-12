"""
ModifyInventory - Converted from Java source
Original: client/inventory/ModifyInventory.java
Package: client.inventory
"""

from typing import Optional, Any

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes


class ModifyInventory:
    """
    Class ModifyInventory
    """

    ADD = 0
    UPDATE = 1
    MOVE = 2
    REMOVE = 3

    def __init__(self, mode: int, item: Any):
        self.mode = 0
        self.item = None
        self.oldPos = 0
        self.mode = mode
        self.item = item.copy()


    def getMode(self) -> int:
        return self.mode

    def getInventoryType(self) -> int:
        return GameConstants.getInventoryType(self.item.getItemId()).getType()

    def getPosition(self) -> int:
        return self.item.getPosition()

    def getOldPosition(self) -> int:
        return self.oldPos

    def getQuantity(self) -> int:
        return self.item.getQuantity()

    def getItem(self) -> Any:
        return self.item

    def clear(self) -> None:
        self.item = None


# Inner class from Java (originally nested)
class Types:
    """
    Class Types
    """

    ADD = 0
    UPDATE = 1
    MOVE = 2
    REMOVE = 3


