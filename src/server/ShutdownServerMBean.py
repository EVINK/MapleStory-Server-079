"""
ShutdownServerMBean - Converted from Java source
Original: server/ShutdownServerMBean.java
Package: server
"""

from typing import Optional, Any
import threading


from abc import ABC, abstractmethod

class ShutdownServerMBean(ABC):
    """Interface ShutdownServerMBean"""

    @abstractmethod
    def shutdown(self) -> None:
        pass

