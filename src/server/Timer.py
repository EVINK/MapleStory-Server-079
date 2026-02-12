"""
Timer - Converted from Java source
Original: server/Timer.java
Package: server
"""

from concurrent.futures import Future
from threading import Lock
from typing import List
from typing import Optional, Any
import sched
import threading
import time

# Internal module imports
# from tools.FileoutputUtil import *  # TODO: import specific classes


class Timer:
    """
    Class Timer
    """

    def __init__(self):
        self.ses = None
        self.file = ""
        self.name = ""
        self.threadNumber = 0

    # Static initializer
    # instance = WorldTimer()


    def start(self) -> None:
        if self.ses is not None && !self.ses.isShutdown() && !self.ses.isTerminated():
            return
        self.file = "logs/Log_" + self.name + "_Except.rtf"
        tname = self.name + Randomizer.nextInt()
        thread = ThreadFactory()
            threadNumber = AtomicInteger(1)
            public Thread newThread(final Runnable r)
                t = Thread(r)
                t.setName(tname + "-Worker-" + self.threadNumber.getAndIncrement())
                return t
        stpe = ScheduledThreadPoolExecutor(3, thread)
        stpe.setKeepAliveTime(10, TimeUnit.MINUTES)
        stpe.allowCoreThreadTimeOut(True)
        stpe.setCorePoolSize(4)
        stpe.setMaximumPoolSize(8)
        stpe.setContinueExistingPeriodicTasksAfterShutdownPolicy(False)
        self.ses = stpe

    def newThread(self, r: Any) -> Any:
        t = Thread(r)
        t.setName(tname + "-Worker-" + self.threadNumber.getAndIncrement())
        return t

    def stop(self) -> None:
        self.ses.shutdown()

    def register(self, r: Any, repeatTime: int, delay: int) -> Any:
        if self.ses is None:
            return None
        return self.ses.scheduleAtFixedRate(LoggingSaveRunnable(r, self.file), delay, repeatTime, TimeUnit.MILLISECONDS)

    def register_r_repeatTime(self, r: Any, repeatTime: int) -> Any:
        if self.ses is None:
            return None
        return self.ses.scheduleAtFixedRate(LoggingSaveRunnable(r, self.file), 0, repeatTime, TimeUnit.MILLISECONDS)

    def schedule(self, r: Any, delay: int) -> Any:
        if self.ses is None:
            return None
        return self.ses.schedule(LoggingSaveRunnable(r, self.file), delay, TimeUnit.MILLISECONDS)

    def scheduleAtTimestamp(self, r: Any, timestamp: int) -> Any:
        return self.schedule(r, timestamp - int(time.time() * 1000))

    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def run(self) -> None:
        try:
            self.r.run()
        except Exception as t:
            FileoutputUtil.outputFileError(self.file, t)


# Inner class from Java (originally nested)
class WorldTimer(Timer):
    """
    Class WorldTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Worldtimer"

    # Static initializer
    # instance = WorldTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class MapTimer(Timer):
    """
    Class MapTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Maptimer"

    # Static initializer
    # instance = MapTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class BuffTimer(Timer):
    """
    Class BuffTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Bufftimer"

    # Static initializer
    # instance = BuffTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class TimerManager(Timer):
    """
    Class TimerManager
    Extends: Timer
    """

    def __init__(self):
        self.name = "TimerManager"

    # Static initializer
    # instance = TimerManager()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class EventTimer(Timer):
    """
    Class EventTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Eventtimer"

    # Static initializer
    # instance = EventTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class CloneTimer(Timer):
    """
    Class CloneTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Clonetimer"

    # Static initializer
    # instance = CloneTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class EtcTimer(Timer):
    """
    Class EtcTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Etctimer"

    # Static initializer
    # instance = EtcTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class MobTimer(Timer):
    """
    Class MobTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Mobtimer"

    # Static initializer
    # instance = MobTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class CheatTimer(Timer):
    """
    Class CheatTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Cheattimer"

    # Static initializer
    # instance = CheatTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class PingTimer(Timer):
    """
    Class PingTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "Pingtimer"

    # Static initializer
    # instance = PingTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class PGTimer(Timer):
    """
    Class PGTimer
    Extends: Timer
    """

    def __init__(self):
        self.name = "PGTimer"

    # Static initializer
    # instance = PGTimer()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Inner class from Java (originally nested)
class LoggingSaveRunnable(Runnable):
    """
    Class LoggingSaveRunnable
    Implements: Runnable
    """

    def __init__(self, r: Any, file: str):
        self.r = r
        self.file = file


    def run(self) -> None:
        try:
            self.r.run()
        except Exception as t:
            FileoutputUtil.outputFileError(self.file, t)

