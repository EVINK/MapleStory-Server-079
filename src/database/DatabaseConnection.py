"""
DatabaseConnection - Converted from Java source
Original: database/DatabaseConnection.java
Package: database
"""

from configparser import ConfigParser
from io import open
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import RLock
from typing import Dict
from typing import List
from typing import Optional, Any
import json
import math
import os
import pymysql
import sys
import threading
import time


class DatabaseConnection:
    """
    Class DatabaseConnection
    """

    def __init__(self):
        self.tid = None
        self.lastAccessTime = 0
        self.connection = None
        self.id = 0

    # Static initializer
    # connections = {}
    # lock = ReentrantLock()
    # DatabaseConnection.propsInited = False
    # dbProps = Properties()
    # DatabaseConnection.connectionTimeOut = 300000
    # DatabaseConnection.CLOSE_CURRENT_RESULT = 1
    # DatabaseConnection.KEEP_CURRENT_RESULT = 2
    # DatabaseConnection.CLOSE_ALL_RESULTS = 3
    # DatabaseConnection.SUCCESS_NO_INFO = -2
    # DatabaseConnection.EXECUTE_FAILED = -3
    # DatabaseConnection.RETURN_GENERATED_KEYS = 1
    # DatabaseConnection.NO_GENERATED_KEYS = 2


    @staticmethod
    def getConnection() -> Any:
        cThread = Thread.currentThread()
        threadID = cThread.getId()
        ret = DatabaseConnection.connections.get(threadID)
        if ret is None:
            retCon = connectToDB()
            ret = ConWrapper(threadID, retCon)
            ret.id = threadID
            DatabaseConnection.connections.put(threadID, ret)
        return ret.getConnection()

    def getWaitTimeout(self, con: Any) -> int:
        stmt = None
        rs = None
        try:
            stmt = con.createStatement()
            rs = stmt.executeQuery("SHOW VARIABLES LIKE 'wait_timeout'")
            if rs.next():
                return max(1000, rs.getInt(2) * 1000 - 1000)
            return -1
        except Exception as ex:
            n = -1
            if stmt is not None:
                try:
                    stmt.close()
                catch (SQLException ex2) {}
                finally:
                    if rs is not None:
                        try:
                            rs.close()
                        catch (SQLException ex3) {}
            return n
        finally:
            if stmt is not None:
                try:
                    stmt.close()
                except Exception as ex4:
                    if rs is not None:
                        try:
                            rs.close()
                        catch (SQLException ex5) {}
                finally:
                    if rs is not None:
                        try:
                            rs.close()
                        catch (SQLException ex6) {}

    def connectToDB(self) -> Any:
        if !DatabaseConnection.propsInited:
            try:
                path = os.environ.get("server_property_db_path")
                # System.out.println("load db pro"+path);
                fR = FileReader(path)
                DatabaseConnection.dbProps.load(fR)
                fR.close()
            except IOError as ex:
                raise DatabaseException(ex)
            DatabaseConnection.dbDriver = DatabaseConnection.dbProps.getProperty("driverClassName")
            DatabaseConnection.dbUrl = DatabaseConnection.dbProps.getProperty("url")
            DatabaseConnection.dbUser = DatabaseConnection.dbProps.getProperty("username")
            DatabaseConnection.dbPass = DatabaseConnection.dbProps.getProperty("password")
            try:
                DatabaseConnection.connectionTimeOut = int(DatabaseConnection.dbProps.getProperty("timeout"))
            except ValueError as e2:
                print("[DB信息] 无法读取超时信息，使用默认值: " + DatabaseConnection.connectionTimeOut + " ")
        try:
            Class.forName(DatabaseConnection.dbDriver)
        except ClassNotFoundException as e3:
            print("[DB信息] 找不到JDBC驱动程序。")
        try:
            con = DriverManager.getConnection(DatabaseConnection.dbUrl, DatabaseConnection.dbUser, DatabaseConnection.dbPass)
            if !DatabaseConnection.propsInited:
                timeout = getWaitTimeout(con)
                if timeout == -1:
                    print("[DB信息] 无法读取 Wait_Timeout, using " + DatabaseConnection.connectionTimeOut + " instead.")
                else:
                    DatabaseConnection.connectionTimeOut = timeout
                    print("数据库正在加载.请稍等....")
                DatabaseConnection.propsInited = True
            return con
        except Exception as e:
            raise DatabaseException(e)

    def closeAll(self) -> None:
        for con in DatabaseConnection.connections.values():
            con.connection.close()
        DatabaseConnection.connections.clear()

    def closeTimeout(self) -> None:
        i = 0
        DatabaseConnection.lock.lock()
        keys = [])
        try:
            for tid in keys:
                con = DatabaseConnection.connections.get(tid)
                if con.close():
                    i += 1
        finally:
            DatabaseConnection.lock.unlock()

    def getConnection(self) -> Any:
        if self.expiredConnection():
            print("[DB信息] 连接 " + self.id + " 已经超时.重新连接...")
            try:
                self.connection.close()
            catch (SQLException ex) {}
            self.connection = connectToDB()
        self.lastAccessTime = int(time.time() * 1000)
        return self.connection

    def expiredConnection(self) -> bool:
        if self.lastAccessTime == 0:
            return False
        try:
            return int(time.time() * 1000) - self.lastAccessTime >= DatabaseConnection.connectionTimeOut || self.connection.isClosed()
        except Exception as ex:
            return True

    def close(self) -> bool:
        ret = False
        if self.connection is None:
            ret = False
        else:
            try:
                DatabaseConnection.lock.lock()
                try:
                    Label_0058:
                        if !self.expiredConnection():
                            if !self.connection.isValid(10):
                                Label_0058 = None
                        try:
                            self.connection.close()
                            ret = True
                        except Exception as e:
                            ret = False
                    DatabaseConnection.connections.remove(self.tid)
                finally:
                    DatabaseConnection.lock.unlock()
            except Exception as ex:
                ret = False
        return ret


# Inner class from Java (originally nested)
class ConWrapper:
    """
    Class ConWrapper
    """

    def __init__(self, tid: int, con: Any):
        self.tid = None
        self.lastAccessTime = 0
        self.connection = None
        self.id = 0
        self.lastAccessTime = 0
        self.tid = tid
        self.connection = con


    def getConnection(self) -> Any:
        if self.expiredConnection():
            print("[DB信息] 连接 " + self.id + " 已经超时.重新连接...")
            try:
                self.connection.close()
            catch (SQLException ex) {}
            self.connection = connectToDB()
        self.lastAccessTime = int(time.time() * 1000)
        return self.connection

    def expiredConnection(self) -> bool:
        if self.lastAccessTime == 0:
            return False
        try:
            return int(time.time() * 1000) - self.lastAccessTime >= DatabaseConnection.connectionTimeOut || self.connection.isClosed()
        except Exception as ex:
            return True

    def close(self) -> bool:
        ret = False
        if self.connection is None:
            ret = False
        else:
            try:
                DatabaseConnection.lock.lock()
                try:
                    Label_0058:
                        if !self.expiredConnection():
                            if !self.connection.isValid(10):
                                Label_0058 = None
                        try:
                            self.connection.close()
                            ret = True
                        except Exception as e:
                            ret = False
                    DatabaseConnection.connections.remove(self.tid)
                finally:
                    DatabaseConnection.lock.unlock()
            except Exception as ex:
                ret = False
        return ret

