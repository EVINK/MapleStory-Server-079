"""
CashShopOperation - Converted from Java source
Original: handling/cashshop/handler/CashShopOperation.java
Package: handling.cashshop.handler
"""

from pymysql import Error
from socket import socket
from typing import Dict
from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.OtherSettings import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.CharacterTransfer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.CashItemFactory import *  # TODO: import specific classes
# from server.CashItemInfo import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class CashShopOperation:
    """
    Class CashShopOperation
    """


    def LeaveCS(self, slea: Any, c: Any, chr: Any) -> None:
        socket = c.getChannelServer().getIP().split(":")
        CashShopServer.getPlayerStorageMTS().deregisterPlayer(chr)
        CashShopServer.getPlayerStorage().deregisterPlayer(chr)
        ip = c.getSessionIPAddress()
        LoginServer.putLoginAuth(chr.getId(), ip[ip.find(47:] + 1, ip), c.getTempIP(), c.getChannel())
        c.updateLoginState(1, ip)
        try:
            chr.saveToDB(False, True)
            c.setReceiving(False)
            World.ChannelChange_Data(CharacterTransfer(chr), chr.getId(), c.getChannel())
            c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(ChannelServer.getInstance(c.getChannel()).getIP().split(":")[1])))
        catch (NumberFormatException | UnknownHostException ex2)
            raise RuntimeError(ex2)

    def EnterCS(self, playerid: int, c: Any) -> None:
        transfer = CashShopServer.getPlayerStorage().getPendingCharacter(playerid)
        mts = False
        if transfer is None:
            transfer = CashShopServer.getPlayerStorageMTS().getPendingCharacter(playerid)
            mts = True
            if transfer is None:
                c.getSession().close(True)
                return
        chr = MapleCharacter.ReconstructChr(transfer, c, False)
        c.setPlayer(chr)
        c.setAccID(chr.getAccountID())
        state = c.getLoginState()
        allowLogin = False
        if (state == MapleClient.LOGIN_SERVER_TRANSITION or state == MapleClient.CHANGE_CHANNEL) and not World.isCharacterListConnected(c.loadCharacterNames(c.getWorld())):
            allowLogin = True
        if not allowLogin:
            c.setPlayer(None)
            c.getSession().close(True)
            return
        c.updateLoginState(MapleClient.LOGIN_LOGGEDIN, c.getSessionIPAddress())
        if mts:
            CashShopServer.getPlayerStorage().registerPlayer(chr)
            c.getSession().write(MTSCSPacket.warpCS(c))
            CSUpdate(c)
        else:
            CashShopServer.getPlayerStorage().registerPlayer(chr)
            c.getSession().write(MTSCSPacket.warpCSS(c))
            CSUpdate(c)

    def CSUpdate(self, c: Any) -> None:
        c.sendPacket(MTSCSPacket.showCashInventory(c))
        c.getSession().write(MTSCSPacket.sendWishList(c.getPlayer(), False))
        c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
        c.getSession().write(MTSCSPacket.getCSGifts(c))

    def TouchingCashShop(self, c: Any) -> None:
        c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))

    def CouponCode(self, code: str, c: Any) -> None:
        validcode = False
        type = -1
        item = -1
        try:
            validcode = MapleCharacterUtil.getNXCodeValid(code.upper(), validcode)
        except Exception as e:
            e.printStackTrace()
        if validcode:
            try:
                type = MapleCharacterUtil.getNXCodeType(code)
                item = MapleCharacterUtil.getNXCodeItem(code)
            except Exception as e:
                e.printStackTrace()
            if type != 4:
                try:
                    MapleCharacterUtil.setNXCodeUsed(c.getPlayer().getName(), code)
                except Exception as e:
                    e.printStackTrace()
            itemz = {}
            maplePoints = 0
            mesos = 0
            # switch (type):
                # case 1:
                # case 2:
                    c.getPlayer().modifyCSPoints(type, item, False)
                    maplePoints = item
                    break
                # case 3:
                    itez = CashItemFactory.getInstance().getItem(item)
                    if itez is None:
                        c.getSession().write(MTSCSPacket.sendCSFail(0))
                        doCSPackets(c)
                        return
                    slot = MapleInventoryManipulator.addId(c, itez.getId(), 1, "", 0)
                    if slot <= -1:
                        c.getSession().write(MTSCSPacket.sendCSFail(0))
                        doCSPackets(c)
                        return
                    itemz.put(item, c.getPlayer().getInventory(GameConstants.getInventoryType(item)).getItem(slot))
                    break
                # case 4:
                    c.getPlayer().modifyCSPoints(1, item, False)
                    maplePoints = item
                    break
                # case 5:
                    c.getPlayer().gainMeso(item, False)
                    mesos = item
                    break
            c.getSession().write(MTSCSPacket.showCouponRedeemedItem(itemz, mesos, maplePoints, c))
        else:
            c.getSession().write(MTSCSPacket.sendCSFail(validcode ? 165 : 167))
        doCSPackets(c)

    def BuyCashItem(self, slea: Any, c: Any, chr: Any) -> None:
        item_id = OtherSettings()
        itembp_id = item_id.getItempb_id()
        itemjy_id = item_id.getItemjy_id()
        action = slea.readByte()
        # switch (action):
            # case 3:
                useNX = slea.readByte() + 1
                snCS = slea.readInt()
                item = CashItemFactory.getInstance().getItem(snCS)
                ii = MapleItemInformationProvider.getInstance()
                if item is None:
                    chr.dropMessage(1, "该物品暂未开放！")
                    doCSPackets(c)
                    return
                for i in range(len(itembp_id)):
                    if item.getId() == int(itembp_id[i]):
                        c.getPlayer().dropMessage(1, "这个物品是禁止购买的.")
                        doCSPackets(c)
                        return
                if item.getPrice() < 100:
                    c.getPlayer().dropMessage(1, "价格(" + item.getPrice() + ")低于100点卷的物品是禁止购买的.")
                    doCSPackets(c)
                    return
                if item is not None and chr.getCSPoints(useNX) >= item.getPrice():
                    if not ii.isCash(item.getId()):
                        if c.getPlayer().getInventory(GameConstants.getInventoryType(item.getId())).getNextFreeSlot() < 0:
                            chr.dropMessage(1, "背包没空位了！")
                            doCSPackets(c)
                            return
                        pos = MapleInventoryManipulator.addId(c, item.getId(), item.getCount(), None, item.getPeriod(), 0)
                        if pos < 0:
                            chr.dropMessage(1, "背包坐标出错！\r\n可能是背包没空位了！")
                            doCSPackets(c)
                            return
                        chr.modifyCSPoints(useNX, -item.getPrice(), False)
                        chr.dropMessage(1, "购买成功！\r\n物品自动放入了背包！")
                    else:
                        chr.modifyCSPoints(useNX, -item.getPrice(), False)
                        if item.getPrice() < 100:
                            c.getPlayer().dropMessage(1, "价格低于100点卷的物品是禁止购买的.")
                            doCSPackets(c)
                            return
                        itemz = chr.getCashInventory().toItem(item)
                        if itemz is not None and itemz.getUniqueId() > 0 and itemz.getItemId() == item.getId() and itemz.getQuantity() == item.getCount():
                            if useNX == 1:
                                flag = itemz.getFlag()
                                交易 = True
                                for j in range(len(itemjy_id)):
                                    if itemz.getItemId() == int(itemjy_id[j]):
                                        交易 = False
                                if 交易:
                                    if itemz.getType() == MapleInventoryType.EQUIP.getType():
                                        flag |= ItemFlag.KARMA_EQ.getValue()
                                    else:
                                        flag |= ItemFlag.KARMA_USE.getValue()
                                    itemz.setFlag(flag)
                            chr.getCashInventory().addToInventory(itemz)
                            c.getSession().write(MTSCSPacket.showBoughtCSItem(itemz, item.getSN(), c.getAccID()))
                        else:
                            c.getSession().write(MTSCSPacket.sendCSFail(0))
                else:
                    c.getSession().write(MTSCSPacket.sendCSFail(0))
                c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 4:
            # case 32:
                snCS2 = slea.readInt()
                type = slea.readByte() + 1
                recipient = slea.readMapleAsciiString()
                message = slea.readMapleAsciiString()
                item2 = CashItemFactory.getInstance().getItem(snCS2)
                itemz2 = chr.getCashInventory().toItem(item2)
                if c.getPlayer().isAdmin():
                    print("包裹购买 ID: " + snCS2)
                if item2.getPrice() < 100:
                    c.getPlayer().dropMessage(1, "价格低于100点卷的物品是禁止购买的.")
                    doCSPackets(c)
                    return
                if itemz2 is None or itemz2.getUniqueId() <= 0 or itemz2.getItemId() != item2.getId() or itemz2.getQuantity() != item2.getCount():
                    c.getPlayer().dropMessage(1, "这个物品是禁止购买的.")
                    doCSPackets(c)
                    break
                if item2 is None or c.getPlayer().getCSPoints(type) < item2.getPrice() or message > 73 or message < 1:
                    c.getSession().write(MTSCSPacket.sendCSFail(0))
                    doCSPackets(c)
                    return
                info = MapleCharacterUtil.getInfoByName(recipient, c.getPlayer().getWorld())
                if info is None or info.getLeft() <= 0 or info.getLeft() == c.getPlayer().getId() or info.getRight().getLeft() == c.getAccID():
                    c.getSession().write(MTSCSPacket.sendCSFail(162))
                    doCSPackets(c)
                    return
                if not item2.genderEquals(info.getRight().getRight()):
                    c.getSession().write(MTSCSPacket.sendCSFail(163))
                    doCSPackets(c)
                    return
                c.getPlayer().getCashInventory().gift(info.getLeft(), c.getPlayer().getName(), message, item2.getSN(), MapleInventoryIdentifier.getInstance())
                c.getPlayer().modifyCSPoints(type, -item2.getPrice(), False)
                c.getSession().write(MTSCSPacket.sendGift(item2.getId(), item2.getCount(), recipient))
                break
            # case 5:
                chr.clearWishlist()
                if slea.available() < 40:
                    c.getSession().write(MTSCSPacket.sendCSFail(0))
                    doCSPackets(c)
                    return
                wishlist = new int[10]
                for k in range(10):
                    wishlist[k] = slea.readInt()
                chr.setWishlist(wishlist)
                c.getSession().write(MTSCSPacket.sendWishList(chr, True))
                break
            # case 6:
                yue = slea.readByte() + 1
                youhuijia = slea.readByte() > 0
                if youhuijia:
                    snCS3 = slea.readInt()
                    types = 1
                    # switch (snCS3):
                        # case 50200018:
                            types = 1
                            break
                        # case 50200019:
                            types = 2
                            break
                        # case 50200020:
                            types = 3
                            break
                        # case 50200021:
                            types = 4
                            break
                        # case 50200043:
                            types = 5
                            break
                    type2 = MapleInventoryType.getByType(types)
                    if chr.isAdmin():
                        print("增加道具栏 snCS " + snCS3 + " 扩充: " + types)
                    if chr.getCSPoints(yue) >= 1100 and chr.getInventory(type2).getSlotLimit() < 96:
                        chr.modifyCSPoints(yue, -1100, False)
                        chr.getInventory(type2).addSlot(8)
                        chr.dropMessage(1, "扩充" + snCS3 + "成功，当前栏位: " + chr.getInventory(type2).getSlotLimit() + " 个。")
                        RefreshCashShop(c)
                        chr.getStorage().saveToDB()
                    else:
                        chr.dropMessage(1, "扩充" + snCS3 + "失败，点卷余额不足或者栏位已超过上限。")
                    break
                type3 = MapleInventoryType.getByType(slea.readByte())
                if chr.getCSPoints(yue) >= 600 and chr.getInventory(type3).getSlotLimit() < 96:
                    chr.modifyCSPoints(yue, -600, False)
                    chr.getInventory(type3).addSlot(4)
                    chr.dropMessage(1, "背包已增加到 " + chr.getInventory(type3).getSlotLimit() + " 个。")
                    RefreshCashShop(c)
                    chr.getStorage().saveToDB()
                else:
                    chr.dropMessage(1, "扩充失败，点卷余额不足或者栏位已达到上限。")
                    c.getSession().write(MTSCSPacket.sendCSFail(164))
                break
            # case 7:
                yue = slea.readByte() + 1
                youhuijia2 = (slea.readByte() > 0) ? 2 : 1
                if chr.getCSPoints(yue) >= ((youhuijia2 == 2) ? 1100 : 600) and chr.getStorage().getSlots() < 97 - 4 * youhuijia2:
                    chr.modifyCSPoints(yue, (youhuijia2 == 2) ? -1100 : -600, False)
                    chr.getStorage().increaseSlots((byte)(4 * youhuijia2))
                    chr.getStorage().saveToDB()
                    chr.dropMessage(1, "仓库扩充成功，当前栏位: " + chr.getStorage().getSlots() + " 个。")
                    RefreshCashShop(c)
                    break
                chr.dropMessage(1, "仓库扩充失败，点卷余额不足或者栏位已超过上限 96 个位置。")
                break
            # case 8:
                useNX2 = slea.readByte() + 1
                item2 = CashItemFactory.getInstance().getItem(slea.readInt())
                slots = c.getCharacterSlots()
                if slots >= LoginServer.getMaxCharacters():
                    chr.dropMessage(1, "角色列表已满无法增加！")
                if item2 is None or c.getPlayer().getCSPoints(useNX2) < item2.getPrice() or slots > LoginServer.getMaxCharacters():
                    c.getSession().write(MTSCSPacket.sendCSFail(0))
                    doCSPackets(c)
                    return
                c.getPlayer().modifyCSPoints(useNX2, -item2.getPrice(), False)
                if c.gainCharacterSlot():
                    c.getSession().write(MTSCSPacket.increasedStorageSlots(slots + 1))
                    chr.dropMessage(1, "角色列表已增加到：" + c.getCharacterSlots() + "个")
                    break
                c.getSession().write(MTSCSPacket.sendCSFail(0))
                break
            # case 13:
                uniqueid = slea.readInt()
                slea.readInt()
                slea.readByte()
                type4 = slea.readByte()
                unknown = slea.readByte()
                item3 = c.getPlayer().getCashInventory().findByCashId(uniqueid)
                if item3 is not None and item3.getQuantity() > 0 and MapleInventoryManipulator.checkSpace(c, item3.getItemId(), item3.getQuantity(), item3.getOwner()):
                    item_ = item3.copy()
                    slot = MapleInventoryManipulator.addbyItem(c, item_, True)
                    if slot >= 0:
                        if item_.getPet() is not None:
                            item_.getPet().setInventoryPosition(type4)
                            c.getPlayer().addPet(item_.getPet())
                        c.getPlayer().getCashInventory().removeFromInventory(item3)
                        c.getSession().write(MTSCSPacket.confirmFromCSInventory(item_, type4))
                    else:
                        c.getSession().write(MaplePacketCreator.serverNotice(1, "您的包裹已满."))
                    break
                c.getSession().write(MaplePacketCreator.serverNotice(1, "放入背包错误A." + item3))
                break
            # case 14:
                uniqueid = slea.readLong()
                type5 = MapleInventoryType.getByType(slea.readByte())
                item4 = c.getPlayer().getInventory(type5).findByUniqueId(uniqueid)
                if item4 is not None and item4.getQuantity() > 0 and item4.getUniqueId() > 0 and c.getPlayer().getCashInventory().getItemsSize() < 100:
                    item_2 = item4.copy()
                    c.getPlayer().getInventory(type5).removeItem(item4.getPosition(), item4.getQuantity(), False)
                    sn = CashItemFactory.getInstance().getItemSN(item_2.getItemId())
                    if item_2.getPet() is not None:
                        c.getPlayer().removePet(item_2.getPet())
                    item_2.setPosition(0)
                    item_2.setGMLog("购物商场购买: " + FileoutputUtil.CurrentReadable_Time())
                    c.getPlayer().getCashInventory().addToInventory(item_2)
                    c.sendPacket(MTSCSPacket.confirmToCSInventory(item4, c.getAccID(), sn))
                else:
                    c.sendPacket(MTSCSPacket.sendCSFail(177))
                RefreshCashShop(c)
                break
            # case 29:
            # case 36:
                sn2 = slea.readInt()
                if sn2 == 209000310:
                    sn2 = 20900026
                item2 = CashItemFactory.getInstance().getItem(sn2)
                partnerName = slea.readMapleAsciiString()
                msg = slea.readMapleAsciiString()
                itemz3 = chr.getCashInventory().toItem(item2)
                for l in range(len(itembp_id)):
                    if item2.getId() == int(itembp_id[l]):
                        c.getPlayer().dropMessage(1, "这个物品是禁止购买的.")
                        doCSPackets(c)
                        return
                if item2 is None or not GameConstants.isEffectRing(item2.getId()) or c.getPlayer().getCSPoints(1) < item2.getPrice() or msg > 73 or msg < 1:
                    chr.dropMessage(1, "购买戒指错误：\r\n你没有足够的点卷或者该物品不存在。。")
                    doCSPackets(c)
                    return
                if not item2.genderEquals(c.getPlayer().getGender()):
                    chr.dropMessage(1, "购买戒指错误：B\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                if c.getPlayer().getCashInventory().getItemsSize() >= 100:
                    chr.dropMessage(1, "购买戒指错误：C\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                if (item2.getPrice() == 2990) {}
                info2 = MapleCharacterUtil.getInfoByName(partnerName, c.getPlayer().getWorld())
                if info2 is None or info2.getLeft() <= 0 or info2.getLeft() == c.getPlayer().getId():
                    chr.dropMessage(1, "购买戒指错误：D\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                if info2.getRight().getLeft() == c.getAccID():
                    chr.dropMessage(1, "购买戒指错误：E\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                if info2.getRight().getRight() == c.getPlayer().getGender() and action == 29:
                    chr.dropMessage(1, "购买戒指错误：F\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                err = MapleRing.createRing(item2.getId(), c.getPlayer(), partnerName, msg, info2.getLeft(), item2.getSN())
                if err != 1:
                    chr.dropMessage(1, "购买戒指错误：G\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                c.getPlayer().modifyCSPoints(1, -item2.getPrice(), False)
                c.getSession().write(MTSCSPacket.商城送礼物(item2.getId(), item2.getCount(), partnerName))
                chr.sendNote(partnerName, partnerName + " 您已收到" + chr.getName() + "送给您的礼物，请进入现金商城查看！")
                chz = World.Find.findChannel(partnerName)
                if chz > 0:
                    receiver = ChannelServer.getInstance(chz).getPlayerStorage().getCharacterByName(partnerName)
                    if receiver is not None:
                        receiver.showNote()
                doCSPackets(c)
                return
            # case 31:
                type6 = slea.readByte() + 1
                snID = slea.readInt()
                item5 = CashItemFactory.getInstance().getItem(snID)
                for m in range(len(itembp_id)):
                    if snID == int(itembp_id[m]):
                        c.getPlayer().dropMessage(1, "这个物品是禁止购买的.")
                        doCSPackets(c)
                        return
                if c.getPlayer().isAdmin():
                    print("礼包购买 ID: " + snID)
                # switch (snID):
                    # case 10001818:
                        c.getPlayer().dropMessage(1, "这个物品是禁止购买的.")
                        doCSPackets(c)
                        break
                ccc = None
                if item5 is not None:
                    ccc = CashItemFactory.getInstance().getPackageItems(item5.getId())
                if item5 is None or ccc is None or c.getPlayer().getCSPoints(type6) < item5.getPrice():
                    chr.dropMessage(1, "购买礼包错误：\r\n你没有足够的点卷或者该物品不存在。")
                    doCSPackets(c)
                    return
                if not item5.genderEquals(c.getPlayer().getGender()):
                    chr.dropMessage(1, "购买礼包错误：B\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                if c.getPlayer().getCashInventory().getItemsSize() >= 100 - ccc:
                    chr.dropMessage(1, "购买礼包错误：C\r\n请联系GM！。")
                    doCSPackets(c)
                    return
                ccz = {}
                for i2 in ccc:
                    for iz in GameConstants.cashBlock:
                        if (i2.getId() == iz) {}
                    itemz4 = chr.getCashInventory().toItem(i2, chr, MapleInventoryManipulator.getUniqueId(i2.getId(), None), "")
                    if itemz4 is not None and itemz4.getUniqueId() > 0:
                        if itemz4.getItemId() != i2.getId():
                            continue
                        ccz.put(i2.getSN(), itemz4)
                        c.getPlayer().getCashInventory().addToInventory(itemz4)
                        c.getSession().write(MTSCSPacket.showBoughtCSItem(itemz4, item5.getSN(), c.getAccID()))
                chr.modifyCSPoints(type6, -item5.getPrice(), False)
                break
            # case 42:
                snCS3 = slea.readInt()
                if snCS3 == 50200031 and c.getPlayer().getCSPoints(1) >= 500:
                    c.getPlayer().modifyCSPoints(1, -500)
                    c.getPlayer().modifyCSPoints(2, 500)
                    c.getSession().write(MaplePacketCreator.serverNotice(1, "兑换500抵用卷成功"))
                elif snCS3 == 50200032 and c.getPlayer().getCSPoints(1) >= 1000:
                    c.getPlayer().modifyCSPoints(1, -1000)
                    c.getPlayer().modifyCSPoints(2, 1000)
                    c.getSession().write(MaplePacketCreator.serverNotice(1, "兑换抵1000用卷成功"))
                elif snCS3 == 50200033 and c.getPlayer().getCSPoints(1) >= 5000:
                    c.getPlayer().modifyCSPoints(1, -5000)
                    c.getPlayer().modifyCSPoints(2, 5000)
                    c.getSession().write(MaplePacketCreator.serverNotice(1, "兑换5000抵用卷成功"))
                else:
                    c.getSession().write(MaplePacketCreator.serverNotice(1, "没有找到这个道具的信息！\r\n或者你点卷不足无法兑换！"))
                c.getSession().write(MTSCSPacket.enableCSorMTS())
                c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 33:
                isMesoGMItem = 1
                if isMesoGMItem == 1:
                    chr.dropMessage(1, "禁止购买。")
                    c.getPlayer().saveToDB(True, True)
                    c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                item2 = CashItemFactory.getInstance().getItem(slea.readInt())
                if item2 is None or not MapleItemInformationProvider.getInstance().isQuestItem(item2.getId()):
                    c.getSession().write(MTSCSPacket.sendCSFail(0))
                    doCSPackets(c)
                    return
                if c.getPlayer().getMeso() < item2.getPrice():
                    c.getSession().write(MTSCSPacket.sendCSFail(184))
                    doCSPackets(c)
                    return
                if c.getPlayer().getInventory(GameConstants.getInventoryType(item2.getId())).getNextFreeSlot() < 0:
                    c.getSession().write(MTSCSPacket.sendCSFail(177))
                    doCSPackets(c)
                    return
                for iz2 in GameConstants.cashBlock:
                    if item2.getId() == iz2:
                        c.getPlayer().dropMessage(1, GameConstants.getCashBlockedMsg(item2.getId()))
                        doCSPackets(c)
                        return
                pos2 = MapleInventoryManipulator.addId(c, item2.getId(), item2.getCount(), None, 0)
                if pos2 < 0:
                    c.getSession().write(MTSCSPacket.sendCSFail(177))
                    doCSPackets(c)
                    return
                chr.gainMeso(-item2.getPrice(), False)
                c.getSession().write(MTSCSPacket.showBoughtCSQuestItem(item2.getPrice(), item2.getCount(), pos2, item2.getId()))
                break
            # default:
                c.getSession().write(MTSCSPacket.sendCSFail(0))
                break
        doCSPackets(c)

    def getInventoryType(self, id: int) -> Any:
        # switch (id):
            # case 50200075:
                return MapleInventoryType.EQUIP
            # case 50200074:
                return MapleInventoryType.USE
            # case 50200073:
                return MapleInventoryType.ETC
            # default:
                return MapleInventoryType.UNDEFINED

    def RefreshCashShop(self, c: Any) -> None:
        c.sendPacket(MTSCSPacket.showCashInventory(c))
        c.sendPacket(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
        c.sendPacket(MTSCSPacket.enableCSUse())
        c.getPlayer().getCashInventory().checkExpire(c)

    def doCSPackets(self, c: Any) -> None:
        c.getSession().write(MTSCSPacket.getCSInventory(c))
        c.getSession().write(MTSCSPacket.enableCSorMTS())
        c.getSession().write(MTSCSPacket.sendWishList(c.getPlayer(), False))
        c.getSession().write(MTSCSPacket.showNXMapleTokens(c.getPlayer()))
        c.getSession().write(MaplePacketCreator.enableActions())
        c.getPlayer().getCashInventory().checkExpire(c)

