"""
PortalScript - Converted from Java source
Original: scripting/PortalScript.java
Package: scripting
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class PortalScript(ABC):
    """Interface PortalScript"""

    @abstractmethod
    def enter(self, p0: Any) -> None:
        pass

