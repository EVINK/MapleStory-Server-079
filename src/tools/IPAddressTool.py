"""
IPAddressTool - Converted from Java source
Original: tools/IPAddressTool.java
Package: tools
"""

from typing import Optional, Any
import math


class IPAddressTool:
    """
    Class IPAddressTool
    """


    def dottedQuadToLong(self, dottedQuad: str) -> int:
        quads = dottedQuad.split("/.")
        if len(quads) != 4:
            raise RuntimeError("Invalid IP Address format.")
        ipAddress = 0
        for i in range(4):
            ipAddress += int(quads[i]) % 256 * math.pow(256.0, 4 - i)
        return ipAddress

    def longToDottedQuad(self, longIP: int) -> str:
        ipAddress = ""
        for i in range(4):
            quad = (int)(longIP / math.pow(256.0, 4 - i))
            longIP -= quad * math.pow(256.0, 4 - i)
            if i > 0:
                ipAddress.append(".")
            if quad > 255:
                raise RuntimeError("Invalid long IP address.")
            ipAddress.append(quad)
        return ipAddress

