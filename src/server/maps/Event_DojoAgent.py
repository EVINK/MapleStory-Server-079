"""
Event_DojoAgent - Converted from Java source
Original: server/maps/Event_DojoAgent.java
Package: server.maps
"""

from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class Event_DojoAgent:
    """
    Class Event_DojoAgent
    """

    baseAgentMapId = 970030000

    # Static initializer
    # point1 = Point(140, 0)
    # point2 = Point(-193, 0)
    # point3 = Point(355, 0)


    @staticmethod
    def warpStartAgent(c: Any, party: bool) -> bool:
        stage = 1
        mapid = 970030000 + stage * 100
        ch = c.getClient().getChannelServer()
        i = mapid
        while i < mapid + 15:
            map = ch.getMapFactory().getMap(i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                c.changeMap(map, map.getPortal(0))
                map.respawn(True)
                return True
        return False

    def warpNextMap_Agent(self, c: Any, fromResting: bool) -> bool:
        currentmap = c.getMapId()
        thisStage = (currentmap - 970030000) / 100
        map = c.getMap()
        bossid = 9500336 + thisStage
        if map.countMonsterById(bossid) > 0:
            return False
        if not fromResting:
            clearMap(map, True)
        ch = c.getClient().getChannelServer()
        if currentmap >= 970032700 and currentmap <= 970032800:
            map = ch.getMapFactory().getMap(970030000)
            c.changeMap(map, map.getPortal(0))
            return True
        i = None
        nextmapid = i = 970030000 + (thisStage + 1) * 100
        while i < nextmapid + 7:
            map = ch.getMapFactory().getMap(i)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                c.changeMap(map, map.getPortal(0))
                map.respawn(True)
                return True
        return False

    def warpStartDojo(self, c: Any, party: bool) -> bool:
        stage = 1
        if party or stage <= -1 or stage > 38:
            stage = 1
        mapid = 925020000 + stage * 100
        canenter = False
        ch = c.getClient().getChannelServer()
        for x in range(15):
            canenterr = True
            for i in range(1, 39):
                map = ch.getMapFactory().getMap(925020000 + 100 * i + x)
                if map.getCharactersSize() > 0:
                    canenterr = False
                    break
                clearMap(map, False)
            if canenterr:
                canenter = True
                mapid += x
                break
        map2 = ch.getMapFactory().getMap(mapid)
        mapidd = c.getMap()
        if canenter:
            if party and c.getParty() is not None:
                for mem in c.getParty().getMembers():
                    chr = mapidd.getCharacterById(mem.getId())
                    if chr is not None:
                        chr.changeMap(map2, map2.getPortal(0))
            else:
                c.changeMap(map2, map2.getPortal(0))
            spawnMonster(map2, stage)
        return canenter

    def warpNextMap(self, c: Any, fromResting: bool) -> bool:
        try:
            currentmap = c.getMap()
            temp = (currentmap.getId() - 925000000) / 100
            thisStage = temp - temp / 100 * 100
            points = getDojoPoints(thisStage)
            ch = c.getClient().getChannelServer()
            if not fromResting:
                clearMap(currentmap, True)
                if c.getParty() is not None and c.getParty().getMembers() > 1:
                    for mem in c.getParty().getMembers():
                        chr = currentmap.getCharacterById(mem.getId())
                        if chr is not None:
                            point = points * 3
                            chr.setDojo(chr.getDojo() + point)
                            chr.getClient().getSession().write(MaplePacketCreator.Mulung_Pts(point, chr.getDojo()))
                else:
                    point2 = (points + 1) * 3
                    c.setDojo(c.getDojo() + point2)
                    c.getClient().getSession().write(MaplePacketCreator.Mulung_Pts(point2, c.getDojo()))
            if currentmap.getId() >= 925023800 and currentmap.getId() <= 925023814:
                map = ch.getMapFactory().getMap(925020003)
                if c.getParty() is not None:
                    for mem2 in c.getParty().getMembers():
                        chr2 = currentmap.getCharacterById(mem2.getId())
                        if chr2 is not None:
                            chr2.changeMap(map, map.getPortal(1))
                else:
                    c.changeMap(map, map.getPortal(1))
                return True
            map = ch.getMapFactory().getMap(currentmap.getId() + 100)
            if map.getCharactersSize() == 0:
                clearMap(map, False)
                if c.getParty() is not None:
                    for mem2 in c.getParty().getMembers():
                        chr2 = currentmap.getCharacterById(mem2.getId())
                        if chr2 is not None:
                            chr2.changeMap(map, map.getPortal(0))
                else:
                    c.changeMap(map, map.getPortal(0))
                spawnMonster(map, thisStage + 1)
                return True
            basemap = currentmap.getId() / 100 * 100 + 100
            for x in range(15):
                mapz = ch.getMapFactory().getMap(basemap + x)
                if mapz.getCharactersSize() == 0:
                    clearMap(mapz, False)
                    if c.getParty() is not None:
                        for mem3 in c.getParty().getMembers():
                            chr3 = currentmap.getCharacterById(mem3.getId())
                            if chr3 is not None:
                                chr3.changeMap(mapz, mapz.getPortal(0))
                    else:
                        c.changeMap(mapz, mapz.getPortal(0))
                    spawnMonster(mapz, thisStage + 1)
                    return True
        except Exception as rm:
            rm.printStackTrace()
        return False

    def clearMap(self, map: Any, check: bool) -> None:
        if check and map.getCharactersSize() != 0:
            return
        map.resetFully()

    def getDojoPoints(self, stage: int) -> int:
        # switch (stage):
            # case 1:
            # case 2:
            # case 3:
            # case 4:
            # case 5:
                return 1
            # case 7:
            # case 8:
            # case 9:
            # case 10:
            # case 11:
                return 2
            # case 13:
            # case 14:
            # case 15:
            # case 16:
            # case 17:
                return 3
            # case 19:
            # case 20:
            # case 21:
            # case 22:
            # case 23:
                return 4
            # case 25:
            # case 26:
            # case 27:
            # case 28:
            # case 29:
                return 5
            # case 31:
            # case 32:
            # case 33:
            # case 34:
            # case 35:
                return 6
            # case 37:
            # case 38:
                return 7
            # default:
                return 0

    def spawnMonster(self, map: Any, stage: int) -> None:
        def _task_1():
            map.spawnMonsterWithEffect(MapleLifeFactory.getMonster(mobid), 15, (rand == 0) ? Event_DojoAgent.point1 : ((rand == 1) ? Event_DojoAgent.point2 : Event_DojoAgent.point3))

        mobid = None
        # switch (stage):
            # case 1:
            mobid = 9300184
            break
            # case 2:
            mobid = 9300185
            break
            # case 3:
            mobid = 9300186
            break
            # case 4:
            mobid = 9300187
            break
            # case 5:
            mobid = 9300188
            break
            # case 7:
            mobid = 9300189
            break
            # case 8:
            mobid = 9300190
            break
            # case 9:
            mobid = 9300191
            break
            # case 10:
            mobid = 9300192
            break
            # case 11:
            mobid = 9300193
            break
            # case 13:
            mobid = 9300194
            break
            # case 14:
            mobid = 9300195
            break
            # case 15:
            mobid = 9300196
            break
            # case 16:
            mobid = 9300197
            break
            # case 17:
            mobid = 9300198
            break
            # case 19:
            mobid = 9300199
            break
            # case 20:
            mobid = 9300200
            break
            # case 21:
            mobid = 9300201
            break
            # case 22:
            mobid = 9300202
            break
            # case 23:
            mobid = 9300203
            break
            # case 25:
            mobid = 9300204
            break
            # case 26:
            mobid = 9300205
            break
            # case 27:
            mobid = 9300206
            break
            # case 28:
            mobid = 9300207
            break
            # case 29:
            mobid = 9300208
            break
            # case 31:
            mobid = 9300209
            break
            # case 32:
            mobid = 9300210
            break
            # case 33:
            mobid = 9300211
            break
            # case 34:
            mobid = 9300212
            break
            # case 35:
            mobid = 9300213
            break
            # case 37:
            mobid = 9300214
            break
            # case 38:
            mobid = 9300215
            break
            # default:
            return
        if mobid != 0:
            rand = Randomizer.nextInt(3)
            Timer.MapTimer.getInstance().schedule(_task_1,3000)

    def run(self) -> None:
        map.spawnMonsterWithEffect(MapleLifeFactory.getMonster(mobid), 15, (rand == 0) ? Event_DojoAgent.point1 : ((rand == 1) ? Event_DojoAgent.point2 : Event_DojoAgent.point3))

