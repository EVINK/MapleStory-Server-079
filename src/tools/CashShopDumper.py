"""
CashShopDumper - Converted from Java source
Original: tools/CashShopDumper.java
Package: tools
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys

# Internal module imports
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.CashItemFactory import *  # TODO: import specific classes
# from server.CashItemInfo import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes


class CashShopDumper:
    """
    Class CashShopDumper
    """

    # Static initializer
    # data = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))


    @staticmethod
    def getModInfo(sn: int) -> Any:
        CashItemInfo.CashModInfo ret = None
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT * FROM cashshop_modified_items WHERE serial = ?")
        try:
            ps.setInt(1, sn)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    ret = new CashItemInfo.CashModInfo(sn, rs.getInt("discount_price"), rs.getInt("mark"), rs.getInt("showup") > 0, rs.getInt("itemid"), rs.getInt("priority"), rs.getInt("package") > 0, rs.getInt("period"), rs.getInt("gender"), rs.getInt("count"), rs.getInt("meso"), rs.getInt("unk_1"), rs.getInt("unk_2"), rs.getInt("unk_3"), rs.getInt("extra_flags"))
        except Exception as ex:
            FilePrinter.printError("CashShopDumper.txt", ex)
        return ret

    def main(self, args: list) -> None:
        final CashItemInfo.CashModInfo m = getModInfo(20000393)
        CashItemFactory.getInstance().initialize()
        final Collection<CashItemInfo.CashModInfo> list = CashItemFactory.getInstance().getAllModInfo()
        con = DatabaseConnection.getConnection()
        itemids = []
        qq = []
        dics = new HashMap<Integer, List<String>>()
        for field in CashShopDumper.data.getData("Commodity.img").getChildren():
            try:
                itemId = MapleDataTool.getIntConvert("ItemId", field, 0)
                sn = MapleDataTool.getIntConvert("SN", field, 0)
                count = MapleDataTool.getIntConvert("Count", field, 0)
                price = MapleDataTool.getIntConvert("Price", field, 0)
                priority = MapleDataTool.getIntConvert("Priority", field, 0)
                period = MapleDataTool.getIntConvert("Period", field, 0)
                gender = MapleDataTool.getIntConvert("Gender", field, -1)
                meso = MapleDataTool.getIntConvert("Meso", field, 0)
                if itemId == 0:
                    continue
                cat = itemId / 10000
                if dics.get(cat) is None:
                    dics.put(cat, [])
                check = False
                if meso > 0:
                    check = True
                if MapleItemInformationProvider.getInstance().getInventoryType(itemId) == MapleInventoryType.EQUIP and not MapleItemInformationProvider.getInstance().isCashItem(itemId):
                    check = True
                if MapleItemInformationProvider.getInstance().getInventoryType(itemId) == MapleInventoryType.EQUIP and period > 0:
                    check = True
                if check:
                    print(MapleItemInformationProvider.getInstance().getName(itemId))
                else:
                    ps = con.prepareStatement("INSERT INTO cashshop_modified_items (serial, showup,itemid,priority,period,gender,count,meso,discount_price,mark, unk_1, unk_2, unk_3) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                    ps.setInt(1, sn)
                    ps.setInt(2, 1)
                    ps.setInt(3, itemId)
                    ps.setInt(4, 0)
                    ps.setInt(5, period)
                    ps.setInt(6, gender)
                    ps.setInt(7, (count > 1) ? count : 0)
                    ps.setInt(8, meso)
                    ps.setInt(9, 0)
                    ps.setInt(10, 0)
                    ps.setInt(11, 0)
                    ps.setInt(12, 0)
                    ps.setInt(13, 0)
                    ps.executeUpdate()
                    ps.close()
            except Exception as ex:
                FilePrinter.printError("CashShopDumper.txt", ex)
        for key in dics.keys():
            fout = File("cashshopItems/" + key + ".sql")
            l = dics.get(key)
            fos = None
            try:
                if not fout.exists():
                    fout.createNewFile()
                fos = FileOutputStream(fout)
                bw = BufferedWriter(OutputStreamWriter(fos))
                for i in range(l):
                    bw.write(l.get(i))
                    bw.newLine()
                bw.close()
            except FileNotFoundException as ex2:
                FilePrinter.printError("CashShopDumper.txt", ex2)
            except IOError as ex3:
                FilePrinter.printError("CashShopDumper.txt", ex3)
            finally:
                try:
                    if fos is not None:
                        fos.close()
                except IOError as ex4:
                    FilePrinter.printError("CashShopDumper.txt", ex4)

