"""
MapleEvent - Converted from Java source
Original: server/events/MapleEvent.java
Package: server.events
"""

from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.RandomRewards import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.SavedLocationType import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleEvent:
    """
    Class MapleEvent
    """

    def __init__(self, channel: int, mapid: list):
        self.channel = 0
        self.isRunning = False
        self.isRunning = False
        self.channel = channel
        self.mapid = mapid


    def setEvent(self, cserv: Any, auto: bool) -> None:
        if auto:
            for t in MapleEventType.values():
                e = cserv.getEvent(t)
                if e.isRunning:
                    for i in e.mapid:
                        if cserv.getEvent() == i:
                            e.broadcast(MaplePacketCreator.serverNotice(0, "距离活动开始只剩下一分钟!"))
                            e.broadcast(MaplePacketCreator.getClock(60))
                            Timer.EventTimer.getInstance().schedule(Runnable()
                                public void run()
                                    e.startEvent()
                            break
        cserv.setEvent(-1)

    def run(self) -> None:
        e.startEvent()

    def mapLoad(self, chr: Any, channel: int) -> None:
        if chr is None:
            return
        for t in MapleEventType.values():
            e = ChannelServer.getInstance(channel).getEvent(t)
            if e.isRunning:
                if chr.getMapId() == 109050000:
                    e.finished(chr)
                for i in e.mapid:
                    if chr.getMapId() == i:
                        e.onMapLoad(chr)

    def onStartEvent(self, chr: Any) -> None:
        for t in MapleEventType.values():
            e = chr.getClient().getChannelServer().getEvent(t)
            if e.isRunning:
                for i in e.mapid:
                    if chr.getMapId() == i:
                        e.startEvent()
                        chr.dropMessage(5, str(t) + " 活动开始")

    def scheduleEvent(self, event: Any, cserv: Any) -> str:
        if cserv.getEvent() != -1 || cserv.getEvent(event) is None:
            return "改活动已经被禁止安排了."
        for i in cserv.getEvent(event).mapid:
            if cserv.getMapFactory().getMap(i).getCharactersSize() > 0:
                return "该活动已经在执行中."
        cserv.setEvent(cserv.getEvent(event).mapid[0])
        cserv.getEvent(event).reset()
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "活动 " + str(event) + " 即将在频道 " + cserv.getChannel() + " 举行 , 要参加的玩家请到频道 " + cserv.getChannel() + ".请找到自由市场相框活动npc并进入！").encode("utf-8"))
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "活动 " + str(event) + " 即将在频道 " + cserv.getChannel() + " 举行 , 要参加的玩家请到频道 " + cserv.getChannel() + ".请找到自由市场相框活动npc并进入！").encode("utf-8"))
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "活动 " + str(event) + " 即将在频道 " + cserv.getChannel() + " 举行 , 要参加的玩家请到频道 " + cserv.getChannel() + ".请找到自由市场相框活动npc并进入！").encode("utf-8"))
        return ""

    def isRunning(self) -> bool:
        return self.isRunning

    def getMap(self, i: int) -> Any:
        return self.getChannelServer().getMapFactory().getMap(self.mapid[i])

    def getChannelServer(self) -> Any:
        return ChannelServer.getInstance(self.channel)

    def broadcast(self, packet: Any) -> None:
        for i in range(self.len(mapid)):
            self.getMap(i).broadcastMessage(packet)

    def givePrize(self, chr: Any) -> None:
        reward = RandomRewards.getInstance().getEventReward()
        # switch (reward):
            # case 0:
                chr.gainMeso(66666, True, False, False)
                chr.dropMessage(5, "你获得 166666 冒险币")
                break
            # case 1:
                chr.gainMeso(399999, True, False, False)
                chr.dropMessage(5, "你获得 399999 冒险币")
                break
            # case 2:
                chr.modifyCSPoints(0, 200, False)
                chr.dropMessage(5, "你获得 200 点卷")
                break
            # case 3:
                chr.addFame(2)
                chr.dropMessage(5, "你获得 2 人气")
                break
        if MapleInventoryManipulator.checkSpace(chr.getClient(), 4032226, 1, ""):
            MapleInventoryManipulator.addById(chr.getClient(), 4032226, 1, 0)
            chr.dropMessage(5, "你获得 1 个黄金猪猪")
        else:
            chr.gainMeso(100000, True, False, False)
            chr.dropMessage(5, "由于你背包满了。所以只能给予你冒险币！")

    def finished(self, chr: Any) -> None:
        pass

    def onMapLoad(self, chr: Any) -> None:
        pass

    def startEvent(self) -> None:
        pass

    def warpBack(self, chr: Any) -> None:
        map = chr.getSavedLocation(SavedLocationType.EVENT)
        if map <= -1:
            map = 104000000
        mapp = chr.getClient().getChannelServer().getMapFactory().getMap(map)
        chr.changeMap(mapp, mapp.getPortal(0))

    def reset(self) -> None:
        self.isRunning = True

    def unreset(self) -> None:
        self.isRunning = False

