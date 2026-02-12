"""
FamilyHandler - Converted from Java source
Original: handling/channel/handler/FamilyHandler.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamily import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyBuff import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyCharacter import *  # TODO: import specific classes
# from server.maps.FieldLimitType import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.FamilyPacket import *  # TODO: import specific classes


class FamilyHandler:
    """
    Class FamilyHandler
    """


    def RequestFamily(self, slea: Any, c: Any) -> None:
        chr = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
        if chr is not None:
            c.getSession().write(FamilyPacket.getFamilyPedigree(chr))

    def OpenFamily(self, slea: Any, c: Any) -> None:
        c.getSession().write(FamilyPacket.getFamilyInfo(c.getPlayer()))

    def UseFamily(self, slea: Any, c: Any) -> None:
        type = slea.readInt()
        final MapleFamilyBuff.MapleFamilyBuffEntry entry = MapleFamilyBuff.getBuffEntry(type)
        if entry is None:
            return
        success = c.getPlayer().getFamilyId() > 0 and c.getPlayer().canUseFamilyBuff(entry) and c.getPlayer().getCurrentRep() > entry.rep
        if not success:
            return
        victim = None
        # switch (type):
            # case 0:
                victim = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
                if FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) or not c.getPlayer().isAlive():
                    c.getPlayer().dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
                    success = False
                    break
                if victim is None or (victim.isGM() and not c.getPlayer().isGM()):
                    c.getPlayer().dropMessage(1, "无效名称或您不在同一频道.")
                    success = False
                    break
                if victim.getFamilyId() == c.getPlayer().getFamilyId() and not FieldLimitType.VipRock.check(victim.getMap().getFieldLimit()) and victim.getId() != c.getPlayer().getId():
                    c.getPlayer().changeMap(victim.getMap(), victim.getMap().getPortal(0))
                    break
                c.getPlayer().dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
                success = False
                break
            # case 1:
                victim = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
                if FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) or not c.getPlayer().isAlive():
                    c.getPlayer().dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
                elif victim is None or (victim.isGM() and not c.getPlayer().isGM()):
                    c.getPlayer().dropMessage(1, "无效名称或您不在同一频道.")
                elif victim.getTeleportName() > 0:
                    c.getPlayer().dropMessage(1, "另一个角色要求传唤这个角色。请稍后再试.")
                elif victim.getFamilyId() == c.getPlayer().getFamilyId() and not FieldLimitType.VipRock.check(victim.getMap().getFieldLimit()) and victim.getId() != c.getPlayer().getId():
                    victim.getClient().getSession().write(FamilyPacket.familySummonRequest(c.getPlayer().getName(), c.getPlayer().getMap().getMapName()))
                    victim.setTeleportName(c.getPlayer().getName())
                else:
                    c.getPlayer().dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
                return
            # case 4:
                fam = World.Family.getFamily(c.getPlayer().getFamilyId())
                chrs = fam.getMFC(c.getPlayer().getId()).getOnlineJuniors(fam)
                if chrs < 7:
                    success = False
                    break
                for chrz in chrs:
                    chr = World.Find.findChannel(chrz.getId())
                    if chr == -1:
                        continue
                    chrr = World.getStorage(chr).getCharacterById(chrz.getId())
                    entry.applyTo(chrr)
                break
            # case 2:
            # case 3:
            # case 5:
            # case 6:
            # case 7:
            # case 8:
                entry.applyTo(c.getPlayer())
                break
            # case 9:
            # case 10:
                entry.applyTo(c.getPlayer())
                if c.getPlayer().getParty() is not None:
                    for mpc in c.getPlayer().getParty().getMembers():
                        if mpc.getId() != c.getPlayer().getId():
                            chr2 = c.getPlayer().getMap().getCharacterById(mpc.getId())
                            if chr2 is None:
                                continue
                            entry.applyTo(chr2)
                    break
                break
        if success:
            c.getPlayer().setCurrentRep(c.getPlayer().getCurrentRep() - entry.rep)
            c.getSession().write(FamilyPacket.changeRep(-entry.rep))
            c.getPlayer().useFamilyBuff(entry)
        else:
            c.getPlayer().dropMessage(5, "发生错误.")

    def FamilyOperation(self, slea: Any, c: Any) -> None:
        if c.getPlayer() is None:
            return
        addChr = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
        if addChr is None:
            c.getPlayer().dropMessage(1, "您邀请的玩家角色名字不正确或者尚未登入.")
        elif addChr.getFamilyId() == c.getPlayer().getFamilyId() and addChr.getFamilyId() > 0:
            c.getPlayer().dropMessage(1, "已经在相同的学院里.")
        elif addChr.getMapId() != c.getPlayer().getMapId():
            c.getPlayer().dropMessage(1, "不再相同的地图里.")
        elif addChr.getSeniorId() != 0:
            c.getPlayer().dropMessage(1, "您邀请的玩家角色已经在別的学院里.")
        elif addChr.getLevel() >= c.getPlayer().getLevel():
            c.getPlayer().dropMessage(1, "您需要邀请比您低等级的玩家.")
        elif addChr.getLevel() < c.getPlayer().getLevel() - 20:
            c.getPlayer().dropMessage(1, "您邀请的玩家等级必須相差20等级以内.")
        elif addChr.getLevel() < 10:
            c.getPlayer().dropMessage(1, "您必須邀请10級以上的玩家.")
        elif c.getPlayer().getJunior1() > 0 and c.getPlayer().getJunior2() > 0:
            c.getPlayer().dropMessage(1, "您学院已经有两个人了，请找您的后代继续邀请別人吧.")
        else:
            addChr.getClient().getSession().write(FamilyPacket.sendFamilyInvite(c.getPlayer().getId(), c.getPlayer().getLevel(), c.getPlayer().getJob(), c.getPlayer().getName()))
        c.getSession().write(MaplePacketCreator.enableActions())

    def FamilyPrecept(self, slea: Any, c: Any) -> None:
        fam = World.Family.getFamily(c.getPlayer().getFamilyId())
        if fam is None or fam.getLeaderId() != c.getPlayer().getId():
            return
        fam.setNotice(slea.readMapleAsciiString())
        c.getPlayer().dropMessage(1, "重开家族视窗即可套用.")

    def FamilySummon(self, slea: Any, c: Any) -> None:
        TYPE = 1
        final MapleFamilyBuff.MapleFamilyBuffEntry cost = MapleFamilyBuff.getBuffEntry(TYPE)
        tt = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
        if c.getPlayer().getFamilyId() > 0 and tt is not None and tt.getFamilyId() == c.getPlayer().getFamilyId() and not FieldLimitType.VipRock.check(tt.getMap().getFieldLimit()) and not FieldLimitType.VipRock.check(c.getPlayer().getMap().getFieldLimit()) and c.getPlayer().isAlive() and tt.isAlive() and tt.canUseFamilyBuff(cost) and c.getPlayer().getTeleportName() == (tt.getName()) and tt.getCurrentRep() > cost.rep and c.getPlayer().getEventInstance() is None and tt.getEventInstance() is None:
            accepted = slea.readByte() > 0
            if accepted:
                c.getPlayer().changeMap(tt.getMap(), tt.getMap().getPortal(0))
                tt.setCurrentRep(tt.getCurrentRep() - cost.rep)
                tt.getClient().getSession().write(FamilyPacket.changeRep(-cost.rep))
                tt.useFamilyBuff(cost)
            else:
                tt.dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
        else:
            c.getPlayer().dropMessage(5, "传唤失败。您当前的位置或状态不允许传唤.")
        c.getPlayer().setTeleportName("")

    def DeleteJunior(self, slea: Any, c: Any) -> None:
        juniorid = slea.readInt()
        if c.getPlayer().getFamilyId() <= 0 or juniorid <= 0 or (c.getPlayer().getJunior1() != juniorid and c.getPlayer().getJunior2() != juniorid):
            return
        fam = World.Family.getFamily(c.getPlayer().getFamilyId())
        other = fam.getMFC(juniorid)
        if other is None:
            return
        oth = c.getPlayer().getMFC()
        junior2 = oth.getJunior2() == juniorid
        if junior2:
            oth.setJunior2(0)
        else:
            oth.setJunior1(0)
        c.getPlayer().saveFamilyStatus()
        other.setSeniorId(0)
        MapleFamily.setOfflineFamilyStatus(other.getFamilyId(), other.getSeniorId(), other.getJunior1(), other.getJunior2(), other.getCurrentRep(), other.getTotalRep(), other.getId())
        MapleCharacterUtil.sendNote(other.getName(), c.getPlayer().getName(), c.getPlayer().getName() + " 我做人失败 解散了家族", 0)
        if not fam.splitFamily(juniorid, other):
            if not junior2:
                fam.resetDescendants()
            fam.resetPedigree()
        c.getPlayer().dropMessage(1, "踢出了 (" + other.getName() + ").")
        c.getSession().write(MaplePacketCreator.enableActions())

    def DeleteSenior(self, slea: Any, c: Any) -> None:
        if c.getPlayer().getFamilyId() <= 0 or c.getPlayer().getSeniorId() <= 0:
            return
        fam = World.Family.getFamily(c.getPlayer().getFamilyId())
        mgc = fam.getMFC(c.getPlayer().getSeniorId())
        mgc_ = c.getPlayer().getMFC()
        mgc_.setSeniorId(0)
        junior2 = mgc.getJunior2() == c.getPlayer().getId()
        if junior2:
            mgc.setJunior2(0)
        else:
            mgc.setJunior1(0)
        MapleFamily.setOfflineFamilyStatus(mgc.getFamilyId(), mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
        c.getPlayer().saveFamilyStatus()
        MapleCharacterUtil.sendNote(mgc.getName(), c.getPlayer().getName(), c.getPlayer().getName() + " 我展翅高飞了 离开你的家族", 0)
        if not fam.splitFamily(c.getPlayer().getId(), mgc_):
            if not junior2:
                fam.resetDescendants()
            fam.resetPedigree()
        c.getPlayer().dropMessage(1, "退出了 (" + mgc.getName() + ") 的家族.")
        c.getSession().write(MaplePacketCreator.enableActions())

    def AcceptFamily(self, slea: Any, c: Any) -> None:
        inviter = c.getPlayer().getMap().getCharacterById(slea.readInt())
        if inviter is not None and c.getPlayer().getSeniorId() == 0 and (c.getPlayer().isGM() or not inviter.isHidden()) and inviter.getLevel() - 20 <= c.getPlayer().getLevel() and inviter.getLevel() >= 10 and inviter.getName() == (slea.readMapleAsciiString()) and inviter.getNoJuniors() < 2 and c.getPlayer().getLevel() >= 10:
            accepted = slea.readByte() > 0
            inviter.getClient().getSession().write(FamilyPacket.sendFamilyJoinResponse(accepted, c.getPlayer().getName()))
            if accepted:
                c.getSession().write(FamilyPacket.getSeniorMessage(inviter.getName()))
                old = (c.getPlayer().getMFC() is None) ? 0 : c.getPlayer().getMFC().getFamilyId()
                oldj1 = (c.getPlayer().getMFC() is None) ? 0 : c.getPlayer().getMFC().getJunior1()
                oldj2 = (c.getPlayer().getMFC() is None) ? 0 : c.getPlayer().getMFC().getJunior2()
                if inviter.getFamilyId() > 0 and World.Family.getFamily(inviter.getFamilyId()) is not None:
                    fam = World.Family.getFamily(inviter.getFamilyId())
                    c.getPlayer().setFamily((old <= 0) ? inviter.getFamilyId() : old, inviter.getId(), (oldj1 <= 0) ? 0 : oldj1, (oldj2 <= 0) ? 0 : oldj2)
                    mf = inviter.getMFC()
                    if mf.getJunior1() > 0:
                        mf.setJunior2(c.getPlayer().getId())
                    else:
                        mf.setJunior1(c.getPlayer().getId())
                    inviter.saveFamilyStatus()
                    if old > 0 and World.Family.getFamily(old) is not None:
                        MapleFamily.mergeFamily(fam, World.Family.getFamily(old))
                    else:
                        c.getPlayer().setFamily(inviter.getFamilyId(), inviter.getId(), (oldj1 <= 0) ? 0 : oldj1, (oldj2 <= 0) ? 0 : oldj2)
                        fam.setOnline(c.getPlayer().getId(), True, c.getChannel())
                        c.getPlayer().saveFamilyStatus()
                    if fam is not None:
                        if inviter.getNoJuniors() == 1 or old > 0:
                            fam.resetDescendants()
                        fam.resetPedigree()
                else:
                    id = MapleFamily.createFamily(inviter.getId())
                    if id > 0:
                        MapleFamily.setOfflineFamilyStatus(id, 0, c.getPlayer().getId(), 0, inviter.getCurrentRep(), inviter.getTotalRep(), inviter.getId())
                        MapleFamily.setOfflineFamilyStatus(id, inviter.getId(), (oldj1 <= 0) ? 0 : oldj1, (oldj2 <= 0) ? 0 : oldj2, c.getPlayer().getCurrentRep(), c.getPlayer().getTotalRep(), c.getPlayer().getId())
                        inviter.setFamily(id, 0, c.getPlayer().getId(), 0)
                        c.getPlayer().setFamily(id, inviter.getId(), (oldj1 <= 0) ? 0 : oldj1, (oldj2 <= 0) ? 0 : oldj2)
                        fam2 = World.Family.getFamily(id)
                        fam2.setOnline(inviter.getId(), True, inviter.getClient().getChannel())
                        if old > 0 and World.Family.getFamily(old) is not None:
                            MapleFamily.mergeFamily(fam2, World.Family.getFamily(old))
                        else:
                            fam2.setOnline(c.getPlayer().getId(), True, c.getChannel())
                        fam2.resetDescendants()
                        fam2.resetPedigree()
                c.getSession().write(FamilyPacket.getFamilyInfo(c.getPlayer()))

