"""
MTSOperation - Converted from Java source
Original: handling/cashshop/handler/MTSOperation.java
Package: handling.cashshop.handler
"""

from typing import Optional, Any
import time

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from server.MTSCart import *  # TODO: import specific classes
# from server.MTSStorage import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class MTSOperation:
    """
    Class MTSOperation
    """


    def MTSUpdate(self, cart: Any, c: Any) -> None:
        c.getPlayer().modifyCSPoints(2, MTSStorage.getInstance().getCart(c.getPlayer().getId()).getSetOwedNX(), False)
        c.getSession().write(MTSCSPacket.getMTSWantedListingOver(0, 0))
        doMTSPackets(cart, c)

    def doMTSPackets(self, cart: Any, c: Any) -> None:
        sendMTSPackets(cart, c, False)

    def sendMTSPackets(self, cart: Any, c: Any, changed: bool) -> None:
        c.getSession().write(MTSStorage.getInstance().getCurrentMTS(cart))
        c.getSession().write(MTSStorage.getInstance().getCurrentNotYetSold(cart))
        c.getSession().write(MTSStorage.getInstance().getCurrentTransfer(cart, changed))
        c.getSession().write(MTSCSPacket.showMTSCash(c.getPlayer()))
        c.getSession().write(MTSCSPacket.enableCSUse())
        MTSStorage.getInstance().checkExpirations()

