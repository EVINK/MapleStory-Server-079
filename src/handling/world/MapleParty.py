"""
MapleParty - Converted from Java source
Original: handling/world/MapleParty.java
Package: handling.world
"""

from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any


class MapleParty:
    """
    Class MapleParty
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, id: int, chrfor: Any):
        self.leader = None
        self.members = None
        self.id = 0
        self.partyBuffs = None
        self.members = []
        self.partyBuffs = new HashMap<Integer, Map<Integer, List<Integer>>>()
        self.leader = chrfor
        self.members.add(self.leader)
        self.id = id


    def containsMembers(self, member: Any) -> bool:
        return (member in self.members)

    def addMember(self, member: Any) -> None:
        self.members.add(member)

    def removeMember(self, member: Any) -> None:
        self.members.remove(member)

    def updateMember(self, member: Any) -> None:
        for i in range(self.members):
            chr = self.members.get(i)
            if chr == (member):
                self.members.set(i, member)

    def getMemberById(self, id: int) -> Any:
        for chr in self.members:
            if chr.getId() == id:
                return chr
        return None

    def getMemberByIndex(self, index: int) -> Any:
        return self.members.get(index)

    def getMembers(self) -> list:
        return []

    def getId(self) -> int:
        return self.id

    def setId(self, id: int) -> None:
        self.id = id

    def getLeader(self) -> Any:
        return self.leader

    def setLeader(self, nLeader: Any) -> None:
        self.leader = nLeader

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + self.id
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.id == other.id

    def givePartyBuff(self, buffId: int, applyfrom: int, applyto: int) -> None:
        if (buffId in self.partyBuffs):
            if self.partyBuffs.get(buffId).__contains__(applyfrom):
                if !self.partyBuffs.get(buffId).keys() == 0:
                    for from in self.partyBuffs.get(buffId).keys():
                        if self.partyBuffs.get(buffId).get(from).__contains__(applyto):
                            self.partyBuffs.get(buffId).get(from).remove(self.partyBuffs.get(buffId).get(from).find(applyto))
                        if self.partyBuffs.get(buffId).get(from) == 0:
                            self.partyBuffs.get(buffId).remove(from)
                if self.partyBuffs is not None && !self.partyBuffs.get(buffId).get(applyfrom).__contains__(applyto):
                    self.partyBuffs.get(buffId).get(applyfrom).add(applyto)
            else:
                applytos = []
                applytos.add(applyto)
                self.partyBuffs.get(buffId).put(applyfrom, applytos)
        else:
            hMap = new HashMap<Integer, List<Integer>>()
            applytos2 = []
            applytos2.add(applyto)
            hMap.put(applyfrom, applytos2)
            self.partyBuffs.put(buffId, hMap)

