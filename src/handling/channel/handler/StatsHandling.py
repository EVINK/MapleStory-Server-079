"""
StatsHandling - Converted from Java source
Original: handling/channel/handler/StatsHandling.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any
import logging
import math

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class StatsHandling:
    """
    Class StatsHandling
    """

    # Static initializer
    # log = LoggerFactory.getLogger(StatsHandling.class)


    @staticmethod
    def DistributeAP(slea: Any, c: Any, chr: Any) -> None:
        statupdate = new ArrayList<Pair<MapleStat, Integer>>(2)
        c.getSession().write(MaplePacketCreator.updatePlayerStats(statupdate, True, chr.getJob()))
        chr.updateTick(slea.readInt())
        stat = chr.getStat()
        job = chr.getJob()
        if chr.getRemainingAp() > 0:
            # switch (slea.readInt()):
                # case 256:
                    if stat.getStr() >= 999:
                        return
                    stat.setStr((short)(stat.getStr() + 1))
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.STR, stat.getStr()))
                    break
                # case 512:
                    if stat.getDex() >= 999:
                        return
                    stat.setDex((short)(stat.getDex() + 1))
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.DEX, stat.getDex()))
                    break
                # case 1024:
                    if stat.getInt() >= 999:
                        return
                    stat.setInt((short)(stat.getInt() + 1))
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.INT, stat.getInt()))
                    break
                # case 2048:
                    if stat.getLuk() >= 999:
                        return
                    stat.setLuk((short)(stat.getLuk() + 1))
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.LUK, stat.getLuk()))
                    break
                # case 8192:
                    maxhp = stat.getMaxHp()
                    if chr.getHpApUsed() >= 10000 || maxhp >= 30000:
                        return
                    if job == 0:
                        maxhp += Randomizer.rand(8, 12)
                    elif (job >= 100 && job <= 132) || (job >= 3200 && job <= 3212):
                        improvingMaxHP = SkillFactory.getSkill(1000001)
                        improvingMaxHPLevel = c.getPlayer().getSkillLevel(improvingMaxHP)
                        maxhp += Randomizer.rand(20, 25)
                        if improvingMaxHPLevel >= 1:
                            maxhp += improvingMaxHP.getEffect(improvingMaxHPLevel).getX()
                    elif (job >= 200 && job <= 232) || GameConstants.isEvan(job):
                        maxhp += Randomizer.rand(10, 20)
                    elif (job >= 300 && job <= 322) || (job >= 400 && job <= 434) || (job >= 1300 && job <= 1312) || (job >= 1400 && job <= 1412) || (job >= 3300 && job <= 3312):
                        maxhp += Randomizer.rand(16, 20)
                    elif (job >= 500 && job <= 522) || (job >= 3500 && job <= 3512):
                        improvingMaxHP = SkillFactory.getSkill(5100000)
                        improvingMaxHPLevel = c.getPlayer().getSkillLevel(improvingMaxHP)
                        maxhp += Randomizer.rand(18, 22)
                        if improvingMaxHPLevel >= 1:
                            maxhp += improvingMaxHP.getEffect(improvingMaxHPLevel).getY()
                    elif job >= 1500 && job <= 1512:
                        improvingMaxHP = SkillFactory.getSkill(15100000)
                        improvingMaxHPLevel = c.getPlayer().getSkillLevel(improvingMaxHP)
                        maxhp += Randomizer.rand(18, 22)
                        if improvingMaxHPLevel >= 1:
                            maxhp += improvingMaxHP.getEffect(improvingMaxHPLevel).getY()
                    elif job >= 1100 && job <= 1112:
                        improvingMaxHP = SkillFactory.getSkill(11000000)
                        improvingMaxHPLevel = c.getPlayer().getSkillLevel(improvingMaxHP)
                        maxhp += Randomizer.rand(36, 42)
                        if improvingMaxHPLevel >= 1:
                            maxhp += improvingMaxHP.getEffect(improvingMaxHPLevel).getY()
                    elif job >= 1200 && job <= 1212:
                        maxhp += Randomizer.rand(15, 21)
                    elif job >= 2000 && job <= 2112:
                        maxhp += Randomizer.rand(40, 50)
                    else:
                        maxhp += Randomizer.rand(50, 100)
                    maxhp = min(30000, abs(maxhp))
                    chr.setHpApUsed((short)(chr.getHpApUsed() + 1))
                    stat.setMaxHp(maxhp)
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.MAXHP, maxhp))
                    break
                # case 32768:
                    maxmp = stat.getMaxMp()
                    Int = (short)((short)(stat.getInt() / 10) - 10)
                    if Int < 0:
                        Int = 0
                    if chr.getHpApUsed() >= 10000 || stat.getMaxMp() >= 30000:
                        return
                    if job == 0:
                        maxmp += Randomizer.rand(6, 8)
                    elif job >= 100 && job <= 132:
                        maxmp += Randomizer.rand(2, 4)
                    elif (job >= 200 && job <= 232) || GameConstants.isEvan(job) || (job >= 3200 && job <= 3212):
                        improvingMaxMP = SkillFactory.getSkill(2000001)
                        improvingMaxMPLevel = c.getPlayer().getSkillLevel(improvingMaxMP)
                        maxmp += Randomizer.rand(18, 20)
                        if improvingMaxMPLevel >= 1:
                            maxmp += (short)(improvingMaxMP.getEffect(improvingMaxMPLevel).getY() * 2)
                    elif (job >= 300 && job <= 322) || (job >= 400 && job <= 434) || (job >= 500 && job <= 522) || (job >= 3200 && job <= 3212) || (job >= 3500 && job <= 3512) || (job >= 1300 && job <= 1312) || (job >= 1400 && job <= 1412) || (job >= 1500 && job <= 1512):
                        maxmp += Randomizer.rand(10, 12)
                    elif job >= 1100 && job <= 1112:
                        maxmp += Randomizer.rand(6, 9)
                    elif job >= 1200 && job <= 1212:
                        improvingMaxMP = SkillFactory.getSkill(12000000)
                        improvingMaxMPLevel = c.getPlayer().getSkillLevel(improvingMaxMP)
                        maxmp += Randomizer.rand(18, 20)
                        if improvingMaxMPLevel >= 1:
                            maxmp += (short)(improvingMaxMP.getEffect(improvingMaxMPLevel).getY() * 2)
                    elif job >= 2000 && job <= 2112:
                        maxmp += Randomizer.rand(6, 9)
                    else:
                        maxmp += Randomizer.rand(50, 100)
                    maxmp += Int
                    maxmp = min(30000, abs(maxmp))
                    chr.setHpApUsed((short)(chr.getHpApUsed() + 1))
                    stat.setMaxMp(maxmp)
                    statupdate.add(new Pair<MapleStat, Integer>(MapleStat.MAXMP, maxmp))
                    break
                # default:
                    c.getSession().write(MaplePacketCreator.updatePlayerStats(MaplePacketCreator.EMPTY_STATUPDATE, True, chr.getJob()))
                    return
            chr.setRemainingAp((short)(chr.getRemainingAp() - 1))
            statupdate.add(new Pair<MapleStat, Integer>(MapleStat.AVAILABLEAP, chr.getRemainingAp()))
            c.getSession().write(MaplePacketCreator.updatePlayerStats(statupdate, True, chr.getJob()))

    def DistributeSP(self, skillid: int, c: Any, chr: Any) -> None:
        isBeginnerSkill = False
        remainingSp = 0
        # switch (skillid):
            # case 1000:
            # case 1001:
            # case 1002:
                snailsLevel = chr.getSkillLevel(SkillFactory.getSkill(1000))
                recoveryLevel = chr.getSkillLevel(SkillFactory.getSkill(1001))
                nimbleFeetLevel = chr.getSkillLevel(SkillFactory.getSkill(1002))
                remainingSp = min(chr.getLevel() - 1, 6) - snailsLevel - recoveryLevel - nimbleFeetLevel
                isBeginnerSkill = True
                break
            # case 10001000:
            # case 10001001:
            # case 10001002:
                snailsLevel = chr.getSkillLevel(SkillFactory.getSkill(10001000))
                recoveryLevel = chr.getSkillLevel(SkillFactory.getSkill(10001001))
                nimbleFeetLevel = chr.getSkillLevel(SkillFactory.getSkill(10001002))
                remainingSp = min(chr.getLevel() - 1, 6) - snailsLevel - recoveryLevel - nimbleFeetLevel
                isBeginnerSkill = True
                break
            # case 20001000:
            # case 20001001:
            # case 20001002:
                snailsLevel = chr.getSkillLevel(SkillFactory.getSkill(20001000))
                recoveryLevel = chr.getSkillLevel(SkillFactory.getSkill(20001001))
                nimbleFeetLevel = chr.getSkillLevel(SkillFactory.getSkill(20001002))
                remainingSp = min(chr.getLevel() - 1, 6) - snailsLevel - recoveryLevel - nimbleFeetLevel
                isBeginnerSkill = True
                break
            # case 20011000:
            # case 20011001:
            # case 20011002:
                snailsLevel = chr.getSkillLevel(SkillFactory.getSkill(20011000))
                recoveryLevel = chr.getSkillLevel(SkillFactory.getSkill(20011001))
                nimbleFeetLevel = chr.getSkillLevel(SkillFactory.getSkill(20011002))
                remainingSp = min(chr.getLevel() - 1, 6) - snailsLevel - recoveryLevel - nimbleFeetLevel
                isBeginnerSkill = True
                break
            # case 30000002:
            # case 30001000:
            # case 30001001:
                snailsLevel = chr.getSkillLevel(SkillFactory.getSkill(30001000))
                recoveryLevel = chr.getSkillLevel(SkillFactory.getSkill(30001001))
                nimbleFeetLevel = chr.getSkillLevel(SkillFactory.getSkill(30000002))
                remainingSp = min(chr.getLevel() - 1, 9) - snailsLevel - recoveryLevel - nimbleFeetLevel
                isBeginnerSkill = True
                break
            # default:
                remainingSp = chr.getRemainingSp(GameConstants.getSkillBookForSkill(skillid))
                break
        skill = SkillFactory.getSkill(skillid)
        if skill.hasRequiredSkill() && chr.getSkillLevel(SkillFactory.getSkill(skill.getRequiredSkillId())) < skill.getRequiredSkillLevel():
            return
        maxlevel = skill.isFourthJob() ? chr.getMasterLevel(skill) : skill.getMaxLevel()
        curLevel = chr.getSkillLevel(skill)
        if skill.isInvisible() && chr.getSkillLevel(skill) == 0 && ((skill.isFourthJob() && chr.getMasterLevel(skill) == 0) || (!skill.isFourthJob() && maxlevel < 10 && !isBeginnerSkill)):
            return
        for i in GameConstants.blockedSkills:
            if skill.getId() == i:
                chr.dropMessage(1, "你可能不会增加这个技能.")
                return
        if remainingSp > 0 && curLevel + 1 <= maxlevel && (skill.canBeLearnedBy(chr.getJob()) || isBeginnerSkill):
            if !isBeginnerSkill:
                skillbook = GameConstants.getSkillBookForSkill(skillid)
                chr.setRemainingSp(chr.getRemainingSp(skillbook) - 1, skillbook)
            chr.updateSingleStat(MapleStat.AVAILABLESP, chr.getRemainingSp())
            chr.changeSkillLevel(skill, (byte)(curLevel + 1), chr.getMasterLevel(skill))
        else if (!skill.canBeLearnedBy(chr.getJob())) {}

    def AutoAssignAP(self, slea: Any, c: Any, chr: Any) -> None:
        statupdate = []
        c.getSession().write(MaplePacketCreator.updatePlayerStats(statupdate, True, chr.getJob()))
        playerst = chr.getStat()
        slea.readInt()
        count = slea.readInt(), i = 0
        while i < count:
            update = slea.readInt()
            updatenumber = slea.readInt()
            if chr.getRemainingAp() >= updatenumber:
                # switch (update):
                    # case 256:
                        if playerst.getStr() + updatenumber >= 30000:
                            return
                        playerst.setStr((short)(playerst.getStr() + updatenumber))
                        statupdate.add(new Pair<MapleStat, Integer>(MapleStat.STR, playerst.getStr()))
                        break
                    # case 512:
                        if playerst.getDex() + updatenumber >= 30000:
                            return
                        playerst.setDex((short)(playerst.getDex() + updatenumber))
                        statupdate.add(new Pair<MapleStat, Integer>(MapleStat.DEX, playerst.getDex()))
                        break
                    # case 1024:
                        if playerst.getInt() + updatenumber >= 30000:
                            return
                        playerst.setInt((short)(playerst.getInt() + updatenumber))
                        statupdate.add(new Pair<MapleStat, Integer>(MapleStat.INT, playerst.getInt()))
                        break
                    # case 2048:
                        if playerst.getLuk() + updatenumber >= 30000:
                            return
                        playerst.setLuk((short)(playerst.getLuk() + updatenumber))
                        statupdate.add(new Pair<MapleStat, Integer>(MapleStat.LUK, playerst.getLuk()))
                        break
                    # default:
                        c.getSession().write(MaplePacketCreator.updatePlayerStats(MaplePacketCreator.EMPTY_STATUPDATE, True, chr.getJob()))
                        return
                chr.setRemainingAp((short)(chr.getRemainingAp() - updatenumber))
            else:
                StatsHandling.log.info("[h4x] Player {} is distributing AP to {} without having any", chr.getName(), update)
        statupdate.add(new Pair<MapleStat, Integer>(MapleStat.AVAILABLEAP, chr.getRemainingAp()))
        c.getSession().write(MaplePacketCreator.updatePlayerStats(statupdate, True, chr.getJob()))

