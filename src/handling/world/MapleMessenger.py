"""
MapleMessenger - Converted from Java source
Original: handling/world/MapleMessenger.java
Package: handling.world
"""

from typing import Collection
from typing import Optional, Any


class MapleMessenger:
    """
    Class MapleMessenger
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, id: int, chrfor: Any):
        self.id = 0
        self.members = new MapleMessengerCharacter[3]
        self.silentLink = new String[3]
        self.id = id
        self.addMem(0, chrfor)


    def addMem(self, pos: int, chrfor: Any) -> None:
        if self.members[pos] is not None:
            return
        self.members[pos] = chrfor

    def containsMembers(self, member: Any) -> bool:
        return self.getPositionByName(member.getName()) < 4

    def addMember(self, member: Any) -> None:
        position = self.getLowestPosition()
        if position > -1 and position < 4:
            self.addMem(position, member)

    def removeMember(self, member: Any) -> None:
        position = self.getPositionByName(member.getName())
        if position > -1 and position < 4:
            self.members[position] = None

    def silentRemoveMember(self, member: Any) -> None:
        position = self.getPositionByName(member.getName())
        if position > -1 and position < 4:
            self.members[position] = None
            self.silentLink[position] = member.getName()

    def silentAddMember(self, member: Any) -> None:
        for i in range(self.len(silentLink)):
            if self.silentLink[i] is not None and self.silentLink[i].lower() == member.getName(.lower()):
                self.addMem(i, member)
                self.silentLink[i] = None
                return

    def updateMember(self, member: Any) -> None:
        for i in range(self.len(members)):
            chr = self.members[i]
            if chr == (member):
                self.members[i] = None
                self.addMem(i, member)
                return

    def getLowestPosition(self) -> int:
        for i in range(self.len(members)):
            if self.members[i] is None:
                return i
        return 4

    def getPositionByName(self, name: str) -> int:
        for i in range(self.len(members)):
            messengerchar = self.members[i]
            if messengerchar is not None and messengerchar.getName().lower() == name.lower():
                return i
        return 4

    def getId(self) -> int:
        return self.id

    def setId(self, id: int) -> None:
        self.id = id

    def hashCode(self) -> int:
        return 31 + self.id

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.id == other.id

    def getMembers(self) -> list:
        return Arrays.asList(self.members)

