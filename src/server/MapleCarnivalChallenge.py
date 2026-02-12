"""
MapleCarnivalChallenge - Converted from Java source
Original: server/MapleCarnivalChallenge.java
Package: server
"""

from typing import Optional, Any
from weakref import ref
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes


class MapleCarnivalChallenge:
    """
    Class MapleCarnivalChallenge
    """

    def __init__(self, challenger: Any):
        self.challengeinfo = ""
        self.challenger = new WeakReference<MapleCharacter>(challenger)
        self.challengeinfo += "#b"
        for pc in challenger.getParty().getMembers():
            c = challenger.getMap().getCharacterById(pc.getId())
            if c is not None:
                self.challengeinfo = self.challengeinfo + "名称：" + c.getName() + " / 等級" + c.getLevel() + " / 职业：" + getJobNameById(c.getJob()) + "\r\n"
        self.challengeinfo += "#k"


    def getJobNameById(self, job: int) -> str:
        # switch (job):
            # case 0:
                return "新手"
            # case 1000:
                return "初心者"
            # case 2000:
                return "战神"
            # case 100:
                return "战士"
            # case 110:
                return "剑客"
            # case 111:
                return "勇士"
            # case 112:
                return "英雄"
            # case 120:
                return "准骑士"
            # case 121:
                return "骑士"
            # case 122:
                return "圣骑士"
            # case 130:
                return "枪战士"
            # case 131:
                return "龙骑士"
            # case 132:
                return "黑骑士"
            # case 200:
                return "魔法师"
            # case 210:
                return "法师(火,毒)"
            # case 211:
                return "巫师(火,毒)"
            # case 212:
                return "魔导师(火,毒)"
            # case 220:
                return "法师(雷,冰)"
            # case 221:
                return "巫师(雷,冰)"
            # case 222:
                return "魔导师(雷,冰)"
            # case 230:
                return "牧师"
            # case 231:
                return "祭司"
            # case 232:
                return "主教"
            # case 300:
                return "弓箭手"
            # case 310:
                return "猎手"
            # case 311:
                return "射手"
            # case 312:
                return "神射手"
            # case 320:
                return "弩弓手"
            # case 321:
                return "游侠"
            # case 322:
                return "箭神"
            # case 400:
                return "飞侠"
            # case 410:
                return "刺客"
            # case 411:
                return "无影人"
            # case 412:
                return "隐士"
            # case 420:
                return "侠客"
            # case 421:
                return "独行客"
            # case 422:
                return "侠盗"
            # case 500:
                return "海盜"
            # case 510:
                return "拳手"
            # case 511:
                return "斗士"
            # case 512:
                return "冲锋队长"
            # case 520:
                return "火枪手"
            # case 521:
                return "大副"
            # case 522:
                return "船长"
            # case 1100:
                return "魂骑士1转"
            # case 1110:
                return "魂骑士2转"
            # case 1111:
                return "魂骑士3转"
            # case 1112:
                return "魂骑士4转"
            # case 1200:
                return "炎术士1转"
            # case 1210:
                return "炎术士2转"
            # case 1211:
                return "炎术士3转"
            # case 1212:
                return "炎术士4转"
            # case 1300:
                return "风灵使者1转"
            # case 1310:
                return "风灵使者2转"
            # case 1311:
                return "风灵使者3转"
            # case 1312:
                return "风灵使者4转"
            # case 1400:
                return "夜行者1转"
            # case 1410:
                return "夜行者2转"
            # case 1411:
                return "夜行者3转"
            # case 1412:
                return "夜行者4转"
            # case 1500:
                return "奇袭者1转"
            # case 1510:
                return "奇袭者2转"
            # case 1511:
                return "奇袭者3转"
            # case 1512:
                return "奇袭者4转"
            # case 2100:
                return "战神1转"
            # case 2110:
                return "战神2转"
            # case 2111:
                return "战神3转"
            # case 2112:
                return "战神4转"
            # default:
                return "未知的职业"

    def getJobBasicNameById(self, job: int) -> str:
        # switch (job):
            # case 0:
                return "新手"
            # case 1000:
                return "初心者"
            # case 2000:
                return "战神"
            # case 100:
                return "战士"
            # case 110:
                return "剑客"
            # case 111:
                return "勇士"
            # case 112:
                return "英雄"
            # case 120:
                return "准骑士"
            # case 121:
                return "骑士"
            # case 122:
                return "圣骑士"
            # case 130:
                return "枪战士"
            # case 131:
                return "龙骑士"
            # case 132:
                return "黑骑士"
            # case 200:
                return "魔法师"
            # case 210:
                return "法师(火,毒)"
            # case 211:
                return "巫师(火,毒)"
            # case 212:
                return "魔导师(火,毒)"
            # case 220:
                return "法师(雷,冰)"
            # case 221:
                return "巫师(雷,冰)"
            # case 222:
                return "魔导师(雷,冰)"
            # case 230:
                return "牧师"
            # case 231:
                return "祭司"
            # case 232:
                return "主教"
            # case 300:
                return "弓箭手"
            # case 310:
                return "猎手"
            # case 311:
                return "射手"
            # case 312:
                return "神射手"
            # case 320:
                return "弩弓手"
            # case 321:
                return "游侠"
            # case 322:
                return "箭神"
            # case 400:
                return "飞侠"
            # case 410:
                return "刺客"
            # case 411:
                return "无影人"
            # case 412:
                return "隐士"
            # case 420:
                return "侠客"
            # case 421:
                return "独行客"
            # case 422:
                return "侠盗"
            # case 500:
                return "海盜"
            # case 510:
                return "拳手"
            # case 511:
                return "斗士"
            # case 512:
                return "冲锋队长"
            # case 520:
                return "火枪手"
            # case 521:
                return "大副"
            # case 522:
                return "船长"
            # case 1100:
                return "魂骑士1转"
            # case 1110:
                return "魂骑士2转"
            # case 1111:
                return "魂骑士3转"
            # case 1112:
                return "魂骑士4转"
            # case 1200:
                return "炎术士1转"
            # case 1210:
                return "炎术士2转"
            # case 1211:
                return "炎术士3转"
            # case 1212:
                return "炎术士4转"
            # case 1300:
                return "风灵使者1转"
            # case 1310:
                return "风灵使者2转"
            # case 1311:
                return "风灵使者3转"
            # case 1312:
                return "风灵使者4转"
            # case 1400:
                return "夜行者1转"
            # case 1410:
                return "夜行者2转"
            # case 1411:
                return "夜行者3转"
            # case 1412:
                return "夜行者4转"
            # case 1500:
                return "奇袭者1转"
            # case 1510:
                return "奇袭者2转"
            # case 1511:
                return "奇袭者3转"
            # case 1512:
                return "奇袭者4转"
            # case 2100:
                return "战神1转"
            # case 2110:
                return "战神2转"
            # case 2111:
                return "战神3转"
            # case 2112:
                return "战神4转"
            # default:
                return "未知的职业"

    def getChallenger(self) -> Any:
        return self.challenger.get()

    def getChallengeInfo(self) -> str:
        return self.challengeinfo

