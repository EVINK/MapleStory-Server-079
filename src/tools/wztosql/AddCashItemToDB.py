"""
AddCashItemToDB - Converted from Java source
Original: tools/wztosql/AddCashItemToDB.java
Package: tools.wztosql
"""

from pymysql import Connection
from pymysql import Error
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class AddCashItemToDB:
    """
    Class AddCashItemToDB
    """


    def addItem(self, id: int, Count: int, Price: int, SN: int, Expire: int, Gender: int, OnSale: int) -> None:
        try:
            conn = DatabaseConnection.getConnection()
            ps = conn.prepareStatement("INSERT INTO `cashshop_items` VALUES (DEFAULT, ?, ?, ?, ?, ?, ?, ?)")
            ps.setInt(1, id)
            ps.setInt(2, Count)
            ps.setInt(3, Price)
            ps.setInt(4, SN)
            ps.setInt(5, Expire)
            ps.setInt(6, Gender)
            ps.setInt(7, OnSale)
            ps.executeUpdate()
            ps.close()
        except Exception as sqle:
            sqle.printStackTrace()

