"""
MapleLifeFactory - Converted from Java source
Original: server/life/MapleLifeFactory.java
Package: server.life
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import math
import os
import pymysql
import sys

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from provider.WzXML.MapleDataType import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class MapleLifeFactory:
    """
    Class MapleLifeFactory
    """

    # Static initializer
    # data = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Mob.wz"))
    # stringDataWZ = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz"))
    # etcDataWZ = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Etc.wz"))
    # mobStringData = MapleLifeFactory.stringDataWZ.getData("Mob.img")
    # npcStringData = MapleLifeFactory.stringDataWZ.getData("Npc.img")
    # npclocData = MapleLifeFactory.etcDataWZ.getData("NpcLocation.img")
    # npcNames = {}
    # monsterStats = {}
    # NPCLoc = {}
    # questCount = new HashMap<Integer, List<Integer>>()


    @staticmethod
    def getLife(id: int, type: str) -> Any:
        if type.lower() == "n".lower():
            return getNPC(id)
        if type.lower() == "m".lower():
            return getMonster(id)
        print("Unknown Life type: " + type + "")
        return None

    def getNPCLocation(self, npcid: int) -> int:
        if (npcid in MapleLifeFactory.NPCLoc):
            return MapleLifeFactory.NPCLoc.get(npcid)
        map = MapleDataTool.getIntConvert(Integer.toString(npcid) + "/0", MapleLifeFactory.npclocData, -1)
        MapleLifeFactory.NPCLoc.put(npcid, map)
        return map

    def loadQuestCounts(self) -> None:
        if MapleLifeFactory.questCount > 0:
            return
        for mapz in MapleLifeFactory.data.getRoot().getSubdirectories():
            if mapz.getName() == ("QuestCountGroup"):
                for entry in mapz.getFiles():
                    id = int(entry.getName()[0:entry.getName(] - 4))
                    dat = MapleLifeFactory.data.getData("QuestCountGroup/" + entry.getName())
                    if dat is not None && dat.getChildByPath("info") is not None:
                        z = []
                        for da in dat.getChildByPath("info"):
                            z.add(MapleDataTool.getInt(da, 0))
                        MapleLifeFactory.questCount.put(id, z)
                    else:
                        print("None questcountgroup")
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT * FROM wz_npcnamedata ORDER BY `npc`"
        try:
        rs = ps.executeQuery())
            while rs.next():
                MapleLifeFactory.npcNames.put(rs.getInt("npc"), rs.getString("name"))
        except Exception as ex:
            print("Failed to load npc name data. " + ex)
            FileoutputUtil.outputFileError("logs/数据库异常.txt", ex)
        print("共加载NPC：" + MapleLifeFactory.npcNames)

    def getQuestCount(self, id: int) -> list:
        return MapleLifeFactory.questCount.get(id)

    def getMonster(self, mid: int) -> Any:
        stats = MapleLifeFactory.monsterStats.get(mid)
        if stats is None:
            monsterData = MapleLifeFactory.data.getData(StringUtil.getLeftPaddedStr(Integer.toString(mid) + ".img", '0', 11))
            if monsterData is None:
                return None
            monsterInfoData = monsterData.getChildByPath("info")
            stats = MapleMonsterStats()
            stats.setHp(MapleDataTool.getIntConvert("maxHP", monsterInfoData))
            stats.setMp(MapleDataTool.getIntConvert("maxMP", monsterInfoData, 0))
            stats.setExp(MapleDataTool.getIntConvert("exp", monsterInfoData, 0))
            stats.setLevel(MapleDataTool.getIntConvert("level", monsterInfoData))
            stats.setRemoveAfter(MapleDataTool.getIntConvert("removeAfter", monsterInfoData, 0))
            stats.setrareItemDropLevel(MapleDataTool.getIntConvert("rareItemDropLevel", monsterInfoData, 0))
            stats.setFixedDamage(MapleDataTool.getIntConvert("fixedDamage", monsterInfoData, -1))
            stats.setOnlyNormalAttack(MapleDataTool.getIntConvert("onlyNormalAttack", monsterInfoData, 0) > 0)
            stats.setBoss(MapleDataTool.getIntConvert("boss", monsterInfoData, 0) > 0 || mid == 8810018 || mid == 9410066 || (mid >= 8810118 && mid <= 8810122))
            stats.setExplosiveReward(MapleDataTool.getIntConvert("explosiveReward", monsterInfoData, 0) > 0)
            stats.setFfaLoot(MapleDataTool.getIntConvert("publicReward", monsterInfoData, 0) > 0)
            stats.setUndead(MapleDataTool.getIntConvert("undead", monsterInfoData, 0) > 0 || mid == 9700004 || mid == 9700009 || mid == 9700010)
            stats.setName(MapleDataTool.getString(mid + "/name", MapleLifeFactory.mobStringData, "MISSINGNO"))
            stats.setBuffToGive(MapleDataTool.getIntConvert("buff", monsterInfoData, -1))
            stats.setFriendly(MapleDataTool.getIntConvert("damagedByMob", monsterInfoData, 0) > 0)
            stats.setExplosiveReward(MapleDataTool.getIntConvert("explosiveReward", monsterInfoData, 0) > 0)
            stats.setNoDoom(MapleDataTool.getIntConvert("noDoom", monsterInfoData, 0) > 0)
            stats.setFfaLoot(MapleDataTool.getIntConvert("publicReward", monsterInfoData, 0) > 0)
            stats.setCP(MapleDataTool.getIntConvert("getCP", monsterInfoData, 0))
            stats.setPoint(MapleDataTool.getIntConvert("point", monsterInfoData, 0))
            stats.setDropItemPeriod(MapleDataTool.getIntConvert("dropItemPeriod", monsterInfoData, 0))
            stats.setPhysicalDefense(MapleDataTool.getIntConvert("PDDamage", monsterInfoData, 0))
            stats.setMagicDefense(MapleDataTool.getIntConvert("MDDamage", monsterInfoData, 0))
            stats.setEva(MapleDataTool.getIntConvert("eva", monsterInfoData, 0))
            hideHP = MapleDataTool.getIntConvert("HPgaugeHide", monsterInfoData, 0) > 0 || MapleDataTool.getIntConvert("hideHP", monsterInfoData, 0) > 0
            selfd = monsterInfoData.getChildByPath("selfDestruction")
            if selfd is not None:
                stats.setSelfDHP(MapleDataTool.getIntConvert("hp", selfd, 0))
                stats.setSelfD(MapleDataTool.getIntConvert("action", selfd, -1))
            else:
                stats.setSelfD((byte)(-1))
            firstAttackData = monsterInfoData.getChildByPath("firstAttack")
            if firstAttackData is not None:
                if firstAttackData.getType() == MapleDataType.FLOAT:
                    stats.setFirstAttack(Math.round(MapleDataTool.getFloat(firstAttackData)) > 0)
                else:
                    stats.setFirstAttack(MapleDataTool.getInt(firstAttackData) > 0)
            if stats.isBoss() || isDmgSponge(mid):
                if hideHP || monsterInfoData.getChildByPath("hpTagColor") is None || monsterInfoData.getChildByPath("hpTagBgcolor") is None:
                    stats.setTagColor(0)
                    stats.setTagBgColor(0)
                else:
                    stats.setTagColor(MapleDataTool.getIntConvert("hpTagColor", monsterInfoData))
                    stats.setTagBgColor(MapleDataTool.getIntConvert("hpTagBgcolor", monsterInfoData))
            banishData = monsterInfoData.getChildByPath("ban")
            if banishData is not None:
                stats.setBanishInfo(BanishInfo(MapleDataTool.getString("banMsg", banishData), MapleDataTool.getInt("banMap/0/field", banishData, -1), MapleDataTool.getString("banMap/0/portal", banishData, "sp")))
            reviveInfo = monsterInfoData.getChildByPath("revive")
            if reviveInfo is not None:
                revives = []
                for bdata in reviveInfo:
                    revives.add(MapleDataTool.getInt(bdata))
                stats.setRevives(revives)
            monsterSkillData = monsterInfoData.getChildByPath("skill")
            if monsterSkillData is not None:
                i = 0
                skills = new ArrayList<Pair<Integer, Integer>>()
                while monsterSkillData.getChildByPath(Integer.toString(i)) is not None:
                    skills.add(new Pair<Integer, Integer>(MapleDataTool.getInt(i + "/skill", monsterSkillData, 0), MapleDataTool.getInt(i + "/level", monsterSkillData, 0)))
                    i += 1
                stats.setSkills(skills)
            decodeElementalString(stats, MapleDataTool.getString("elemAttr", monsterInfoData, ""))
            link = MapleDataTool.getIntConvert("link", monsterInfoData, 0)
            if link != 0:
                monsterData = MapleLifeFactory.data.getData(StringUtil.getLeftPaddedStr(link + ".img", '0', 11))
            for idata in monsterData:
                if idata.getName() == ("fly"):
                    stats.setFly(True)
                    stats.setMobile(True)
                    break
                if !idata.getName() == ("move"):
                    continue
                stats.setMobile(True)
            hpdisplaytype = -1
            if stats.getTagColor() > 0:
                hpdisplaytype = 0
            elif stats.isFriendly():
                hpdisplaytype = 1
            elif mid >= 9300184 && mid <= 9300215:
                hpdisplaytype = 2
            elif !stats.isBoss() || mid == 9410066:
                hpdisplaytype = 3
            stats.setHPDisplayType(hpdisplaytype)
            MapleLifeFactory.monsterStats.put(mid, stats)
        return MapleMonster(mid, stats)

    def decodeElementalString(self, stats: Any, elemAttr: str) -> None:
        i = 0
        while i < elemAttr:
            stats.setEffectiveness(Element.getFromChar(elemAttr[i]), ElementalEffectiveness.getByNumber(Integer.valueOf(str(elemAttr[i + 1]))))

    def isDmgSponge(self, mid: int) -> bool:
        # switch (mid):
            # case 8810018:
            # case 8810118:
            # case 8810119:
            # case 8810120:
            # case 8810121:
            # case 8810122:
            # case 8820009:
            # case 8820010:
            # case 8820011:
            # case 8820012:
            # case 8820013:
            # case 8820014:
                return True
            # default:
                return False

    def getNPC(self, nid: int) -> Any:
        name = MapleLifeFactory.npcNames.get(nid)
        if name is None:
            name = MapleDataTool.getString(nid + "/name", MapleLifeFactory.npcStringData, "MISSINGNO")
            MapleLifeFactory.npcNames.put(nid, name)
        if name.find("Maple TV") != -1:
            return None
        return MapleNPC(nid, name)

