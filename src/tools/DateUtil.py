"""
DateUtil - Converted from Java source
Original: tools/DateUtil.java
Package: tools
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from datetime import timezone
from typing import Optional, Any


class DateUtil:
    """
    Class DateUtil
    """

    FT_UT_OFFSET = 116444520000000000
    sdf1 = SimpleDateFormat("yyyy-mm-dd HH:mm:ss")
    sdf2 = SimpleDateFormat("yyyy-mm-dd")


    @staticmethod
    def isDST() -> bool:
        return TimeZone.getDefault().inDaylightTime(Date())

    def getFileTimestamp(self, timeStampinMillis: int) -> int:
        return getFileTimestamp(timeStampinMillis, False)

    def getFileTimestamp_timeStampinMillis_roundToMinutes(self, timeStampinMillis: int, roundToMinutes: bool) -> int:
        if isDST():
            timeStampinMillis -= 3600000
        timeStampinMillis += 50400000
        time = None
        if roundToMinutes:
            time = timeStampinMillis / 1000 / 60 * 600000000
        else:
            time = timeStampinMillis * 10000
        return time + 116444520000000000

    def getCurrentDateStr(self) -> str:
        return sdf1.format(Date())

    def getCurrentDateStr2(self) -> str:
        return sdf2.format(Date())

