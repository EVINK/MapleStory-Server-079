"""
LifeMovementFragment - Converted from Java source
Original: server/movement/LifeMovementFragment.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class LifeMovementFragment(ABC):
    """Interface LifeMovementFragment"""

    @abstractmethod
    def serialize(self, p0: Any) -> None:
        pass

    @abstractmethod
    def getPosition(self) -> Any:
        pass

