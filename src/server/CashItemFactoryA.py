"""
CashItemFactoryA - Converted from Java source
Original: server/CashItemFactoryA.java
Package: server
"""

from typing import List
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes


class CashItemFactoryA:
    """
    Class CashItemFactoryA
    """

    # Static initializer
    # snLookup = {}
    # idLookup = {}
    # itemStats = {}
    # data = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
    # commodities = CashItemFactoryA.data.getData(StringUtil.getLeftPaddedStr("Commodity.img", '0', 11))
    # cashPackages = new HashMap<Integer, List<CashItemInfoA>>()


    @staticmethod
    def getItem(sn: int) -> Any:
        stats = CashItemFactoryA.itemStats.get(sn)
        if stats is None:
            cid = getCommodityFromSN(sn)
            itemId = MapleDataTool.getIntConvert(cid + "/ItemId", CashItemFactoryA.commodities)
            count = MapleDataTool.getIntConvert(cid + "/Count", CashItemFactoryA.commodities, 1)
            price = MapleDataTool.getIntConvert(cid + "/Price", CashItemFactoryA.commodities, 0)
            period = MapleDataTool.getIntConvert(cid + "/Period", CashItemFactoryA.commodities, 0)
            gender = MapleDataTool.getIntConvert(cid + "/Gender", CashItemFactoryA.commodities, 2)
            onSale = MapleDataTool.getIntConvert(cid + "/OnSale", CashItemFactoryA.commodities, 0) == 1
            stats = CashItemInfoA(sn, itemId, count, price, period, gender, onSale)
            CashItemFactoryA.itemStats.put(sn, stats)
        return stats

    def getCommodityFromSN(self, sn: int) -> int:
        cid = None
        if CashItemFactoryA.snLookup.get(sn) is None:
            curr = CashItemFactoryA.snLookup - 1
            currSN = 0
            if curr == -1:
                curr = 0
                currSN = MapleDataTool.getIntConvert("0/SN", CashItemFactoryA.commodities)
                CashItemFactoryA.snLookup.put(currSN, curr)
            i = CashItemFactoryA.snLookup - 1
            while currSN != sn:
                curr = i
                currSN = MapleDataTool.getIntConvert(curr + "/SN", CashItemFactoryA.commodities)
                CashItemFactoryA.snLookup.put(currSN, curr)
                i += 1
            cid = curr
        else:
            cid = CashItemFactoryA.snLookup.get(sn)
        return cid

    def getPackageItems(self, itemId: int) -> list:
        if (itemId in CashItemFactoryA.cashPackages):
            return CashItemFactoryA.cashPackages.get(itemId)
        packageItems = []
        dataProvider = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
        a = dataProvider.getData("CashPackage.img")
        for b in a.getChildren():
            if itemId == int(b.getName()):
                for c in b.getChildren():
                    for d in c.getChildren():
                        SN = MapleDataTool.getIntConvert("" + int(d.getName()), c)
                        packageItems.add(getItem(SN))
                break
        CashItemFactoryA.cashPackages.put(itemId, packageItems)
        return packageItems

    def getSnFromId(self, id: int) -> int:
        cid = None
        if CashItemFactoryA.idLookup.get(id) is None:
            curr = CashItemFactoryA.idLookup - 1
            currSN = 0
            if curr == -1:
                curr = 0
                currSN = MapleDataTool.getIntConvert("0/ItemId", CashItemFactoryA.commodities)
                CashItemFactoryA.idLookup.put(currSN, curr)
            i = CashItemFactoryA.idLookup - 1
            while currSN != id:
                curr = i
                currSN = MapleDataTool.getIntConvert(curr + "/ItemId", CashItemFactoryA.commodities)
                CashItemFactoryA.idLookup.put(currSN, curr)
                i += 1
            cid = curr
        else:
            cid = CashItemFactoryA.idLookup.get(id)
        return MapleDataTool.getIntConvert(cid + "/SN", CashItemFactoryA.commodities)

