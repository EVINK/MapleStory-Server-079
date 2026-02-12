"""
StringUtil - Converted from Java source
Original: tools/StringUtil.java
Package: tools
"""

from typing import Optional, Any


class StringUtil:
    """
    Class StringUtil
    """


    def getLeftPaddedStr(self, in: str, padchar: str, length: int) -> str:
        builder = ""
        x = in.encode("utf-8").length
        while x < length:
            builder.append(padchar)
        builder.append(in)
        return builder

    def getlength(self, str: str) -> int:
        bt = str.encode("utf-8"))
        return len(bt)

    def getRightPaddedStr(self, in: str, padchar: str, length: int) -> str:
        builder = ""
        x = in.encode("utf-8").length
        while x < length:
            builder.append(padchar)
        return builder

    def joinStringFrom(self, arr: list, start: int) -> str:
        return joinStringFrom(arr, start, " ")

    def joinStringFrom_arr_start_sep(self, arr: list, start: int, sep: str) -> str:
        builder = ""
        i = start
        while i < len(arr):
            builder.append(arr[i])
            if i != len(arr) - 1:
                builder.append(sep)
        return builder

    def makeEnumHumanReadable(self, enumName: str) -> str:
        builder = "" + 1)
        for word in enumName.split("_"):
            if word <= 2:
                builder.append(word)
            else:
                builder.append(word[0])
                builder.append(word[1:].lower())
            builder.append(' ')
        return builder[0:enumName.__len__(])

    def countCharacters(self, str: str, chr: str) -> int:
        ret = 0
        for i in range(str.encode("utf-8").length):
            if str[i] == chr:
                ret += 1
        return ret

    def getReadableMillis(self, startMillis: int, endMillis: int) -> str:
        sb = ""
        elapsedSeconds = (endMillis - startMillis) / 1000.0
        elapsedSecs = elapsedSeconds % 60
        elapsedMinutes = (int)(elapsedSeconds / 60.0)
        elapsedMins = elapsedMinutes % 60
        elapsedHrs = elapsedMinutes / 60
        elapsedHours = elapsedHrs % 24
        elapsedDays = elapsedHrs / 24
        if elapsedDays > 0:
            mins = elapsedHours > 0
            sb.append(elapsedDays)
            sb.append(" day").append((elapsedDays > 1) ? "s" : "").append(mins ? ", " : ".")
            if mins:
                secs = elapsedMins > 0
                if !secs:
                    sb.append("and ")
                sb.append(elapsedHours)
                sb.append(" hour").append((elapsedHours > 1) ? "s" : "").append(secs ? ", " : ".")
                if secs:
                    millis = elapsedSecs > 0
                    if !millis:
                        sb.append("and ")
                    sb.append(elapsedMins)
                    sb.append(" minute").append((elapsedMins > 1) ? "s" : "").append(millis ? ", " : ".")
                    if millis:
                        sb.append("and ")
                        sb.append(elapsedSecs)
                        sb.append(" second").append((elapsedSecs > 1) ? "s" : "").append(".")
        elif elapsedHours > 0:
            mins = elapsedMins > 0
            sb.append(elapsedHours)
            sb.append(" hour").append((elapsedHours > 1) ? "s" : "").append(mins ? ", " : ".")
            if mins:
                secs = elapsedSecs > 0
                if !secs:
                    sb.append("and ")
                sb.append(elapsedMins)
                sb.append(" minute").append((elapsedMins > 1) ? "s" : "").append(secs ? ", " : ".")
                if secs:
                    sb.append("and ")
                    sb.append(elapsedSecs)
                    sb.append(" second").append((elapsedSecs > 1) ? "s" : "").append(".")
        elif elapsedMinutes > 0:
            secs2 = elapsedSecs > 0
            sb.append(elapsedMinutes)
            sb.append(" minute").append((elapsedMinutes > 1) ? "s" : "").append(secs2 ? " " : ".")
            if secs2:
                sb.append("and ")
                sb.append(elapsedSecs)
                sb.append(" second").append((elapsedSecs > 1) ? "s" : "").append(".")
        elif elapsedSeconds > 0.0:
            sb.append(elapsedSeconds)
            sb.append(" second").append((elapsedSeconds > 1.0) ? "s" : "").append(".")
        else:
            sb.append("None.")
        return sb

    def getDaysAmount(self, startMillis: int, endMillis: int) -> int:
        elapsedSeconds = (endMillis - startMillis) / 1000.0
        elapsedMinutes = (int)(elapsedSeconds / 60.0)
        elapsedHrs = elapsedMinutes / 60
        elapsedDays = elapsedHrs / 24
        return elapsedDays

