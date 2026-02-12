"""
CherryMScustomEventFactory - Converted from Java source
Original: KinMS/db/CherryMScustomEventFactory.java
Package: KinMS.db
"""

from typing import Optional, Any

# Internal module imports
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes


class CherryMScustomEventFactory:
    """
    Class CherryMScustomEventFactory
    """

    # Static initializer
    # CherryMScustomEventFactory.instance = None


    @staticmethod
    def isCANLOG() -> bool:
        return CherryMScustomEventFactory.CANLOG

    def setCANLOG(self, CANLOG: bool) -> None:
        CANLOG = CANLOG

    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getCherryMSLottery(self) -> Any:
        return CherryMSLotteryImpl.getInstance()

    def getCherryMSLottery_cserv_mapFactory(self, cserv: Any, mapFactory: Any) -> Any:
        return CherryMSLotteryImpl.getInstance(cserv, mapFactory)

