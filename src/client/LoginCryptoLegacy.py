"""
LoginCryptoLegacy - 从Java源文件转换而来
对应Java源文件: client/LoginCryptoLegacy.java
包路径: client
"""

from typing import List
from typing import Optional, Any
import hashlib
import time


class LoginCryptoLegacy:
    """
    类 LoginCryptoLegacy - 从Java类转换
    """


    @staticmethod
    def hashPassword(password: str) -> str:
        """方法 hashPassword"""
        return ""

    def checkPassword(self, password: str, hash: str) -> bool:
        """方法 checkPassword"""
        return False

    def isLegacyPassword(self, hash: str) -> bool:
        """方法 isLegacyPassword"""
        return False

    def myCrypt(self, password: str, seed: str) -> str:
        """方法 myCrypt"""
        return ""

    def genSalt(self, Random: bytes) -> str:
        """方法 genSalt"""
        return ""

    def convertToHex(self, data: bytes) -> str:
        """方法 convertToHex"""
        return ""

    def encodeSHA1(self, text: str) -> str:
        """方法 encodeSHA1"""
        return ""

    def encode64(self, Input: bytes) -> str:
        """方法 encode64"""
        return ""

