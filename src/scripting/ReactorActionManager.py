"""
ReactorActionManager - Converted from Java source
Original: scripting/ReactorActionManager.java
Package: scripting
"""

from typing import Iterator
from typing import List
from typing import Optional, Any
import math
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.MapleCarnivalFactory import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.maps.ReactorDropEntry import *  # TODO: import specific classes


class ReactorActionManager(AbstractPlayerInteraction):
    """
    Class ReactorActionManager
    Extends: AbstractPlayerInteraction
    """

    def __init__(self, c: Any, reactor: Any):
        self.reactor = None
        super(c)
        self.reactor = reactor


    def dropItems(self) -> None:
        self.dropItems(False, 0, 0, 0, 0)

    def dropItems_meso_mesoChance_minMeso_maxMeso(self, meso: bool, mesoChance: int, minMeso: int, maxMeso: int) -> None:
        self.dropItems(meso, mesoChance, minMeso, maxMeso, 0)

    def dropItems_meso_mesoChance_minMeso_maxMeso_minItems(self, meso: bool, mesoChance: int, minMeso: int, maxMeso: int, minItems: int) -> None:
        chances = ReactorScriptManager.getInstance().getDrops(self.reactor.getReactorId())
        items = []
        if meso && random.random() < 1.0 / mesoChance:
            items.add(ReactorDropEntry(0, mesoChance, -1))
        numItems = 0
        for d in chances:
            count = 1.0 / d.chance
            if random.random() < 1.0 / d.chance && (d.questid <= 0 || self.getPlayer().getQuestStatus(d.questid) == 1):
                numItems += 1
                items.add(d)
        while items < minItems:
            items.add(ReactorDropEntry(0, mesoChance, -1))
            numItems += 1
        position = None
        dropPos = position = self.reactor.getPosition()
        position.x -= 12 * numItems
        ii = MapleItemInformationProvider.getInstance()
        for d2 in items:
            if d2.itemId == 0:
                range = maxMeso - minMeso
                mesoDrop = Randomizer.nextInt(range) + minMeso * ChannelServer.getInstance(self.getClient().getChannel()).getMesoRate()
                self.reactor.getMap().spawnMesoDrop(mesoDrop, dropPos, self.reactor, self.getPlayer(), False, 0)
            else:
                drop = None
                if GameConstants.getInventoryType(d2.itemId) != MapleInventoryType.EQUIP:
                    drop = Item(d2.itemId, 0, 1, 0)
                else:
                    drop = ii.randomizeStats(ii.getEquipById(d2.itemId))
                self.reactor.getMap().spawnItemDrop(self.reactor, self.getPlayer(), drop, dropPos, False, False)
            point = dropPos
            point.x += 25

    def spawnNpc(self, npcId: int) -> None:
        self.spawnNpc(npcId, self.getPosition())

    def getPosition(self) -> Any:
        position = None
        pos = position = self.reactor.getPosition()
        position.y -= 10
        return pos

    def getReactor(self) -> Any:
        return self.reactor

    def spawnZakum(self) -> None:
        self.reactor.getMap().spawnZakum(self.getPosition().x, self.getPosition().y)

    def spawnFakeMonster(self, id: int) -> None:
        self.spawnFakeMonster(id, 1, self.getPosition())

    def spawnFakeMonster_id_x_y(self, id: int, x: int, y: int) -> None:
        self.spawnFakeMonster(id, 1, Point(x, y))

    def spawnFakeMonster_id_qty(self, id: int, qty: int) -> None:
        self.spawnFakeMonster(id, qty, self.getPosition())

    def spawnFakeMonster_id_qty_x_y(self, id: int, qty: int, x: int, y: int) -> None:
        self.spawnFakeMonster(id, qty, Point(x, y))

    def spawnFakeMonster_id_qty_pos(self, id: int, qty: int, pos: Any) -> None:
        for i in range(qty):
            self.reactor.getMap().spawnFakeMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), pos)

    def killAll(self) -> None:
        self.reactor.getMap().killAllMonsters(True)

    def killMonster(self, monsId: int) -> None:
        self.reactor.getMap().killMonster(monsId)

    def spawnMonster(self, id: int) -> None:
        self.spawnMonster(id, 1, self.getPosition())

    def spawnMonster_id_qty(self, id: int, qty: int) -> None:
        self.spawnMonster(id, qty, self.getPosition())

    def dispelAllMonsters(self, num: int) -> None:
        final MapleCarnivalFactory.MCSkill skil = MapleCarnivalFactory.getInstance().getGuardian(num)
        if skil is not None:
            for mons in self.getMap().getAllMonstersThreadsafe():
                mons.dispelSkill(skil.getSkill())

