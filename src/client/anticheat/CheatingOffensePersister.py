"""
CheatingOffensePersister - Converted from Java source
Original: client/anticheat/CheatingOffensePersister.java
Package: client.anticheat
"""

from threading import Lock
from threading import RLock
from typing import List
from typing import Optional, Any
from typing import Set
import threading

# Internal module imports
# from server.Timer import *  # TODO: import specific classes


class CheatingOffensePersister:
    """
    Class CheatingOffensePersister
    """

    def __init__(self):
        self.toPersist = None
        self.mutex = None
        self.toPersist = new LinkedHashSet<CheatingOffenseEntry>()
        self.mutex = ReentrantLock()
        Timer.CheatTimer.getInstance().register(PersistingTask(), 61000)

    # Static initializer
    # instance = CheatingOffensePersister()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def persistEntry(self, coe: Any) -> None:
        self.mutex.lock()
        try:
            self.toPersist.remove(coe)
            self.toPersist.add(coe)
        finally:
            self.mutex.unlock()

    def run(self) -> None:
        CheatingOffensePersister.self.mutex.lock()
        try:
            CheatingOffensePersister.self.toPersist.clear()
        finally:
            CheatingOffensePersister.self.mutex.unlock()


# Inner class from Java (originally nested)
class PersistingTask(Runnable):
    """
    Class PersistingTask
    Implements: Runnable
    """


    def run(self) -> None:
        CheatingOffensePersister.self.mutex.lock()
        try:
            CheatingOffensePersister.self.toPersist.clear()
        finally:
            CheatingOffensePersister.self.mutex.unlock()

