"""
PlayerInteractionHandler - Converted from Java source
Original: handling/channel/handler/PlayerInteractionHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.OtherSettings import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleTrade import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.shops.HiredMerchant import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from server.shops.MapleMiniGame import *  # TODO: import specific classes
# from server.shops.MaplePlayerShop import *  # TODO: import specific classes
# from server.shops.MaplePlayerShopItem import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class PlayerInteractionHandler:
    """
    Class PlayerInteractionHandler
    """

    CREATE = 0
    INVITE_TRADE = 2
    DENY_TRADE = 3
    VISIT = 4
    CHAT = 6
    EXIT = 10
    OPEN = 11
    CASH_ITEM_INTER = 13
    SET_ITEMS = 14
    SET_MESO = 15
    CONFIRM_TRADE = 16
    TRADE_SOMETHING = 18
    PLAYER_SHOP_ADD_ITEM = 20
    BUY_ITEM_PLAYER_SHOP = 21
    MERCHANT_EXIT = 27
    ADD_ITEM = 31
    BUY_ITEM_HIREDMERCHANT = 32
    BUY_ITEM_STORE = 33
    REMOVE_ITEM = 35
    TAKE_ITEM_BACK = 36
    MAINTANCE_OFF = 37
    MAINTANCE_ORGANISE = 38
    CLOSE_MERCHANT = 39
    ADMIN_STORE_NAMECHANGE = 43
    VIEW_MERCHANT_VISITOR = 44
    VIEW_MERCHANT_BLACKLIST = 45
    MERCHANT_BLACKLIST_ADD = 46
    MERCHANT_BLACKLIST_REMOVE = 47
    REQUEST_TIE = 48
    ANSWER_TIE = 49


    @staticmethod
    def PlayerInteraction(slea: Any, c: Any, chr: Any) -> None:
        if chr is None:
            return
        action = slea.readByte()
        # switch (action):
            # case 0:
                createType = slea.readByte()
                if createType == 3:
                    MapleTrade.startTrade(chr)
                    break
                if createType != 1 and createType != 2 and createType != 4 and createType != 5:
                    break
                if createType == 4 and not chr.isAdmin():
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if chr.getMap().getMapObjectsInRange(chr.getPosition(), 20000.0, Arrays.asList(MapleMapObjectType.SHOP, MapleMapObjectType.HIRED_MERCHANT)) != 0:
                    chr.dropMessage(1, "你不可能在这里建立一个商店.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if (createType == 1 or createType == 2) and FieldLimitType.Minigames.check(chr.getMap().getFieldLimit()):
                    chr.dropMessage(1, "你不可以在这里使用的迷你游戏。")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                desc = slea.readMapleAsciiString()
                pass = ""
                if slea.readByte() > 0 and (createType == 1 or createType == 2):
                    pass = slea.readMapleAsciiString()
                if createType == 1 or createType == 2:
                    piece = slea.readByte()
                    itemId = (createType == 1) ? (4080000 + piece) : 4080100
                    if not chr.haveItem(itemId) or (c.getPlayer().getMapId() >= 910000001 and c.getPlayer().getMapId() <= 910000022):
                        return
                    game = MapleMiniGame(chr, itemId, desc, pass, createType)
                    game.setPieceType(piece)
                    chr.setPlayerShop(game)
                    game.setAvailable(True)
                    game.setOpen(True)
                    game.send(c)
                    chr.getMap().addMapObject(game)
                    game.update()
                else:
                    shop = c.getPlayer().getInventory(MapleInventoryType.CASH).getItem(slea.readShort())
                    if shop is None or shop.getQuantity() <= 0 or shop.getItemId() != slea.readInt() or c.getPlayer().getMapId() < 910000000 or c.getPlayer().getMapId() > 910000022:
                        return
                    if createType == 4:
                        mps = MaplePlayerShop(chr, shop.getItemId(), desc)
                        chr.setPlayerShop(mps)
                        chr.getMap().addMapObject(mps)
                        c.getSession().write(PlayerShopPacket.getPlayerStore(chr, True))
                    else:
                        merch = HiredMerchant(chr, shop.getItemId(), desc)
                        chr.setPlayerShop(merch)
                        chr.getMap().addMapObject(merch)
                        c.getSession().write(PlayerShopPacket.getHiredMerch(chr, merch, True))
                break
            # case 2:
                MapleTrade.inviteTrade(chr, chr.getMap().getCharacterById(slea.readInt()))
                break
            # case 3:
                MapleTrade.declineTrade(chr)
                break
            # case 13:
                类型 = slea.readByte()
                现金交易 = slea.readByte()
                if 类型 == 11 and 现金交易 == 5:
                    c.getPlayer().dropMessage(1, "请先放入一个不是现金物品的东西贩卖\r\n开启商店后管理商店放入现金物品！")
                    return
                未知类型 = slea.readInt()
                obid = slea.readInt()
                otherChar = c.getPlayer().getMap().getCharacterById(obid)
                ob = chr.getMap().getMapObject(obid, MapleMapObjectType.HIRED_MERCHANT)
                if 现金交易 == 6 and 类型 == 4 and c.getPlayer().getTrade() is not None and c.getPlayer().getTrade().getPartner() is not None:
                    MapleTrade.visit现金交易(chr, chr.getTrade().getPartner().getChr())
                    try:
                        c.getPlayer().dropMessage(6, "玩家 " + otherChar.getName() + " 接受现金交易邀请!")
                    except Exception as ex:
                        pass
                    break
                if 现金交易 == 6 and 类型 != 4:
                    MapleTrade.start现金交易(chr)
                    MapleTrade.invite现金交易(chr, otherChar)
                    c.getPlayer().dropMessage(6, "向玩家 " + otherChar.getName() + " 发送现金交易邀请!")
                    break
                if chr.getMap() is None:
                    break
                if ob is None:
                    ob = chr.getMap().getMapObject(obid, MapleMapObjectType.SHOP)
                if isinstance(ob, IMaplePlayerShop) and chr.getPlayerShop() is None:
                    ips = ob
                    if isinstance(ob, HiredMerchant):
                        merchant = ips
                        if merchant.isOwner(chr):
                            merchant.setOpen(False)
                            merchant.broadcastToVisitors(PlayerShopPacket.shopErrorMessage(13, 1), False)
                            merchant.removeAllVisitors(16, 0)
                            chr.setPlayerShop(ips)
                            c.getSession().write(PlayerShopPacket.getHiredMerch(chr, merchant, False))
                        elif not merchant.isOpen() or not merchant.isAvailable():
                            chr.dropMessage(1, "主人正在整理商店物品\r\n请稍后再度光临！")
                        elif ips.getFreeSlot() == -1:
                            chr.dropMessage(1, "商店人数已经满了,请稍后再进入")
                        elif merchant.isInBlackList(chr.getName()):
                            chr.dropMessage(1, "你被这家商店加入黑名单了,所以不能进入")
                        else:
                            chr.setPlayerShop(ips)
                            merchant.addVisitor(chr)
                            c.getSession().write(PlayerShopPacket.getHiredMerch(chr, merchant, False))
                    elif isinstance(ips, MaplePlayerShop) and (ips).isBanned(chr.getName()):
                        chr.dropMessage(1, "你被这家商店加入黑名单了,所以不能进入.")
                    elif ips.getFreeSlot() < 0 or ips.getVisitorSlot(chr) > -1 or not ips.isOpen() or not ips.isAvailable():
                        c.getSession().write(PlayerShopPacket.getMiniGameFull())
                    else:
                        if slea.available() > 0 and slea.readByte() > 0:
                            pass2 = slea.readMapleAsciiString()
                            if not pass2 == (ips.getPassword()):
                                c.getPlayer().dropMessage(1, "你输入的密码错误.请从新在试一次.")
                                return
                        elif ips.getPassword() > 0:
                            c.getPlayer().dropMessage(1, "你输入的密码错误.请从新在试一次.")
                            return
                        chr.setPlayerShop(ips)
                        ips.addVisitor(chr)
                        if isinstance(ips, MapleMiniGame):
                            (ips).send(c)
                        else:
                            c.getSession().write(PlayerShopPacket.getPlayerStore(chr, False))
                    break
                break
            # case 4:
                if chr.getTrade() is not None and chr.getTrade().getPartner() is not None:
                    MapleTrade.visitTrade(chr, chr.getTrade().getPartner().getChr())
                    break
                if chr.getMap() is not None:
                    obid2 = slea.readInt()
                    ob2 = chr.getMap().getMapObject(obid2, MapleMapObjectType.HIRED_MERCHANT)
                    if ob2 is None:
                        ob2 = chr.getMap().getMapObject(obid2, MapleMapObjectType.SHOP)
                    if isinstance(ob2, IMaplePlayerShop) and chr.getPlayerShop() is None:
                        ips2 = ob2
                        if isinstance(ob2, HiredMerchant):
                            merchant2 = ips2
                            if merchant2.isOwner(chr):
                                merchant2.setOpen(False)
                                merchant2.removeAllVisitors(16, 0)
                                chr.setPlayerShop(ips2)
                                c.getSession().write(PlayerShopPacket.getHiredMerch(chr, merchant2, False))
                            elif not merchant2.isOpen() or not merchant2.isAvailable():
                                chr.dropMessage(1, "这个商店正在整理或者是没有再贩卖东西")
                            elif ips2.getFreeSlot() == -1:
                                chr.dropMessage(1, "商店人数已经满了，请稍后在进入")
                            elif merchant2.isInBlackList(chr.getName()):
                                chr.dropMessage(1, "你已经被这家商店加入黑名单，所以不能进入")
                            else:
                                chr.setPlayerShop(ips2)
                                merchant2.addVisitor(chr)
                                c.getSession().write(PlayerShopPacket.getHiredMerch(chr, merchant2, False))
                        elif isinstance(ips2, MaplePlayerShop) and (ips2).isBanned(chr.getName()):
                            chr.dropMessage(1, "你被这家商店加入黑名单了,所以不能进入.")
                        elif ips2.getFreeSlot() < 0 or ips2.getVisitorSlot(chr) > -1 or not ips2.isOpen() or not ips2.isAvailable():
                            c.getSession().write(PlayerShopPacket.getMiniGameFull())
                        else:
                            if slea.available() > 0 and slea.readByte() > 0:
                                pass3 = slea.readMapleAsciiString()
                                if not pass3 == (ips2.getPassword()):
                                    c.getPlayer().dropMessage(1, "你输入的密码错误.请从新在试一次")
                                    return
                            elif ips2.getPassword() > 0:
                                c.getPlayer().dropMessage(1, "你输入的密码错误.请从新在试一次.")
                                return
                            chr.setPlayerShop(ips2)
                            ips2.addVisitor(chr)
                            if isinstance(ips2, MapleMiniGame):
                                (ips2).send(c)
                            else:
                                c.getSession().write(PlayerShopPacket.getPlayerStore(chr, False))
                    break
                break
            # case 6:
                if chr.getTrade() is not None:
                    chr.getTrade().chat(slea.readMapleAsciiString())
                    break
                if chr.getPlayerShop() is not None:
                    ips3 = chr.getPlayerShop()
                    ips3.broadcastToVisitors(PlayerShopPacket.shopChat(chr.getName() + " : " + slea.readMapleAsciiString(), ips3.getVisitorSlot(chr)))
                    break
                break
            # case 10:
                if chr.getTrade() is not None:
                    MapleTrade.cancelTrade(chr.getTrade(), chr.getClient())
                    break
                ips3 = chr.getPlayerShop()
                if ips3 is None:
                    return
                if not ips3.isAvailable() or (ips3.isOwner(chr) and ips3.getShopType() != 1) or (ips3.isOwner(chr) and ips3.getItems() == 0):
                    ips3.closeShop(True, ips3.isAvailable())
                else:
                    ips3.removeVisitor(chr)
                chr.setPlayerShop(None)
                NPCScriptManager.getInstance().dispose(c)
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 11:
                shop2 = chr.getPlayerShop()
                if shop2 is None or not shop2.isOwner(chr) or shop2.getShopType() >= 3:
                    break
                if not chr.getMap().allowPersonalShop():
                    c.getSession().close(True)
                    break
                if c.getChannelServer().isShutdown():
                    chr.dropMessage(1, "伺服器即将关闭所以不能整理商店.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    shop2.closeShop(shop2.getShopType() == 1, False)
                    return
                if shop2.getShopType() == 1:
                    merchant3 = shop2
                    merchant3.setStoreid(c.getChannelServer().addMerchant(merchant3))
                    merchant3.setOpen(True)
                    merchant3.setAvailable(True)
                    chr.getMap().broadcastMessage(PlayerShopPacket.spawnHiredMerchant(merchant3))
                    chr.setPlayerShop(None)
                    chr.setLastHM(int(time.time() * 1000))
                    break
                if shop2.getShopType() == 2:
                    shop2.setOpen(True)
                    shop2.setAvailable(True)
                    shop2.update()
                    break
                break
            # case 14:
                item_id = OtherSettings()
                itemgy_id = item_id.getItempb_id()
                ii = MapleItemInformationProvider.getInstance()
                ivType = MapleInventoryType.getByType(slea.readByte())
                item = chr.getInventory(ivType).getItem(slea.readShort())
                quantity = slea.readShort()
                targetSlot = slea.readByte()
                for i in range(len(itemgy_id)):
                    if item.getItemId() == int(itemgy_id[i]):
                        c.getPlayer().dropMessage(1, "这个物品是禁止雇佣贩卖的.")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                if chr.getTrade() is not None and item is not None and ((quantity <= item.getQuantity() and quantity >= 0) or GameConstants.is飞镖道具(item.getItemId()) or GameConstants.is子弹道具(item.getItemId())):
                    chr.getTrade().setItems(c, item, targetSlot, quantity)
                    break
                break
            # case 15:
                trade = chr.getTrade()
                if trade is not None:
                    trade.setMeso(slea.readInt())
                    break
                break
            # case 16:
                if chr.getTrade() is not None:
                    MapleTrade.completeTrade(chr)
                    break
                break
            # case 20:
            # case 31:
                type = MapleInventoryType.getByType(slea.readByte())
                slot = slea.readShort()
                bundles = slea.readShort()
                perBundle = slea.readShort()
                price = slea.readInt()
                if price <= 0 or bundles <= 0 or perBundle <= 0:
                    return
                shop3 = chr.getPlayerShop()
                if shop3 is None or not shop3.isOwner(chr) or isinstance(shop3, MapleMiniGame):
                    return
                ivItem = chr.getInventory(type).getItem(slot)
                ii2 = MapleItemInformationProvider.getInstance()
                if ivItem is None:
                    break
                check = bundles * perBundle
                if check > 32767 or check <= 0:
                    return
                bundles_perbundle = (short)(bundles * perBundle)
                if ivItem.getQuantity() >= bundles_perbundle:
                    flag = ivItem.getFlag()
                    if ItemFlag.UNTRADEABLE.check(flag) or ItemFlag.LOCK.check(flag):
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if (ii2.isDropRestricted(ivItem.getItemId()) or ii2.isAccountShared(ivItem.getItemId())) and not ItemFlag.KARMA_EQ.check(flag) and not ItemFlag.KARMA_USE.check(flag):
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if bundles_perbundle >= 50 and GameConstants.isUpgradeScroll(ivItem.getItemId()):
                        c.setMonitored(True)
                    if GameConstants.is飞镖道具(ivItem.getItemId()) or GameConstants.is子弹道具(ivItem.getItemId()):
                        MapleInventoryManipulator.removeFromSlot(c, type, slot, ivItem.getQuantity(), True)
                        sellItem = ivItem.copy()
                        shop3.addItem(MaplePlayerShopItem(sellItem, 1, price, sellItem.getFlag()))
                    else:
                        MapleInventoryManipulator.removeFromSlot(c, type, slot, bundles_perbundle, True)
                        sellItem = ivItem.copy()
                        sellItem.setQuantity(perBundle)
                        shop3.addItem(MaplePlayerShopItem(sellItem, bundles, price, sellItem.getFlag()))
                    c.getSession().write(PlayerShopPacket.shopItemUpdate(shop3))
                break
            # case 21:
            # case 32:
            # case 33:
                if chr.getTrade() is not None:
                    MapleTrade.completeTrade(chr)
                    break
                item2 = slea.readByte()
                quantity2 = slea.readShort()
                shop4 = chr.getPlayerShop()
                if shop4 is None or shop4.isOwner(chr) or isinstance(shop4, MapleMiniGame) or item2 >= shop4.getItems():
                    return
                tobuy = shop4.getItems().get(item2)
                if tobuy is None:
                    return
                check2 = tobuy.bundles * quantity2
                check3 = tobuy.price * quantity2
                check4 = tobuy.item.getQuantity() * quantity2
                if check2 <= 0 or check3 > 2147483647 or check3 <= 0 or check4 > 32767 or check4 < 0:
                    return
                if tobuy.bundles < quantity2 or (tobuy.bundles % quantity2 != 0 and GameConstants.isEquip(tobuy.item.getItemId())) or chr.getMeso() - check3 < 0 or chr.getMeso() - check3 > 2147483647 or shop4.getMeso() + check3 < 0 or shop4.getMeso() + check3 > 2147483647:
                    return
                if (quantity2 < 50 or tobuy.item.getItemId() == 2340000) {}
                shop4.buy(c, item2, quantity2)
                shop4.broadcastToVisitors(PlayerShopPacket.shopItemUpdate(shop4))
                break
            # case 35:
            # case 36:
                slot2 = slea.readShort()
                shop5 = chr.getPlayerShop()
                if shop5 is None or not shop5.isOwner(chr) or isinstance(shop5, MapleMiniGame) or shop5.getItems() <= 0 or shop5.getItems() <= slot2 or slot2 < 0:
                    return
                item3 = shop5.getItems().get(slot2)
                if item3 is not None and item3.bundles > 0:
                    item_get = item3.item.copy()
                    check2 = item3.bundles * item3.item.getQuantity()
                    if check2 <= 0 or check2 > 32767:
                        return
                    item_get.setQuantity(check2)
                    if item_get.getQuantity() >= 50 and GameConstants.isUpgradeScroll(item3.item.getItemId()):
                        c.setMonitored(True)
                    if MapleInventoryManipulator.checkSpace(c, item_get.getItemId(), item_get.getQuantity(), item_get.getOwner()):
                        MapleInventoryManipulator.addFromDrop(c, item_get, False)
                        item3.bundles = 0
                        shop5.removeFromSlot(slot2)
                c.getSession().write(PlayerShopPacket.shopItemUpdate(shop5))
                break
            # case 37:
                shop2 = chr.getPlayerShop()
                if shop2 is not None and isinstance(shop2, HiredMerchant) and shop2.isOwner(chr):
                    shop2.setOpen(True)
                    chr.setPlayerShop(None)
                    break
                break
            # case 38:
                imps = chr.getPlayerShop()
                if imps is None or not imps.isOwner(chr) or isinstance(imps, MapleMiniGame):
                    c.sendPacket(MaplePacketCreator.enableActions())
                    break
                for j in range(imps.getItems()):
                    if imps.getItems().get(j).bundles == 0:
                        imps.getItems().remove(j)
                if chr.getMeso() + imps.getMeso() < 0:
                    c.sendPacket(PlayerShopPacket.shopItemUpdate(imps))
                    break
                chr.gainMeso(imps.getMeso(), False)
                imps.setMeso(0)
                c.sendPacket(PlayerShopPacket.shopItemUpdate(imps))
                break
            # case 39:
                merchant4 = chr.getPlayerShop()
                if merchant4 is not None and merchant4.getShopType() == 1 and merchant4.isOwner(chr) and merchant4.isAvailable():
                    merchant4.removeAllVisitors(-1, -1)
                    merchant4.closeShop(True, True)
                    chr.setPlayerShop(None)
                    c.getPlayer().dropMessage(1, "请通过弗兰德里拿回剩余物品。")
                    break
                break
            # case 44:
                merchant4 = chr.getPlayerShop()
                if merchant4 is not None and merchant4.getShopType() == 1 and merchant4.isOwner(chr):
                    (merchant4).sendVisitor(c)
                    break
                break
            # case 45:
                merchant4 = chr.getPlayerShop()
                if merchant4 is not None and merchant4.getShopType() == 1 and merchant4.isOwner(chr):
                    (merchant4).sendBlackList(c)
                    break
                break
            # case 46:
                merchant4 = chr.getPlayerShop()
                if merchant4 is not None and merchant4.getShopType() == 1 and merchant4.isOwner(chr):
                    (merchant4).addBlackList(slea.readMapleAsciiString())
                    break
                break
            # case 47:
                merchant4 = chr.getPlayerShop()
                if merchant4 is not None and merchant4.getShopType() == 1 and merchant4.isOwner(chr):
                    (merchant4).removeBlackList(slea.readMapleAsciiString())
                    break
                break
            # case 50:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                game2.broadcastToVisitors(PlayerShopPacket.getMiniGameResult(game2, 0, game2.getVisitorSlot(chr)))
                game2.nextLoser()
                game2.setOpen(True)
                game2.update()
                game2.checkExitAfterGame()
                break
            # case 59:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                if not (ips3).isOpen():
                    break
                ips3.removeAllVisitors(3, 1)
                break
            # case 57:
            # case 58:
                ips3 = chr.getPlayerShop()
                if ips3 is not None and isinstance(ips3, MapleMiniGame):
                    game2 = ips3
                    if not game2.isOwner(chr) and game2.isOpen():
                        game2.setReady(game2.getVisitorSlot(chr))
                        game2.broadcastToVisitors(PlayerShopPacket.getMiniGameReady(game2.isReady(game2.getVisitorSlot(chr))))
                    break
                break
            # case 60:
                ips3 = chr.getPlayerShop()
                if ips3 is not None and isinstance(ips3, MapleMiniGame):
                    game2 = ips3
                    if game2.isOwner(chr) and game2.isOpen():
                        for k in range(1, ips3.getSize()):
                            if not game2.isReady(k):
                                return
                        game2.setGameType()
                        game2.shuffleList()
                        if game2.getGameType() == 1:
                            game2.broadcastToVisitors(PlayerShopPacket.getMiniGameStart(game2.getLoser()))
                        else:
                            game2.broadcastToVisitors(PlayerShopPacket.getMatchCardStart(game2, game2.getLoser()))
                        game2.setOpen(False)
                        game2.update()
                    break
                break
            # case 48:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                if game2.isOwner(chr):
                    game2.broadcastToVisitors(PlayerShopPacket.getMiniGameRequestTie(), False)
                else:
                    game2.getMCOwner().getClient().getSession().write(PlayerShopPacket.getMiniGameRequestTie())
                game2.setRequestedTie(game2.getVisitorSlot(chr))
                break
            # case 49:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                if game2.getRequestedTie() > -1 and game2.getRequestedTie() != game2.getVisitorSlot(chr):
                    if slea.readByte() > 0:
                        game2.broadcastToVisitors(PlayerShopPacket.getMiniGameResult(game2, 1, game2.getRequestedTie()))
                        game2.nextLoser()
                        game2.setOpen(True)
                        game2.update()
                        game2.checkExitAfterGame()
                    else:
                        game2.broadcastToVisitors(PlayerShopPacket.getMiniGameDenyTie())
                    game2.setRequestedTie(-1)
                break
            # case 53:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                if game2.isOwner(chr):
                    game2.broadcastToVisitors(PlayerShopPacket.getMiniGameRequestREDO(), False)
                else:
                    game2.getMCOwner().getClient().getSession().write(PlayerShopPacket.getMiniGameRequestREDO())
                game2.setRequestedTie(game2.getVisitorSlot(chr))
                break
            # case 54:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                if slea.readByte() > 0:
                    ips3.broadcastToVisitors(PlayerShopPacket.getMiniGameSkip1(ips3.getVisitorSlot(chr)))
                    game2.nextLoser()
                else:
                    game2.broadcastToVisitors(PlayerShopPacket.getMiniGameDenyTie())
                game2.setRequestedTie(-1)
                break
            # case 62:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                ips3.broadcastToVisitors(PlayerShopPacket.getMiniGameSkip(ips3.getVisitorSlot(chr)))
                game2.nextLoser()
                break
            # case 63:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                game2.setPiece(slea.readInt(), slea.readInt(), slea.readByte(), chr)
                break
            # case 67:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                if slea.readByte() != game2.getTurn():
                    game2.broadcastToVisitors(PlayerShopPacket.shopChat("不能放在通过 " + chr.getName() + ". 失败者: " + game2.getLoser() + " 游客: " + game2.getVisitorSlot(chr) + " 是否為真: " + game2.getTurn(), game2.getVisitorSlot(chr)))
                    return
                slot3 = slea.readByte()
                turn = game2.getTurn()
                fs = game2.getFirstSlot()
                if turn == 1:
                    game2.setFirstSlot(slot3)
                    if game2.isOwner(chr):
                        game2.broadcastToVisitors(PlayerShopPacket.getMatchCardSelect(turn, slot3, fs, turn), False)
                    else:
                        game2.getMCOwner().getClient().getSession().write(PlayerShopPacket.getMatchCardSelect(turn, slot3, fs, turn))
                    game2.setTurn(0)
                    return
                if fs > 0 and game2.getCardId(fs + 1) == game2.getCardId(slot3 + 1):
                    game2.broadcastToVisitors(PlayerShopPacket.getMatchCardSelect(turn, slot3, fs, game2.isOwner(chr) ? 2 : 3))
                    game2.setPoints(game2.getVisitorSlot(chr))
                else:
                    game2.broadcastToVisitors(PlayerShopPacket.getMatchCardSelect(turn, slot3, fs, (int)(game2.isOwner(chr) ? 0 : 1)))
                    game2.nextLoser()
                game2.setTurn(1)
                game2.setFirstSlot(0)
                break
            # case 55:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                game2.broadcastToVisitors(PlayerShopPacket.getMiniGameResult(game2, 0, game2.getVisitorSlot(chr)))
                game2.nextLoser()
                game2.setOpen(True)
                game2.update()
                game2.checkExitAfterGame()
                break
            # case 56:
                ips3 = chr.getPlayerShop()
                if ips3 is None or not (isinstance(ips3, MapleMiniGame)):
                    break
                game2 = ips3
                if game2.isOpen():
                    break
                game2.setExitAfter(chr)
                game2.broadcastToVisitors(PlayerShopPacket.getMiniGameExitAfter(game2.isExitAfter(chr)))
                break

