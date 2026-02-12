"""
BBSHandler - Converted from Java source
Original: handling/channel/handler/BBSHandler.java
Package: handling.channel.handler
"""

from typing import Iterator
from typing import List
from typing import Optional, Any
import threading

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleBBSThread import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class BBSHandler:
    """
    Class BBSHandler
    """


    def correctLength(self, in: str, maxSize: int) -> str:
        if in > maxSize:
            return in[0:maxSize]
        return in

    def BBSOperatopn(self, slea: Any, c: Any) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        localthreadid = 0
        action = slea.readByte()
        # switch (action):
            # case 0:
                bEdit = slea.readByte() > 0
                if bEdit:
                    localthreadid = slea.readInt()
                bNotice = slea.readByte() > 0
                title = correctLength(slea.readMapleAsciiString(), 25)
                text = correctLength(slea.readMapleAsciiString(), 600)
                icon = slea.readInt()
                if icon >= 100 and icon <= 106:
                    if not c.getPlayer().haveItem(5290000 + icon - 100, 1, False, True):
                        return
                elif icon < 0 or icon > 2:
                    return
                if not bEdit:
                    newBBSThread(c, title, text, icon, bNotice)
                    break
                editBBSThread(c, title, text, icon, localthreadid)
                break
            # case 1:
                localthreadid = slea.readInt()
                deleteBBSThread(c, localthreadid)
                break
            # case 2:
                start = slea.readInt()
                listBBSThreads(c, start * 10)
                break
            # case 3:
                localthreadid = slea.readInt()
                displayThread(c, localthreadid)
                break
            # case 4:
                localthreadid = slea.readInt()
                text = correctLength(slea.readMapleAsciiString(), 25)
                newBBSReply(c, localthreadid, text)
                break
            # case 5:
                localthreadid = slea.readInt()
                replyid = slea.readInt()
                deleteBBSReply(c, localthreadid, replyid)
                break

    def listBBSThreads(self, c: Any, start: int) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        c.getSession().write(MaplePacketCreator.BBSThreadList(World.Guild.getBBS(c.getPlayer().getGuildId()), start))

    def newBBSReply(self, c: Any, localthreadid: int, text: str) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        World.Guild.addBBSReply(c.getPlayer().getGuildId(), localthreadid, text, c.getPlayer().getId())
        displayThread(c, localthreadid)

    def editBBSThread(self, c: Any, title: str, text: str, icon: int, localthreadid: int) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        World.Guild.editBBSThread(c.getPlayer().getGuildId(), localthreadid, title, text, icon, c.getPlayer().getId(), c.getPlayer().getGuildRank())
        displayThread(c, localthreadid)

    def newBBSThread(self, c: Any, title: str, text: str, icon: int, bNotice: bool) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        displayThread(c, World.Guild.addBBSThread(c.getPlayer().getGuildId(), title, text, icon, bNotice, c.getPlayer().getId()))

    def deleteBBSThread(self, c: Any, localthreadid: int) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        World.Guild.deleteBBSThread(c.getPlayer().getGuildId(), localthreadid, c.getPlayer().getId(), c.getPlayer().getGuildRank())

    def deleteBBSReply(self, c: Any, localthreadid: int, replyid: int) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        World.Guild.deleteBBSReply(c.getPlayer().getGuildId(), localthreadid, replyid, c.getPlayer().getId(), c.getPlayer().getGuildRank())
        displayThread(c, localthreadid)

    def displayThread(self, c: Any, localthreadid: int) -> None:
        if c.getPlayer().getGuildId() <= 0:
            return
        bbsList = World.Guild.getBBS(c.getPlayer().getGuildId())
        if bbsList is not None:
            for t in bbsList:
                if t is not None and t.localthreadID == localthreadid:
                    c.getSession().write(MaplePacketCreator.showThread(t))

