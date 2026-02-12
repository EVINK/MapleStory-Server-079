"""
MonsterCarnivalHandler - Converted from Java source
Original: handling/channel/handler/MonsterCarnivalHandler.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from server.MapleCarnivalFactory import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.MonsterCarnivalPacket import *  # TODO: import specific classes


class MonsterCarnivalHandler:
    """
    Class MonsterCarnivalHandler
    """


    def MonsterCarnival(self, slea: Any, c: Any) -> None:
        if c.getPlayer().getCarnivalParty() is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        tab = slea.readByte()
        num = slea.readInt()
        # switch (tab):
            # case 0:
                mobs = c.getPlayer().getMap().getMobsToSpawn()
                if num >= mobs || c.getPlayer().getAvailableCP() < mobs.get(num).right:
                    c.getPlayer().dropMessage(5, "你没有足够的CP.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                mons = MapleLifeFactory.getMonster(mobs.get(num).left)
                if c.getPlayer().isGM():
                    print("tab：" + tab)
                    print("num：" + num)
                    print("mons：" + mons)
                    print("num：" + num)
                    print("判断A：" + mons is not None)
                    print("判断B：" + c.getPlayer().getMap().makeCarnivalSpawn(c.getPlayer().getCarnivalParty().getTeam(), mons, num))
                if mons is not None && c.getPlayer().getMap().makeCarnivalSpawn(c.getPlayer().getCarnivalParty().getTeam(), mons, num):
                    c.getPlayer().getCarnivalParty().useCP(c.getPlayer(), mobs.get(num).right)
                    c.getPlayer().CPUpdate(False, c.getPlayer().getAvailableCP(), c.getPlayer().getTotalCP(), 0)
                    for chr in c.getPlayer().getMap().getCharactersThreadsafe():
                        chr.CPUpdate(True, c.getPlayer().getCarnivalParty().getAvailableCP(), c.getPlayer().getCarnivalParty().getTotalCP(), c.getPlayer().getCarnivalParty().getTeam())
                    c.getPlayer().getMap().broadcastMessage(MonsterCarnivalPacket.playerSummoned(c.getPlayer().getName(), tab, num))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    break
                c.getPlayer().dropMessage(5, "你不能再召唤怪物了.")
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 1:
                skillid = c.getPlayer().getMap().getSkillIds()
                if num >= skillid:
                    c.getPlayer().dropMessage(5, "发生了一个错误.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                final MapleCarnivalFactory.MCSkill skil = MapleCarnivalFactory.getInstance().getSkill(skillid.get(num))
                if skil is None || c.getPlayer().getAvailableCP() < skil.cpLoss:
                    c.getPlayer().dropMessage(5, "你没有足够的CP.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                dis = skil.getDisease()
                found = False
                for chr2 in c.getPlayer().getMap().getCharactersThreadsafe():
                    if (chr2.getParty() is None || (c.getPlayer().getParty() is not None && chr2.getParty().getId() != c.getPlayer().getParty().getId())) && (skil.targetsAll || Randomizer.nextBoolean()):
                        found = True
                        if dis is None:
                            chr2.dispel()
                        elif skil.getSkill() is None:
                            chr2.giveDebuff(dis, 1, 30000, MapleDisease.getByDisease(dis), 1)
                        else:
                            chr2.giveDebuff(dis, skil.getSkill())
                        if !skil.targetsAll:
                            break
                        continue
                if found:
                    c.getPlayer().getCarnivalParty().useCP(c.getPlayer(), skil.cpLoss)
                    c.getPlayer().CPUpdate(False, c.getPlayer().getAvailableCP(), c.getPlayer().getTotalCP(), 0)
                    for chr2 in c.getPlayer().getMap().getCharactersThreadsafe():
                        chr2.CPUpdate(True, c.getPlayer().getCarnivalParty().getAvailableCP(), c.getPlayer().getCarnivalParty().getTotalCP(), c.getPlayer().getCarnivalParty().getTeam())
                        chr2.dropMessage(5, "[" + ((c.getPlayer().getCarnivalParty().getTeam() == 0) ? "红队" : "蓝队") + "] " + c.getPlayer().getName() + " has used a skill. [" + dis.name() + "].")
                    c.getPlayer().getMap().broadcastMessage(MonsterCarnivalPacket.playerSummoned(c.getPlayer().getName(), tab, num))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    break
                c.getPlayer().dropMessage(5, "发生错误B.")
                c.getSession().write(MaplePacketCreator.enableActions())
                break
            # case 2:
                final MapleCarnivalFactory.MCSkill skil2 = MapleCarnivalFactory.getInstance().getGuardian(num)
                if skil2 is None || c.getPlayer().getAvailableCP() < skil2.cpLoss:
                    c.getPlayer().dropMessage(5, "你没有足够的CP.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                if c.getPlayer().getMap().makeCarnivalReactor(c.getPlayer().getCarnivalParty().getTeam(), num):
                    c.getPlayer().getCarnivalParty().useCP(c.getPlayer(), skil2.cpLoss)
                    c.getPlayer().CPUpdate(False, c.getPlayer().getAvailableCP(), c.getPlayer().getTotalCP(), 0)
                    for chr3 in c.getPlayer().getMap().getCharactersThreadsafe():
                        chr3.CPUpdate(True, c.getPlayer().getCarnivalParty().getAvailableCP(), c.getPlayer().getCarnivalParty().getTotalCP(), c.getPlayer().getCarnivalParty().getTeam())
                    c.getPlayer().getMap().broadcastMessage(MonsterCarnivalPacket.playerSummoned(c.getPlayer().getName(), tab, num))
                    c.getSession().write(MaplePacketCreator.enableActions())
                    break
                c.getPlayer().dropMessage(5, "你不能再召唤了.")
                c.getSession().write(MaplePacketCreator.enableActions())
                break

