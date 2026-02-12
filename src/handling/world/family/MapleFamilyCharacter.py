"""
MapleFamilyCharacter - 从Java源文件转换而来
对应Java源文件: handling/world/family/MapleFamilyCharacter.java
包路径: handling.world.family
"""

from typing import List
from typing import Optional, List, Dict, Any, Set
import math

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类


class MapleFamilyCharacter:
    """
    类 MapleFamilyCharacter - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, c: Any, fid: int, sid: int, j1: int, j2: int):
        """初始化 MapleFamilyCharacter"""
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


    def getLevel(self) -> int:
        """方法 getLevel"""
        return getattr(self, 'level', 0)

    def setLevel(self, l: int) -> None:
        """方法 setLevel"""
        self.level = l
        return None

    def getId(self) -> int:
        """方法 getId"""
        return getattr(self, 'id', 0)

    def setChannel(self, ch: int) -> None:
        """方法 setChannel"""
        self.channel = ch
        return None

    def getChannel(self) -> int:
        """方法 getChannel"""
        return getattr(self, 'channel', 0)

    def getJobId(self) -> int:
        """方法 getJobId"""
        return getattr(self, 'job_id', 0)

    def setJobId(self, job: int) -> None:
        """方法 setJobId"""
        self.job_id = job
        return None

    def getCurrentRep(self) -> int:
        """方法 getCurrentRep"""
        return getattr(self, 'current_rep', 0)

    def setCurrentRep(self, cr: int) -> None:
        """方法 setCurrentRep"""
        self.current_rep = cr
        return None

    def getTotalRep(self) -> int:
        """方法 getTotalRep"""
        return getattr(self, 'total_rep', 0)

    def setTotalRep(self, tr: int) -> None:
        """方法 setTotalRep"""
        self.total_rep = tr
        return None

    def getJunior1(self) -> int:
        """方法 getJunior1"""
        return getattr(self, 'junior1', 0)

    def getJunior2(self) -> int:
        """方法 getJunior2"""
        return getattr(self, 'junior2', 0)

    def setJunior1(self, trs: int) -> None:
        """方法 setJunior1"""
        self.junior1 = trs
        return None

    def setJunior2(self, trs: int) -> None:
        """方法 setJunior2"""
        self.junior2 = trs
        return None

    def getSeniorId(self) -> int:
        """方法 getSeniorId"""
        return getattr(self, 'senior_id', 0)

    def setSeniorId(self, si: int) -> None:
        """方法 setSeniorId"""
        self.senior_id = si
        return None

    def getFamilyId(self) -> int:
        """方法 getFamilyId"""
        return getattr(self, 'family_id', 0)

    def setFamilyId(self, fi: int) -> None:
        """方法 setFamilyId"""
        self.family_id = fi
        return None

    def isOnline(self) -> bool:
        """方法 isOnline"""
        return bool(getattr(self, 'online', False))

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def equals(self, other: Any) -> bool:
        """方法 equals"""
        return self is other or getattr(self, '__eq__', lambda o: False)(other)

    def setOnline(self, f: bool) -> None:
        """方法 setOnline"""
        self.online = f
        return None

    def getAllJuniors(self, fam: Any) -> list:
        """方法 getAllJuniors"""
        return []

    def getOnlineJuniors(self, fam: Any) -> list:
        """方法 getOnlineJuniors"""
        return []

    def getPedigree(self) -> list:
        """方法 getPedigree"""
        return getattr(self, 'pedigree', [])

    def resetPedigree(self, fam: Any) -> None:
        """方法 resetPedigree"""
        pass

    def getDescendants(self) -> int:
        """方法 getDescendants"""
        return getattr(self, 'descendants', 0)

    def resetDescendants(self, fam: Any) -> int:
        """方法 resetDescendants"""
        return 0

    def resetGenerations(self, fam: Any) -> int:
        """方法 resetGenerations"""
        return 0

    def getNoJuniors(self) -> int:
        """方法 getNoJuniors"""
        return getattr(self, 'no_juniors', 0)

