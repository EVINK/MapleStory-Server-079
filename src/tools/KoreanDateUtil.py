"""
KoreanDateUtil - Converted from Java source
Original: tools/KoreanDateUtil.java
Package: tools
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from datetime import timezone
from typing import Optional, Any


class KoreanDateUtil:
    """
    Class KoreanDateUtil
    """

    ITEM_YEAR2000 = -1085019342
    REAL_YEAR2000 = 946681229830
    QUEST_UNIXAGE = 27111908
    FT_UT_OFFSET = 116444736000000000

    # Static initializer
    # KoreanDateUtil.MAX_TIME = 150842304000000000
    # KoreanDateUtil.ZERO_TIME = 94354848000000000
    # KoreanDateUtil.PERMANENT = 150841440000000000


    @staticmethod
    def getKoreanTimestamp(realTimestamp: int) -> int:
        return getTime(realTimestamp)

    def getTime(self, realTimestamp: int) -> int:
        if realTimestamp == -1:
            return KoreanDateUtil.MAX_TIME
        if realTimestamp == -2:
            return KoreanDateUtil.ZERO_TIME
        if realTimestamp == -3:
            return KoreanDateUtil.PERMANENT
        return realTimestamp * 10000 + 116444736000000000

    def getTempBanTimestamp(self, realTimestamp: int) -> int:
        return realTimestamp * 10000 + 116444736000000000

    def getItemTimestamp(self, realTimestamp: int) -> int:
        time = (int)((realTimestamp - 946681229830) / 1000 / 60)
        return (int)(time * 35.762787) - 1085019342

    def getQuestTimestamp(self, realTimestamp: int) -> int:
        time = (int)(realTimestamp / 1000 / 60)
        return (int)(time * 0.1396987) + 27111908

    def isDST(self) -> bool:
        return TimeZone.getDefault().inDaylightTime(Date())

    def getFileTimestamp(self, timeStampinMillis: int, roundToMinutes: bool) -> int:
        if isDST():
            timeStampinMillis -= 3600000
        time = None
        if roundToMinutes:
            time = timeStampinMillis / 1000 / 60 * 600000000
        else:
            time = timeStampinMillis * 10000
        return time + 116444736000000000

