"""
EventScriptManager - Converted from Java source
Original: scripting/EventScriptManager.java
Package: scripting
"""

from pathlib import Path
from threading import Lock
from typing import Dict
from typing import Optional, Any
import tkinter

# Internal module imports
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes


class EventScriptManager(AbstractScriptManager):
    """
    Class EventScriptManager
    Extends: AbstractScriptManager
    """

    def __init__(self, cserv: Any, scripts: list):
        self.events = None
        self.runningInstanceMapId = None
        self.script = ""
        self.iv = None
        self.em = None
        self.events = {}
        self.runningInstanceMapId = AtomicInteger(0)
        for script in scripts:
            if not script == (""):
                iv = self.getInvocable("event"+ File.separator + script + ".js", None)
                if iv is not None:
                    self.events.put(script, EventEntry(script, iv, EventManager(cserv, iv, script)))


    def getNewInstanceMapId(self) -> int:
        return self.runningInstanceMapId.addAndGet(1)

    def getEventManager(self, event: str) -> Any:
        entry = self.events.get(event)
        if entry is None:
            return None
        return entry.em

    def init(self) -> None:
        for entry in self.events.values():
            try:
                (entry.iv).put("em", entry.em)
                entry.iv.invokeFunction("init", None)
            except Exception as ex:
                print("Error initiating event: " + entry.script + ":" + ex)
                FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error initiating event: " + entry.script + ":" + ex)

    def cancel(self) -> None:
        for entry in self.events.values():
            entry.em.cancel()


# Inner class from Java (originally nested)
class EventEntry:
    """
    Class EventEntry
    """

    def __init__(self, script: str, iv: Any, em: Any):
        self.script = ""
        self.iv = None
        self.em = None
        self.script = script
        self.iv = iv
        self.em = em


