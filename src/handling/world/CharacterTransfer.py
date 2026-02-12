"""
CharacterTransfer - Converted from Java source
Original: handling/world/CharacterTransfer.java
Package: handling.world
"""

from typing import Dict
from typing import List
from typing import Optional, Any
import math
import os
import time

# Internal module imports
# from client.BuddyEntry import *  # TODO: import specific classes
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillEntry import *  # TODO: import specific classes
# from client.inventory.MapleMount import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class CharacterTransfer(Externalizable):
    """
    Class CharacterTransfer
    Implements: Externalizable
    """

    def __init__(self):
        self.characterid = 0
        self.accountid = 0
        self.exp = 0
        self.shaguai = 0
        self.skillzq = 0
        self.bosslog = 0
        self.PGMaxDamage = 0
        self.jzname = 0
        self.mrsjrw = 0
        self.mrsgrw = 0
        self.mrsbossrw = 0
        self.mrfbrw = 0
        self.hythd = 0
        self.mrsgrwa = 0
        self.mrsbossrwa = 0
        self.mrfbrwa = 0
        self.mrsgrws = 0
        self.mrsbossrws = 0
        self.mrfbrws = 0
        self.mrsgrwas = 0
        self.mrsbossrwas = 0
        self.mrfbrwas = 0
        self.ddj = 0
        self.vip = 0
        self.vipexpired = 0
        self.djjl = 0
        self.qiandao = 0
        self.jf = 0
        self.beans = 0
        self.meso = 0
        self.hair = 0
        self.face = 0
        self.mapid = 0
        self.guildid = 0
        self.partyid = 0
        self.messengerid = 0
        self.mBookCover = 0
        self.dojo = 0
        self.ACash = 0
        self.MaplePoints = 0
        self.mbook = {}
        self.keymap = new LinkedHashMap<Integer, Pair<Byte, Integer>>()
        self.finishedAchievements = []
        self.famedcharacters = []
        self.buddies = {}
        self.Quest = {}
        self.InfoQuest = {}
        self.Skills = {}


    def readExternal(self, in: Any) -> None:
        self.lastGainHM = in.readLong()
        self.DebugMessage = in.readBoolean()
        self.characterid = in.readInt()
        self.accountid = in.readInt()
        self.accountname = in.readUTF()
        self.channel = in.readByte()
        self.ACash = in.readInt()
        self.MaplePoints = in.readInt()
        self.name = in.readUTF()
        self.fame = in.readShort()
        self.gender = in.readByte()
        self.level = in.readShort()
        self.str = in.readShort()
        self.dex = in.readShort()
        self.int_ = in.readShort()
        self.luk = in.readShort()
        self.hp = in.readShort()
        self.mp = in.readShort()
        self.maxhp = in.readShort()
        self.maxmp = in.readShort()
        self.exp = in.readInt()
        self.hpApUsed = in.readShort()
        self.remainingAp = in.readShort()
        self.remainingSp = new int[in.readByte()]
        for i in range(self.len(remainingSp)):
            self.remainingSp[i] = in.readInt()
        self.beans = in.readInt()
        self.meso = in.readInt()
        self.skinColor = in.readByte()
        self.job = in.readShort()
        self.hair = in.readInt()
        self.face = in.readInt()
        self.mapid = in.readInt()
        self.initialSpawnPoint = in.readByte()
        self.world = in.readByte()
        self.guildid = in.readInt()
        self.guildrank = in.readByte()
        self.alliancerank = in.readByte()
        self.gmLevel = in.readByte()
        self.points = in.readInt()
        self.vpoints = in.readInt()
        if in.readByte() == 1:
            self.BlessOfFairy = in.readUTF()
        else:
            self.BlessOfFairy = None
        if in.readByte() == 1:
            self.chalkboard = in.readUTF()
        else:
            self.chalkboard = None
        self.clonez = in.readByte()
        self.skillmacro = in.readObject()
        self.lastfametime = in.readLong()
        self.storage = in.readObject()
        self.cs = in.readObject()
        self.mount_itemid = in.readInt()
        self.mount_Fatigue = in.readByte()
        self.mount_level = in.readByte()
        self.mount_exp = in.readInt()
        self.partyid = in.readInt()
        self.messengerid = in.readInt()
        self.mBookCover = in.readInt()
        self.dojo = in.readInt()
        self.dojoRecord = in.readByte()
        self.inventorys = in.readObject()
        self.fairyExp = in.readByte()
        self.subcategory = in.readByte()
        self.marriageId = in.readInt()
        self.familyid = in.readInt()
        self.seniorid = in.readInt()
        self.junior1 = in.readInt()
        self.junior2 = in.readInt()
        self.currentrep = in.readInt()
        self.totalrep = in.readInt()
        self.charmessage = in.readUTF()
        self.expression = in.readByte()
        self.constellation = in.readInt()
        self.skillzq = in.readInt()
        self.bosslog = in.readInt()
        self.PGMaxDamage = in.readInt()
        self.jzname = in.readInt()
        self.mrfbrw = in.readInt()
        self.mrsbossrw = in.readInt()
        self.mrsgrw = in.readInt()
        self.mrsjrw = in.readInt()
        self.hythd = in.readInt()
        self.mrfbrwa = in.readInt()
        self.mrsbossrwa = in.readInt()
        self.mrsgrwa = in.readInt()
        self.mrfbrwas = in.readInt()
        self.mrsbossrwas = in.readInt()
        self.mrsgrwas = in.readInt()
        self.mrfbrws = in.readInt()
        self.mrsbossrws = in.readInt()
        self.mrsgrws = in.readInt()
        self.ddj = in.readInt()
        self.vip = in.readInt()
        self.vipexpired = in.readLong()
        self.djjl = in.readInt()
        self.qiandao = in.readInt()
        self.jf = in.readInt()
        self.blood = in.readInt()
        self.month = in.readInt()
        self.day = in.readInt()
        self.battleshipHP = in.readInt()
        self.prefix = in.readInt()
        self.tempIP = in.readUTF()
        self.shaguai = in.readInt()
        mbooksize = in.readShort(), j = 0
        while j < mbooksize:
            self.mbook.put(in.readInt(), in.readInt())
        skillsize = in.readShort(), k = 0
        while k < skillsize:
            self.Skills.put(in.readInt(), SkillEntry(in.readByte(), in.readByte(), in.readLong()))
        self.buddysize = in.readByte()
        addedbuddysize = in.readShort()
        for l in range(addedbuddysize):
            self.buddies.put(BuddyEntry(in.readUTF(), in.readInt(), in.readUTF(), in.readInt(), in.readBoolean(), in.readInt(), in.readInt()), in.readBoolean())
        questsize = in.readShort(), m = 0
        while m < questsize:
            self.Quest.put(in.readInt(), in.readObject())
        achievesize = in.readShort(), i2 = 0
        while i2 < achievesize:
            self.finishedAchievements.add(in.readInt())
        famesize = in.readInt(), i3 = 0
        while i3 < famesize:
            self.famedcharacters.add(in.readInt())
        savesize = in.readShort()
        self.savedlocation = new int[savesize]
        for i4 in range(savesize):
            self.savedlocation[i4] = in.readInt()
        wsize = in.readShort()
        self.wishlist = new int[wsize]
        for i5 in range(wsize):
            self.wishlist[i5] = in.readInt()
        rsize = in.readShort()
        self.rocks = new int[rsize]
        for i6 in range(rsize):
            self.rocks[i6] = in.readInt()
        resize = in.readShort()
        self.regrocks = new int[resize]
        for i7 in range(resize):
            self.regrocks[i7] = in.readInt()
        infosize = in.readShort(), i8 = 0
        while i8 < infosize:
            self.InfoQuest.put(in.readInt(), in.readUTF())
        keysize = in.readInt(), i9 = 0
        while i9 < keysize:
            self.keymap.put(in.readInt(), new Pair<Byte, Integer>(in.readByte(), in.readInt()))
        self.petStore = new byte[in.readByte()]
        for i9 in range(3):
            self.petStore[i9] = in.readByte()
        self.TranferTime = int(time.time() * 1000)

    def writeExternal(self, out: Any) -> None:
        out.writeLong(self.lastGainHM)
        out.writeBoolean(self.DebugMessage)
        out.writeInt(self.characterid)
        out.writeInt(self.accountid)
        out.writeUTF(self.accountname)
        out.writeByte(self.channel)
        out.writeInt(self.ACash)
        out.writeInt(self.MaplePoints)
        out.writeUTF(self.name)
        out.writeShort(self.fame)
        out.writeByte(self.gender)
        out.writeShort(self.level)
        out.writeShort(self.str)
        out.writeShort(self.dex)
        out.writeShort(self.int_)
        out.writeShort(self.luk)
        out.writeShort(self.hp)
        out.writeShort(self.mp)
        out.writeShort(self.maxhp)
        out.writeShort(self.maxmp)
        out.writeInt(self.exp)
        out.writeShort(self.hpApUsed)
        out.writeShort(self.remainingAp)
        out.writeByte(self.len(remainingSp))
        for i in range(self.len(remainingSp)):
            out.writeInt(self.remainingSp[i])
        out.writeInt(self.beans)
        out.writeInt(self.meso)
        out.writeByte(self.skinColor)
        out.writeShort(self.job)
        out.writeInt(self.hair)
        out.writeInt(self.face)
        out.writeInt(self.mapid)
        out.writeByte(self.initialSpawnPoint)
        out.writeByte(self.world)
        out.writeInt(self.guildid)
        out.writeByte(self.guildrank)
        out.writeByte(self.alliancerank)
        out.writeByte(self.gmLevel)
        out.writeInt(self.points)
        out.writeInt(self.vpoints)
        out.writeByte((self.BlessOfFairy is not None) ? 1 : 0)
        if self.BlessOfFairy is not None:
            out.writeUTF(self.BlessOfFairy)
        out.writeByte((self.chalkboard is not None) ? 1 : 0)
        if self.chalkboard is not None:
            out.writeUTF(self.chalkboard)
        out.writeByte(self.clonez)
        out.writeObject(self.skillmacro)
        out.writeLong(self.lastfametime)
        out.writeObject(self.storage)
        out.writeObject(self.cs)
        out.writeInt(self.mount_itemid)
        out.writeByte(self.mount_Fatigue)
        out.writeByte(self.mount_level)
        out.writeInt(self.mount_exp)
        out.writeInt(self.partyid)
        out.writeInt(self.messengerid)
        out.writeInt(self.mBookCover)
        out.writeInt(self.dojo)
        out.writeByte(self.dojoRecord)
        out.writeObject(self.inventorys)
        out.writeByte(self.fairyExp)
        out.writeByte(self.subcategory)
        out.writeInt(self.marriageId)
        out.writeUTF(self.tempIP)
        out.writeInt(self.familyid)
        out.writeInt(self.seniorid)
        out.writeInt(self.junior1)
        out.writeInt(self.junior2)
        out.writeInt(self.currentrep)
        out.writeInt(self.totalrep)
        out.writeInt(self.battleshipHP)
        out.writeUTF(self.charmessage)
        out.writeInt(self.expression)
        out.writeInt(self.constellation)
        out.writeInt(self.skillzq)
        out.writeInt(self.bosslog)
        out.writeInt(self.PGMaxDamage)
        out.writeInt(self.jzname)
        out.writeInt(self.mrfbrw)
        out.writeInt(self.mrsbossrw)
        out.writeInt(self.mrsgrw)
        out.writeInt(self.mrsjrw)
        out.writeInt(self.mrfbrwa)
        out.writeInt(self.mrsbossrwa)
        out.writeInt(self.mrsgrwa)
        out.writeInt(self.mrfbrwas)
        out.writeInt(self.mrsbossrwas)
        out.writeInt(self.mrsgrwas)
        out.writeInt(self.mrfbrws)
        out.writeInt(self.mrsbossrws)
        out.writeInt(self.mrsgrws)
        out.writeInt(self.hythd)
        out.writeInt(self.ddj)
        out.writeInt(self.djjl)
        out.writeInt(self.qiandao)
        out.writeInt(self.jf)
        out.writeInt(self.vip)
        out.writeLong(self.vipexpired)
        out.writeInt(self.blood)
        out.writeInt(self.month)
        out.writeInt(self.day)
        out.writeInt(self.prefix)
        out.writeInt(self.shaguai)
        out.writeShort(self.mbook)
        for (final Map.Entry<Integer, Integer> ms : self.mbook.items())
            out.writeInt(ms.getKey())
            out.writeInt(ms.getValue())
        out.writeShort(self.Skills)
        for (final Map.Entry<Integer, SkillEntry> qs : self.Skills.items())
            out.writeInt(qs.getKey())
            out.writeByte(qs.getValue().skillevel)
            out.writeByte(qs.getValue().masterlevel)
            out.writeLong(qs.getValue().expiration)
        out.writeByte(self.buddysize)
        out.writeShort(self.buddies)
        for (final Map.Entry<BuddyEntry, Boolean> qs2 : self.buddies.items())
            out.writeUTF(qs2.getKey().getName())
            out.writeInt(qs2.getKey().getCharacterId())
            out.writeUTF(qs2.getKey().getGroup())
            out.writeInt(qs2.getKey().getChannel())
            out.writeBoolean(qs2.getValue())
            out.writeInt(qs2.getKey().getLevel())
            out.writeInt(qs2.getKey().getJob())
            out.writeBoolean(qs2.getValue())
        out.writeShort(self.Quest)
        for (final Map.Entry<Integer, Object> qs3 : self.Quest.items())
            out.writeInt(qs3.getKey())
            out.writeObject(qs3.getValue())
        out.writeShort(self.finishedAchievements)
        for zz in self.finishedAchievements:
            out.writeInt(zz)
        out.writeInt(self.famedcharacters)
        for zz in self.famedcharacters:
            out.writeInt(zz)
        out.writeShort(self.len(savedlocation))
        for zz2 in self.savedlocation:
            out.writeInt(zz2)
        out.writeShort(self.len(wishlist))
        for zz2 in self.wishlist:
            out.writeInt(zz2)
        out.writeShort(self.len(rocks))
        for zz2 in self.rocks:
            out.writeInt(zz2)
        out.writeShort(self.len(regrocks))
        for zz2 in self.regrocks:
            out.writeInt(zz2)
        out.writeShort(self.InfoQuest)
        for (final Map.Entry<Integer, String> qs4 : self.InfoQuest.items())
            out.writeInt(qs4.getKey())
            out.writeUTF(qs4.getValue())
        out.writeInt(self.keymap)
        for (final Map.Entry<Integer, Pair<Byte, Integer>> qs5 : self.keymap.items())
            out.writeInt(qs5.getKey())
            out.writeByte(qs5.getValue().left)
            out.writeInt(qs5.getValue().right)
        out.writeByte(self.len(petStore))
        for i in range(self.len(petStore)):
            out.writeByte(self.petStore[i])

