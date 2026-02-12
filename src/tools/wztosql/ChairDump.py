"""
ChairDump - Converted from Java source
Original: tools/wztosql/ChairDump.java
Package: tools.wztosql
"""

from typing import Optional, Any
import os

# Internal module imports
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class ChairDump:
    """
    Class ChairDump
    """


    def main(self, args: list) -> None:
        out = FileOutputStream("ChairDump.txt", False)
        sb = ""
        shopId = 145274
        npcId = 9010000
        sb.append("INSERT INTO shops (`shopid`, `npcid`) VALUES(").append(shopId).append(", ").append(npcId).append(");\r\n")
        price = 1
        for item in MapleItemInformationProvider.getInstance().getAllItems2():
            if item.getLeft() >= 3010000 && item.getLeft() < 3020000:
                sb.append("INSERT INTO shopitems (`shopid`, `itemid`, `price`, `position`) VALUES(").append(shopId).append(", ").append(item.getLeft()).append(", ").append(price).append(", 0);\r\n")
        out.write(sb.encode("utf-8"))

