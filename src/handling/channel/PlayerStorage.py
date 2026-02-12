"""
PlayerStorage - Converted from Java source
Original: handling/channel/PlayerStorage.java
Package: handling.channel
"""

from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.CharacterTransfer import *  # TODO: import specific classes
# from handling.world.CheaterData import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes


class PlayerStorage:
    """
    Class PlayerStorage
    """

    def __init__(self, channel: int):
        self.mutex = None
        self.rL = None
        self.wL = None
        self.mutex2 = None
        self.rL2 = None
        self.wL2 = None
        self.nameToChar = None
        self.idToChar = None
        self.PendingCharacter = None
        self.channel = None
        self.mutex = ReentrantReadWriteLock()
        self.rL = self.mutex.readLock()
        self.wL = self.mutex.writeLock()
        self.mutex2 = ReentrantReadWriteLock()
        self.rL2 = self.mutex2.readLock()
        self.wL2 = self.mutex2.writeLock()
        self.nameToChar = {}
        self.idToChar = {}
        self.PendingCharacter = {}
        self.channel = channel
        Timer.PingTimer.getInstance().schedule(PersistingTask(), 900000)


    def getAllCharacters(self) -> list:
        self.rL.lock()
        try:
            return Collections.unmodifiableCollection((Collection<? extends MapleCharacter>)self.idToChar.values())
        finally:
            self.rL.unlock()

    def registerPlayer(self, chr: Any) -> None:
        self.wL.lock()
        try:
            self.nameToChar.put(chr.getName().lower(), chr)
            self.idToChar.put(chr.getId(), chr)
        finally:
            self.wL.unlock()
        World.Find.register(chr.getId(), chr.getName(), self.channel)

    def registerPendingPlayer(self, chr: Any, playerid: int) -> None:
        self.wL2.lock()
        try:
            self.PendingCharacter.put(playerid, chr)
        finally:
            self.wL2.unlock()

    def deregisterPlayer(self, chr: Any) -> None:
        self.wL.lock()
        try:
            self.nameToChar.remove(chr.getName().lower())
            self.idToChar.remove(chr.getId())
        finally:
            self.wL.unlock()
        World.Find.forceDeregister(chr.getId(), chr.getName())

    def deregisterPlayer_idz_namez(self, idz: int, namez: str) -> None:
        self.wL.lock()
        try:
            self.nameToChar.remove(namez.lower())
            self.idToChar.remove(idz)
        finally:
            self.wL.unlock()
        World.Find.forceDeregister(idz, namez)

    def deregisterPendingPlayer(self, charid: int) -> None:
        self.wL2.lock()
        try:
            self.PendingCharacter.remove(charid)
        finally:
            self.wL2.unlock()

    def getPendingCharacter(self, charid: int) -> Any:
        self.rL2.lock()
        toreturn = None
        try:
            toreturn = self.PendingCharacter.get(charid)
        finally:
            self.rL2.unlock()
        if toreturn is not None:
            self.deregisterPendingPlayer(charid)
        return toreturn

    def getCharacterByName(self, name: str) -> Any:
        self.rL.lock()
        try:
            return self.nameToChar.get(name.lower())
        finally:
            self.rL.unlock()

    def getCharacterById(self, id: int) -> Any:
        self.rL.lock()
        try:
            return self.idToChar.get(id)
        finally:
            self.rL.unlock()

    def getConnectedClients(self) -> int:
        return self.idToChar

    def getCheaters(self) -> list:
        cheaters = []
        self.rL.lock()
        try:
            for chr in self.nameToChar.values():
                if chr.getCheatTracker().getPoints() > 0:
                    cheaters.add(CheaterData(chr.getCheatTracker().getPoints(), MapleCharacterUtil.makeMapleReadable(chr.getName()) + " (" + chr.getCheatTracker().getPoints() + ") " + chr.getCheatTracker().getSummary()))
        finally:
            self.rL.unlock()
        return cheaters

    def disconnectAll(self) -> None:
        self.disconnectAll(False)

    def disconnectAll_checkGM(self, checkGM: bool) -> None:
        self.wL.lock()
        try:
            itr = self.nameToChar.values().iterator()
            while itr.hasNext():
                chr = itr.next()
                if !chr.isGM() || !checkGM:
                    chr.getClient().disconnect(False, False, True)
                    chr.getClient().getSession().close(True)
                    World.Find.forceDeregister(chr.getId(), chr.getName())
                    itr.remove()
        finally:
            self.wL.unlock()

    def getOnlinePlayers(self, byGM: bool) -> str:
        sb = ""
        if byGM:
            self.rL.lock()
            try:
                itr = self.nameToChar.values().iterator()
                while itr.hasNext():
                    sb.append(MapleCharacterUtil.makeMapleReadable(itr.next().getName()))
                    sb.append(", ")
            finally:
                self.rL.unlock()
        else:
            self.rL.lock()
            try:
                for chr in self.nameToChar.values():
                    if !chr.isGM():
                        sb.append(MapleCharacterUtil.makeMapleReadable(chr.getName()))
                        sb.append(", ")
            finally:
                self.rL.unlock()
        return sb

    def broadcastPacket(self, data: Any) -> None:
        self.rL.lock()
        try:
            itr = self.nameToChar.values().iterator()
            while itr.hasNext():
                itr.next().getClient().getSession().write(data)
        finally:
            self.rL.unlock()

    def broadcastSmegaPacket(self, data: Any) -> None:
        self.rL.lock()
        try:
            for chr in self.nameToChar.values():
                if chr.getClient().isLoggedIn() && chr.getSmega():
                    chr.getClient().getSession().write(data)
        finally:
            self.rL.unlock()

    def broadcastGMPacket(self, data: Any) -> None:
        self.rL.lock()
        try:
            for chr in self.nameToChar.values():
                if chr.getClient().isLoggedIn() && chr.isGM():
                    chr.getClient().getSession().write(data)
        finally:
            self.rL.unlock()

    def getAllCharactersThreadSafe(self) -> list:
        ret = []
        ret.addAll(self.getAllCharacters())
        return ret

    def run(self) -> None:
        PlayerStorage.self.wL2.lock()
        try:
            currenttime = int(time.time() * 1000)
            final Iterator<Map.Entry<Integer, CharacterTransfer>> itr = PlayerStorage.self.PendingCharacter.items().iterator()
            while itr.hasNext():
                if currenttime - itr.next().getValue().TranferTime > 40000:
                    itr.remove()
            Timer.PingTimer.getInstance().schedule(PersistingTask(), 900000)
        finally:
            PlayerStorage.self.wL2.unlock()


# Inner class from Java (originally nested)
class PersistingTask(Runnable):
    """
    Class PersistingTask
    Implements: Runnable
    """


    def run(self) -> None:
        PlayerStorage.self.wL2.lock()
        try:
            currenttime = int(time.time() * 1000)
            final Iterator<Map.Entry<Integer, CharacterTransfer>> itr = PlayerStorage.self.PendingCharacter.items().iterator()
            while itr.hasNext():
                if currenttime - itr.next().getValue().TranferTime > 40000:
                    itr.remove()
            Timer.PingTimer.getInstance().schedule(PersistingTask(), 900000)
        finally:
            PlayerStorage.self.wL2.unlock()

