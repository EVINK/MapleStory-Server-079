"""
BuddyListHandler - Converted from Java source
Original: handling/channel/handler/BuddyListHandler.java
Package: handling.channel.handler
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.BuddyEntry import *  # TODO: import specific classes
# from client.BuddyList import *  # TODO: import specific classes
# from client.CharacterNameAndId import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class BuddyListHandler:
    """
    Class BuddyListHandler
    """

    def __init__(self):
        self.buddyCapacity = None


    def nextPendingRequest(self, c: Any) -> None:
        pendingBuddyRequest = c.getPlayer().getBuddylist().pollPendingRequest()
        if pendingBuddyRequest is not None:
            c.getSession().write(MaplePacketCreator.requestBuddylistAdd(pendingBuddyRequest.getCharacterId(), pendingBuddyRequest.getName(), pendingBuddyRequest.getLevel(), pendingBuddyRequest.getJob()))

    def getCharacterIdAndNameFromDatabase(self, name: str, group: str) -> Any:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT * FROM characters WHERE name LIKE ?")
        ps.setString(1, name)
        rs = ps.executeQuery()
        ret = None
        if rs.next() && rs.getInt("gm") == 0:
            ret = CharacterIdNameBuddyCapacity(rs.getInt("id"), rs.getString("name"), rs.getInt("level"), rs.getInt("job"), group, rs.getInt("buddyCapacity"))
        rs.close()
        ps.close()
        return ret

    def BuddyOperation(self, slea: Any, c: Any) -> None:
        mode = slea.readByte()
        buddylist = c.getPlayer().getBuddylist()
        # switch (mode):
            # case 1:
                addName = slea.readMapleAsciiString()
                groupName = slea.readMapleAsciiString()
                ble = buddylist.get(addName)
                if addName > 13 || groupName > 16:
                    return
                if ble is not None && (ble.getGroup() == (groupName) || !ble.isVisible()):
                    c.getSession().write(MaplePacketCreator.buddylistMessage(11))
                elif ble is not None && ble.isVisible():
                    ble.setGroup(groupName)
                    c.getSession().write(MaplePacketCreator.updateBuddylist(buddylist.getBuddies()))
                    c.getSession().write(MaplePacketCreator.buddylistMessage(13))
                elif buddylist.isFull():
                    c.getSession().write(MaplePacketCreator.buddylistMessage(11))
                else:
                    try:
                        charWithId = None
                        channel = World.Find.findChannel(addName)
                        otherChar = None
                        if channel > 0:
                            otherChar = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterByName(addName)
                            if !otherChar.isGM() || c.getPlayer().isGM():
                                charWithId = CharacterIdNameBuddyCapacity(otherChar.getId(), otherChar.getName(), otherChar.getLevel(), otherChar.getJob(), groupName, otherChar.getBuddylist().getCapacity())
                        else:
                            charWithId = getCharacterIdAndNameFromDatabase(addName, groupName)
                        if charWithId is not None:
                            BuddyList.BuddyAddResult buddyAddResult = None
                            if channel > 0:
                                buddyAddResult = World.Buddy.requestBuddyAdd(addName, c.getChannel(), c.getPlayer().getId(), c.getPlayer().getName(), c.getPlayer().getLevel(), c.getPlayer().getJob())
                            else:
                                con = DatabaseConnection.getConnection()
                                ps = con.prepareStatement("SELECT COUNT(*) as buddyCount FROM buddies WHERE characterid = ? AND pending = 0")
                                ps.setInt(1, charWithId.getId())
                                rs = ps.executeQuery()
                                if !rs.next():
                                    ps.close()
                                    rs.close()
                                    raise RuntimeError("Result set expected")
                                count = rs.getInt("buddyCount")
                                if count >= charWithId.getBuddyCapacity():
                                    buddyAddResult = BuddyList.BuddyAddResult.BUDDYLIST_FULL
                                rs.close()
                                ps.close()
                                ps = con.prepareStatement("SELECT pending FROM buddies WHERE characterid = ? AND buddyid = ?")
                                ps.setInt(1, charWithId.getId())
                                ps.setInt(2, c.getPlayer().getId())
                                rs = ps.executeQuery()
                                if rs.next():
                                    buddyAddResult = BuddyList.BuddyAddResult.ALREADY_ON_LIST
                                rs.close()
                                ps.close()
                            if buddyAddResult == BuddyList.BuddyAddResult.BUDDYLIST_FULL:
                                c.getSession().write(MaplePacketCreator.buddylistMessage(12))
                            else:
                                displayChannel = -1
                                otherCid = charWithId.getId()
                                if buddyAddResult == BuddyList.BuddyAddResult.ALREADY_ON_LIST && channel > 0:
                                    displayChannel = channel
                                    notifyRemoteChannel(c, channel, otherCid, groupName, BuddyList.BuddyOperation.ADDED)
                                elif buddyAddResult != BuddyList.BuddyAddResult.ALREADY_ON_LIST && channel > 0:
                                    con2 = DatabaseConnection.getConnection()
                                    ps2 = con2.prepareStatement("INSERT INTO buddies (`characterid`, `buddyid`, `groupname`, `pending`) VALUES (?, ?, ?, 1)")
                                    ps2.setInt(1, charWithId.getId())
                                    ps2.setInt(2, c.getPlayer().getId())
                                    ps2.setString(3, groupName)
                                    ps2.executeUpdate()
                                    ps2.close()
                                buddylist.put(BuddyEntry(charWithId.getName(), otherCid, groupName, displayChannel, True, charWithId.getLevel(), charWithId.getJob()))
                                c.getSession().write(MaplePacketCreator.updateBuddylist(buddylist.getBuddies()))
                        else:
                            c.getSession().write(MaplePacketCreator.buddylistMessage(15))
                    except Exception as e:
                        print("SQL THROW" + e)
                nextPendingRequest(c)
                break
            # case 2:
                otherCid2 = slea.readInt()
                if !buddylist.isFull():
                    try:
                        channel = World.Find.findChannel(otherCid2)
                        otherName = None
                        otherLevel = 0
                        otherJob = 0
                        if channel < 0:
                            con3 = DatabaseConnection.getConnection()
                            ps3 = con3.prepareStatement("SELECT name, level, job FROM characters WHERE id = ?")
                            ps3.setInt(1, otherCid2)
                            rs2 = ps3.executeQuery()
                            if rs2.next():
                                otherName = rs2.getString("name")
                                otherLevel = rs2.getInt("level")
                                otherJob = rs2.getInt("job")
                            rs2.close()
                            ps3.close()
                        else:
                            otherChar2 = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterById(otherCid2)
                            otherName = otherChar2.getName()
                            otherLevel = otherChar2.getLevel()
                            otherJob = otherChar2.getJob()
                        if otherName is not None:
                            buddylist.put(BuddyEntry(otherName, otherCid2, BuddyList.DEFAULT_GROUP, channel, True, otherLevel, otherJob))
                            c.getSession().write(MaplePacketCreator.updateBuddylist(buddylist.getBuddies()))
                            notifyRemoteChannel(c, channel, otherCid2, BuddyList.DEFAULT_GROUP, BuddyList.BuddyOperation.ADDED)
                    except Exception as e2:
                        print("SQL THROW" + e2)
                else:
                    c.getSession().write(MaplePacketCreator.buddylistMessage(11))
                nextPendingRequest(c)
                break
            # case 3:
                otherCid2 = slea.readInt()
                blz = buddylist.get(otherCid2)
                if blz is not None && blz.isVisible():
                    notifyRemoteChannel(c, World.Find.findChannel(otherCid2), otherCid2, blz.getGroup(), BuddyList.BuddyOperation.DELETED)
                buddylist.remove(otherCid2)
                c.getSession().write(MaplePacketCreator.updateBuddylist(c.getPlayer().getBuddylist().getBuddies()))
                nextPendingRequest(c)
                break
            # default:
                print("Unknown buddylist: " + slea)
                break

    def notifyRemoteChannel(self, c: Any, remoteChannel: int, otherCid: int, group: str, operation: Any) -> None:
        player = c.getPlayer()
        if remoteChannel > 0:
            World.Buddy.buddyChanged(otherCid, player.getId(), player.getName(), c.getChannel(), operation, player.getLevel(), player.getJob(), group)

    def getBuddyCapacity(self) -> int:
        return self.buddyCapacity


# Inner class from Java (originally nested)
class CharacterIdNameBuddyCapacity(CharacterNameAndId):
    """
    Class CharacterIdNameBuddyCapacity
    Extends: CharacterNameAndId
    """

    def __init__(self, id: int, name: str, level: int, job: int, group: str, buddyCapacity: int):
        self.buddyCapacity = None
        super(id, name, level, job, group)
        self.buddyCapacity = buddyCapacity


    def getBuddyCapacity(self) -> int:
        return self.buddyCapacity

