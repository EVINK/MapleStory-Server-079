"""
PacketHelper - Converted from Java source
Original: tools/packet/PacketHelper.java
Package: tools.packet
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from datetime import timezone
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import math
import time

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCoolDownValueHolder import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillEntry import *  # TODO: import specific classes
# from client.inventory.IEquip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from server.shops.AbstractPlayerStore import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from tools.DateUtil import *  # TODO: import specific classes
# from tools.KoreanDateUtil import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class PacketHelper:
    """
    Class PacketHelper
    """

    FT_UT_OFFSET = 116444592000000000

    # Static initializer
    # PacketHelper.MAX_TIME = 150842304000000000
    # PacketHelper.unk1 = new byte[] { 0, 64, -32, -3 }
    # PacketHelper.unk2 = new byte[] { 59, 55, 79, 1 }


    @staticmethod
    def getKoreanTimestamp(realTimestamp: int) -> int:
        if realTimestamp == -1:
            return PacketHelper.MAX_TIME
        time = realTimestamp / 1000 / 60
        return time * 600000000 + 116444592000000000

    def getTime(self, realTimestamp: int) -> int:
        if realTimestamp == -1:
            return PacketHelper.MAX_TIME
        time = realTimestamp / 1000
        return time * 10000000 + 116444592000000000

    def getFileTimestamp(self, timeStampinMillis: int, roundToMinutes: bool) -> int:
        if TimeZone.getDefault().inDaylightTime(Date()):
            timeStampinMillis -= 3600000
        time = None
        if roundToMinutes:
            time = timeStampinMillis / 1000 / 60 * 600000000
        else:
            time = timeStampinMillis * 10000
        return time + 116444592000000000

    def addQuestInfo(self, mplew: Any, chr: Any) -> None:
        started = chr.getStartedQuests()
        mplew.writeShort(started)
        for q in started:
            mplew.writeShort(q.getQuest().getId())
            mplew.writeMapleAsciiString((q.getCustomData() is not None) ? q.getCustomData() : "")
        completed = chr.getCompletedQuests()
        mplew.writeShort(completed)
        for q2 in completed:
            mplew.writeShort(q2.getQuest().getId())
            time = KoreanDateUtil.getQuestTimestamp(q2.getCompletionTime())
            mplew.writeLong(time)

    def addSkillInfo(self, mplew: Any, chr: Any) -> None:
        skills = chr.getSkills()
        mplew.writeShort(skills)
        for (final Map.Entry<ISkill, SkillEntry> skill : skills.items())
            mplew.writeInt(skill.getKey().getId())
            mplew.writeInt(skill.getValue().skillevel)
            if skill.getKey().isFourthJob():
                mplew.writeInt(skill.getValue().masterlevel)

    def addCoolDownInfo(self, mplew: Any, chr: Any) -> None:
        cd = chr.getCooldowns()
        mplew.writeShort(cd)
        for cooling in cd:
            mplew.writeInt(cooling.skillId)
            mplew.writeShort((int)(len(cooling) + cooling.startTime - int(time.time() * 1000)) / 1000)

    def addRocksInfo(self, mplew: Any, chr: Any) -> None:
        mapz = chr.getRegRocks()
        for i in range(5):
            mplew.writeInt(mapz[i])
        map = chr.getRocks()
        for j in range(10):
            mplew.writeInt(map[j])

    def addMonsterBookInfo(self, mplew: Any, chr: Any) -> None:
        mplew.writeInt(chr.getMonsterBookCover())
        mplew.write(0)
        chr.getMonsterBook().addCardPacket(mplew)

    def addRingInfo(self, mplew: Any, chr: Any) -> None:
        mplew.writeShort(0)
        aRing = chr.getRings(True)
        cRing = aRing.getLeft()
        mplew.writeShort(cRing)
        for ring in cRing:
            mplew.writeInt(ring.getPartnerChrId())
            mplew.writeAsciiString(ring.getPartnerName(), 13)
            mplew.writeLong(ring.getRingId())
            mplew.writeLong(ring.getPartnerRingId())
        fRing = aRing.getRight()
        mplew.writeShort(fRing)
        for ring2 in fRing:
            mplew.writeInt(ring2.getPartnerChrId())
            mplew.writeAsciiString(ring2.getPartnerName(), 13)
            mplew.writeLong(ring2.getRingId())
            mplew.writeLong(ring2.getPartnerRingId())
            mplew.writeInt(ring2.getItemId())
        mplew.writeShort(0)

    def addInventoryInfo(self, mplew: Any, chr: Any) -> None:
        mplew.writeMapleAsciiString(chr.getName())
        mplew.writeInt(chr.getMeso())
        mplew.writeInt(chr.getId())
        mplew.writeInt(chr.getBeans())
        mplew.writeInt(0)
        mplew.write(chr.getInventory(MapleInventoryType.EQUIP).getSlotLimit())
        if ServerConstants.调试输出封包:
            print("-------背包装备格子数据输出：" + chr.getInventory(MapleInventoryType.EQUIP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.USE).getSlotLimit())
        if ServerConstants.调试输出封包:
            print("-------背包消耗格子数据输出：" + chr.getInventory(MapleInventoryType.USE).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.SETUP).getSlotLimit())
        if ServerConstants.调试输出封包:
            print("-------背包特殊格子数据输出：" + chr.getInventory(MapleInventoryType.SETUP).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.ETC).getSlotLimit())
        if ServerConstants.调试输出封包:
            print("-------背包其他格子数据输出：" + chr.getInventory(MapleInventoryType.ETC).getSlotLimit())
        mplew.write(chr.getInventory(MapleInventoryType.CASH).getSlotLimit())
        if ServerConstants.调试输出封包:
            print("-------背包现金格子数据输出：" + chr.getInventory(MapleInventoryType.CASH).getSlotLimit())
        mplew.writeLong(getTime(int(time.time() * 1000)))
        iv = chr.getInventory(MapleInventoryType.EQUIPPED)
        equippedC = iv.list()
        equipped = [])
        for item in equippedC:
            equipped.add(item)
        Collections.sort(equipped)
        for item2 in equipped:
            if item2.getPosition() < 0 and item2.getPosition() > -100:
                addItemInfo(mplew, item2, False, False)
        mplew.write(0)
        for item2 in equipped:
            if item2.getPosition() <= -100 and item2.getPosition() > -1000:
                addItemInfo(mplew, item2, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.EQUIP)
        for item in iv.list():
            addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.USE)
        for item in iv.list():
            addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.SETUP)
        for item in iv.list():
            addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.ETC)
        for item in iv.list():
            addItemInfo(mplew, item, False, False)
        mplew.write(0)
        iv = chr.getInventory(MapleInventoryType.CASH)
        for item in iv.list():
            addItemInfo(mplew, item, False, False)
        mplew.write(0)

    def addCharStats(self, mplew: Any, chr: Any) -> None:
        mplew.writeInt(chr.getId())
        mplew.writeAsciiString(chr.getName(), 13)
        mplew.write(chr.getGender())
        mplew.write(chr.getSkinColor())
        mplew.writeInt(chr.getFace())
        mplew.writeInt(chr.getHair())
        mplew.writeZeroBytes(24)
        mplew.write(chr.getLevel())
        mplew.writeShort(chr.getJob())
        chr.getStat().connectData(mplew)
        mplew.writeShort(chr.getRemainingAp())
        mplew.writeShort(chr.getRemainingSp())
        mplew.writeInt(chr.getExp())
        mplew.writeShort(chr.getFame())
        mplew.writeInt(0)
        mplew.writeLong(getTime(int(time.time() * 1000)))
        mplew.writeInt(chr.getMapId())
        mplew.write(chr.getInitialSpawnpoint())

    def addCharLook(self, mplew: Any, chr: Any, mega: bool) -> None:
        addCharLook(mplew, chr, mega, True)

    def addCharLook_mplew_chr_mega_channelserver(self, mplew: Any, chr: Any, mega: bool, channelserver: bool) -> None:
        mplew.write(chr.getGender())
        mplew.write(chr.getSkinColor())
        mplew.writeInt(chr.getFace())
        mplew.write(mega ? 0 : 1)
        mplew.writeInt(chr.getHair())
        myEquip = {}
        maskedEquip = {}
        equip = chr.getInventory(MapleInventoryType.EQUIPPED)
        for item in equip.list():
            if item.getPosition() < -128:
                continue
            pos = (byte)(item.getPosition() * -1)
            if pos < 100 and myEquip.get(pos) is None:
                myEquip.put(pos, item.getItemId())
            elif (pos > 100 or pos == -128) and pos != 111:
                pos = (byte)((pos == -128) ? 28 : (pos - 100))
                if myEquip.get(pos) is not None:
                    maskedEquip.put(pos, myEquip.get(pos))
                myEquip.put(pos, item.getItemId())
            else:
                if myEquip.get(pos) is None:
                    continue
                maskedEquip.put(pos, item.getItemId())
        for (final Map.Entry<Byte, Integer> entry : myEquip.items())
            mplew.write(entry.getKey())
            mplew.writeInt(entry.getValue())
        mplew.write(255)
        for (final Map.Entry<Byte, Integer> entry : maskedEquip.items())
            mplew.write(entry.getKey())
            mplew.writeInt(entry.getValue())
        mplew.write(255)
        cWeapon = equip.getItem((short)(-111))
        mplew.writeInt((cWeapon is not None) ? cWeapon.getItemId() : 0)
        for i in range(3):
            if channelserver:
                mplew.writeInt((chr.getPet(i) is not None) ? chr.getPet(i).getPetItemId() : 0)
            else:
                mplew.writeInt(0)

    def addExpirationTime(self, mplew: Any, time: int) -> None:
        mplew.write(0)
        mplew.writeShort(1408)
        if time != -1:
            mplew.writeInt(KoreanDateUtil.getItemTimestamp(time))
            mplew.write(1)
        else:
            mplew.writeInt(400967355)
            mplew.write(2)

    def addDDItemInfo(self, mplew: Any, item: Any, zeroPosition: bool, leaveOut: bool, cs: bool) -> None:
        pos = item.getPosition()
        if zeroPosition:
            if not leaveOut:
                mplew.write(0)
        elif pos <= -1:
            pos = (byte)(pos * -1)
            if pos > 100:
                mplew.write(pos - 100)
            else:
                mplew.write(pos)
        else:
            mplew.write(item.getPosition())
        mplew.write((byte)((item.getPet() is not None) ? 3 : item.getType()))
        mplew.writeInt(item.getItemId())
        hasUniqueId = item.getUniqueId() > 0
        mplew.write(hasUniqueId ? 1 : 0)
        if hasUniqueId:
            mplew.writeLong(item.getUniqueId())
        addExpirationTime(mplew, item.getExpiration())
        if item.getType() == 1:
            equip = item
            mplew.write(equip.getUpgradeSlots())
            mplew.write(equip.getLevel())
            mplew.writeShort(equip.getStr())
            mplew.writeShort(equip.getDex())
            mplew.writeShort(equip.getInt())
            mplew.writeShort(equip.getLuk())
            mplew.writeShort(equip.getHp())
            mplew.writeShort(equip.getMp())
            mplew.writeShort(equip.getWatk())
            mplew.writeShort(equip.getMatk())
            mplew.writeShort(equip.getWdef())
            mplew.writeShort(equip.getMdef())
            mplew.writeShort(equip.getAcc())
            mplew.writeShort(equip.getAvoid())
            mplew.writeShort(equip.getHands())
            mplew.writeShort(equip.getSpeed())
            mplew.writeShort(equip.getJump())
            mplew.writeMapleAsciiString(equip.getOwner())
            mplew.writeShort(equip.getFlag())
            mplew.write(0)
            mplew.write(0)
            mplew.writeShort(0)
            mplew.writeShort(0)
            mplew.write(0)
            mplew.write(0)
            mplew.writeLong(0)
            mplew.writeShort(0)
            mplew.writeShort(0)
            mplew.writeShort(0)
            mplew.writeLong(DateUtil.getFileTimestamp(int(time.time() * 1000)))
            mplew.writeInt(-1)
        else:
            mplew.writeShort(item.getQuantity())
            mplew.writeMapleAsciiString(item.getOwner())
            mplew.writeShort(0)
            if GameConstants.is飞镖道具(item.getItemId()) or GameConstants.is子弹道具(item.getItemId()):
                mplew.writeInt(2)
                mplew.writeShort(84)
                mplew.write(0)
                mplew.write(52)

    def addItemInfo(self, mplew: Any, item: Any, zeroPosition: bool, leaveOut: bool) -> None:
        addItemInfo(mplew, item, zeroPosition, leaveOut, False)

    def addItemInfo_mplew_item_zeroPosition_leaveOut_trade(self, mplew: Any, item: Any, zeroPosition: bool, leaveOut: bool, trade: bool) -> None:
        pos = item.getPosition()
        if zeroPosition:
            if not leaveOut:
                mplew.write(0)
        elif pos <= -1:
            pos = (byte)(pos * -1)
            if pos == -128:
                mplew.write(28)
            elif pos > 100:
                mplew.write(pos - 100)
            else:
                mplew.write(pos)
        else:
            mplew.write(item.getPosition())
        mplew.write((byte)((item.getPet() is not None) ? 3 : item.getType()))
        mplew.writeInt(item.getItemId())
        hasUniqueId = item.getUniqueId() > 0
        mplew.write(hasUniqueId ? 1 : 0)
        if hasUniqueId:
            mplew.writeLong(item.getUniqueId())
        if item.getPet() is not None:
            addPetItemInfo(mplew, item, item.getPet(), True)
        else:
            addExpirationTime(mplew, item.getExpiration())
            if item.getType() == 1:
                equip = item
                mplew.write(equip.getUpgradeSlots())
                mplew.write(equip.getLevel())
                mplew.writeShort(equip.getStr())
                mplew.writeShort(equip.getDex())
                mplew.writeShort(equip.getInt())
                mplew.writeShort(equip.getLuk())
                mplew.writeShort(equip.getHp())
                mplew.writeShort(equip.getMp())
                mplew.writeShort(equip.getWatk())
                mplew.writeShort(equip.getMatk())
                mplew.writeShort(equip.getWdef())
                mplew.writeShort(equip.getMdef())
                mplew.writeShort(equip.getAcc())
                mplew.writeShort(equip.getAvoid())
                mplew.writeShort(equip.getHands())
                mplew.writeShort(equip.getSpeed())
                mplew.writeShort(equip.getJump())
                mplew.writeMapleAsciiString(equip.getOwner())
                mplew.writeShort(equip.getFlag())
                if not hasUniqueId:
                    mplew.write(0)
                    mplew.write(max(equip.getBaseLevel(), equip.getEquipLevel()))
                    mplew.writeInt(equip.getExpPercentage())
                    mplew.writeInt(equip.getViciousHammer())
                    mplew.writeLong(0)
                else:
                    mplew.writeShort(0)
                    mplew.writeShort(0)
                    mplew.writeShort(0)
                    mplew.writeShort(0)
                    mplew.writeShort(0)
                if GameConstants.is豆豆装备(equip.getItemId()):
                    mplew.writeInt(0)
                    mplew.writeLong(DateUtil.getFileTimestamp(int(time.time() * 1000)))
                else:
                    addExpirationTime(mplew, item.getExpiration())
                mplew.writeInt(-1)
            else:
                mplew.writeShort(item.getQuantity())
                mplew.writeMapleAsciiString(item.getOwner())
                mplew.writeShort(item.getFlag())
                if GameConstants.isThrowingStar(item.getItemId()) or GameConstants.isBullet(item.getItemId()):
                    mplew.writeInt(2)
                    mplew.writeShort(84)
                    mplew.write(0)
                    mplew.write(52)

    def serializeMovementList(self, lew: Any, moves: list) -> None:
        lew.write(moves)
        for move in moves:
            move.serialize(lew)

    def addAnnounceBox(self, mplew: Any, chr: Any) -> None:
        if chr.getPlayerShop() is not None and chr.getPlayerShop().isOwner(chr) and chr.getPlayerShop().getShopType() != 1 and chr.getPlayerShop().isAvailable():
            addInteraction(mplew, chr.getPlayerShop())
        else:
            mplew.write(0)

    def addInteraction(self, mplew: Any, shop: Any) -> None:
        mplew.write(shop.getGameType())
        mplew.writeInt((shop).getObjectId())
        mplew.writeMapleAsciiString(shop.getDescription())
        if shop.getShopType() != 1:
            mplew.write((shop.getPassword() > 0) ? 1 : 0)
        mplew.write(shop.getItemId() % 10)
        mplew.write(shop.getSize())
        mplew.write(shop.getMaxSize())
        if shop.getShopType() != 1:
            mplew.write(shop.isOpen() ? 0 : 1)

    def addCharacterInfo(self, mplew: Any, chr: Any) -> None:
        mplew.writeLong(-1)
        mplew.write(0)
        addCharStats(mplew, chr)
        mplew.write(chr.getBuddylist().getCapacity())
        mplew.write(1)
        addInventoryInfo(mplew, chr)
        addSkillInfo(mplew, chr)
        addCoolDownInfo(mplew, chr)
        addQuestInfo(mplew, chr)
        addRingInfo(mplew, chr)
        addRocksInfo(mplew, chr)
        addMonsterBookInfo(mplew, chr)
        chr.QuestInfoPacket(mplew)
        mplew.writeInt(0)
        mplew.writeShort(0)

    def addPetItemInfo(self, mplew: Any, item: Any, pet: Any, active: bool) -> None:
        if item is None:
            mplew.writeLong(getKoreanTimestamp((long)(int(time.time() * 1000) * 1.5)))
        else:
            addExpirationTime(mplew, (item.getExpiration() <= int(time.time() * 1000)) ? -1 : item.getExpiration())
        mplew.writeAsciiString(pet.getName(), 13)
        mplew.write(pet.getLevel())
        mplew.writeShort(pet.getCloseness())
        mplew.write(pet.getFullness())
        if item is None:
            mplew.writeLong(getKoreanTimestamp((long)(int(time.time() * 1000) * 1.5)))
        else:
            addExpirationTime(mplew, (item.getExpiration() <= int(time.time() * 1000)) ? -1 : item.getExpiration())
        mplew.writeShort(0)
        mplew.writeShort(pet.getFlags())
        mplew.writeInt((pet.getPetItemId() == 5000054 and pet.getSecondsLeft() > 0) ? pet.getSecondsLeft() : 0)
        mplew.write(0)
        mplew.write((byte)(active ? (pet.getSummoned() ? pet.getSummonedValue() : 0) : 0))

    def addRingItemInfo(self, mplew: Any, item: Any, zeroPosition: bool, leaveOut: bool, cs: bool) -> None:
        ii = MapleItemInformationProvider.getInstance()
        ring = False
        equip = None
        if item.getType() == 1:
            equip = item
            if equip.getRing() is not None:
                ring = True
        pos = item.getPosition()
        masking = False
        equipped = False
        if zeroPosition:
            if not leaveOut:
                mplew.write(0)
        elif pos <= -1:
            pos *= -1
            if pos > 100 or pos == -128 or ring:
                masking = True
                mplew.write(pos - 100)
            else:
                mplew.write(pos)
            equipped = True
        else:
            mplew.write(item.getPosition())
        mplew.write(item.getType())
        mplew.writeInt(item.getItemId())
        mplew.write(1)
        mplew.writeInt(equip.getUniqueId())
        mplew.writeInt(0)
        mplew.writeLong(DateUtil.getFileTimestamp(item.getExpiration()))
        mplew.write(equip.getUpgradeSlots())
        mplew.write(equip.getLevel())
        mplew.writeShort(equip.getStr())
        mplew.writeShort(equip.getDex())
        mplew.writeShort(equip.getInt())
        mplew.writeShort(equip.getLuk())
        mplew.writeShort(equip.getHp())
        mplew.writeShort(equip.getMp())
        mplew.writeShort(equip.getWatk())
        mplew.writeShort(equip.getMatk())
        mplew.writeShort(equip.getWdef())
        mplew.writeShort(equip.getMdef())
        mplew.writeShort(equip.getAcc())
        mplew.writeShort(equip.getAvoid())
        mplew.writeShort(equip.getHands())
        mplew.writeShort(equip.getSpeed())
        mplew.writeShort(equip.getJump())
        mplew.writeMapleAsciiString(equip.getOwner())
        mplew.writeShort(0)
        mplew.writeShort(0)
        mplew.write(1)
        mplew.write(0)
        mplew.writeShort(0)
        mplew.writeShort(0)
        mplew.writeShort(0)
        mplew.writeLong(DateUtil.getFileTimestamp(int(time.time() * 1000)))
        mplew.writeInt(-1)

