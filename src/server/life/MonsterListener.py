"""
MonsterListener - Converted from Java source
Original: server/life/MonsterListener.java
Package: server.life
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MonsterListener(ABC):
    """Interface MonsterListener"""

    @abstractmethod
    def monsterKilled(self) -> None:
        pass

