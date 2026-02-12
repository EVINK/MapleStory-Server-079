"""
GetInfo - Converted from Java source
Original: tools/GetInfo.java
Package: tools
"""

from configparser import ConfigParser
from socket import socket
from typing import Dict
from typing import List
from typing import Optional, Any
import json
import os
import sys

# Internal module imports
# from handling.RecvPacketOpcode import *  # TODO: import specific classes


class GetInfo:
    """
    Class GetInfo
    """


    def main(self, args: list) -> None:
        Config()
        getConfig()
        all()
        # System.setProperty("server_property_file_path","E:/game/2020mxd079/079sever/HuaiMS_服务端配置.properties");
        # System.setProperty("server_property_db_path","E:/game/2020mxd079/079sever/HuaiMS_数据库配置.properties");
        # System.setProperty("server_property_shop_path","E:/game/2020mxd079/079sever/HuaiMS_封商城道具.properties");
        # System.setProperty("server_property_fish_path","E:/game/2020mxd079/079sever/HuaiMS_钓鱼设置.properties");

    def getIpconfig(self) -> None:
        map = System.getenv()
        print(map)
        print(map.get("USERNAME"))
        print(map.get("COMPUTERNAME"))
        print(map.get("USERDOMAIN"))
        print(map.get("USER"))

    def all(self) -> None:
        設定檔 = System.getProperties()
        print("Java的運行環境版本：" + 設定檔.getProperty("java.version"))
        print("Java的運行環境供應商：" + 設定檔.getProperty("java.vendor"))
        print("Java供應商的URL：" + 設定檔.getProperty("java.vendor.url"))
        print("Java的安裝路徑：" + 設定檔.getProperty("java.home"))
        print("Java的虛擬機規範版本：" + 設定檔.getProperty("java.vm.specification.version"))
        print("Java的虛擬機規範供應商：" + 設定檔.getProperty("java.vm.specification.vendor"))
        print("Java的虛擬機規範名稱：" + 設定檔.getProperty("java.vm.specification.name"))
        print("Java的虛擬機實現版本：" + 設定檔.getProperty("java.vm.version"))
        print("Java的虛擬機實現供應商：" + 設定檔.getProperty("java.vm.vendor"))
        print("Java的虛擬機實現名稱：" + 設定檔.getProperty("java.vm.name"))
        print("Java運行時環境規範版本：" + 設定檔.getProperty("java.specification.version"))
        print("Java運行時環境規範名稱：" + 設定檔.getProperty("java.specification.name"))
        print("Java的類格式版本號：" + 設定檔.getProperty("java.class.version"))
        print("Java的類路徑：" + 設定檔.getProperty("java.class.path"))
        print("加載庫時搜索的路徑列表：" + 設定檔.getProperty("java.library.path"))
        print("默認的臨時文件路徑：" + 設定檔.getProperty("java.io.tmpdir"))
        print("一個或多個擴展目錄的路徑：" + 設定檔.getProperty("java.ext.dirs"))
        print("操作系統的構架：" + 設定檔.getProperty("os.arch"))
        print("操作系統的版本：" + 設定檔.getProperty("os.version"))
        print("文件分隔符：" + 設定檔.getProperty("file.separator"))
        print("路徑分隔符：" + 設定檔.getProperty("path.separator"))
        print("行分隔符：" + 設定檔.getProperty("line.separator"))
        print("用戶的賬戶名稱：" + 設定檔.getProperty("user.name"))
        print("用戶的主目錄：" + 設定檔.getProperty("user.home"))
        print("用戶的當前工作目錄：" + 設定檔.getProperty("user.dir"))

    def Config(self) -> None:
        try:
            addr = InetAddress.getLocalHost()
            ip = addr.getHostAddress()
            hostName = addr.getHostName()
            print("本機IP：" + ip + "\n本機名稱:" + hostName)
            設定檔 = System.getProperties()
            print("操作系統的名稱：" + 設定檔.getProperty("os.name"))
            print("操作系統的版本：" + 設定檔.getProperty("os.version"))
        except UnknownHostException as e:
            e.printStackTrace()

    def getConfig(self) -> None:
        try:
            address = InetAddress.getLocalHost()
            ni = NetworkInterface.getByInetAddress(address)
            mac = ni.getHardwareAddress()
            if mac is None:
            mac = (ni.getInetAddresses().nextElement()).getAddress()
            sIP = address.getHostAddress()
            sMAC = ""
            formatter = Formatter()
            for i in range(len(mac)):
                sMAC = formatter.format(Locale.getDefault(), "%02X%s", new Object[] { Byte.valueOf(mac[i]), (i < len(mac) - 1) ? "-" : "" })
            print("IP：" + sIP)
            print("MAC：" + sMAC)
        except Exception:
            e.printStackTrace()

