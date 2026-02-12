"""
Skill - Converted from Java source
Original: client/Skill.java
Package: client
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.life.Element import *  # TODO: import specific classes


class Skill(ISkill):
    """
    Class Skill
    Implements: ISkill
    """

    def __init__(self, id: int):
        self.name = ""
        self.effects = None
        self.element = None
        self.level = 0
        self.id = None
        self.animationTime = 0
        self.requiredSkill = 0
        self.masterLevel = 0
        self.action = False
        self.invisible = False
        self.chargeskill = False
        self.timeLimited = False
        self.name = ""
        self.effects = []
        self.id = id


    def loadFromData(self, id: int, data: Any) -> Any:
        ret = Skill(id)
        isBuff = False
        skillType = MapleDataTool.getInt("skillType", data, -1)
        elem = MapleDataTool.getString("elemAttr", data, None)
        if elem is not None:
            ret.element = Element.getFromChar(elem[0])
        else:
            ret.element = Element.NEUTRAL
        ret.invisible = (MapleDataTool.getInt("invisible", data, 0) > 0)
        ret.timeLimited = (MapleDataTool.getInt("timeLimited", data, 0) > 0)
        ret.masterLevel = MapleDataTool.getInt("masterLevel", data, 0)
        effect = data.getChildByPath("effect")
        if skillType != -1:
            if skillType == 2:
                isBuff = True
        else:
            action_ = data.getChildByPath("action")
            hit = data.getChildByPath("hit")
            ball = data.getChildByPath("ball")
            action = False
            if action_ is None:
                if data.getChildByPath("prepare/action") is not None:
                    action = True
                else:
                    # switch (id):
                        # case 3101005:
                        # case 4221001:
                        # case 5201001:
                        # case 5221009:
                            action = True
                            break
            else:
                action = True
            ret.action = action
            isBuff = (effect is not None && hit is None && ball is None)
            isBuff |= (action_ is not None && MapleDataTool.getString("0", action_, "") == ("alert2"))
            # switch (id):
                # case 2111002:
                # case 2111003:
                # case 2121001:
                # case 2221001:
                # case 2301002:
                # case 2321001:
                # case 4211001:
                # case 12111005:
                # case 21000000:
                # case 21120006:
                    isBuff = False
                    break
                # case 1004:
                # case 1017:
                # case 1111002:
                # case 1111007:
                # case 1211009:
                # case 1311007:
                # case 1320009:
                # case 4111001:
                # case 4211003:
                # case 5001005:
                # case 5110001:
                # case 5111005:
                # case 5121003:
                # case 5121009:
                # case 5211001:
                # case 5211002:
                # case 5211006:
                # case 5220002:
                # case 5220011:
                # case 9001004:
                # case 10001004:
                # case 10001019:
                # case 13111005:
                # case 15001003:
                # case 15100004:
                # case 15101006:
                # case 15111002:
                # case 15111005:
                # case 15111006:
                # case 20001004:
                # case 20001019:
                # case 21101003:
                    isBuff = True
                    break
        ret.chargeskill = (data.getChildByPath("keydown") is not None)
        for level in data.getChildByPath("level"):
            ret.effects.add(MapleStatEffect.loadSkillEffectFromData(level, id, isBuff, Byte.parseByte(level.getName())))
        reqDataRoot = data.getChildByPath("req")
        if reqDataRoot is not None:
            for reqData in reqDataRoot.getChildren():
                ret.requiredSkill = int(reqData.getName())
                ret.level = MapleDataTool.getInt(reqData, 1)
        ret.animationTime = 0
        if effect is not None:
            for effectEntry in effect:
                skill = ret
                skill.animationTime += MapleDataTool.getIntConvert("delay", effectEntry, 0)
        return ret

    def setName(self, name: str) -> None:
        self.name = name

    def getId(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def getEffect(self, level: int) -> Any:
        if self.effects < level:
            if self.effects > 0:
                return self.effects.get(self.effects - 1)
            return None
        else:
            if level <= 0:
                return self.effects.get(0)
            return self.effects.get(level - 1)

    def getAction(self) -> bool:
        return self.action

    def isChargeSkill(self) -> bool:
        return self.chargeskill

    def isInvisible(self) -> bool:
        return self.invisible

    def hasRequiredSkill(self) -> bool:
        return self.level > 0

    def getRequiredSkillLevel(self) -> int:
        return self.level

    def getRequiredSkillId(self) -> int:
        return self.requiredSkill

    def getMaxLevel(self) -> int:
        return self.effects

    def canBeLearnedBy(self, job: int) -> bool:
        jid = job
        skillForJob = self.id / 10000
        return (skillForJob == 2001 && GameConstants.isEvan(job)) || (jid / 100 == skillForJob / 100 && jid / 1000 == skillForJob / 1000 && (!GameConstants.isAdventurer(skillForJob) || GameConstants.isAdventurer(job)) && (!GameConstants.isKOC(skillForJob) || GameConstants.isKOC(job)) && (!GameConstants.isAran(skillForJob) || GameConstants.isAran(job)) && (!GameConstants.isEvan(skillForJob) || GameConstants.isEvan(job)) && (!GameConstants.isResist(skillForJob) || GameConstants.isResist(job)) && skillForJob / 10 % 10 <= jid / 10 % 10 && skillForJob % 10 <= jid % 10)

    def isTimeLimited(self) -> bool:
        return self.timeLimited

    def isFourthJob(self) -> bool:
        if self.id / 10000 >= 2212 && self.id / 10000 < 3000:
            return self.id / 10000 % 10 >= 7
        if self.id / 10000 >= 430 && self.id / 10000 <= 434:
            return self.id / 10000 % 10 == 4 || self.getMasterLevel() > 0
        return self.id / 10000 % 10 == 2

    def getElement(self) -> Any:
        return self.element

    def getAnimationTime(self) -> int:
        return self.animationTime

    def getMasterLevel(self) -> int:
        return self.masterLevel

    def isBeginnerSkill(self) -> bool:
        jobId = self.id / 10000
        return jobId == 0 || jobId == 1000 || jobId == 2000 || jobId == 2001 || jobId == 3000

