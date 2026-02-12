"""
MerchItemPackage - 从Java源文件转换而来
对应Java源文件: server/MerchItemPackage.java
包路径: server
"""

from typing import List
from typing import Optional, List, Dict, Any, Set

# 内部模块导入 (Internal module imports)
# from client.inventory.IItem import *  # TODO: 根据实际需要导入具体类


class MerchItemPackage:
    """
    类 MerchItemPackage - 从Java类转换
    """

    def __init__(self):
        """初始化 MerchItemPackage"""
        self.sentTime = 0
        self.mesos = 0
        self.packageid = 0
        self.items = []


    def setItems(self, items: list) -> None:
        """方法 setItems"""
        self.items = items
        return None

    def getItems(self) -> list:
        """方法 getItems"""
        return getattr(self, 'items', [])

    def setSentTime(self, sentTime: int) -> None:
        """方法 setSentTime"""
        self.sent_time = sentTime
        return None

    def getSentTime(self) -> int:
        """方法 getSentTime"""
        return getattr(self, 'sent_time', 0)

    def getMesos(self) -> int:
        """方法 getMesos"""
        return getattr(self, 'mesos', 0)

    def setMesos(self, set: int) -> None:
        """方法 setMesos"""
        self.mesos = set
        return None

    def getPackageid(self) -> int:
        """方法 getPackageid"""
        return getattr(self, 'packageid', 0)

    def setPackageid(self, packageid: int) -> None:
        """方法 setPackageid"""
        self.packageid = packageid
        return None

