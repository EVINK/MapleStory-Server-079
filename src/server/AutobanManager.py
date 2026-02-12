"""
AutobanManager - Converted from Java source
Original: server/AutobanManager.java
Package: server
"""

from threading import RLock
from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set
import threading
import time

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class AutobanManager(Runnable):
    """
    Class AutobanManager
    Implements: Runnable
    """

    AUTOBAN_POINTS = 5000

    def __init__(self):
        self.points = None
        self.reasons = None
        self.expirations = None
        self.lock = None
        self.time = 0
        self.acc = 0
        self.points = 0
        self.points = {}
        self.reasons = new HashMap<Integer, List<String>>()
        self.expirations = new TreeSet<ExpirationEntry>()
        self.lock = ReentrantLock(True)

    # Static initializer
    # instance = AutobanManager()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def autoban(self, c: Any, reason: str) -> None:
        if c.getPlayer().isGM() or c.getPlayer().isClone():
            c.getPlayer().dropMessage(5, "[WARNING] A/b triggled : " + reason)
            return
        self.addPoints(c, AUTOBAN_POINTS, 0, reason)

    def addPoints(self, c: Any, points: int, expiration: int, reason: str) -> None:
        self.lock.lock()
        try:
            acc = c.getPlayer().getAccountID()
            if (acc in self.points):
                SavedPoints = self.points.get(acc)
                if SavedPoints >= AUTOBAN_POINTS:
                    return
                self.points.put(acc, SavedPoints + points)
                reasonList = self.reasons.get(acc)
                reasonList.add(reason)
            else:
                self.points.put(acc, points)
                reasonList = []
                reasonList.add(reason)
                self.reasons.put(acc, reasonList)
            if self.points.get(acc) >= AUTOBAN_POINTS:
                if c.getPlayer().isGM() or c.getPlayer().isClone():
                    c.getPlayer().dropMessage(5, "[WARNING] A/b triggled : " + reason)
                    return
                sb = ""
                sb.append(c.getPlayer().getName())
                sb.append(" (IP ")
                sb.append(c.getSession().getRemoteAddress())
                sb.append("): ")
                sb.append(" (MAC ")
                sb.append(c.getMac())
                sb.append("): ")
                for s in self.reasons.get(acc):
                    sb.append(s)
                    sb.append(", ")
                FileoutputUtil.logToFile_chr(c.getPlayer(), FileoutputUtil.ban_log, sb)
                c.getPlayer().ban(sb, False, True, False)
                World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "封号系统：玩家" + c.getPlayer().getName() + "使用非法程序，账号已被封处理'").encode("utf-8"))
                c.disconnect(True, False)
            elif expiration > 0:
                self.expirations.add(ExpirationEntry(int(time.time() * 1000) + expiration, acc, points))
        finally:
            self.lock.unlock()

    def run(self) -> None:
        now = int(time.time() * 1000)
        for e in self.expirations:
            if e.time > now:
                return
            self.points.put(e.acc, self.points.get(e.acc) - e.points)

    def compareTo(self, o: Any) -> int:
        return (int)(self.time - o.time)

    def equals(self, oth: Any) -> bool:
        if not (isinstance(oth, ExpirationEntry)):
            return False
        ee = oth
        return self.time == ee.time and self.points == ee.points and self.acc == ee.acc


# Inner class from Java (originally nested)
class ExpirationEntry:
    """
    Class ExpirationEntry
    Implements: Comparable<ExpirationEntry>
    """

    def __init__(self, time: int, acc: int, points: int):
        self.time = 0
        self.acc = 0
        self.points = 0
        self.time = time
        self.acc = acc
        self.points = points


    def compareTo(self, o: Any) -> int:
        return (int)(self.time - o.time)

    def equals(self, oth: Any) -> bool:
        if not (isinstance(oth, ExpirationEntry)):
            return False
        ee = oth
        return self.time == ee.time and self.points == ee.points and self.acc == ee.acc

