"""
Event_PyramidSubway - Converted from Java source
Original: server/maps/Event_PyramidSubway.java
Package: server.maps
"""

from concurrent.futures import Future
from typing import Optional, Any
import sched
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class Event_PyramidSubway:
    """
    Class Event_PyramidSubway
    """

    def __init__(self, c: Any):
        self.kill = 0
        self.cool = 0
        self.miss = 0
        self.skill = 0
        self.type = None
        self.energybar = 0
        self.broaded = False
        self.kill = 0
        self.cool = 0
        self.miss = 0
        self.skill = 0
        self.energybar = 100
        self.broaded = False
        mapid = c.getMapId()
        if mapid / 10000 == 91032:
            self.type = -1
        else:
            self.type = mapid % 10000 / 1000
        if c.getParty() is None || c.getParty().getLeader() == (MaplePartyCharacter(c)):
            self.commenceTimerNextMap(c, 1)
            self.energyBarDecrease = Timer.MapTimer.getInstance().register(Runnable()
                public void run()
                    Event_PyramidSubway.self.energybar -= ((c.getParty() is not None && c.getParty().getMembers() > 1) ? 10 : 5)
                    if Event_PyramidSubway.self.broaded:
                        c.getMap().respawn(True)
                    else:
                        Event_PyramidSubway.self.broaded = True
                    if Event_PyramidSubway.self.energybar <= 0:
                        Event_PyramidSubway.self.fail(c)


    def warpStartSubway(self, c: Any) -> bool:
        mapid = 910320100
        ch = c.getClient().getChannelServer()
        for i in range(5):
            map = ch.getMapFactory().getMap(mapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                changeMap(c, map, 25, 30)
                return True
        return False

    def warpBonusSubway(self, c: Any) -> bool:
        mapid = 910320010
        ch = c.getClient().getChannelServer()
        for i in range(20):
            map = ch.getMapFactory().getMap(mapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                c.changeMap(map, map.getPortal(0))
                return True
        return False

    def warpNextMap_Subway(self, c: Any) -> bool:
        currentmap = c.getMapId()
        thisStage = (currentmap - 910320100) / 100
        map = c.getMap()
        clearMap(map, True)
        ch = c.getClient().getChannelServer()
        if thisStage >= 2:
            map = ch.getMapFactory().getMap(910330001)
            changeMap(c, map, 1, 200, 1)
            return True
        nextmapid = 910320100 + (thisStage + 1) * 100
        for i in range(5):
            map = ch.getMapFactory().getMap(nextmapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                changeMap(c, map, 1, 200, 1)
                return True
        return False

    def warpStartPyramid(self, c: Any, difficulty: int) -> bool:
        mapid = 926010100 + difficulty * 1000
        minLevel = 40
        maxLevel = 60
        # switch (difficulty):
            # case 1:
                minLevel = 45
                break
            # case 2:
                minLevel = 50
                break
            # case 3:
                minLevel = 61
                maxLevel = 200
                break
        ch = c.getClient().getChannelServer()
        for i in range(5):
            map = ch.getMapFactory().getMap(mapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                changeMap(c, map, minLevel, maxLevel)
                return True
        return False

    def warpBonusPyramid(self, c: Any, difficulty: int) -> bool:
        mapid = 926010010 + difficulty * 20
        ch = c.getClient().getChannelServer()
        for i in range(20):
            map = ch.getMapFactory().getMap(mapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                c.changeMap(map, map.getPortal(0))
                return True
        return False

    def warpNextMap_Pyramid(self, c: Any, difficulty: int) -> bool:
        currentmap = c.getMapId()
        thisStage = (currentmap - (926010100 + difficulty * 1000)) / 100
        map = c.getMap()
        clearMap(map, True)
        ch = c.getClient().getChannelServer()
        if thisStage >= 4:
            map = ch.getMapFactory().getMap(926020001 + difficulty)
            changeMap(c, map, 1, 200, 1)
            return True
        nextmapid = 926010100 + (thisStage + 1) * 100 + difficulty * 1000
        for i in range(5):
            map = ch.getMapFactory().getMap(nextmapid + i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                changeMap(c, map, 1, 200, 1)
                return True
        return False

    def changeMap(self, c: Any, map: Any, minLevel: int, maxLevel: int) -> None:
        changeMap(c, map, minLevel, maxLevel, 0)

    def changeMap_c_map_minLevel_maxLevel_clear(self, c: Any, map: Any, minLevel: int, maxLevel: int, clear: int) -> None:
        oldMap = c.getMap()
        if c.getParty() is not None && c.getParty().getMembers() > 1:
            for mpc in c.getParty().getMembers():
                chr = oldMap.getCharacterById(mpc.getId())
                if chr is not None && chr.getId() != c.getId() && chr.getLevel() >= minLevel && chr.getLevel() <= maxLevel:
                    if clear == 1:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("pvp/victory"))
                    elif clear == 2:
                        chr.getClient().getSession().write(MaplePacketCreator.showEffect("pvp/lose"))
                    chr.changeMap(map, map.getPortal(0))
        if clear == 1:
            c.getClient().getSession().write(MaplePacketCreator.showEffect("pvp/victory"))
        elif clear == 2:
            c.getClient().getSession().write(MaplePacketCreator.showEffect("pvp/lose"))
        c.changeMap(map, map.getPortal(0))

    def clearMap(self, map: Any, check: bool) -> None:
        if check && map.getCharactersSize() > 0:
            return
        map.resetFully(False)

    def run(self) -> None:
        Event_PyramidSubway.self.energybar -= ((c.getParty() is not None && c.getParty().getMembers() > 1) ? 10 : 5)
        if Event_PyramidSubway.self.broaded:
            c.getMap().respawn(True)
        else:
            Event_PyramidSubway.self.broaded = True
        if Event_PyramidSubway.self.energybar <= 0:
            Event_PyramidSubway.self.fail(c)

    def fullUpdate(self, c: Any, stage: int) -> None:
        self.broadcastEnergy(c, "massacre_party", (c.getParty() is None) ? 0 : c.getParty().getMembers())
        self.broadcastEnergy(c, "massacre_miss", self.miss)
        self.broadcastEnergy(c, "massacre_cool", self.cool)
        self.broadcastEnergy(c, "massacre_skill", self.skill)
        self.broadcastEnergy(c, "massacre_laststage", stage - 1)
        self.broadcastEnergy(c, "massacre_hit", self.kill)
        self.broadcastUpdate(c)

    def commenceTimerNextMap(self, c: Any, stage: int) -> None:
        if self.timerSchedule is not None:
            self.timerSchedule.cancel(False)
            self.timerSchedule = None
        if self.yetiSchedule is not None:
            self.yetiSchedule.cancel(False)
            self.yetiSchedule = None
        ourMap = c.getMap()
        time = ((self.type == -1) ? 180 : ((stage == 1) ? 240 : 300)) - 1
        if c.getParty() is not None && c.getParty().getMembers() > 1:
            for mpc in c.getParty().getMembers():
                chr = ourMap.getCharacterById(mpc.getId())
                if chr is not None:
                    chr.getClient().getSession().write(MaplePacketCreator.getClock(time))
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/number/" + stage))
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/stage"))
                    chr.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/start"))
                    self.fullUpdate(chr, stage)
        else:
            c.getClient().getSession().write(MaplePacketCreator.getClock(time))
            c.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/number/" + stage))
            c.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/stage"))
            c.getClient().getSession().write(MaplePacketCreator.showEffect("killing/first/start"))
            self.fullUpdate(c, stage)
        if self.type != -1 && (stage == 4 || stage == 5):
            pos = c.getPosition()
            map = c.getMap()
            self.yetiSchedule = Timer.MapTimer.getInstance().register(Runnable()
                public void run()
                    if map.countMonsterById(9300021) <= ((stage == 4) ? 1 : 2):
                        map.spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(9300021), Point(pos))
        self.timerSchedule = Timer.MapTimer.getInstance().schedule(Runnable()
            public void run()
                ret = False
                if Event_PyramidSubway.self.type == -1:
                    ret = Event_PyramidSubway.warpNextMap_Subway(c)
                else:
                    ret = Event_PyramidSubway.warpNextMap_Pyramid(c, Event_PyramidSubway.self.type)
                if !ret:
                    Event_PyramidSubway.self.fail(c)

    def onKill(self, c: Any) -> None:
        self.kill += 1
        if Randomizer.nextInt(100) < 5:
            self.broadcastEnergy(c, "massacre_cool", ++self.cool)
        self.energybar += 5
        if self.energybar > 100:
            self.energybar = 100
        if self.type != -1:
            i = 5
            while i >= 1:
                if (self.kill + self.cool) % (i * 100) == 0 && Randomizer.nextInt(100) < 50:
                    self.broadcastEffect(c, "killing/yeti" + (i - 1))
                    break
            if (self.kill + self.cool) % 500 == 0:
                self.broadcastEnergy(c, "massacre_skill", ++self.skill)
        self.broadcastUpdate(c)
        self.broadcastEnergy(c, "massacre_hit", self.kill)

    def onMiss(self, c: Any) -> None:
        self.miss += 1
        self.energybar -= 5
        self.broadcastUpdate(c)
        self.broadcastEnergy(c, "massacre_miss", self.miss)

    def onSkillUse(self, c: Any) -> bool:
        if self.skill > 0 && self.type != -1:
            self.broadcastEnergy(c, "massacre_skill", --self.skill)
            return True
        return False

    def onChangeMap(self, c: Any, newmapid: int) -> None:
        if (newmapid == 910330001 && self.type == -1) || (newmapid == 926020001 + self.type && self.type != -1):
            self.succeed(c)
        elif self.type == -1 && (newmapid < 910320100 || newmapid > 910320304):
            self.dispose(c)
        elif self.type != -1 && (newmapid < 926010100 || newmapid > 926013504):
            self.dispose(c)
        elif c.getParty() is None || c.getParty().getLeader() == (MaplePartyCharacter(c)):
            self.commenceTimerNextMap(c, newmapid % 1000 / (self.energybar = 100))

    def succeed(self, c: Any) -> None:
        record = c.getQuestNAdd(MapleQuest.getInstance((self.type == -1) ? 7662 : 7760))
        data = record.getCustomData()
        if data is None:
            record.setCustomData("0")
            data = record.getCustomData()
        mons = int(data)
        tk = self.kill + self.cool
        record.setCustomData(str(mons + tk))
        rank = 4
        if self.type == -1:
            if tk >= 2000:
                rank = 0
            elif tk >= 1500 && tk <= 1999:
                rank = 1
            elif tk >= 1000 && tk <= 1499:
                rank = 2
            elif tk >= 500 && tk <= 999:
                rank = 3
        elif tk >= 3000:
            rank = 0
        elif tk >= 2000 && tk <= 2999:
            rank = 1
        elif tk >= 1500 && tk <= 1999:
            rank = 2
        elif tk >= 500 && tk <= 1499:
            rank = 3
        pt = 0
        Label_0581:
            # switch (self.type):
                # case 0:
                    # switch (rank):
                        # case 0:
                            pt = 60500
                            break
                        # case 1:
                            pt = 55000
                            break
                        # case 2:
                            pt = 46750
                            break
                        # case 3:
                            pt = 22000
                            break
                    break
                # case 1:
                    # switch (rank):
                        # case 0:
                            pt = 66000
                            break
                        # case 1:
                            pt = 60000
                            break
                        # case 2:
                            pt = 51750
                            break
                        # case 3:
                            pt = 24000
                            break
                    break
                # case 2:
                    # switch (rank):
                        # case 0:
                            pt = 71500
                            break
                        # case 1:
                            pt = 65000
                            break
                        # case 2:
                            pt = 55250
                            break
                        # case 3:
                            pt = 26000
                            break
                    break
                # case 3:
                    # switch (rank):
                        # case 0:
                            pt = 77000
                            break
                        # case 1:
                            pt = 70000
                            break
                        # case 2:
                            pt = 59500
                            break
                        # case 3:
                            pt = 28000
                            break
                    break
                # default:
                    # switch (rank):
                        # case 0:
                            pt = 22000
                            Label_0581 = None
                        # case 1:
                            pt = 17000
                            Label_0581 = None
                        # case 2:
                            pt = 10750
                            Label_0581 = None
                        # case 3:
                            pt = 7000
                            Label_0581 = None
                    break
        exp = 0
        if rank < 4:
            exp = (self.kill * 2 + self.cool * 10 + pt) * c.getClient().getChannelServer().getExpRate()
            c.gainExp(exp, True, False, False)
        c.getClient().getSession().write(MaplePacketCreator.showEffect("pvp/victory"))
        c.getClient().getSession().write(MaplePacketCreator.sendPyramidResult(rank, exp))
        self.dispose(c)

    def fail(self, c: Any) -> None:
        map = None
        if self.type == -1:
            map = c.getClient().getChannelServer().getMapFactory().getMap(910320001)
        else:
            map = c.getClient().getChannelServer().getMapFactory().getMap(926010001 + self.type)
        changeMap(c, map, 1, 200, 2)
        self.dispose(c)

    def dispose(self, c: Any) -> None:
        lead = self.energyBarDecrease is not None && self.timerSchedule is not None
        if self.energyBarDecrease is not None:
            self.energyBarDecrease.cancel(False)
            self.energyBarDecrease = None
        if self.timerSchedule is not None:
            self.timerSchedule.cancel(False)
            self.timerSchedule = None
        if self.yetiSchedule is not None:
            self.yetiSchedule.cancel(False)
            self.yetiSchedule = None
        if c.getParty() is not None && lead && c.getParty().getMembers() > 1:
            self.fail(c)
            return
        c.setPyramidSubway(None)

    def broadcastUpdate(self, c: Any) -> None:
        map = c.getMap()
        if c.getParty() is not None && c.getParty().getMembers() > 1:
            for mpc in c.getParty().getMembers():
                chr = map.getCharacterById(mpc.getId())
                if chr is not None:
                    chr.getClient().getSession().write(MaplePacketCreator.sendPyramidUpdate(self.energybar))
        else:
            c.getClient().getSession().write(MaplePacketCreator.sendPyramidUpdate(self.energybar))

    def broadcastEffect(self, c: Any, effect: str) -> None:
        c.getClient().getSession().write(MaplePacketCreator.showEffect(effect))

    def broadcastEnergy(self, c: Any, type: str, amount: int) -> None:
        c.getClient().getSession().write(MaplePacketCreator.sendPyramidEnergy(type, str(amount)))

