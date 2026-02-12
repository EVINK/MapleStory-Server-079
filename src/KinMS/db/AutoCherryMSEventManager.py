"""
AutoCherryMSEventManager - Converted from Java source
Original: KinMS/db/AutoCherryMSEventManager.java
Package: KinMS.db
"""

from typing import Optional, Any
import threading

# Internal module imports
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes


class AutoCherryMSEventManager(Runnable):
    """
    Class AutoCherryMSEventManager
    Implements: Runnable
    """

    def __init__(self):
        self.cserv = None
        self.mapFactory = None

    # Static initializer
    # AutoCherryMSEventManager.instance = None


    def newInstance(self) -> Any:
        return AutoCherryMSEventManager()

    def newInstance_cserv_mapFactory(self, cserv: Any, mapFactory: Any) -> Any:
        return AutoCherryMSEventManager.instance = AutoCherryMSEventManager(cserv, mapFactory)

    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getInstance_cserv_mapFactory(self, cserv: Any, mapFactory: Any) -> Any:
        if AutoCherryMSEventManager.instance is None:
            AutoCherryMSEventManager.instance = AutoCherryMSEventManager(cserv, mapFactory)
        return AutoCherryMSEventManager.instance

    def getChannelServer(self) -> Any:
        return self.cserv

    def getMapleMapFactory(self) -> Any:
        return self.mapFactory

    def run(self) -> None:
        CherryMScustomEventFactory.getInstance().getCherryMSLottery(self.cserv, self.mapFactory).doLottery()

