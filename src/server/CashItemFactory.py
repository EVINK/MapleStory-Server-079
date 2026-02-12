"""
CashItemFactory - Converted from Java source
Original: server/CashItemFactory.java
Package: server
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes


class CashItemFactory:
    """
    Class CashItemFactory
    """

    def __init__(self):
        self.initialized = False
        self.itemStats = None
        self.itemPackage = None
        self.data = None
        self.itemStringInfo = None
        self.idLookup = None
        self.initialized = False
        self.itemStats = {}
        self.itemPackage = new HashMap<Integer, List<CashItemInfo>>()
        self.itemMods = {}
        self.data = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
        self.itemStringInfo = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz"))
        self.idLookup = {}

    # Static initializer
    # instance = CashItemFactory()
    # bestItems = new int[] { 10099994, 20490094, 10099993, 60090092, 50290004 }


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        print("商城 :::")
        itemids = []
        for field in self.data.getData("Commodity.img").getChildren():
            SN = MapleDataTool.getIntConvert("SN", field, 0)
            itemId = MapleDataTool.getIntConvert("ItemId", field, 0)
            stats = CashItemInfo(MapleDataTool.getIntConvert("ItemId", field, 0), MapleDataTool.getIntConvert("Count", field, 1), MapleDataTool.getIntConvert("Price", field, 0), SN, MapleDataTool.getIntConvert("Period", field, 0), MapleDataTool.getIntConvert("Gender", field, 2), MapleDataTool.getIntConvert("OnSale", field, 0) > 0 && MapleDataTool.getIntConvert("Price", field, 0) > 0)
            if SN > 0:
                self.itemStats.put(SN, stats)
                self.idLookup.put(itemId, SN)
            if itemId > 0:
                itemids.add(itemId)
        for i in itemids:
            self.getPackageItems(i)
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT * FROM cashshop_modified_items"
            try:
            rs = ps.executeQuery())
                while rs.next():
                    final CashItemInfo.CashModInfo ret = new CashItemInfo.CashModInfo(rs.getInt("serial"), rs.getInt("discount_price"), rs.getInt("mark"), rs.getInt("showup") > 0, rs.getInt("itemid"), rs.getInt("priority"), rs.getInt("package") > 0, rs.getInt("period"), rs.getInt("gender"), rs.getInt("count"), rs.getInt("meso"), rs.getInt("unk_1"), rs.getInt("unk_2"), rs.getInt("unk_3"), rs.getInt("extra_flags"))
                    if ret.showUp:
                        self.itemMods.put(ret.sn, ret)
                        cc = self.itemStats.get(ret.sn)
                        if cc is None:
                            continue
                        ret.toCItem(cc)
        except Exception as e:
            e.printStackTrace()
        for i in self.itemStats.keys():
            self.getItem(i)
        self.initialized = True

    def getItem(self, sn: int) -> Any:
        stats = self.itemStats.get(sn)
        final CashItemInfo.CashModInfo z = self.getModInfo(sn)
        if z is not None && z.showUp:
            return z.toCItem(stats)
        if stats is None || !stats.onSale():
            return None
        return stats

    def getPackageItems(self, itemId: int) -> list:
        if self.itemPackage.get(itemId) is not None:
            return self.itemPackage.get(itemId)
        packageItems = []
        b = self.data.getData("CashPackage.img")
        if b is None || b.getChildByPath(itemId + "/SN") is None:
            return None
        for d in b.getChildByPath(itemId + "/SN").getChildren():
            packageItems.add(self.itemStats.get(MapleDataTool.getIntConvert(d)))
        self.itemPackage.put(itemId, packageItems)
        return packageItems

    def getModInfo(self, sn: int) -> Any:
        return self.itemMods.get(sn)

    def getAllModInfo(self) -> list:
        if !self.initialized:
            self.initialize()
        return self.itemMods.values()

    def getBestItems(self) -> list:
        return CashItemFactory.bestItems

    def getSnFromId(self, itemId: int) -> int:
        return self.idLookup.get(itemId)

    def clearCashShop(self) -> None:
        self.itemStats.clear()
        self.itemPackage.clear()
        self.itemMods.clear()
        self.idLookup.clear()
        self.initialized = False
        self.initialize()

    def getItemSN(self, itemid: int) -> int:
        for (final Map.Entry<Integer, CashItemInfo> ci : self.itemStats.items())
            if ci.getValue().getId() == itemid:
                return ci.getValue().getSN()
        return 0

