"""
HiredMerchantSave - 从Java源文件转换而来
对应Java源文件: server/shops/HiredMerchantSave.java
包路径: server.shops
"""

from threading import Lock
from typing import List
from typing import Optional, Any
import logging
import threading
import time


class HiredMerchantSave:
    """
    类 HiredMerchantSave - 从Java类转换
    """

    def __init__(self):
        """初始化 HiredMerchantSave"""
        self.ext = None
        self.ThreadID = None
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.ToNotify = None
        self.Queue = None


    @staticmethod
    def QueueShopForSave(hm: Any) -> None:
        """方法 QueueShopForSave"""
        pass

    def Execute(self, ToNotify: Any) -> None:
        """方法 Execute"""
        pass

    def getRunnable(self) -> Any:
        """方法 getRunnable"""
        raise NotImplementedError("方法 getRunnable 尚未实现")

    def run(self) -> None:
        """方法 run"""
        pass

    def Queue(self, hm: Any) -> None:
        """方法 Queue"""
        pass

    def SetToNotify(self, o: Any) -> None:
        """方法 SetToNotify"""
        pass


class TimingThread(Thread):
    """
    类 TimingThread - 从Java类转换
    继承自: Thread
    """

    def __init__(self, r: Any):
        """初始化 TimingThread"""
        self.ext = None
        self.ThreadID = None
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.ToNotify = None
        self.Queue = None


    @staticmethod
    def QueueShopForSave(hm: Any) -> None:
        """方法 QueueShopForSave"""
        pass

    def Execute(self, ToNotify: Any) -> None:
        """方法 Execute"""
        pass

    def getRunnable(self) -> Any:
        """方法 getRunnable"""
        raise NotImplementedError("方法 getRunnable 尚未实现")

    def run(self) -> None:
        """方法 run"""
        pass

    def Queue(self, hm: Any) -> None:
        """方法 Queue"""
        pass

    def SetToNotify(self, o: Any) -> None:
        """方法 SetToNotify"""
        pass


class HiredMerchantSaveRunnable(Runnable):
    """
    类 HiredMerchantSaveRunnable - 从Java类转换
    实现接口: Runnable
    """

    def __init__(self):
        """初始化 HiredMerchantSaveRunnable"""
        self.ext = None
        self.ThreadID = None
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.ToNotify = None
        self.Queue = None


    @staticmethod
    def QueueShopForSave(hm: Any) -> None:
        """方法 QueueShopForSave"""
        pass

    def Execute(self, ToNotify: Any) -> None:
        """方法 Execute"""
        pass

    def getRunnable(self) -> Any:
        """方法 getRunnable"""
        raise NotImplementedError("方法 getRunnable 尚未实现")

    def run(self) -> None:
        """方法 run"""
        pass

    def Queue(self, hm: Any) -> None:
        """方法 Queue"""
        pass

    def SetToNotify(self, o: Any) -> None:
        """方法 SetToNotify"""
        pass

