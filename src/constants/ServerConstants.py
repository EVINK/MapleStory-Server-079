"""
ServerConstants - Converted from Java source
Original: constants/ServerConstants.java
Package: constants
"""

from enum import Enum, IntEnum
from typing import Optional, Any

# Internal module imports
# from server.ServerProperties import *  # TODO: import specific classes


class ServerConstants:
    """
    Class ServerConstants
    """

    def __init__(self):
        self.commandPrefix = None
        self.level = None
        self.level = None

    # Static initializer
    # ServerConstants.PollEnabled = False
    # ServerConstants.Poll_Question = "Are you mudkiz?"
    # ServerConstants.Poll_Answers = new String[] { "test1", "test2", "test3" }
    # ServerConstants.MAPLE_TYPE = MapleType.中国
    # ServerConstants.MAPLE_VERSION = 79
    # ServerConstants.MAPLE_PATCH = "1"
    # ServerConstants.Use_Fixed_IV = False
    # ServerConstants.MIN_MTS = 110
    # ServerConstants.MTS_BASE = 100
    # ServerConstants.MTS_TAX = 10
    # ServerConstants.MTS_MESO = 5000
    # ServerConstants.CHANNEL_COUNT = 200
    # ServerConstants.封包显示 = bool(ServerProperties.getProperty("RoyMS.封包显示", "False"))
    # ServerConstants.调试输出封包 = bool(ServerProperties.getProperty("RoyMS.调试输出封包", "False"))
    # ServerConstants.自动注册 = bool(ServerProperties.getProperty("RoyMS.AutoRegister", "False"))
    # ServerConstants.PACKET_ERROR_OFF = bool(ServerProperties.getProperty("RoyMS.记录38错误", "False"))
    # ServerConstants.Super_password = False
    # ServerConstants.clientAutoDisconnect = True
    # ServerConstants.superpw = ""
    # ServerConstants.PACKET_ERROR = ""
    # ServerConstants.Channel = 0
    # ServerConstants.removePlayerFromMap = 0
    # ServerConstants.loadop = True


    @staticmethod
    def setPACKET_ERROR(ERROR: str) -> None:
        ServerConstants.PACKET_ERROR = ERROR

    def getPACKET_ERROR(self) -> str:
        return ServerConstants.PACKET_ERROR

    def setChannel(self, ERROR: int) -> None:
        ServerConstants.Channel = ERROR

    def getChannel(self) -> int:
        return ServerConstants.Channel

    def setRemovePlayerFromMap(self, ERROR: int) -> None:
        ServerConstants.removePlayerFromMap = ERROR

    def getRemovePlayerFromMap(self) -> int:
        return ServerConstants.removePlayerFromMap

    def getAutoReg(self) -> bool:
        return ServerConstants.自动注册

    def ChangeAutoReg(self) -> str:
        ServerConstants.自动注册 = not getAutoReg()
        return ServerConstants.自动注册 ? "开启" : "关闭"

    def Class_Bonus_EXP(self, job: int) -> int:
        # switch (job):
            # case 3000:
            # case 3200:
            # case 3210:
            # case 3211:
            # case 3212:
            # case 3300:
            # case 3310:
            # case 3311:
            # case 3312:
            # case 3500:
            # case 3510:
            # case 3511:
            # case 3512:
                return 10
            # default:
                return 0

    def getCommandPrefix(self) -> str:
        return self.commandPrefix

    def getLevel(self) -> int:
        return self.level

    def getType(self) -> int:
        return self.level

    def getAscii(self) -> str:
        return self.ascii

    def getByType(self, type: int) -> Any:
        for l in values():
            if l.getType() == type:
                return l
        return MapleType.中国


# Inner class from Java (originally nested)
class PlayerGMRank(Enum):
    """Enum PlayerGMRank"""

    NORMAL = ('@', 0)
    INTERN = ('!', 1)
    GM = ('!', 2)
    ADMIN = ('!', 3)

    def __init__(self, ch, level):
        self._ch = ch
        self._level = level

    def getCommandPrefix(self) -> str:
        return self.commandPrefix

    def getLevel(self) -> int:
        return self.level


# Inner class from Java (originally nested)
class CommandType(Enum):
    """Enum CommandType"""

    NORMAL = (0)
    TRADE = (1)

    def __init__(self, level):
        self._level = level

    def getType(self) -> int:
        return self.level


# Inner class from Java (originally nested)
class MapleType(Enum):
    """Enum MapleType"""

    中国 = (4, "GB18030")

    def __init__(self, type, ascii):
        self._type = type
        self._ascii = ascii

    def getAscii(self) -> str:
        return self.ascii

    def getType(self) -> int:
        return self.type

    def getByType(self, type: int) -> Any:
        for l in values():
            if l.getType() == type:
                return l
        return MapleType.中国

