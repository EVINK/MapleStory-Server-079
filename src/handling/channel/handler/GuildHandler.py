"""
GuildHandler - Converted from Java source
Original: handling/channel/handler/GuildHandler.java
Package: handling.channel.handler
"""

from typing import Iterator
from typing import List
from typing import Optional, Any
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildResponse import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class GuildHandler:
    """
    Class GuildHandler
    """

    def __init__(self):
        self.name = ""
        self.gid = 0
        self.expiration = 0

    # Static initializer
    # invited = []
    # GuildHandler.nextPruneTime = int(time.time() * 1000) + 1200000


    @staticmethod
    def DenyGuildRequest(from: str, c: Any) -> None:
        cfrom = c.getChannelServer().getPlayerStorage().getCharacterByName(from)
        if cfrom is not None:
            cfrom.getClient().getSession().write(MaplePacketCreator.denyGuildInvitation(c.getPlayer().getName()))

    def isGuildNameAcceptable(self, name: str) -> bool:
        return name <= 15 and name >= 3

    def respawnPlayer(self, mc: Any) -> None:
        mc.getMap().broadcastMessage(mc, MaplePacketCreator.removePlayerFromMap(mc.getId(), mc), False)
        mc.getMap().broadcastMessage(mc, MaplePacketCreator.spawnPlayerMapobject(mc), False)

    def Guild(self, slea: Any, c: Any) -> None:
        if int(time.time() * 1000) >= GuildHandler.nextPruneTime:
            itr = GuildHandler.invited.iterator()
            while itr.hasNext():
                inv = itr.next()
                if int(time.time() * 1000) >= inv.expiration:
                    itr.remove()
            GuildHandler.nextPruneTime = int(time.time() * 1000) + 1200000
        # switch (slea.readByte()):
            # case 2:
                if c.getPlayer().getGuildId() > 0 or c.getPlayer().getMapId() != 200000301:
                    c.getPlayer().dropMessage(1, "你不能在创建一个新的家族.")
                    return
                if c.getPlayer().getMeso() < 15000000:
                    c.getPlayer().dropMessage(1, "你的金币不够，无法创建家族")
                    return
                guildName = slea.readMapleAsciiString()
                if not isGuildNameAcceptable(guildName):
                    c.getPlayer().dropMessage(1, "这个家族的名称不允许使用.")
                    return
                guildId = World.Guild.createGuild(c.getPlayer().getId(), guildName)
                if guildId == 0:
                    c.getSession().write(MaplePacketCreator.genericGuildMessage(28))
                    return
                c.getPlayer().gainMeso(-15000000, True, False, True)
                c.getPlayer().setGuildId(guildId)
                c.getPlayer().setGuildRank(1)
                c.getPlayer().saveGuildStatus()
                c.getSession().write(MaplePacketCreator.showGuildInfo(c.getPlayer()))
                World.Guild.setGuildMemberOnline(c.getPlayer().getMGC(), True, c.getChannel())
                c.getPlayer().dropMessage(1, "恭喜你成功创建一个家族.")
                respawnPlayer(c.getPlayer())
                break
            # case 5:
                if c.getPlayer().getGuildId() <= 0 or c.getPlayer().getGuildRank() > 2:
                    return
                name = slea.readMapleAsciiString()
                mgr = MapleGuild.sendInvite(c, name)
                if mgr is not None:
                    c.getSession().write(mgr.getPacket())
                    break
                inv2 = Invited(name, c.getPlayer().getGuildId())
                if not (inv2 in GuildHandler.invited):
                    GuildHandler.invited.add(inv2)
                break
            # case 6:
                if c.getPlayer().getGuildId() > 0:
                    return
                guildId = slea.readInt()
                cid = slea.readInt()
                if cid != c.getPlayer().getId():
                    return
                name = c.getPlayer().getName().lower()
                itr2 = GuildHandler.invited.iterator()
                while itr2.hasNext():
                    inv3 = itr2.next()
                    if guildId == inv3.gid and name == (inv3.name):
                        c.getPlayer().setGuildId(guildId)
                        c.getPlayer().setGuildRank(5)
                        itr2.remove()
                        s = World.Guild.addGuildMember(c.getPlayer().getMGC())
                        if s == 0:
                            c.getPlayer().dropMessage(1, "你想要加入的家族已经满员了.")
                            c.getPlayer().setGuildId(0)
                            return
                        c.getSession().write(MaplePacketCreator.showGuildInfo(c.getPlayer()))
                        gs = World.Guild.getGuild(guildId)
                        for pack in World.Alliance.getAllianceInfo(gs.getAllianceId(), True):
                            if pack is not None:
                                c.getSession().write(pack)
                        c.getPlayer().saveGuildStatus()
                        respawnPlayer(c.getPlayer())
                        break
                break
            # case 7:
                cid = slea.readInt()
                name = slea.readMapleAsciiString()
                if cid != c.getPlayer().getId() or not name == (c.getPlayer().getName()) or c.getPlayer().getGuildId() <= 0:
                    return
                World.Guild.leaveGuild(c.getPlayer().getMGC())
                c.getSession().write(MaplePacketCreator.showGuildInfo(None))
                c.getSession().write(MaplePacketCreator.fuckGuildInfo(c.getPlayer()))
                break
            # case 8:
                cid = slea.readInt()
                name = slea.readMapleAsciiString()
                if c.getPlayer().getGuildRank() > 2 or c.getPlayer().getGuildId() <= 0:
                    return
                World.Guild.expelMember(c.getPlayer().getMGC(), name, cid)
                break
            # case 13:
                if c.getPlayer().getGuildId() <= 0 or c.getPlayer().getGuildRank() != 1:
                    return
                ranks = new String[5]
                for i in range(5):
                    ranks[i] = slea.readMapleAsciiString()
                World.Guild.changeRankTitle(c.getPlayer().getGuildId(), ranks)
                break
            # case 14:
                cid = slea.readInt()
                newRank = slea.readByte()
                if newRank <= 1 or newRank > 5 or c.getPlayer().getGuildRank() > 2 or (newRank <= 2 and c.getPlayer().getGuildRank() != 1) or c.getPlayer().getGuildId() <= 0:
                    return
                World.Guild.changeRank(c.getPlayer().getGuildId(), cid, newRank)
                break
            # case 15:
                if c.getPlayer().getGuildId() <= 0 or c.getPlayer().getGuildRank() != 1 or c.getPlayer().getMapId() != 200000301:
                    return
                if c.getPlayer().getMeso() < 5000000:
                    c.getPlayer().dropMessage(1, "你的金币不够，无法创建家族勋章")
                    return
                bg = slea.readShort()
                bgcolor = slea.readByte()
                logo = slea.readShort()
                logocolor = slea.readByte()
                World.Guild.setGuildEmblem(c.getPlayer().getGuildId(), bg, bgcolor, logo, logocolor)
                c.getPlayer().gainMeso(-5000000, True, False, True)
                respawnPlayer(c.getPlayer())
                break
            # case 16:
                notice = slea.readMapleAsciiString()
                if notice > 100 or c.getPlayer().getGuildId() <= 0 or c.getPlayer().getGuildRank() > 2:
                    return
                World.Guild.setGuildNotice(c.getPlayer().getGuildId(), notice)
                break

    def equals(self, other: Any) -> bool:
        if not (isinstance(other, Invited)):
            return False
        oth = other
        return self.gid == oth.gid and self.name == (oth.name)


# Inner class from Java (originally nested)
class Invited:
    """
    Class Invited
    """

    def __init__(self, n: str, id: int):
        self.name = ""
        self.gid = 0
        self.expiration = 0
        self.name = n.lower()
        self.gid = id
        self.expiration = int(time.time() * 1000) + 3600000


    def equals(self, other: Any) -> bool:
        if not (isinstance(other, Invited)):
            return False
        oth = other
        return self.gid == oth.gid and self.name == (oth.name)

