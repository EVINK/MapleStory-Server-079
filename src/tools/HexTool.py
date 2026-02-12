"""
HexTool - Converted from Java source
Original: tools/HexTool.java
Package: tools
"""

from io import BytesIO
from typing import Optional, Any
import asyncio
import struct


class HexTool:
    """
    Class HexTool
    """

    # Static initializer
    # HEX = new char[] { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' }


    @staticmethod
    def toString(byteValue: int) -> str:
        tmp = byteValue << 8
        retstr = { HexTool.HEX[tmp >> 12 & 0xF], HexTool.HEX[tmp >> 8 & 0xF] }
        return str(retstr)

    def toString(self, buf: Any) -> str:
        buf.flip()
        arr = new byte[buf.remaining()]
        buf.get(arr)
        ret = toString(arr)
        buf.flip()
        buf.put(arr)
        return ret

    def toString_intValue(self, intValue: int) -> str:
        return Integer.toHexString(intValue)

    def toString_bytes(self, bytes: bytes) -> str:
        hexed = ""
        for i in range(len(bytes)):
            hexed.append(toString(bytes[i]))
            hexed.append(' ')
        return hexed[0:hexed.__len__(] - 1)

    def toStringFromAscii(self, bytes: bytes) -> str:
        ret = new byte[len(bytes)]
        for x in range(len(bytes)):
            if bytes[x] < 32 and bytes[x] >= 0:
                ret[x] = 46
            else:
                chr = bytes[x] & 0xFF
                ret[x] = chr
        encode = "gbk"
        try:
            str = String(ret, encode)
            return str
        except UnsupportedEncodingException as ex:
            return ""

    def toPaddedStringFromAscii(self, bytes: bytes) -> str:
        str = toStringFromAscii(bytes)
        ret = "" * 3)
        for i in range(str):
            ret.append(str[i])
            ret.append(" ")
        return ret

    def getByteArrayFromHexString(self, hex: str) -> bytes:
        baos = ByteArrayOutputStream()
        nexti = 0
        nextb = 0
        highoc = True
        Block_2:
        while True:
            number = -1
            while number == -1:
                if nexti == hex:
                    Block_2 = None
                chr = hex[nexti]
                if chr >= '0' and chr <= '9':
                    number = chr - '0'
                elif chr >= 'a' and chr <= 'f':
                    number = chr - 'a' + 10
                elif chr >= 'A' and chr <= 'F':
                    number = chr - 'A' + 10
                else:
                    number = -1
                nexti += 1
            if highoc:
                nextb = number << 4
                highoc = False
            else:
                nextb |= number
                highoc = True
                baos.write(nextb)
        return baos.toByteArray()

    def getOpcodeToString(self, op: int) -> str:
        return "0x" + StringUtil.getLeftPaddedStr(Integer.toHexString(op).upper(), '0', 4)

