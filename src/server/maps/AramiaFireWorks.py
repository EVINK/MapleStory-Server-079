"""
AramiaFireWorks - Converted from Java source
Original: server/maps/AramiaFireWorks.java
Package: server.maps
"""

from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class AramiaFireWorks:
    """
    Class AramiaFireWorks
    """

    KEG_ID = 4031875
    SUN_ID = 4001246
    DEC_ID = 4001473
    MAX_KEGS = 10000
    MAX_SUN = 14000
    MAX_DEC = 18000
    flake_Y = 149

    def __init__(self):
        self.kegs = 0
        self.sunshines = 0
        self.decorations = 0
        self.kegs = 0
        self.sunshines = 2333
        self.decorations = 3000

    # Static initializer
    # instance = AramiaFireWorks()
    # arrayMob = new int[] { 9400708 }
    # arrayX = new int[] { -115 }
    # arrayY = new int[] { 154 }
    # array_X = new int[] { 720, 180, 630, 270, 360, 540, 450, 142, 142, 218, 772, 810, 848, 232, 308, 142 }
    # array_Y = new int[] { 1234, 1234, 1174, 1234, 1174, 1174, 1174, 1260, 1234, 1234, 1234, 1234, 1234, 1114, 1114, 1140 }


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def giveKegs(self, c: Any, kegs: int) -> None:
        self.kegs += kegs
        if self.kegs >= 10000:
            self.kegs = 0
            self.broadcastEvent(c)

    def broadcastServer(self, c: Any, itemid: int) -> None:
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, itemid, "<頻道 " + c.getClient().getChannel() + "> 弓箭手村邱比特公園即將開始發射煙火!").encode("utf-8"))

    def getKegsPercentage(self) -> int:
        return (short)(self.kegs / 10000 * 10000)

    def broadcastEvent(self, c: Any) -> None:
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                AramiaFireWorks.self.startEvent(c.getClient().getChannelServer().getMapFactory().getMap(209080000))

    def run(self) -> None:
        AramiaFireWorks.self.startEvent(c.getClient().getChannelServer().getMapFactory().getMap(209080000))

    def startEvent(self, map: Any) -> None:
        map.startMapEffect("雪人大大出現啦", 5120000)
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                AramiaFireWorks.self.spawnMonster(map)

    def spawnMonster(self, map: Any) -> None:
        for i in range(AramiaFireWorks.len(arrayMob)):
            pos = Point(AramiaFireWorks.arrayX[i], AramiaFireWorks.arrayY[i])
            map.spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(AramiaFireWorks.arrayMob[i]), pos)

    def giveSuns(self, c: Any, kegs: int) -> None:
        self.sunshines += kegs
        map = c.getClient().getChannelServer().getMapFactory().getMap(555000000)
        reactor = map.getReactorByName("XmasTree")
        gogo = kegs + 2333
        while gogo > 0:
            # switch (reactor.getState()):
                # case 0:
                # case 1:
                # case 2:
                # case 3:
                # case 4:
                    if self.sunshines >= 2333 * (2 + reactor.getState()):
                        reactor.setState((byte)(reactor.getState() + 1))
                        reactor.setTimerActive(False)
                        map.broadcastMessage(MaplePacketCreator.triggerReactor(reactor, reactor.getState()))
                        break
                    break
                # default:
                    if self.sunshines >= 2333:
                        map.resetReactors()
                        break
                    break
        if self.sunshines >= 14000:
            self.sunshines = 0
            self.broadcastSun(c)

    def getSunsPercentage(self) -> int:
        return (short)(self.sunshines / 14000 * 10000)

    def broadcastSun(self, c: Any) -> None:
        self.broadcastServer(c, 4001246)
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                AramiaFireWorks.self.startSun(c.getClient().getChannelServer().getMapFactory().getMap(970010000))

    def startSun(self, map: Any) -> None:
        map.startMapEffect("The tree is bursting with sunshine!", 5121010)
        for i in range(3):
            Timer.EventTimer.getInstance().schedule(Runnable()
                public void run()
                    AramiaFireWorks.self.spawnItem(map)

    def spawnItem(self, map: Any) -> None:
        for i in range(Randomizer.nextInt(5) + 10):
            pos = Point(AramiaFireWorks.array_X[i], AramiaFireWorks.array_Y[i])
            map.spawnAutoDrop((Randomizer.nextInt(3) == 1) ? 3010025 : 4001246, pos)

    def giveDecs(self, c: Any, kegs: int) -> None:
        self.decorations += kegs
        map = c.getClient().getChannelServer().getMapFactory().getMap(555000000)
        reactor = map.getReactorByName("XmasTree")
        gogo = kegs + 3000
        while gogo > 0:
            # switch (reactor.getState()):
                # case 0:
                # case 1:
                # case 2:
                # case 3:
                # case 4:
                    if self.decorations >= 3000 * (2 + reactor.getState()):
                        reactor.setState((byte)(reactor.getState() + 1))
                        reactor.setTimerActive(False)
                        map.broadcastMessage(MaplePacketCreator.triggerReactor(reactor, reactor.getState()))
                        break
                    break
                # default:
                    if self.decorations >= 3000:
                        map.resetReactors()
                        break
                    break
        if self.decorations >= 18000:
            self.decorations = 0
            self.broadcastDec(c)

    def getDecsPercentage(self) -> int:
        return (short)(self.decorations / 18000 * 10000)

    def broadcastDec(self, c: Any) -> None:
        self.broadcastServer(c, 4001473)
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                AramiaFireWorks.self.startDec(c.getClient().getChannelServer().getMapFactory().getMap(555000000))

    def startDec(self, map: Any) -> None:
        map.startMapEffect("The tree is bursting with snow!", 5120000)
        for i in range(3):
            Timer.EventTimer.getInstance().schedule(Runnable()
                public void run()
                    AramiaFireWorks.self.spawnDec(map)

    def spawnDec(self, map: Any) -> None:
        for i in range(Randomizer.nextInt(10) + 40):
            pos = Point(Randomizer.nextInt(800) - 400, 149)
            map.spawnAutoDrop((Randomizer.nextInt(15) == 1) ? 2060006 : 2060006, pos)

