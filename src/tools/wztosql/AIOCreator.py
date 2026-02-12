"""
AIOCreator - Converted from Java source
Original: tools/wztosql/AIOCreator.java
Package: tools.wztosql
"""

from typing import Iterator
from typing import List
from typing import Optional, Any
import os

# Internal module imports
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class AIOCreator:
    """
    Class AIOCreator
    """

    # Static initializer
    # Lists.ALL = []


    def main(self, args: list) -> None:
        provider = MapleItemInformationProvider.getInstance()
        for iteminfo in provider.getAllItems2():
            id = iteminfo.getLeft()
            if (id / 10000 >= 100 and id / 10000 <= 153) or id / 10000 == 190 or id / 10000 == 191:
                Lists.ALL.add(id)
        createSQLQuery()

    def createSQLQuery(self) -> None:
        out = FileOutputStream("AIO.txt", False)
        sb = ""
        for id in range(100, = 153):
            addLine(sb, "INSERT INTO `shops` (`shopid`, `npcid`) VALUES ('" + id * 1000 + "', '9900002');")
        addLine(sb, "INSERT INTO `shops` (`shopid`, `npcid`) VALUES ('190000', '9900002');")
        addLine(sb, "INSERT INTO `shops` (`shopid`, `npcid`) VALUES ('191000', '9900002');")
        if not Lists.ALL == 0:
            for id2 in Lists.ALL:
                addLine(sb, "INSERT INTO `shopitems` (`shopid`, `itemid`, `price`, `position`, `reqitem`, `reqitemq`, `rank`, `buyable`, `category`, `minLevel`, `expiration`) VALUES ('" + id2 / 10000 * 1000 + "', '" + id2 + "', '" + getPrice(id2) + "', '0', '0', '0', '0', '0', '0', '0', '0');")
        print("Success")
        out.write(sb.encode("utf-8"))

    def addLine(self, sb: Any, string: str) -> None:
        sb.append(string).append("\r\n")

    def getPrice(self, id: int) -> int:
        return 1


# Inner class from Java (originally nested)
class ItemType:
    """
    Class ItemType
    """

    pass


# Inner class from Java (originally nested)
class WeaponType:
    """
    Class WeaponType
    """

    pass


# Inner class from Java (originally nested)
class Lists:
    """
    Class Lists
    """

    # Static initializer
    # Lists.ALL = []

    pass

