"""
MapleTrade - Converted from Java source
Original: server/MapleTrade.java
Package: server
"""

from typing import List
from typing import Optional, Any
from weakref import ref
import threading
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class MapleTrade:
    """
    Class MapleTrade
    """

    def __init__(self, tradingslot: int, chr: Any):
        self.partner = None
        self.items = None
        self.exchangeItems = []
        self.meso = 0
        self.exchangeMeso = 0
        self.locked = False
        self.chr = None
        self.tradingslot = None
        self.partner = None
        self.items = []
        self.meso = 0
        self.exchangeMeso = 0
        self.locked = False
        self.tradingslot = tradingslot
        self.chr = new WeakReference<MapleCharacter>(chr)


    def completeTrade(self, c: Any) -> None:
        local = c.getTrade()
        partner = local.getPartner()
        if partner is None or local.locked:
            return
        local.locked = True
        partner.getChr().getClient().getSession().write(MaplePacketCreator.getTradeConfirmation())
        partner.exchangeItems = local.items
        partner.exchangeMeso = local.meso
        if partner.isLocked():
            lz = local.check()
            lz2 = partner.check()
            if lz == 0 and lz2 == 0:
                local.CompleteTrade()
                partner.CompleteTrade()
            else:
                partner.cancel(partner.getChr().getClient(), (lz == 0) ? lz2 : lz)
                local.cancel(c.getClient(), (lz == 0) ? lz2 : lz)
            partner.getChr().setTrade(None)
            c.setTrade(None)

    def cancelTrade(self, Localtrade: Any, c: Any) -> None:
        Localtrade.cancel(c)
        partner = Localtrade.getPartner()
        if partner is not None:
            partner.cancel(partner.getChr().getClient())
            partner.getChr().setTrade(None)
        if Localtrade.chr.get() is not None:
            Localtrade.chr.get().setTrade(None)

    def startTrade(self, c: Any) -> None:
        if c.getTrade() is None:
            c.setTrade(MapleTrade(0, c))
            c.getClient().getSession().write(MaplePacketCreator.getTradeStart(c.getClient(), c.getTrade(), 0, False))
        else:
            c.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "不能同时做多件事情。"))

    def translated_start现金交易(self, c: Any) -> None:
        if c.getTrade() is None:
            c.setTrade(MapleTrade(0, c))
            c.getClient().getSession().write(MaplePacketCreator.getTradeStart(c.getClient(), c.getTrade(), 0, True))
        else:
            c.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "不能同时做多件事情。"))

    def inviteTrade(self, c1: Any, c2: Any) -> None:
        if c1 is None or c1.getTrade() is None:
            return
        if c1.getMap().getId() == c2.getMap().getId():
            if c2 is not None and c2.getTrade() is None:
                c2.setTrade(MapleTrade(1, c2))
                c2.getTrade().setPartner(c1.getTrade())
                c1.getTrade().setPartner(c2.getTrade())
                c2.getClient().getSession().write(MaplePacketCreator.getTradeInvite(c1, False))
            else:
                c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方正在和其他玩家进行交易中。"))
                cancelTrade(c1.getTrade(), c1.getClient())
        else:
            c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方与你不在同一个地图。"))

    def translated_invite现金交易(self, c1: Any, c2: Any) -> None:
        if c1 is None or c1.getTrade() is None:
            return
        if c1.getMap().getId() == c2.getMap().getId():
            if c2 is not None and c2.getTrade() is None:
                c2.setTrade(MapleTrade(1, c2))
                c2.getTrade().setPartner(c1.getTrade())
                c1.getTrade().setPartner(c2.getTrade())
                c2.getClient().getSession().write(MaplePacketCreator.getTradeInvite(c1, True))
            else:
                c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方正在和其他玩家进行交易中。"))
                cancelTrade(c1.getTrade(), c1.getClient())
        else:
            c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方与你不在同一个地图。"))

    def translated_visit现金交易(self, c1: Any, c2: Any) -> None:
        if c1.getMap().getId() == c2.getMap().getId():
            if c1.getTrade() is not None and c1.getTrade().getPartner() == c2.getTrade() and c2.getTrade() is not None and c2.getTrade().getPartner() == c1.getTrade():
                c2.getClient().getSession().write(MaplePacketCreator.getTradePartnerAdd(c1))
                c1.getClient().getSession().write(MaplePacketCreator.getTradeStart(c1.getClient(), c1.getTrade(), 1, True))
            else:
                c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方已经取消了交易。"))
        else:
            c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方与你不在同一个地图。"))

    def visitTrade(self, c1: Any, c2: Any) -> None:
        if c1.getMap().getId() == c2.getMap().getId():
            if c1.getTrade() is not None and c1.getTrade().getPartner() == c2.getTrade() and c2.getTrade() is not None and c2.getTrade().getPartner() == c1.getTrade():
                c2.getClient().getSession().write(MaplePacketCreator.getTradePartnerAdd(c1))
                c1.getClient().getSession().write(MaplePacketCreator.getTradeStart(c1.getClient(), c1.getTrade(), 1, False))
            else:
                c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方已经取消了交易。"))
        else:
            c1.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "对方与你不在同一个地图。"))

    def declineTrade(self, c: Any) -> None:
        trade = c.getTrade()
        if trade is not None:
            if trade.getPartner() is not None:
                other = trade.getPartner().getChr()
                other.getTrade().cancel(other.getClient())
                other.setTrade(None)
                other.dropMessage(5, c.getName() + " 拒绝了你的交易邀请。")
            trade.cancel(c.getClient())
            c.setTrade(None)

    def CompleteTrade(self) -> None:
        ii = MapleItemInformationProvider.getInstance()
        if self.exchangeItems is not None:
            for item in self.exchangeItems:
                flag = item.getFlag()
                if ItemFlag.KARMA_EQ.check(flag):
                    item.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
                elif ItemFlag.KARMA_USE.check(flag):
                    item.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
                MapleInventoryManipulator.addFromDrop(self.chr.get().getClient(), item, False)
            self.exchangeItems.clear()
        if self.exchangeMeso > 0:
            self.chr.get().gainMeso(self.exchangeMeso - GameConstants.getTaxAmount(self.exchangeMeso), False, True, False)
        self.exchangeMeso = 0
        self.chr.get().getClient().getSession().write(MaplePacketCreator.TradeMessage(self.tradingslot, 8))

    def cancel(self, c: Any) -> None:
        self.cancel(c, 0)

    def cancel_c_unsuccessful(self, c: Any, unsuccessful: int) -> None:
        if self.items is not None:
            for item in self.items:
                MapleInventoryManipulator.addFromDrop(c, item, False)
            self.items.clear()
        if self.meso > 0:
            c.getPlayer().gainMeso(self.meso, False, True, False)
        self.meso = 0
        c.getSession().write(MaplePacketCreator.getTradeCancel(self.tradingslot, unsuccessful))

    def isLocked(self) -> bool:
        return self.locked

    def setMeso(self, meso: int) -> None:
        if self.locked or self.partner is None or meso <= 0 or self.meso + meso <= 0:
            return
        if self.chr.get().getMeso() >= meso:
            self.chr.get().gainMeso(-meso, False, True, False)
            self.meso += meso
            self.chr.get().getClient().getSession().write(MaplePacketCreator.getTradeMesoSet(0, self.meso))
            if self.partner is not None:
                self.partner.getChr().getClient().getSession().write(MaplePacketCreator.getTradeMesoSet(1, self.meso))

    def addItem(self, item: Any) -> None:
        if self.locked or self.partner is None:
            return
        self.items.add(item)
        self.chr.get().getClient().getSession().write(MaplePacketCreator.getTradeItemAdd(0, item))
        if self.partner is not None:
            self.partner.getChr().getClient().getSession().write(MaplePacketCreator.getTradeItemAdd(1, item))

    def chat(self, message: str) -> None:
        self.chr.get().dropMessage(-2, self.chr.get().getName() + " : " + message)
        if self.partner is not None:
            self.partner.getChr().getClient().getSession().write(PlayerShopPacket.shopChat(self.chr.get().getName() + " : " + message, 1))

    def getPartner(self) -> Any:
        return self.partner

    def setPartner(self, partner: Any) -> None:
        if self.locked:
            return
        self.partner = partner

    def getChr(self) -> Any:
        return self.chr.get()

    def getNextTargetSlot(self) -> int:
        if self.items >= 9:
            return -1
        ret = 1
        for item in self.items:
            if item.getPosition() == ret:
                ret += 1
        return ret

    def setItems(self, c: Any, item: Any, targetSlot: int, quantity: int) -> bool:
        target = self.getNextTargetSlot()
        ii = MapleItemInformationProvider.getInstance()
        if target == -1 or GameConstants.isPet(item.getItemId()) or self.isLocked() or (GameConstants.getInventoryType(item.getItemId()) == MapleInventoryType.CASH and quantity != 1) or (GameConstants.getInventoryType(item.getItemId()) == MapleInventoryType.EQUIP and quantity != 1):
            return False
        flag = item.getFlag()
        if ItemFlag.UNTRADEABLE.check(flag) or ItemFlag.LOCK.check(flag):
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        if (ii.isDropRestricted(item.getItemId()) or ii.isAccountShared(item.getItemId())) and not ItemFlag.KARMA_EQ.check(flag) and not ItemFlag.KARMA_USE.check(flag):
            c.getSession().write(MaplePacketCreator.enableActions())
            return False
        tradeItem = item.copy()
        if GameConstants.is飞镖道具(item.getItemId()) or GameConstants.is子弹道具(item.getItemId()):
            tradeItem.setQuantity(item.getQuantity())
            MapleInventoryManipulator.removeFromSlot(c, GameConstants.getInventoryType(item.getItemId()), item.getPosition(), item.getQuantity(), True)
        else:
            tradeItem.setQuantity(quantity)
            MapleInventoryManipulator.removeFromSlot(c, GameConstants.getInventoryType(item.getItemId()), item.getPosition(), quantity, True)
        if targetSlot < 0:
            targetSlot = target
        else:
            for itemz in self.items:
                if itemz.getPosition() == targetSlot:
                    targetSlot = target
                    break
        tradeItem.setPosition(targetSlot)
        self.addItem(tradeItem)
        return True

    def check(self) -> int:
        if self.chr.get().getMeso() + self.exchangeMeso < 0:
            return 1
        ii = MapleItemInformationProvider.getInstance()
        eq = 0
        use = 0
        setup = 0
        etc = 0
        cash = 0
        for item in self.exchangeItems:
            # switch (GameConstants.getInventoryType(item.getItemId())):
                # case EQUIP:
                    eq += 1
                    break
                # case USE:
                    use += 1
                    break
                # case SETUP:
                    setup += 1
                    break
                # case ETC:
                    etc += 1
                    break
                # case CASH:
                    cash += 1
                    break
            if ii.isPickupRestricted(item.getItemId()) and self.chr.get().getInventory(GameConstants.getInventoryType(item.getItemId())).findById(item.getItemId()) is not None:
                return 2
        if self.chr.get().getInventory(MapleInventoryType.EQUIP).getNumFreeSlot() < eq or self.chr.get().getInventory(MapleInventoryType.USE).getNumFreeSlot() < use or self.chr.get().getInventory(MapleInventoryType.SETUP).getNumFreeSlot() < setup or self.chr.get().getInventory(MapleInventoryType.ETC).getNumFreeSlot() < etc or self.chr.get().getInventory(MapleInventoryType.CASH).getNumFreeSlot() < cash:
            return 1
        return 0

