"""
ServerProperties - Converted from Java source
Original: server/ServerProperties.java
Package: server
"""

from configparser import ConfigParser
from io import TextIOWrapper
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Optional, Any
import json
import os
import pymysql
import sys

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class ServerProperties:
    """
    Class ServerProperties
    """

    def __init__(self):
        pass
        pass

    # Static initializer
    # ServerProperties.showPacket = True
    # ServerProperties.props = Properties()
    # try:
    # path = os.environ.get("server_property_file_path")
    # fr = InputStreamReader(FileInputStream(path), "UTF-8")
    # ServerProperties.props.load(fr)
    # fr.close()
    # except IOError as ex:
    # print("加载Settings错误：" + ex)
    # try:
    # ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM auth_server_channel_ip")
    # rs = ps.executeQuery()
    # while rs.next():
    # props.put(rs.getString("name") + rs.getInt("channelid"), rs.getString("value"))
    # rs.close()
    # ps.close()
    # except SQLException as ex:
    # ex.printStackTrace()
    # sys.exit(0)


    @staticmethod
    def ShowPacket() -> bool:
        return ServerProperties.showPacket

    def getProperty(self, s: str) -> str:
        return ServerProperties.props.getProperty(s)

    def setProperty(self, prop: str, newInf: str) -> None:
        ServerProperties.props.setProperty(prop, newInf)

    def getProperty_s_def(self, s: str, def: str) -> str:
        return ServerProperties.props.getProperty(s, def)

