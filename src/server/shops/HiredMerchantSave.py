"""
HiredMerchantSave - Converted from Java source
Original: server/shops/HiredMerchantSave.java
Package: server.shops
"""

from threading import Lock
from typing import List
from typing import Optional, Any
import logging
import threading
import time


class HiredMerchantSave:
    """
    Class HiredMerchantSave
    """

    def __init__(self):
        self.ext = None
        self.ThreadID = None
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.ToNotify = None
        self.Queue = None

    # Static initializer
    # HiredMerchantSave.NumSavingThreads = 5
    # Threads = new TimingThread[5]
    # for i in range(HiredMerchantSave.len(Threads)):
    # HiredMerchantSave.Threads[i] = TimingThread(HiredMerchantSaveRunnable())
    # Distribute = AtomicInteger(0)


    @staticmethod
    def QueueShopForSave(hm: Any) -> None:
        Current = HiredMerchantSave.Distribute.getAndIncrement() % 5
        HiredMerchantSave.Threads[Current].getRunnable().Queue(hm)

    def Execute(self, ToNotify: Any) -> None:
        for i in range(HiredMerchantSave.len(Threads)):
            HiredMerchantSave.Threads[i].getRunnable().SetToNotify(ToNotify)
        for i in range(HiredMerchantSave.len(Threads)):
            HiredMerchantSave.Threads[i].start()

    def getRunnable(self) -> Any:
        return self.ext

    def run(self) -> None:
        try:
            while not self.Queue == 0:
                next = self.Queue.take()
                Start = int(time.time() * 1000)
                next.closeShop(True, False)
                self.TimeTaken += int(time.time() * 1000) - Start
                self.ShopsSaved += 1
            print("[保存雇佣商店数据 线程 " + self.ThreadID + "] 共保存: " + self.ShopsSaved + " | 耗时: " + self.TimeTaken + " 毫秒.")
            with self.ToNotify:  # synchronized
                self.ToNotify.notify()
        except InterruptedException as ex:
            Logger.getLogger(HiredMerchantSave.class.getName()).log(Level.SEVERE, None, ex)

    def Queue(self, hm: Any) -> None:
        self.Queue.add(hm)

    def SetToNotify(self, o: Any) -> None:
        if self.ToNotify is None:
            self.ToNotify = o


# Inner class from Java (originally nested)
class TimingThread(Thread):
    """
    Class TimingThread
    Extends: Thread
    """

    def __init__(self, r: Any):
        self.ext = None
        self.ext = r


    def getRunnable(self) -> Any:
        return self.ext


# Inner class from Java (originally nested)
class HiredMerchantSaveRunnable(Runnable):
    """
    Class HiredMerchantSaveRunnable
    Implements: Runnable
    """

    def __init__(self):
        self.ThreadID = None
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.ToNotify = None
        self.Queue = None
        self.ThreadID = HiredMerchantSaveRunnable.RunningThreadID.incrementAndGet()
        self.TimeTaken = 0
        self.ShopsSaved = 0
        self.Queue = new ArrayBlockingQueue<HiredMerchant>(500)

    # Static initializer
    # RunningThreadID = AtomicInteger(0)


    def run(self) -> None:
        try:
            while not self.Queue == 0:
                next = self.Queue.take()
                Start = int(time.time() * 1000)
                next.closeShop(True, False)
                self.TimeTaken += int(time.time() * 1000) - Start
                self.ShopsSaved += 1
            print("[保存雇佣商店数据 线程 " + self.ThreadID + "] 共保存: " + self.ShopsSaved + " | 耗时: " + self.TimeTaken + " 毫秒.")
            with self.ToNotify:  # synchronized
                self.ToNotify.notify()
        except InterruptedException as ex:
            Logger.getLogger(HiredMerchantSave.class.getName()).log(Level.SEVERE, None, ex)

    def Queue(self, hm: Any) -> None:
        self.Queue.add(hm)

    def SetToNotify(self, o: Any) -> None:
        if self.ToNotify is None:
            self.ToNotify = o

