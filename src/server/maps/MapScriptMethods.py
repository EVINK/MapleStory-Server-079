"""
MapScriptMethods - Converted from Java source
Original: server/maps/MapScriptMethods.java
Package: server.maps
"""

from enum import Enum, IntEnum
from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from scripting.EventManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.OverrideMonsterStats import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.UIPacket import *  # TODO: import specific classes


class MapScriptMethods:
    """
    Class MapScriptMethods
    """

    # Static initializer
    # witchTowerPos = Point(-60, 184)
    # mulungEffects = new String[] { "我一直在等你! 如果你有一点勇气,你就马上走进去!", "你勇敢的接受了武陵塔的挑战!勇气可嘉！", "我会保证你会后悔进入武陵道场训练塔的", "我真的很喜欢你的勇气，但希望不是鲁莽！", "如果你不想走上失败的道理，就要这么做！" }


    @staticmethod
    def startScript_FirstUser(c: Any, scriptName: str) -> None:
        if c.getPlayer() is None:
            return
        # switch (scriptName):
            # case "summon_pepeking":
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/frame/W"))
                if c.getPlayer().getMap().getAllMonster() == 0:
                    rand = Randomizer.rand(0, 2)
                    mob = MapleLifeFactory.getMonster(3300005 + rand)
                    oms = OverrideMonsterStats()
                    oms.setOExp(7110)
                    oms.setOHp(mob.getMobMaxHp())
                    oms.setOMp(mob.getMobMaxMp())
                    mob.setOverrideStats(oms)
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, Point(358, -68))
                    # switch (rand):
                        # case 0:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeB"))
                            break
                        # case 1:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeG"))
                            break
                        # case 2:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeW"))
                            break
                else:
                    c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeB"))
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/chat/nugu"))
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/frame/B"))
                break
        # switch (onFirstUserEnter.fromString(scriptName)):
            # case pepeking_effect:
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/frame/W"))
                if c.getPlayer().getMap().getAllMonster() == 0:
                    rand2 = Randomizer.rand(0, 2)
                    mob2 = MapleLifeFactory.getMonster(3300005 + rand2)
                    oms2 = OverrideMonsterStats()
                    oms2.setOExp(7110)
                    oms2.setOHp(mob2.getMobMaxHp())
                    oms2.setOMp(mob2.getMobMaxMp())
                    mob2.setOverrideStats(oms2)
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob2, Point(358, -68))
                    # switch (rand2):
                        # case 0:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeB"))
                            break
                        # case 1:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeG"))
                            break
                        # case 2:
                            c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeW"))
                            break
                else:
                    c.sendPacket(MaplePacketCreator.showEffect("pepeKing/pepe/pepeB"))
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/chat/nugu"))
                c.sendPacket(MaplePacketCreator.showEffect("pepeKing/frame/B"))
                break
            # case dojang_Eff:
                temp = (c.getPlayer().getMapId() - 925000000) / 100
                stage = temp - temp / 100 * 100
                sendDojoClock(c, getTiming(stage) * 60)
                sendDojoStart(c, stage - getDojoStageDec(stage))
                break
            # case PinkBeen_before:
                handlePinkBeanStart(c)
                break
            # case onRewordMap:
                reloadWitchTower(c)
                break
            # case GhostF:
                c.getPlayer().getMap().startMapEffect("这个地图感觉阴森森的..有种莫名的奇怪感觉..", 5120025)
                break
            # case moonrabbit_mapEnter:
                c.getPlayer().getMap().startMapEffect("粥环绕月球的月见草种子和保护月球兔子！", 5120016)
                break
            # case StageMsg_together:
                # switch (c.getPlayer().getMapId()):
                    # case 103000800:
                        c.getPlayer().getMap().startMapEffect("解决问题并收集通行证的数量!", 5120017)
                        break
                    # case 103000801:
                        c.getPlayer().getMap().startMapEffect("上绳索，揭开正确的组合!", 5120017)
                        break
                    # case 103000802:
                        c.getPlayer().getMap().startMapEffect("在平台上推出正确的组合!", 5120017)
                        break
                    # case 103000803:
                        c.getPlayer().getMap().startMapEffect("在桶上，揭开正确的组合!", 5120017)
                        break
                    # case 103000804:
                        c.getPlayer().getMap().startMapEffect("打败绿水灵王和他的爪牙!", 5120017)
                        break
                break
            # case StageMsg_romio:
                # switch (c.getPlayer().getMapId()):
                    # case 926100000:
                        c.getPlayer().getMap().startMapEffect("请找到隐藏的门，通过调查实验室！", 5120021)
                        break
                    # case 926100001:
                        c.getPlayer().getMap().startMapEffect("找到你的方式通过这黑暗！", 5120021)
                        break
                    # case 926100100:
                        c.getPlayer().getMap().startMapEffect("充满能量的烧杯！", 5120021)
                        break
                    # case 926100200:
                        c.getPlayer().getMap().startMapEffect("获取实验的文件通过每个门！", 5120021)
                        break
                    # case 926100203:
                        c.getPlayer().getMap().startMapEffect("请打败所有的怪物！", 5120021)
                        break
                    # case 926100300:
                        c.getPlayer().getMap().startMapEffect("找到你的方法通过实验室！", 5120021)
                        break
                    # case 926100401:
                        c.getPlayer().getMap().startMapEffect("请保护我的爱人！", 5120021)
                        break
                break
            # case StageMsg_juliet:
                # switch (c.getPlayer().getMapId()):
                    # case 926110000:
                        c.getPlayer().getMap().startMapEffect("请找到隐藏的门，通过调查实验室！", 5120022)
                        break
                    # case 926110001:
                        c.getPlayer().getMap().startMapEffect("找到你的方式通过这黑暗！", 5120022)
                        break
                    # case 926110100:
                        c.getPlayer().getMap().startMapEffect("充满能量的烧杯！", 5120022)
                        break
                    # case 926110200:
                        c.getPlayer().getMap().startMapEffect("获取实验的文件通过每个门！", 5120022)
                        break
                    # case 926110203:
                        c.getPlayer().getMap().startMapEffect("请打败所有的怪物！", 5120022)
                        break
                    # case 926110300:
                        c.getPlayer().getMap().startMapEffect("找到你的方法通过实验室！", 5120022)
                        break
                    # case 926110401:
                        c.getPlayer().getMap().startMapEffect("请保护我的爱人！", 5120022)
                        break
                break
            # case party6weatherMsg:
                # switch (c.getPlayer().getMapId()):
                    # case 930000000:
                        c.getPlayer().getMap().startMapEffect("进入传送点，我要对你们施放变身魔法了！", 5120023)
                        break
                    # case 930000100:
                        c.getPlayer().getMap().startMapEffect("消灭所有怪物！", 5120023)
                        break
                    # case 930000200:
                        c.getPlayer().getMap().startMapEffect("对荆棘施放稀释的毒液4个！", 5120023)
                        break
                    # case 930000300:
                        c.getPlayer().getMap().startMapEffect("妈妈你在哪里呜呜哭哭喔我迷路了", 5120023)
                        break
                    # case 930000400:
                        c.getPlayer().getMap().startMapEffect("找我对话拿净化之珠其中一个队员集满10个怪物珠给我！", 5120023)
                        break
                    # case 930000500:
                        c.getPlayer().getMap().startMapEffect("从怪人书桌中寻找紫色魔力石！！", 5120023)
                        break
                    # case 930000600:
                        c.getPlayer().getMap().startMapEffect("将紫色魔力石放在祭坛上！", 5120023)
                        break
                break
            # case StageMsg_davy:
                # switch (c.getPlayer().getMapId()):
                    # case 925100000:
                        c.getPlayer().getMap().startMapEffect("击败外的怪物的船舶推进!", 5120020)
                        break
                    # case 925100100:
                        c.getPlayer().getMap().startMapEffect("我们必须证明自己！给我海盗勋章!", 5120020)
                        break
                    # case 925100200:
                        c.getPlayer().getMap().startMapEffect("在这里击败守卫!", 5120020)
                        break
                    # case 925100300:
                        c.getPlayer().getMap().startMapEffect("消灭这里的守卫!", 5120020)
                        break
                    # case 925100400:
                        c.getPlayer().getMap().startMapEffect("锁上门！密封船舶动力的根!", 5120020)
                        break
                    # case 925100500:
                        c.getPlayer().getMap().startMapEffect("主，消灭海盗!", 5120020)
                        break
                em = c.getChannelServer().getEventSM().getEventManager("Pirate")
                if c.getPlayer().getMapId() == 925100500 && em is not None && em.getProperty("stage5") is not None:
                    mobId = Randomizer.nextBoolean() ? 9300119 : 9300119
                    st = int(em.getProperty("stage5"))
                    # switch (st):
                        # case 1:
                            mobId = 9300105
                            break
                        # case 2:
                            mobId = 9300106
                            break
                    shammos = MapleLifeFactory.getMonster(mobId)
                    if c.getPlayer().getEventInstance() is not None:
                        c.getPlayer().getEventInstance().registerMonster(shammos)
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(shammos, Point(411, 236))
                    break
                break
            # case astaroth_summon:
                c.getPlayer().getMap().resetFully()
                c.getPlayer().getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(9400633), Point(600, -26))
                break
            # case boss_Ravana:
                c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(5, "那已经出现!"))
                break
            # case killing_BonusSetting:
                c.getPlayer().getMap().resetFully()
                c.getSession().write(MaplePacketCreator.showEffect("killing/bonus/bonus"))
                c.getSession().write(MaplePacketCreator.showEffect("killing/bonus/stage"))
                pos1 = None
                pos2 = None
                pos3 = None
                spawnPer = 0
                mobId2 = 0
                if c.getPlayer().getMapId() >= 910320010 && c.getPlayer().getMapId() <= 910320029:
                    pos1 = Point(121, 218)
                    pos2 = Point(396, 43)
                    pos3 = Point(-63, 43)
                    mobId2 = 9700020
                    spawnPer = 10
                elif c.getPlayer().getMapId() >= 926010010 && c.getPlayer().getMapId() <= 926010029:
                    pos1 = Point(0, 88)
                    pos2 = Point(-326, -115)
                    pos3 = Point(361, -115)
                    mobId2 = 9700019
                    spawnPer = 10
                elif c.getPlayer().getMapId() >= 926010030 && c.getPlayer().getMapId() <= 926010049:
                    pos1 = Point(0, 88)
                    pos2 = Point(-326, -115)
                    pos3 = Point(361, -115)
                    mobId2 = 9700019
                    spawnPer = 15
                elif c.getPlayer().getMapId() >= 926010050 && c.getPlayer().getMapId() <= 926010069:
                    pos1 = Point(0, 88)
                    pos2 = Point(-326, -115)
                    pos3 = Point(361, -115)
                    mobId2 = 9700019
                    spawnPer = 20
                else:
                    if c.getPlayer().getMapId() < 926010070 || c.getPlayer().getMapId() > 926010089:
                        break
                    pos1 = Point(0, 88)
                    pos2 = Point(-326, -115)
                    pos3 = Point(361, -115)
                    mobId2 = 9700029
                    spawnPer = 20
                for i in range(spawnPer):
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(mobId2), Point(pos1))
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(mobId2), Point(pos2))
                    c.getPlayer().getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(mobId2), Point(pos3))
                c.getPlayer().startMapTimeLimitTask(120, c.getPlayer().getMap().getReturnMap())
                break
            # case shammos_Fenter:
                if c.getPlayer().getMapId() >= 921120100 && c.getPlayer().getMapId() < 921120500:
                    shammos2 = MapleLifeFactory.getMonster(9300275)
                    if c.getPlayer().getEventInstance() is not None:
                        c.getPlayer().getEventInstance().registerMonster(shammos2)
                        if c.getPlayer().getEventInstance().getProperty("HP") is not None:
                            shammos2.setHp(int(c.getPlayer().getEventInstance().getProperty("HP")))
                        else:
                            c.getPlayer().getEventInstance().setProperty("HP", "50000")
                    c.getPlayer().getMap().spawnMonsterWithEffectBelow(shammos2, Point(c.getPlayer().getMap().getPortal(0).getPosition()), 12)
                    shammos2.switchController(c.getPlayer(), False)
                    break
                break
            # case PRaid_D_Fenter:
                # switch (c.getPlayer().getMapId() % 10):
                    # case 0:
                        c.getPlayer().getMap().startMapEffect("消灭所有的怪物!", 5120033)
                        break
                    # case 1:
                        c.getPlayer().getMap().startMapEffect("打破盒子，消灭怪物!", 5120033)
                        break
                    # case 2:
                        c.getPlayer().getMap().startMapEffect("消除!", 5120033)
                        break
                    # case 3:
                        c.getPlayer().getMap().startMapEffect("消灭所有的怪物!", 5120033)
                        break
                    # case 4:
                        c.getPlayer().getMap().startMapEffect("找到另一边的路!", 5120033)
                        break
                break
            # case PRaid_B_Fenter:
                c.getPlayer().getMap().startMapEffect("打败幽灵船船长!", 5120033)
            # case metro_firstSetting:
            # case killing_MapSetting:
            # case Sky_TrapFEnter:
            # case balog_bonusSetting:
                c.getPlayer().getMap().resetFully()
                break

    def startScript_User(self, c: Any, scriptName: str) -> None:
        if c.getPlayer() is None:
            return
        data = ""
        # switch (scriptName):
            # case "103000804":
                if (c.getPlayer().getParty() is None || c.getPlayer().getParty().getLeader().getId() == c.getPlayer().getId()) {}
                break
        # switch (onUserEnter.fromString(scriptName)):
            # case cygnusTest:
            # case cygnusJobTutorial:
                showIntro2(c, "Effect/Direction.img/cygnusJobTutorial/Scene" + (c.getPlayer().getMapId() - 913040100))
                break
            # case shammos_Enter:
                if c.getPlayer().getEventInstance() is not None && c.getPlayer().getMapId() == 921120500:
                    NPCScriptManager.getInstance().dispose(c)
                    NPCScriptManager.getInstance().start(c, 2022006)
                    break
                break
            # case start_itemTake:
                em = c.getChannelServer().getEventSM().getEventManager("OrbisPQ")
                if em is not None && em.getProperty("pre") == ("0"):
                    NPCScriptManager.getInstance().dispose(c)
                    break
                break
            # case PRaid_D_Enter:
            # case PRaid_B_Enter:
            # case PRaid_WinEnter:
            # case PRaid_FailEnter:
            # case PRaid_Revive:
            # case metro_firstSetting:
            # case blackSDI:
            # case summonIceWall:
            # case onSDI:
            # case enterBlackfrog:
            # case Sky_Quest:
            # case dollCave00:
            # case dollCave01:
            # case shammos_Base:
            # case shammos_Result:
            # case Sky_BossEnter:
            # case Sky_GateMapEnter:
            # case balog_dateSet:
            # case balog_buff:
            # case outCase:
            # case Sky_StageEnter:
            # case dojang_QcheckSet:
            # case evanTogether:
            # case aranTutorAlone:
            # case Ghost:
                c.getPlayer().getMap().startMapEffect("这个地图感觉阴森森的..有一种莫名的奇怪感觉..", 5120025)
                break
            # case evanAlone:
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case startEreb:
            # case mirrorCave:
            # case babyPigMap:
            # case evanleaveD:
                c.getSession().write(UIPacket.IntroDisableUI(False))
                c.getSession().write(UIPacket.IntroLock(False))
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case dojang_Msg:
                c.getPlayer().getMap().startMapEffect(MapScriptMethods.mulungEffects[Randomizer.nextInt(MapScriptMethods.len(mulungEffects))], 5120024)
                break
            # case dojang_1st:
                c.getPlayer().writeMulungEnergy()
                break
            # case undomorphdarco:
            # case reundodraco:
                c.getPlayer().cancelEffect(MapleItemInformationProvider.getInstance().getItemEffect(2210016), False, -1)
                break
            # case goAdventure:
                showIntro2(c, "Effect/Direction3.img/goAdventure/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case crash_Dragon:
                showIntro2(c, "Effect/Direction4.img/crash/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case getDragonEgg:
                showIntro2(c, "Effect/Direction4.img/getDragonEgg/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case meetWithDragon:
                showIntro2(c, "Effect/Direction4.img/meetWithDragon/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case PromiseDragon:
                showIntro2(c, "Effect/Direction4.img/PromiseDragon/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case evanPromotion:
                # switch (c.getPlayer().getMapId()):
                    # case 900090000:
                        data = "Effect/Direction4.img/promotion/Scene0" + ((c.getPlayer().getGender() == 0) ? "0" : "1")
                        break
                    # case 900090001:
                        data = "Effect/Direction4.img/promotion/Scene1"
                        break
                    # case 900090002:
                        data = "Effect/Direction4.img/promotion/Scene2" + ((c.getPlayer().getGender() == 0) ? "0" : "1")
                        break
                    # case 900090003:
                        data = "Effect/Direction4.img/promotion/Scene3"
                        break
                    # case 900090004:
                        c.getSession().write(UIPacket.IntroDisableUI(False))
                        c.getSession().write(UIPacket.IntroLock(False))
                        c.getSession().write(MaplePacketCreator.enableActions())
                        mapto = c.getChannelServer().getMapFactory().getMap(900010000)
                        c.getPlayer().changeMap(mapto, mapto.getPortal(0))
                        return
                showIntro2(c, data)
                break
            # case TD_MC_title:
                c.getSession().write(UIPacket.IntroDisableUI(False))
                c.getSession().write(UIPacket.IntroLock(False))
                c.getSession().write(MaplePacketCreator.enableActions())
                c.getSession().write(UIPacket.MapEff("temaD/enter/mushCatle"))
                break
            # case explorationPoint:
                if c.getPlayer().getMapId() == 104000000:
                    c.getSession().write(UIPacket.IntroDisableUI(False))
                    c.getSession().write(UIPacket.IntroLock(False))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    c.getSession().write(UIPacket.MapNameDisplay(c.getPlayer().getMapId()))
                MapleQuest.MedalQuest m = None
                for (final MapleQuest.MedalQuest mq : MapleQuest.MedalQuest.values())
                    for i in mq.maps:
                        if c.getPlayer().getMapId() == i:
                            m = mq
                            break
                if m is not None && c.getPlayer().getLevel() >= m.level && c.getPlayer().getQuestStatus(m.questid) != 2:
                    if c.getPlayer().getQuestStatus(m.lquestid) != 1:
                        MapleQuest.getInstance(m.lquestid).forceStart(c.getPlayer(), 0, "0")
                    if c.getPlayer().getQuestStatus(m.questid) != 1:
                        MapleQuest.getInstance(m.questid).forceStart(c.getPlayer(), 0, None)
                        sb = ""
                        for j in range(m.len(maps)):
                            sb.append("0")
                        c.getPlayer().updateInfoQuest(m.questid - 2005, sb)
                        MapleQuest.getInstance(m.questid - 1995).forceStart(c.getPlayer(), 0, "0")
                    quest = c.getPlayer().getInfoQuest(m.questid - 2005)
                    stat = c.getPlayer().getQuestNAdd(MapleQuest.getInstance(m.questid - 1995))
                    if stat.getCustomData() is None:
                        stat.setCustomData("0")
                    number = int(stat.getCustomData())
                    sb2 = ""
                    changedd = False
                    for k in range(m.len(maps)):
                        changed = False
                        try:
                            if c.getPlayer().getMapId() == m.maps[k] && quest[k + 6:k + 7] == ("0"):
                                sb2.append("1")
                                changed = True
                                changedd = True
                            if !changed:
                                sb2.append(quest[k + 6:k + 7])
                        catch (Exception ex) {}
                    if changedd:
                        number += 1
                        c.getPlayer().updateInfoQuest(m.questid - 2005, sb2)
                        MapleQuest.getInstance(m.questid - 1995).forceStart(c.getPlayer(), 0, str(number))
                        c.getPlayer().dropMessage(5, "访问 " + number + "/" + m.len(maps) + " 个地区.")
                        c.getPlayer().dropMessage(5, "称号 " + str(m) + " 已完成了")
                        c.getSession().write(MaplePacketCreator.showQuestMsg("称号 " + str(m) + " 已完成访问 " + number + "/" + m.len(maps) + " 个地区"))
                    break
                break
            # case go10000:
            # case go20000:
            # case go30000:
            # case go40000:
            # case go50000:
            # case go1000000:
            # case go1020000:
            # case go104000000:
                c.getSession().write(UIPacket.IntroDisableUI(False))
                c.getSession().write(UIPacket.IntroLock(False))
            # case go2000000:
            # case go1010000:
            # case go1010100:
            # case go1010200:
            # case go1010300:
            # case go1010400:
                c.getSession().write(UIPacket.MapNameDisplay(c.getPlayer().getMapId()))
                break
            # case goArcher:
                showIntro2(c, "Effect/Direction3.img/archer/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case goPirate:
                showIntro2(c, "Effect/Direction3.img/pirate/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case goRogue:
                showIntro2(c, "Effect/Direction3.img/rogue/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case goMagician:
                showIntro2(c, "Effect/Direction3.img/magician/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case goSwordman:
                showIntro2(c, "Effect/Direction3.img/swordman/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case goLith:
                showIntro2(c, "Effect/Direction3.img/goLith/Scene" + ((c.getPlayer().getGender() == 0) ? "0" : "1"))
                break
            # case TD_MC_Openning:
                showIntro2(c, "Effect/Direction2.img/open")
                break
            # case TD_MC_gasi:
                showIntro2(c, "Effect/Direction2.img/gasi")
                break
            # case aranDirection:
                # switch (c.getPlayer().getMapId()):
                    # case 914090010:
                        data = "Effect/Direction1.img/aranTutorial/Scene0"
                        break
                    # case 914090011:
                        data = "Effect/Direction1.img/aranTutorial/Scene1" + ((c.getPlayer().getGender() == 0) ? "0" : "1")
                        break
                    # case 914090012:
                        data = "Effect/Direction1.img/aranTutorial/Scene2" + ((c.getPlayer().getGender() == 0) ? "0" : "1")
                        break
                    # case 914090013:
                        data = "Effect/Direction1.img/aranTutorial/Scene3"
                        break
                    # case 914090100:
                        data = "Effect/Direction1.img/aranTutorial/HandedPoleArm" + ((c.getPlayer().getGender() == 0) ? "0" : "1")
                        break
                    # case 914090200:
                        data = "Effect/Direction1.img/aranTutorial/Maha"
                        break
                showIntro2(c, data)
                break
            # case iceCave:
                c.getPlayer().changeSkillLevel(SkillFactory.getSkill(20000014), 0, 0)
                c.getPlayer().changeSkillLevel(SkillFactory.getSkill(20000015), 0, 0)
                c.getPlayer().changeSkillLevel(SkillFactory.getSkill(20000016), 0, 0)
                c.getPlayer().changeSkillLevel(SkillFactory.getSkill(20000017), 0, 0)
                c.getPlayer().changeSkillLevel(SkillFactory.getSkill(20000018), 0, 0)
                c.getSession().write(UIPacket.ShowWZEffect("Effect/Direction1.img/aranTutorial/ClickLirin", -1))
                c.getSession().write(UIPacket.IntroDisableUI(False))
                c.getSession().write(UIPacket.IntroLock(False))
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case rienArrow:
                if c.getPlayer().getInfoQuest(21019) == ("miss=o;helper=clear"):
                    c.getPlayer().updateInfoQuest(21019, "miss=o;arr=o;helper=clear")
                    c.getSession().write(UIPacket.AranTutInstructionalBalloon("Effect/OnUserEff.img/guideEffect/aranTutorial/tutorialArrow3"))
                    break
                break
            # case rien:
                if c.getPlayer().getQuestStatus(21101) == 2 && c.getPlayer().getInfoQuest(21019) == ("miss=o;arr=o;helper=clear"):
                    c.getPlayer().updateInfoQuest(21019, "miss=o;arr=o;ck=1;helper=clear")
                c.getSession().write(UIPacket.IntroDisableUI(False))
                c.getSession().write(UIPacket.IntroLock(False))
                break
            # case check_count:
                if c.getPlayer().getMapId() == 950101010 && (!c.getPlayer().haveItem(4001433, 20) || c.getPlayer().getLevel() < 50):
                    mapp = c.getChannelServer().getMapFactory().getMap(950101100)
                    c.getPlayer().changeMap(mapp, mapp.getPortal(0))
                    break
                break
            # case Massacre_first:
                if c.getPlayer().getPyramidSubway() is None:
                    c.getPlayer().setPyramidSubway(Event_PyramidSubway(c.getPlayer()))
                    break
                break
            # case Massacre_result:
                c.getSession().write(MaplePacketCreator.showEffect("pvp/lose"))
                break

    def getTiming(self, ids: int) -> int:
        if ids <= 5:
            return 5
        if ids >= 7 && ids <= 11:
            return 6
        if ids >= 13 && ids <= 17:
            return 7
        if ids >= 19 && ids <= 23:
            return 8
        if ids >= 25 && ids <= 29:
            return 9
        if ids >= 31 && ids <= 35:
            return 10
        if ids >= 37 && ids <= 38:
            return 15
        return 0

    def getDojoStageDec(self, ids: int) -> int:
        if ids <= 5:
            return 0
        if ids >= 7 && ids <= 11:
            return 1
        if ids >= 13 && ids <= 17:
            return 2
        if ids >= 19 && ids <= 23:
            return 3
        if ids >= 25 && ids <= 29:
            return 4
        if ids >= 31 && ids <= 35:
            return 5
        if ids >= 37 && ids <= 38:
            return 6
        return 0

    def showIntro(self, c: Any, data: str) -> None:
        c.getSession().write(UIPacket.IntroDisableUI(True))
        c.getSession().write(UIPacket.IntroLock(True))
        c.getSession().write(UIPacket.ShowWZEffect(data, -1))

    def showIntro2(self, c: Any, data: str) -> None:
        c.getSession().write(UIPacket.IntroDisableUI(True))
        c.getSession().write(UIPacket.IntroLock(True))
        c.getSession().write(UIPacket.ShowWZEffectS(data, -1))

    def sendDojoClock(self, c: Any, time: int) -> None:
        c.getSession().write(MaplePacketCreator.getClock(time))

    def sendDojoStart(self, c: Any, stage: int) -> None:
        c.getSession().write(MaplePacketCreator.environmentChange("Dojang/start", 4))
        c.getSession().write(MaplePacketCreator.environmentChange("dojang/start/stage", 3))
        c.getSession().write(MaplePacketCreator.environmentChange("dojang/start/number/" + stage, 3))
        c.getSession().write(MaplePacketCreator.trembleEffect(0, 1))

    def handlePinkBeanStart(self, c: Any) -> None:
        map = c.getPlayer().getMap()
        map.resetFully()
        if !map.containsNPC(2141000):
            map.spawnNpc(2141000, Point(-190, -42))

    def reloadWitchTower(self, c: Any) -> None:
        map = c.getPlayer().getMap()
        map.killAllMonsters(False)
        level = c.getPlayer().getLevel()
        mob = None
        if level <= 10:
            mob = 9300367
        elif level <= 20:
            mob = 9300368
        elif level <= 30:
            mob = 9300369
        elif level <= 40:
            mob = 9300370
        elif level <= 50:
            mob = 9300371
        elif level <= 60:
            mob = 9300372
        elif level <= 70:
            mob = 9300373
        elif level <= 80:
            mob = 9300374
        elif level <= 90:
            mob = 9300375
        elif level <= 100:
            mob = 9300376
        else:
            mob = 9300377
        map.spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(mob), MapScriptMethods.witchTowerPos)

    def fromString(self, Str: str) -> Any:
        try:
            return valueOf(Str)
        except IllegalArgumentException as ex:
            return onFirstUserEnter.NULL

    def fromString_Str(self, Str: str) -> Any:
        try:
            return valueOf(Str)
        except IllegalArgumentException as ex:
            return onUserEnter.NULL


# Inner class from Java (originally nested)
class onFirstUserEnter(Enum):
    """Enum onFirstUserEnter"""

    pepeking_effect = 0
    dojang_Eff = 1
    PinkBeen_before = 2
    onRewordMap = 3
    StageMsg_together = 4
    StageMsg_davy = 5
    party6weatherMsg = 6
    StageMsg_juliet = 7
    StageMsg_romio = 8
    moonrabbit_mapEnter = 9
    astaroth_summon = 10
    boss_Ravana = 11
    killing_BonusSetting = 12
    killing_MapSetting = 13
    metro_firstSetting = 14
    balog_bonusSetting = 15
    balog_summon = 16
    easy_balog_summon = 17
    Sky_TrapFEnter = 18
    shammos_Fenter = 19
    PRaid_D_Fenter = 20
    PRaid_B_Fenter = 21
    GhostF = 22
    NULL = 23

    def fromString(self, Str: str) -> Any:
        try:
            return valueOf(Str)
        except IllegalArgumentException as ex:
            return onFirstUserEnter.NULL


# Inner class from Java (originally nested)
class onUserEnter(Enum):
    """Enum onUserEnter"""

    babyPigMap = 0
    crash_Dragon = 1
    evanleaveD = 2
    getDragonEgg = 3
    meetWithDragon = 4
    go1010100 = 5
    go1010200 = 6
    go1010300 = 7
    go1010400 = 8
    evanPromotion = 9
    PromiseDragon = 10
    evanTogether = 11
    incubation_dragon = 12
    TD_MC_Openning = 13
    TD_MC_gasi = 14
    TD_MC_title = 15
    cygnusJobTutorial = 16
    cygnusTest = 17
    startEreb = 18
    dojang_Msg = 19
    dojang_1st = 20
    reundodraco = 21
    undomorphdarco = 22
    explorationPoint = 23
    goAdventure = 24
    go10000 = 25
    go20000 = 26
    go30000 = 27
    go40000 = 28
    go50000 = 29
    go1000000 = 30
    go1010000 = 31
    go1020000 = 32
    go2000000 = 33
    go104000000 = 34
    goArcher = 35
    goPirate = 36
    goRogue = 37
    goMagician = 38
    goSwordman = 39
    goLith = 40
    iceCave = 41
    mirrorCave = 42
    aranDirection = 43
    rienArrow = 44
    rien = 45
    check_count = 46
    Massacre_first = 47
    Massacre_result = 48
    aranTutorAlone = 49
    evanAlone = 50
    dojang_QcheckSet = 51
    Sky_StageEnter = 52
    outCase = 53
    balog_buff = 54
    balog_dateSet = 55
    Sky_BossEnter = 56
    Sky_GateMapEnter = 57
    shammos_Enter = 58
    shammos_Result = 59
    shammos_Base = 60
    dollCave00 = 61
    dollCave01 = 62
    Sky_Quest = 63
    enterBlackfrog = 64
    onSDI = 65
    blackSDI = 66
    summonIceWall = 67
    metro_firstSetting = 68
    start_itemTake = 69
    PRaid_D_Enter = 70
    PRaid_B_Enter = 71
    PRaid_Revive = 72
    PRaid_W_Enter = 73
    PRaid_WinEnter = 74
    PRaid_FailEnter = 75
    Ghost = 76
    NULL = 77

    def fromString(self, Str: str) -> Any:
        try:
            return valueOf(Str)
        except IllegalArgumentException as ex:
            return onUserEnter.NULL

