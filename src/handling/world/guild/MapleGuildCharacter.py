"""
MapleGuildCharacter - 从Java源文件转换而来
对应Java源文件: handling/world/guild/MapleGuildCharacter.java
包路径: handling.world.guild
"""

# 内部模块导入 (Internal module imports)
# from client.MapleCharacter import *  # TODO: 根据实际需要导入具体类


class MapleGuildCharacter:
    """
    类 MapleGuildCharacter - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, c: Any):
        """初始化 MapleGuildCharacter"""
        self.channel = 0
        self.guildrank = 0
        self.allianceRank = 0
        self.level = 0
        self.id = 0
        self.jobid = 0
        self.guildid = 0
        self.online = False
        self.name = ""


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

    def getGuildId(self) -> int:
        """方法 getGuildId"""
        return getattr(self, 'guild_id', 0)

    def setGuildId(self, gid: int) -> None:
        """方法 setGuildId"""
        self.guild_id = gid
        return None

    def setGuildRank(self, rank: int) -> None:
        """方法 setGuildRank"""
        self.guild_rank = rank
        return None

    def getGuildRank(self) -> int:
        """方法 getGuildRank"""
        return getattr(self, 'guild_rank', 0)

    def isOnline(self) -> bool:
        """方法 isOnline"""
        return bool(getattr(self, 'online', False))

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def setOnline(self, f: bool) -> None:
        """方法 setOnline"""
        self.online = f
        return None

    def setAllianceRank(self, rank: int) -> None:
        """方法 setAllianceRank"""
        self.alliance_rank = rank
        return None

    def getAllianceRank(self) -> int:
        """方法 getAllianceRank"""
        return getattr(self, 'alliance_rank', 0)

