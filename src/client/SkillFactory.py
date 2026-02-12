"""
SkillFactory - Converted from Java source
Original: client/SkillFactory.java
Package: client
"""

from pathlib import Path
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import sys
import threading

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class SkillFactory:
    """
    Class SkillFactory
    """

    # Static initializer
    # skills = {}
    # skillsByJob = new HashMap<Integer, List<Integer>>()
    # SummonSkillInformation = {}
    # stringData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz")).getData("Skill.img")
    # datasource = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Skill.wz"))


    @staticmethod
    def getSkill(id: int) -> Any:
        if SkillFactory.skills != 0:
            return SkillFactory.skills.get(id)
        print("加载 技能完成 :::")
        datasource = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Skill.wz"))
        root = datasource.getRoot()
        for topDir in root.getFiles():
            if topDir.getName() <= 8:
                for data in datasource.getData(topDir.getName()):
                    if data.getName() == ("skill"):
                        for data2 in data:
                            if data2 is not None:
                                skillid = int(data2.getName())
                                skil = Skill.loadFromData(skillid, data2)
                                job = SkillFactory.skillsByJob.get(skillid / 10000)
                                if job is None:
                                    job = []
                                    SkillFactory.skillsByJob.put(skillid / 10000, job)
                                job.add(skillid)
                                skil.setName(getName(skillid))
                                SkillFactory.skills.put(skillid, skil)
                                summon_data = data2.getChildByPath("summon/attack1/info")
                                if summon_data is None:
                                    continue
                                sse = SummonSkillEntry()
                                sse.attackAfter = MapleDataTool.getInt("attackAfter", summon_data, 999999)
                                sse.type = MapleDataTool.getInt("type", summon_data, 0)
                                sse.mobCount = MapleDataTool.getInt("mobCount", summon_data, 1)
                                SkillFactory.SummonSkillInformation.put(skillid, sse)
        return None

    def getSkill1(self, id: int) -> Any:
        ret = SkillFactory.skills.get(id)
        if ret is not None:
            return ret
        with SkillFactory.skills:  # synchronized
            ret = SkillFactory.skills.get(id)
            if ret is None:
                job = id / 10000
                skillroot = SkillFactory.datasource.getData(StringUtil.getLeftPaddedStr(str(job), '0', 3) + ".img")
                skillData = skillroot.getChildByPath("skill/" + StringUtil.getLeftPaddedStr(str(id), '0', 7))
                if skillData is not None:
                    ret = Skill.loadFromData(id, skillData)
                SkillFactory.skills.put(id, ret)
            return ret

    def getSkillsByJob(self, jobId: int) -> list:
        return SkillFactory.skillsByJob.get(jobId)

    def getSkillName(self, id: int) -> str:
        skil = getSkill(id)
        if skil is not None:
            return skil.getName()
        return None

    def getName(self, id: int) -> str:
        strId = Integer.toString(id)
        strId = StringUtil.getLeftPaddedStr(strId, '0', 7)
        skillroot = SkillFactory.stringData.getChildByPath(strId)
        if skillroot is not None:
            return MapleDataTool.getString(skillroot.getChildByPath("name"), "")
        return None

    def getSummonData(self, skillid: int) -> Any:
        return SkillFactory.SummonSkillInformation.get(skillid)

    def getAllSkills(self) -> list:
        return SkillFactory.skills.values()

