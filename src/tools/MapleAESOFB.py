"""
MapleAESOFB - 从Java源文件转换而来
对应Java源文件: tools/MapleAESOFB.java
包路径: tools
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import Optional, Any
import tkinter


class MapleAESOFB:
    """
    类 MapleAESOFB - 从Java类转换
    """

    def __init__(self, iv: bytes, mapleVersion: int):
        """初始化 MapleAESOFB"""
        self.cipher = None
        self.mapleVersion = None


    def getPacketLength(self, packetHeader: int) -> int:
        """方法 getPacketLength"""
        return 0

    def getNewIv(self, oldIv: bytes) -> bytes:
        """方法 getNewIv"""
        return b""

    def funnyShit(self, inputByte: int, in: bytes) -> None:
        """方法 funnyShit"""
        pass

    def setIv(self, iv: bytes) -> None:
        """方法 setIv"""
        self.iv = iv
        return None

    def getIv(self) -> bytes:
        """方法 getIv"""
        return getattr(self, 'iv', b"")

    def crypt(self, data: bytes) -> bytes:
        """方法 crypt"""
        return b""

    def updateIv(self) -> None:
        """方法 updateIv"""
        pass

    def getPacketHeader(self, length: int) -> bytes:
        """方法 getPacketHeader"""
        return b""

    def checkPacket(self, packet: bytes) -> bool:
        """方法 checkPacket"""
        return False

    def checkPacket(self, packetHeader: int) -> bool:
        """方法 checkPacket"""
        return False

    def toString(self) -> str:
        """方法 toString"""
        return ""

