"""
FixShopItemsPrice - Converted from Java source
Original: tools/FixShopItemsPrice.java
Package: tools
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Iterator
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes


class FixShopItemsPrice:
    """
    Class FixShopItemsPrice
    """

    def __init__(self):
        self.con = None
        self.con = DatabaseConnection.getConnection()


    def main(self, args: list) -> None:
        os.environ["wzPath"] = os.environ.get("wzPath")
        i = FixShopItemsPrice()
        print("正在加载道具数据......")
        MapleItemInformationProvider.getInstance().load()
        print("正在读取商店内商品......")
        list = i.loadFromDB()
        print("正在处理商店内商品价格......")
        for ii in list:
            i.changePrice(ii)
        print("处理商品价格结束。")

    def loadFromDB(self) -> list:
        shopItemsId = []
        try:
            ps = self.con.prepareStatement("SELECT itemid FROM shopitems ORDER BY itemid")
            rs = ps.executeQuery()
            itemId = 0
            while rs.next():
                if itemId != rs.getInt("itemid"):
                    itemId = rs.getInt("itemid")
                    shopItemsId.add(itemId)
            rs.close()
            ps.close()
        except Exception as e:
            print("无法载入商店")
        return shopItemsId

    def changePrice(self, itemId: int) -> None:
        ii = MapleItemInformationProvider.getInstance()
        try:
            ps = self.con.prepareStatement("SELECT shopid, price FROM shopitems WHERE itemid = ? ORDER BY price")
            ps.setInt(1, itemId)
            rs = ps.executeQuery()
            while rs.next():
                if ii.getPrice(itemId) > rs.getLong("price"):
                    print("道具: " + MapleItemInformationProvider.getInstance().getName(itemId) + "道具ID: " + itemId + " 商店: " + rs.getInt("shopid") + " 价格: " + rs.getLong("price") + " 新价格:" + ii.getPrice(itemId))
                    pp = self.con.prepareStatement("UPDATE shopitems SET price = ? WHERE itemid = ? AND shopid = ?")
                    pp.setLong(1, ii.getPrice(itemId))
                    pp.setInt(2, itemId)
                    pp.setInt(3, rs.getInt("shopid"))
                    pp.execute()
                    pp.close()
            rs.close()
            ps.close()
        except Exception as e:
            print("處理商品失敗, 道具ID:" + itemId)

