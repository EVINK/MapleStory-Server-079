"""
PartyHandler - Converted from Java source
Original: handling/channel/handler/PartyHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PartyOperation import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class PartyHandler:
    """
    Class PartyHandler
    """


    def DenyPartyRequest(self, slea: Any, c: Any) -> None:
        action = slea.readByte()
        partyid = slea.readInt()
        if c.getPlayer().getParty() is None:
            party = World.Party.getParty(partyid)
            if party is not None:
                # switch (action):
                    # case 27:
                        if party.getMembers() < 6:
                            World.Party.updateParty(partyid, PartyOperation.JOIN, MaplePartyCharacter(c.getPlayer()))
                            c.getPlayer().receivePartyMemberHP()
                            c.getPlayer().updatePartyMemberHP()
                            break
                        c.getSession().write(MaplePacketCreator.partyStatusMessage(17))
                        break
                    # case 22:
                        cfrom = c.getChannelServer().getPlayerStorage().getCharacterById(party.getLeader().getId())
                        if cfrom is not None:
                            cfrom.getClient().getSession().write(MaplePacketCreator.partyStatusMessage(23, c.getPlayer().getName()))
                            break
                        break
            else:
                c.getPlayer().dropMessage(5, "要参加的队伍不存在。")
        else:
            c.getPlayer().dropMessage(5, "您已经有一个组队，无法加入其他组队!")

    def PartyOperatopn(self, slea: Any, c: Any) -> None:
        operation = slea.readByte()
        party = c.getPlayer().getParty()
        partyplayer = MaplePartyCharacter(c.getPlayer())
        # switch (operation):
            # case 1:
                if party is None:
                    party = World.Party.createParty(partyplayer)
                    c.getPlayer().setParty(party)
                    c.getSession().write(MaplePacketCreator.partyCreated(party.getId()))
                    break
                if partyplayer == (party.getLeader()) and party.getMembers() == 1:
                    c.getSession().write(MaplePacketCreator.partyCreated(party.getId()))
                    break
                c.getPlayer().dropMessage(5, "你不能创建一个组队,因为你已经存在一个队伍中")
                break
            # case 2:
                if party is not None:
                    if partyplayer == (party.getLeader()):
                        World.Party.updateParty(party.getId(), PartyOperation.DISBAND, partyplayer)
                        if c.getPlayer().getEventInstance() is not None:
                            c.getPlayer().getEventInstance().disbandParty()
                        if c.getPlayer().getPyramidSubway() is not None:
                            c.getPlayer().getPyramidSubway().fail(c.getPlayer())
                    else:
                        World.Party.updateParty(party.getId(), PartyOperation.LEAVE, partyplayer)
                        if c.getPlayer().getEventInstance() is not None:
                            c.getPlayer().getEventInstance().leftParty(c.getPlayer())
                        if c.getPlayer().getPyramidSubway() is not None:
                            c.getPlayer().getPyramidSubway().fail(c.getPlayer())
                    c.getPlayer().setParty(None)
                    break
                break
            # case 3:
                partyid = slea.readInt()
                if party is not None:
                    c.getPlayer().dropMessage(5, "你已经有队伍了，无法再加入其他队伍。请退组再试！")
                    break
                party = World.Party.getParty(partyid)
                if party is None:
                    c.getPlayer().dropMessage(5, "要加入的队伍不存在")
                    break
                if party.getMembers() < 6:
                    World.Party.updateParty(party.getId(), PartyOperation.JOIN, partyplayer)
                    c.getPlayer().receivePartyMemberHP()
                    c.getPlayer().updatePartyMemberHP()
                    break
                c.getSession().write(MaplePacketCreator.partyStatusMessage(17))
                break
            # case 4:
                invited = c.getChannelServer().getPlayerStorage().getCharacterByName(slea.readMapleAsciiString())
                if invited is None:
                    c.getSession().write(MaplePacketCreator.partyStatusMessage(18))
                    break
                if invited.getParty() is not None or party is None:
                    c.getSession().write(MaplePacketCreator.partyStatusMessage(16))
                    break
                if party.getMembers() < 6:
                    invited.getClient().getSession().write(MaplePacketCreator.partyInvite(c.getPlayer()))
                    break
                c.getSession().write(MaplePacketCreator.partyStatusMessage(17))
                break
            # case 5:
                if party is None or partyplayer is None:
                    break
                if not partyplayer == (party.getLeader()):
                    break
                if partyplayer == (party.getLeader()):
                    expelled = party.getMemberById(slea.readInt())
                    if expelled is not None:
                        World.Party.updateParty(party.getId(), PartyOperation.EXPEL, expelled)
                        if c.getPlayer().getEventInstance() is not None and expelled.isOnline():
                            c.getPlayer().getEventInstance().disbandParty()
                        if c.getPlayer().getPyramidSubway() is not None and expelled.isOnline():
                            c.getPlayer().getPyramidSubway().fail(c.getPlayer())
                    break
                break
            # case 6:
                if party is not None:
                    newleader = party.getMemberById(slea.readInt())
                    if newleader is not None and partyplayer == (party.getLeader()):
                        party.setLeader(newleader)
                        World.Party.updateParty(party.getId(), PartyOperation.SILENT_UPDATE, newleader)
                    c.getSession().write(MaplePacketCreator.enableActions())
                    break
                break
            # default:
                print("未知的队伍操作. 0x0" + operation)
                break

