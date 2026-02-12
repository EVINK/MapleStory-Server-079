"""
MapleCharacter - Converted from Java source
Original: client/MapleCharacter.java
Package: client
"""

from concurrent.futures import Future
from datetime import datetime
from datetime import datetime, timezone, timedelta
from enum import Enum
from enum import Enum, IntEnum
from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from socket import socket
from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set
from weakref import ref
import asyncio
import logging
import math
import os
import pymysql
import sched
import sys
import threading
import time
import weakref

# Internal module imports
# from client.anticheat.CheatTracker import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MapleMount import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from client.inventory.ModifyInventory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from database.DatabaseException import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.CharacterTransfer import *  # TODO: import specific classes
# from handling.world.MapleMessenger import *  # TODO: import specific classes
# from handling.world.MapleMessengerCharacter import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PartyOperation import *  # TODO: import specific classes
# from handling.world.PlayerBuffStorage import *  # TODO: import specific classes
# from handling.world.PlayerBuffValueHolder import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamily import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyBuff import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyCharacter import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildCharacter import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from scripting.EventInstanceManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.AutobanManager import *  # TODO: import specific classes
# from server.CashShop import *  # TODO: import specific classes
# from server.MapleCarnivalChallenge import *  # TODO: import specific classes
# from server.MapleCarnivalParty import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.MapleShop import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.MapleStorage import *  # TODO: import specific classes
# from server.MapleTrade import *  # TODO: import specific classes
# from server.RandomRewards import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from server.life.PlayerNPC import *  # TODO: import specific classes
# from server.maps.AbstractAnimatedMapleMapObject import *  # TODO: import specific classes
# from server.maps.Event_PyramidSubway import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from server.maps.MapleDoor import *  # TODO: import specific classes
# from server.maps.MapleFoothold import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapEffect import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleSummon import *  # TODO: import specific classes
# from server.maps.SavedLocationType import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from tools.ConcurrentEnumMap import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.MockIOSession import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes
# from tools.packet.MonsterCarnivalPacket import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes
# from tools.packet.UIPacket import *  # TODO: import specific classes


class MapleCharacter(AbstractAnimatedMapleMapObject):
    """
    Class MapleCharacter
    Extends: AbstractAnimatedMapleMapObject
    Implements: Serializable
    """

    serialVersionUID = 845748950829

    def __init__(self, ChannelServer: bool):
        self.name = ""
        self.chalktext = ""
        self.BlessOfFairy_Origin = ""
        self.charmessage = ""
        self.lastComboTime = 0
        self.lastfametime = 0
        self.keydown_skill = 0
        self.dojoRecord = 0
        self.gmLevel = 0
        self.gender = 0
        self.initialSpawnPoint = 0
        self.skinColor = 0
        self.guildrank = 0
        self.allianceRank = 0
        self.world = 0
        self.fairyExp = 0
        self.numClones = 0
        self.subcategory = 0
        self.level = 0
        self.mulung_energy = 0
        self.aranCombo = 0
        self.availableCP = 0
        self.totalCP = 0
        self.fame = 0
        self.hpApUsed = 0
        self.job = 0
        self.remainingAp = 0
        self.accountid = 0
        self.id = 0
        self.meso = 0
        self.exp = 0
        self.hair = 0
        self.face = 0
        self.mapid = 0
        self.bookCover = 0
        self.dojo = 0
        self.guildid = 0
        self.fallcounter = 0
        self.maplepoints = 0
        self.acash = 0
        self.guildrank = 5
        self.allianceRank = 5
        self.fairyExp = 10
        self.guildid = 0
        self.fallcounter = 0
        self.rank = 1
        self.rankMove = 0
        self.jobRank = 1
        self.jobRankMove = 0
        self.marriageItemId = 0
        self.linkMid = 0
        self.coconutteam = 0
        self.followid = 0
        self.battleshipHP = 0
        self.old = Point(0, 0)
        self.hasSummon = False
        self.remainingSp = new int[10]
        self.skills = {}
        self.effects = new ConcurrentEnumMap<MapleBuffStat, MapleBuffStatValueHolder>(MapleBuffStat.class)
        self.coolDowns = {}
        self.diseases = new ConcurrentEnumMap<MapleDisease, MapleDiseaseValueHolder>(MapleDisease.class)
        self.finishedAchievements = []
        self.invincible = False
        self.canTalk = True
        self.clone = False
        self.followinitiator = False
        self.followon = False
        self.skillMacros = new SkillMacro[5]
        self.nextConsume = 0
        self.pqStartTime = 0
        self.pyramidSubway = None
        self.pendingExpiration = None
        self.pendingSkills = None
        self.movedMobs = {}
        self.teleportname = ""
        self.lasttime = 0
        self.currenttime = 0
        self.deadtime = 1000
        self.apprentice = 0
        self.master = 0
        self.DebugMessage = False
        self.ariantScore = 0
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
        self.shaguai = 0
        self.curPGDamage = 0
        self.lastRecoveryTime = 0
        self.MobVac = 0
        self.MobVac2 = 0
        self.cancelEnergyRunnable = Runnable()
            public void run()
                energyLevel = 0
                MapleCharacter.self.setBuffedValue(MapleBuffStat.能量获得, energyLevel)
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, energyLevel))
                MapleCharacter.self.client.getSession().write(MaplePacketCreator.能量条(stat, 0))
                MapleCharacter.self.cancelEnergy = True
        self.cancelEnergy = True
        self.setStance(0)
        self.setPosition(Point(0, 0))
        self.inventory = new MapleInventory[MapleInventoryType.values().length]
        for type in MapleInventoryType.values():
            self.inventory[type.ordinal()] = MapleInventory(type, 100)
        self.quests = {}
        self.stats = PlayerStats(this)
        for i in range(self.len(remainingSp)):
            self.remainingSp[i] = 0
        if ChannelServer:
            self.lastMoveItemTime = 0
            self.lastCheckPeriodTime = 0
            self.lastQuestTime = 0
            self.lastHPTime = 0
            self.lastMPTime = 0
            self.lastComboTime = 0
            self.mulung_energy = 0
            self.aranCombo = 0
            self.keydown_skill = 0
            self.smega = True
            self.petStore = new byte[3]
            for i in range(self.len(petStore)):
                self.petStore[i] = -1
            self.wishlist = new int[10]
            self.rocks = new int[10]
            self.regrocks = new int[5]
            self.clones = (WeakReference<MapleCharacter>[])new WeakReference[25]
            for i in range(self.len(clones)):
                self.clones[i] = new WeakReference<MapleCharacter>(None)
            (self.inst = AtomicInteger()).set(0)
            self.keylayout = MapleKeyLayout()
            self.doors = []
            self.controlled = new LinkedHashSet<MapleMonster>()
            self.summons = []
            self.summonsLock = ReentrantReadWriteLock()
            self.visibleMapObjects = new LinkedHashSet<MapleMapObject>()
            self.visibleMapObjectsLock = ReentrantReadWriteLock()
            self.controlledLock = ReentrantReadWriteLock()
            self.pendingCarnivalRequests = []
            self.savedLocations = new int[SavedLocationType.values().length]
            for i in range(SavedLocationType.values().length):
                self.savedLocations[i] = -1
            self.questinfo = {}
            self.anticheat = CheatTracker(this)
            self.pets = []

    # Static initializer
    # ariantroomleader = new String[3]
    # ariantroomslot = new int[3]
    # MapleCharacter.tutorial = False


    def getDefault(self, client: Any, type: int) -> Any:
        ret = MapleCharacter(False)
        ret.client = client
        ret.map = None
        ret.exp = 0
        ret.gmLevel = 0
        ret.job = (short)((type == 1) ? 0 : ((type == 0) ? 1000 : ((type == 3) ? 2001 : ((type == 4) ? 3000 : 2000))))
        ret.beans = 0
        ret.meso = 0
        ret.level = 1
        ret.remainingAp = 0
        ret.fame = 0
        ret.accountid = client.getAccID()
        ret.buddylist = BuddyList(20)
        ret.stats.str = 12
        ret.stats.dex = 5
        ret.stats.int_ = 4
        ret.stats.luk = 4
        ret.stats.maxhp = 50
        ret.stats.hp = 50
        ret.stats.maxmp = 50
        ret.stats.mp = 50
        ret.prefix = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
            ps.setInt(1, ret.accountid)
            rs = ps.executeQuery()
            if rs.next():
                ret.client.setAccountName(rs.getString("name"))
                ret.acash = rs.getInt("ACash")
                ret.maplepoints = rs.getInt("mPoints")
                ret.points = rs.getInt("points")
                ret.vpoints = rs.getInt("vpoints")
                ret.lastGainHM = rs.getLong("lastGainHM")
            rs.close()
            ps.close()
        except Exception as e:
            print("Error getting character default" + e)
        return ret

    def ReconstructChr(self, ct: Any, client: Any, isChannel: bool) -> Any:
        ret = MapleCharacter(True)
        ret.client = client
        if not isChannel:
        ret.client.setChannel(ct.channel)
        ret.DebugMessage = ct.DebugMessage
        ret.id = ct.characterid
        ret.name = ct.name
        ret.level = ct.level
        ret.fame = ct.fame
        ret.CRand = PlayerRandomStream()
        ret.stats.str = ct.str
        ret.stats.dex = ct.dex
        ret.stats.int_ = ct.int_
        ret.stats.luk = ct.luk
        ret.stats.maxhp = ct.maxhp
        ret.stats.maxmp = ct.maxmp
        ret.stats.hp = ct.hp
        ret.stats.mp = ct.mp
        ret.chalktext = ct.chalkboard
        ret.exp = ct.exp
        ret.hpApUsed = ct.hpApUsed
        ret.remainingSp = ct.remainingSp
        ret.remainingAp = ct.remainingAp
        ret.beans = ct.beans
        ret.meso = ct.meso
        ret.gmLevel = ct.gmLevel
        ret.skinColor = ct.skinColor
        ret.gender = ct.gender
        ret.job = ct.job
        ret.hair = ct.hair
        ret.face = ct.face
        ret.accountid = ct.accountid
        ret.mapid = ct.mapid
        ret.initialSpawnPoint = ct.initialSpawnPoint
        ret.world = ct.world
        ret.bookCover = ct.mBookCover
        ret.dojo = ct.dojo
        ret.dojoRecord = ct.dojoRecord
        ret.guildid = ct.guildid
        ret.guildrank = ct.guildrank
        ret.allianceRank = ct.alliancerank
        ret.points = ct.points
        ret.vpoints = ct.vpoints
        ret.fairyExp = ct.fairyExp
        ret.marriageId = ct.marriageId
        ret.currentrep = ct.currentrep
        ret.totalrep = ct.totalrep
        ret.charmessage = ct.charmessage
        ret.expression = ct.expression
        ret.constellation = ct.constellation
        ret.skillzq = ct.skillzq
        ret.bosslog = ct.bosslog
        ret.PGMaxDamage = ct.PGMaxDamage
        ret.jzname = ct.jzname
        ret.mrfbrw = ct.mrfbrw
        ret.mrsbossrw = ct.mrsbossrw
        ret.mrsgrw = ct.mrsgrw
        ret.mrfbrwa = ct.mrfbrwa
        ret.mrsbossrwa = ct.mrsbossrwa
        ret.mrsgrwa = ct.mrsgrwa
        ret.mrfbrws = ct.mrfbrws
        ret.mrsbossrws = ct.mrsbossrws
        ret.mrsgrws = ct.mrsgrws
        ret.mrfbrwas = ct.mrfbrwas
        ret.mrsbossrwas = ct.mrsbossrwas
        ret.mrsgrwas = ct.mrsgrwas
        ret.mrsjrw = ct.mrsjrw
        ret.hythd = ct.hythd
        ret.ddj = ct.ddj
        ret.vip = ct.vip
        ret.vipexpired = ct.vipexpired
        ret.djjl = ct.djjl
        ret.qiandao = ct.qiandao
        ret.jf = ct.jf
        ret.blood = ct.blood
        ret.month = ct.month
        ret.day = ct.day
        ret.pvpDeaths = ct.pvpDeaths
        ret.pvpKills = ct.pvpKills
        ret.pvpVictory = ct.pvpVictory
        ret.shaguai = ct.shaguai
        ret.makeMFC(ct.familyid, ct.seniorid, ct.junior1, ct.junior2)
        if ret.guildid > 0:
        ret.mgc = MapleGuildCharacter(ret)
        ret.buddylist = BuddyList(ct.buddysize)
        ret.subcategory = ct.subcategory
        ret.prefix = ct.prefix
        if isChannel:
            mapFactory = ChannelServer.getInstance(client.getChannel()).getMapFactory()
            ret.map = mapFactory.getMap(ret.mapid)
            if ret.map is None:
                ret.map = mapFactory.getMap(100000000)
            elif ret.map.getForcedReturnId() != 999999999:
                ret.map = ret.map.getForcedReturnMap()
            portal = ret.map.getPortal(ret.initialSpawnPoint)
            if portal is None:
                portal = ret.map.getPortal(0)
                ret.initialSpawnPoint = 0
            ret.setPosition(portal.getPosition())
            messengerid = ct.messengerid
            if messengerid > 0:
            ret.messenger = World.Messenger.getMessenger(messengerid)
        else:
            ret.messenger = None
        partyid = ct.partyid
        if partyid >= 0:
            party = World.Party.getParty(partyid)
            if party is not None and party.getMemberById(ret.id) is not None:
            ret.party = party
        for (Map.Entry<Integer, Object> qs : (Iterable<Map.Entry<Integer, Object>>)ct.Quest.items())
            quest = MapleQuest.getInstance((qs.getKey()))
            queststatus_from = qs.getValue()
            queststatus = MapleQuestStatus(quest, queststatus_from.getStatus())
            queststatus.setForfeited(queststatus_from.getForfeited())
            queststatus.setCustomData(queststatus_from.getCustomData())
            queststatus.setCompletionTime(queststatus_from.getCompletionTime())
            if queststatus_from.getMobKills() is not None:
            for (Map.Entry<Integer, Integer> mobkills : queststatus_from.getMobKills().items())
            queststatus.setMobKills((mobkills.getKey()), (mobkills.getValue()))
            ret.quests.put(quest, queststatus)
        for (Map.Entry<Integer, SkillEntry> qs : (Iterable<Map.Entry<Integer, SkillEntry>>)ct.Skills.items())
        ret.skills.put(SkillFactory.getSkill((qs.getKey())), qs.getValue())
        for zz in ct.finishedAchievements:
        ret.finishedAchievements.add(zz)
        ret.monsterbook = MonsterBook(ct.mbook)
        ret.inventory = (MapleInventory[])ct.inventorys
        ret.BlessOfFairy_Origin = ct.BlessOfFairy
        ret.skillMacros = (SkillMacro[])ct.skillmacro
        ret.petStore = ct.petStore
        ret.keylayout = MapleKeyLayout(ct.keymap)
        ret.questinfo = ct.InfoQuest
        ret.savedLocations = ct.savedlocation
        ret.wishlist = ct.wishlist
        ret.rocks = ct.rocks
        ret.regrocks = ct.regrocks
        ret.buddylist.loadFromTransfer(ct.buddies)
        ret.keydown_skill = 0
        ret.lastfametime = ct.lastfametime
        ret.lastmonthfameids = ct.famedcharacters
        ret.storage = ct.storage
        ret.pvpStats = ct.pvpStats
        ret.cs = ct.cs
        client.setAccountName(ct.accountname)
        ret.acash = ct.ACash
        ret.lastGainHM = ct.lastGainHM
        ret.maplepoints = ct.MaplePoints
        ret.numClones = ct.clonez
        ret.mount = MapleMount(ret, ct.mount_itemid, GameConstants.isKOC(ret.job) ? 10001004 : (GameConstants.isAran(ret.job) ? 20001004 : (GameConstants.isEvan(ret.job) ? 20011004 : 1004)), ct.mount_Fatigue, ct.mount_level, ct.mount_exp)
        ret.stats.recalcLocalStats(True)
        return ret

    def loadCharFromDB(self, charid: int, client: Any, channelserver: bool) -> Any:
        ret = MapleCharacter(channelserver)
        ret.client = client
        ret.id = charid
        con = DatabaseConnection.getConnection()
        ps = None
        pse = None
        rs = None
        try:
            ps = con.prepareStatement("SELECT * FROM characters WHERE id = ?")
            ps.setInt(1, charid)
            rs = ps.executeQuery()
            if not rs.next():
                raise RuntimeError("Loading the Char Failed (char not found)")
            ret.name = rs.getString("name")
            ret.level = rs.getShort("level")
            ret.fame = rs.getShort("fame")
            ret.stats.str = rs.getShort("str")
            ret.stats.dex = rs.getShort("dex")
            ret.stats.int_ = rs.getShort("int")
            ret.stats.luk = rs.getShort("luk")
            ret.stats.maxhp = rs.getShort("maxhp")
            ret.stats.maxmp = rs.getShort("maxmp")
            ret.stats.hp = rs.getShort("hp")
            ret.stats.mp = rs.getShort("mp")
            ret.exp = rs.getInt("exp")
            ret.hpApUsed = rs.getShort("hpApUsed")
            sp = rs.getString("sp").split(",")
            for i in range(ret.len(remainingSp)):
                ret.remainingSp[i] = int(sp[i])
            ret.remainingAp = rs.getShort("ap")
            ret.beans = rs.getInt("beans")
            ret.meso = rs.getInt("meso")
            ret.gmLevel = rs.getByte("gm")
            ret.skinColor = rs.getByte("skincolor")
            ret.gender = rs.getByte("gender")
            ret.job = rs.getShort("job")
            ret.hair = rs.getInt("hair")
            ret.face = rs.getInt("face")
            ret.accountid = rs.getInt("accountid")
            ret.mapid = rs.getInt("map")
            ret.initialSpawnPoint = rs.getByte("spawnpoint")
            ret.world = rs.getByte("world")
            ret.guildid = rs.getInt("guildid")
            ret.guildrank = rs.getByte("guildrank")
            ret.allianceRank = rs.getByte("allianceRank")
            ret.currentrep = rs.getInt("currentrep")
            ret.totalrep = rs.getInt("totalrep")
            ret.makeMFC(rs.getInt("familyid"), rs.getInt("seniorid"), rs.getInt("junior1"), rs.getInt("junior2"))
            if ret.guildid > 0:
                ret.mgc = MapleGuildCharacter(ret)
            ret.buddylist = BuddyList(rs.getByte("buddyCapacity"))
            ret.subcategory = rs.getByte("subcategory")
            ret.mount = MapleMount(ret, 0, (ret.job > 1000 and ret.job < 2000) ? 10001004 : ((ret.job >= 2000) ? ((ret.job == 2001 or (ret.job >= 2200 and ret.job <= 2218)) ? 20011004 : ((ret.job >= 3000) ? 30001004 : 20001004)) : 1004), 0, 1, 0)
            ret.rank = rs.getInt("rank")
            ret.rankMove = rs.getInt("rankMove")
            ret.jobRank = rs.getInt("jobRank")
            ret.jobRankMove = rs.getInt("jobRankMove")
            ret.marriageId = rs.getInt("marriageId")
            ret.charmessage = rs.getString("charmessage")
            ret.expression = rs.getInt("expression")
            ret.constellation = rs.getInt("constellation")
            ret.skillzq = rs.getInt("skillzq")
            ret.bosslog = rs.getInt("bosslog")
            ret.PGMaxDamage = rs.getInt("PGMaxDamage")
            ret.jzname = rs.getInt("jzname")
            ret.mrfbrw = rs.getInt("mrfbrw")
            ret.mrsbossrw = rs.getInt("mrsbossrw")
            ret.mrsgrw = rs.getInt("mrsgrw")
            ret.mrfbrws = rs.getInt("mrfbrws")
            ret.mrsbossrws = rs.getInt("mrsbossrws")
            ret.mrsgrws = rs.getInt("mrsgrws")
            ret.mrsjrw = rs.getInt("mrsjrw")
            ret.hythd = rs.getInt("hythd")
            ret.mrfbrwa = rs.getInt("mrfbrwa")
            ret.mrsbossrwa = rs.getInt("mrsbossrwa")
            ret.mrsgrwa = rs.getInt("mrsgrwa")
            ret.mrfbrwas = rs.getInt("mrfbrwas")
            ret.mrsbossrwas = rs.getInt("mrsbossrwas")
            ret.mrsgrwas = rs.getInt("mrsgrwas")
            ret.blood = rs.getInt("blood")
            ret.ddj = rs.getInt("ddj")
            ret.vip = rs.getInt("vip")
            ret.vipexpired = rs.getLong("vipexpired")
            ret.djjl = rs.getInt("djjl")
            ret.qiandao = rs.getInt("qiandao")
            ret.jf = rs.getInt("jf")
            ret.pvpDeaths = rs.getInt("pvpDeaths")
            ret.pvpKills = rs.getInt("pvpKills")
            ret.pvpVictory = rs.getInt("pvpVictory")
            ret.month = rs.getInt("month")
            ret.day = rs.getInt("day")
            ret.prefix = rs.getInt("prefix")
            ret.shaguai = rs.getInt("shaguai")
            if channelserver:
                ret.pvpStats = MaplePvpStats.loadOrCreateFromDB(ret.accountid)
                ret.antiMacro = MapleLieDetector(ret)
                mapFactory = ChannelServer.getInstance(client.getChannel()).getMapFactory()
                ret.map = mapFactory.getMap(ret.mapid)
                if ret.map is None:
                    ret.map = mapFactory.getMap(100000000)
                portal = ret.map.getPortal(ret.initialSpawnPoint)
                if portal is None:
                    portal = ret.map.getPortal(0)
                    ret.initialSpawnPoint = 0
                ret.setPosition(portal.getPosition())
                partyid = rs.getInt("party")
                if partyid >= 0:
                    party = World.Party.getParty(partyid)
                    if party is not None and party.getMemberById(ret.id) is not None:
                        ret.party = party
                ret.bookCover = rs.getInt("monsterbookcover")
                ret.dojo = rs.getInt("dojo_pts")
                ret.dojoRecord = rs.getByte("dojoRecord")
                pets = rs.getString("pets").split(",")
                for j in range(ret.len(petStore)):
                    ret.petStore[j] = Byte.parseByte(pets[j])
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT * FROM achievements WHERE accountid = ?")
                ps.setInt(1, ret.accountid)
                rs = ps.executeQuery()
                while rs.next():
                    ret.finishedAchievements.add(rs.getInt("achievementid"))
            rs.close()
            ps.close()
            compensate_previousEvans = False
            ps = con.prepareStatement("SELECT * FROM queststatus WHERE characterid = ?")
            ps.setInt(1, charid)
            rs = ps.executeQuery()
            pse = con.prepareStatement("SELECT * FROM queststatusmobs WHERE queststatusid = ?")
            while rs.next():
                id = rs.getInt("quest")
                if id == 170000:
                    compensate_previousEvans = True
                q = MapleQuest.getInstance(id)
                status = MapleQuestStatus(q, rs.getByte("status"))
                cTime = rs.getLong("time")
                if cTime > -1:
                    status.setCompletionTime(cTime * 1000)
                status.setForfeited(rs.getInt("forfeited"))
                status.setCustomData(rs.getString("customData"))
                ret.quests.put(q, status)
                pse.setInt(1, rs.getInt("queststatusid"))
                rsMobs = pse.executeQuery()
                while rsMobs.next():
                    status.setMobKills(rsMobs.getInt("mob"), rsMobs.getInt("count"))
                rsMobs.close()
            rs.close()
            ps.close()
            pse.close()
            if channelserver:
                ret.CRand = PlayerRandomStream()
                ret.monsterbook = MonsterBook.loadCards(charid)
                ps = con.prepareStatement("SELECT * FROM inventoryslot where characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                if not rs.next():
                    rs.close()
                    ps.close()
                    raise RuntimeError("No Inventory slot column found in SQL. [inventoryslot]*********************")
                ret.getInventory(MapleInventoryType.EQUIP).setSlotLimit(rs.getByte("equip"))
                ret.getInventory(MapleInventoryType.USE).setSlotLimit(rs.getByte("use"))
                ret.getInventory(MapleInventoryType.SETUP).setSlotLimit(rs.getByte("setup"))
                ret.getInventory(MapleInventoryType.ETC).setSlotLimit(rs.getByte("etc"))
                ret.getInventory(MapleInventoryType.CASH).setSlotLimit(rs.getByte("cash"))
                ps.close()
                rs.close()
                for mit in ItemLoader.装备道具.loadItems(False, charid).values():
                    ret.getInventory(mit.getRight()).addFromDB(mit.getLeft())
                    if mit.getLeft().getPet() is not None:
                        ret.pets.add(mit.getLeft().getPet())
                ps = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
                ps.setInt(1, ret.accountid)
                rs = ps.executeQuery()
                if rs.next():
                    ret.getClient().setAccountName(rs.getString("name"))
                    ret.lastGainHM = rs.getLong("lastGainHM")
                    ret.acash = rs.getInt("ACash")
                    ret.maplepoints = rs.getInt("mPoints")
                    ret.points = rs.getInt("points")
                    ret.vpoints = rs.getInt("vpoints")
                    if rs.getTimestamp("lastlogon") is not None:
                        cal = Calendar.getInstance()
                        cal.setTimeInMillis(rs.getTimestamp("lastlogon").getTime())
                    rs.close()
                    ps.close()
                    ps = con.prepareStatement("UPDATE accounts SET lastlogon = CURRENT_TIMESTAMP() WHERE id = ?")
                    ps.setInt(1, ret.accountid)
                    ps.executeUpdate()
                else:
                    rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT * FROM questinfo WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                while rs.next():
                    ret.questinfo.put(rs.getInt("quest"), rs.getString("customData"))
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT skillid, skilllevel, masterlevel, expiration FROM skills WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                while rs.next():
                    skil = SkillFactory.getSkill(rs.getInt("skillid"))
                    if skil is not None and GameConstants.isApplicableSkill(rs.getInt("skillid")):
                        ret.skills.put(skil, SkillEntry(rs.getByte("skilllevel"), rs.getByte("masterlevel"), rs.getLong("expiration")))
                    else:
                        if skil is not None:
                            continue
                        remainingSp = ret.remainingSp
                        skillBookForSkill = GameConstants.getSkillBookForSkill(rs.getInt("skillid"))
                        remainingSp[skillBookForSkill] += rs.getByte("skilllevel")
                rs.close()
                ps.close()
                ret.expirationTask(False)
                ps = con.prepareStatement("SELECT * FROM characters WHERE accountid = ? ORDER BY level DESC")
                ps.setInt(1, ret.accountid)
                rs = ps.executeQuery()
                maxlevel_ = 0
                while rs.next():
                    if rs.getInt("id") != charid:
                        maxlevel = (byte)(rs.getShort("level") / 10)
                        if maxlevel > 20:
                            maxlevel = 20
                        if maxlevel <= maxlevel_:
                            continue
                        maxlevel_ = maxlevel
                        ret.BlessOfFairy_Origin = rs.getString("name")
                    else:
                        if charid >= 17000 or compensate_previousEvans or ret.job < 2200 or ret.job > 2218:
                            continue
                        for k in range(= GameConstants.getSkillBook(ret.job)):
                            remainingSp2 = ret.remainingSp
                            n = k
                            remainingSp2[n] += 2
                        ret.setQuestAdd(MapleQuest.getInstance(170000), 0, None)
                ret.skills.put(SkillFactory.getSkill(GameConstants.getBOF_ForJob(ret.job)), SkillEntry(maxlevel_, 0, -1))
                ps.close()
                rs.close()
                for k in range(5):
                    ret.skillMacros[k] = SkillMacro(0, 0, 0, "", 0, k)
                ps = con.prepareStatement("SELECT * FROM skillmacros WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                while rs.next():
                    position = rs.getInt("position")
                    macro = SkillMacro(rs.getInt("skill1"), rs.getInt("skill2"), rs.getInt("skill3"), rs.getString("name"), rs.getInt("shout"), position)
                    ret.skillMacros[position] = macro
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT `key`,`type`,`action` FROM keymap WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                keyb = ret.keylayout.Layout()
                while rs.next():
                    keyb.put(rs.getInt("key"), new Pair<Byte, Integer>(rs.getByte("type"), rs.getInt("action")))
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT `locationtype`,`map` FROM savedlocations WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                while rs.next():
                    ret.savedLocations[rs.getInt("locationtype")] = rs.getInt("map")
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT `characterid_to`,`when` FROM famelog WHERE characterid = ? AND DATEDIFF(NOW(),`when`) < 30")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                ret.lastfametime = 0
                ret.lastmonthfameids = []
                while rs.next():
                    ret.lastfametime = max(ret.lastfametime, rs.getTimestamp("when").getTime())
                    ret.lastmonthfameids.add(rs.getInt("characterid_to"))
                rs.close()
                ps.close()
                ret.buddylist.loadFromDb(charid)
                ret.storage = MapleStorage.loadStorage(ret.accountid)
                ret.cs = CashShop(ret.accountid, charid, ret.getJob())
                ps = con.prepareStatement("SELECT sn FROM wishlist WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                l = 0
                while rs.next():
                    ret.wishlist[l] = rs.getInt("sn")
                    l += 1
                while l < 10:
                    ret.wishlist[l] = 0
                    l += 1
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT mapid FROM trocklocations WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                r = 0
                while rs.next():
                    ret.rocks[r] = rs.getInt("mapid")
                    r += 1
                while r < 10:
                    ret.rocks[r] = 999999999
                    r += 1
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT mapid FROM regrocklocations WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                r = 0
                while rs.next():
                    ret.regrocks[r] = rs.getInt("mapid")
                    r += 1
                while r < 5:
                    ret.regrocks[r] = 999999999
                    r += 1
                rs.close()
                ps.close()
                ps = con.prepareStatement("SELECT * FROM mountdata WHERE characterid = ?")
                ps.setInt(1, charid)
                rs = ps.executeQuery()
                if not rs.next():
                    raise RuntimeError("No mount data found on SQL column")
                mount = ret.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18))
                ret.mount = MapleMount(ret, (mount is not None) ? mount.getItemId() : 0, (ret.job > 1000 and ret.job < 2000) ? 10001004 : ((ret.job >= 2000) ? ((ret.job == 2001 or ret.job >= 2200) ? 20011004 : ((ret.job >= 3000) ? 30001004 : 20001004)) : 1004), rs.getByte("Fatigue"), rs.getByte("Level"), rs.getInt("Exp"))
                ps.close()
                rs.close()
                ret.stats.recalcLocalStats(True)
            else:
                for mit in ItemLoader.装备道具.loadItems(True, charid).values():
                    ret.getInventory(mit.getRight()).addFromDB(mit.getLeft())
        except Exception as ess:
            ess.printStackTrace()
            print("加载角色数据信息出错...")
            FileoutputUtil.outputFileError("logs/Packet_Except.log", ess)
        finally:
            try:
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
            except SQLException as ex:
                pass
        return ret

    def saveNewCharToDB(self, chr: Any, type: int, db: bool) -> None:
        con = DatabaseConnection.getConnection()
        ps = None
        pse = None
        rs = None
        try:
            con.setTransactionIsolation(1)
            con.setAutoCommit(False)
            ps = con.prepareStatement("INSERT INTO characters (level, fame, str, dex, luk, `int`, exp, hp, mp, maxhp, maxmp, sp, ap, gm, skincolor, gender, job, hair, face, map, meso, hpApUsed, spawnpoint, party, buddyCapacity, monsterbookcover, dojo_pts, dojoRecord, pets, subcategory, marriageId, currentrep, totalrep, prefix, accountid, name, world) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 1)
            ps.setInt(1, 1)
            ps.setShort(2, 0)
            stat = chr.stats
            ps.setShort(3, stat.getStr())
            ps.setShort(4, stat.getDex())
            ps.setShort(5, stat.getInt())
            ps.setShort(6, stat.getLuk())
            ps.setInt(7, 0)
            ps.setShort(8, stat.getHp())
            ps.setShort(9, stat.getMp())
            ps.setShort(10, stat.getMaxHp())
            ps.setShort(11, stat.getMaxMp())
            ps.setString(12, "0,0,0,0,0,0,0,0,0,0")
            ps.setShort(13, 0)
            ps.setInt(14, chr.getClient().gm ? 5 : 0)
            ps.setByte(15, chr.skinColor)
            ps.setByte(16, chr.gender)
            ps.setShort(17, chr.job)
            ps.setInt(18, chr.hair)
            ps.setInt(19, chr.face)
            ps.setInt(20, (type == 1) ? 0 : ((type == 0) ? 130030000 : ((type == 2) ? 914000000 : 910000000)))
            ps.setInt(21, chr.meso)
            ps.setShort(22, 0)
            ps.setByte(23, 0)
            ps.setInt(24, -1)
            ps.setByte(25, chr.buddylist.getCapacity())
            ps.setInt(26, 0)
            ps.setInt(27, 0)
            ps.setInt(28, 0)
            ps.setString(29, "-1,-1,-1")
            ps.setInt(30, 0)
            ps.setInt(31, 0)
            ps.setInt(32, 0)
            ps.setInt(33, 0)
            ps.setInt(34, chr.prefix)
            ps.setInt(35, chr.getAccountID())
            ps.setString(36, chr.name)
            ps.setByte(37, chr.world)
            ps.executeUpdate()
            rs = ps.getGeneratedKeys()
            if not rs.next():
                raise DatabaseException("Inserting char failed.")
            chr.id = rs.getInt(1)
            ps.close()
            rs.close()
            ps = con.prepareStatement("INSERT INTO queststatus (`queststatusid`, `characterid`, `quest`, `status`, `time`, `forfeited`, `customData`) VALUES (DEFAULT, ?, ?, ?, ?, ?, ?)", 1)
            pse = con.prepareStatement("INSERT INTO queststatusmobs VALUES (DEFAULT, ?, ?, ?)")
            ps.setInt(1, chr.id)
            for q in chr.quests.values():
                ps.setInt(2, q.getQuest().getId())
                ps.setInt(3, q.getStatus())
                ps.setInt(4, (int)(q.getCompletionTime() / 1000))
                ps.setInt(5, q.getForfeited())
                ps.setString(6, q.getCustomData())
                ps.executeUpdate()
                rs = ps.getGeneratedKeys()
                rs.next()
                if q.hasMobKills():
                    for mob in q.getMobKills().keys():
                        pse.setInt(1, rs.getInt(1))
                        pse.setInt(2, mob)
                        pse.setInt(3, q.getMobKills(mob))
                        pse.executeUpdate()
                rs.close()
            ps.close()
            pse.close()
            ps = con.prepareStatement("INSERT INTO inventoryslot (characterid, `equip`, `use`, `setup`, `etc`, `cash`) VALUES (?, ?, ?, ?, ?, ?)")
            ps.setInt(1, chr.id)
            ps.setByte(2, 32)
            ps.setByte(3, 32)
            ps.setByte(4, 32)
            ps.setByte(5, 32)
            ps.setByte(6, 60)
            ps.execute()
            ps.close()
            ps = con.prepareStatement("INSERT INTO mountdata (characterid, `Level`, `Exp`, `Fatigue`) VALUES (?, ?, ?, ?)")
            ps.setInt(1, chr.id)
            ps.setByte(2, 1)
            ps.setInt(3, 0)
            ps.setByte(4, 0)
            ps.execute()
            ps.close()
            listing = new ArrayList<Pair<IItem, MapleInventoryType>>()
            for iv in chr.inventory:
                for item in iv.list():
                    listing.add(new Pair<IItem, MapleInventoryType>(item, iv.getType()))
            ItemLoader.装备道具.saveItems(listing, con, chr.id)
            array1 = { 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 23, 25, 26, 27, 29, 31, 34, 35, 37, 38, 40, 41, 43, 44, 45, 46, 48, 50, 56, 57, 59, 60, 61, 62, 63, 64, 65 }
            array2 = { 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6 }
            array3 = { 10, 12, 13, 18, 24, 21, 8, 5, 0, 4, 1, 19, 14, 15, 52, 2, 17, 11, 3, 20, 16, 23, 9, 50, 51, 6, 22, 7, 53, 54, 100, 101, 102, 103, 104, 105, 106 }
            ps = con.prepareStatement("INSERT INTO keymap (characterid, `key`, `type`, `action`) VALUES (?, ?, ?, ?)")
            ps.setInt(1, chr.id)
            for i in range(len(array1)):
                ps.setInt(2, array1[i])
                ps.setInt(3, array2[i])
                ps.setInt(4, array3[i])
                ps.execute()
            ps.close()
            con.commit()
        except DatabaseException as ex2:
            pass
        except Exception as e:
            e.printStackTrace()
            FileoutputUtil.outputFileError("logs/Packet_Except.log", e)
            print("[charsave] Error saving character data")
            try:
                con.rollback()
            except Exception as ex:
                e.printStackTrace()
                FileoutputUtil.outputFileError("logs/Packet_Except.log", ex)
                print("[charsave] Error Rolling Back")
            try:
                if pse is not None:
                    pse.close()
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
                con.setAutoCommit(True)
                con.setTransactionIsolation(4)
            except Exception as e2:
                e2.printStackTrace()
                FileoutputUtil.outputFileError("logs/Packet_Except.log", e2)
                print("[charsave] Error going back to autocommit mode")
        finally:
            try:
                if pse is not None:
                    pse.close()
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
                con.setAutoCommit(True)
                con.setTransactionIsolation(4)
            except Exception as e3:
                e3.printStackTrace()
                FileoutputUtil.outputFileError("logs/Packet_Except.log", e3)
                print("[charsave] Error going back to autocommit mode")

    def deleteWhereCharacterId(self, con: Any, sql: str, id: int) -> None:
        ps = con.prepareStatement(sql)
        ps.setInt(1, id)
        ps.executeUpdate()
        ps.close()

    def ban(self, id: str, reason: str, accountId: bool, gmlevel: int, hellban: bool) -> bool:
        try:
            con = DatabaseConnection.getConnection()
            if id.matches("/[0-9]{1,3}/..*"):
                if (id != "/127.0.0.1") {}
                return True
            ps = None
            if accountId:
                ps = con.prepareStatement("SELECT id FROM accounts WHERE name = ?")
            else:
                ps = con.prepareStatement("SELECT accountid FROM characters WHERE name = ?")
            ret = False
            ps.setString(1, id)
            rs = ps.executeQuery()
            if rs.next():
                z = rs.getInt(1)
                psb = con.prepareStatement("UPDATE accounts SET banned = 1, banreason = ? WHERE id = ? AND gm < ?")
                psb.setString(1, reason)
                psb.setInt(2, z)
                psb.setInt(3, gmlevel)
                psb.execute()
                psb.close()
                if gmlevel > 100:
                    psa = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
                    psa.setInt(1, z)
                    rsa = psa.executeQuery()
                    if rsa.next():
                        sessionIP = rsa.getString("sessionIP")
                        if sessionIP is not None and sessionIP.matches("/[0-9]{1,3}/..*"):
                            psz = con.prepareStatement("INSERT INTO ipbans VALUES (DEFAULT, ?)")
                            psz.setString(1, sessionIP)
                            psz.execute()
                            psz.close()
                        if rsa.getString("macs") is not None:
                            macData = rsa.getString("macs").split(", ")
                            if len(macData) > 0:
                                MapleClient.banMacs(macData)
                        if hellban:
                            pss = con.prepareStatement("UPDATE accounts SET banned = 1, banreason = ? WHERE email = ?" + ((sessionIP is None) ? "" : " OR SessionIP = ?"))
                            pss.setString(1, reason)
                            pss.setString(2, rsa.getString("email"))
                            if sessionIP is not None:
                                pss.setString(3, sessionIP)
                            pss.execute()
                            pss.close()
                    rsa.close()
                    psa.close()
                ret = True
            rs.close()
            ps.close()
            return ret
        except Exception as ex:
            print("Error while banning" + ex)
            return False

    def getAriantRoomLeaderName(self, room: int) -> str:
        return MapleCharacter.ariantroomleader[room]

    def getAriantSlotsRoom(self, room: int) -> int:
        return MapleCharacter.ariantroomslot[room]

    def removeAriantRoom(self, room: int) -> None:
        MapleCharacter.ariantroomleader[room] = ""
        MapleCharacter.ariantroomslot[room] = 0

    def setAriantRoomLeader(self, room: int, charname: str) -> None:
        MapleCharacter.ariantroomleader[room] = charname

    def setAriantSlotRoom(self, room: int, slot: int) -> None:
        MapleCharacter.ariantroomslot[room] = slot

    def run(self) -> None:
        energyLevel = 0
        MapleCharacter.self.setBuffedValue(MapleBuffStat.能量获得, energyLevel)
        stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, energyLevel))
        MapleCharacter.self.client.getSession().write(MaplePacketCreator.能量条(stat, 0))
        MapleCharacter.self.cancelEnergy = True

    def saveToDB(self, dc: bool, fromcs: bool) -> None:
        if self.isClone():
            return
        con = DatabaseConnection.getConnection()
        ps = None
        ps2 = None
        ps3 = None
        ps4 = None
        rs = None
        try:
            con.setTransactionIsolation(1)
            con.setAutoCommit(False)
            ps = con.prepareStatement("UPDATE characters SET level = ?, fame = ?, str = ?, dex = ?, luk = ?, `int` = ?, exp = ?, hp = ?, mp = ?, maxhp = ?, maxmp = ?, sp = ?, ap = ?, gm = ?, skincolor = ?, gender = ?, job = ?, hair = ?, face = ?, map = ?, meso = ?, hpApUsed = ?, spawnpoint = ?, party = ?, buddyCapacity = ?, monsterbookcover = ?, dojo_pts = ?, dojoRecord = ?, pets = ?, subcategory = ?, marriageId = ?, currentrep = ?, totalrep = ?, charmessage = ?, expression = ?, constellation = ?, blood = ?, month = ?, day = ?, beans = ?, prefix = ?, skillzq = ?, bosslog = ?, PGMaxDamage = ?, jzname = ?, mrfbrw = ?, mrsjrw = ?, mrsgrw = ?, mrsbossrw = ?, hythd = ?, mrsgrwa = ?, mrfbrwa = ?, mrsbossrwa = ?, mrsgrws = ?, mrsbossrws = ?, mrfbrws = ?, mrsgrwas = ?, mrsbossrwas = ?, mrfbrwas = ?, ddj = ?, vip = ?, djjl = ?, qiandao = ?, jf = ?, pvpDeaths = ?, pvpKills = ?, pvpVictory = ?, shaguai = ?, name = ? WHERE id = ?", DatabaseConnection.RETURN_GENERATED_KEYS)
            ps.setInt(1, self.level)
            ps.setShort(2, self.fame)
            ps.setShort(3, self.stats.getStr())
            ps.setShort(4, self.stats.getDex())
            ps.setShort(5, self.stats.getLuk())
            ps.setShort(6, self.stats.getInt())
            ps.setInt(7, self.exp)
            ps.setShort(8, (short)((self.stats.getHp() < 1) ? 50 : self.stats.getHp()))
            ps.setShort(9, self.stats.getMp())
            ps.setShort(10, self.stats.getMaxHp())
            ps.setShort(11, self.stats.getMaxMp())
            sps = ""
            for i in range(self.len(remainingSp)):
                sps.append(self.remainingSp[i])
                sps.append(",")
            sp = sps
            ps.setString(12, sp[0:sp.__len__(] - 1))
            ps.setShort(13, self.remainingAp)
            ps.setByte(14, self.gmLevel)
            ps.setByte(15, self.skinColor)
            ps.setByte(16, self.gender)
            ps.setShort(17, self.job)
            ps.setInt(18, self.hair)
            ps.setInt(19, self.face)
            if not fromcs and self.map is not None:
                if self.map.getForcedReturnId() != 999999999:
                    ps.setInt(20, self.map.getForcedReturnId())
                else:
                    ps.setInt(20, (self.stats.getHp() < 1) ? self.map.getReturnMapId() : self.map.getId())
            else:
                ps.setInt(20, self.mapid)
            ps.setInt(21, self.meso)
            ps.setShort(22, self.hpApUsed)
            if self.map is None:
                ps.setByte(23, 0)
            else:
                closest = self.map.findClosestSpawnpoint(self.getPosition())
                ps.setByte(23, (byte)((closest is not None) ? closest.getId() : 0))
            ps.setInt(24, (self.party is not None) ? self.party.getId() : -1)
            ps.setShort(25, self.buddylist.getCapacity())
            ps.setInt(26, self.bookCover)
            ps.setInt(27, self.dojo)
            ps.setInt(28, self.dojoRecord)
            petz = ""
            petLength = 0
            for pet in self.pets:
                pet.saveToDb()
                if pet.getSummoned():
                    petz.append(pet.getInventoryPosition())
                    petz.append(",")
                    petLength += 1
            while petLength < 3:
                petz.append("-1,")
                petLength += 1
            petstring = petz
            ps.setString(29, petstring[0:petstring.__len__(] - 1))
            ps.setByte(30, self.subcategory)
            ps.setInt(31, self.marriageId)
            ps.setInt(32, self.currentrep)
            ps.setInt(33, self.totalrep)
            ps.setString(34, self.charmessage)
            ps.setInt(35, self.expression)
            ps.setInt(36, self.constellation)
            ps.setInt(37, self.blood)
            ps.setInt(38, self.month)
            ps.setInt(39, self.day)
            ps.setInt(40, self.beans)
            ps.setInt(41, self.prefix)
            ps.setInt(42, self.skillzq)
            ps.setInt(43, self.bosslog)
            ps.setInt(44, self.PGMaxDamage)
            ps.setInt(45, self.jzname)
            ps.setInt(46, self.mrfbrw)
            ps.setInt(47, self.mrsjrw)
            ps.setInt(48, self.mrsgrw)
            ps.setInt(49, self.mrsbossrw)
            ps.setInt(50, self.hythd)
            ps.setInt(51, self.mrsgrwa)
            ps.setInt(52, self.mrfbrwa)
            ps.setInt(53, self.mrsbossrwa)
            ps.setInt(54, self.mrsgrws)
            ps.setInt(55, self.mrsbossrws)
            ps.setInt(56, self.mrfbrws)
            ps.setInt(57, self.mrsgrwas)
            ps.setInt(58, self.mrsbossrwas)
            ps.setInt(59, self.mrfbrwas)
            ps.setInt(60, self.ddj)
            ps.setInt(61, self.vip)
            ps.setInt(62, self.djjl)
            ps.setInt(63, self.qiandao)
            ps.setInt(64, self.jf)
            ps.setInt(65, self.pvpDeaths)
            ps.setInt(66, self.pvpKills)
            ps.setInt(67, self.pvpVictory)
            ps.setInt(68, self.shaguai)
            ps.setString(69, self.name)
            ps.setInt(70, self.id)
            if ps.executeUpdate() < 1:
                ps.close()
                raise DatabaseException("Character not in database (" + self.id + ")")
            ps.close()
            ps = con.prepareStatement("UPDATE skillmacros SET `skill1` = ?, `skill2` = ?, `skill3` = ?, `name` = ?, `shout` = ? WHERE `characterid` = ? and `position` = ?")
            ps.setInt(6, self.id)
            for j in range(5):
                macro = self.skillMacros[j]
                if macro is not None:
                    ps.setInt(1, macro.getSkill1())
                    ps.setInt(2, macro.getSkill2())
                    ps.setInt(3, macro.getSkill3())
                    ps.setString(4, macro.getName())
                    ps.setInt(5, macro.getShout())
                    ps.setInt(7, j)
                    ps.executeUpdate()
            ps = con.prepareStatement("UPDATE inventoryslot SET `equip` = ?, `use` = ?, `setup` = ?, `etc` = ?, `cash` = ? WHERE characterid = ?")
            ps.setByte(1, self.getInventory(MapleInventoryType.EQUIP).getSlotLimit())
            ps.setByte(2, self.getInventory(MapleInventoryType.USE).getSlotLimit())
            ps.setByte(3, self.getInventory(MapleInventoryType.SETUP).getSlotLimit())
            ps.setByte(4, self.getInventory(MapleInventoryType.ETC).getSlotLimit())
            ps.setByte(5, self.getInventory(MapleInventoryType.CASH).getSlotLimit())
            ps.setInt(6, self.id)
            ps.executeUpdate()
            ps.close()
            listing = new ArrayList<Pair<IItem, MapleInventoryType>>()
            for iv in self.inventory:
                for item in iv.list():
                    listing.add(new Pair<IItem, MapleInventoryType>(item, iv.getType()))
            if con is not None:
                ItemLoader.装备道具.saveItems(listing, con, self.id)
            else:
                ItemLoader.装备道具.saveItems(listing, self.id)
            ps = con.prepareStatement("SELECT * FROM questinfo WHERE `characterid` = ? AND `quest` = ? LIMIT 1")
            ps.setInt(1, self.id)
            for (final Map.Entry<Integer, String> q : self.questinfo.items())
                questID = q.getKey()
                ps.setInt(2, questID)
                rs = ps.executeQuery()
                if rs.next():
                    ps2 = con.prepareStatement("UPDATE questinfo SET `customData` = ? WHERE `characterid` = ? AND `quest` = ?")
                    ps2.setString(1, q.getValue())
                    ps2.setInt(2, self.id)
                    ps2.setInt(3, questID)
                    ps2.executeUpdate()
                    ps2.close()
                else:
                    ps2 = con.prepareStatement("INSERT INTO questinfo (`characterid`, `quest`, `customData`) VALUES (?, ?, ?)")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, q.getKey())
                    ps2.setString(3, q.getValue())
                    ps2.executeUpdate()
                    ps2.close()
                rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM queststatus WHERE `characterid` = ? AND `quest` = ? LIMIT 1")
            ps.setInt(1, self.id)
            for q2 in self.quests.values():
                questID = q2.getQuest().getId()
                ps.setInt(2, questID)
                rs = ps.executeQuery()
                if rs.next():
                    ps2 = con.prepareStatement("UPDATE queststatus SET `status` = ?, `time` = ?, `forfeited` = ?, `customData` = ? WHERE `characterid` = ? AND `quest` = ?")
                    ps2.setInt(1, q2.getStatus())
                    ps2.setInt(2, (int)(q2.getCompletionTime() / 1000))
                    ps2.setInt(3, q2.getForfeited())
                    ps2.setString(4, q2.getCustomData())
                    ps2.setInt(5, self.id)
                    ps2.setInt(6, questID)
                    ps2.executeUpdate()
                    queststatusid = rs.getInt("queststatusid")
                    if q2.hasMobKills():
                        ps3 = con.prepareStatement("UPDATE queststatusmobs SET `count` = ? WHERE `queststatusid` = ? AND `mob` = ?")
                        for mob in q2.getMobKills().keys():
                            ps3.setInt(1, q2.getMobKills(mob))
                            ps3.setInt(2, queststatusid)
                            ps3.setInt(3, mob)
                            ps3.executeUpdate()
                        ps3.close()
                    rs.close()
                    ps2.close()
                else:
                    ps2 = con.prepareStatement("INSERT INTO queststatus (`queststatusid`, `characterid`, `quest`, `status`, `time`, `forfeited`, `customData`) VALUES (DEFAULT, ?, ?, ?, ?, ?, ?)", 1)
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, q2.getQuest().getId())
                    ps2.setInt(3, q2.getStatus())
                    ps2.setInt(4, (int)(q2.getCompletionTime() / 1000))
                    ps2.setInt(5, q2.getForfeited())
                    ps2.setString(6, q2.getCustomData())
                    ps2.executeUpdate()
                    rs.close()
                    rs = ps2.getGeneratedKeys()
                    rs.next()
                    if q2.hasMobKills():
                        ps3 = con.prepareStatement("INSERT INTO queststatusmobs VALUES (DEFAULT, ?, ?, ?)")
                        for mob2 in q2.getMobKills().keys():
                            ps3.setInt(1, rs.getInt(1))
                            ps3.setInt(2, mob2)
                            ps3.setInt(3, q2.getMobKills(mob2))
                            ps3.executeUpdate()
                        ps3.close()
                    rs.close()
                    ps2.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM skills WHERE `characterid` = ?")
            ps.setInt(1, self.id)
            rs = ps.executeQuery()
            while rs.next():
                skillID = rs.getInt("skillid")
                find = False
                for (final Map.Entry<ISkill, SkillEntry> skill : self.skills.items())
                    if skill.getKey().getId() == skillID:
                        find = True
                        break
                if not find:
                    ps2 = con.prepareStatement("DELETE FROM skills WHERE `characterid` = ? AND `skillid` = ?")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, skillID)
                    ps2.execute()
                    ps2.close()
            ps.close()
            rs.close()
            ps = con.prepareStatement("SELECT * FROM skills WHERE `characterid` = ? AND `skillid` = ? LIMIT 1")
            ps.setInt(1, self.id)
            for (final Map.Entry<ISkill, SkillEntry> skill2 : self.skills.items())
                skillID2 = skill2.getKey().getId()
                if not GameConstants.isApplicableSkill(skillID2):
                    continue
                ps.setInt(2, skillID2)
                rs = ps.executeQuery()
                if rs.next():
                    ps2 = con.prepareStatement("UPDATE skills SET `skilllevel` = ?, `masterlevel` = ?, `expiration` = ? WHERE `characterid` = ? AND `skillid` = ?")
                    ps2.setByte(1, skill2.getValue().skillevel)
                    ps2.setByte(2, skill2.getValue().masterlevel)
                    ps2.setLong(3, skill2.getValue().expiration)
                    ps2.setInt(4, self.id)
                    ps2.setInt(5, skill2.getKey().getId())
                    ps2.executeUpdate()
                    ps2.close()
                else:
                    ps2 = con.prepareStatement("INSERT INTO skills (characterid, skillid, skilllevel, masterlevel, expiration) VALUES (?, ?, ?, ?, ?)")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, skill2.getKey().getId())
                    ps2.setByte(3, skill2.getValue().skillevel)
                    ps2.setByte(4, skill2.getValue().masterlevel)
                    ps2.setLong(5, skill2.getValue().expiration)
                    ps2.execute()
                rs.close()
            ps.close()
            cd = self.getCooldowns()
            if dc and cd > 0:
                ps = con.prepareStatement("INSERT INTO skills_cooldowns (charid, SkillID, StartTime, length) VALUES (?, ?, ?, ?)")
                ps.setInt(1, self.getId())
                for cooling in cd:
                    ps.setInt(2, cooling.skillId)
                    ps.setLong(3, cooling.startTime)
                    ps.setLong(4, len(cooling))
                    ps.execute()
                ps.close()
            ps = con.prepareStatement("SELECT * FROM savedlocations WHERE `characterid` = ?")
            ps.setInt(1, self.id)
            rs = ps.executeQuery()
            while rs.next():
                locationType = rs.getInt("locationtype")
                find2 = False
                for savedLocationType in SavedLocationType.values():
                    if self.savedLocations[savedLocationType.getValue()] != -1 and savedLocationType.getValue() == locationType:
                        find2 = True
                        break
                if not find2:
                    ps2 = con.prepareStatement("DELETE FROM savedlocations WHERE `characterid` = ? AND `locationtype` = ?")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, locationType)
                    ps2.execute()
                    ps2.close()
            ps.close()
            rs.close()
            ps = con.prepareStatement("SELECT * FROM savedlocations WHERE `characterid` = ? AND `locationtype` = ? LIMIT 1")
            ps.setInt(1, self.id)
            for savedLocationType2 in SavedLocationType.values():
                locationType2 = savedLocationType2.getValue()
                ps.setInt(2, locationType2)
                rs = ps.executeQuery()
                if rs.next():
                    if self.savedLocations[savedLocationType2.getValue()] != -1:
                        ps2 = con.prepareStatement("UPDATE savedlocations SET `map` = ? WHERE `characterid` = ? AND `locationtype` = ?")
                        ps2.setInt(1, self.savedLocations[savedLocationType2.getValue()])
                        ps2.setInt(2, self.id)
                        ps2.setInt(3, savedLocationType2.getValue())
                        ps2.executeUpdate()
                        ps2.close()
                elif self.savedLocations[savedLocationType2.getValue()] != -1:
                    ps2 = con.prepareStatement("INSERT INTO savedlocations (characterid, `locationtype`, `map`) VALUES (?, ?, ?)")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, savedLocationType2.getValue())
                    ps2.setInt(3, self.savedLocations[savedLocationType2.getValue()])
                    ps2.execute()
                    ps2.close()
                rs.close()
            ps.close()
            if self.buddylist.changed():
                ps = con.prepareStatement("SELECT * FROM buddies WHERE `characterid` = ?")
                ps.setInt(1, self.id)
                rs = ps.executeQuery()
                while rs.next():
                    buddyID = rs.getInt("buddyid")
                    find2 = False
                    for entry in self.buddylist.getBuddies():
                        if entry is not None and entry.getCharacterId() == buddyID:
                            find2 = True
                            break
                    if not find2:
                        ps2 = con.prepareStatement("DELETE FROM buddies WHERE `characterid` = ? AND `buddyid` = ?")
                        ps2.setInt(1, self.id)
                        ps2.setInt(2, buddyID)
                        ps2.execute()
                        ps2.close()
                ps.close()
                rs.close()
                ps = con.prepareStatement("SELECT * FROM buddies WHERE `characterid` = ? AND `buddyid` = ? LIMIT 1")
                ps.setInt(1, self.id)
                for entry2 in self.buddylist.getBuddies():
                    buddyID2 = entry2.getCharacterId()
                    ps.setInt(2, buddyID2)
                    rs = ps.executeQuery()
                    if rs.next():
                        if entry2 is not None:
                            ps2 = con.prepareStatement("UPDATE buddies SET `pending` = ?, `groupname` = ? WHERE `characterid` = ? AND `buddyid` = ?")
                            ps2.setInt(1, entry2.isVisible() ? 0 : 1)
                            ps2.setString(2, entry2.getGroup())
                            ps2.setInt(3, self.id)
                            ps2.setInt(4, buddyID2)
                            ps2.executeUpdate()
                            ps2.close()
                    elif entry2 is not None:
                        ps2 = con.prepareStatement("INSERT INTO buddies (`characterid`, `buddyid`, `pending`, `groupname`) VALUES (?, ?, ?, ?)")
                        ps2.setInt(1, self.id)
                        ps2.setInt(2, buddyID2)
                        ps2.setInt(3, entry2.isVisible() ? 0 : 1)
                        ps2.setString(4, entry2.getGroup())
                        ps2.execute()
                        ps2.close()
                    rs.close()
                ps.close()
            ps = con.prepareStatement("UPDATE accounts SET `ACash` = ?, `mPoints` = ?, `points` = ?, `vpoints` = ? WHERE id = ?")
            ps.setInt(1, self.acash)
            ps.setInt(2, self.maplepoints)
            ps.setInt(3, self.points)
            ps.setInt(4, self.vpoints)
            ps.setInt(5, self.client.getAccID())
            ps.execute()
            ps.close()
            if self.storage is not None:
                self.storage.saveToDB()
            ps = con.prepareStatement("UPDATE accounts SET `lastGainHM` = ? WHERE id = ?")
            ps.setLong(1, self.lastGainHM)
            ps.setInt(2, self.client.getAccID())
            ps.execute()
            ps.close()
            if self.cs is not None:
                self.cs.save()
            PlayerNPC.updateByCharId(this)
            self.keylayout.saveKeys(self.id)
            self.mount.saveMount(self.id)
            self.monsterbook.saveCards(self.id)
            self.pvpStats.saveToDb(self.accountid)
            self.deleteWhereCharacterId(con, "DELETE FROM wishlist WHERE characterid = ?")
            for k in range(self.getWishlistSize()):
                ps = con.prepareStatement("INSERT INTO wishlist(characterid, sn) VALUES(?, ?) ")
                ps.setInt(1, self.getId())
                ps.setInt(2, self.wishlist[k])
                ps.execute()
                ps.close()
            ps = con.prepareStatement("SELECT * FROM trocklocations WHERE `characterid` = ?")
            ps.setInt(1, self.id)
            rs = ps.executeQuery()
            while rs.next():
                mapid = rs.getInt("mapid")
                find2 = False
                for l in range(self.len(rocks)):
                    if self.rocks[l] == mapid:
                        find2 = True
                        break
                if not find2:
                    ps2 = con.prepareStatement("DELETE FROM trocklocations WHERE `characterid` = ? AND `mapid` = ?")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, mapid)
                    ps2.execute()
                    ps2.close()
            ps.close()
            rs.close()
            ps = con.prepareStatement("SELECT * FROM trocklocations WHERE `characterid` = ? AND `mapid` = ?")
            ps.setInt(1, self.id)
            for k in range(self.len(rocks)):
                mapid2 = self.rocks[k]
                ps.setInt(2, mapid2)
                rs = ps.executeQuery()
                if not rs.next():
                    ps2 = con.prepareStatement("INSERT INTO trocklocations (`characterid`, `mapid`) VALUES (?, ?)")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, mapid2)
                    ps2.execute()
                    ps2.close()
                rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM regrocklocations WHERE `characterid` = ?")
            ps.setInt(1, self.id)
            rs = ps.executeQuery()
            while rs.next():
                mapid = rs.getInt("mapid")
                find2 = False
                for l in range(self.len(regrocks)):
                    if self.regrocks[l] == mapid:
                        find2 = True
                        break
                if not find2:
                    ps2 = con.prepareStatement("DELETE FROM regrocklocations WHERE `characterid` = ? AND `mapid` = ?")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, mapid)
                    ps2.execute()
                    ps2.close()
            ps.close()
            rs.close()
            ps = con.prepareStatement("SELECT * FROM regrocklocations WHERE `characterid` = ? AND `mapid` = ?")
            ps.setInt(1, self.id)
            for k in range(self.len(regrocks)):
                mapid2 = self.regrocks[k]
                ps.setInt(2, mapid2)
                rs = ps.executeQuery()
                if not rs.next():
                    ps2 = con.prepareStatement("INSERT INTO regrocklocations (`characterid`, `mapid`) VALUES (?, ?)")
                    ps2.setInt(1, self.id)
                    ps2.setInt(2, mapid2)
                    ps2.execute()
                    ps2.close()
                rs.close()
            ps.close()
            con.commit()
        except SQLException as ex2:
            pass
        except DatabaseException as ex3:
            pass
        except UnsupportedOperationException as e:
            FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e)
            print(MapleClient.getLogMessage(this, "[charsave] 保存角色数据出现错误") + e)
            try:
                con.rollback()
            except Exception as ex:
                FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, ex)
                print(MapleClient.getLogMessage(this, "[charsave] 保存角色数据出现错误") + e)
            try:
                if ps is not None:
                    ps.close()
                if ps2 is not None:
                    ps2.close()
                if ps3 is not None:
                    ps3.close()
                if ps4 is not None:
                    ps4.close()
                if rs is not None:
                    rs.close()
                con.setAutoCommit(True)
                con.setTransactionIsolation(4)
            except Exception as e2:
                FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e2)
                print(MapleClient.getLogMessage(this, "[charsave] Error going back to autocommit mode") + e2)
        finally:
            try:
                if ps is not None:
                    ps.close()
                if ps2 is not None:
                    ps2.close()
                if ps3 is not None:
                    ps3.close()
                if ps4 is not None:
                    ps4.close()
                if rs is not None:
                    rs.close()
                con.setAutoCommit(True)
                con.setTransactionIsolation(4)
            except Exception as e3:
                FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e3)
                print(MapleClient.getLogMessage(this, "[charsave] Error going back to autocommit mode") + e3)

    def deleteWhereCharacterId_con_sql(self, con: Any, sql: str) -> None:
        deleteWhereCharacterId(con, sql, self.id)

    def getStat(self) -> Any:
        return self.stats

    def CRand(self) -> Any:
        return self.CRand

    def QuestInfoPacket(self, mplew: Any) -> None:
        mplew.writeShort(self.questinfo)
        for (final Map.Entry<Integer, String> q : self.questinfo.items())
            mplew.writeShort(q.getKey())
            mplew.writeMapleAsciiString((q.getValue() is None) ? "" : q.getValue())

    def updateInfoQuest(self, questid: int, data: str) -> None:
        self.questinfo.put(questid, data)
        self.client.getSession().write(MaplePacketCreator.updateInfoQuest(questid, data))

    def getInfoQuest(self, questid: int) -> str:
        if (questid in self.questinfo):
            return self.questinfo.get(questid)
        return ""

    def getNumQuest(self) -> int:
        i = 0
        for q in self.quests.values():
            if q.getStatus() == 2 and not q.isCustom():
                i += 1
        return i

    def getQuestStatus(self, quest: int) -> int:
        return self.getQuest(MapleQuest.getInstance(quest)).getStatus()

    def getQuest(self, quest: Any) -> Any:
        if not (quest in self.quests):
            return MapleQuestStatus(quest, 0)
        return self.quests.get(quest)

    def setQuestAdd(self, quest: int) -> None:
        self.setQuestAddZ(MapleQuest.getInstance(quest), 2, None)

    def setQuestAddZ(self, quest: Any, status: int, customData: str) -> None:
        stat = MapleQuestStatus(quest, status)
        stat.setCustomData(customData)
        self.quests.put(quest, stat)

    def setQuestAdd_quest_status_customData(self, quest: Any, status: int, customData: str) -> None:
        if not (quest in self.quests):
            stat = MapleQuestStatus(quest, status)
            stat.setCustomData(customData)
            self.quests.put(quest, stat)

    def getQuestNAdd(self, quest: Any) -> Any:
        if not (quest in self.quests):
            status = MapleQuestStatus(quest, 0)
            self.quests.put(quest, status)
            return status
        return self.quests.get(quest)

    def getQuestRemove(self, quest: Any) -> Any:
        return self.quests.remove(quest)

    def getQuestNoAdd(self, quest: Any) -> Any:
        return self.quests.get(quest)

    def updateQuest(self, quest: Any) -> None:
        self.updateQuest(quest, False)

    def updateQuest_quest_update(self, quest: Any, update: bool) -> None:
        self.quests.put(quest.getQuest(), quest)
        if not quest.isCustom():
            self.client.getSession().write(MaplePacketCreator.updateQuest(quest))
            if quest.getStatus() == 1 and not update:
                self.client.getSession().write(MaplePacketCreator.updateQuestInfo(this, quest.getQuest().getId(), quest.getNpc(), 8))

    def getInfoQuest_Map(self) -> dict:
        return self.questinfo

    def getQuest_Map(self) -> dict:
        return self.quests

    def isActiveBuffedValue(self, skillid: int) -> bool:
        allBuffs = [])
        for mbsvh in allBuffs:
            if mbsvh.effect.isSkill() and mbsvh.effect.getSourceId() == skillid:
                return True
        return False

    def getBuffedValue(self, effect: Any) -> int:
        mbsvh = self.effects.get(effect)
        return (mbsvh is None) ? None : Integer.valueOf(mbsvh.value)

    def getBuffedSkill_X(self, effect: Any) -> int:
        mbsvh = self.effects.get(effect)
        if mbsvh is None:
            return None
        return mbsvh.effect.getX()

    def getBuffedSkill_Y(self, effect: Any) -> int:
        mbsvh = self.effects.get(effect)
        if mbsvh is None:
            return None
        return mbsvh.effect.getY()

    def isBuffFrom(self, stat: Any, skill: Any) -> bool:
        mbsvh = self.effects.get(stat)
        return mbsvh is not None and mbsvh.effect.isSkill() and mbsvh.effect.getSourceId() == skill.getId()

    def getBuffSource(self, stat: Any) -> int:
        mbsvh = self.effects.get(stat)
        return (mbsvh is None) ? -1 : mbsvh.effect.getSourceId()

    def getItemQuantity(self, itemid: int, checkEquipped: bool) -> int:
        possesed = self.inventory[GameConstants.getInventoryType(itemid).ordinal()].countById(itemid)
        if checkEquipped:
            possesed += self.inventory[MapleInventoryType.EQUIPPED.ordinal()].countById(itemid)
        return possesed

    def setBuffedValue(self, effect: Any, value: int) -> None:
        mbsvh = self.effects.get(effect)
        if mbsvh is None:
            return
        mbsvh.value = value

    def getBuffedStarttime(self, effect: Any) -> int:
        mbsvh = self.effects.get(effect)
        return (mbsvh is None) ? None : Long.valueOf(mbsvh.startTime)

    def getStatForBuff(self, effect: Any) -> Any:
        mbsvh = self.effects.get(effect)
        return (mbsvh is None) ? None : mbsvh.effect

    def prepareDragonBlood(self, bloodEffect: Any) -> None:
        def _task_1():
            if MapleCharacter.self.stats.getHp() - bloodEffect.getX() > 1:
                MapleCharacter.self.cancelBuffStats(MapleBuffStat.龙之力)
            else:
                MapleCharacter.self.addHP(-bloodEffect.getX())
                MapleCharacter.self.client.getSession().write(MaplePacketCreator.showOwnBuffEffect(bloodEffect.getSourceId(), 5))
                MapleCharacter.self.map.broadcastMessage(MapleCharacter.this, MaplePacketCreator.showBuffeffect(MapleCharacter.self.getId(), bloodEffect.getSourceId(), 5), False)

        if self.dragonBloodSchedule is not None:
            self.dragonBloodSchedule.cancel(False)
        self.dragonBloodSchedule = Timer.BuffTimer.getInstance().register(_task_1, 4000, 4000)

    def startMapTimeLimitTask(self, time: int, to: Any) -> None:
        def _task_1():
            MapleCharacter.self.changeMap(to, to.getPortal(0))

        self.client.getSession().write(MaplePacketCreator.getClock(time))
        time *= 1000
        self.mapTimeLimitTask = Timer.MapTimer.getInstance().register(_task_1, time, time)

    def startFishingTask(self, VIP: bool) -> None:
        def _task_1():
            expMulti = MapleCharacter.self.haveItem(2300001, 1, False, True)
            if not expMulti and not MapleCharacter.self.haveItem(2300000, 1, False, True):
                MapleCharacter.self.cancelFishingTask()
                return
            MapleInventoryManipulator.removeById(MapleCharacter.self.client, MapleInventoryType.USE, expMulti ? 2300001 : 2300000, 1, False, False)
            randval = RandomRewards.getInstance().getFishingReward()
            tmp = Randomizer.nextInt(10000)
            tmp2 = Randomizer.nextInt(10000)
            if tmp2 == 9998:
                if MapleItemInformationProvider.getInstance().itemExists(2101070):
                    if MapleCharacter.self.getInventory(GameConstants.getInventoryType(2101070)).getNextFreeSlot() > -1:
                        MapleInventoryManipulator.addById(MapleCharacter.self.client, 2101070, 1, 0)
                        MapleCharacter.self.client.getSession().write( UIPacket.fishingUpdate(0, 2101070))
                        MapleCharacter.self.getClient().getSession().write(UIPacket.getTopMsg("钓鱼获得:[" + MapleItemInformationProvider.getInstance().getName(2101070) + "]not "))
                        MapleCharacter.self.dropMessage(6, "钓鱼获得:[" + MapleItemInformationProvider.getInstance().getName(2101070) + "]not ")
                        msg = MapleCharacter.self.getName() + "钓到了传说中的大金鱼，据说其肚内藏有无尽的宝物！"
                        World.Broadcast.broadcastSmega(MaplePacketCreator.serverNotice(12, MapleCharacter.self.getClient().getChannel(), "[钓鱼公告] : " + msg).encode("utf-8"))
                    else:
                        MapleCharacter.self.dropMessage(5, "背包满了!停止钓鱼!")
                        MapleCharacter.self.dropTopMsg("背包满了!停止钓鱼!")
                        MapleCharacter.self.cancelFishingTask()
            elif tmp == 9998:
                MapleCharacter.self.dropMessage(5, "什么都没发生")
                MapleCharacter.self.dropTopMsg("什么都没发生")
            elif tmp % 3 == 0:
                if MapleItemInformationProvider.getInstance().itemExists(randval):
                    if MapleCharacter.self.getInventory(GameConstants.getInventoryType(randval)).getNextFreeSlot() > -1:
                        MapleInventoryManipulator.addById(MapleCharacter.self.client, randval, 1, 0)
                        MapleCharacter.self.client.getSession().write(UIPacket.fishingUpdate(0, randval))
                        MapleCharacter.self.getClient().getSession().write(UIPacket.getTopMsg("钓鱼获得:[" + MapleItemInformationProvider.getInstance().getName(randval) + "]not "))
                        MapleCharacter.self.dropMessage(6, "钓鱼获得:[" + MapleItemInformationProvider.getInstance().getName(randval) + "]not ")
                    else:
                        MapleCharacter.self.dropMessage(5, "背包满了!停止钓鱼!")
                        MapleCharacter.self.dropTopMsg("背包满了!停止钓鱼!")
                        MapleCharacter.self.cancelFishingTask()
            else:
                MapleCharacter.self.dropMessage(5, "运气背，什么都没钓到")
            MapleCharacter.self.map.broadcastMessage(UIPacket.fishingCaught(MapleCharacter.self.id))

        time = 5000
        self.cancelFishingTask()
        self.fishing = Timer.EtcTimer.getInstance().register(_task_1, time, time)

    def dropTopMsg(self, message: str) -> None:
        self.client.getSession().write(UIPacket.getTopMsg(message))

    def cancelMapTimeLimitTask(self) -> None:
        if self.mapTimeLimitTask is not None:
            self.mapTimeLimitTask.cancel(False)
            self.mapTimeLimitTask = None

    def cancelFishingTask(self) -> None:
        if self.fishing is not None:
            self.fishing.cancel(False)

    def registerEffect(self, effect: Any, starttime: int, schedule: Any) -> None:
        self.registerEffect(effect, starttime, schedule, effect.getStatups())

    def registerEffect_effect_starttime_schedule_statups(self, effect: Any, starttime: int, schedule: Any, statups: list) -> None:
        if effect.is隐藏术():
            self.hidden = True
            self.map.broadcastMessage(this, MaplePacketCreator.removePlayerFromMap(self.getId(), this), False)
        elif effect.isDragonBlood():
            self.prepareDragonBlood(effect)
        elif effect.isBerserk():
            self.checkBerserk()
        elif effect.isMonsterRiding_():
            self.getMount().startSchedule()
        elif effect.is灵魂助力():
            self.prepareBeholderEffect()
        elif effect.getSourceId() == 1001 or effect.getSourceId() == 10001001 or effect.getSourceId() == 1001:
            self.prepareRecovery()
        clonez = 0
        for statup in statups:
            if statup.getLeft() == MapleBuffStat.ILLUSION:
                clonez = statup.getRight()
            value = statup.getRight()
            if statup.getLeft() == MapleBuffStat.骑兽技能 and effect.getSourceId() == 5221006 and self.battleshipHP <= 0:
                self.battleshipHP = value
            self.effects.put(statup.getLeft(), MapleBuffStatValueHolder(effect, starttime, schedule, value))
        if clonez > 0:
            cloneSize = max(self.getNumClones(), self.getCloneSize())
            if clonez > cloneSize:
                for i in range(clonez - cloneSize):
                    self.cloneLook()
        self.stats.recalcLocalStats()

    def getBuffStats(self, effect: Any, startTime: int) -> list:
        bstats = []
        allBuffs = new EnumMap<MapleBuffStat, MapleBuffStatValueHolder>(self.effects)
        for (final Map.Entry<MapleBuffStat, MapleBuffStatValueHolder> stateffect : allBuffs.items())
            mbsvh = stateffect.getValue()
            if mbsvh.effect.sameSource(effect) and (startTime == -1 or startTime == mbsvh.startTime):
                bstats.add(stateffect.getKey())
        return bstats

    def deregisterBuffStats(self, stats: list) -> bool:
        clonez = False
        effectsToCancel = [])
        for stat in stats:
            mbsvh = self.effects.remove(stat)
            if mbsvh is not None:
                addMbsvh = True
                for contained in effectsToCancel:
                    if mbsvh.startTime == contained.startTime and contained.effect == mbsvh.effect:
                        addMbsvh = False
                if addMbsvh:
                    effectsToCancel.add(mbsvh)
                if stat == MapleBuffStat.召唤兽 or stat == MapleBuffStat.替身术 or stat == MapleBuffStat.灵魂助力 or stat == MapleBuffStat.REAPER or stat == MapleBuffStat.RAINING_MINES:
                    summonId = mbsvh.effect.getSourceId()
                    toRemove = []
                    self.visibleMapObjectsLock.writeLock().lock()
                    self.summonsLock.writeLock().lock()
                    try:
                        for summon in self.summons:
                            if summon.getSkill() == summonId or (stat == MapleBuffStat.RAINING_MINES and summonId == 33101008) or (summonId == 35121009 and summon.getSkill() == 35121011) or ((summonId == 86 or summonId == 88 or summonId == 91 or summonId == 180 or summonId == 96) and summon.getSkill() == summonId + 999) or ((summonId == 1085 or summonId == 1087 or summonId == 1090 or summonId == 1179 or summonId == 1154) and summon.getSkill() == summonId - 999):
                                self.map.broadcastMessage(MaplePacketCreator.removeSummon(summon, True))
                                self.map.removeMapObject(summon)
                                self.visibleMapObjects.remove(summon)
                                toRemove.add(summon)
                            if summon.getSkill() == 1321007:
                                if self.beholderHealingSchedule is not None:
                                    self.beholderHealingSchedule.cancel(False)
                                    self.beholderHealingSchedule = None
                                if self.beholderBuffSchedule is None:
                                    continue
                                self.beholderBuffSchedule.cancel(False)
                                self.beholderBuffSchedule = None
                        for s in toRemove:
                            self.summons.remove(s)
                    finally:
                        self.summonsLock.writeLock().unlock()
                        self.visibleMapObjectsLock.writeLock().unlock()
                elif stat == MapleBuffStat.龙之力:
                    if self.dragonBloodSchedule is None:
                        continue
                    self.dragonBloodSchedule.cancel(False)
                    self.dragonBloodSchedule = None
                elif stat == MapleBuffStat.神圣祈祷:
                    self.cancelBuffStats(MapleBuffStat.神圣祈祷)
                elif stat == MapleBuffStat.灵魂助力:
                    self.cancelBuffStats(MapleBuffStat.灵魂助力)
                else:
                    if stat != MapleBuffStat.ILLUSION:
                        continue
                    self.disposeClones()
                    clonez = True
        for cancelEffectCancelTasks in effectsToCancel:
            if self.getBuffStats(cancelEffectCancelTasks.effect, cancelEffectCancelTasks.startTime) == 0 and cancelEffectCancelTasks.schedule is not None:
                cancelEffectCancelTasks.schedule.cancel(False)
        return clonez

    def cancelEffect(self, effect: Any, overwrite: bool, startTime: int) -> None:
        if effect is None:
            return
        self.cancelEffect(effect, overwrite, startTime, effect.getStatups())

    def cancelEffect_effect_overwrite_startTime_statups(self, effect: Any, overwrite: bool, startTime: int, statups: list) -> None:
        if effect is None:
            return
        buffstats = None
        if not overwrite:
            buffstats = self.getBuffStats(effect, startTime)
        else:
            buffstats = [])
            for statup in statups:
                buffstats.add(statup.getLeft())
        if buffstats <= 0:
            return
        clonez = self.deregisterBuffStats(buffstats)
        if effect.is时空门():
            if not self.getDoors() == 0:
                door = self.getDoors().iterator().next()
                for chr in door.getTarget().getCharacters():
                    door.sendDestroyData(chr.client)
                for chr in door.getTown().getCharacters():
                    door.sendDestroyData(chr.client)
                for destroyDoor in self.getDoors():
                    door.getTarget().removeMapObject(destroyDoor)
                    door.getTown().removeMapObject(destroyDoor)
                self.removeDoor()
                self.silentPartyUpdate()
        elif effect.isMonsterRiding_():
            self.getMount().cancelSchedule()
        elif effect.isMonsterRiding():
            self.cancelEffectFromBuffStat(MapleBuffStat.金属机甲)
        elif effect.isMonsterS():
            self.getMount().cancelSchedule()
        elif effect.is神圣祈祷():
            self.cancelBuffStats(MapleBuffStat.神圣祈祷)
        elif effect.isAranCombo():
            self.aranCombo = 0
        if not overwrite:
            if effect.isMonsterS():
                self.cancelPlayerBuffs(buffstats, effect)
            else:
                self.cancelPlayerBuffs(buffstats)
            if effect.is隐藏术() and self.client.getChannelServer().getPlayerStorage().getCharacterById(self.getId()) is not None:
                self.hidden = False
                self.map.broadcastMessage(this, MaplePacketCreator.spawnPlayerMapobject(this), False)
                for pet in self.pets:
                    if pet.getSummoned():
                        self.map.broadcastMessage(this, PetPacket.showPet(this, pet, False, False), False)
                clones = self.clones
                length = len(clones)
                n = 0
                if n < length:
                    chr2 = clones[n]
                    if chr2.get() is not None:
                        self.map.broadcastMessage(chr2.get(), MaplePacketCreator.spawnPlayerMapobject(chr2.get()), False)
        if not clonez:
            clones2 = self.clones
            length2 = len(clones2)
            n2 = 0
            if n2 < length2:
                chr2 = clones2[n2]
                if chr2.get() is not None:
                    chr2.get().cancelEffect(effect, overwrite, startTime)

    def cancelBuffStats(self, stat: Any) -> None:
        buffStatList = Arrays.asList(stat)
        self.deregisterBuffStats(buffStatList)
        self.cancelPlayerBuffs(buffStatList)

    def cancelEffectFromBuffStat(self, stat: Any) -> None:
        if self.effects.get(stat) is not None:
            self.cancelEffect(self.effects.get(stat).effect, False, -1)

    def cancelPlayerBuffs(self, buffstats: list) -> None:
        write = self.client.getChannelServer().getPlayerStorage().getCharacterById(self.getId()) is not None
        if (MapleBuffStat.导航辅助 in buffstats):
            if write:
                self.client.getSession().write(MaplePacketCreator.cancelHoming())
        elif (MapleBuffStat.骑兽技能 in buffstats):
            self.client.getSession().write(MaplePacketCreator.cancelBuffMONSTER(buffstats))
            self.map.broadcastMessage(this, MaplePacketCreator.cancelForeignBuffMONSTER(self.getId(), buffstats), False)
        else:
            self.client.getSession().write(MaplePacketCreator.cancelBuff(buffstats))
            self.map.broadcastMessage(this, MaplePacketCreator.cancelForeignBuff(self.getId(), buffstats), False)

    def cancelPlayerBuffs_buffstats_effect(self, buffstats: list, effect: Any) -> None:
        if effect.isMonsterS():
            self.client.getSession().write(MaplePacketCreator.cancelBuffMONSTERS(buffstats))
            self.map.broadcastMessage(this, MaplePacketCreator.cancelForeignBuffMONSTERS(self.getId(), buffstats), False)

    def dispel(self) -> None:
        if not self.isHidden():
            allBuffs = [])
            for mbsvh in allBuffs:
                if mbsvh.effect.isSkill() and mbsvh.schedule is not None and not mbsvh.effect.isMorph():
                    self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)

    def dispelSkill(self, skillid: int) -> None:
        allBuffs = [])
        for mbsvh in allBuffs:
            if skillid == 0:
                if mbsvh.effect.isSkill() and (mbsvh.effect.getSourceId() == 4331003 or mbsvh.effect.getSourceId() == 4331002 or mbsvh.effect.getSourceId() == 4341002 or mbsvh.effect.getSourceId() == 22131001 or mbsvh.effect.getSourceId() == 1321007 or mbsvh.effect.getSourceId() == 2121005 or mbsvh.effect.getSourceId() == 2221005 or mbsvh.effect.getSourceId() == 2311006 or mbsvh.effect.getSourceId() == 2321003 or mbsvh.effect.getSourceId() == 3111002 or mbsvh.effect.getSourceId() == 3111005 or mbsvh.effect.getSourceId() == 3211002 or mbsvh.effect.getSourceId() == 3211005 or mbsvh.effect.getSourceId() == 4111002):
                    self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)
                    break
                continue
            else:
                if mbsvh.effect.isSkill() and mbsvh.effect.getSourceId() == skillid:
                    self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)
                    break
                continue

    def dispelBuff(self, skillid: int) -> None:
        allBuffs = [])
        for mbsvh in allBuffs:
            if mbsvh.effect.getSourceId() == skillid:
                self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)
                break

    def cancelAllBuffs_(self) -> None:
        self.effects.clear()

    def cancelAllBuffs(self) -> None:
        allBuffs = [])
        for mbsvh in allBuffs:
            self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)

    def cancelMorphs(self) -> None:
        allBuffs = [])
        for mbsvh in allBuffs:
            # switch (mbsvh.effect.getSourceId()):
                # case 5111005:
                # case 5121003:
                # case 13111005:
                case 15111002: {}
                # default:
                    if not mbsvh.effect.isMorph():
                        continue
                    self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)
                    continue

    def getMorphState(self) -> int:
        allBuffs = [])
        for mbsvh in allBuffs:
            if mbsvh.effect.isMorph():
                return mbsvh.effect.getSourceId()
        return -1

    def silentGiveBuffs(self, buffs: list) -> None:
        if buffs is None:
            return
        for mbsvh in buffs:
            mbsvh.effect.silentApplyBuff(this, mbsvh.startTime)

    def getAllBuffs(self) -> list:
        ret = []
        allBuffs = [])
        for mbsvh in allBuffs:
            ret.add(PlayerBuffValueHolder(mbsvh.startTime, mbsvh.effect))
        return ret

    def cancelMagicDoor(self) -> None:
        allBuffs = [])
        for mbsvh in allBuffs:
            if mbsvh.effect.is时空门():
                self.cancelEffect(mbsvh.effect, False, mbsvh.startTime)
                break

    def getSkillLevel(self, skillid: int) -> int:
        return self.getSkillLevel(SkillFactory.getSkill(skillid))

    def handleEnergyCharge(self, skillid: int, targets: int) -> None:
        echskill = SkillFactory.getSkill(skillid)
        skilllevel = self.getSkillLevel(echskill)
        if skilllevel > 0:
            echeff = echskill.getEffect(skilllevel)
            if targets > 0:
                if self.getBuffedValue(MapleBuffStat.能量获得) is None:
                    echeff.applyEnergyBuff(this, True)
                else:
                    energyLevel = self.getBuffedValue(MapleBuffStat.能量获得)
                    if energyLevel <= 10000:
                        energyLevel += echeff.getX() * targets
                        self.client.getSession().write(MaplePacketCreator.showOwnBuffEffect(skillid, 2))
                        self.map.broadcastMessage(this, MaplePacketCreator.showBuffeffect(self.id, skillid, 2), False)
                        if energyLevel >= 10000:
                            energyLevel = 10000
                            if self.cancelEnergy:
                                Timer.BuffTimer.getInstance().schedule(self.cancelEnergyRunnable, 100000)
                                self.cancelEnergy = False
                        stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, energyLevel))
                        self.client.getSession().write(MaplePacketCreator.能量条(stat, energyLevel / 1000))
                        self.setBuffedValue(MapleBuffStat.能量获得, energyLevel)

    def handleBattleshipHP(self, damage: int) -> None:
        if self.isActiveBuffedValue(5221006):
            self.battleshipHP -= damage
            if self.battleshipHP <= 0:
                self.battleshipHP = 0
                effect = self.getStatForBuff(MapleBuffStat.骑兽技能)
                self.client.getSession().write(MaplePacketCreator.skillCooldown(5221006, effect.getCooldown()))
                self.addCooldown(5221006, int(time.time() * 1000), effect.getCooldown() * 1000)
                self.dispelSkill(5221006)

    def handleOrbgain(self) -> None:
        if self.getBuffedValue(MapleBuffStat.斗气集中) is None:
            return
        orbcount = self.getBuffedValue(MapleBuffStat.斗气集中)
        combo = None
        advcombo = None
        # switch (self.getJob()):
            # case 1110:
            # case 1111:
            # case 1112:
                combo = SkillFactory.getSkill(11111001)
                advcombo = SkillFactory.getSkill(11110005)
                break
            # default:
                combo = SkillFactory.getSkill(1111002)
                advcombo = SkillFactory.getSkill(1120003)
                break
        ceffect = None
        advComboSkillLevel = self.getSkillLevel(advcombo)
        if advComboSkillLevel > 0:
            ceffect = advcombo.getEffect(advComboSkillLevel)
        else:
            if self.getSkillLevel(combo) <= 0:
                return
            ceffect = combo.getEffect(self.getSkillLevel(combo))
        if orbcount < ceffect.getX() + 1:
            neworbcount = orbcount + 1
            if advComboSkillLevel > 0 and ceffect.makeChanceResult() and neworbcount < ceffect.getX() + 1:
                neworbcount += 1
            stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.斗气集中, neworbcount))
            self.setBuffedValue(MapleBuffStat.斗气集中, neworbcount)
            duration = ceffect.getDuration()
            duration += (int)(self.getBuffedStarttime(MapleBuffStat.斗气集中) - int(time.time() * 1000))
            self.client.getSession().write(MaplePacketCreator.giveBuff(combo.getId(), duration, stat, ceffect))
            self.map.broadcastMessage(this, MaplePacketCreator.giveForeignBuff(this, self.getId(), stat, ceffect), False)

    def handleOrbconsume(self) -> None:
        combo = None
        # switch (self.getJob()):
            # case 1110:
            # case 1111:
                combo = SkillFactory.getSkill(11111001)
                break
            # default:
                combo = SkillFactory.getSkill(1111002)
                break
        if self.getSkillLevel(combo) <= 0:
            return
        ceffect = self.getStatForBuff(MapleBuffStat.斗气集中)
        if ceffect is None:
            return
        stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.斗气集中, 1))
        self.setBuffedValue(MapleBuffStat.斗气集中, 1)
        duration = ceffect.getDuration()
        duration += (int)(self.getBuffedStarttime(MapleBuffStat.斗气集中) - int(time.time() * 1000))
        self.client.getSession().write(MaplePacketCreator.giveBuff(combo.getId(), duration, stat, ceffect))
        self.map.broadcastMessage(this, MaplePacketCreator.giveForeignBuff(this, self.getId(), stat, ceffect), False)

    def silentEnforceMaxHpMp(self) -> None:
        self.stats.setMp(self.stats.getMp())
        self.stats.setHp(self.stats.getHp(), True)

    def enforceMaxHpMp(self) -> None:
        statups = new ArrayList<Pair<MapleStat, Integer>>(2)
        if self.stats.getMp() > self.stats.getCurrentMaxMp():
            self.stats.setMp(self.stats.getMp())
            statups.add(new Pair<MapleStat, Integer>(MapleStat.MP, self.stats.getMp()))
        if self.stats.getHp() > self.stats.getCurrentMaxHp():
            self.stats.setHp(self.stats.getHp())
            statups.add(new Pair<MapleStat, Integer>(MapleStat.HP, self.stats.getHp()))
        if statups > 0:
            self.client.getSession().write( MaplePacketCreator.updatePlayerStats(statups, self.getJob()))

    def getMap(self) -> Any:
        return self.map

    def getMonsterBook(self) -> Any:
        return self.monsterbook

    def setMap(self, newmap: Any) -> None:
        self.map = newmap

    def setMap_PmapId(self, PmapId: int) -> None:
        self.mapid = PmapId

    def getMapId(self) -> int:
        if self.map is not None:
            return self.map.getId()
        return self.mapid

    def getInitialSpawnpoint(self) -> int:
        return self.initialSpawnPoint

    def getId(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def getBlessOfFairyOrigin(self) -> str:
        return self.BlessOfFairy_Origin

    def getLevel(self) -> int:
        return self.level

    def getFame(self) -> int:
        return self.fame

    def getDojo(self) -> int:
        return self.dojo

    def getDojoRecord(self) -> int:
        return self.dojoRecord

    def getFallCounter(self) -> int:
        return self.fallcounter

    def getClient(self) -> Any:
        return self.client

    def setClient(self, client: Any) -> None:
        self.client = client

    def getExp(self) -> int:
        return self.exp

    def getRemainingAp(self) -> int:
        return self.remainingAp

    def getRemainingSp(self) -> int:
        return self.remainingSp[GameConstants.getSkillBook(self.job)]

    def getRemainingSp_skillbook(self, skillbook: int) -> int:
        return self.remainingSp[skillbook]

    def getRemainingSps(self) -> list:
        return self.remainingSp

    def getRemainingSpSize(self) -> int:
        ret = 0
        for i in range(self.len(remainingSp)):
            if self.remainingSp[i] > 0:
                ret += 1
        return ret

    def getHpApUsed(self) -> int:
        return self.hpApUsed

    def isHidden(self) -> bool:
        return self.hidden

    def setHpApUsed(self, hpApUsed: int) -> None:
        self.hpApUsed = hpApUsed

    def getSkinColor(self) -> int:
        return self.skinColor

    def setSkinColor(self, skinColor: int) -> None:
        self.skinColor = skinColor

    def getJob(self) -> int:
        return self.job

    def getGender(self) -> int:
        return self.gender

    def getHair(self) -> int:
        return self.hair

    def getFace(self) -> int:
        return self.face

    def setName(self, name: str) -> None:
        self.name = name

    def setExp(self, exp: int) -> None:
        self.exp = exp

    def setHair(self, hair: int) -> None:
        self.hair = hair

    def setFace(self, face: int) -> None:
        self.face = face

    def setFame(self, fame: int) -> None:
        self.fame = fame

    def setDojo(self, dojo: int) -> None:
        self.dojo = dojo

    def setDojoRecord(self, reset: bool) -> None:
        if reset:
            self.dojo = 0
            self.dojoRecord = 0
        else:
            self.dojoRecord += 1

    def setFallCounter(self, fallcounter: int) -> None:
        self.fallcounter = fallcounter

    def getOldPosition(self) -> Any:
        return self.old

    def setOldPosition(self, x: Any) -> None:
        self.old = x

    def setRemainingAp(self, remainingAp: int) -> None:
        self.remainingAp = remainingAp

    def setRemainingSp(self, remainingSp: int) -> None:
        self.remainingSp[GameConstants.getSkillBook(self.job)] = remainingSp

    def setRemainingSp_remainingSp_skillbook(self, remainingSp: int, skillbook: int) -> None:
        self.remainingSp[skillbook] = remainingSp

    def setGender(self, gender: int) -> None:
        self.gender = gender

    def setInvincible(self, invinc: bool) -> None:
        self.invincible = invinc

    def isInvincible(self) -> bool:
        return self.invincible

    def getCheatTracker(self) -> Any:
        return self.anticheat

    def getBuddylist(self) -> Any:
        return self.buddylist

    def addFame(self, famechange: int) -> None:
        self.fame += famechange

    def changeMapBanish(self, mapid: int, portal: str, msg: str) -> None:
        self.dropMessage(5, msg)
        map = self.client.getChannelServer().getMapFactory().getMap(mapid)
        if map is not None:
            self.changeMap(map, map.getPortal(portal))

    def changeMap(self, to: int) -> None:
        map = ChannelServer.getInstance(self.getClient().getChannel()).getMapFactory().getMap(to)
        self.changeMapInternal(map, map.getPortal(0).getPosition(), MaplePacketCreator.getWarpToMap(map, 0, this), map.getPortal(0))

    def changeMap_map_portal(self, map: int, portal: int) -> None:
        warpMap = self.client.getChannelServer().getMapFactory().getMap(map)
        self.changeMap(warpMap, warpMap.getPortal(portal))

    def changeMap_to_pos(self, to: Any, pos: Any) -> None:
        self.changeMapInternal(to, pos, MaplePacketCreator.getWarpToMap(to, 128, this), None)

    def changeMap_to_pto(self, to: Any, pto: Any) -> None:
        self.changeMapInternal(to, pto.getPosition(), MaplePacketCreator.getWarpToMap(to, pto.getId(), this), None)

    def changeMapPortal(self, to: Any, pto: Any) -> None:
        self.changeMapInternal(to, pto.getPosition(), MaplePacketCreator.getWarpToMap(to, pto.getId(), this), pto)

    def changeMapInternal(self, to: Any, pos: Any, warpPacket: Any, pto: Any) -> None:
        if to is None:
            return
        self.saveToDB(False, False)
        nowmapid = self.map.getId()
        if self.eventInstance is not None:
            self.eventInstance.changedMap(this, to.getId())
        pyramid = self.pyramidSubway is not None
        if self.map.getId() == nowmapid:
            self.client.getSession().write(warpPacket)
            self.map.removePlayer(this)
            if not self.isClone() and self.client.getChannelServer().getPlayerStorage().getCharacterById(self.getId()) is not None:
                self.map = to
                self.setPosition(pos)
                self.setStance(0)
                self.setPosition(Point(pos.x, pos.y - 50))
                to.addPlayer(this)
                self.stats.relocHeal()
        if self.party is not None:
            self.silentPartyUpdate()
            self.getClient().getSession().write(MaplePacketCreator.updateParty(self.getClient().getChannel(), self.party, PartyOperation.SILENT_UPDATE, None))
            self.updatePartyMemberHP()
        if pyramid and self.pyramidSubway is not None:
            self.pyramidSubway.onChangeMap(this, to.getId())

    def leaveMap(self, map: Any) -> None:
        self.controlledLock.writeLock().lock()
        self.visibleMapObjectsLock.writeLock().lock()
        try:
            for mons in self.controlled:
                if mons is not None:
                    mons.setController(None)
                    mons.setControllerHasAggro(False)
                    map.updateMonsterController(mons)
            self.controlled.clear()
            self.visibleMapObjects.clear()
        finally:
            self.controlledLock.writeLock().unlock()
            self.visibleMapObjectsLock.writeLock().unlock()
        if self.chair != 0:
            self.chair = 0
        self.cancelFishingTask()
        self.cancelMapTimeLimitTask()
        if self.getTrade() is not None:
            MapleTrade.cancelTrade(self.getTrade(), self.client)

    def changeJob(self, newJob: int) -> None:
        try:
            isEv = GameConstants.isEvan(self.job) or GameConstants.isResist(self.job)
            self.job = newJob
            if newJob != 0 and newJob != 1000 and newJob != 2000 and newJob != 2001 and newJob != 3000:
                if isEv:
                    remainingSp = self.remainingSp
                    skillBook = GameConstants.getSkillBook(newJob)
                    remainingSp[skillBook] += 5
                    self.client.getSession().write(UIPacket.getSPMsg(5, newJob))
                else:
                    remainingSp2 = self.remainingSp
                    skillBook2 = GameConstants.getSkillBook(newJob)
                    ++remainingSp2[skillBook2]
                    if newJob % 10 >= 2:
                        remainingSp3 = self.remainingSp
                        skillBook3 = GameConstants.getSkillBook(newJob)
                        remainingSp3[skillBook3] += 2
            if newJob > 0 and not self.isGM():
                self.resetStatsByJob(True)
                if not GameConstants.isEvan(newJob):
                    if self.getLevel() > ((newJob == 200) ? 8 : 10) and newJob % 100 == 0 and newJob % 1000 / 100 > 0:
                        remainingSp4 = self.remainingSp
                        skillBook4 = GameConstants.getSkillBook(newJob)
                        remainingSp4[skillBook4] += 3 * (self.getLevel() - ((newJob == 200) ? 8 : 10))
                elif newJob == 2200:
                    MapleQuest.getInstance(22100).forceStart(this, 0, None)
                    MapleQuest.getInstance(22100).forceComplete(this, 0)
                    self.expandInventory(1, 4)
                    self.expandInventory(2, 4)
                    self.expandInventory(3, 4)
                    self.expandInventory(4, 4)
                    self.client.getSession().write(MaplePacketCreator.getEvanTutorial("UI/tutorial/evan/14/0"))
                    self.dropMessage(5, "The baby Dragon hatched and appears to have something to tell you. Click the baby Dragon to start a conversation.")
            self.client.getSession().write(MaplePacketCreator.updateSp(this, False, isEv))
            self.updateSingleStat(MapleStat.JOB, newJob)
            maxhp = self.stats.getMaxHp()
            maxmp = self.stats.getMaxMp()
            # switch (self.job):
                # case 100:
                # case 1100:
                # case 2100:
                # case 3200:
                    maxhp += Randomizer.rand(200, 250)
                    break
                # case 200:
                # case 2200:
                # case 2210:
                    maxmp += Randomizer.rand(100, 150)
                    break
                # case 300:
                # case 400:
                # case 500:
                # case 3300:
                # case 3500:
                    maxhp += Randomizer.rand(100, 150)
                    maxmp += Randomizer.rand(25, 50)
                    break
                # case 110:
                    maxhp += Randomizer.rand(300, 350)
                    break
                # case 120:
                # case 130:
                # case 510:
                # case 512:
                # case 1110:
                # case 2110:
                # case 3210:
                    maxhp += Randomizer.rand(300, 350)
                    break
                # case 210:
                # case 220:
                # case 230:
                    maxmp += Randomizer.rand(400, 450)
                    break
                # case 310:
                # case 312:
                # case 320:
                # case 322:
                # case 410:
                # case 412:
                # case 420:
                # case 422:
                # case 430:
                # case 520:
                # case 522:
                # case 1310:
                # case 1410:
                # case 3310:
                # case 3510:
                    maxhp += Randomizer.rand(300, 350)
                    maxhp += Randomizer.rand(150, 200)
                    break
                # case 800:
                # case 900:
                    maxhp += 30000
                    maxhp += 30000
                    break
            if maxhp >= 30000:
                maxhp = 30000
            if maxmp >= 30000:
                maxmp = 30000
            self.stats.setMaxHp(maxhp)
            self.stats.setMaxMp(maxmp)
            self.stats.setHp(maxhp)
            self.stats.setMp(maxmp)
            statup = new ArrayList<Pair<MapleStat, Integer>>(4)
            statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXHP, maxhp))
            statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXMP, maxmp))
            statup.add(new Pair<MapleStat, Integer>(MapleStat.HP, maxhp))
            statup.add(new Pair<MapleStat, Integer>(MapleStat.MP, maxmp))
            self.stats.recalcLocalStats()
            self.client.getSession().write(MaplePacketCreator.updatePlayerStats(statup, self.getJob()))
            self.map.broadcastMessage(this, MaplePacketCreator.showForeignEffect(self.getId(), 8), False)
            self.silentPartyUpdate()
            self.guildUpdate()
            self.familyUpdate()
            self.baseSkills()
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, e)

    def baseSkills(self) -> None:
        if GameConstants.getJobNumber(self.job) >= 3:
            skills = SkillFactory.getSkillsByJob(self.job)
            if skills is not None:
                for i in skills:
                    skil = SkillFactory.getSkill(i)
                    if skil is not None and not skil.isInvisible() and skil.isFourthJob() and self.getSkillLevel(skil) <= 0 and self.getMasterLevel(skil) <= 0 and skil.getMasterLevel() > 0:
                        self.changeSkillLevel(skil, 0, skil.getMasterLevel())

    def gainAp(self, ap: int) -> None:
        self.remainingAp += ap
        self.updateSingleStat(MapleStat.AVAILABLEAP, self.remainingAp)

    def gainSP(self, sp: int) -> None:
        remainingSp = self.remainingSp
        skillBook = GameConstants.getSkillBook(self.job)
        remainingSp[skillBook] += sp
        self.client.getSession().write(MaplePacketCreator.updateSp(this, False))
        self.client.getSession().write(UIPacket.getSPMsg(sp, self.job))

    def gainSP_sp_skillbook(self, sp: int, skillbook: int) -> None:
        remainingSp = self.remainingSp
        remainingSp[skillbook] += sp
        self.client.getSession().write(MaplePacketCreator.updateSp(this, False))
        self.client.getSession().write(UIPacket.getSPMsg(sp, self.job))

    def resetSP(self, sp: int) -> None:
        for i in range(self.len(remainingSp)):
            self.remainingSp[i] = sp
        self.updateSingleStat(MapleStat.AVAILABLESP, self.getRemainingSp())

    def resetAPSP(self) -> None:
        for i in range(self.len(remainingSp)):
            self.remainingSp[i] = 0
        self.client.getSession().write(MaplePacketCreator.updateSp(this, False))
        self.gainAp((short)(-self.remainingAp))

    def getAllSkillLevels(self) -> int:
        rett = 0
        for (Map.Entry<ISkill, SkillEntry> ret : self.skills.items())
            if not (ret.getKey()).isBeginnerSkill() and (ret.getValue()).skillevel > 0:
            rett += (ret.getValue()).skillevel
        return rett

    def changeSkillLevel(self, skill: Any, newLevel: int, newMasterlevel: int) -> None:
        if skill is None:
            return
        self.changeSkillLevel(skill, newLevel, newMasterlevel, skill.isTimeLimited() ? (int(time.time() * 1000) + 2592000000) : -1)

    def changeSkillLevel_skill_newLevel_newMasterlevel_expiration(self, skill: Any, newLevel: int, newMasterlevel: int, expiration: int) -> None:
        if skill is None or (not GameConstants.isApplicableSkill(skill.getId()) and not GameConstants.isApplicableSkill_(skill.getId())):
            return
        self.client.getSession().write(MaplePacketCreator.updateSkill(skill.getId(), newLevel, newMasterlevel, expiration))
        if newLevel == 0 and newMasterlevel == 0:
            if not (skill in self.skills):
                return
            self.skills.remove(skill)
        else:
            self.skills.put(skill, SkillEntry(newLevel, newMasterlevel, expiration))
        if GameConstants.isRecoveryIncSkill(skill.getId()):
            self.stats.relocHeal()
        elif GameConstants.isElementAmp_Skill(skill.getId()):
            self.stats.recalcLocalStats()

    def changeSkillLevel_Skip(self, skill: Any, newLevel: int, newMasterlevel: int) -> None:
        if skill is None:
            return
        self.client.getSession().write(MaplePacketCreator.updateSkill(skill.getId(), newLevel, newMasterlevel, -1))
        if newLevel == 0 and newMasterlevel == 0:
            if (skill in self.skills):
                self.skills.remove(skill)
        else:
            self.skills.put(skill, SkillEntry(newLevel, newMasterlevel, -1))

    def playerDead(self) -> None:
        statss = self.getStatForBuff(MapleBuffStat.灵魂之石)
        if statss is not None:
            self.dropMessage(5, "你已经被灵魂石复活了。")
            self.getStat().setHp(self.getStat().getMaxHp() / 100 * statss.getX())
            self.updateSingleStat(MapleStat.HP, self.getHp())
            self.setStance(0)
            self.changeMap(self.getMap(), self.getMap().getPortal(0))
            return
        charmID = { 5130000, 5130002, 5131000, 4031283, 4140903 }
        possesed = 0
        i = None
        = 0
        while i < len(charmID):
            quantity = self.getItemQuantity(charmID[i], False)
            if possesed == 0 and quantity > 0:
                possesed = quantity
                break
        if possesed > 0:
            possesed -= 1
            self.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "因使用了 [护身符] 死亡后您的经验不会减少！剩余 (" + possesed + " 个)"))
            MapleInventoryManipulator.removeById(self.getClient(), MapleItemInformationProvider.getInstance().getInventoryType(charmID[i]), charmID[i], 1, True, False)
        else:
            if self.getEventInstance() is not None:
                self.getEventInstance().playerKilled(this)
            self.dispelSkill(0)
            self.cancelEffectFromBuffStat(MapleBuffStat.变身)
            self.cancelEffectFromBuffStat(MapleBuffStat.骑兽技能)
            self.cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
            self.cancelEffectFromBuffStat(MapleBuffStat.REAPER)
            self.cancelEffectFromBuffStat(MapleBuffStat.替身术)
            self.checkFollow()
            if self.job != 0 and self.job != 1000 and self.job != 2000:
                diepercentage = 0.0
                expforlevel = GameConstants.getExpNeededForLevel(self.level)
                if self.map.isTown() or FieldLimitType.RegularExpLoss.check(self.map.getFieldLimit()):
                    diepercentage = 0.01
                else:
                    v8 = 0.0
                    if self.job / 100 == 3:
                        v8 = 0.08
                    else:
                        v8 = 0.2
                    diepercentage = (float)(v8 / self.stats.getLuk() + 0.05)
                v9 = (int)(self.exp - (long)(expforlevel * diepercentage))
                if v9 < 0:
                    v9 = 0
                self.exp = v9
            self.updateSingleStat(MapleStat.EXP, self.exp)
            if not self.stats.checkEquipDurabilitys(this, -100):
                self.dropMessage(5, "耐久度已经归零.")
            if self.pyramidSubway is not None:
                self.stats.setHp(50)
                self.pyramidSubway.fail(this)

    def updatePartyMemberHP(self) -> None:
        if self.party is not None:
            channel = self.client.getChannel()
            for partychar in self.party.getMembers():
                if partychar.getMapid() == self.getMapId() and partychar.getChannel() == channel:
                    other = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterByName(partychar.getName())
                    if other is None:
                        continue
                    self.updateSingleStat(MapleStat.HP, self.stats.getHp())
                    other.getClient().getSession().write(MaplePacketCreator.updatePartyMemberHP(self.getId(), self.stats.getHp(), self.stats.getCurrentMaxHp()))

    def receivePartyMemberHP(self) -> None:
        if self.party is None:
            return
        channel = self.client.getChannel()
        for partychar in self.party.getMembers():
            if partychar.getMapid() == self.getMapId() and partychar.getChannel() == channel:
                other = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterByName(partychar.getName())
                if other is None:
                    continue
                self.client.getSession().write(MaplePacketCreator.updatePartyMemberHP(other.getId(), other.getStat().getHp(), other.getStat().getCurrentMaxHp()))

    def healHP(self, delta: int) -> None:
        self.addHP(delta)

    def healMP(self, delta: int) -> None:
        self.addMP(delta)

    def addHP(self, delta: int) -> None:
        if self.stats.setHp(self.stats.getHp() + delta):
            self.updateSingleStat(MapleStat.HP, self.stats.getHp())

    def addMP(self, delta: int) -> None:
        if self.stats.setMp(self.stats.getMp() + delta):
            self.updateSingleStat(MapleStat.MP, self.stats.getMp())

    def addMPHP(self, hpDiff: int, mpDiff: int) -> None:
        statups = new ArrayList<Pair<MapleStat, Integer>>()
        if self.stats.setHp(self.stats.getHp() + hpDiff):
            statups.add(new Pair<MapleStat, Integer>(MapleStat.HP, self.stats.getHp()))
        if self.stats.setMp(self.stats.getMp() + mpDiff):
            statups.add(new Pair<MapleStat, Integer>(MapleStat.MP, self.stats.getMp()))
        if statups > 0:
            self.client.getSession().write(MaplePacketCreator.updatePlayerStats(statups, self.getJob()))

    def canQuestAction(self) -> bool:
        if self.lastQuestTime + 250 > int(time.time() * 1000):
            return False
        self.lastQuestTime = int(time.time() * 1000)
        return True

    def prepareRecovery(self) -> None:
        self.lastRecoveryTime = int(time.time() * 1000)

    def canRecovery(self) -> bool:
        return self.lastRecoveryTime > 0 and self.lastRecoveryTime + 5000 < int(time.time() * 1000) + 5000

    def doRecovery(self) -> None:
        eff = self.getStatForBuff(MapleBuffStat.团队治疗)
        if eff is not None:
            self.prepareRecovery()
            if self.stats.getHp() > self.stats.getCurrentMaxHp():
                self.cancelEffectFromBuffStat(MapleBuffStat.团队治疗)
            else:
                self.healHP(eff.getX())

    def canHP(self) -> bool:
        if self.lastHPTime + 5000 > int(time.time() * 1000):
            return False
        self.lastHPTime = int(time.time() * 1000)
        return True

    def canMP(self) -> bool:
        if self.lastMPTime + 5000 > int(time.time() * 1000):
            return False
        self.lastMPTime = int(time.time() * 1000)
        return True

    def canCheckPeriod(self) -> bool:
        if self.lastCheckPeriodTime + 30000 > int(time.time() * 1000):
            return False
        self.lastCheckPeriodTime = int(time.time() * 1000)
        return True

    def canMoveItem(self) -> bool:
        if self.lastMoveItemTime + 250 > int(time.time() * 1000):
            return False
        self.lastMoveItemTime = int(time.time() * 1000)
        return True

    def updateSingleStat(self, stat: Any, newval: int) -> None:
        self.updateSingleStat(stat, newval, False)

    def updateSingleStat_stat_newval_itemReaction(self, stat: Any, newval: int, itemReaction: bool) -> None:
        statpair = new Pair<MapleStat, Integer>(stat, newval)
        self.client.getSession().write(MaplePacketCreator.updatePlayerStats(Collections.singletonList(statpair), itemReaction, self.getJob()))

    def gainExp(self, total: int, show: bool, inChat: bool, white: bool) -> None:
        try:
            prevexp = self.getExp()
            needed = GameConstants.getExpNeededForLevel(self.level)
            if self.level >= int(ServerProperties.getProperty("RoyMS.MLevel")) or (GameConstants.isKOC(self.job) and self.level >= int(ServerProperties.getProperty("RoyMS.QLevel"))):
                if self.exp + total > needed:
                    self.setExp(needed)
                else:
                    self.exp += total
            else:
                leveled = False
                if self.exp + total >= needed:
                    self.exp += total
                    self.levelUp()
                    leveled = True
                    needed = GameConstants.getExpNeededForLevel(self.level)
                    if self.exp > needed:
                        self.setExp(needed)
                else:
                    self.exp += total
                if total > 0:
                    self.familyRep(prevexp, needed, leveled)
            if total != 0:
                if self.exp < 0:
                    if total > 0:
                        self.setExp(needed)
                    elif total < 0:
                        self.setExp(0)
                if show:
                    self.client.getSession().write(MaplePacketCreator.GainEXP_Others(total, inChat, white))
                self.updateSingleStat(MapleStat.EXP, self.getExp())
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, e)

    def familyRep(self, prevexp: int, needed: int, leveled: bool) -> None:
        if self.mfc is not None:
            onepercent = needed / 100
            percentrep = prevexp / onepercent + self.getExp() / onepercent
            if leveled:
                percentrep = 100 - percentrep + self.level / 2
            if percentrep > 0:
                sensen = World.Family.setRep(self.mfc.getFamilyId(), self.mfc.getSeniorId(), percentrep, self.level)
                if sensen > 0:
                    World.Family.setRep(self.mfc.getFamilyId(), sensen, percentrep / 2, self.level)

    def gainExpMonster(self, gain: int, show: bool, white: bool, pty: int, Class_Bonus_EXP: int, 网吧特别经验: int) -> None:
        组队经验值 = 0
        结婚奖励经验值 = 0
        道具佩戴附加经验值 = 0
        prevexp = self.getExp()
        totalExp = gain + Class_Bonus_EXP + 道具佩戴附加经验值 + 网吧特别经验 + 组队经验值 + 结婚奖励经验值
        if self.marriageId > 0:
            marrChr = self.map.getCharacterById(self.marriageId)
            if marrChr is not None:
                结婚奖励经验值 = (int)(gain / 100.0 * 30.0)
                totalExp += 结婚奖励经验值
        if self.hasEquipped(1122017):
            道具佩戴附加经验值 = (int)(gain / 100.0 * self.fairyExp)
            totalExp += 道具佩戴附加经验值
        if self.haveItem(1142145):
            网吧特别经验 = (int)(gain / 100.0 * 30.0)
            totalExp += 网吧特别经验
        if pty > 1:
            组队经验值 = (int)((float)(gain / 20.0) * (pty + 1))
            totalExp += 组队经验值
        if gain > 0 and totalExp < gain:
            totalExp = 2147483647
        needed = GameConstants.getExpNeededForLevel(self.level)
        if self.level >= int(ServerProperties.getProperty("RoyMS.MLevel")) or (GameConstants.isKOC(self.job) and self.level >= int(ServerProperties.getProperty("RoyMS.QLevel"))):
            if self.exp + totalExp > needed:
                self.setExp(needed)
            else:
                self.exp += totalExp
        else:
            leveled = False
            if self.exp + totalExp >= needed:
                self.exp += totalExp
                self.levelUp()
                leveled = True
                needed = GameConstants.getExpNeededForLevel(self.level)
                if self.exp > needed:
                    self.setExp(needed)
            else:
                self.exp += totalExp
            if totalExp > 0:
                self.familyRep(prevexp, needed, leveled)
        if gain != 0:
            if self.exp < 0:
                if gain > 0:
                    self.setExp(GameConstants.getExpNeededForLevel(self.level))
                elif gain < 0:
                    self.setExp(0)
            self.updateSingleStat(MapleStat.EXP, self.getExp())
            if show:
                self.client.getSession().write(MaplePacketCreator.GainEXP_Monster(gain, white, 结婚奖励经验值, 组队经验值, Class_Bonus_EXP, 道具佩戴附加经验值, 网吧特别经验))

    def forceReAddItem_NoUpdate(self, item: Any, type: Any) -> None:
        self.getInventory(type).removeSlot(item.getPosition())
        self.getInventory(type).addFromDB(item)

    def forceReAddItem(self, item: Any, type: Any) -> None:
        self.forceReAddItem_NoUpdate(item, type)
        if type != MapleInventoryType.UNDEFINED:
            self.client.getSession().write(MaplePacketCreator.updateSpecialItemUse(item, (byte)((type == MapleInventoryType.EQUIPPED) ? 1 : type.getType())))

    def forceReAddItem_Flag(self, item: Any, type: Any) -> None:
        self.forceReAddItem_NoUpdate(item, type)
        if type != MapleInventoryType.UNDEFINED:
            self.client.getSession().write(MaplePacketCreator.updateSpecialItemUse_(item, (byte)((type == MapleInventoryType.EQUIPPED) ? 1 : type.getType())))

    def silentPartyUpdate(self) -> None:
        if self.party is not None:
            World.Party.updateParty(self.party.getId(), PartyOperation.SILENT_UPDATE, MaplePartyCharacter(this))

    def isGM(self) -> bool:
        return self.gmLevel > 0

    def isAdmin(self) -> bool:
        return self.gmLevel >= 2

    def getGMLevel(self) -> int:
        return self.gmLevel

    def isPlayer(self) -> bool:
        return self.gmLevel == 0

    def hasGmLevel(self, level: int) -> bool:
        return self.gmLevel >= level

    def getInventory(self, type: Any) -> Any:
        return self.inventory[type.ordinal()]

    def getInventorys(self) -> list:
        return self.inventory

    def expirationTask(self) -> None:
        self.expirationTask(False)

    def expirationTask_pending(self, pending: bool) -> None:
        self.expirationTask(False, pending)

    def expirationTask_packet_pending(self, packet: bool, pending: bool) -> None:
        if pending:
            if self.pendingExpiration is not None:
                for z in self.pendingExpiration:
                    self.client.sendPacket(MTSCSPacket.itemExpired(z))
            self.pendingExpiration = None
            if self.pendingSkills is not None:
                for z in self.pendingSkills:
                    self.client.sendPacket(MaplePacketCreator.updateSkill(z, 0, 0, -1))
                    self.client.sendPacket(MaplePacketCreator.serverNotice(5, "[" + SkillFactory.getSkillName(z) + "] 技能已过期，无法使用。 "))
            self.pendingSkills = None
            return
        ret = []
        currenttime = int(time.time() * 1000)
        toberemove = new ArrayList<Pair<MapleInventoryType, IItem>>()
        tobeunlock = []
        for inv in MapleInventoryType.values():
            for item in self.getInventory(inv):
                expiration = item.getExpiration()
                if expiration != -1 and not GameConstants.isPet(item.getItemId()) and currenttime > expiration:
                    if ItemFlag.LOCK.check(item.getFlag()):
                        tobeunlock.add(item)
                    else:
                        if currenttime <= expiration:
                            continue
                        toberemove.add(new Pair<MapleInventoryType, IItem>(inv, item))
                else:
                    if item.getItemId() != 5000054 or item.getPet() is None or item.getPet().getSecondsLeft() > 0:
                        continue
                    toberemove.add(new Pair<MapleInventoryType, IItem>(inv, item))
        for itemz in toberemove:
            item2 = itemz.getRight()
            ret.add(item2.getItemId())
            if packet:
                self.getInventory(itemz.getLeft()).removeItem(item2.getPosition(), item2.getQuantity(), False, this)
            else:
                self.getInventory(itemz.getLeft()).removeItem(item2.getPosition(), item2.getQuantity(), False)
        for itemz2 in tobeunlock:
            itemz2.setExpiration(-1)
            itemz2.setFlag((byte)(itemz2.getFlag() - ItemFlag.LOCK.getValue()))
        self.pendingExpiration = ret
        skilz = []
        toberem = []
        for (final Map.Entry<ISkill, SkillEntry> skil : self.skills.items())
            if skil.getValue().expiration != -1 and currenttime > skil.getValue().expiration:
                toberem.add(skil.getKey())
        for skil2 in toberem:
            skilz.add(skil2.getId())
            self.skills.remove(skil2)
        self.pendingSkills = skilz

    def getShop(self) -> Any:
        return self.shop

    def setShop(self, shop: Any) -> None:
        self.shop = shop

    def getMeso(self) -> int:
        return self.meso

    def getSavedLocations(self) -> list:
        return self.savedLocations

    def getSavedLocation(self, type: Any) -> int:
        return self.savedLocations[type.getValue()]

    def saveLocation(self, type: Any) -> None:
        self.savedLocations[type.getValue()] = self.getMapId()

    def saveLocation_type_mapz(self, type: Any, mapz: int) -> None:
        self.savedLocations[type.getValue()] = mapz

    def clearSavedLocation(self, type: Any) -> None:
        self.savedLocations[type.getValue()] = -1

    def getDY(self) -> int:
        return self.maplepoints

    def setDY(self, set: int) -> None:
        self.maplepoints = set

    def gainDY(self, gain: int) -> None:
        self.maplepoints += gain

    def getjf(self) -> int:
        return self.jf

    def setjf(self, count: int) -> None:
        self.jf = count

    def gainjf(self, count: int) -> None:
        self.jf += count

    def gainMeso(self, gain: int, show: bool) -> None:
        self.gainMeso(gain, show, False, False)

    def gainMeso_gain_show_enableActions(self, gain: int, show: bool, enableActions: bool) -> None:
        self.gainMeso(gain, show, enableActions, False)

    def gainMeso_gain_show_enableActions_inChat(self, gain: int, show: bool, enableActions: bool, inChat: bool) -> None:
        if self.meso + gain < 0:
            self.client.getSession().write(MaplePacketCreator.enableActions())
            return
        self.meso += gain
        self.updateSingleStat(MapleStat.MESO, self.meso, enableActions)
        if show:
            self.client.getSession().write(MaplePacketCreator.showMesoGain(gain, inChat))

    def controlMonster(self, monster: Any, aggro: bool) -> None:
        if self.clone or monster is None:
            return
        monster.setController(this)
        self.controlledLock.writeLock().lock()
        try:
            self.controlled.add(monster)
        finally:
            self.controlledLock.writeLock().unlock()
        self.client.getSession().write(MobPacket.controlMonster(monster, False, aggro))

    def stopControllingMonster(self, monster: Any) -> None:
        if self.clone or monster is None:
            return
        self.controlledLock.writeLock().lock()
        try:
            if (monster in self.controlled):
                self.controlled.remove(monster)
        finally:
            self.controlledLock.writeLock().unlock()

    def checkMonsterAggro(self, monster: Any) -> None:
        if self.clone or monster is None:
            return
        if monster.getController() == this:
            monster.setControllerHasAggro(True)
        else:
            monster.switchController(this, True)

    def getControlled(self) -> set:
        return self.controlled

    def getControlledSize(self) -> int:
        return self.controlled

    def getAccountID(self) -> int:
        return self.accountid

    def mobKilled(self, id: int, skillID: int) -> None:
        for q in self.quests.values():
            if q.getStatus() == 1:
                if not q.hasMobKills():
                    continue
                if not q.mobKilled(id, skillID):
                    continue
                self.client.getSession().write(MaplePacketCreator.updateQuestMobKills(q))
                if not q.getQuest().canComplete(this, None):
                    continue
                self.client.getSession().write(MaplePacketCreator.getShowQuestCompletion(q.getQuest().getId()))

    def getStartedQuests(self) -> list:
        ret = []
        for q in self.quests.values():
            if q.getStatus() == 1 and not q.isCustom():
                ret.add(q)
        return ret

    def getCompletedQuests(self) -> list:
        ret = []
        for q in self.quests.values():
            if q.getStatus() == 2 and not q.isCustom():
                ret.add(q)
        return ret

    def getSkills(self) -> dict:
        return Collections.unmodifiableMap((Map<? extends ISkill, ? extends SkillEntry>)self.skills)

    def getSkillLevel_skill(self, skill: Any) -> int:
        ret = self.skills.get(skill)
        if ret is None or ret.skillevel <= 0:
            return 0
        return min(skill.getMaxLevel(), ret.skillevel + (skill.isBeginnerSkill() ? 0 : self.stats.incAllskill))

    def getMasterLevel(self, skill: int) -> int:
        return self.getMasterLevel(SkillFactory.getSkill(skill))

    def getMasterLevel_skill(self, skill: Any) -> int:
        ret = self.skills.get(skill)
        if ret is None:
            return 0
        return ret.masterlevel

    def levelUp(self) -> None:
        if GameConstants.isKOC(self.job):
            if self.level <= 70:
                self.remainingAp += 6
            else:
                self.remainingAp += 5
        else:
            self.remainingAp += 5
        maxhp = self.stats.getMaxHp()
        maxmp = self.stats.getMaxMp()
        if self.job == 0 or self.job == 1000 or self.job == 2000 or self.job == 2001 or self.job == 3000:
            maxhp += Randomizer.rand(12, 16)
            maxmp += Randomizer.rand(10, 12)
        elif self.job >= 100 and self.job <= 132:
            improvingMaxHP = SkillFactory.getSkill(1000001)
            slevel = self.getSkillLevel(improvingMaxHP)
            if slevel > 0:
                maxhp += improvingMaxHP.getEffect(slevel).getX()
            maxhp += Randomizer.rand(24, 28)
            maxmp += Randomizer.rand(4, 6)
        elif self.job >= 200 and self.job <= 232:
            improvingMaxMP = SkillFactory.getSkill(2000001)
            slevel = self.getSkillLevel(improvingMaxMP)
            if slevel > 0:
                maxmp += improvingMaxMP.getEffect(slevel).getX() * 2
            maxhp += Randomizer.rand(10, 14)
            maxmp += Randomizer.rand(22, 24)
        elif self.job >= 3200 and self.job <= 3212:
            maxhp += Randomizer.rand(20, 24)
            maxmp += Randomizer.rand(42, 44)
        elif (self.job >= 300 and self.job <= 322) or (self.job >= 400 and self.job <= 434) or (self.job >= 1300 and self.job <= 1311) or (self.job >= 1400 and self.job <= 1411) or (self.job >= 3300 and self.job <= 3312):
            maxhp += Randomizer.rand(20, 24)
            maxmp += Randomizer.rand(14, 16)
        elif (self.job >= 500 and self.job <= 522) or (self.job >= 3500 and self.job <= 3512):
            improvingMaxHP = SkillFactory.getSkill(5100000)
            slevel = self.getSkillLevel(improvingMaxHP)
            if slevel > 0:
                maxhp += improvingMaxHP.getEffect(slevel).getX()
            maxhp += Randomizer.rand(22, 26)
            maxmp += Randomizer.rand(18, 22)
        elif self.job >= 1100 and self.job <= 1111:
            improvingMaxHP = SkillFactory.getSkill(11000000)
            slevel = self.getSkillLevel(improvingMaxHP)
            if slevel > 0:
                maxhp += improvingMaxHP.getEffect(slevel).getX()
            maxhp += Randomizer.rand(24, 28)
            maxmp += Randomizer.rand(4, 6)
        elif self.job >= 1200 and self.job <= 1211:
            improvingMaxMP = SkillFactory.getSkill(12000000)
            slevel = self.getSkillLevel(improvingMaxMP)
            if slevel > 0:
                maxmp += improvingMaxMP.getEffect(slevel).getX() * 2
            maxhp += Randomizer.rand(10, 14)
            maxmp += Randomizer.rand(22, 24)
        elif self.job >= 1500 and self.job <= 1512:
            improvingMaxHP = SkillFactory.getSkill(15100000)
            slevel = self.getSkillLevel(improvingMaxHP)
            if slevel > 0:
                maxhp += improvingMaxHP.getEffect(slevel).getX()
            maxhp += Randomizer.rand(22, 26)
            maxmp += Randomizer.rand(18, 22)
        elif self.job >= 2100 and self.job <= 2112:
            maxhp += Randomizer.rand(50, 52)
            maxmp += Randomizer.rand(4, 6)
        elif self.job >= 2200 and self.job <= 2218:
            maxhp += Randomizer.rand(12, 16)
            maxmp += Randomizer.rand(50, 52)
        else:
            maxhp += Randomizer.rand(50, 100)
            maxmp += Randomizer.rand(50, 100)
        maxmp += self.stats.getTotalInt() / 10
        self.exp -= GameConstants.getExpNeededForLevel(self.level)
        self.level += 1
        level = self.getLevel()
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "[升级提示]" + self.getName() + "在" + self.getMap().getMapName() + " 等级达到" + level + "级，大家一起祝贺一下吧。"))
        if (level == 3 or level == 6 or level == 9 or level == 12 or level == 15 or level == 18 or level == 21 or level == 24 or level == 27 or level == 30 or level == 33 or level == 36 or level == 39 or level == 42 or level == 45 or level == 48 or level == 51 or level == 54 or level == 57 or level == 60 or level == 63 or level == 66 or level == 69 or level == 72 or level == 75 or level == 78 or level == 81 or level == 84 or level == 87 or level == 90 or level == 93 or level == 96 or level == 99) {}
        maxhp = min(30000, maxhp)
        maxmp = min(30000, maxmp)
        statup = new ArrayList<Pair<MapleStat, Integer>>(8)
        statup.add(new Pair<MapleStat, Integer>(MapleStat.AVAILABLEAP, self.remainingAp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXHP, maxhp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MAXMP, maxmp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.HP, maxhp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.MP, maxmp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.EXP, self.exp))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.LEVEL, level))
        if self.isGM() or (self.job != 0 and self.job != 1000 and self.job != 2000 and self.job != 2001 and self.job != 3000):
            remainingSp = self.remainingSp
            skillBook = GameConstants.getSkillBook(self.job)
            remainingSp[skillBook] += 3
            self.client.getSession().write(MaplePacketCreator.updateSp(this, False))
        elif level <= 10:
            self.stats.setStr((short)(self.stats.getStr() + self.remainingAp))
            self.remainingAp = 0
            statup.add(new Pair<MapleStat, Integer>(MapleStat.STR, self.stats.getStr()))
        statup.add(new Pair<MapleStat, Integer>(MapleStat.AVAILABLEAP, self.remainingAp))
        self.stats.setMaxHp(maxhp)
        self.stats.setMaxMp(maxmp)
        self.stats.setHp(maxhp)
        self.stats.setMp(maxmp)
        self.client.getSession().write(MaplePacketCreator.updatePlayerStats(statup, self.getJob()))
        self.map.broadcastMessage(this, MaplePacketCreator.showForeignEffect(self.getId(), 0), False)
        self.stats.recalcLocalStats()
        self.silentPartyUpdate()
        self.guildUpdate()
        self.familyUpdate()
        self.saveToDB(False, False)

    def changeKeybinding(self, key: int, type: int, action: int) -> None:
        if type != 0:
            self.keylayout.Layout().put(key, new Pair<Byte, Integer>(type, action))
        else:
            self.keylayout.Layout().remove(key)

    def sendMacros(self) -> None:
        for i in range(5):
            if self.skillMacros[i] is not None:
                self.client.getSession().write(MaplePacketCreator.getMacros(self.skillMacros))
                break

    def updateMacros(self, position: int, updateMacro: Any) -> None:
        self.skillMacros[position] = updateMacro

    def getMacros(self) -> list:
        return self.skillMacros

    def tempban(self, reason: str, duration: Any, greason: int, IPMac: bool) -> None:
        if IPMac:
            self.client.banMacs()
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("INSERT INTO ipbans VALUES (DEFAULT, ?)")
            ps.setString(1, self.client.getSession().getRemoteAddress().split(":")[0])
            ps.execute()
            ps.close()
            self.client.getSession().close(True)
            ps = con.prepareStatement("UPDATE accounts SET tempban = ?, banreason = ?, greason = ? WHERE id = ?")
            TS = Timestamp(duration.getTimeInMillis())
            ps.setTimestamp(1, TS)
            ps.setString(2, reason)
            ps.setInt(3, greason)
            ps.setInt(4, self.accountid)
            ps.execute()
            ps.close()
        except Exception as ex:
            print("Error while tempbanning" + ex)

    def ban_reason_IPMac_autoban_hellban(self, reason: str, IPMac: bool, autoban: bool, hellban: bool) -> bool:
        hellban = False
        if self.lastmonthfameids is None:
            raise RuntimeError("Trying to ban a non-loaded character (testhack)")
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts SET banned = ?, banreason = ? WHERE id = ?")
            ps.setInt(1, autoban ? 2 : 1)
            ps.setString(2, reason)
            ps.setInt(3, self.accountid)
            ps.execute()
            ps.close()
            self.client.banMacs()
            if hellban:
                psa = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
                psa.setInt(1, self.accountid)
                rsa = psa.executeQuery()
                if rsa.next():
                    pss = con.prepareStatement("UPDATE accounts SET banned = ?, banreason = ? WHERE email = ? ")
                    pss.setInt(1, autoban ? 2 : 1)
                    pss.setString(2, reason)
                    pss.setString(3, rsa.getString("email"))
                    pss.execute()
                    pss.close()
                rsa.close()
                psa.close()
        except Exception as ex:
            print("Error while banning" + ex)
            return False
        self.client.getSession().close(True)
        return True

    def getObjectId(self) -> int:
        return self.getId()

    def setObjectId(self, id: int) -> None:
        raise NotImplementedError()

    def getStorage(self) -> Any:
        return self.storage

    def addVisibleMapObject(self, mo: Any) -> None:
        if self.clone:
            return
        self.visibleMapObjectsLock.writeLock().lock()
        try:
            self.visibleMapObjects.add(mo)
        finally:
            self.visibleMapObjectsLock.writeLock().unlock()

    def removeVisibleMapObject(self, mo: Any) -> None:
        if self.clone:
            return
        self.visibleMapObjectsLock.writeLock().lock()
        try:
            self.visibleMapObjects.remove(mo)
        finally:
            self.visibleMapObjectsLock.writeLock().unlock()

    def isMapObjectVisible(self, mo: Any) -> bool:
        self.visibleMapObjectsLock.readLock().lock()
        try:
            return not self.clone and (mo in self.visibleMapObjects)
        finally:
            self.visibleMapObjectsLock.readLock().unlock()

    def getAndWriteLockVisibleMapObjects(self) -> list:
        self.visibleMapObjectsLock.writeLock().lock()
        return self.visibleMapObjects

    def unlockWriteVisibleMapObjects(self) -> None:
        self.visibleMapObjectsLock.writeLock().unlock()

    def isAlive(self) -> bool:
        return self.stats.getHp() > 0

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.removePlayerFromMap(self.getObjectId(), this))
        for chr in self.clones:
            if chr.get() is not None:
                chr.get().sendDestroyData(client)

    def sendSpawnData(self, client: Any) -> None:
        if client.getPlayer().allowedToTarget(this):
            client.getSession().write(MaplePacketCreator.spawnPlayerMapobject(this))
            if self.getParty() is not None:
                self.updatePartyMemberHP()
                self.receivePartyMemberHP()
            for pet in self.pets:
                if pet.getSummoned():
                    client.getSession().write(PetPacket.showPet(this, pet, False, False))
                    client.sendPacket(PetPacket.petStatUpdate(this))
            for chr in self.clones:
                if chr.get() is not None:
                    chr.get().sendSpawnData(client)
            if self.summons is not None and self.summons > 0:
                self.summonsLock.readLock().lock()
                try:
                    for summon in self.summons:
                        if summon.getOwner() is not None:
                            client.getSession().write(MaplePacketCreator.spawnSummon(summon, False))
                finally:
                    self.summonsLock.readLock().unlock()
            if (self.followid <= 0 or self.followon) {}

    def equipChanged(self) -> None:
        self.map.broadcastMessage(this, MaplePacketCreator.updateCharLook(this), False)
        self.map.broadcastMessage(MaplePacketCreator.loveEffect())
        self.stats.recalcLocalStats()
        if self.getMessenger() is not None:
            World.Messenger.updateMessenger(self.getMessenger().getId(), self.getName(), self.client.getChannel())
        self.saveToDB(False, False)

    def getPet(self, index: int) -> Any:
        count = 0
        for pet in self.pets:
            if pet.getSummoned():
                if count == index:
                    return pet
                count += 1
        return None

    def addPet(self, pet: Any) -> None:
        if (pet in self.pets):
            self.pets.remove(pet)
        self.pets.add(pet)

    def removePet(self, pet: Any) -> None:
        pet.setSummoned(0)
        self.pets.remove(pet)

    def getSummonedPets(self) -> list:
        ret = []
        for i in range(3):
            ret.add(None)
        for pet in self.pets:
            if pet is not None and pet.getSummoned():
                index = pet.getSummonedValue() - 1
                ret.remove(index)
                ret.add(index, pet)
        nullArr = []
        NoneArr.add(None)
        ret.removeAll(NoneArr)
        return ret

    def getSummonedPet(self, index: int) -> Any:
        for pet in self.getSummonedPets():
            if pet.getSummonedValue() - 1 == index:
                return pet
        return None

    def shiftPetsRight(self) -> None:
        petsz = self.getSummonedPets()
        if petsz < 3:
            if petsz >= 1:
                indexBool = { False, False, False }
                for i in range(3):
                    for p in petsz:
                        if p.getSummonedValue() == i + 1:
                            indexBool[i] = True
                if petsz > 1:
                    if not indexBool[2]:
                        petsz.get(0).setSummoned(2)
                        petsz.get(1).setSummoned(3)
                    elif not indexBool[1]:
                        petsz.get(0).setSummoned(2)
                elif indexBool[0]:
                    petsz.get(0).setSummoned(2)

    def getPetSlotNext(self) -> int:
        petsz = self.getSummonedPets()
        index = 0
        if petsz >= 3:
            self.unequipPet(self.getSummonedPet(0), False)
        else:
            indexBool = { False, False, False }
            for i in range(3):
                for p in petsz:
                    if p.getSummonedValue() == i + 1:
                        indexBool[i] = True
            for b in indexBool:
                if not b:
                    break
                index += 1
            index = min(index, 2)
            for p2 in petsz:
                if p2.getSummonedValue() == index + 1:
                    self.unequipPet(p2, False)
        return index

    def getPetIndex(self, petz: Any) -> int:
        return max(-1, petz.getSummonedValue() - 1)

    def getPetIndex_petId(self, petId: int) -> int:
        for pet in self.getSummonedPets():
            if pet.getUniqueId() == petId:
                return max(-1, pet.getSummonedValue() - 1)
        return -1

    def getPetIndexById(self, petId: int) -> int:
        for pet in self.getSummonedPets():
            if pet.getPetItemId() == petId:
                return max(-1, pet.getSummonedValue() - 1)
        return -1

    def getPets(self) -> list:
        return self.pets

    def unequipAllPets(self) -> None:
        for pet in self.getSummonedPets():
            self.unequipPet(pet, False)

    def unequipPet(self, pet: Any, hunger: bool) -> None:
        if pet.getSummoned():
            pet.saveToDb()
            summonedPets = self.getSummonedPets()
            if (pet in summonedPets):
                summonedPets.remove(pet)
                i = 1
                for p in summonedPets:
                    if p is None:
                        continue
                    p.setSummoned(i)
                    i += 1
            if self.map is not None:
                self.map.broadcastMessage(this, PetPacket.showPet(this, pet, True, hunger), True)
            pet.setSummoned(0)
            self.client.sendPacket(PetPacket.petStatUpdate(this))
            self.client.sendPacket(MaplePacketCreator.enableActions())

    def getLastFameTime(self) -> int:
        return self.lastfametime

    def getFamedCharacters(self) -> list:
        return self.lastmonthfameids

    def canGiveFame(self, from: Any) -> Any:
        if self.lastfametime >= int(time.time() * 1000) - 86400000:
            return FameStatus.NOT_TODAY
        if from is None or self.lastmonthfameids is None or (from.getId( in self.lastmonthfameids)):
            return FameStatus.NOT_THIS_MONTH
        return FameStatus.OK

    def hasGivenFame(self, to: Any) -> None:
        self.lastfametime = int(time.time() * 1000)
        self.lastmonthfameids.add(to.getId())
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("INSERT INTO famelog (characterid, characterid_to) VALUES (?, ?)")
            ps.setInt(1, self.getId())
            ps.setInt(2, to.getId())
            ps.execute()
            ps.close()
        except Exception as e:
            print("ERROR writing famelog for char " + self.getName() + " to " + to.getName() + e)

    def getKeyLayout(self) -> Any:
        return self.keylayout

    def getParty(self) -> Any:
        return self.party

    def getPartyId(self) -> int:
        return (self.party is not None) ? self.party.getId() : -1

    def getWorld(self) -> int:
        return self.world

    def setWorld(self, world: int) -> None:
        self.world = world

    def setParty(self, party: Any) -> None:
        self.party = party

    def getTrade(self) -> Any:
        return self.trade

    def setTrade(self, trade: Any) -> None:
        self.trade = trade

    def getEventInstance(self) -> Any:
        return self.eventInstance

    def setEventInstance(self, eventInstance: Any) -> None:
        self.eventInstance = eventInstance

    def addDoor(self, door: Any) -> None:
        self.doors.add(door)

    def clearDoors(self) -> None:
        self.doors.clear()

    def getDoors(self) -> list:
        return []

    def setSmega(self) -> None:
        if self.smega:
            self.smega = False
            self.dropMessage(5, "You have set megaphone to disabled mode")
        else:
            self.smega = True
            self.dropMessage(5, "You have set megaphone to enabled mode")

    def getSmega(self) -> bool:
        return self.smega

    def getSummons(self) -> list:
        return self.summons

    def getSummonsReadLock(self) -> list:
        self.summonsLock.readLock().lock()
        return self.summons

    def getSummonsSize(self) -> int:
        return self.summons

    def unlockSummonsReadLock(self) -> None:
        self.summonsLock.readLock().unlock()

    def addSummon(self, s: Any) -> None:
        self.summonsLock.writeLock().lock()
        try:
            self.summons.add(s)
        finally:
            self.summonsLock.writeLock().unlock()

    def removeSummon(self, s: Any) -> None:
        self.summonsLock.writeLock().lock()
        try:
            self.summons.remove(s)
        finally:
            self.summonsLock.writeLock().unlock()

    def getChair(self) -> int:
        return self.chair

    def getItemEffect(self) -> int:
        return self.itemEffect

    def setChair(self, chair: int) -> None:
        self.chair = chair
        self.stats.relocHeal()

    def setItemEffect(self, itemEffect: int) -> None:
        self.itemEffect = itemEffect

    def getType(self) -> Any:
        return MapleMapObjectType.PLAYER

    def getFamilyId(self) -> int:
        if self.mfc is None:
            return 0
        return self.mfc.getFamilyId()

    def getSeniorId(self) -> int:
        if self.mfc is None:
            return 0
        return self.mfc.getSeniorId()

    def getJunior1(self) -> int:
        if self.mfc is None:
            return 0
        return self.mfc.getJunior1()

    def getJunior2(self) -> int:
        if self.mfc is None:
            return 0
        return self.mfc.getJunior2()

    def getCurrentRep(self) -> int:
        return self.currentrep

    def getTotalRep(self) -> int:
        return self.totalrep

    def getVip(self) -> int:
        return self.vip

    def getVipexpired(self) -> int:
        return vipexpired

    def setVipexpired(self, vipexpired: int) -> None:
        self.vipexpired = vipexpired

    def setCurrentRep(self, _rank: int) -> None:
        self.currentrep = _rank
        if self.mfc is not None:
            self.mfc.setCurrentRep(_rank)

    def setTotalRep(self, _rank: int) -> None:
        self.totalrep = _rank
        if self.mfc is not None:
            self.mfc.setTotalRep(_rank)

    def getGuildId(self) -> int:
        return self.guildid

    def getGuildRank(self) -> int:
        return self.guildrank

    def setGuildId(self, _id: int) -> None:
        self.guildid = _id
        if self.guildid > 0:
            if self.mgc is None:
                self.mgc = MapleGuildCharacter(this)
            else:
                self.mgc.setGuildId(self.guildid)
        else:
            self.mgc = None

    def setGuildRank(self, _rank: int) -> None:
        self.guildrank = _rank
        if self.mgc is not None:
            self.mgc.setGuildRank(_rank)

    def getMGC(self) -> Any:
        return self.mgc

    def setAllianceRank(self, rank: int) -> None:
        self.allianceRank = rank
        if self.mgc is not None:
            self.mgc.setAllianceRank(rank)

    def getAllianceRank(self) -> int:
        return self.allianceRank

    def getGuild(self) -> Any:
        if self.getGuildId() <= 0:
            return None
        return World.Guild.getGuild(self.getGuildId())

    def guildUpdate(self) -> None:
        if self.guildid <= 0:
            return
        self.mgc.setLevel(self.level)
        self.mgc.setJobId(self.job)
        World.Guild.memberLevelJobUpdate(self.mgc)

    def saveGuildStatus(self) -> None:
        MapleGuild.setOfflineGuildStatus(self.guildid, self.guildrank, self.allianceRank, self.id)

    def familyUpdate(self) -> None:
        if self.mfc is None:
            return
        World.Family.memberFamilyUpdate(self.mfc, this)

    def saveFamilyStatus(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE characters SET familyid = ?, seniorid = ?, junior1 = ?, junior2 = ? WHERE id = ?")
            if self.mfc is None:
                ps.setInt(1, 0)
                ps.setInt(2, 0)
                ps.setInt(3, 0)
                ps.setInt(4, 0)
            else:
                ps.setInt(1, self.mfc.getFamilyId())
                ps.setInt(2, self.mfc.getSeniorId())
                ps.setInt(3, self.mfc.getJunior1())
                ps.setInt(4, self.mfc.getJunior2())
            ps.setInt(5, self.id)
            ps.execute()
            ps.close()
        except Exception as se:
            print("SQLException: " + se.getLocalizedMessage())
            se.printStackTrace()

    def modifyCSPoints(self, type: int, quantity: int) -> None:
        self.modifyCSPoints(type, quantity, False)

    def dropMessage(self, message: str) -> None:
        self.dropMessage(6, message)

    def modifyCSPoints_type_quantity_show(self, type: int, quantity: int, show: bool) -> None:
        # switch (type):
            # case 1:
                if self.acash + quantity < 0:
                    if show:
                        self.dropMessage(5, "你的点卷已经满了")
                    return
                self.acash += quantity
                break
            # case 2:
                if self.maplepoints + quantity < 0:
                    if show:
                        self.dropMessage(5, "你的抵用卷已经满了.")
                    return
                self.maplepoints += quantity
                break
        if show and quantity != 0:
            self.dropMessage(5, "你已经 " + ((quantity > 0) ? "获得 " : "使用 ") + quantity + ((type == 1) ? " 点卷." : " 抵用卷."))

    def getCSPoints(self, type: int) -> int:
        # switch (type):
            # case 1:
                return self.acash
            # case 2:
                return self.maplepoints
            # default:
                return 0

    def hasEquipped(self, itemid: int) -> bool:
        return self.inventory[MapleInventoryType.EQUIPPED.ordinal()].countById(itemid) >= 1

    def haveItem(self, itemid: int, quantity: int, checkEquipped: bool, greaterOrEquals: bool) -> bool:
        type = GameConstants.getInventoryType(itemid)
        possesed = self.inventory[type.ordinal()].countById(itemid)
        if checkEquipped and type == MapleInventoryType.EQUIP:
            possesed += self.inventory[MapleInventoryType.EQUIPPED.ordinal()].countById(itemid)
        if greaterOrEquals:
            return possesed >= quantity
        return possesed == quantity

    def haveItem_itemid_quantity(self, itemid: int, quantity: int) -> bool:
        return self.haveItem(itemid, quantity, True, True)

    def haveItem_itemid(self, itemid: int) -> bool:
        return self.haveItem(itemid, 1, True, True)

    def maxAllSkills(self) -> None:
        dataProvider = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz"))
        skilldData = dataProvider.getData("Skill.img")
        for skill_ in skilldData.getChildren():
            try:
                skill = SkillFactory.getSkill1(int(skill_.getName()))
                if self.level < 0:
                    continue
                self.changeSkillLevel(skill, skill.getMaxLevel(), skill.getMaxLevel())
            except ValueError as nfe:
                break
            except NullPointerException as ex:
                pass

    def setAPQScore(self, score: int) -> None:
        self.APQScore = score

    def getAPQScore(self) -> int:
        return self.APQScore

    def getLasttime(self) -> int:
        return self.lasttime

    def setLasttime(self, lasttime: int) -> None:
        self.lasttime = lasttime

    def getCurrenttime(self) -> int:
        return self.currenttime

    def setCurrenttime(self, currenttime: int) -> None:
        self.currenttime = currenttime

    def petUpdateStats(self, pet: Any) -> None:
        mods = []
        Pet = self.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition())
        mods.add(ModifyInventory(3, Pet))
        mods.add(ModifyInventory(0, Pet))
        self.getClient().getSession().write(MaplePacketCreator.modifyInventory(False, mods))

    def forceUpdateItem(self, item: Any) -> None:
        self.forceUpdateItem(item, False)

    def forceUpdateItem_item_updateTick(self, item: Any, updateTick: bool) -> None:
        mods = []
        mods.add(ModifyInventory(3, item))
        mods.add(ModifyInventory(0, item))
        self.client.getSession().write(MaplePacketCreator.modifyInventory(False, ModifyInventory(ModifyInventory.Types.UPDATE, item)))

    def forceUpdateItem_type_item(self, type: Any, item: Any) -> None:
        self.client.getSession().write(MaplePacketCreator.clearInventoryItem(type, item.getPosition(), False))
        self.client.getSession().write(MaplePacketCreator.addInventorySlot(type, item, False))

    def getAntiMacro(self) -> Any:
        return self.antiMacro

    def startLieDetector(self, isItem: bool) -> None:
        if not self.getAntiMacro().inProgress():
            self.getAntiMacro().startLieDetector(self.getName(), isItem, False)

    def getBuddyCapacity(self) -> int:
        return self.buddylist.getCapacity()

    def setBuddyCapacity(self, capacity: int) -> None:
        self.buddylist.setCapacity(capacity)
        self.client.getSession().write(MaplePacketCreator.updateBuddyCapacity(capacity))

    def getMessenger(self) -> Any:
        return self.messenger

    def setMessenger(self, messenger: Any) -> None:
        self.messenger = messenger

    def addCooldown(self, skillId: int, startTime: int, length: int) -> None:
        self.coolDowns.put(skillId, MapleCoolDownValueHolder(skillId, startTime, length))

    def removeCooldown(self, skillId: int) -> None:
        if (skillId in self.coolDowns):
            self.coolDowns.remove(skillId)

    def skillisCooling(self, skillId: int) -> bool:
        return (skillId in self.coolDowns)

    def giveCoolDowns(self, skillid: int, starttime: int, length: int) -> None:
        self.addCooldown(skillid, starttime, length)

    def giveCoolDowns_cooldowns(self, cooldowns: list) -> None:
        if cooldowns is not None:
            for cooldown in cooldowns:
                self.coolDowns.put(cooldown.skillId, cooldown)
        else:
            try:
                con = DatabaseConnection.getConnection()
                ps = con.prepareStatement("SELECT SkillID,StartTime,length FROM skills_cooldowns WHERE charid = ?")
                ps.setInt(1, self.getId())
                rs = ps.executeQuery()
                while rs.next():
                    if rs.getLong("length") + rs.getLong("StartTime") - int(time.time() * 1000) <= 0:
                        continue
                    self.giveCoolDowns(rs.getInt("SkillID"), rs.getLong("StartTime"), rs.getLong("length"))
                ps.close()
                rs.close()
                self.deleteWhereCharacterId(con, "DELETE FROM skills_cooldowns WHERE charid = ?")
            except Exception as e:
                print("Error while retriving cooldown from SQL storage")

    def getCooldowns(self) -> list:
        return [])

    def getAllDiseases(self) -> list:
        return [])

    def hasDisease(self, dis: Any) -> bool:
        return self.diseases.keys().__contains__(dis)

    def giveDebuff(self, disease: Any, skill: Any) -> None:
        self.giveDebuff(disease, skill.getX(), skill.getDuration(), skill.getSkillId(), skill.getSkillLevel())

    def giveDebuff_disease_x_duration_skillid_level(self, disease: Any, x: int, duration: int, skillid: int, level: int) -> None:
        debuff = Collections.singletonList(new Pair<MapleDisease, Integer>(disease, x))
        if not self.hasDisease(disease) and self.diseases < 2:
            if disease != MapleDisease.诱惑 and disease != MapleDisease.眩晕 and self.isActiveBuffedValue(2321005):
                return
            self.diseases.put(disease, MapleDiseaseValueHolder(disease, int(time.time() * 1000), duration))
            self.client.getSession().write(MaplePacketCreator.giveDebuff(debuff, skillid, level, duration))
            self.map.broadcastMessage(this, MaplePacketCreator.giveForeignDebuff(self.id, debuff, skillid, level), False)
            if x > 0 and disease == MapleDisease.中毒:
                self.addHP((int)(-(x * ((duration - self.stats.decreaseDebuff) / 1000))))

    def giveSilentDebuff(self, ld: list) -> None:
        if ld is not None:
            for disease in ld:
                self.diseases.put(disease.disease, disease)

    def dispelDebuff(self, debuff: Any) -> None:
        if self.hasDisease(debuff):
            mask = debuff.getValue()
            first = debuff.isFirst()
            self.client.getSession().write(MaplePacketCreator.cancelDebuff(mask, first))
            self.map.broadcastMessage(this, MaplePacketCreator.cancelForeignDebuff(self.id, mask, first), False)
            self.diseases.remove(debuff)

    def dispelDebuffs(self) -> None:
        diseasess = [])
        for d in diseasess:
            self.dispelDebuff(d)

    def cancelAllDebuffs(self) -> None:
        self.diseases.clear()

    def getDiseaseSize(self) -> int:
        return self.diseases

    def setLevel(self, level: int) -> None:
        self.level = (short)(level - 1)

    def sendNote(self, to: str, msg: str) -> None:
        self.sendNote(to, msg, 0)

    def sendNote_to_msg_fame(self, to: str, msg: str, fame: int) -> None:
        MapleCharacterUtil.sendNote(to, self.getName(), msg, fame)

    def showNote(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM notes WHERE `to`=?", 1005, 1008)
            ps.setString(1, self.getName())
            rs = ps.executeQuery()
            rs.last()
            count = rs.getRow()
            rs.first()
            self.client.getSession().write(MTSCSPacket.showNotes(rs, count))
            rs.close()
            ps.close()
        except Exception as e:
            print("Unable to show note" + e)

    def deleteNote(self, id: int, fame: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT gift FROM notes WHERE `id`=?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if rs.next() and rs.getInt("gift") == fame and fame > 0:
                self.addFame(fame)
                self.updateSingleStat(MapleStat.FAME, self.getFame())
                self.client.getSession().write(MaplePacketCreator.getShowFameGain(fame))
            rs.close()
            ps.close()
            ps = con.prepareStatement("DELETE FROM notes WHERE `id`=?")
            ps.setInt(1, id)
            ps.execute()
            ps.close()
        except Exception as e:
            print("Unable to delete note" + e)

    def mulung_EnergyModify(self, inc: bool) -> None:
        if inc:
            if self.mulung_energy + 100 > 10000:
                self.mulung_energy = 10000
            else:
                self.mulung_energy += 100
        else:
            self.mulung_energy = 0

    def writeMulungEnergy(self) -> None:
        pass

    def writeEnergy(self, type: str, inc: str) -> None:
        pass

    def writeStatus(self, type: str, inc: str) -> None:
        pass

    def writePoint(self, type: str, inc: str) -> None:
        pass

    def getCombo(self) -> int:
        return self.aranCombo

    def setCombo(self, combo: int) -> None:
        self.aranCombo = combo

    def getLastCombo(self) -> int:
        return self.lastComboTime

    def setLastComboTime(self, time: int) -> None:
        self.lastComboTime = time

    def getKeyDownSkill_Time(self) -> int:
        return self.keydown_skill

    def setKeyDownSkill_Time(self, keydown_skill: int) -> None:
        self.keydown_skill = keydown_skill

    def checkBerserk(self) -> None:
        def _task_1():
            MapleCharacter.self.checkBerserk()

        if self.BerserkSchedule is not None:
            self.BerserkSchedule.cancel(False)
            self.BerserkSchedule = None
        BerserkX = SkillFactory.getSkill(1320006)
        skilllevel = self.getSkillLevel(BerserkX)
        if skilllevel >= 1:
            ampStat = BerserkX.getEffect(skilllevel)
            self.stats.Berserk = (self.stats.getHp() * 100 / self.stats.getMaxHp() <= ampStat.getX())
            self.client.getSession().write(MaplePacketCreator.showOwnBuffEffect(1320006, 1, (byte)(self.stats.Berserk ? 1 : 0)))
            self.map.broadcastMessage(this, MaplePacketCreator.showBuffeffect(self.getId(), 1320006, 1, (byte)(self.stats.Berserk ? 1 : 0)), False)
            self.BerserkSchedule = Timer.BuffTimer.getInstance().schedule(_task_1, 10000)

    def prepareBeholderEffect(self) -> None:
        def _task_1():
            remhppercentage = math.ceil(MapleCharacter.self.getStat().getHp() * 100.0 / MapleCharacter.self.getStat().getMaxHp())
            if berserkLvl == 0 or remhppercentage >= berserkLvl + 10:
                MapleCharacter.self.addHP(healEffect.getHp())
            MapleCharacter.self.client.getSession().write(MaplePacketCreator.showOwnBuffEffect(1321007, 2))
            MapleCharacter.self.map.broadcastMessage(MaplePacketCreator.summonSkill(MapleCharacter.self.getId(), 1321007, 5))
            MapleCharacter.self.map.broadcastMessage(MapleCharacter.this, MaplePacketCreator.showBuffeffect(MapleCharacter.self.getId(), 1321007, 2), False)

        def _task_2():
            buffEffect.applyTo(MapleCharacter.this)
            MapleCharacter.self.client.getSession().write(MaplePacketCreator.showOwnBuffEffect(1321007, 2))
            MapleCharacter.self.map.broadcastMessage(MaplePacketCreator.summonSkill(MapleCharacter.self.getId(), 1321007, Randomizer.nextInt(3) + 6))
            MapleCharacter.self.map.broadcastMessage(MapleCharacter.this, MaplePacketCreator.showBuffeffect(MapleCharacter.self.getId(), 1321007, 2), False)

        if self.beholderHealingSchedule is not None:
            self.beholderHealingSchedule.cancel(False)
        if self.beholderBuffSchedule is not None:
            self.beholderBuffSchedule.cancel(False)
        bHealing = SkillFactory.getSkill(1320008)
        bHealingLvl = self.getSkillLevel(bHealing)
        berserkLvl = self.getSkillLevel(SkillFactory.getSkill(1320006))
        if bHealingLvl > 0:
            healEffect = bHealing.getEffect(bHealingLvl)
            healInterval = healEffect.getX() * 1000
            self.beholderHealingSchedule = Timer.BuffTimer.getInstance().register(_task_1, healInterval, healInterval)
        bBuff = SkillFactory.getSkill(1320009)
        bBuffLvl = self.getSkillLevel(bBuff)
        if bBuffLvl > 0:
            buffEffect = bBuff.getEffect(bBuffLvl)
            buffInterval = buffEffect.getX() * 1000
            self.beholderBuffSchedule = Timer.BuffTimer.getInstance().register(_task_2, buffInterval, buffInterval)

    def setChalkboard(self, text: str) -> None:
        self.chalktext = text
        self.map.broadcastMessage(MTSCSPacket.useChalkboard(self.getId(), text))

    def getChalkboard(self) -> str:
        return self.chalktext

    def getMount(self) -> Any:
        return self.mount

    def getWishlist(self) -> list:
        return self.wishlist

    def clearWishlist(self) -> None:
        for i in range(10):
            self.wishlist[i] = 0

    def getWishlistSize(self) -> int:
        ret = 0
        for i in range(10):
            if self.wishlist[i] > 0:
                ret += 1
        return ret

    def setWishlist(self, wl: list) -> None:
        self.wishlist = wl

    def getRocks(self) -> list:
        return self.rocks

    def getRockSize(self) -> int:
        ret = 0
        for i in range(10):
            if self.rocks[i] != 999999999:
                ret += 1
        return ret

    def deleteFromRocks(self, map: int) -> None:
        for i in range(10):
            if self.rocks[i] == map:
                self.rocks[i] = 999999999
                break

    def addRockMap(self) -> None:
        if self.getRockSize() >= 10:
            return
        for i in range(10):
            if self.rocks[i] == 999999999:
                self.rocks[i] = self.getMapId()
                return
        self.rocks[self.getRockSize()] = self.getMapId()

    def isRockMap(self, id: int) -> bool:
        for i in range(10):
            if self.rocks[i] == id:
                return True
        return False

    def getRegRocks(self) -> list:
        return self.regrocks

    def getRegRockSize(self) -> int:
        ret = 0
        for i in range(5):
            if self.regrocks[i] != 999999999:
                ret += 1
        return ret

    def deleteFromRegRocks(self, map: int) -> None:
        for i in range(5):
            if self.regrocks[i] == map:
                self.regrocks[i] = 999999999
                break

    def addRegRockMap(self) -> None:
        if self.getRegRockSize() >= 5:
            return
        for i in range(5):
            if self.regrocks[i] == 999999999:
                self.regrocks[i] = self.getMapId()
                return
        self.regrocks[self.getRegRockSize()] = self.getMapId()

    def isRegRockMap(self, id: int) -> bool:
        for i in range(5):
            if self.regrocks[i] == id:
                return True
        return False

    def getLastRes(self) -> list:
        return self.lastres

    def setLastRes(self, lastres: list) -> None:
        self.lastres = lastres

    def setMonsterBookCover(self, bookCover: int) -> None:
        self.bookCover = bookCover

    def getMonsterBookCover(self) -> int:
        return self.bookCover

    def getOneTimeLog(self, bossid: str) -> int:
        con1 = DatabaseConnection.getConnection()
        try:
            ret_count = 0
            ps = con1.prepareStatement("select count(*) from onetimelog where characterid = ? and log = ?")
            ps.setInt(1, self.id)
            ps.setString(2, bossid)
            rs = ps.executeQuery()
            if rs.next():
                ret_count = rs.getInt(1)
            else:
                ret_count = -1
            rs.close()
            ps.close()
            return ret_count
        except Exception as Ex:
            return -1

    def setOneTimeLog(self, bossid: str) -> None:
        con1 = DatabaseConnection.getConnection()
        try:
            ps = con1.prepareStatement("insert into onetimelog (characterid, log) values (?,?)")
            ps.setInt(1, self.id)
            ps.setString(2, bossid)
            ps.executeUpdate()
            ps.close()
        except SQLException as ex:
            pass

    def getBossLog(self, boss: str) -> int:
        return self.getBossLog(boss, 0)

    def getBossLog_boss_type(self, boss: str, type: int) -> int:
        try:
            count = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM bosslog WHERE characterid = ? AND bossid = ?")
            ps.setInt(1, self.id)
            ps.setString(2, boss)
            rs = ps.executeQuery()
            if rs.next():
                count = rs.getInt("count")
                bossTime = rs.getTimestamp("time")
                rs.close()
                ps.close()
                if type == 0:
                    if bossTime is not None:
                        cal = Calendar.getInstance()
                        cal.setTimeInMillis(bossTime.getTime())
                        if cal.get(6) + 1 <= Calendar.getInstance().get(6) or cal.get(1) + 1 <= Calendar.getInstance().get(1):
                            count = 0
                            ps = con.prepareStatement("UPDATE bosslog SET count = 0 WHERE characterid = ? AND bossid = ?")
                            ps.setInt(1, self.id)
                            ps.setString(2, boss)
                            ps.executeUpdate()
                    rs.close()
                    ps.close()
                    ps = con.prepareStatement("UPDATE bosslog SET time = CURRENT_TIMESTAMP() WHERE characterid = ? AND bossid = ?")
                    ps.setInt(1, self.id)
                    ps.setString(2, boss)
                    ps.executeUpdate()
            else:
                psu = con.prepareStatement("INSERT INTO bosslog (characterid, bossid, count, type) VALUES (?, ?, ?, ?)")
                psu.setInt(1, self.id)
                psu.setString(2, boss)
                psu.setInt(3, 0)
                psu.setInt(4, type)
                psu.executeUpdate()
                psu.close()
            rs.close()
            ps.close()
            return count
        except Exception as Ex:
            print("Error while read bosslog." + Ex)
            return -1

    def getBossLogType(self, boss: str) -> int:
        try:
            type = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM bosslog WHERE characterid = ? AND bossid = ?")
            ps.setInt(1, self.id)
            ps.setString(2, boss)
            rs = ps.executeQuery()
            if rs.next():
                type = rs.getInt("type")
            rs.close()
            ps.close()
            return type
        except Exception as Ex:
            print("Error while read bosslog." + Ex)
            return -1

    def getBossLogChannel(self, boss: str) -> int:
        try:
            channel = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM bosslog WHERE characterid = ? AND bossid = ?")
            ps.setInt(1, self.id)
            ps.setString(2, boss)
            rs = ps.executeQuery()
            if rs.next():
                channel = rs.getInt("channel")
            rs.close()
            ps.close()
            return channel
        except Exception as Ex:
            print("Error while read bosslog." + Ex)
            return 0

    def setBossLog(self, boss: str) -> None:
        self.setBossLog(boss, 0)

    def setBossLog_boss_type(self, boss: str, type: int) -> None:
        self.setBossLog(boss, type, 1)

    def setBossLog_boss_type_count(self, boss: str, type: int, count: int) -> None:
        bossCount = self.getBossLog(boss, type)
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE bosslog SET count = ?, type = ?, time = CURRENT_TIMESTAMP(), channel = ? WHERE characterid = ? AND bossid = ?")
            ps.setInt(1, bossCount + count)
            ps.setInt(2, type)
            ps.setInt(3, self.client.getChannel())
            ps.setInt(4, self.id)
            ps.setString(5, boss)
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("Error while set bosslog." + Ex)

    def resetBossLog(self, boss: str) -> None:
        self.resetBossLog(boss, 0)

    def resetBossLog_boss_type(self, boss: str, type: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE bosslog SET count = ?, type = ?, time = CURRENT_TIMESTAMP(), channel = ? WHERE characterid = ? AND bossid = ?")
            ps.setInt(1, 0)
            ps.setInt(2, type)
            ps.setInt(3, 0)
            ps.setInt(4, self.id)
            ps.setString(5, boss)
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("Error while reset bosslog." + Ex)

    def setPrizeLog(self, bossid: str) -> None:
        con1 = DatabaseConnection.getConnection()
        try:
            ps = con1.prepareStatement("insert into Prizelog (accid, bossid) values (?,?)")
            ps.setInt(1, self.getClient().getAccID())
            ps.setString(2, bossid)
            ps.executeUpdate()
            ps.close()
        except SQLException as ex:
            pass

    def getPrizeLog(self, bossid: str) -> int:
        con1 = DatabaseConnection.getConnection()
        try:
            ret_count = 0
            ps = con1.prepareStatement("select count(*) from Prizelog where accid = ? and bossid = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setString(2, bossid)
            rs = ps.executeQuery()
            if rs.next():
                ret_count = rs.getInt(1)
            else:
                ret_count = -1
            rs.close()
            ps.close()
            return ret_count
        except Exception as Wx:
            return -1

    def dropMessage_type_message(self, type: int, message: str) -> None:
        if type == -2:
            self.client.getSession().write( PlayerShopPacket.shopChat(message, 0))
        else:
            self.client.getSession().write(MaplePacketCreator.serverNotice(type, message))

    def getPlayerShop(self) -> Any:
        return self.playerShop

    def setPlayerShop(self, playerShop: Any) -> None:
        self.playerShop = playerShop

    def getConversation(self) -> int:
        return self.inst.get()

    def setConversation(self, inst: int) -> None:
        self.inst.set(inst)

    def getCarnivalParty(self) -> Any:
        return self.carnivalParty

    def setCarnivalParty(self, party: Any) -> None:
        self.carnivalParty = party

    def addCP(self, ammount: int) -> None:
        self.totalCP += ammount
        self.availableCP += ammount

    def useCP(self, ammount: int) -> None:
        self.availableCP -= ammount

    def getAvailableCP(self) -> int:
        return self.availableCP

    def getTotalCP(self) -> int:
        return self.totalCP

    def resetCP(self) -> None:
        self.totalCP = 0
        self.availableCP = 0

    def addCarnivalRequest(self, request: Any) -> None:
        self.pendingCarnivalRequests.add(request)

    def getNextCarnivalRequest(self) -> Any:
        return self.pendingCarnivalRequests.pollLast()

    def clearCarnivalRequests(self) -> None:
        self.pendingCarnivalRequests = []

    def startMonsterCarnival(self, enemyavailable: int, enemytotal: int) -> None:
        self.client.getSession().write( MonsterCarnivalPacket.startMonsterCarnival(this, enemyavailable, enemytotal))

    def CPUpdate(self, party: bool, available: int, total: int, team: int) -> None:
        self.client.getSession().write(MonsterCarnivalPacket.CPUpdate(party, available, total, team))

    def playerDiedCPQ(self, name: str, lostCP: int, team: int) -> None:
        self.client.getSession().write(MonsterCarnivalPacket.playerDiedMessage(name, lostCP, team))

    def getCanTalk(self) -> bool:
        return self.canTalk

    def canTalk(self, talk: bool) -> None:
        self.canTalk = talk

    def getMaxHp(self) -> int:
        return self.stats.maxhp

    def setMaxHp(self, maxhp: int) -> None:
        self.stats.setMaxHp(maxhp)

    def getMaxMp(self) -> int:
        return self.stats.maxmp

    def setMaxMp(self, maxmp: int) -> None:
        self.stats.setMaxMp(maxmp)

    def getHp(self) -> int:
        return self.stats.hp

    def setHp(self, hp: int) -> None:
        self.stats.setHp(hp)

    def getMp(self) -> int:
        return self.stats.mp

    def setMp(self, mp: int) -> None:
        self.stats.setMp(mp)

    def getStr(self) -> int:
        return self.stats.str

    def getDex(self) -> int:
        return self.stats.dex

    def getLuk(self) -> int:
        return self.stats.luk

    def getInt(self) -> int:
        return self.stats.int_

    def getEXPMod(self) -> int:
        return self.stats.expMod

    def getDropMod(self) -> int:
        return self.stats.dropMod

    def getCashMod(self) -> int:
        return self.stats.cashMod

    def setPoints(self, p: int) -> None:
        self.points = p

    def getPoints(self) -> int:
        return self.points

    def setVPoints(self, p: int) -> None:
        self.vpoints = p

    def getVPoints(self) -> int:
        return self.vpoints

    def getCashInventory(self) -> Any:
        return self.cs

    def removeAll(self, id: int) -> None:
        self.removeAll(id, True, False)

    def removeAll_id_show_checkEquipped(self, id: int, show: bool, checkEquipped: bool) -> None:
        type = GameConstants.getInventoryType(id)
        possessed = self.getInventory(type).countById(id)
        if possessed > 0:
            MapleInventoryManipulator.removeById(self.getClient(), type, id, possessed, True, False)
            if show:
                self.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, (short)(-possessed), True))
        if checkEquipped and type == MapleInventoryType.EQUIP:
            type = MapleInventoryType.EQUIPPED
            possessed = self.getInventory(type).countById(id)
            if possessed > 0:
                MapleInventoryManipulator.removeById(self.getClient(), type, id, possessed, True, False)
                if show:
                    self.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, (short)(-possessed), True))
                self.equipChanged()

    def getRings(self, equip: bool) -> Any:
        iv = self.getInventory(MapleInventoryType.EQUIPPED)
        equippedC = iv.list()
        equipped = [])
        for item in equippedC:
            equipped.add(item)
        Collections.sort(equipped)
        crings = []
        frings = []
        for item2 in equipped:
            if item2.getRing() is not None:
                ring = item2.getRing()
                ring.setEquipped(True)
                if not GameConstants.isFriendshipRing(item2.getItemId()) and not GameConstants.isCrushRing(item2.getItemId()):
                    continue
                if equip:
                    if GameConstants.isCrushRing(item2.getItemId()):
                        crings.add(ring)
                    else:
                        if not GameConstants.isFriendshipRing(item2.getItemId()):
                            continue
                        frings.add(ring)
                elif crings == 0 and GameConstants.isCrushRing(item2.getItemId()):
                    crings.add(ring)
                else:
                    if not frings == 0 or not GameConstants.isFriendshipRing(item2.getItemId()):
                        continue
                    frings.add(ring)
        if equip:
            iv = self.getInventory(MapleInventoryType.EQUIP)
            for item3 in iv.list():
                if item3.getRing() is not None and GameConstants.isEffectRing(item3.getItemId()):
                    ring = item3.getRing()
                    ring.setEquipped(False)
                    if GameConstants.isFriendshipRing(item3.getItemId()):
                        frings.add(ring)
                    else:
                        if not GameConstants.isCrushRing(item3.getItemId()):
                            continue
                        crings.add(ring)
        Collections.sort(frings, new MapleRing.RingComparator())
        Collections.sort(crings, new MapleRing.RingComparator())
        return new Pair<List<MapleRing>, List<MapleRing>>(crings, frings)

    def getFH(self) -> int:
        fh = self.getMap().getFootholds().findBelow(self.getPosition())
        if fh is not None:
            return fh.getId()
        return 0

    def startFairySchedule(self, exp: bool) -> None:
        self.startFairySchedule(exp, False)

    def startFairySchedule_exp_equipped(self, exp: bool, equipped: bool) -> None:
        def _task_1():
            if MapleCharacter.self.fairyExp < 30 and MapleCharacter.self.stats.equippedFairy:
                gamepoints = MapleCharacter.self.getGamePoints()
                if gamepoints > 0 and gamepoints < 60:
                    MapleCharacter.self.fairyExp = 10
                elif gamepoints >= 60 and gamepoints < 120:
                    MapleCharacter.self.fairyExp = 20
                elif gamepoints >= 120:
                    MapleCharacter.self.fairyExp = 30
                MapleCharacter.self.dropMessage(5, "精灵吊坠经验获取量增加到 " + MapleCharacter.self.fairyExp + "%.")
                MapleCharacter.self.startFairySchedule(False, True)
            else:
                MapleCharacter.self.cancelFairySchedule(not MapleCharacter.self.stats.equippedFairy)

        gamepoints = self.getGamePoints()
        if gamepoints > 0 and gamepoints < 60:
            self.fairyExp = 10
        elif gamepoints >= 60 and gamepoints < 120:
            self.fairyExp = 20
        elif gamepoints >= 120:
            self.fairyExp = 30
        self.cancelFairySchedule(exp)
        if self.fairyExp < 30 and self.stats.equippedFairy:
            if equipped:
                self.dropMessage(5, "您装备了精灵吊坠在1小时后经验获取将增加到 " + (self.fairyExp + 10) + "%.请保持在线哟~！！")
            self.fairySchedule = Timer.EtcTimer.getInstance().schedule(_task_1, 1800000)
        else:
            self.cancelFairySchedule(not self.stats.equippedFairy)

    def cancelFairySchedule(self, exp: bool) -> None:
        if self.fairySchedule is not None:
            self.fairySchedule.cancel(False)
            self.fairySchedule = None
        if exp:
            self.fairyExp = 10

    def getFairyExp(self) -> int:
        return self.fairyExp

    def getCoconutTeam(self) -> int:
        return self.coconutteam

    def setCoconutTeam(self, team: int) -> None:
        self.coconutteam = team

    def spawnPet(self, slot: int) -> None:
        self.spawnPet(slot, False, True)

    def spawnPet_slot_lead(self, slot: int, lead: bool) -> None:
        self.spawnPet(slot, lead, True)

    def spawnPet_slot_lead_broadcast(self, slot: int, lead: bool, broadcast: bool) -> None:
        item = self.getInventory(MapleInventoryType.CASH).getItem(slot)
        ii = MapleItemInformationProvider.getInstance()
        if item is None or not GameConstants.isPet(item.getItemId()):
            self.client.getSession().write(MaplePacketCreator.enableActions())
            return
        # switch (item.getItemId()):
            # case 5000028:
            # case 5000047:
                pet = MaplePet.createPet(item.getItemId() + 1, MapleInventoryIdentifier.getInstance())
                if pet is not None:
                    MapleInventoryManipulator.addById(self.client, item.getItemId() + 1, 1, item.getOwner(), pet, 45, 0)
                    MapleInventoryManipulator.removeFromSlot(self.client, MapleInventoryType.CASH, slot, 1, False)
                    break
                break
            # default:
                pet = item.getPet()
                if pet is None or (item.getItemId() == 5000054 and pet.getSecondsLeft() <= 0) or (item.getExpiration() != -1 and item.getExpiration() <= int(time.time() * 1000)):
                    break
                if pet.getSummoned():
                    self.unequipPet(pet, False)
                    break
                leadid = 8
                if GameConstants.isKOC(self.getJob()):
                    leadid = 10000018
                elif GameConstants.isAran(self.getJob()):
                    leadid = 20000024
                if self.getSkillLevel(SkillFactory.getSkill(leadid)) == 0 and self.getPet(0) is not None:
                    self.unequipPet(self.getPet(0), False)
                elif lead:
                    self.shiftPetsRight()
                position = None
                pos = position = self.getPosition()
                position.y -= 12
                pet.setPos(pos)
                try:
                    pet.setFh(self.getMap().getFootholds().findBelow(pos).getId())
                except TypeError as e:
                    pet.setFh(0)
                pet.setStance(0)
                pet.setSummoned(self.getPetSlotNext() + 1)
                self.addPet(pet)
                if broadcast:
                    self.getMap().broadcastMessage(this, PetPacket.showPet(this, pet, False, False), True)
                    self.client.sendPacket(PetPacket.petStatUpdate(this))
                break
        self.client.sendPacket(PetPacket.emptyStatUpdate())

    def addMoveMob(self, mobid: int) -> None:
        if (mobid in self.movedMobs):
            self.movedMobs.put(mobid, self.movedMobs.get(mobid) + 1)
            if self.movedMobs.get(mobid) > 30:
                for chr in self.getMap().getCharactersThreadsafe():
                    if chr.getMoveMobs().__contains__(mobid):
                        chr.getClient().getSession().write(MobPacket.killMonster(mobid, 1))
                        chr.getMoveMobs().remove(mobid)
        else:
            self.movedMobs.put(mobid, 1)

    def getMoveMobs(self) -> dict:
        return self.movedMobs

    def getLinkMid(self) -> int:
        return self.linkMid

    def setLinkMid(self, lm: int) -> None:
        self.linkMid = lm

    def isClone(self) -> bool:
        return self.clone

    def setClone(self, c: bool) -> None:
        self.clone = c

    def getClones(self) -> list:
        return self.clones

    def cloneLooks(self) -> Any:
        cs = MapleClient(None, None, MockIOSession())
        minus = self.getId() + Randomizer.nextInt(self.getId())
        ret = MapleCharacter(True)
        ret.id = minus
        ret.client = cs
        ret.exp = 0
        ret.meso = 0
        ret.beans = self.beans
        ret.blood = self.blood
        ret.month = self.month
        ret.day = self.day
        ret.charmessage = self.charmessage
        ret.expression = self.expression
        ret.constellation = self.constellation
        ret.remainingAp = 0
        ret.fame = 0
        ret.accountid = self.client.getAccID()
        ret.name = self.name
        ret.level = self.level
        ret.fame = self.fame
        ret.job = self.job
        ret.hair = self.hair
        ret.face = self.face
        ret.skinColor = self.skinColor
        ret.bookCover = self.bookCover
        ret.monsterbook = self.monsterbook
        ret.mount = self.mount
        ret.CRand = PlayerRandomStream()
        ret.gmLevel = self.gmLevel
        ret.gender = self.gender
        ret.mapid = self.map.getId()
        ret.map = self.map
        ret.setStance(self.getStance())
        ret.chair = self.chair
        ret.itemEffect = self.itemEffect
        ret.guildid = self.guildid
        ret.currentrep = self.currentrep
        ret.totalrep = self.totalrep
        ret.stats = self.stats
        ret.effects.putAll(self.effects)
        if ret.effects.get(MapleBuffStat.ILLUSION) is not None:
            ret.effects.remove(MapleBuffStat.ILLUSION)
        if ret.effects.get(MapleBuffStat.召唤兽) is not None:
            ret.effects.remove(MapleBuffStat.召唤兽)
        if ret.effects.get(MapleBuffStat.REAPER) is not None:
            ret.effects.remove(MapleBuffStat.REAPER)
        if ret.effects.get(MapleBuffStat.替身术) is not None:
            ret.effects.remove(MapleBuffStat.替身术)
        ret.guildrank = self.guildrank
        ret.allianceRank = self.allianceRank
        ret.hidden = self.hidden
        ret.setPosition(Point(self.getPosition()))
        for equip in self.getInventory(MapleInventoryType.EQUIPPED):
            ret.getInventory(MapleInventoryType.EQUIPPED).addFromDB(equip)
        ret.skillMacros = self.skillMacros
        ret.keylayout = self.keylayout
        ret.questinfo = self.questinfo
        ret.savedLocations = self.savedLocations
        ret.wishlist = self.wishlist
        ret.rocks = self.rocks
        ret.regrocks = self.regrocks
        ret.buddylist = self.buddylist
        ret.keydown_skill = 0
        ret.lastmonthfameids = self.lastmonthfameids
        ret.lastfametime = self.lastfametime
        ret.storage = self.storage
        ret.cs = self.cs
        ret.client.setAccountName(self.client.getAccountName())
        ret.acash = self.acash
        ret.lastGainHM = self.lastGainHM
        ret.maplepoints = self.maplepoints
        ret.clone = True
        ret.client.setChannel(self.client.getChannel())
        print("cloneLooks输出：" + self.client.getChannel())
        while self.map.getCharacterById(ret.id) is not None or self.client.getChannelServer().getPlayerStorage().getCharacterById(ret.id) is not None:
            mapleCharacter = ret
            mapleCharacter.id += 1
        ret.client.setPlayer(ret)
        return ret

    def cloneLook(self) -> None:
        if self.clone:
            return
        for i in range(self.len(clones)):
            if self.clones[i].get() is None:
                newp = self.cloneLooks()
                self.map.addPlayer(newp)
                self.map.broadcastMessage(MaplePacketCreator.updateCharLook(newp))
                self.map.movePlayer(newp, self.getPosition())
                self.clones[i] = new WeakReference<MapleCharacter>(newp)
                return

    def disposeClones(self) -> None:
        self.numClones = 0
        for i in range(self.len(clones)):
            if self.clones[i].get() is not None:
                self.map.removePlayer(self.clones[i].get())
                self.clones[i].get().getClient().disconnect(False, False)
                self.clones[i] = new WeakReference<MapleCharacter>(None)
                self.numClones += 1

    def getCloneSize(self) -> int:
        z = 0
        for i in range(self.len(clones)):
            if self.clones[i].get() is not None:
                z += 1
        return z

    def spawnClones(self) -> None:
        if self.numClones == 0 and self.stats.hasClone:
            self.cloneLook()
        for i in range(self.numClones):
            self.cloneLook()
        self.numClones = 0

    def getNumClones(self) -> int:
        return self.numClones

    def spawnSavedPets(self) -> None:
        for i in range(self.len(petStore)):
            if self.petStore[i] > -1:
                self.spawnPet(self.petStore[i], False, False)
        self.client.getSession().write(PetPacket.petStatUpdate(this))
        self.petStore = new byte[] { -1, -1, -1 }

    def getPetStores(self) -> bytes:
        return self.petStore

    def resetStats(self, str: int, dex: int, int_: int, luk: int) -> None:
        stat = new ArrayList<Pair<MapleStat, Integer>>(2)
        total = self.stats.getStr() + self.stats.getDex() + self.stats.getLuk() + self.stats.getInt() + self.getRemainingAp()
        total -= str
        self.stats.setStr(str)
        total -= dex
        self.stats.setDex(dex)
        total -= int_
        self.stats.setInt(int_)
        total -= luk
        self.stats.setLuk(luk)
        self.setRemainingAp(total)
        if self.getRemainingAp() < 0:
            self.remainingAp = 0
        stat.add(new Pair<MapleStat, Integer>(MapleStat.STR, str))
        stat.add(new Pair<MapleStat, Integer>(MapleStat.DEX, dex))
        stat.add(new Pair<MapleStat, Integer>(MapleStat.INT, int_))
        stat.add(new Pair<MapleStat, Integer>(MapleStat.LUK, luk))
        stat.add(new Pair<MapleStat, Integer>(MapleStat.AVAILABLEAP, total))
        self.client.getSession().write(MaplePacketCreator.updatePlayerStats(stat, False, self.getJob()))

    def getPyramidSubway(self) -> Any:
        return self.pyramidSubway

    def setPyramidSubway(self, ps: Any) -> None:
        self.pyramidSubway = ps

    def getSubcategory(self) -> int:
        if self.job >= 430 and self.job <= 434:
            return 1
        return self.subcategory

    def itemQuantity(self, itemid: int) -> int:
        return self.getInventory(GameConstants.getInventoryType(itemid)).countById(itemid)

    def setRPS(self, rps: Any) -> None:
        self.rps = rps

    def getRPS(self) -> Any:
        return self.rps

    def getNextConsume(self) -> int:
        return self.nextConsume

    def setNextConsume(self, nc: int) -> None:
        self.nextConsume = nc

    def getRank(self) -> int:
        return self.rank

    def getRankMove(self) -> int:
        return self.rankMove

    def getJobRank(self) -> int:
        return self.jobRank

    def getJobRankMove(self) -> int:
        return self.jobRankMove

    def changeChannel(self, channel: int) -> None:
        energyLevel = self.getBuffedValue(MapleBuffStat.能量获得)
        if energyLevel is not None and energyLevel > 0:
            self.setBuffedValue(MapleBuffStat.能量获得, energyLevel)
            stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, energyLevel))
            self.client.getSession().write(MaplePacketCreator.能量条(stat, 0))
        socket = self.client.getChannelServer().getIP().split(":")
        toch = ChannelServer.getInstance(channel)
        if channel == self.client.getChannel() or toch is None or toch.isShutdown():
            return
        self.changeRemoval()
        ch = ChannelServer.getInstance(self.client.getChannel())
        if self.getMessenger() is not None:
            World.Messenger.silentLeaveMessenger(self.getMessenger().getId(), MapleMessengerCharacter(this))
        PlayerBuffStorage.addBuffsToStorage(self.getId(), self.getAllBuffs())
        PlayerBuffStorage.addCooldownsToStorage(self.getId(), self.getCooldowns())
        PlayerBuffStorage.addDiseaseToStorage(self.getId(), self.getAllDiseases())
        World.ChannelChange_Data(CharacterTransfer(this), self.getId(), channel)
        ch.removePlayer(this)
        self.client.updateLoginState(MapleClient.CHANGE_CHANNEL, self.client.getSessionIPAddress())
        s = self.client.getSessionIPAddress()
        LoginServer.addIPAuth(s[s.find(47:] + 1, s))
        try:
            self.client.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(toch.getIP().split(":")[1])))
        except UnknownHostException as ex:
            Logger.getLogger(MapleCharacter.class.getName()).log(Level.SEVERE, None, ex)
        self.saveToDB(False, False)
        self.getMap().removePlayer(this)
        self.client.setPlayer(None)
        self.client.setReceiving(False)
        self.expirationTask(True, False)

    def expandInventory(self, type: int, amount: int) -> None:
        inv = self.getInventory(MapleInventoryType.getByType(type))
        if inv.getSlotLimit() < 96:
            inv.addSlot(amount)
            self.client.getSession().write(MaplePacketCreator.getSlotUpdate(type, inv.getSlotLimit()))

    def allowedToTarget(self, other: Any) -> bool:
        return other is not None and (not other.isHidden() or self.getGMLevel() >= other.getGMLevel())

    def getFollowId(self) -> int:
        return self.followid

    def setFollowId(self, fi: int) -> None:
        self.followid = fi
        if fi == 0:
            self.followinitiator = False
            self.followon = False

    def setFollowInitiator(self, fi: bool) -> None:
        self.followinitiator = fi

    def setFollowOn(self, fi: bool) -> None:
        self.followon = fi

    def isFollowOn(self) -> bool:
        return self.followon

    def isFollowInitiator(self) -> bool:
        return self.followinitiator

    def checkFollow(self) -> None:
        if self.followon:
            tt = self.map.getCharacterById(self.followid)
            if tt is not None:
                tt.setFollowId(0)
            self.setFollowId(0)

    def getMarriageId(self) -> int:
        return self.marriageId

    def setMarriageId(self, mi: int) -> None:
        self.marriageId = mi

    def getMarriageItemId(self) -> int:
        return self.marriageItemId

    def setMarriageItemId(self, mi: int) -> None:
        self.marriageItemId = mi

    def isStaff(self) -> bool:
        return self.gmLevel > ServerConstants.PlayerGMRank.NORMAL.getLevel()

    def startPartyQuest(self, questid: int) -> bool:
        ret = False
        if not (MapleQuest.getInstance(questid in self.quests)) or not (questid in self.questinfo):
            status = self.getQuestNAdd(MapleQuest.getInstance(questid))
            status.setStatus(1)
            self.updateQuest(status)
            # switch (questid):
                # case 1300:
                # case 1301:
                # case 1302:
                    self.updateInfoQuest(questid, "min=0;sec=0;date=0000-00-00;have=0;rank=F;try=0;cmp=0;CR=0;VR=0;gvup=0;vic=0;lose=0;draw=0")
                    break
                # case 1204:
                    self.updateInfoQuest(questid, "min=0;sec=0;date=0000-00-00;have0=0;have1=0;have2=0;have3=0;rank=F;try=0;cmp=0;CR=0;VR=0")
                    break
                # case 1206:
                    self.updateInfoQuest(questid, "min=0;sec=0;date=0000-00-00;have0=0;have1=0;rank=F;try=0;cmp=0;CR=0;VR=0")
                    break
                # default:
                    self.updateInfoQuest(questid, "min=0;sec=0;date=0000-00-00;have=0;rank=F;try=0;cmp=0;CR=0;VR=0")
                    break
            ret = True
        return ret

    def getOneInfo(self, questid: int, key: str) -> str:
        if not (questid in self.questinfo) or key is None:
            return None
        split3 = None
        split = split3 = self.questinfo.get(questid).split(";")
        for x in split3:
            split2 = x.split("=")
            if len(split2) == 2 and split2[0] == (key):
                return split2[1]
        return None

    def updateOneInfo(self, questid: int, key: str, value: str) -> None:
        if not (questid in self.questinfo) or key is None or value is None:
            return
        split = self.questinfo.get(questid).split(";")
        changed = False
        newQuest = ""
        for x in split:
            split2 = x.split("=")
            if len(split2) == 2:
                if split2[0] == (key):
                    newQuest.append(key).append("=").append(value)
                else:
                    newQuest.append(x)
                newQuest.append(";")
                changed = True
        self.updateInfoQuest(questid, changed ? newQuest[0:newQuest.__len__(] - 1) : newQuest)

    def recalcPartyQuestRank(self, questid: int) -> None:
        if not self.startPartyQuest(questid):
            oldRank = self.getOneInfo(questid, "rank")
            if oldRank is None or oldRank == ("S"):
                return
            split = self.questinfo.get(questid).split(";")
            newRank = None
            s = oldRank
            # switch (s):
                # case "A":
                    newRank = "S"
                    break
                # case "B":
                    newRank = "A"
                    break
                # case "C":
                    newRank = "B"
                    break
                # case "D":
                    newRank = "C"
                    break
                # case "F":
                    newRank = "D"
                    break
                # default:
                    return
            questInfo = MapleQuest.getInstance(questid).getInfoByRank(newRank)
            for q in questInfo:
                found = False
                val = self.getOneInfo(questid, q.right.left)
                if val is None:
                    return
                vall = 0
                try:
                    vall = int(val)
                except ValueError as e:
                    return
                s2 = q.left
                # switch (s2):
                    # case "less":
                        found = (vall < q.right.right)
                        break
                    # case "more":
                        found = (vall > q.right.right)
                        break
                    # case "equal":
                        found = (vall == q.right.right)
                        break
                if not found:
                    return
            self.updateOneInfo(questid, "rank", newRank)

    def tryPartyQuest(self, questid: int) -> None:
        try:
            self.startPartyQuest(questid)
            self.pqStartTime = int(time.time() * 1000)
            self.updateOneInfo(questid, "try", str(int(self.getOneInfo(questid, "try")) + 1))
        except ValueError as e:
            e.printStackTrace()
            print("tryPartyQuest error")

    def endPartyQuest(self, questid: int) -> None:
        try:
            self.startPartyQuest(questid)
            if self.pqStartTime > 0:
                changeTime = int(time.time() * 1000) - self.pqStartTime
                mins = (int)(changeTime / 1000 / 60)
                secs = (int)(changeTime / 1000 % 60)
                mins2 = int(self.getOneInfo(questid, "min"))
                secs2 = int(self.getOneInfo(questid, "sec"))
                if mins2 <= 0 or mins < mins2:
                    self.updateOneInfo(questid, "min", str(mins))
                    self.updateOneInfo(questid, "sec", str(secs))
                    self.updateOneInfo(questid, "date", FileoutputUtil.CurrentReadable_Date())
                newCmp = int(self.getOneInfo(questid, "cmp")) + 1
                self.updateOneInfo(questid, "cmp", str(newCmp))
                self.updateOneInfo(questid, "CR", str(math.ceil(newCmp * 100.0 / int(self.getOneInfo(questid, "try")))))
                self.recalcPartyQuestRank(questid)
                self.pqStartTime = 0
        except ValueError as e:
            e.printStackTrace()
            print("endPartyQuest error")

    def havePartyQuest(self, itemId: int) -> None:
        questid = 0
        index = -1
        # switch (itemId):
            # case 1002798:
                questid = 1200
                break
            # case 1072369:
                questid = 1201
                break
            # case 1022073:
                questid = 1202
                break
            # case 1082232:
                questid = 1203
                break
            # case 1002571:
            # case 1002572:
            # case 1002573:
            # case 1002574:
                questid = 1204
                index = itemId - 1002571
                break
            # case 1122010:
                questid = 1205
                break
            # case 1032060:
            # case 1032061:
                questid = 1206
                index = itemId - 1032060
                break
            # case 3010018:
                questid = 1300
                break
            # case 1122007:
                questid = 1301
                break
            # case 1122058:
                questid = 1302
                break
            # default:
                return
        self.startPartyQuest(questid)
        self.updateOneInfo(questid, "have" + ((index == -1) ? "" : Integer.valueOf(index)), "1")

    def resetStatsByJob(self, beginnerJob: bool) -> None:
        baseJob = beginnerJob ? (self.job % 1000) : (self.job % 1000 / 100 * 100)
        # switch (baseJob):
            # case 100:
                self.resetStats(25, 4, 4, 4)
                break
            # case 200:
                self.resetStats(4, 4, 20, 4)
                break
            # case 300:
            # case 400:
                self.resetStats(4, 25, 4, 4)
                break
            # case 500:
                self.resetStats(4, 20, 4, 4)
                break

    def hasSummon(self) -> bool:
        return self.hasSummon

    def setHasSummon(self, summ: bool) -> None:
        self.hasSummon = summ

    def removeDoor(self) -> None:
        door = self.getDoors().iterator().next()
        for chr in door.getTarget().getCharactersThreadsafe():
            door.sendDestroyData(chr.getClient())
        for chr in door.getTown().getCharactersThreadsafe():
            door.sendDestroyData(chr.getClient())
        for destroyDoor in self.getDoors():
            door.getTarget().removeMapObject(destroyDoor)
            door.getTown().removeMapObject(destroyDoor)
        self.clearDoors()

    def changeRemoval(self) -> None:
        self.changeRemoval(False)

    def changeRemoval_dc(self, dc: bool) -> None:
        if self.getTrade() is not None:
            MapleTrade.cancelTrade(self.getTrade(), self.client)
        if self.getCheatTracker() is not None:
            self.getCheatTracker().dispose()
        if not dc:
            self.cancelEffectFromBuffStat(MapleBuffStat.骑兽技能)
            self.cancelEffectFromBuffStat(MapleBuffStat.召唤兽)
            self.cancelEffectFromBuffStat(MapleBuffStat.REAPER)
            self.cancelEffectFromBuffStat(MapleBuffStat.替身术)
        if self.getPyramidSubway() is not None:
            self.getPyramidSubway().dispose(this)
        if self.playerShop is not None and not dc:
            self.playerShop.removeVisitor(this)
            if self.playerShop.isOwner(this):
                self.playerShop.setOpen(True)
        if not self.getDoors() == 0:
            self.removeDoor()
        self.disposeClones()
        NPCScriptManager.getInstance().dispose(self.client)

    def updateTick(self, newTick: int) -> None:
        self.anticheat.updateTick(newTick)

    def canUseFamilyBuff(self, buff: Any) -> bool:
        stat = self.getQuestNAdd(MapleQuest.getInstance(buff.questID))
        if stat.getCustomData() is None:
            stat.setCustomData("0")
        return int(stat.getCustomData()) + 86400000 < int(time.time() * 1000)

    def useFamilyBuff(self, buff: Any) -> None:
        stat = self.getQuestNAdd(MapleQuest.getInstance(buff.questID))
        stat.setCustomData(str(int(time.time() * 1000)))

    def usedBuffs(self) -> list:
        used = new ArrayList<Pair<Integer, Integer>>()
        for (final MapleFamilyBuff.MapleFamilyBuffEntry buff : MapleFamilyBuff.getBuffEntry())
            if not self.canUseFamilyBuff(buff):
                used.add(new Pair<Integer, Integer>(buff.index, buff.count))
        return used

    def getTeleportName(self) -> str:
        return self.teleportname

    def setTeleportName(self, tname: str) -> None:
        self.teleportname = tname

    def getNoJuniors(self) -> int:
        if self.mfc is None:
            return 0
        return self.mfc.getNoJuniors()

    def getMFC(self) -> Any:
        return self.mfc

    def makeMFC(self, familyid: int, seniorid: int, junior1: int, junior2: int) -> None:
        if familyid > 0:
            f = World.Family.getFamily(familyid)
            if f is None:
                self.mfc = None
            else:
                self.mfc = f.getMFC(self.id)
                if self.mfc is None:
                    self.mfc = f.addFamilyMemberInfo(this, seniorid, junior1, junior2)
                if self.mfc.getSeniorId() != seniorid:
                    self.mfc.setSeniorId(seniorid)
                if self.mfc.getJunior1() != junior1:
                    self.mfc.setJunior1(junior1)
                if self.mfc.getJunior2() != junior2:
                    self.mfc.setJunior2(junior2)
        else:
            self.mfc = None

    def setFamily(self, newf: int, news: int, newj1: int, newj2: int) -> None:
        if self.mfc is None or newf != self.mfc.getFamilyId() or news != self.mfc.getSeniorId() or newj1 != self.mfc.getJunior1() or newj2 != self.mfc.getJunior2():
            self.makeMFC(newf, news, newj1, newj2)

    def maxBattleshipHP(self, skillid: int) -> int:
        return self.getSkillLevel(skillid) * 5000 + (self.getLevel() - 120) * 3000

    def currentBattleshipHP(self) -> int:
        return self.battleshipHP

    def sendEnglishQuiz(self, msg: str) -> None:
        self.client.getSession().write(MaplePacketCreator.englishQuizMsg(msg))

    def fakeRelog(self) -> None:
        self.client.getSession().write(MaplePacketCreator.getCharInfo(this))
        mapp = self.getMap()
        mapp.removePlayer(this)
        mapp.addPlayer(this)
        self.client.getSession().write(MaplePacketCreator.serverNotice(5, "刷新人数据完成..."))

    def getcharmessage(self) -> str:
        return self.charmessage

    def setcharmessage(self, s: str) -> None:
        self.charmessage = s

    def getexpression(self) -> int:
        return self.expression

    def setexpression(self, s: int) -> None:
        self.expression = s

    def getconstellation(self) -> int:
        return self.constellation

    def setconstellation(self, s: int) -> None:
        self.constellation = s

    def getblood(self) -> int:
        return self.blood

    def setblood(self, s: int) -> None:
        self.blood = s

    def getmonth(self) -> int:
        return self.month

    def setmonth(self, s: int) -> None:
        self.month = s

    def getday(self) -> int:
        return self.day

    def setday(self, s: int) -> None:
        self.day = s

    def getTeam(self) -> int:
        return self.coconutteam

    def setTeam(self, team: int) -> None:
        self.coconutteam = team

    def getBeans(self) -> int:
        return self.beans

    def gainBeans(self, s: int) -> None:
        self.beans += s

    def setBeans(self, s: int) -> None:
        self.beans = s

    def getBeansNum(self) -> int:
        return self.beansNum

    def setBeansNum(self, beansNum: int) -> None:
        self.beansNum = beansNum

    def getBeansRange(self) -> int:
        return self.beansRange

    def setBeansRange(self, beansRange: int) -> None:
        beansRange = beansRange

    def isCanSetBeansNum(self) -> bool:
        return self.canSetBeansNum

    def setCanSetBeansNum(self, canSetBeansNum: bool) -> None:
        self.canSetBeansNum = canSetBeansNum

    def haveGM(self) -> bool:
        return self.gmLevel >= 2 and self.gmLevel <= 3

    def setprefix(self, prefix: int) -> None:
        self.prefix = prefix

    def getPrefix(self) -> int:
        return self.prefix

    def startMapEffect(self, msg: str, itemId: int) -> None:
        self.startMapEffect(msg, itemId, 10000)

    def startMapEffect1(self, msg: str, itemId: int) -> None:
        self.startMapEffect(msg, itemId, 20000)

    def startMapEffect_msg_itemId_duration(self, msg: str, itemId: int, duration: int) -> None:
        def _task_1():
            MapleCharacter.self.getClient().getSession().write(mapEffect.makeDestroyData())

        mapEffect = MapleMapEffect(msg, itemId)
        self.getClient().getSession().write(mapEffect.makeStartData())
        Timer.EventTimer.getInstance().schedule(_task_1, duration)

    def getDeadtime(self) -> int:
        return self.deadtime

    def setDeadtime(self, deadtime: int) -> None:
        self.deadtime = deadtime

    def increaseEquipExp(self, mobexp: int) -> None:
        mii = MapleItemInformationProvider.getInstance()
        try:
            for item in self.getInventory(MapleInventoryType.EQUIPPED).list():
                nEquip = item
                itemName = mii.getName(nEquip.getItemId())
                if itemName is None:
                    continue
                if (("重生" in itemName) or nEquip.getEquipLevel() >= 4) and (not ("永恒" in itemName) or nEquip.getEquipLevel() >= 6):
                    continue
                nEquip.gainItemExp(self.client, mobexp, ("永恒" in itemName))
        except Exception as ex:
            pass

    def petName(self, name: str) -> None:
        pet = self.getPet(0)
        if pet is None:
            self.getClient().getSession().write(MaplePacketCreator.serverNotice(1, "请召唤一只宠物出来！"))
            self.getClient().getSession().write(MaplePacketCreator.enableActions())
            return
        pet.setName(name)
        self.getClient().getSession().write(PetPacket.updatePet(pet, self.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
        self.getClient().getSession().write(MaplePacketCreator.enableActions())
        self.getClient().getPlayer().getMap().broadcastMessage(self.getClient().getPlayer(), MTSCSPacket.changePetName(self.getClient().getPlayer(), name, 1), True)

    def reloadC(self) -> None:
        self.client.getSession().write(MaplePacketCreator.getCharInfo(self.client.getPlayer()))
        self.client.getPlayer().getMap().removePlayer(self.client.getPlayer())
        self.client.getPlayer().getMap().addPlayer(self.client.getPlayer())

    def maxSkills(self) -> None:
        for sk in SkillFactory.getAllSkills():
            self.changeSkillLevel(sk, sk.getMaxLevel(), sk.getMaxLevel())

    def UpdateCash(self) -> None:
        self.getClient().getSession().write(MaplePacketCreator.showCharCash(this))

    def addAriantScore(self) -> None:
        self.ariantScore += 1

    def resetAriantScore(self) -> None:
        self.ariantScore = 0

    def getAriantScore(self) -> int:
        return self.ariantScore

    def updateAriantScore(self) -> None:
        self.getMap().broadcastMessage(MaplePacketCreator.updateAriantScore(self.getName(), self.getAriantScore(), False))

    def getAveragePartyLevel(self) -> int:
        averageLevel = 0
        size = 0
        for pl in self.getParty().getMembers():
            averageLevel += pl.getLevel()
            size += 1
        if size <= 0:
            return self.level
        averageLevel /= size
        return averageLevel

    def getAverageMapLevel(self) -> int:
        averageLevel = 0
        size = 0
        for pl in self.getMap().getCharacters():
            averageLevel += pl.getLevel()
            size += 1
        if size <= 0:
            return self.level
        averageLevel /= size
        return averageLevel

    def setApprentice(self, app: int) -> None:
        self.apprentice = app

    def hasApprentice(self) -> bool:
        return self.apprentice > 0

    def getMaster(self) -> int:
        return self.master

    def getApprentice(self) -> int:
        return self.apprentice

    def getApp(self) -> Any:
        return self.client.getChannelServer().getPlayerStorage().getCharacterById(self.apprentice)

    def getMster(self) -> Any:
        return self.client.getChannelServer().getPlayerStorage().getCharacterById(self.master)

    def setMaster(self, mstr: int) -> None:
        self.master = mstr

    def getMarriageRing(self, incluedEquip: bool) -> Any:
        iv = self.getInventory(MapleInventoryType.EQUIPPED)
        equippedC = iv.list()
        equipped = [])
        for item in equippedC:
            equipped.add(item)
        for item2 in equipped:
            if item2.getRing() is not None:
                ring = item2.getRing()
                ring.setEquipped(True)
                if GameConstants.isMarriageRing(item2.getItemId()):
                    return ring
                continue
        if incluedEquip:
            iv = self.getInventory(MapleInventoryType.EQUIP)
            for item in iv.list():
                if item.getRing() is not None and GameConstants.isMarriageRing(item.getItemId()):
                    ring = item.getRing()
                    ring.setEquipped(False)
                    return ring
        return None

    def setDebugMessage(self, control: bool) -> None:
        self.DebugMessage = control

    def getDebugMessage(self) -> bool:
        return self.DebugMessage

    def getNX(self) -> int:
        return self.getCSPoints(1)

    def canHold(self, itemid: int) -> bool:
        return self.getInventory(GameConstants.getInventoryType(itemid)).getNextFreeSlot() > -1

    def getIntRecord(self, questID: int) -> int:
        stat = self.getQuestNAdd(MapleQuest.getInstance(questID))
        if stat.getCustomData() is None:
            stat.setCustomData("0")
        return int(stat.getCustomData())

    def getIntNoRecord(self, questID: int) -> int:
        stat = self.getQuestNoAdd(MapleQuest.getInstance(questID))
        if stat is None or stat.getCustomData() is None:
            return 0
        return int(stat.getCustomData())

    def updatePetEquip(self) -> None:
        if self.getIntNoRecord(122221) > 0:
            self.client.getSession().write(MaplePacketCreator.petAutoHP(self.getIntRecord(122221)))
        if self.getIntNoRecord(122222) > 0:
            self.client.getSession().write(MaplePacketCreator.petAutoMP(self.getIntRecord(122222)))

    def spawnBomb(self) -> None:
        def _task_1():
            MapleCharacter.self.map.killMonster(bomb, MapleCharacter.self.client.getPlayer(), False, False, 1)

        bomb = MapleLifeFactory.getMonster(9300166)
        bomb.changeLevel(250, True)
        self.getMap().spawnMonster_sSack(bomb, self.getPosition(), -2)
        Timer.EventTimer.getInstance().schedule(_task_1, 10000)

    def isAriantPQMap(self) -> bool:
        # switch (self.getMapId()):
            # case 980010101:
            # case 980010201:
            # case 980010301:
                return True
            # default:
                return False

    def addMobVac(self, type: int) -> None:
        if type == 1:
            self.MobVac += 1
        elif type == 2:
            self.MobVac2 += 1

    def getMobVac(self, type: int) -> int:
        # switch (type):
            # case 1:
                return self.MobVac
            # case 2:
                return self.MobVac2
            # default:
                return 0

    def gainIten(self, id: int, amount: int) -> None:
        MapleInventoryManipulator.addById(self.getClient(), id, amount, 0)

    def getLastHM(self) -> int:
        return self.lastGainHM

    def setLastHM(self, newTime: int) -> None:
        self.lastGainHM = newTime

    def inIntro(self) -> bool:
        return MapleCharacter.tutorial

    def checkCopyItems(self) -> None:
        equipOnlyIds = []
        checkItems = {}
        for item in self.getInventory(MapleInventoryType.EQUIP).list():
            equipOnlyId = item.getEquipOnlyId()
            if equipOnlyId > 0:
                if (equipOnlyId in checkItems):
                    if checkItems.get(equipOnlyId) != item.getItemId():
                        continue
                    equipOnlyIds.add(equipOnlyId)
                else:
                    checkItems.put(equipOnlyId, item.getItemId())
        for item in self.getInventory(MapleInventoryType.EQUIPPED).list():
            equipOnlyId = item.getEquipOnlyId()
            if equipOnlyId > 0:
                if (equipOnlyId in checkItems):
                    if checkItems.get(equipOnlyId) != item.getItemId():
                        continue
                    equipOnlyIds.add(equipOnlyId)
                else:
                    checkItems.put(equipOnlyId, item.getItemId())
        for item in self.getInventory(MapleInventoryType.ETC).list():
            equipOnlyId = item.getEquipOnlyId()
            if equipOnlyId > 0:
                if (equipOnlyId in checkItems):
                    if checkItems.get(equipOnlyId) != item.getItemId():
                        continue
                    equipOnlyIds.add(equipOnlyId)
                else:
                    checkItems.put(equipOnlyId, item.getItemId())
        for item in self.getInventory(MapleInventoryType.USE).list():
            equipOnlyId = item.getEquipOnlyId()
            if equipOnlyId > 0:
                if (equipOnlyId in checkItems):
                    if checkItems.get(equipOnlyId) != item.getItemId():
                        continue
                    equipOnlyIds.add(equipOnlyId)
                else:
                    checkItems.put(equipOnlyId, item.getItemId())
        for item in self.getInventory(MapleInventoryType.CASH).list():
            equipOnlyId = item.getEquipOnlyId()
            if equipOnlyId > 0:
                if (equipOnlyId in checkItems):
                    if checkItems.get(equipOnlyId) != item.getItemId():
                        continue
                    equipOnlyIds.add(equipOnlyId)
                else:
                    checkItems.put(equipOnlyId, item.getItemId())
        autoban = False
        for equipOnlyId2 in equipOnlyIds:
            MapleInventoryManipulator.removeAllByEquipOnlyId(self.client, equipOnlyId2)
            autoban = True
        if autoban:
            AutobanManager.getInstance().autoban(self.client, "无理由.")
        checkItems.clear()
        equipOnlyIds.clear()

    def getskillzq(self) -> int:
        return self.skillzq

    def setskillzq(self, s: int) -> None:
        self.skillzq = s

    def getbosslog(self) -> int:
        return self.bosslog

    def setbosslog(self, s: int) -> None:
        self.bosslog = s

    def getPGMaxDamage(self) -> int:
        return self.PGMaxDamage

    def setPGMaxDamage(self, s: int) -> None:
        self.PGMaxDamage = s

    def getjzname(self) -> int:
        return self.jzname

    def setjzname(self, s: int) -> None:
        self.jzname = s

    def getmrsgrw(self) -> int:
        return self.mrsgrw

    def setmrsgrw(self, s: int) -> None:
        self.mrsgrw = s

    def getmrsgrwa(self) -> int:
        return self.mrsgrwa

    def setmrsgrwa(self, s: int) -> None:
        self.mrsgrwa = s

    def getmrsgrwas(self) -> int:
        return self.mrsgrwas

    def setmrsgrwas(self, s: int) -> None:
        self.mrsgrwas = s

    def getmrsgrws(self) -> int:
        return self.mrsgrws

    def setmrsgrws(self, s: int) -> None:
        self.mrsgrws = s

    def gethythd(self) -> int:
        return self.hythd

    def sethythd(self, s: int) -> None:
        self.hythd = s

    def getmrsjrw(self) -> int:
        return self.mrsjrw

    def setmrsjrw(self, s: int) -> None:
        self.mrsjrw = s

    def getmrfbrw(self) -> int:
        return self.mrfbrw

    def setmrfbrw(self, s: int) -> None:
        self.mrfbrw = s

    def getmrsbossrw(self) -> int:
        return self.mrsbossrw

    def setmrsbossrw(self, s: int) -> None:
        self.mrsbossrw = s

    def getmrfbrws(self) -> int:
        return self.mrfbrws

    def setmrfbrws(self, s: int) -> None:
        self.mrfbrws = s

    def getmrsbossrws(self) -> int:
        return self.mrsbossrws

    def setmrsbossrws(self, s: int) -> None:
        self.mrsbossrws = s

    def getmrfbrwa(self) -> int:
        return self.mrfbrwa

    def setmrfbrwa(self, s: int) -> None:
        self.mrfbrwa = s

    def getmrsbossrwa(self) -> int:
        return self.mrsbossrwa

    def setmrsbossrwa(self, s: int) -> None:
        self.mrsbossrwa = s

    def getmrfbrwas(self) -> int:
        return self.mrfbrwas

    def setmrfbrwas(self, s: int) -> None:
        self.mrfbrwas = s

    def getvip(self) -> int:
        return self.vip

    def setvip(self, s: int) -> None:
        self.vip = s

    def gainvip(self, s: int) -> None:
        self.vip += s

    def getddj(self) -> int:
        return self.ddj

    def setddj(self, s: int) -> None:
        self.ddj = s

    def gainddj(self, s: int) -> None:
        self.ddj += s

    def getdjjl(self) -> int:
        return self.djjl

    def setdjjl(self, s: int) -> None:
        self.djjl = s

    def gaindjjl(self, s: int) -> None:
        self.djjl += s

    def getSG(self) -> int:
        return self.shaguai

    def setSG(self, s: int) -> None:
        self.shaguai = s

    def gainSG(self, s: int) -> None:
        self.shaguai += s

    def getqiandao(self) -> int:
        return self.qiandao

    def setqiandao(self, s: int) -> None:
        self.qiandao = s

    def gainqiandao(self, s: int) -> None:
        self.qiandao += s

    def getmrsbossrwas(self) -> int:
        return self.mrsbossrwas

    def setmrsbossrwas(self, s: int) -> None:
        self.mrsbossrwas = s

    def translated_获取全民夺宝总数(self) -> int:
        con = DatabaseConnection.getConnection()
        sql = "SELECT count(*) from qmdbplayer"
        ps = con.prepareStatement(sql)
        rs = ps.executeQuery()
        count = -1
        if rs.next():
            count = rs.getInt(1)
        rs.close()
        ps.close()
        return count

    def translated_全民夺宝(self, type: int) -> int:
        pay = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from qmdb")
            rs = ps.executeQuery()
            if rs.next():
                # switch (type):
                    # case 1:
                        pay = rs.getInt("itemid")
                        break
                    # case 2:
                        pay = rs.getInt("money")
                        break
                    # case 3:
                        pay = rs.getInt("characterid")
                        break
                    # case 4:
                        pay = rs.getInt("type")
                        break
                    # case 5:
                        pay = rs.getInt("sl")
                        break
                    # default:
                        pay = 0
                        break
            ps.close()
            rs.close()
        except Exception as ex:
            print("查询全民夺宝信息错误: " + ex)
        return pay

    def translated_全民夺宝2(self, id: int) -> str:
        pay = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from qmdbplayer where id = " + id + "")
            rs = ps.executeQuery()
            if rs.next():
                pay = rs.getString("name")
            ps.close()
            rs.close()
        except Exception as ex:
            print("查询全民夺宝信息Name错误: " + ex)
        return pay

    def translated_全民夺宝3(self, id: int) -> int:
        pay = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from qmdbplayer where id = " + id + "")
            rs = ps.executeQuery()
            if rs.next():
                pay = rs.getInt("characterid")
            ps.close()
            rs.close()
        except Exception as ex:
            print("查询全民夺宝信息Id错误: " + ex)
        return pay

    def translated_领取日志(self) -> str:
        result = ""
        i = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM qmdblog")
            rs = ps.executeQuery()
            while rs.next():
                result = result + "#b时间#r#e[" + rs.getTimestamp("sj") + "]#n#k\r\n幸运玩家：#b#e" + rs.getString("name") + "#n #k赢取奖励:#b#e#z" + rs.getInt("itemid") + "#x" + rs.getInt("sl") + "#n\r\n---------------------------------------------\r\n"
        except Exception as ex:
            return ""
        return result

    def translated_玩家获得物品(self, id: int, name: str) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE qmdb SET characterid = " + id + ",name = " + name + ",type = 1")
            ps2 = con.prepareStatement("UPDATE qmdblog SET sj = CURRENT_TIMESTAMP(),characterid = " + id + ",name = " + name + "")
            ps.executeUpdate()
            ps2.executeUpdate()
            ps.close()
            ps2.cancel()
            return 1
        except Exception as ex:
            print("数据库操作错误，方法:玩家获得物品(int id,String name) " + ex)
            return 0

    def translated_玩家获得物品2(self, lx: int) -> int:
        pay = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from qmdb where characterid = " + self.getId() + "")
            rs = ps.executeQuery()
            if rs.next():
                if lx == 1:
                    pay = rs.getInt("itemid")
                elif lx == 2:
                    pay = rs.getInt("sl")
            ps.close()
            rs.close()
        except Exception as ex:
            print("查询全民夺宝信息Id错误: " + ex)
        return pay

    def translated_全民夺宝删除(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("Truncate Table qmdb ")
            ps2 = con.prepareStatement("Truncate Table qmdbplayer ")
            ps.executeUpdate()
            ps2.executeUpdate()
            ps.close()
            ps2.cancel()
        except Exception as ex:
            print("数据库操作错误，全民夺宝删除 " + ex)

    def translated_参加全民夺宝(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            psu = con.prepareStatement("insert into qmdbplayer (characterid, name) VALUES (?, ?)")
            psu.setInt(1, self.getId())
            psu.setString(2, self.getName())
            psu.executeUpdate()
            psu.close()
        except Exception as ex:
            print("参加全民夺宝发生了错误: " + ex)

    def getSJRW(self) -> int:
        try:
            sjrw = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                sjrw = rs.getInt("sjrw")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    sjrw = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET sjrw = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, sjrw) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return sjrw
        except Exception as Ex:
            print("获取角色帐号的0点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainSJRW(self, amount: int) -> None:
        sjrw = self.getSJRW() + amount
        self.updateSJRW(sjrw)

    def resetSJRW(self) -> None:
        self.updateSJRW(0)

    def updateSJRW(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET sjrw = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getFBRW(self) -> int:
        try:
            fbrw = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                fbrw = rs.getInt("fbrw")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    fbrw = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET fbrw = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, fbrw) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return fbrw
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainFBRW(self, amount: int) -> None:
        fbrw = self.getFBRW() + amount
        self.updateFBRW(fbrw)

    def resetFBRW(self) -> None:
        self.updateFBRW(0)

    def updateFBRW(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET fbrw = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getFBRWA(self) -> int:
        try:
            fbrwa = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                fbrwa = rs.getInt("fbrwa")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    fbrwa = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET fbrwa = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, fbrwa) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return fbrwa
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainFBRWA(self, amount: int) -> None:
        fbrw = self.getFBRWA() + amount
        self.updateFBRWA(fbrw)

    def resetFBRWA(self) -> None:
        self.updateFBRWA(0)

    def updateFBRWA(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET fbrwa = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getSGRW(self) -> int:
        try:
            sgrw = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                sgrw = rs.getInt("sgrw")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    sgrw = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET sgrw = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, sgrw) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return sgrw
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainSGRW(self, amount: int) -> None:
        sgrw = self.getSGRW() + amount
        self.updateSGRW(sgrw)

    def resetSGRW(self) -> None:
        self.updateSGRW(0)

    def updateSGRW(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET sgrw = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getSGRWA(self) -> int:
        try:
            sgrwa = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                sgrwa = rs.getInt("sgrwa")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    sgrwa = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET sgrwa = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, sgrwa) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return sgrwa
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainSGRWA(self, amount: int) -> None:
        sgrw = self.getSGRWA() + amount
        self.updateSGRWA(sgrw)

    def resetSGRWA(self) -> None:
        self.updateSGRWA(0)

    def updateSGRWA(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET sgrwa = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getSBOSSRW(self) -> int:
        try:
            sbossrw = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                sbossrw = rs.getInt("sbossrw")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    sbossrw = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET sbossrw = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, sbossrw) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return sbossrw
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainSBOSSRW(self, amount: int) -> None:
        sbossrw = self.getSBOSSRW() + amount
        self.updateSBOSSRW(sbossrw)

    def resetSBOSSRW(self) -> None:
        self.updateSBOSSRW(0)

    def updateSBOSSRW(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET sbossrw = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getSBOSSRWA(self) -> int:
        try:
            sbossrwa = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                sbossrwa = rs.getInt("sbossrwa")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    sbossrwa = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET sbossrwa = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, sbossrwa) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return sbossrwa
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainSBOSSRWA(self, amount: int) -> None:
        sbossrw = self.getSBOSSRWA() + amount
        self.updateSBOSSRWA(sbossrw)

    def resetSBOSSRWA(self) -> None:
        self.updateSBOSSRWA(0)

    def updateSBOSSRWA(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET sbossrwa = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getlb(self) -> int:
        try:
            lb = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                lb = rs.getInt("lb")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    lb = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET lb = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, lb) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return lb
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainlb(self, amount: int) -> None:
        lb = self.getlb() + amount
        self.updatelb(lb)

    def resetlb(self) -> None:
        self.updatelb(0)

    def updatelb(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET lb = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getGamePoints(self) -> int:
        try:
            gamePoints = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                gamePoints = rs.getInt("gamePoints")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    gamePoints = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET gamePoints = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, gamePoints) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return gamePoints
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def getGamePointsPD(self) -> int:
        try:
            gamePointsPD = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                gamePointsPD = rs.getInt("gamePointspd")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    gamePointsPD = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET gamePointspd = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, gamePointspd) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return gamePointsPD
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainGamePoints(self, amount: int) -> None:
        gamePoints = self.getGamePoints() + amount
        self.updateGamePoints(gamePoints)

    def gainGamePointsPD(self, amount: int) -> None:
        gamePointsPD = self.getGamePointsPD() + amount
        self.updateGamePointsPD(gamePointsPD)

    def resetGamePointsPD(self) -> None:
        self.updateGamePointsPD(0)

    def updateGamePointsPD(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET gamePointspd = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def resetGamePoints(self) -> None:
        self.updateGamePoints(0)

    def updateGamePoints(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET gamePoints = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getGamePointsRQ(self) -> int:
        try:
            gamePointsRQ = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                gamePointsRQ = rs.getInt("gamePointsrq")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    gamePointsRQ = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET gamePointsrq = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, gamePointsrq) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return gamePointsRQ
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainGamePointsRQ(self, amount: int) -> None:
        gamePointsRQ = self.getGamePointsRQ() + amount
        self.updateGamePointsRQ(gamePointsRQ)

    def resetGamePointsRQ(self) -> None:
        self.updateGamePointsRQ(0)

    def updateGamePointsRQ(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET gamePointsrq = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getGamePointsPS(self) -> int:
        try:
            gamePointsRQ = 0
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts_info WHERE accId = ? AND worldId = ?")
            ps.setInt(1, self.getClient().getAccID())
            ps.setInt(2, self.getWorld())
            rs = ps.executeQuery()
            if rs.next():
                gamePointsRQ = rs.getInt("gamePointsps")
                updateTime = rs.getTimestamp("updateTime")
                sqlcal = Calendar.getInstance()
                if updateTime is not None:
                    sqlcal.setTimeInMillis(updateTime.getTime())
                if sqlcal.get(5) + 1 <= Calendar.getInstance().get(5) or sqlcal.get(2) + 1 <= Calendar.getInstance().get(2) or sqlcal.get(1) + 1 <= Calendar.getInstance().get(1):
                    gamePointsRQ = 0
                    psu = con.prepareStatement("UPDATE accounts_info SET gamePointsps = 0, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
                    psu.setInt(1, self.getClient().getAccID())
                    psu.setInt(2, self.getWorld())
                    psu.executeUpdate()
                    psu.close()
            else:
                psu2 = con.prepareStatement("INSERT INTO accounts_info (accId, worldId, gamePointsps) VALUES (?, ?, ?)")
                psu2.setInt(1, self.getClient().getAccID())
                psu2.setInt(2, self.getWorld())
                psu2.setInt(3, 0)
                psu2.executeUpdate()
                psu2.close()
            rs.close()
            ps.close()
            return gamePointsRQ
        except Exception as Ex:
            print("获取角色帐号的在线时间点出现错误 - 数据库查询失败" + Ex)
            return -1

    def gainGamePointsPS(self, amount: int) -> None:
        gamePointsPS = self.getGamePointsPS() + amount
        self.updateGamePointsPS(gamePointsPS)

    def resetGamePointsPS(self) -> None:
        self.updateGamePointsPS(0)

    def updateGamePointsPS(self, amount: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE accounts_info SET gamePointsps = ?, updateTime = CURRENT_TIMESTAMP() WHERE accId = ? AND worldId = ?")
            ps.setInt(1, amount)
            ps.setInt(2, self.getClient().getAccID())
            ps.setInt(3, self.getWorld())
            ps.executeUpdate()
            ps.close()
        except Exception as Ex:
            print("更新角色帐号的在线时间出现错误 - 数据库更新失败." + Ex)

    def getHyPay(self, type: int) -> int:
        pay = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from hypay where accname = ?")
            ps.setString(1, self.getClient().getAccountName())
            rs = ps.executeQuery()
            if rs.next():
                # switch (type):
                    # case 1:
                        pay = rs.getInt("pay")
                        break
                    # case 2:
                        pay = rs.getInt("payUsed")
                        break
                    # case 3:
                        pay = rs.getInt("pay") + rs.getInt("payUsed")
                        break
                    # case 4:
                        pay = rs.getInt("payReward")
                        break
                    # default:
                        pay = 0
                        break
            else:
                psu = con.prepareStatement("insert into hypay (accname, pay, payUsed, payReward) VALUES (?, ?, ?, ?)")
                psu.setString(1, self.getClient().getAccountName())
                psu.setInt(2, 0)
                psu.setInt(3, 0)
                psu.setInt(4, 0)
                psu.executeUpdate()
                psu.close()
            ps.close()
            rs.close()
        except Exception as ex:
            print("获取充值信息发生错误: " + ex)
        return pay

    def gainHyPay(self, hypay: int) -> int:
        pay = self.getHyPay(1)
        payUsed = self.getHyPay(2)
        payReward = self.getHyPay(4)
        if hypay <= 0:
            return 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE hypay SET pay = ? ,payUsed = ? ,payReward = ? where accname = ?")
            ps.setInt(1, pay + hypay)
            ps.setInt(2, payUsed)
            ps.setInt(3, payReward)
            ps.setString(4, self.getClient().getAccountName())
            ps.executeUpdate()
            ps.close()
            return 1
        except Exception as ex:
            print("加减充值信息发生错误: " + ex)
            return 0

    def addHyPay(self, hypay: int) -> int:
        pay = self.getHyPay(1)
        payUsed = self.getHyPay(2)
        payReward = self.getHyPay(4)
        if hypay > pay:
            return -1
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE hypay SET pay = ? ,payUsed = ? ,payReward = ? where accname = ?")
            ps.setInt(1, pay - hypay)
            ps.setInt(2, payUsed + hypay)
            ps.setInt(3, payReward + hypay)
            ps.setString(4, self.getClient().getAccountName())
            ps.executeUpdate()
            ps.close()
            return 1
        except Exception as ex:
            print("加减充值信息发生错误: " + ex)
            return -1

    def delPayReward(self, pay: int) -> int:
        payReward = self.getHyPay(4)
        if pay <= 0:
            return -1
        if pay > payReward:
            return -1
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE hypay SET payReward = ? where accname = ?")
            ps.setInt(1, payReward - pay)
            ps.setString(2, self.getClient().getAccountName())
            ps.executeUpdate()
            ps.close()
            return 1
        except Exception as ex:
            print("加减消费奖励信息发生错误: " + ex)
            return -1

    def getFishingJF(self, type: int) -> int:
        jf = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("select * from fishingjf where accname = ?")
            ps.setString(1, self.getClient().getAccountName())
            rs = ps.executeQuery()
            if rs.next():
                # switch (type):
                    # case 1:
                        jf = rs.getInt("fishing")
                        break
                    # case 2:
                        jf = rs.getInt("XX")
                        break
                    # case 3:
                        jf = rs.getInt("XXX")
                        break
                    # default:
                        jf = 0
                        break
            else:
                psu = con.prepareStatement("insert into fishingjf (accname, fishing, XX, XXX) VALUES (?, ?, ?, ?)")
                psu.setString(1, self.getClient().getAccountName())
                psu.setInt(2, 0)
                psu.setInt(3, 0)
                psu.setInt(4, 0)
                psu.executeUpdate()
                psu.close()
            ps.close()
            rs.close()
        except Exception as ex:
            print("获取钓鱼积分信息发生错误: " + ex)
        return jf

    def gainFishingJF(self, hypay: int) -> int:
        jf = self.getFishingJF(1)
        XX = self.getFishingJF(2)
        XXX = self.getFishingJF(3)
        if hypay <= 0:
            return 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE fishingjf SET fishing = ? ,XX = ? ,XXX = ? where accname = ?")
            ps.setInt(1, hypay + jf)
            ps.setInt(2, XX)
            ps.setInt(3, XXX)
            ps.setString(4, self.getClient().getAccountName())
            ps.executeUpdate()
            ps.close()
            return 1
        except Exception as ex:
            print("加减钓鱼积分信息发生错误: " + ex)
            return 0

    def addFishingJF(self, hypay: int) -> int:
        jf = self.getFishingJF(1)
        XX = self.getFishingJF(2)
        XXX = self.getFishingJF(3)
        if hypay > jf:
            return -1
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE fishingjf SET fishing = ? ,XX = ? ,XXX = ? where accname = ?")
            ps.setInt(1, jf - hypay)
            ps.setInt(2, XX)
            ps.setInt(3, XXX)
            ps.setString(4, self.getClient().getAccountName())
            ps.executeUpdate()
            ps.close()
            return 1
        except Exception as ex:
            print("加减钓鱼积分信息发生错误: " + ex)
            return -1

    def getBounds(self) -> Any:
        return Rectangle(self.getTruePosition().x - 25, self.getTruePosition().y - 75, 50, 75)

    def getTouzhuNX(self) -> int:
        return self.touzhuNX

    def setTouzhuNX(self, touzhuNX: int) -> None:
        self.touzhuNX = touzhuNX

    def getTouzhuNum(self) -> int:
        return self.touzhuNum

    def setTouzhuNum(self, touzhuNum: int) -> None:
        self.touzhuNum = touzhuNum

    def getTouzhuType(self) -> int:
        return self.touzhuType

    def setTouzhuType(self, touzhuType: int) -> None:
        self.touzhuType = touzhuType

    def getPvpStats(self) -> Any:
        return self.pvpStats

    def getPvpKills(self) -> int:
        return self.pvpKills

    def gainPvpKill(self) -> None:
        self.pvpKills += 1
        self.pvpVictory += 1
        if self.pvpVictory == 5:
            self.map.broadcastMessage(MaplePacketCreator.serverNotice(6, "[Pvp] 玩家 " + self.getName() + " 已经达到 5 连斩。"))
        elif self.pvpVictory == 10:
            self.client.getChannelServer().broadcastMessage(MaplePacketCreator.serverNotice(6, "[Pvp] 玩家 " + self.getName() + " 已经达到 10 连斩。"))
        elif self.pvpVictory >= 20:
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "[Pvp] 玩家 " + self.getName() + " 已经达到 " + self.pvpVictory + " 连斩。他在频道 " + self.client.getChannel() + " 地图 " + self.map.getMapName() + " 中喊道谁能赐我一死."))
        else:
            self.dropMessage(6, "当前: " + self.pvpVictory + " 连斩.")

    def getPvpDeaths(self) -> int:
        return self.pvpDeaths

    def gainPvpDeath(self) -> None:
        self.pvpDeaths += 1
        self.pvpVictory = 0

    def getPvpVictory(self) -> int:
        return self.pvpVictory

    def getMerchantMeso(self) -> int:
        mesos = 0
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT * from hiredmerch where characterid = ?")
            ps.setInt(1, self.id)
            rs = ps.executeQuery()
            if rs.next():
                mesos = rs.getInt("Mesos")
            rs.close()
            ps.close()
        except Exception as se:
            print("获取雇佣商店金币发生错误" + se)
        return mesos

    def canExpiration(self, now: int) -> bool:
        return self.lastExpirationTime > 0 and self.lastExpirationTime + 60000 < now

    def startCheck(self) -> None:
        mac = self.client.getMac()
        if not self.client.isBanndMac2(mac) and self.client.getHandSome(self.client.getAccountName()) == self.client.getHandSome2():
            print("[作弊] 检测到玩家 " + self.getName() + " 登录器关闭，系统对其进行断开连接处理。")
            FileoutputUtil.packetLog("logs/防万能检测.txt", "玩家名称：" + self.getName() + " 账号在数据库的ID：" + self.getAccountID() + "检测到其与登录器断开连接。服务器对他执行断线处理。他的MAC地址：" + self.getClient().getMac() + "\r\n")
            self.sendPolice()
        elif self.client.getHandSome(self.client.getAccountName()) == 100:
            print("[发现偷渡者] 检测到玩家 " + self.getName() + " 非法进入游戏")
            FileoutputUtil.packetLog("logs/防万能检测.txt", "玩家名称：" + self.getName() + " 账号在数据库的ID：" + self.getAccountID() + "检测到其非法进入游戏。服务器对他执行断线处理。他的MAC地址：" + self.getClient().getMac() + "\r\n")
            self.sendPolice()

    def sendPolice(self) -> None:
        def _task_1():
            MapleCharacter.self.client.disconnect(True, False)
            if MapleCharacter.self.client.getSession().isConnected():
                MapleCharacter.self.client.getSession().close(True)
            FileoutputUtil.packetLog("玩家被断开连接.txt", MapleCharacter.self.getName() + " 源代码 第8776行 原因：防万能检测到其与登陆器断开，服务器断开他的连接\r\n")

        self.client.getSession().write(MaplePacketCreator.serverNotice(1, "检测到登录器关闭，游戏即将断开。"))
        Timer.WorldTimer.getInstance().schedule(_task_1, 6000)

    def translated_获取怪物数量(self, mapId: int) -> int:
        return self.client.getChannelServer().getMapFactory().getMap(mapId).getNumMonsters()

    def translated_刷新地图(self) -> None:
        custMap = True
        mapid = self.getMapId()
        map = custMap ? self.getClient().getChannelServer().getMapFactory().getMap(mapid) : self.getMap()
        if self.getClient().getChannelServer().getMapFactory().destroyMap(mapid):
            newMap = self.getClient().getChannelServer().getMapFactory().getMap(mapid)
            newPor = newMap.getPortal(0)
            mcs = new LinkedHashSet<MapleCharacter>(map.getCharacters())
            for m in mcs:
                x = 0
                while x < 5:
                    try:
                        m.changeMap(newMap, newPor)
                    except Exception as t:
                        x += 1
                        continue
                    break

    def translated_获取角色数量(self, mapid: int) -> int:
        return self.client.getChannelServer().getMapFactory().getMap(mapid).getCharactersSize()

    def refreshPGDamage(self) -> None:
        self.curPGDamage = self.stats.getCurrentMaxBaseDamage()
        if self.curPGDamage > self.getPGMaxDamage():
            self.setPGMaxDamage(self.curPGDamage)


# Inner class from Java (originally nested)
class FameStatus(Enum):
    """Enum FameStatus"""

    OK = 0
    NOT_TODAY = 1
    NOT_THIS_MONTH = 2

