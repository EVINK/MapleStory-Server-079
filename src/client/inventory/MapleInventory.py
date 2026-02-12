"""
MapleInventory - Converted from Java source
Original: client/inventory/MapleInventory.java
Package: client.inventory
"""

from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleInventory:
    """
    Class MapleInventory
    Implements: Iterable<IItem>, Serializable
    """

    def __init__(self, type: Any, slotLimit: int):
        self.inventory = None
        self.slotLimit = 0
        self.type = None
        self.inventory = {}
        self.slotLimit = slotLimit
        self.type = type


    def addSlot(self, slot: int) -> None:
        self.slotLimit = (byte)(self.slotLimit + slot)
        if self.slotLimit > 96:
        self.slotLimit = 96

    def getSlotLimit(self) -> int:
        return self.slotLimit

    def setSlotLimit(self, slot: int) -> None:
        if slot > 96:
        slot = 96
        self.slotLimit = slot

    def findById(self, itemId: int) -> Any:
        for item in self.inventory.values():
            if item.getItemId() == itemId:
            return item
        return None

    def findByUniqueId(self, itemId: int) -> Any:
        for item in self.inventory.values():
            if item.getUniqueId() == itemId:
            return item
        return None

    def countById(self, itemId: int) -> int:
        possesed = 0
        for item in self.inventory.values():
            if item.getItemId() == itemId:
            possesed += item.getQuantity()
        return possesed

    def listById(self, itemId: int) -> list:
        ret = []
        for item in self.inventory.values():
            if item.getItemId() == itemId:
            ret.add(item)
        if ret > 1:
        Collections.sort(ret)
        return ret

    def list(self) -> list:
        return self.inventory.values()

    def addItem(self, item: Any) -> int:
        slotId = getNextFreeSlot()
        if slotId < 0:
        return -1
        self.inventory.put(Short.valueOf(slotId), item)
        item.setPosition(slotId)
        return slotId

    def addFromDB(self, item: Any) -> None:
        if item.getPosition() < 0 && !self.type == (MapleInventoryType.EQUIPPED):
        return
        self.inventory.put(Short.valueOf(item.getPosition()), item)

    def move(self, sSlot: int, dSlot: int, slotMax: int) -> None:
        if dSlot > self.slotLimit:
        return
        source = self.inventory.get(Short.valueOf(sSlot))
        target = self.inventory.get(Short.valueOf(dSlot))
        if source is None:
        raise InventoryException("Trying to move empty slot")
        if target is None:
            source.setPosition(dSlot)
            self.inventory.put(Short.valueOf(dSlot), source)
            self.inventory.remove(Short.valueOf(sSlot))
        elif target.getItemId() == source.getItemId() && !GameConstants.isThrowingStar(source.getItemId()) && !GameConstants.isBullet(source.getItemId()) && target.getOwner() == (source.getOwner()) && target.getExpiration() == source.getExpiration():
            if self.type.getType() == MapleInventoryType.EQUIP.getType() || self.type.getType() == MapleInventoryType.CASH.getType():
                swap(target, source)
            elif source.getQuantity() + target.getQuantity() > slotMax:
                source.setQuantity((short)(source.getQuantity() + target.getQuantity() - slotMax))
                target.setQuantity(slotMax)
            else:
                target.setQuantity((short)(source.getQuantity() + target.getQuantity()))
                self.inventory.remove(Short.valueOf(sSlot))
        else:
            swap(target, source)

    def swap(self, source: Any, target: Any) -> None:
        self.inventory.remove(Short.valueOf(source.getPosition()))
        self.inventory.remove(Short.valueOf(target.getPosition()))
        swapPos = source.getPosition()
        source.setPosition(target.getPosition())
        target.setPosition(swapPos)
        self.inventory.put(Short.valueOf(source.getPosition()), source)
        self.inventory.put(Short.valueOf(target.getPosition()), target)

    def getItem(self, slot: int) -> Any:
        return self.inventory.get(Short.valueOf(slot))

    def removeItem(self, slot: int) -> None:
        removeItem(slot, 1, False)

    def removeItem_slot_quantity_allowZero(self, slot: int, quantity: int, allowZero: bool) -> None:
        removeItem(slot, quantity, allowZero, None)

    def removeItem_slot_quantity_allowZero_chr(self, slot: int, quantity: int, allowZero: bool, chr: Any) -> None:
        item = self.inventory.get(Short.valueOf(slot))
        if item is None:
        return
        item.setQuantity((short)(item.getQuantity() - quantity))
        if item.getQuantity() < 0:
        item.setQuantity(0)
        if item.getQuantity() == 0 && !allowZero:
        removeSlot(slot)
        if chr is not None:
            chr.getClient().sendPacket(MaplePacketCreator.modifyInventory(False, ModifyInventory(ModifyInventory.Types.REMOVE, item)))
            chr.dropMessage(5, "期限道具[" + MapleItemInformationProvider.getInstance().getName(item.getItemId()) + "]已经过期")

    def removeSlot(self, slot: int) -> None:
        self.inventory.remove(Short.valueOf(slot))

    def isFull(self) -> bool:
        return (self.inventory >= self.slotLimit)

    def isFull_margin(self, margin: int) -> bool:
        return (self.inventory + margin >= self.slotLimit)

    def getNextFreeSlot(self) -> int:
        if isFull():
        return -1
        i = 1
        while i <= self.slotLimit:
            if !self.inventory.keys().__contains__(Short.valueOf(i)):
            return i
        return -1

    def getNumFreeSlot(self) -> int:
        if isFull():
        return 0
        free = 0
        i = 1
        while i <= self.slotLimit:
            if !self.inventory.keys().__contains__(Short.valueOf(i)):
            free = (byte)(free + 1)
        return free

    def getType(self) -> Any:
        return self.type

    def iterator(self) -> iter:
        return Collections.<IItem>unmodifiableCollection(self.inventory.values()).iterator()

    def listByEquipOnlyId(self, equipOnlyId: int) -> list:
        ret = []
        for item in self.inventory.values():
            if item.getEquipOnlyId() > 0 && item.getEquipOnlyId() == equipOnlyId:
            ret.add(item)
        if ret > 1:
        Collections.sort(ret)
        return ret

    def findByEquipOnlyId(self, onlyId: int, itemId: int) -> Any:
        for item in self.inventory.values():
            if item.getEquipOnlyId() == onlyId && item.getItemId() == itemId:
            return item
        return None

