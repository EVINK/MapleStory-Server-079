"""
ChatHandler - Converted from Java source
Original: handling/channel/handler/ChatHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.messages.CommandProcessor import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleMessenger import *  # TODO: import specific classes
# from handling.world.MapleMessengerCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class ChatHandler:
    """
    Class ChatHandler
    """


    def GeneralChat(self, text: str, unk: int, c: Any, chr: Any) -> None:
        if chr is not None:
            try:
                condition = CommandProcessor.processCommand(c, text, ServerConstants.CommandType.NORMAL)
                if condition:
                    return
            except Exception as e:
                print(e)
            if !chr.isGM() && text >= 80:
                return
            if chr.isHidden():
                chr.getMap().broadcastGMMessage(chr, MaplePacketCreator.getChatText(chr.getId(), text, c.getPlayer().isGM(), unk), True)
            else:
                chr.getCheatTracker().checkMsg()
                chr.getMap().broadcastMessage(MaplePacketCreator.getChatText(chr.getId(), text, c.getPlayer().isGM(), unk), c.getPlayer().getPosition())

    def Others(self, slea: Any, c: Any, chr: Any) -> None:
        type = slea.readByte()
        numRecipients = slea.readByte()
        recipients = new int[numRecipients]
        i = 0
        while i < numRecipients:
            recipients[i] = slea.readInt()
        chattext = slea.readMapleAsciiString()
        if chr is None || !chr.getCanTalk():
            c.getSession().write(MaplePacketCreator.serverNotice(6, "你已经被禁言，因此无法说话."))
            return
        if CommandProcessor.processCommand(c, chattext, ServerConstants.CommandType.NORMAL):
            return
        chr.getCheatTracker().checkMsg()
        # switch (type):
            # case 0:
                World.Buddy.buddyChat(recipients, chr.getId(), chr.getName(), chattext)
                break
            # case 1:
                if chr.getParty() is None:
                    break
                World.Party.partyChat(chr.getParty().getId(), chattext, chr.getName())
                break
            # case 2:
                if chr.getGuildId() <= 0:
                    break
                World.Guild.guildChat(chr.getGuildId(), chr.getName(), chr.getId(), chattext)
                break
            # case 3:
                if chr.getGuildId() <= 0:
                    break
                World.Alliance.allianceChat(chr.getGuildId(), chr.getName(), chr.getId(), chattext)
                break

    def Messenger(self, slea: Any, c: Any) -> None:
        messenger = c.getPlayer().getMessenger()
        # switch (slea.readByte()):
            # case 0:
                if messenger is None:
                    messengerid = slea.readInt()
                    if messengerid == 0:
                        c.getPlayer().setMessenger(World.Messenger.createMessenger(MapleMessengerCharacter(c.getPlayer())))
                    else:
                        messenger = World.Messenger.getMessenger(messengerid)
                        if messenger is not None:
                            position = messenger.getLowestPosition()
                            if position > -1 && position < 4:
                                c.getPlayer().setMessenger(messenger)
                                World.Messenger.joinMessenger(messenger.getId(), MapleMessengerCharacter(c.getPlayer()), c.getPlayer().getName(), c.getChannel())
                    break
                break
            # case 2:
                if messenger is not None:
                    messengerplayer = MapleMessengerCharacter(c.getPlayer())
                    World.Messenger.leaveMessenger(messenger.getId(), messengerplayer)
                    c.getPlayer().setMessenger(None)
                    break
                break
            # case 3:
                if messenger is None:
                    break
                position2 = messenger.getLowestPosition()
                if position2 <= -1 || position2 >= 4:
                    return
                input = slea.readMapleAsciiString()
                target = c.getChannelServer().getPlayerStorage().getCharacterByName(input)
                if target is not None:
                    if target.getMessenger() is None:
                        if !target.isGM() || c.getPlayer().isGM():
                            c.getSession().write(MaplePacketCreator.messengerNote(input, 4, 1))
                            target.getClient().getSession().write(MaplePacketCreator.messengerInvite(c.getPlayer().getName(), messenger.getId()))
                        else:
                            c.getSession().write(MaplePacketCreator.messengerNote(input, 4, 0))
                    else:
                        c.getSession().write(MaplePacketCreator.messengerChat(c.getPlayer().getName() + " : " + target.getName() + "已经是使用枫叶信使."))
                elif World.isConnected(input):
                    World.Messenger.messengerInvite(c.getPlayer().getName(), messenger.getId(), input, c.getChannel(), c.getPlayer().isGM())
                else:
                    c.getSession().write(MaplePacketCreator.messengerNote(input, 4, 0))
                break
            # case 5:
                targeted = slea.readMapleAsciiString()
                target = c.getChannelServer().getPlayerStorage().getCharacterByName(targeted)
                if target is not None:
                    if target.getMessenger() is not None:
                        target.getClient().getSession().write(MaplePacketCreator.messengerNote(c.getPlayer().getName(), 5, 0))
                        break
                    break
                else:
                    if !c.getPlayer().isGM():
                        World.Messenger.declineChat(targeted, c.getPlayer().getName())
                        break
                    break
            # case 6:
                if messenger is not None:
                    World.Messenger.messengerChat(messenger.getId(), slea.readMapleAsciiString(), c.getPlayer().getName())
                    break
                break

    def Whisper_Find(self, slea: Any, c: Any) -> None:
        mode = slea.readByte()
        # switch (mode):
            # case 5:
            # case 68:
                recipient = slea.readMapleAsciiString()
                player = c.getChannelServer().getPlayerStorage().getCharacterByName(recipient)
                if player is None:
                    ch = World.Find.findChannel(recipient)
                    if ch > 0:
                        player = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(recipient)
                        if player is None:
                            break
                        if player is not None:
                            if !player.isGM() || (c.getPlayer().isGM() && player.isGM()):
                                c.getSession().write(MaplePacketCreator.getFindReply(recipient, ch, mode == 68))
                            else:
                                c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 0))
                            return
                    # switch (ch):
                        # case -10:
                            c.getSession().write(MaplePacketCreator.getFindReplyWithCS(recipient, mode == 68))
                            break
                        # case -20:
                            c.getSession().write(MaplePacketCreator.getFindReplyWithMTS(recipient, mode == 68))
                            break
                        # default:
                            c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 0))
                            break
                    break
                if !player.isGM() || (c.getPlayer().isGM() && player.isGM()):
                    c.getSession().write(MaplePacketCreator.getFindReplyWithMap(player.getName(), player.getMap().getId(), mode == 68))
                    break
                c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 0))
                break
            # case 6:
                if !c.getPlayer().getCanTalk():
                    c.getSession().write(MaplePacketCreator.serverNotice(6, "你已经被禁言，因此无法说话."))
                    return
                c.getPlayer().getCheatTracker().checkMsg()
                recipient = slea.readMapleAsciiString()
                text = slea.readMapleAsciiString()
                ch = World.Find.findChannel(recipient)
                if ch <= 0:
                    c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 0))
                    break
                player2 = ChannelServer.getInstance(ch).getPlayerStorage().getCharacterByName(recipient)
                if player2 is None:
                    break
                player2.getClient().getSession().write(MaplePacketCreator.getWhisper(c.getPlayer().getName(), c.getChannel(), text))
                if !c.getPlayer().isGM() && player2.isGM():
                    c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 0))
                else:
                    c.getSession().write(MaplePacketCreator.getWhisperReply(recipient, 1))
                break

