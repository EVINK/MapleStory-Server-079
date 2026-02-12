"""
AutoRegister - Converted from Java source
Original: handling/login/handler/AutoRegister.java
Package: handling.login.handler
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.LoginCrypto import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes


class AutoRegister:
    """
    Class AutoRegister
    """

    ACCOUNTS_PER_MAC = 100

    # Static initializer
    # AutoRegister.autoRegister = ServerConstants.getAutoReg()
    # AutoRegister.success = False
    # AutoRegister.mac = True


    @staticmethod
    def getAccountExists(login: str) -> bool:
        accountExists = False
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT name FROM accounts WHERE name = ?")
            ps.setString(1, login)
            rs = ps.executeQuery()
            if rs.first():
                accountExists = True
            rs.close()
            ps.close()
        except Exception as ex:
            print("getAccountExists " + ex)
        return accountExists

    def getAccountExistsByID(self, id: int) -> bool:
        accountExists = False
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT name FROM accounts WHERE id = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if rs.first():
                accountExists = True
            rs.close()
            ps.close()
        except Exception as ex:
            print("getAccountExists " + ex)
        return accountExists

    def createAccount(self, login: str, pwd: str, eip: str, macs: str) -> None:
        sockAddr = eip
        con = None
        try:
            con = DatabaseConnection.getConnection()
        except Exception as ex:
            print(ex)
            return
        try:
            ipc = con.prepareStatement("SELECT macs FROM accounts WHERE macs = ?")
            ipc.setString(1, macs)
            rs = ipc.executeQuery()
            if not rs.first() or (rs.last() and rs.getRow() < 100):
                ps = con.prepareStatement("INSERT INTO accounts (name, password, email, birthday, macs, SessionIP) VALUES (?, ?, ?, ?, ?, ?)")
                ps.setString(1, login)
                ps.setString(2, LoginCrypto.hexSha1(pwd))
                ps.setString(3, "autoregister@mail.com")
                ps.setString(4, "2008-04-07")
                ps.setString(5, macs)
                ps.setString(6, "/" + sockAddr[1:sockAddr.rfind(58]))
                ps.executeUpdate()
                AutoRegister.success = True
            AutoRegister.success = True
            if rs.getRow() >= 100:
                AutoRegister.mac = False
        except Exception as ex2:
            ex2.printStackTrace()
            print(ex2)

