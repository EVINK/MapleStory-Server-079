"""
MapleInventoryManipulator - Converted from Java source
Original: server/MapleInventoryManipulator.java
Package: server
"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import math
import time

# Internal module imports
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.InventoryException import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.ModifyInventory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class MapleInventoryManipulator:
    """
    Class MapleInventoryManipulator
    """


    def addRing(self, chr: Any, itemId: int, ringId: int, sn: int) -> None:
        csi = CashItemFactory.getInstance().getItem(sn)
        if csi is None:
            return
        ring = chr.getCashInventory().toItem(csi, ringId)
        if ring is None || ring.getUniqueId() != ringId || ring.getUniqueId() <= 0 || ring.getItemId() != itemId:
            return
        chr.getCashInventory().addToInventory(ring)
        chr.getClient().getSession().write(MTSCSPacket.showBoughtCSItem(ring, sn, chr.getClient().getAccID()))

    def addbyItem(self, c: Any, item: Any) -> bool:
        return addbyItem(c, item, False) >= 0

    def addbyItem_c_item_fromcs(self, c: Any, item: Any, fromcs: bool) -> int:
        type = GameConstants.getInventoryType(item.getItemId())
        newSlot = c.getPlayer().getInventory(type).addItem(item)
        if newSlot == -1:
            if !fromcs:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
            return newSlot
        if !fromcs:
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, item))
        c.getPlayer().havePartyQuest(item.getItemId())
        if !fromcs && type == (MapleInventoryType.EQUIP):
            c.getPlayer().checkCopyItems()
        return newSlot

    def gainItemPeriod(self, c: Any, id: int, quantity: int, period: int) -> None:
        gainItem(c, id, quantity, False, period, -1, "", 0)

    def gainItemPeriod_c_id_quantity_period_owner(self, c: Any, id: int, quantity: int, period: int, owner: str) -> None:
        gainItem(c, id, quantity, False, period, -1, owner, 0)

    def gainItem(self, c: Any, id: int, quantity: int) -> None:
        gainItem(c, id, quantity, False, 0, -1, "", 0)

    def gainItem_c_id_quantity_period_Flag(self, c: Any, id: int, quantity: int, period: int, Flag: int) -> None:
        gainItem(c, id, quantity, False, period, -1, "", Flag)

    def gainItem_c_id_quantity_randomStats(self, c: Any, id: int, quantity: int, randomStats: bool) -> None:
        gainItem(c, id, quantity, randomStats, 0, -1, "", 0)

    def gainItem_c_id_quantity_randomStats_slots(self, c: Any, id: int, quantity: int, randomStats: bool, slots: int) -> None:
        gainItem(c, id, quantity, randomStats, 0, slots, "", 0)

    def gainItem_c_id_quantity_period(self, c: Any, id: int, quantity: int, period: int) -> None:
        gainItem(c, id, quantity, False, period, -1, "", 0)

    def gainItem_c_id_quantity_randomStats_period_slots(self, c: Any, id: int, quantity: int, randomStats: bool, period: int, slots: int) -> None:
        gainItem(c, id, quantity, randomStats, period, slots, "", 0)

    def gainItem_c_id_quantity_randomStats_period_slots_owner_Flag(self, c: Any, id: int, quantity: int, randomStats: bool, period: int, slots: int, owner: str, Flag: int) -> None:
        gainItem(id, quantity, randomStats, period, slots, owner, c, Flag)

    def gainItem_id_quantity_randomStats_period_slots_owner_cg_Flag(self, id: int, quantity: int, randomStats: bool, period: int, slots: int, owner: str, cg: Any, Flag: int) -> None:
        if quantity >= 0:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(id)
            if !checkSpace(cg, id, quantity, ""):
                return
            if type == (MapleInventoryType.EQUIP) && !GameConstants.is飞镖道具(id) && !GameConstants.is子弹道具(id):
                item = (Equip)(randomStats ? ii.randomizeStats(ii.getEquipById(id)) : ii.getEquipById(id))
                if period > 0:
                    item.setExpiration(int(time.time() * 1000) + period * 60 * 60 * 1000)
                if slots > 0:
                    item.setUpgradeSlots((byte)(item.getUpgradeSlots() + slots))
                if owner is not None:
                    item.setOwner(owner)
                name = ii.getName(id)
                if id / 10000 == 114 && name is not None && name > 0:
                    msg = "你已获得称号 <" + name + ">"
                    cg.getPlayer().dropMessage(5, msg)
                    cg.getPlayer().dropMessage(5, msg)
                addbyItem(cg, item.copy())
            else:
                addById(cg, id, quantity, (owner is None) ? "" : owner, None, period, Flag)
        else:
            removeById(cg, GameConstants.getInventoryType(id), id, -quantity, True, False)

    def getUniqueId(self, itemId: int, pet: Any) -> int:
        uniqueid = -1
        if GameConstants.isPet(itemId):
            if pet is not None:
                uniqueid = pet.getUniqueId()
            else:
                uniqueid = MapleInventoryIdentifier.getInstance()
        elif GameConstants.getInventoryType(itemId) == MapleInventoryType.CASH || MapleItemInformationProvider.getInstance().isCash(itemId):
            uniqueid = MapleInventoryIdentifier.getInstance()
        return uniqueid

    def addById(self, c: Any, itemId: int, quantity: int, Flag: int) -> bool:
        return addById(c, itemId, quantity, None, None, 0, Flag)

    def addById_c_itemId_quantity_owner_Flag(self, c: Any, itemId: int, quantity: int, owner: str, Flag: int) -> bool:
        return addById(c, itemId, quantity, owner, None, 0, Flag)

    def addId(self, c: Any, itemId: int, quantity: int, owner: str, Flag: int) -> int:
        return addId(c, itemId, quantity, owner, None, 0, Flag)

    def addId_c_itemId_quantity_owner_period_Flag(self, c: Any, itemId: int, quantity: int, owner: str, period: int, Flag: int) -> int:
        return addId(c, itemId, quantity, owner, None, period, Flag)

    def addById_c_itemId_quantity_owner_pet_Flag(self, c: Any, itemId: int, quantity: int, owner: str, pet: Any, Flag: int) -> bool:
        return addById(c, itemId, quantity, owner, pet, 0, Flag)

    def addById_c_itemId_quantity_owner_pet_period_Flag(self, c: Any, itemId: int, quantity: int, owner: str, pet: Any, period: int, Flag: int) -> bool:
        return addId(c, itemId, quantity, owner, pet, period, Flag) >= 0

    def addId_c_itemId_quantity_owner_pet_period_Flag(self, c: Any, itemId: int, quantity: int, owner: str, pet: Any, period: int, Flag: int) -> int:
        ii = MapleItemInformationProvider.getInstance()
        if ii.isPickupRestricted(itemId) && c.getPlayer().haveItem(itemId, 1, True, False):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            c.getSession().write(MaplePacketCreator.showItemUnavailable())
            return -1
        type = GameConstants.getInventoryType(itemId)
        uniqueid = getUniqueId(itemId, pet)
        newSlot = -1
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, itemId)
            existing = c.getPlayer().getInventory(type).listById(itemId)
            if !GameConstants.isRechargable(itemId):
                if existing > 0:
                    i = existing.iterator()
                    while (quantity > 0 &&
                    i.hasNext())
                        eItem = i.next()
                        oldQ = eItem.getQuantity()
                        if oldQ < slotMax && (eItem.getOwner() == (owner) || owner is None) && eItem.getExpiration() == -1:
                            newQ = min(oldQ + quantity, slotMax)
                            quantity = (short)(quantity - newQ - oldQ)
                            eItem.setQuantity(newQ)
                            c.getSession().write(MaplePacketCreator.updateInventorySlot(type, eItem, False))
                while quantity > 0:
                    newQ = min(quantity, slotMax)
                    if newQ != 0:
                        quantity = (short)(quantity - newQ)
                        nItem = Item(itemId, 0, newQ, 0, uniqueid)
                        newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                        if newSlot == -1:
                            c.getSession().write(MaplePacketCreator.getInventoryFull())
                            c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                            return -1
                        if owner is not None:
                        nItem.setOwner(owner)
                        if Flag > 0 && ii.isCash(nItem.getItemId()):
                            flag = nItem.getFlag()
                            flag = (byte)(flag | ItemFlag.KARMA_EQ.getValue())
                            nItem.setFlag(flag)
                        if period > 0:
                        nItem.setExpiration(int(time.time() * 1000) + period * 60 * 60 * 1000)
                        if pet is not None:
                            nItem.setPet(pet)
                            pet.setInventoryPosition(newSlot)
                            c.getPlayer().addPet(pet)
                        c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                        if GameConstants.isRechargable(itemId) && quantity == 0:
                        break
                        continue
                    c.getPlayer().havePartyQuest(itemId)
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return newSlot
            else:
                nItem = Item(itemId, 0, quantity, 0, uniqueid)
                newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                if newSlot == -1:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return -1
                if period > 0:
                nItem.setExpiration(int(time.time() * 1000) + period * 60 * 60 * 1000)
                c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                c.getSession().write(MaplePacketCreator.enableActions())
        elif quantity == 1:
            nEquip = ii.getEquipById(itemId)
            if owner is not None:
            nEquip.setOwner(owner)
            nEquip.setUniqueId(uniqueid)
            if Flag > 0 && ii.isCash(nEquip.getItemId()):
                flag = nEquip.getFlag()
                flag = (byte)(flag | ItemFlag.KARMA_USE.getValue())
                nEquip.setFlag(flag)
            if period > 0:
            nEquip.setExpiration(int(time.time() * 1000) + period * 60 * 60 * 1000)
            newSlot = c.getPlayer().getInventory(type).addItem(nEquip)
            if newSlot == -1:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                return -1
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, nEquip))
            c.getPlayer().checkCopyItems()
        else:
            raise InventoryException("Trying to create equip with non-one quantity")
        c.getPlayer().havePartyQuest(itemId)
        return newSlot

    def addbyId_Gachapon(self, c: Any, itemId: int, quantity: int) -> Any:
        return addbyId_Gachapon(c, itemId, quantity, None, 0)

    def addbyId_Gachapon_c_itemId_quantity_gmLog(self, c: Any, itemId: int, quantity: int, gmLog: str) -> Any:
        return addbyId_Gachapon(c, itemId, quantity, None, 0)

    def addbyId_Gachapon_c_itemId_quantity_gmLog_period(self, c: Any, itemId: int, quantity: int, gmLog: str, period: int) -> Any:
        if c.getPlayer().getInventory(MapleInventoryType.EQUIP).getNextFreeSlot() == -1 || c.getPlayer().getInventory(MapleInventoryType.USE).getNextFreeSlot() == -1 || c.getPlayer().getInventory(MapleInventoryType.ETC).getNextFreeSlot() == -1 || c.getPlayer().getInventory(MapleInventoryType.SETUP).getNextFreeSlot() == -1:
            return None
        ii = MapleItemInformationProvider.getInstance()
        if ii.isPickupRestricted(itemId) && c.getPlayer().haveItem(itemId, 1, True, False):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            c.getSession().write(MaplePacketCreator.showItemUnavailable())
            return None
        type = GameConstants.getInventoryType(itemId)
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, itemId)
            existing = c.getPlayer().getInventory(type).listById(itemId)
            if !GameConstants.isRechargable(itemId):
                nItem = None
                recieved = False
                if existing > 0:
                    i = existing.iterator()
                    while quantity > 0 && i.hasNext():
                        nItem = i.next()
                        oldQ = nItem.getQuantity()
                        if oldQ < slotMax:
                            recieved = True
                            newQ = min(oldQ + quantity, slotMax)
                            quantity -= (short)(newQ - oldQ)
                            nItem.setQuantity(newQ)
                            c.getSession().write(MaplePacketCreator.updateInventorySlot(type, nItem, False))
                while quantity > 0:
                    newQ2 = min(quantity, slotMax)
                    if newQ2 == 0:
                        break
                    quantity -= newQ2
                    nItem = Item(itemId, 0, newQ2, 0)
                    newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                    if newSlot == -1 && recieved:
                        return nItem
                    if newSlot == -1:
                        return None
                    recieved = True
                    if gmLog is not None:
                        nItem.setGMLog(gmLog)
                    if period > 0:
                        if period < 1000:
                            nItem.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
                        else:
                            nItem.setExpiration(int(time.time() * 1000) + period)
                    c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                    if GameConstants.isRechargable(itemId) && quantity == 0:
                        break
                if recieved:
                    c.getPlayer().havePartyQuest(nItem.getItemId())
                    return nItem
                return None
            else:
                nItem2 = Item(itemId, 0, quantity, 0)
                newSlot2 = c.getPlayer().getInventory(type).addItem(nItem2)
                if newSlot2 == -1:
                    return None
                c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem2))
                c.getPlayer().havePartyQuest(nItem2.getItemId())
                return nItem2
        else:
            if quantity != 1:
                raise InventoryException("Trying to create equip with non-one quantity")
            item = ii.randomizeStats(ii.getEquipById(itemId))
            newSlot3 = c.getPlayer().getInventory(type).addItem(item)
            if newSlot3 == -1:
                return None
            if gmLog is not None:
                item.setGMLog(gmLog)
            if period > 0:
                if period < 1000:
                    item.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
                else:
                    item.setExpiration(int(time.time() * 1000) + period)
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, item, True))
            c.getPlayer().havePartyQuest(item.getItemId())
            return item

    def addFromDrop(self, c: Any, item: Any, show: bool) -> bool:
        return addFromDrop(c, item, show, False)

    def addFromDrop_c_item_show_enhance(self, c: Any, item: Any, show: bool, enhance: bool) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        if ii.isPickupRestricted(item.getItemId()) && c.getPlayer().haveItem(item.getItemId(), 1, True, False):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            c.getSession().write(MaplePacketCreator.showItemUnavailable())
            return False
        before = c.getPlayer().itemQuantity(item.getItemId())
        quantity = item.getQuantity()
        type = GameConstants.getInventoryType(item.getItemId())
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, item.getItemId())
            existing = c.getPlayer().getInventory(type).listById(item.getItemId())
            if !GameConstants.isRechargable(item.getItemId()):
                if quantity <= 0:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.showItemUnavailable())
                    return False
                if existing > 0:
                    i = existing.iterator()
                    while (quantity > 0 &&
                    i.hasNext())
                        eItem = i.next()
                        oldQ = eItem.getQuantity()
                        if oldQ < slotMax && item.getOwner() == (eItem.getOwner()) && item.getExpiration() == eItem.getExpiration():
                            newQ = min(oldQ + quantity, slotMax)
                            quantity = (short)(quantity - newQ - oldQ)
                            eItem.setQuantity(newQ)
                            c.getSession().write(MaplePacketCreator.updateInventorySlot(type, eItem, True))
                while quantity > 0:
                    newQ = min(quantity, slotMax)
                    quantity = (short)(quantity - newQ)
                    nItem = Item(item.getItemId(), 0, newQ, item.getFlag())
                    nItem.setExpiration(item.getExpiration())
                    nItem.setOwner(item.getOwner())
                    nItem.setPet(item.getPet())
                    newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                    if newSlot == -1:
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        item.setQuantity((short)(quantity + newQ))
                        return False
                    c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem, True))
            else:
                nItem = Item(item.getItemId(), 0, quantity, item.getFlag())
                nItem.setExpiration(item.getExpiration())
                nItem.setOwner(item.getOwner())
                nItem.setPet(item.getPet())
                newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                if newSlot == -1:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return False
                c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                c.getSession().write(MaplePacketCreator.enableActions())
        elif quantity == 1:
            if enhance:
            item = checkEnhanced(item, c.getPlayer())
            newSlot = c.getPlayer().getInventory(type).addItem(item)
            if newSlot == -1:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                return False
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, item, True))
            c.getPlayer().checkCopyItems()
        else:
            raise RuntimeError("Trying to create equip with non-one quantity")
        if item.getQuantity() >= 50 && GameConstants.isUpgradeScroll(item.getItemId()):
        c.setMonitored(True)
        if before == 0:
        # switch (item.getItemId()):
            # case 4031875:
            c.getPlayer().dropMessage(5, "You have gained a Powder Keg, you can give this in to Aramia of Henesys.")
            break
            # case 4001246:
            c.getPlayer().dropMessage(5, "You have gained a Warm Sun, you can give this in to Maple Tree Hill through @joyce.")
            break
            # case 4001473:
            c.getPlayer().dropMessage(5, "You have gained a Tree Decoration, you can give this in to White Christmas Hill through @joyce.")
            break
        c.getPlayer().havePartyQuest(item.getItemId())
        if show:
        c.getSession().write(MaplePacketCreator.getShowItemGain(item.getItemId(), item.getQuantity()))
        return True

    def translated_商店防止复制(self, c: Any, item: Any, show: bool) -> bool:
        return 商店防止复制(c, item, show, False)

    def translated_商店防止复制_c_item_show_enhance(self, c: Any, item: Any, show: bool, enhance: bool) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        if ii.isPickupRestricted(item.getItemId()) && c.getPlayer().haveItem(item.getItemId(), 1, True, False):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            c.getSession().write(MaplePacketCreator.showItemUnavailable())
            return False
        before = c.getPlayer().itemQuantity(item.getItemId())
        quantity = item.getQuantity()
        type = GameConstants.getInventoryType(item.getItemId())
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, item.getItemId())
            existing = c.getPlayer().getInventory(type).listById(item.getItemId())
            if !GameConstants.isRechargable(item.getItemId()):
                if quantity <= 0:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.showItemUnavailable())
                    return False
                if existing > 0:
                    i = existing.iterator()
                    while (quantity > 0 &&
                    i.hasNext())
                        eItem = i.next()
                        oldQ = eItem.getQuantity()
                        if oldQ < slotMax && item.getOwner() == (eItem.getOwner()) && item.getExpiration() == eItem.getExpiration() && slotMax <= slotMax - oldQ:
                            newQ = min(oldQ + quantity, slotMax)
                            quantity = (short)(quantity - newQ - oldQ)
                            eItem.setQuantity(newQ)
                            c.getSession().write(MaplePacketCreator.updateInventorySlot(type, eItem, True))
                while quantity > 0:
                    newQ = min(quantity, slotMax)
                    quantity = (short)(quantity - newQ)
                    nItem = Item(item.getItemId(), 0, newQ, item.getFlag())
                    nItem.setExpiration(item.getExpiration())
                    nItem.setOwner(item.getOwner())
                    nItem.setPet(item.getPet())
                    newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                    if newSlot == -1:
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        item.setQuantity((short)(quantity + newQ))
                        return False
                    c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem, True))
            else:
                nItem = Item(item.getItemId(), 0, quantity, item.getFlag())
                nItem.setExpiration(item.getExpiration())
                nItem.setOwner(item.getOwner())
                nItem.setPet(item.getPet())
                newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                if newSlot == -1:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return False
                c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                c.getSession().write(MaplePacketCreator.enableActions())
        elif quantity == 1:
            if enhance:
            item = checkEnhanced(item, c.getPlayer())
            newSlot = c.getPlayer().getInventory(type).addItem(item)
            if newSlot == -1:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                return False
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, item, True))
        else:
            raise RuntimeError("Trying to create equip with non-one quantity")
        if item.getQuantity() >= 50 && GameConstants.isUpgradeScroll(item.getItemId()):
        c.setMonitored(True)
        if before == 0:
        # switch (item.getItemId()):
            # case 4031875:
            c.getPlayer().dropMessage(5, "You have gained a Powder Keg, you can give this in to Aramia of Henesys.")
            break
            # case 4001246:
            c.getPlayer().dropMessage(5, "You have gained a Warm Sun, you can give this in to Maple Tree Hill through @joyce.")
            break
            # case 4001473:
            c.getPlayer().dropMessage(5, "You have gained a Tree Decoration, you can give this in to White Christmas Hill through @joyce.")
            break
        c.getPlayer().havePartyQuest(item.getItemId())
        if show:
        c.getSession().write(MaplePacketCreator.getShowItemGain(item.getItemId(), item.getQuantity()))
        return True

    def pet_addFromDrop(self, c: Any, item: Any, show: bool, enhance: bool) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        if ii.isPickupRestricted(item.getItemId()) && c.getPlayer().haveItem(item.getItemId(), 1, True, False):
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            c.getSession().write(MaplePacketCreator.showItemUnavailable())
            return False
        before = c.getPlayer().itemQuantity(item.getItemId())
        quantity = item.getQuantity()
        type = GameConstants.getInventoryType(item.getItemId())
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, item.getItemId())
            existing = c.getPlayer().getInventory(type).listById(item.getItemId())
            if !GameConstants.isRechargable(item.getItemId()):
                if quantity <= 0:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.showItemUnavailable())
                    return False
                if existing > 0:
                    i = existing.iterator()
                    while (quantity > 0 &&
                    i.hasNext())
                        eItem = i.next()
                        oldQ = eItem.getQuantity()
                        if oldQ < slotMax && item.getOwner() == (eItem.getOwner()) && item.getExpiration() == eItem.getExpiration():
                            newQ = min(oldQ + quantity, slotMax)
                            quantity = (short)(quantity - newQ - oldQ)
                            eItem.setQuantity(newQ)
                            c.getSession().write(MaplePacketCreator.updateInventorySlot(type, eItem, False))
                while quantity > 0:
                    newQ = min(quantity, slotMax)
                    quantity = (short)(quantity - newQ)
                    nItem = Item(item.getItemId(), 0, newQ, item.getFlag())
                    nItem.setExpiration(item.getExpiration())
                    nItem.setOwner(item.getOwner())
                    nItem.setPet(item.getPet())
                    newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                    if newSlot == -1:
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        item.setQuantity((short)(quantity + newQ))
                        return False
                    c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem, False))
            else:
                nItem = Item(item.getItemId(), 0, quantity, item.getFlag())
                nItem.setExpiration(item.getExpiration())
                nItem.setOwner(item.getOwner())
                nItem.setPet(item.getPet())
                newSlot = c.getPlayer().getInventory(type).addItem(nItem)
                if newSlot == -1:
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return False
                c.getSession().write(MaplePacketCreator.addInventorySlot(type, nItem))
                c.getSession().write(MaplePacketCreator.enableActions())
        elif quantity == 1:
            if enhance:
            item = checkEnhanced(item, c.getPlayer())
            newSlot = c.getPlayer().getInventory(type).addItem(item)
            if newSlot == -1:
                c.getSession().write(MaplePacketCreator.getInventoryFull())
                c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                return False
            c.getSession().write(MaplePacketCreator.addInventorySlot(type, item, False))
        else:
            raise RuntimeError("Trying to create equip with non-one quantity")
        if item.getQuantity() >= 50 && GameConstants.isUpgradeScroll(item.getItemId()):
        c.setMonitored(True)
        if before == 0:
        # switch (item.getItemId()):
            # case 4031875:
            c.getPlayer().dropMessage(5, "You have gained a Powder Keg, you can give this in to Aramia of Henesys.")
            break
            # case 4001246:
            c.getPlayer().dropMessage(5, "You have gained a Warm Sun, you can give this in to Maple Tree Hill through @joyce.")
            break
            # case 4001473:
            c.getPlayer().dropMessage(5, "You have gained a Tree Decoration, you can give this in to White Christmas Hill through @joyce.")
            break
        c.getPlayer().havePartyQuest(item.getItemId())
        if show:
        c.getSession().write(MaplePacketCreator.getShowItemGain(item.getItemId(), item.getQuantity()))
        return True

    def checkEnhanced(self, before: Any, chr: Any) -> Any:
        if isinstance(before, Equip):
            eq = before
            if eq.getState() == 0 && (eq.getUpgradeSlots() >= 1 || eq.getLevel() >= 1) && Randomizer.nextInt(100) > 80:
                eq.resetPotential()
        return before

    def rand(self, min: int, max: int) -> int:
        return abs(Randomizer.rand(min, max))

    def checkSpace(self, c: Any, itemid: int, quantity: int, owner: str) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        if c.getPlayer() is None || (ii.isPickupRestricted(itemid) && c.getPlayer().haveItem(itemid, 1, True, False)):
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        if quantity <= 0 && !GameConstants.isRechargable(itemid):
            return False
        type = GameConstants.getInventoryType(itemid)
        if c.getPlayer() is None || c.getPlayer().getInventory(type) is None:
            return False
        if !type == (MapleInventoryType.EQUIP):
            slotMax = ii.getSlotMax(c, itemid)
            existing = c.getPlayer().getInventory(type).listById(itemid)
            if !GameConstants.isRechargable(itemid) && existing > 0:
                for eItem in existing:
                    oldQ = eItem.getQuantity()
                    if oldQ < slotMax && owner is not None && owner == (eItem.getOwner()):
                        newQ = min(oldQ + quantity, slotMax)
                        quantity -= newQ - oldQ
                    if quantity <= 0:
                        break
            numSlotsNeeded = None
            if slotMax > 0 && !GameConstants.isRechargable(itemid):
                numSlotsNeeded = math.ceil(quantity / slotMax)
            else:
                numSlotsNeeded = 1
            return !c.getPlayer().getInventory(type).isFull(numSlotsNeeded - 1)
        return !c.getPlayer().getInventory(type).isFull()

    def removeFromSlot(self, c: Any, type: Any, slot: int, quantity: int, fromDrop: bool) -> None:
        removeFromSlot(c, type, slot, quantity, fromDrop, False)

    def removeFromSlot_c_type_slot_quantity_fromDrop_consume(self, c: Any, type: Any, slot: int, quantity: int, fromDrop: bool, consume: bool) -> None:
        if c.getPlayer() is None || c.getPlayer().getInventory(type) is None:
            return
        item = c.getPlayer().getInventory(type).getItem(slot)
        if item is not None:
            allowZero = consume && GameConstants.isRechargable(item.getItemId())
            c.getPlayer().getInventory(type).removeItem(slot, quantity, allowZero)
            if item.getQuantity() == 0 && !allowZero:
                c.getSession().write(MaplePacketCreator.clearInventoryItem(type, item.getPosition(), fromDrop))
            else:
                c.getSession().write(MaplePacketCreator.updateInventorySlot(type, item, fromDrop))

    def removeById(self, c: Any, type: Any, itemId: int, quantity: int, fromDrop: bool, consume: bool) -> bool:
        remremove = quantity
        if c.getPlayer() is None || c.getPlayer().getInventory(type) is None:
            return False
        for item in c.getPlayer().getInventory(type).listById(itemId):
            theQ = item.getQuantity()
            if remremove <= theQ:
                removeFromSlot(c, type, item.getPosition(), remremove, fromDrop, consume)
                remremove = 0
                break
            if remremove <= theQ:
                continue
            removeFromSlot(c, type, item.getPosition(), item.getQuantity(), fromDrop, consume)
            remremove -= theQ
        return remremove <= 0

    def move(self, c: Any, type: Any, src: int, dst: int) -> None:
        if src < 0 || dst < 0 || dst > c.getPlayer().getInventory(type).getSlotLimit() || src == dst:
            return
        ii = MapleItemInformationProvider.getInstance()
        source = c.getPlayer().getInventory(type).getItem(src)
        initialTarget = c.getPlayer().getInventory(type).getItem(dst)
        if source is None:
            c.getPlayer().dropMessage(1, "移动道具失败，找不到移动道具的信息。")
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        olddstQ = -1
        if initialTarget is not None:
            olddstQ = initialTarget.getQuantity()
        oldsrcQ = source.getQuantity()
        slotMax = ii.getSlotMax(c, source.getItemId())
        c.getPlayer().getInventory(type).move(src, dst, slotMax)
        if !type == (MapleInventoryType.EQUIP) && initialTarget is not None && initialTarget.getItemId() == source.getItemId() && initialTarget.getOwner() == (source.getOwner()) && initialTarget.getExpiration() == source.getExpiration() && !GameConstants.isRechargable(source.getItemId()) && !type == (MapleInventoryType.CASH):
            if olddstQ + oldsrcQ > slotMax:
                c.getSession().write(MaplePacketCreator.moveAndMergeWithRestInventoryItem(type, src, dst, (short)(olddstQ + oldsrcQ - slotMax), slotMax))
            else:
                c.getSession().write(MaplePacketCreator.moveAndMergeInventoryItem(type, src, dst, (c.getPlayer().getInventory(type).getItem(dst)).getQuantity()))
        else:
            c.getSession().write(MaplePacketCreator.moveInventoryItem(type, src, dst))

    def equip(self, c: Any, src: int, dst: int) -> None:
        itemChanged = False
        ii = MapleItemInformationProvider.getInstance()
        chr = c.getPlayer()
        if chr is None:
            return
        statst = c.getPlayer().getStat()
        source = chr.getInventory(MapleInventoryType.EQUIP).getItem(src)
        target = chr.getInventory(MapleInventoryType.EQUIPPED).getItem(dst)
        if source is None || source.getDurability() == 0:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if MapleItemInformationProvider.getInstance().isUntradeableOnEquip(source.getItemId()):
            source.setFlag(ItemFlag.UNTRADEABLE.getValue())
            itemChanged = True
        stats = ii.getEquipStats(source.getItemId())
        if ii.isCash(source.getItemId()) && source.getUniqueId() <= 0:
            source.setUniqueId(1)
            c.getSession().write(MaplePacketCreator.updateSpecialItemUse_(source, GameConstants.getInventoryType(source.getItemId()).getType()))
        if dst < -999 && !GameConstants.isEvanDragonItem(source.getItemId()) && !GameConstants.is豆豆装备(source.getItemId()):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if dst >= -999 && dst < -99 && stats.get("cash") == 0 && !GameConstants.is豆豆装备(source.getItemId()) && !GameConstants.isEffectRing(source.getItemId()):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if !ii.canEquip(stats, source.getItemId(), chr.getLevel(), chr.getJob(), chr.getFame(), statst.getTotalStr(), statst.getTotalDex(), statst.getTotalLuk(), statst.getTotalInt(), c.getPlayer().getStat().levelBonus):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if GameConstants.isWeapon(source.getItemId()) && dst != -10 && dst != -11:
            AutobanManager.getInstance().autoban(c, "Equipment hack, itemid " + source.getItemId() + " to slot " + dst)
            return
        if !ii.isCash(source.getItemId()) && !GameConstants.isMountItemAvailable(source.getItemId(), c.getPlayer().getJob()):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        # switch (dst):
            # case -6:
                top = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-5))
                if top is None || !GameConstants.isOverall(top.getItemId()):
                    break
                if chr.getInventory(MapleInventoryType.EQUIP).isFull():
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return
                unequip(c, (short)(-5), chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot())
                break
            # case -5:
                top = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-5))
                bottom = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-6))
                if top is not None && GameConstants.isOverall(source.getItemId()):
                    if chr.getInventory(MapleInventoryType.EQUIP).isFull((bottom is not None && GameConstants.isOverall(source.getItemId())) ? 1 : 0):
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        return
                    unequip(c, (short)(-5), chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot())
                if bottom is None || !GameConstants.isOverall(source.getItemId()):
                    break
                if chr.getInventory(MapleInventoryType.EQUIP).isFull():
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return
                unequip(c, (short)(-6), chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot())
                break
            # case -10:
                weapon = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-11))
                if GameConstants.isKatara(source.getItemId()):
                    if (chr.getJob() != 900 && (chr.getJob() < 430 || chr.getJob() > 434)) || weapon is None || !GameConstants.isDagger(weapon.getItemId()):
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        return
                    break
                else:
                    if weapon is None || !GameConstants.isTwoHanded(weapon.getItemId()):
                        break
                    if chr.getInventory(MapleInventoryType.EQUIP).isFull():
                        c.getSession().write(MaplePacketCreator.getInventoryFull())
                        c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                        return
                    unequip(c, (short)(-11), chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot())
                    break
            # case -11:
                shield = chr.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-10))
                if shield is None || !GameConstants.isTwoHanded(source.getItemId()):
                    break
                if chr.getInventory(MapleInventoryType.EQUIP).isFull():
                    c.getSession().write(MaplePacketCreator.getInventoryFull())
                    c.getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return
                unequip(c, (short)(-10), chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot())
                break
        source = chr.getInventory(MapleInventoryType.EQUIP).getItem(src)
        target = chr.getInventory(MapleInventoryType.EQUIPPED).getItem(dst)
        if source is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        flag = source.getFlag()
        if stats.get("equipTradeBlock") == 1:
            if !ItemFlag.UNTRADEABLE.check(flag):
                flag |= ItemFlag.UNTRADEABLE.getValue()
                source.setFlag(flag)
                c.getSession().write(MaplePacketCreator.updateSpecialItemUse_(source, GameConstants.getInventoryType(source.getItemId()).getType()))
        elif ItemFlag.KARMA_EQ.check(flag):
            source.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
            c.getSession().write(MaplePacketCreator.updateSpecialItemUse(source, GameConstants.getInventoryType(source.getItemId()).getType()))
        elif ItemFlag.KARMA_USE.check(flag):
            source.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
            c.getSession().write(MaplePacketCreator.updateSpecialItemUse(source, GameConstants.getInventoryType(source.getItemId()).getType()))
        chr.getInventory(MapleInventoryType.EQUIP).removeSlot(src)
        if target is not None:
            chr.getInventory(MapleInventoryType.EQUIPPED).removeSlot(dst)
        mods = []
        if itemChanged:
            mods.add(ModifyInventory(3, source))
            mods.add(ModifyInventory(0, source.copy()))
        source.setPosition(dst)
        chr.getInventory(MapleInventoryType.EQUIPPED).addFromDB(source)
        if target is not None:
            target.setPosition(src)
            chr.getInventory(MapleInventoryType.EQUIP).addFromDB(target)
        if GameConstants.isWeapon(source.getItemId()):
            if chr.getBuffedValue(MapleBuffStat.攻击加速) is not None:
                chr.cancelBuffStats(MapleBuffStat.攻击加速)
            if chr.getBuffedValue(MapleBuffStat.暗器伤人) is not None:
                chr.cancelBuffStats(MapleBuffStat.暗器伤人)
            if chr.getBuffedValue(MapleBuffStat.无形箭弩) is not None:
                chr.cancelBuffStats(MapleBuffStat.无形箭弩)
            if chr.getBuffedValue(MapleBuffStat.属性攻击) is not None:
                chr.cancelBuffStats(MapleBuffStat.属性攻击)
            if chr.getBuffedValue(MapleBuffStat.LIGHTNING_CHARGE) is not None:
                chr.cancelBuffStats(MapleBuffStat.LIGHTNING_CHARGE)
        if source.getItemId() == 1122017:
            c.getPlayer().dropMessage(5, "精灵吊坠已佩戴。计时开始。1小时后经验增加百分之10.")
            chr.startFairySchedule(True, True)
        mods.add(ModifyInventory(2, source, src))
        c.getSession().write(MaplePacketCreator.moveInventoryItem(MapleInventoryType.EQUIP, src, dst, 2))
        chr.equipChanged()
        c.getSession().write(MaplePacketCreator.updateSpecialItemUse_(source, GameConstants.getInventoryType(source.getItemId()).getType()))

    def unequip(self, c: Any, src: int, dst: int) -> None:
        source = c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).getItem(src)
        target = c.getPlayer().getInventory(MapleInventoryType.EQUIP).getItem(dst)
        if dst < 0 || source is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if target is not None && src <= 0:
            c.getSession().write(MaplePacketCreator.getInventoryFull())
            return
        c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).removeSlot(src)
        if target is not None:
            c.getPlayer().getInventory(MapleInventoryType.EQUIP).removeSlot(dst)
        source.setPosition(dst)
        c.getPlayer().getInventory(MapleInventoryType.EQUIP).addFromDB(source)
        if target is not None:
            target.setPosition(src)
            c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).addFromDB(target)
        if GameConstants.isWeapon(source.getItemId()):
            if c.getPlayer().getBuffedValue(MapleBuffStat.攻击加速) is not None:
                c.getPlayer().cancelBuffStats(MapleBuffStat.攻击加速)
            if c.getPlayer().getBuffedValue(MapleBuffStat.暗器伤人) is not None:
                c.getPlayer().cancelBuffStats(MapleBuffStat.暗器伤人)
            if c.getPlayer().getBuffedValue(MapleBuffStat.无形箭弩) is not None:
                c.getPlayer().cancelBuffStats(MapleBuffStat.无形箭弩)
            if c.getPlayer().getBuffedValue(MapleBuffStat.属性攻击) is not None:
                c.getPlayer().cancelBuffStats(MapleBuffStat.属性攻击)
        if source.getItemId() == 1122017:
            c.getPlayer().dropMessage(5, "精灵吊坠已脱下。计时结束。")
            c.getPlayer().cancelFairySchedule(True)
        c.getSession().write(MaplePacketCreator.moveInventoryItem(MapleInventoryType.EQUIP, src, dst, 1))
        c.getPlayer().equipChanged()

    def drop(self, c: Any, type: Any, src: int, quantity: int) -> bool:
        return drop(c, type, src, quantity, False)

    def drop_c_type_src_quantity_npcInduced(self, c: Any, type: Any, src: int, quantity: int, npcInduced: bool) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        if src < 0:
            type = MapleInventoryType.EQUIPPED
        if c.getPlayer() is None:
            return False
        source = c.getPlayer().getInventory(type).getItem(src)
        if source is None || (!npcInduced && GameConstants.isPet(source.getItemId())):
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        if ii.isCash(source.getItemId()) || source.getExpiration() > 0:
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        flag = source.getFlag()
        id = source.getItemId()
        if GameConstants.isRechargable(id) && source.getQuantity() == 0:
            source.setQuantity(1)
        if quantity > source.getQuantity():
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        if ItemFlag.LOCK.check(flag) || (quantity != 1 && type == MapleInventoryType.EQUIP):
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        c.getPlayer().setCurrenttime(int(time.time() * 1000))
        if c.getPlayer().getCurrenttime() - c.getPlayer().getLasttime() < 1000:
            c.getPlayer().dropMessage(1, "<温馨提醒>：请您慢点使用.")
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        c.getPlayer().setLasttime(int(time.time() * 1000))
        dropPos = Point(c.getPlayer().getPosition())
        c.getPlayer().getCheatTracker().checkDrop()
        if quantity < source.getQuantity() && !GameConstants.isRechargable(source.getItemId()):
            target = source.copy()
            target.setQuantity(quantity)
            source.setQuantity((short)(source.getQuantity() - quantity))
            c.getSession().write(MaplePacketCreator.dropInventoryItemUpdate(type, source))
            if ii.isDropRestricted(target.getItemId()) || ii.isAccountShared(target.getItemId()):
                if ItemFlag.KARMA_EQ.check(flag):
                    target.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
                    c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), target, dropPos, True, True)
                elif ItemFlag.KARMA_USE.check(flag):
                    target.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
                    c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), target, dropPos, True, True)
                else:
                    c.getPlayer().getMap().disappearingItemDrop(c.getPlayer(), c.getPlayer(), target, dropPos)
            elif GameConstants.isPet(source.getItemId()) || ItemFlag.UNTRADEABLE.check(flag):
                c.getPlayer().getMap().disappearingItemDrop(c.getPlayer(), c.getPlayer(), target, dropPos)
            else:
                c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), target, dropPos, True, True)
        else:
            c.getPlayer().getInventory(type).removeSlot(src)
            c.getSession().write(MaplePacketCreator.dropInventoryItem((src < 0) ? MapleInventoryType.EQUIP : type, src))
            if src < 0:
                c.getPlayer().equipChanged()
            if ii.isDropRestricted(source.getItemId()) || ii.isAccountShared(source.getItemId()):
                if ItemFlag.KARMA_EQ.check(flag):
                    source.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
                    c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), source, dropPos, True, True)
                elif ItemFlag.KARMA_USE.check(flag):
                    source.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
                    c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), source, dropPos, True, True)
                else:
                    c.getPlayer().getMap().disappearingItemDrop(c.getPlayer(), c.getPlayer(), source, dropPos)
            elif GameConstants.isPet(source.getItemId()) || ItemFlag.UNTRADEABLE.check(flag):
                c.getPlayer().getMap().disappearingItemDrop(c.getPlayer(), c.getPlayer(), source, dropPos)
            else:
                c.getPlayer().getMap().spawnItemDrop(c.getPlayer(), c.getPlayer(), source, dropPos, True, True)
        return True

    def removeAllByEquipOnlyId(self, c: Any, equipOnlyId: int) -> None:
        if c.getPlayer() is None:
            return
        locked = False
        ii = MapleItemInformationProvider.getInstance()
        copyEquipItems = c.getPlayer().getInventory(MapleInventoryType.EQUIP).listByEquipOnlyId(equipOnlyId)
        for item in copyEquipItems:
            if item is not None:
                if !locked:
                    flag = item.getFlag()
                    flag |= ItemFlag.LOCK.getValue()
                    flag |= ItemFlag.UNTRADEABLE.getValue()
                    item.setFlag(flag)
                    item.setOwner("复制装备")
                    c.getPlayer().forceUpdateItem(item)
                    c.getPlayer().dropMessage(5, "在背包中发现复制装备[" + ii.getName(item.getItemId()) + "]已经将其锁定。")
                    msgtext = "玩家 " + c.getPlayer().getName() + " ID: " + c.getPlayer().getId() + " (等级 " + c.getPlayer().getLevel() + ") 地图: " + c.getPlayer().getMapId() + " 在玩家背包中发现复制装备[" + ii.getName(item.getItemId()) + "]已经将其锁定。"
                    FileoutputUtil.log("logs/复制装备.txt", msgtext + " 道具唯一ID: " + item.getEquipOnlyId())
                    locked = True
                else:
                    removeFromSlot(c, MapleInventoryType.EQUIP, item.getPosition(), item.getQuantity(), True, False)
                    c.getPlayer().dropMessage(5, "在背包中发现复制装备[" + ii.getName(item.getItemId()) + "]已经将其删除。")
        locked = False
        copyEquipedItems = c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).listByEquipOnlyId(equipOnlyId)
        for item2 in copyEquipedItems:
            if item2 is not None:
                if !locked:
                    flag2 = item2.getFlag()
                    flag2 |= ItemFlag.LOCK.getValue()
                    flag2 |= ItemFlag.UNTRADEABLE.getValue()
                    item2.setFlag(flag2)
                    item2.setOwner("复制装备")
                    c.getPlayer().forceUpdateItem(item2)
                    c.getPlayer().dropMessage(5, "在穿戴中发现复制装备[" + ii.getName(item2.getItemId()) + "]已经将其锁定。")
                    msgtext2 = "玩家 " + c.getPlayer().getName() + " ID: " + c.getPlayer().getId() + " (等级 " + c.getPlayer().getLevel() + ") 地图: " + c.getPlayer().getMapId() + " 在玩家穿戴中发现复制装备[" + ii.getName(item2.getItemId()) + "]已经将其锁定。"
                    FileoutputUtil.log("logs/复制装备.txt", msgtext2 + " 道具唯一ID: " + item2.getEquipOnlyId())
                    locked = True
                else:
                    removeFromSlot(c, MapleInventoryType.EQUIPPED, item2.getPosition(), item2.getQuantity(), True, False)
                    c.getPlayer().dropMessage(5, "在穿戴中发现复制装备[" + ii.getName(item2.getItemId()) + "]已经将其删除。")
                    c.getPlayer().equipChanged()
        locked = False
        copyUseItems = c.getPlayer().getInventory(MapleInventoryType.USE).listByEquipOnlyId(equipOnlyId)
        for item3 in copyUseItems:
            if item3 is not None:
                if !locked:
                    flag3 = item3.getFlag()
                    flag3 |= ItemFlag.LOCK.getValue()
                    flag3 |= ItemFlag.UNTRADEABLE.getValue()
                    item3.setFlag(flag3)
                    item3.setOwner("复制道具")
                    c.getPlayer().forceUpdateItem(item3)
                    c.getPlayer().dropMessage(5, "在消耗中发现复制道具[" + ii.getName(item3.getItemId()) + "]已经将其锁定。")
                    msgtext3 = "玩家 " + c.getPlayer().getName() + " ID: " + c.getPlayer().getId() + " (等级 " + c.getPlayer().getLevel() + ") 地图: " + c.getPlayer().getMapId() + " 在玩家消耗中发现复制道具[" + ii.getName(item3.getItemId()) + "]已经将其锁定。"
                    FileoutputUtil.log("logs/复制装备.txt", msgtext3 + " 道具唯一ID: " + item3.getEquipOnlyId())
                    locked = True
                else:
                    removeFromSlot(c, MapleInventoryType.USE, item3.getPosition(), item3.getQuantity(), True, False)
                    c.getPlayer().dropMessage(5, "在消耗中发现复制道具[" + ii.getName(item3.getItemId()) + "]已经将其删除。")
                    c.getPlayer().equipChanged()
        locked = False
        copyEtcItems = c.getPlayer().getInventory(MapleInventoryType.ETC).listByEquipOnlyId(equipOnlyId)
        for item4 in copyEtcItems:
            if item4 is not None:
                if !locked:
                    flag4 = item4.getFlag()
                    flag4 |= ItemFlag.LOCK.getValue()
                    flag4 |= ItemFlag.UNTRADEABLE.getValue()
                    item4.setFlag(flag4)
                    item4.setOwner("复制道具")
                    c.getPlayer().forceUpdateItem(item4)
                    c.getPlayer().dropMessage(5, "在其他中发现复制道具[" + ii.getName(item4.getItemId()) + "]已经将其锁定。")
                    msgtext4 = "玩家 " + c.getPlayer().getName() + " ID: " + c.getPlayer().getId() + " (等级 " + c.getPlayer().getLevel() + ") 地图: " + c.getPlayer().getMapId() + " 在玩家其他中发现复制道具[" + ii.getName(item4.getItemId()) + "]已经将其锁定。"
                    FileoutputUtil.log("logs/复制装备.txt", msgtext4 + " 道具唯一ID: " + item4.getEquipOnlyId())
                    locked = True
                else:
                    removeFromSlot(c, MapleInventoryType.ETC, item4.getPosition(), item4.getQuantity(), True, False)
                    c.getPlayer().dropMessage(5, "在其他中发现复制道具[" + ii.getName(item4.getItemId()) + "]已经将其删除。")
                    c.getPlayer().equipChanged()
        locked = False
        copyCashItems = c.getPlayer().getInventory(MapleInventoryType.CASH).listByEquipOnlyId(equipOnlyId)
        for item5 in copyCashItems:
            if item5 is not None:
                if !locked:
                    flag5 = item5.getFlag()
                    flag5 |= ItemFlag.LOCK.getValue()
                    flag5 |= ItemFlag.UNTRADEABLE.getValue()
                    item5.setFlag(flag5)
                    item5.setOwner("复制道具")
                    c.getPlayer().forceUpdateItem(item5)
                    c.getPlayer().dropMessage(5, "在现金道具中发现复制道具[" + ii.getName(item5.getItemId()) + "]已经将其锁定。")
                    msgtext5 = "玩家 " + c.getPlayer().getName() + " ID: " + c.getPlayer().getId() + " (等级 " + c.getPlayer().getLevel() + ") 地图: " + c.getPlayer().getMapId() + " 在玩家现金道具中发现复制道具[" + ii.getName(item5.getItemId()) + "]已经将其锁定。"
                    FileoutputUtil.log("logs/复制装备.txt", msgtext5 + " 道具唯一ID: " + item5.getEquipOnlyId())
                    locked = True
                else:
                    removeFromSlot(c, MapleInventoryType.CASH, item5.getPosition(), item5.getQuantity(), True, False)
                    c.getPlayer().dropMessage(5, "在现金道具中发现复制道具[" + ii.getName(item5.getItemId()) + "]已经将其删除。")
                    c.getPlayer().equipChanged()

