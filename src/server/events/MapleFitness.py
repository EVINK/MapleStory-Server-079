"""
MapleFitness - Converted from Java source
Original: server/events/MapleFitness.java
Package: server.events
"""

from concurrent.futures import Future
from typing import Optional, Any
import sched
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleFitness(MapleEvent):
    """
    Class MapleFitness
    Extends: MapleEvent
    """

    serialVersionUID = 845748950824

    def __init__(self, channel: int, mapid: list):
        self.time = 600000
        self.timeStarted = 0
        super(channel, mapid)
        self.timeStarted = 0


    def finished(self, chr: Any) -> None:
        self.givePrize(chr)

    def onMapLoad(self, chr: Any) -> None:
        if self.isTimerStarted():
            chr.getClient().getSession().write(MaplePacketCreator.getClock((int)(self.getTimeLeft() / 1000)))

    def startEvent(self) -> None:
        self.unreset()
        super.reset()
        self.broadcast(MaplePacketCreator.getClock(600))
        self.timeStarted = int(time.time() * 1000)
        self.checkAndMessage()
        final Timer.EventTimer instance = Timer.EventTimer.getInstance()
        r = Runnable()
            public void run()
                for i in range(MapleFitness.self.len(mapid)):
                    for chr in MapleFitness.self.getMap(i).getCharactersThreadsafe():
                        MapleFitness.self.warpBack(chr)
                MapleFitness.self.unreset()
        self.getClass()
        self.fitnessSchedule = instance.schedule(r, 600000)
        self.broadcast(MaplePacketCreator.serverNotice(0, "门已打开。记得在光柱门↑键进入。"))

    def run(self) -> None:
        for i in range(MapleFitness.self.len(mapid)):
            for chr in MapleFitness.self.getMap(i).getCharactersThreadsafe():
                MapleFitness.self.warpBack(chr)
        MapleFitness.self.unreset()

    def isTimerStarted(self) -> bool:
        return self.timeStarted > 0

    def getTime(self) -> int:
        return 600000

    def resetSchedule(self) -> None:
        self.timeStarted = 0
        if self.fitnessSchedule is not None:
            self.fitnessSchedule.cancel(False)
        self.fitnessSchedule = None
        if self.msgSchedule is not None:
            self.msgSchedule.cancel(False)
        self.msgSchedule = None

    def reset(self) -> None:
        super.reset()
        self.resetSchedule()
        self.getMap(0).getPortal("join00").setPortalState(False)

    def unreset(self) -> None:
        super.unreset()
        self.resetSchedule()
        self.getMap(0).getPortal("join00").setPortalState(True)

    def getTimeLeft(self) -> int:
        return 600000 - (int(time.time() * 1000) - self.timeStarted)

    def checkAndMessage(self) -> None:
        self.msgSchedule = Timer.EventTimer.getInstance().register(Runnable()
            public void run()
                timeLeft = MapleFitness.self.getTimeLeft()
                if timeLeft > 9000 && timeLeft < 11000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "对于你们无法战胜的比赛，我们希望您下一次战胜它！下次再见~"))
                elif timeLeft > 11000 && timeLeft < 101000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "好吧，你剩下的时间没有多少了。请抓紧时间!"))
                elif timeLeft > 101000 && timeLeft < 241000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "第4阶段，是最后一项 [冒险岛体能测试]. 请不要在最后一刻放弃，拼尽全力. 丰厚的奖励在最高层等着你哦!"))
                elif timeLeft > 241000 && timeLeft < 301000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "第三阶段，有很多陷阱，你可能会看到他们，但你不能踩他们.按照你的方式进行下去吧."))
                elif timeLeft > 301000 && timeLeft < 361000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "请务必慢慢地移动，小心掉到下面去。"))
                elif timeLeft > 361000 && timeLeft < 501000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "请记住，如果你在活动期间死掉了，你会从游戏中淘汰. 如果你想补充HP，使用药水或移动之前先恢复HP。"))
                elif timeLeft > 501000 && timeLeft < 601000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "最重要的是你需要知道，不要被猴子扔的香蕉打中，请在规定的时间完成一切！"))
                elif timeLeft > 601000 && timeLeft < 661000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "第二阶段障碍是猴子扔香蕉. 请确保沿着正确的路线移动，躲避它们的攻击。"))
                elif timeLeft > 661000 && timeLeft < 701000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "请记住，如果你在活动期间死掉了，你会从游戏中淘汰. 如果你想补充HP，使用药水或移动之前先恢复HP。"))
                elif timeLeft > 701000 && timeLeft < 781000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "每个人都该参加 [冒险岛体能测试] 参加这个项目，无论完成的顺序，都会获得奖励，所以只是娱乐，慢慢来，清除了4个阶段。"))
                elif timeLeft > 781000 && timeLeft < 841000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "不要畏惧苦难，继续下去，享受游戏，重在娱乐嘛."))
                elif timeLeft > 841000:
                    MapleFitness.self.broadcast(MaplePacketCreator.serverNotice(0, "[冒险岛体能测试]有4个阶段，如果你碰巧在游戏过程中死亡，你会从比赛被淘汰，所以请注意这一点。"))

