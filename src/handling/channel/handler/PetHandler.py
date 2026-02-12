"""
PetHandler - Converted from Java source
Original: handling/channel/handler/PetHandler.java
Package: handling.channel.handler
"""

from threading import Lock
from typing import List
from typing import Optional, Any
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.PetCommand import *  # TODO: import specific classes
# from client.inventory.PetDataFactory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleMapItem import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes


class PetHandler:
    """
    Class PetHandler
    """


    def PickExceptionList(self, slea: Any, c: Any, chr: Any) -> None:
        if chr is None or chr.getMap() is None:
            return
        itemid = slea.readInt()
        if not chr.haveItem(itemid):
            c.getSession().write(MaplePacketCreator.enableActions())

    def SpawnPet(self, slea: Any, c: Any, chr: Any) -> None:
        chr.updateTick(slea.readInt())
        chr.spawnPet(slea.readByte(), slea.readByte() > 0)

    def Pet_AutoPotion(self, slea: Any, c: Any, chr: Any) -> None:
        slea.skip(13)
        slot = slea.readByte()
        if chr is None or not chr.isAlive() or chr.getMapId() == 749040100 or chr.getMap() is None or chr.hasDisease(MapleDisease.POTION):
            return
        toUse = chr.getInventory(MapleInventoryType.USE).getItem(slot)
        if toUse is None or toUse.getQuantity() < 1:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        time = int(time.time() * 1000)
        if chr.getNextConsume() > time:
            chr.dropMessage(5, "你可能不使用这个项目.")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if not FieldLimitType.PotionUse.check(chr.getMap().getFieldLimit()) or chr.getMapId() == 610030600:
            if MapleItemInformationProvider.getInstance().getItemEffect(toUse.getItemId()).applyTo(chr):
                MapleInventoryManipulator.removeFromSlot(c, MapleInventoryType.USE, slot, 1, False)
                if chr.getMap().getConsumeItemCoolTime() > 0:
                    chr.setNextConsume(time + chr.getMap().getConsumeItemCoolTime() * 1000)
        else:
            c.getSession().write(MaplePacketCreator.enableActions())

    def PetChat(self, petid: int, command: int, text: str, chr: Any) -> None:
        if chr is None or chr.getMap() is None or chr.getPetIndex(petid) < 0:
            return
        chr.getMap().broadcastMessage(chr, PetPacket.petChat(chr.getId(), command, text, chr.getPetIndex(petid)), True)

    def PetCommand(self, slea: Any, c: Any, chr: Any) -> None:
        petIndex = chr.getPetIndex(slea.readInt())
        if petIndex == -1:
            return
        pet = chr.getPet(petIndex)
        if pet is None:
            return
        slea.skip(5)
        command = slea.readByte()
        petCommand = PetDataFactory.getPetCommand(pet.getPetItemId(), command)
        success = False
        if Randomizer.nextInt(99) <= petCommand.getProbability():
            success = True
            if pet.getCloseness() < 30000:
                newCloseness = pet.getCloseness() + petCommand.getIncrease()
                if newCloseness > 30000:
                    newCloseness = 30000
                pet.setCloseness(newCloseness)
                if newCloseness >= GameConstants.getClosenessNeededForLevel(pet.getLevel() + 1):
                    pet.setLevel(pet.getLevel() + 1)
                    c.getSession().write(PetPacket.showOwnPetLevelUp(petIndex))
                    chr.getMap().broadcastMessage(PetPacket.showPetLevelUp(chr, petIndex))
                c.getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
        chr.getMap().broadcastMessage(chr, PetPacket.commandResponse(chr.getId(), command, petIndex, success, False), True)

    def PetFood(self, slea: Any, c: Any, chr: Any) -> None:
        previousFullness = 100
        pet = None
        if chr is None:
            return
        for pets in chr.getPets():
            if pets.getSummoned() and pets.getFullness() < previousFullness:
                previousFullness = pets.getFullness()
                pet = pets
        if pet is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        slea.skip(6)
        itemId = slea.readInt()
        gainCloseness = False
        if Randomizer.nextInt(99) <= 50:
            gainCloseness = True
        if pet.getFullness() < 100:
            newFullness = pet.getFullness() + 30
            if newFullness > 100:
                newFullness = 100
            pet.setFullness(newFullness)
            index = chr.getPetIndex(pet)
            if gainCloseness and pet.getCloseness() < 30000:
                newCloseness = pet.getCloseness() + 1
                if newCloseness > 30000:
                    newCloseness = 30000
                pet.setCloseness(newCloseness)
                if newCloseness >= GameConstants.getClosenessNeededForLevel(pet.getLevel() + 1):
                    pet.setLevel(pet.getLevel() + 1)
                    c.getSession().write(PetPacket.showOwnPetLevelUp(index))
                    chr.getMap().broadcastMessage(PetPacket.showPetLevelUp(chr, index))
            c.getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
            chr.getMap().broadcastMessage(c.getPlayer(), PetPacket.commandResponse(chr.getId(), 1, index, True, True), True)
        else:
            if gainCloseness:
                newCloseness2 = pet.getCloseness() - 1
                if newCloseness2 < 0:
                    newCloseness2 = 0
                pet.setCloseness(newCloseness2)
                if newCloseness2 < GameConstants.getClosenessNeededForLevel(pet.getLevel()):
                    pet.setLevel(pet.getLevel() - 1)
            c.getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
            chr.getMap().broadcastMessage(chr, PetPacket.commandResponse(chr.getId(), 1, chr.getPetIndex(pet), False, True), True)
        MapleInventoryManipulator.removeById(c, MapleInventoryType.USE, itemId, 1, True, False)
        c.getSession().write(MaplePacketCreator.enableActions())

    def MovePet(self, slea: Any, chr: Any) -> None:
        petId = slea.readInt()
        slea.skip(8)
        res = MovementParse.parseMovement(slea, 3)
        if res is not None and chr is not None and res != 0:
            slot = chr.getPetIndex(petId)
            if slot == -1:
                return
            chr.getPet(slot).updatePosition(res)
            chr.getMap().broadcastMessage(chr, PetPacket.movePet(chr.getId(), petId, slot, res), False)
            if chr.getPlayerShop() is not None or chr.getConversation() > 0 or chr.getTrade() is not None:
                return
            if chr.getStat().hasVac and (chr.getStat().hasMeso or chr.getStat().hasItem):
                objects = chr.getMap().getAllItems()
                for mapitem in objects:
                    lock = mapitem.getLock()
                    lock.lock()
                    try:
                        if mapitem.isPickedUp():
                            continue
                        if mapitem.getOwner() != chr.getId() and mapitem.isPlayerDrop():
                            continue
                        if mapitem.getOwner() != chr.getId() and ((not mapitem.isPlayerDrop() and mapitem.getDropType() == 0) or (mapitem.isPlayerDrop() and chr.getMap().getEverlast())):
                            continue
                        if not mapitem.isPlayerDrop() and mapitem.getDropType() == 1 and mapitem.getOwner() != chr.getId() and (chr.getParty() is None or chr.getParty().getMemberById(mapitem.getOwner()) is None):
                            continue
                        if mapitem.getMeso() > 0 and chr.getStat().hasMeso:
                            if chr.getParty() is not None and mapitem.getOwner() != chr.getId():
                                toGive = []
                                for mem in chr.getParty().getMembers():
                                    m = chr.getMap().getCharacterById(mem.getId())
                                    if m is not None:
                                        toGive.add(m)
                                for i in toGive:
                                    i.gainMeso(mapitem.getMeso() / toGive + (i.getStat().hasPartyBonus ? ((int)(mapitem.getMeso() / 20.0)) : 0), True, True)
                            else:
                                chr.gainMeso(mapitem.getMeso(), True, True)
                            InventoryHandler.removeItem_Pet(chr, mapitem, slot)
                        else:
                            if not chr.getStat().hasItem or not MapleItemInformationProvider.getInstance().isPickupBlocked(mapitem.getItem().getItemId()):
                                continue
                            if InventoryHandler.useItem(chr.getClient(), mapitem.getItemId()):
                                InventoryHandler.removeItem_Pet(chr, mapitem, slot)
                            else:
                                if not MapleInventoryManipulator.checkSpace(chr.getClient(), mapitem.getItem().getItemId(), mapitem.getItem().getQuantity(), mapitem.getItem().getOwner()):
                                    continue
                                if mapitem.getItem().getQuantity() >= 50 and GameConstants.isUpgradeScroll(mapitem.getItem().getItemId()):
                                    chr.getClient().setMonitored(True)
                                if not MapleInventoryManipulator.addFromDrop(chr.getClient(), mapitem.getItem(), True, mapitem.getDropper() instanceof MapleMonster):
                                    continue
                                InventoryHandler.removeItem_Pet(chr, mapitem, slot)
                    finally:
                        lock.unlock()

