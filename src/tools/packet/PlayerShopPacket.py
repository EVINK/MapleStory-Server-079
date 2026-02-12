"""
PlayerShopPacket - Converted from Java source
Original: tools/packet/PlayerShopPacket.java
Package: tools.packet
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from server.MerchItemPackage import *  # TODO: import specific classes
# from server.shops.AbstractPlayerStore import *  # TODO: import specific classes
# from server.shops.HiredMerchant import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from server.shops.MapleMiniGame import *  # TODO: import specific classes
# from server.shops.MaplePlayerShop import *  # TODO: import specific classes
# from server.shops.MaplePlayerShopItem import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class PlayerShopPacket:
    """
    Class PlayerShopPacket
    """


    def addCharBox(self, c: Any, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("addCharBox--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_CHAR_BOX.getValue())
        mplew.writeInt(c.getId())
        PacketHelper.addAnnounceBox(mplew, c)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removeCharBox(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removeCharBox--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_CHAR_BOX.getValue())
        mplew.writeInt(c.getId())
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendTitleBox(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendTitleBox--------------------")
        mplew.writeShort(SendPacketOpcode.SEND_TITLE_BOX.getValue())
        mplew.write(7)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendPlayerShopBox(self, c: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendPlayerShopBox--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_CHAR_BOX.getValue())
        mplew.writeInt(c.getId())
        PacketHelper.addAnnounceBox(mplew, c)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getHiredMerch(self, chr: Any, merch: Any, firstTime: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getHiredMerch--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(5)
        mplew.write(5)
        mplew.write(4)
        mplew.writeShort(merch.getVisitorSlot(chr))
        mplew.writeInt(merch.getItemId())
        mplew.writeMapleAsciiString("雇佣商人")
        for storechr in merch.getVisitors():
            mplew.write(storechr.left)
            PacketHelper.addCharLook(mplew, storechr.right, False)
            mplew.writeMapleAsciiString(storechr.right.getName())
        mplew.write(-1)
        mplew.writeShort(0)
        mplew.writeMapleAsciiString(merch.getOwnerName())
        if merch.isOwner(chr):
            mplew.writeInt(merch.getTimeLeft())
            mplew.write(firstTime ? 1 : 0)
            mplew.write(merch.getBoughtItems())
            for (final AbstractPlayerStore.BoughtItem SoldItem : merch.getBoughtItems())
                mplew.writeInt(SoldItem.id)
                mplew.writeShort(SoldItem.quantity)
                mplew.writeInt(SoldItem.totalPrice)
                mplew.writeMapleAsciiString(SoldItem.buyer)
            mplew.writeInt(merch.getMeso())
        mplew.writeMapleAsciiString(merch.getDescription())
        mplew.write(10)
        mplew.writeInt(merch.getMeso())
        mplew.write(merch.getItems())
        for item in merch.getItems():
            mplew.writeShort(item.bundles)
            mplew.writeShort(item.item.getQuantity())
            mplew.writeInt(item.price)
            PacketHelper.addItemInfo(mplew, item.item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getPlayerStore(self, chr: Any, firstTime: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getPlayerStore--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        ips = chr.getPlayerShop()
        # switch (ips.getShopType()):
            # case 2:
                mplew.write(5)
                mplew.write(4)
                mplew.write(4)
                break
            # case 3:
                mplew.write(5)
                mplew.write(2)
                mplew.write(2)
                break
            # case 4:
                mplew.write(5)
                mplew.write(1)
                mplew.write(2)
                break
        mplew.writeShort(ips.getVisitorSlot(chr))
        PacketHelper.addCharLook(mplew, (ips).getMCOwner(), False)
        mplew.writeMapleAsciiString(ips.getOwnerName())
        for storechr in ips.getVisitors():
            mplew.write(storechr.left)
            PacketHelper.addCharLook(mplew, storechr.right, False)
            mplew.writeMapleAsciiString(storechr.right.getName())
        mplew.write(255)
        mplew.writeMapleAsciiString(ips.getDescription())
        mplew.write(10)
        mplew.write(ips.getItems())
        for item in ips.getItems():
            mplew.writeShort(item.bundles)
            mplew.writeShort(item.item.getQuantity())
            mplew.writeInt(item.price)
            PacketHelper.addItemInfo(mplew, item.item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopChat(self, message: str, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopChat--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(6)
        mplew.write(8)
        mplew.write(slot)
        mplew.writeMapleAsciiString(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopErrorMessage(self, error: int, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopErrorMessage--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(10)
        mplew.write(type)
        mplew.write(error)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def spawnHiredMerchant(self, hm: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("spawnHiredMerchant--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_HIRED_MERCHANT.getValue())
        mplew.writeInt(hm.getOwnerId())
        mplew.writeInt(hm.getItemId())
        mplew.writePos(hm.getPosition())
        mplew.writeShort(0)
        mplew.writeMapleAsciiString(hm.getOwnerName())
        PacketHelper.addInteraction(mplew, hm)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def destroyHiredMerchant(self, id: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("destroyHiredMerchant--------------------")
        mplew.writeShort(SendPacketOpcode.DESTROY_HIRED_MERCHANT.getValue())
        mplew.writeInt(id)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopItemUpdate(self, shop: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopItemUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(23)
        if shop.getShopType() == 1:
            mplew.writeInt(0)
        mplew.write(shop.getItems())
        for item in shop.getItems():
            mplew.writeShort(item.bundles)
            mplew.writeShort(item.item.getQuantity())
            mplew.writeInt(item.price)
            PacketHelper.addItemInfo(mplew, item.item, True, True)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopVisitorAdd(self, chr: Any, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopVisitorAdd--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(4)
        mplew.write(slot)
        PacketHelper.addCharLook(mplew, chr, False)
        mplew.writeMapleAsciiString(chr.getName())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopVisitorLeave(self, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopVisitorLeave--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(10)
        if slot > 0:
            mplew.write(slot)
            mplew.write(slot)
            mplew.write(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def Merchant_Buy_Error(self, message: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("Merchant_Buy_Error--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(23)
        mplew.write(message)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def updateHiredMerchant(self, shop: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updateHiredMerchant--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_HIRED_MERCHANT.getValue())
        mplew.writeInt(shop.getOwnerId())
        PacketHelper.addInteraction(mplew, shop)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def merchItem_Message(self, op: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("merchItem_Message--------------------")
        mplew.writeShort(SendPacketOpcode.MERCH_ITEM_MSG.getValue())
        mplew.write(op)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def merchItemStore(self, op: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("merchItemStore--------------------")
        mplew.writeShort(SendPacketOpcode.MERCH_ITEM_STORE.getValue())
        mplew.write(op)
        # switch (op):
            # case 36:
                mplew.writeZeroBytes(8)
                break
            # default:
                mplew.write(0)
                break
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def merchItemStore_ItemData(self, pack: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("merchItemStore_ItemData--------------------")
        mplew.writeShort(SendPacketOpcode.MERCH_ITEM_STORE.getValue())
        mplew.write(35)
        mplew.writeInt(9030000)
        mplew.writeInt(32272)
        mplew.writeZeroBytes(5)
        mplew.writeInt(pack.getMesos())
        mplew.write(0)
        mplew.write(pack.getItems())
        for item in pack.getItems():
            PacketHelper.addItemInfo(mplew, item, True, True)
        mplew.writeZeroBytes(3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGame(self, c: Any, minigame: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGame--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(5)
        mplew.write(minigame.getGameType())
        mplew.write(minigame.getMaxSize())
        mplew.writeShort(minigame.getVisitorSlot(c.getPlayer()))
        PacketHelper.addCharLook(mplew, minigame.getMCOwner(), False)
        mplew.writeMapleAsciiString(minigame.getOwnerName())
        for visitorz in minigame.getVisitors():
            mplew.write(visitorz.getLeft())
            PacketHelper.addCharLook(mplew, visitorz.getRight(), False)
            mplew.writeMapleAsciiString(visitorz.getRight().getName())
        mplew.write(-1)
        mplew.write(0)
        addGameInfo(mplew, minigame.getMCOwner(), minigame)
        for visitorz in minigame.getVisitors():
            mplew.write(visitorz.getLeft())
            addGameInfo(mplew, visitorz.getRight(), minigame)
        mplew.write(-1)
        mplew.writeMapleAsciiString(minigame.getDescription())
        mplew.writeShort(minigame.getPieceType())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameReady(self, ready: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameReady--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(ready ? 57 : 58)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameExitAfter(self, ready: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameExitAfter--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(ready ? 55 : 56)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameStart(self, loser: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameStart--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(60)
        mplew.write((loser != 1) ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameSkip(self, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameSkip--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(62)
        mplew.write(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameSkip1(self, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameSkip1--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(62)
        mplew.write((slot != 1) ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameRequestTie(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameRequestTie--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(48)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameRequestREDO(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameRequestREDO--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(53)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameDenyTie(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameDenyTie--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(49)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameDenyREDO(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameDenyREDO--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(48)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameFull(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameFull--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.writeShort(5)
        mplew.write(2)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameMoveOmok(self, move1: int, move2: int, move3: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameMoveOmok--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(63)
        mplew.writeInt(move1)
        mplew.writeInt(move2)
        mplew.write(move3)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameNewVisitor(self, c: Any, slot: int, game: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameNewVisitor--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(4)
        mplew.write(slot)
        PacketHelper.addCharLook(mplew, c, False)
        mplew.writeMapleAsciiString(c.getName())
        addGameInfo(mplew, c, game)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addGameInfo(self, mplew: Any, chr: Any, game: Any) -> None:
        mplew.writeInt(game.getGameType())
        mplew.writeInt(game.getWins(chr))
        mplew.writeInt(game.getTies(chr))
        mplew.writeInt(game.getLosses(chr))
        mplew.writeInt(game.getScore(chr))

    def getMiniGameClose(self, number: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameClose--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(10)
        mplew.write(1)
        mplew.write(number)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMatchCardStart(self, game: Any, loser: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMatchCardStart--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(60)
        mplew.write((loser != 1) ? 1 : 0)
        times = (game.getPieceType() == 1) ? 20 : ((game.getPieceType() == 2) ? 30 : 12)
        mplew.write(times)
        for i in range(1, = times):
            mplew.writeInt(game.getCardId(i))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMatchCardSelect(self, turn: int, slot: int, firstslot: int, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMatchCardSelect--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(67)
        mplew.write(turn)
        mplew.write(slot)
        if turn == 0:
            mplew.write(firstslot)
            mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def getMiniGameResult(self, game: Any, type: int, x: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("getMiniGameResult--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(61)
        mplew.write(type)
        game.setPoints(x, type)
        if type != 0:
            game.setPoints((x != 1) ? 1 : 0, (type != 2) ? 1 : 0)
        if type != 1:
            if type == 0:
                mplew.write((x != 1) ? 1 : 0)
            else:
                mplew.write(x)
        addGameInfo(mplew, game.getMCOwner(), game)
        for visitorz in game.getVisitors():
            addGameInfo(mplew, visitorz.right, game)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def MerchantVisitorView(self, visitor: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("MerchantVisitorView--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(44)
        mplew.writeShort(visitor)
        for visit in visitor:
            mplew.writeMapleAsciiString(visit)
            mplew.writeInt(1)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def MerchantBlackListView(self, blackList: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("MerchantBlackListView--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(45)
        mplew.writeShort(blackList)
        for i in range(blackList):
            if blackList.get(i) is not None:
                mplew.writeMapleAsciiString(blackList.get(i))
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def sendHiredMerchantMessage(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("sendHiredMerchantMessage--------------------")
        mplew.writeShort(SendPacketOpcode.MERCH_ITEM_MSG.getValue())
        mplew.write(type)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def shopMessage(self, type: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("shopMessage--------------------")
        mplew.writeShort(SendPacketOpcode.PLAYER_INTERACTION.getValue())
        mplew.write(type)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

