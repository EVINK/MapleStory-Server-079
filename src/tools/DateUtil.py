"""
DateUtil - 从Java源文件转换而来
对应Java源文件: tools/DateUtil.java
包路径: tools
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from datetime import timezone


class DateUtil:
    """
    类 DateUtil - 从Java类转换
    """

    # 静态字段 (Static fields)
    FT_UT_OFFSET = 116444520000000000
    sdf1 = SimpleDateFormat("yyyy-mm-dd HH:mm:ss")
    sdf2 = SimpleDateFormat("yyyy-mm-dd")


    def isDST(self) -> bool:
        """方法 isDST"""
        return False

    def getFileTimestamp(self, timeStampinMillis: int) -> int:
        """方法 getFileTimestamp"""
        return 0

    def getFileTimestamp(self, timeStampinMillis: int, roundToMinutes: bool) -> int:
        """方法 getFileTimestamp"""
        return 0

    def getCurrentDateStr(self) -> str:
        """方法 getCurrentDateStr"""
        return ""

    def getCurrentDateStr2(self) -> str:
        """方法 getCurrentDateStr2"""
        return ""

