"""
MapleBuffStatValueHolder - Converted from Java source
Original: client/MapleBuffStatValueHolder.java
Package: client
"""

from concurrent.futures import Future
from typing import List
from typing import Optional, Any
import sched

# Internal module imports
# from server import *  # TODO: import specific classes


class MapleBuffStatValueHolder:
    """
    Class MapleBuffStatValueHolder
    """

    def __init__(self, effect: Any, startTime: int, schedule: Any, value: int):
        self.effect = None
        self.startTime = 0
        self.value = 0
        self.effect = effect
        self.startTime = startTime
        self.schedule = schedule
        self.value = value


