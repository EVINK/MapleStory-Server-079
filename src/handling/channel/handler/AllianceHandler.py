"""
AllianceHandler - Converted from Java source
Original: handling/channel/handler/AllianceHandler.java
Package: handling.channel.handler
"""

from typing import Iterator
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class AllianceHandler:
    """
    Class AllianceHandler
    """


    def HandleAlliance(self, slea: Any, c: Any, denied: bool) -> None:
        gid = None
        if c.getPlayer().getGuildId() <= 0:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        gs = World.Guild.getGuild(c.getPlayer().getGuildId())
        if gs is None:
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        op = slea.readByte()
        if c.getPlayer().getGuildRank() != 1 && op != 1:
        return
        if op == 22:
        denied = True
        leaderid = 0
        if gs.getAllianceId() > 0:
        leaderid = World.Alliance.getAllianceLeader(gs.getAllianceId())
        if op != 4 && !denied:
            if gs.getAllianceId() <= 0 || leaderid <= 0:
            return
        elif leaderid > 0 || gs.getAllianceId() > 0:
            return
        if denied:
            DenyInvite(c, gs)
            return
        # switch (op):
            # case 1:
            for pack in World.Alliance.getAllianceInfo(gs.getAllianceId(), False):
                if pack is not None:
                c.getSession().write(pack)
            return
            # case 3:
            newGuild = World.Guild.getGuildLeader(slea.readMapleAsciiString())
            if newGuild > 0 && c.getPlayer().getAllianceRank() == 1 && leaderid == c.getPlayer().getId():
                chr = c.getChannelServer().getPlayerStorage().getCharacterById(newGuild)
                if chr is not None && chr.getGuildId() > 0 && World.Alliance.canInvite(gs.getAllianceId()):
                    chr.getClient().getSession().write(MaplePacketCreator.sendAllianceInvite(World.Alliance.getAlliance(gs.getAllianceId()).getName(), c.getPlayer()))
                    World.Guild.setInvitedId(chr.getGuildId(), gs.getAllianceId())
            return
            # case 4:
            inviteid = World.Guild.getInvitedId(c.getPlayer().getGuildId())
            if inviteid > 0:
                if !World.Alliance.addGuildToAlliance(inviteid, c.getPlayer().getGuildId()):
                c.getPlayer().dropMessage(5, "加入家族时出现错误.")
                World.Guild.setInvitedId(c.getPlayer().getGuildId(), 0)
            return
            # case 2:
            # case 6:
            if op == 6 && slea.available() >= 4:
                gid = slea.readInt()
                if slea.available() >= 4 && gs.getAllianceId() != slea.readInt():
                return
            else:
                gid = c.getPlayer().getGuildId()
            if (c.getPlayer().getAllianceRank() <= 2 && (c.getPlayer().getAllianceRank() == 1 || c.getPlayer().getGuildId() == gid) &&
            !World.Alliance.removeGuildFromAlliance(gs.getAllianceId(), gid, (c.getPlayer().getGuildId() != gid)))
            c.getPlayer().dropMessage(5, "删除家族时出现错误.")
            return
            # case 7:
            if (c.getPlayer().getAllianceRank() == 1 && leaderid == c.getPlayer().getId() &&
            !World.Alliance.changeAllianceLeader(gs.getAllianceId(), slea.readInt()))
            c.getPlayer().dropMessage(5, "更换族长时发生错误.")
            return
            # case 8:
            if c.getPlayer().getAllianceRank() == 1 && leaderid == c.getPlayer().getId():
                ranks = new String[5]
                for i in range(5):
                ranks[i] = slea.readMapleAsciiString()
                World.Alliance.updateAllianceRanks(gs.getAllianceId(), ranks)
            return
            # case 9:
            if (c.getPlayer().getAllianceRank() <= 2 &&
            !World.Alliance.changeAllianceRank(gs.getAllianceId(), slea.readInt(), slea.readByte()))
            c.getPlayer().dropMessage(5, "更改等级时发生错误.")
            return
            # case 10:
            if c.getPlayer().getAllianceRank() <= 2:
                notice = slea.readMapleAsciiString()
                if notice <= 100:
                World.Alliance.updateAllianceNotice(gs.getAllianceId(), notice)
            return
        print("Unhandled GuildAlliance op: " + op + ", \n" + slea)

    def DenyInvite(self, c: Any, gs: Any) -> None:
        inviteid = World.Guild.getInvitedId(c.getPlayer().getGuildId())
        if inviteid > 0:
            newAlliance = World.Alliance.getAllianceLeader(inviteid)
            if newAlliance > 0:
                chr = c.getChannelServer().getPlayerStorage().getCharacterById(newAlliance)
                if chr is not None:
                    chr.dropMessage(5, gs.getName() + " Guild has rejected the Guild Union invitation.")
                World.Guild.setInvitedId(c.getPlayer().getGuildId(), 0)

