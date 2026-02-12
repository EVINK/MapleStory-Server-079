"""
Equip - Converted from Java source
Original: client/inventory/Equip.java
Package: client.inventory
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from constants import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from server import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes


class Equip(Item, IEquip):
    """
    Class Equip
    Extends: Item
    Implements: IEquip, Serializable
    """

    def __init__(self, id: int, position: int):
        self.upgradeSlots = 0
        self.level = 0
        self.vicioushammer = 0
        self.enhance = 0
        self.str = 0
        self.dex = 0
        self._int = 0
        self.luk = 0
        self.hp = 0
        self.mp = 0
        self.watk = 0
        self.matk = 0
        self.wdef = 0
        self.mdef = 0
        self.acc = 0
        self.avoid = 0
        self.hands = 0
        self.speed = 0
        self.jump = 0
        self.potential1 = 0
        self.potential2 = 0
        self.potential3 = 0
        self.hpR = 0
        self.mpR = 0
        self.itemEXP = 0
        self.durability = 0
        self.itemLevel = 0
        super(id, position, 1, 0)
        self.upgradeSlots = 0
        self.level = 0
        self.vicioushammer = 0
        self.enhance = 0
        self.str = 0
        self.dex = 0
        self._int = 0
        self.luk = 0
        self.hp = 0
        self.mp = 0
        self.watk = 0
        self.matk = 0
        self.wdef = 0
        self.mdef = 0
        self.acc = 0
        self.avoid = 0
        self.hands = 0
        self.speed = 0
        self.jump = 0
        self.potential1 = 0
        self.potential2 = 0
        self.potential3 = 0
        self.hpR = 0
        self.mpR = 0
        self.itemEXP = 0
        self.durability = -1


    def copy(self) -> Any:
        ret = Equip(self.getItemId(), self.getPosition(), self.getUniqueId(), self.getFlag())
        ret.str = self.str
        ret.dex = self.dex
        ret._int = self._int
        ret.luk = self.luk
        ret.hp = self.hp
        ret.mp = self.mp
        ret.matk = self.matk
        ret.mdef = self.mdef
        ret.watk = self.watk
        ret.wdef = self.wdef
        ret.acc = self.acc
        ret.avoid = self.avoid
        ret.hands = self.hands
        ret.speed = self.speed
        ret.jump = self.jump
        ret.enhance = self.enhance
        ret.upgradeSlots = self.upgradeSlots
        ret.level = self.level
        ret.itemEXP = self.itemEXP
        ret.durability = self.durability
        ret.vicioushammer = self.vicioushammer
        ret.potential1 = self.potential1
        ret.potential2 = self.potential2
        ret.potential3 = self.potential3
        ret.hpR = self.hpR
        ret.mpR = self.mpR
        ret.itemLevel = self.itemLevel
        ret.setGiftFrom(self.getGiftFrom())
        ret.setOwner(self.getOwner())
        ret.setQuantity(self.getQuantity())
        ret.setExpiration(self.getExpiration())
        ret.setEquipOnlyId(self.getEquipOnlyId())
        return ret

    def getType(self) -> int:
        return 1

    def getUpgradeSlots(self) -> int:
        return self.upgradeSlots

    def getStr(self) -> int:
        return self.str

    def getDex(self) -> int:
        return self.dex

    def getInt(self) -> int:
        return self._int

    def getLuk(self) -> int:
        return self.luk

    def getHp(self) -> int:
        return self.hp

    def getMp(self) -> int:
        return self.mp

    def getWatk(self) -> int:
        return self.watk

    def getMatk(self) -> int:
        return self.matk

    def getWdef(self) -> int:
        return self.wdef

    def getMdef(self) -> int:
        return self.mdef

    def getAcc(self) -> int:
        return self.acc

    def getAvoid(self) -> int:
        return self.avoid

    def getHands(self) -> int:
        return self.hands

    def getSpeed(self) -> int:
        return self.speed

    def getJump(self) -> int:
        return self.jump

    def setStr(self, str: int) -> None:
        if str < 0:
            str = 0
        self.str = str

    def setDex(self, dex: int) -> None:
        if dex < 0:
            dex = 0
        self.dex = dex

    def setInt(self, _int: int) -> None:
        if _int < 0:
            _int = 0
        self._int = _int

    def setLuk(self, luk: int) -> None:
        if luk < 0:
            luk = 0
        self.luk = luk

    def setHp(self, hp: int) -> None:
        if hp < 0:
            hp = 0
        self.hp = hp

    def setMp(self, mp: int) -> None:
        if mp < 0:
            mp = 0
        self.mp = mp

    def setWatk(self, watk: int) -> None:
        if watk < 0:
            watk = 0
        self.watk = watk

    def setMatk(self, matk: int) -> None:
        if matk < 0:
            matk = 0
        self.matk = matk

    def setWdef(self, wdef: int) -> None:
        if wdef < 0:
            wdef = 0
        self.wdef = wdef

    def setMdef(self, mdef: int) -> None:
        if mdef < 0:
            mdef = 0
        self.mdef = mdef

    def setAcc(self, acc: int) -> None:
        if acc < 0:
            acc = 0
        self.acc = acc

    def setAvoid(self, avoid: int) -> None:
        if avoid < 0:
            avoid = 0
        self.avoid = avoid

    def setHands(self, hands: int) -> None:
        if hands < 0:
            hands = 0
        self.hands = hands

    def setSpeed(self, speed: int) -> None:
        if speed < 0:
            speed = 0
        self.speed = speed

    def setJump(self, jump: int) -> None:
        if jump < 0:
            jump = 0
        self.jump = jump

    def setUpgradeSlots(self, upgradeSlots: int) -> None:
        self.upgradeSlots = upgradeSlots

    def getLevel(self) -> int:
        return self.level

    def setLevel(self, level: int) -> None:
        self.level = level

    def getViciousHammer(self) -> int:
        return self.vicioushammer

    def setViciousHammer(self, ham: int) -> None:
        self.vicioushammer = ham

    def getItemEXP(self) -> int:
        return self.itemEXP

    def setItemEXP(self, itemEXP: int) -> None:
        if itemEXP < 0:
            itemEXP = 0
        self.itemEXP = itemEXP

    def getEquipExp(self) -> int:
        if self.itemEXP <= 0:
            return 0
        if GameConstants.isWeapon(self.getItemId()):
            return self.itemEXP / 700000
        return self.itemEXP / 350000

    def getEquipExpForLevel(self) -> int:
        if self.getEquipExp() <= 0:
            return 0
        expz = self.getEquipExp()
        for (int i = self.getBaseLevel(); i <= GameConstants.getMaxLevel(self.getItemId()) && expz >= GameConstants.getExpForLevel(i, self.getItemId()); expz -= GameConstants.getExpForLevel(i, self.getItemId()), ++i) {}
        return expz

    def getExpPercentage(self) -> int:
        return self.itemEXP

    def getEquipLevels(self) -> int:
        if GameConstants.getMaxLevel(self.getItemId()) <= 0:
            return 0
        if self.getEquipExp() <= 0:
            return self.getBaseLevel()
        levelz = self.getBaseLevel()
        expz = self.getEquipExp()
        i = levelz
        while True:
            if GameConstants.getStatFromWeapon(self.getItemId()) is None:
                if i > GameConstants.getMaxLevel(self.getItemId()):
                    break
            elif i >= GameConstants.getMaxLevel(self.getItemId()):
                break
            if expz < GameConstants.getExpForLevel(i, self.getItemId()):
                break
            levelz += 1
            expz -= GameConstants.getExpForLevel(i, self.getItemId())
            i += 1
        return levelz

    def getBaseLevel(self) -> int:
        return (GameConstants.getStatFromWeapon(self.getItemId()) is None) ? 1 : 0

    def setQuantity(self, quantity: int) -> None:
        if quantity < 0 || quantity > 1:
            raise RuntimeError("Setting the quantity to " + quantity + " on an equip (itemid: " + self.getItemId() + ")")
        super.setQuantity(quantity)

    def getDurability(self) -> int:
        return self.durability

    def setDurability(self, dur: int) -> None:
        self.durability = dur

    def getEnhance(self) -> int:
        return self.enhance

    def setEnhance(self, en: int) -> None:
        self.enhance = en

    def getPotential1(self) -> int:
        return self.potential1

    def setPotential1(self, en: int) -> None:
        self.potential1 = en

    def getPotential2(self) -> int:
        return self.potential2

    def setPotential2(self, en: int) -> None:
        self.potential2 = en

    def getPotential3(self) -> int:
        return self.potential3

    def setPotential3(self, en: int) -> None:
        self.potential3 = en

    def getState(self) -> int:
        pots = self.potential1 + self.potential2 + self.potential3
        if self.potential1 >= 30000 || self.potential2 >= 30000 || self.potential3 >= 30000:
            return 7
        if self.potential1 >= 20000 || self.potential2 >= 20000 || self.potential3 >= 20000:
            return 6
        if pots >= 1:
            return 5
        if pots < 0:
            return 1
        return 0

    def resetPotential(self) -> None:
        rank = (Randomizer.nextInt(100) < 4) ? ((Randomizer.nextInt(100) < 4) ? -7 : -6) : -5
        self.setPotential1(rank)
        self.setPotential2((short)((Randomizer.nextInt(10) == 1) ? rank : 0))
        self.setPotential3(0)

    def renewPotential(self) -> None:
        rank = (Randomizer.nextInt(100) < 4 && self.getState() != 7) ? (-(self.getState() + 1)) : (-self.getState())
        self.setPotential1(rank)
        self.setPotential2((short)((self.getPotential3() > 0) ? rank : 0))
        self.setPotential3(0)

    def getHpR(self) -> int:
        return self.hpR

    def setHpR(self, hp: int) -> None:
        self.hpR = hp

    def getMpR(self) -> int:
        return self.mpR

    def setMpR(self, mp: int) -> None:
        self.mpR = mp

    def gainItemLevel(self) -> None:
        self.itemLevel += 1

    def gainItemExp(self, c: Any, gain: int, timeless: bool) -> None:
        self.itemEXP += gain
        expNeeded = 0
        if timeless:
            expNeeded = ExpTable.getTimelessItemExpNeededForLevel(self.itemLevel + 1)
        else:
            expNeeded = ExpTable.getReverseItemExpNeededForLevel(self.itemLevel + 1)
        if self.itemEXP >= expNeeded:
            self.gainItemLevel(c, timeless)
            c.getSession().write(MaplePacketCreator.showItemLevelup())

    def gainItemLevel_c_timeless(self, c: Any, timeless: bool) -> None:
        stats = MapleItemInformationProvider.getInstance().getItemLevelupStats(self.getItemId(), self.itemLevel, timeless)
        for stat in stats:
            s = stat.getLeft()
            # switch (s):
                # case "incDEX":
                    self.dex += (short)stat.getRight()
                    continue
                # case "incSTR":
                    self.str += (short)stat.getRight()
                    continue
                # case "incINT":
                    self._int += (short)stat.getRight()
                    continue
                # case "incLUK":
                    self.luk += (short)stat.getRight()
                    continue
                # case "incMHP":
                    self.hp += (short)stat.getRight()
                    continue
                # case "incMMP":
                    self.mp += (short)stat.getRight()
                    continue
                # case "incPAD":
                    self.watk += (short)stat.getRight()
                    continue
                # case "incMAD":
                    self.matk += (short)stat.getRight()
                    continue
                # case "incPDD":
                    self.wdef += (short)stat.getRight()
                    continue
                # case "incMDD":
                    self.mdef += (short)stat.getRight()
                    continue
                # case "incEVA":
                    self.avoid += (short)stat.getRight()
                    continue
                # case "incACC":
                    self.acc += (short)stat.getRight()
                    continue
                # case "incSpeed":
                    self.speed += (short)stat.getRight()
                    continue
                # case "incJump":
                    self.jump += (short)stat.getRight()
                    continue
        self.itemLevel += 1
        c.getPlayer().getClient().getSession().write(MaplePacketCreator.showEquipmentLevelUp())
        c.getPlayer().getClient().getSession().write(MaplePacketCreator.updateSpecialItemUse(this, self.getType()))
        c.getPlayer().getClient().getSession().write(MaplePacketCreator.getCharInfo(c.getPlayer()))

    def setEquipLevel(self, gf: int) -> None:
        self.itemLevel = gf

    def getEquipLevel(self) -> int:
        return self.itemLevel

