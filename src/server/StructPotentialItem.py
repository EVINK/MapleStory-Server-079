"""
StructPotentialItem - Converted from Java source
Original: server/StructPotentialItem.java
Package: server
"""

from typing import Optional, Any


class StructPotentialItem:
    """
    Class StructPotentialItem
    """

    def __init__(self):
        self.incSTR = 0
        self.incDEX = 0
        self.incINT = 0
        self.incLUK = 0
        self.incACC = 0
        self.incEVA = 0
        self.incSpeed = 0
        self.incJump = 0
        self.incPAD = 0
        self.incMAD = 0
        self.incPDD = 0
        self.incMDD = 0
        self.prop = 0
        self.time = 0
        self.incSTRr = 0
        self.incDEXr = 0
        self.incINTr = 0
        self.incLUKr = 0
        self.incMHPr = 0
        self.incMMPr = 0
        self.incACCr = 0
        self.incEVAr = 0
        self.incPADr = 0
        self.incMADr = 0
        self.incPDDr = 0
        self.incMDDr = 0
        self.incCr = 0
        self.incDAMr = 0
        self.RecoveryHP = 0
        self.RecoveryMP = 0
        self.HP = 0
        self.MP = 0
        self.level = 0
        self.ignoreTargetDEF = 0
        self.ignoreDAM = 0
        self.DAMreflect = 0
        self.mpconReduce = 0
        self.mpRestore = 0
        self.incMesoProp = 0
        self.incRewardProp = 0


    def toString(self) -> str:
        ret = ""
        if self.incMesoProp > 0:
            ret.append("Gives MESO(not coded): ")
            ret.append(self.incMesoProp)
            ret.append(" ")
        if self.incRewardProp > 0:
            ret.append("Gives ITEM(not coded): ")
            ret.append(self.incRewardProp)
            ret.append(" ")
        if self.prop > 0:
            ret.append("Probability(not coded): ")
            ret.append(self.prop)
            ret.append(" ")
        if self.time > 0:
            ret.append("Duration(not coded): ")
            ret.append(self.time)
            ret.append(" ")
        if self.attackType > 0:
            ret.append("Attack Type(not coded): ")
            ret.append(self.attackType)
            ret.append(" ")
        if self.incAllskill > 0:
            ret.append("Gives ALL SKILLS: ")
            ret.append(self.incAllskill)
            ret.append(" ")
        if self.skillID > 0:
            ret.append("Gives SKILL: ")
            ret.append(self.skillID)
            ret.append(" ")
        if self.boss:
            ret.append("BOSS ONLY, ")
        if self.face > 0:
            ret.append("Face Expression: ")
            ret.append(self.face)
            ret.append(" ")
        if self.RecoveryUP > 0:
            ret.append("Gives Recovery % on potions: ")
            ret.append(self.RecoveryUP)
            ret.append(" ")
        if self.DAMreflect > 0:
            ret.append("Reflects Damage when Hit: ")
            ret.append(self.DAMreflect)
            ret.append(" ")
        if self.mpconReduce > 0:
            ret.append("Reduces MP Needed for skills: ")
            ret.append(self.mpconReduce)
            ret.append(" ")
        if self.ignoreTargetDEF > 0:
            ret.append("Ignores Monster DEF %: ")
            ret.append(self.ignoreTargetDEF)
            ret.append(" ")
        if self.RecoveryHP > 0:
            ret.append("Recovers HP: ")
            ret.append(self.RecoveryHP)
            ret.append(" ")
        if self.RecoveryMP > 0:
            ret.append("Recovers MP: ")
            ret.append(self.RecoveryMP)
            ret.append(" ")
        if self.HP > 0:
            ret.append("Recovers HP: ")
            ret.append(self.HP)
            ret.append(" ")
        if self.MP > 0:
            ret.append("Recovers MP: ")
            ret.append(self.MP)
            ret.append(" ")
        if self.mpRestore > 0:
            ret.append("Recovers MP: ")
            ret.append(self.mpRestore)
            ret.append(" ")
        if self.ignoreDAM > 0:
            ret.append("Ignores Monster Damage: ")
            ret.append(self.ignoreDAM)
            ret.append(" ")
        if self.ignoreDAMr > 0:
            ret.append("Ignores Monster Damage %: ")
            ret.append(self.ignoreDAMr)
            ret.append(" ")
        if self.incMHP > 0:
            ret.append("Gives HP: ")
            ret.append(self.incMHP)
            ret.append(" ")
        if self.incMMP > 0:
            ret.append("Gives MP: ")
            ret.append(self.incMMP)
            ret.append(" ")
        if self.incMHPr > 0:
            ret.append("Gives HP %: ")
            ret.append(self.incMHPr)
            ret.append(" ")
        if self.incMMPr > 0:
            ret.append("Gives MP %: ")
            ret.append(self.incMMPr)
            ret.append(" ")
        if self.incSTR > 0:
            ret.append("Gives STR: ")
            ret.append(self.incSTR)
            ret.append(" ")
        if self.incDEX > 0:
            ret.append("Gives DEX: ")
            ret.append(self.incDEX)
            ret.append(" ")
        if self.incINT > 0:
            ret.append("Gives INT: ")
            ret.append(self.incINT)
            ret.append(" ")
        if self.incLUK > 0:
            ret.append("Gives LUK: ")
            ret.append(self.incLUK)
            ret.append(" ")
        if self.incACC > 0:
            ret.append("Gives ACC: ")
            ret.append(self.incACC)
            ret.append(" ")
        if self.incEVA > 0:
            ret.append("Gives EVA: ")
            ret.append(self.incEVA)
            ret.append(" ")
        if self.incSpeed > 0:
            ret.append("Gives Speed: ")
            ret.append(self.incSpeed)
            ret.append(" ")
        if self.incJump > 0:
            ret.append("Gives Jump: ")
            ret.append(self.incJump)
            ret.append(" ")
        if self.incPAD > 0:
            ret.append("Gives Attack: ")
            ret.append(self.incPAD)
            ret.append(" ")
        if self.incMAD > 0:
            ret.append("Gives Magic Attack: ")
            ret.append(self.incMAD)
            ret.append(" ")
        if self.incPDD > 0:
            ret.append("Gives Defense: ")
            ret.append(self.incPDD)
            ret.append(" ")
        if self.incMDD > 0:
            ret.append("Gives Magic Defense: ")
            ret.append(self.incMDD)
            ret.append(" ")
        if self.incSTRr > 0:
            ret.append("Gives STR %: ")
            ret.append(self.incSTRr)
            ret.append(" ")
        if self.incDEXr > 0:
            ret.append("Gives DEX %: ")
            ret.append(self.incDEXr)
            ret.append(" ")
        if self.incINTr > 0:
            ret.append("Gives INT %: ")
            ret.append(self.incINTr)
            ret.append(" ")
        if self.incLUKr > 0:
            ret.append("Gives LUK %: ")
            ret.append(self.incLUKr)
            ret.append(" ")
        if self.incACCr > 0:
            ret.append("Gives ACC %: ")
            ret.append(self.incACCr)
            ret.append(" ")
        if self.incEVAr > 0:
            ret.append("Gives EVA %: ")
            ret.append(self.incEVAr)
            ret.append(" ")
        if self.incPADr > 0:
            ret.append("Gives Attack %: ")
            ret.append(self.incPADr)
            ret.append(" ")
        if self.incMADr > 0:
            ret.append("Gives Magic Attack %: ")
            ret.append(self.incMADr)
            ret.append(" ")
        if self.incPDDr > 0:
            ret.append("Gives Defense %: ")
            ret.append(self.incPDDr)
            ret.append(" ")
        if self.incMDDr > 0:
            ret.append("Gives Magic Defense %: ")
            ret.append(self.incMDDr)
            ret.append(" ")
        if self.incCr > 0:
            ret.append("Gives Critical %: ")
            ret.append(self.incCr)
            ret.append(" ")
        if self.incDAMr > 0:
            ret.append("Gives Total Damage %: ")
            ret.append(self.incDAMr)
            ret.append(" ")
        if self.level > 0:
            ret.append("Level: ")
            ret.append(self.level)
            ret.append(" ")
        return ret

