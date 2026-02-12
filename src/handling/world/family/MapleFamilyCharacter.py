"""
MapleFamilyCharacter - Converted from Java source
Original: handling/world/family/MapleFamilyCharacter.java
Package: handling.world.family
"""

from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes


class MapleFamilyCharacter:
    """
    Class MapleFamilyCharacter
    Implements: Serializable
    """

    def __init__(self, c: Any, fid: int, sid: int, j1: int, j2: int):
        self.level = 0
        self.id = 0
        self.channel = 0
        self.jobid = 0
        self.familyid = 0
        self.seniorid = 0
        self.currentrep = 0
        self.totalrep = 0
        self.junior1 = 0
        self.junior2 = 0
        self.online = False
        self.name = ""
        self.pedigree = []
        self.descendants = 0
        self.channel = -1
        self.pedigree = []
        self.descendants = 0
        self.name = c.getName()
        self.level = c.getLevel()
        self.id = c.getId()
        self.channel = c.getClient().getChannel()
        self.jobid = c.getJob()
        self.familyid = fid
        self.junior1 = j1
        self.junior2 = j2
        self.seniorid = sid
        self.currentrep = c.getCurrentRep()
        self.totalrep = c.getTotalRep()
        self.online = True

    # Static initializer
    # MapleFamilyCharacter.serialVersionUID = 2058609046116597760


    def getLevel(self) -> int:
        return self.level

    def setLevel(self, l: int) -> None:
        self.level = l

    def getId(self) -> int:
        return self.id

    def setChannel(self, ch: int) -> None:
        self.channel = ch

    def getChannel(self) -> int:
        return self.channel

    def getJobId(self) -> int:
        return self.jobid

    def setJobId(self, job: int) -> None:
        self.jobid = job

    def getCurrentRep(self) -> int:
        return self.currentrep

    def setCurrentRep(self, cr: int) -> None:
        self.currentrep = cr

    def getTotalRep(self) -> int:
        return self.totalrep

    def setTotalRep(self, tr: int) -> None:
        self.totalrep = tr

    def getJunior1(self) -> int:
        return self.junior1

    def getJunior2(self) -> int:
        return self.junior2

    def setJunior1(self, trs: int) -> None:
        self.junior1 = trs

    def setJunior2(self, trs: int) -> None:
        self.junior2 = trs

    def getSeniorId(self) -> int:
        return self.seniorid

    def setSeniorId(self, si: int) -> None:
        self.seniorid = si

    def getFamilyId(self) -> int:
        return self.familyid

    def setFamilyId(self, fi: int) -> None:
        self.familyid = fi

    def isOnline(self) -> bool:
        return self.online

    def getName(self) -> str:
        return self.name

    def equals(self, other: Any) -> bool:
        if !(isinstance(other, MapleFamilyCharacter)):
            return False
        o = other
        return o.getId() == self.id && o.getName() == (self.name)

    def setOnline(self, f: bool) -> None:
        self.online = f

    def getAllJuniors(self, fam: Any) -> list:
        ret = []
        ret.add(this)
        if self.junior1 > 0:
            chr = fam.getMFC(self.junior1)
            if chr is not None:
                ret.addAll(chr.getAllJuniors(fam))
        if self.junior2 > 0:
            chr = fam.getMFC(self.junior2)
            if chr is not None:
                ret.addAll(chr.getAllJuniors(fam))
        return ret

    def getOnlineJuniors(self, fam: Any) -> list:
        ret = []
        ret.add(this)
        if self.junior1 > 0:
            chr = fam.getMFC(self.junior1)
            if chr is not None:
                if chr.isOnline():
                    ret.add(chr)
                if chr.getJunior1() > 0:
                    chr2 = fam.getMFC(chr.getJunior1())
                    if chr2 is not None && chr2.isOnline():
                        ret.add(chr2)
                if chr.getJunior2() > 0:
                    chr2 = fam.getMFC(chr.getJunior2())
                    if chr2 is not None && chr2.isOnline():
                        ret.add(chr2)
        if self.junior2 > 0:
            chr = fam.getMFC(self.junior2)
            if chr is not None:
                if chr.isOnline():
                    ret.add(chr)
                if chr.getJunior1() > 0:
                    chr2 = fam.getMFC(chr.getJunior1())
                    if chr2 is not None && chr2.isOnline():
                        ret.add(chr2)
                if chr.getJunior2() > 0:
                    chr2 = fam.getMFC(chr.getJunior2())
                    if chr2 is not None && chr2.isOnline():
                        ret.add(chr2)
        return ret

    def getPedigree(self) -> list:
        return self.pedigree

    def resetPedigree(self, fam: Any) -> None:
        (self.pedigree = []).add(self.id)
        if self.seniorid > 0:
            chr = fam.getMFC(self.seniorid)
            if chr is not None:
                self.pedigree.add(self.seniorid)
                if chr.getSeniorId() > 0:
                    self.pedigree.add(chr.getSeniorId())
                if chr.getJunior1() > 0 && chr.getJunior1() != self.id:
                    self.pedigree.add(chr.getJunior1())
                elif chr.getJunior2() > 0 && chr.getJunior2() != self.id:
                    self.pedigree.add(chr.getJunior2())
        if self.junior1 > 0:
            chr = fam.getMFC(self.junior1)
            if chr is not None:
                self.pedigree.add(self.junior1)
                if chr.getJunior1() > 0:
                    self.pedigree.add(chr.getJunior1())
                if chr.getJunior2() > 0:
                    self.pedigree.add(chr.getJunior2())
        if self.junior2 > 0:
            chr = fam.getMFC(self.junior2)
            if chr is not None:
                self.pedigree.add(self.junior2)
                if chr.getJunior1() > 0:
                    self.pedigree.add(chr.getJunior1())
                if chr.getJunior2() > 0:
                    self.pedigree.add(chr.getJunior2())

    def getDescendants(self) -> int:
        return self.descendants

    def resetDescendants(self, fam: Any) -> int:
        self.descendants = 0
        if self.junior1 > 0:
            chr = fam.getMFC(self.junior1)
            if chr is not None:
                self.descendants += 1 + chr.resetDescendants(fam)
        if self.junior2 > 0:
            chr = fam.getMFC(self.junior2)
            if chr is not None:
                self.descendants += 1 + chr.resetDescendants(fam)
        return self.descendants

    def resetGenerations(self, fam: Any) -> int:
        descendants1 = 0, descendants2 = 0
        if self.junior1 > 0:
            chr = fam.getMFC(self.junior1)
            if chr is not None:
            descendants1 = chr.resetGenerations(fam)
        if self.junior2 > 0:
            chr = fam.getMFC(self.junior2)
            if chr is not None:
            descendants2 = chr.resetGenerations(fam)
        ret = max(descendants1, descendants2)
        return ret + ((ret > 0) ? 1 : 0)

    def getNoJuniors(self) -> int:
        ret = 0
        if self.junior1 > 0:
            ret += 1
        if self.junior2 > 0:
            ret += 1
        return ret

