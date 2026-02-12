"""
PlayerBuffValueHolder - Converted from Java source
Original: handling/world/PlayerBuffValueHolder.java
Package: handling.world
"""

from typing import Optional, Any

# Internal module imports
# from server.MapleStatEffect import *  # TODO: import specific classes


class PlayerBuffValueHolder:
    """
    Class PlayerBuffValueHolder
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, startTime: int, effect: Any):
        self.startTime = 0
        self.effect = None
        self.startTime = startTime
        self.effect = effect


