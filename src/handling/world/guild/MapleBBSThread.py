"""
MapleBBSThread - 从Java源文件转换而来
对应Java源文件: handling/world/guild/MapleBBSThread.java
包路径: handling.world.guild
"""

from typing import Dict
from typing import List
from typing import Optional, List, Dict, Any, Set
import threading


class MapleBBSThread:
    """
    类 MapleBBSThread - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, localthreadID: int, name: str, text: str, timestamp: int, guildID: int, ownerID: int, icon: int):
        """初始化 MapleBBSThread"""
        self.name = ""
        self.text = ""
        self.timestamp = 0
        self.localthreadID = 0
        self.guildID = 0
        self.ownerID = 0
        self.icon = 0
        self.replies = {}
        self.replyid = 0
        self.ownerID = 0
        self.timestamp = 0
        self.content = ""


    def getReplyCount(self) -> int:
        """方法 getReplyCount"""
        return getattr(self, 'reply_count', 0)

    def isNotice(self) -> bool:
        """方法 isNotice"""
        return bool(getattr(self, 'notice', False))

    def compare(self, o1: Any, o2: Any) -> int:
        """方法 compare"""
        return 0


class MapleBBSReply:
    """
    类 MapleBBSReply - 从Java类转换
    实现接口: Serializable
    """

    def __init__(self, replyid: int, ownerID: int, content: str, timestamp: int):
        """初始化 MapleBBSReply"""
        self.name = ""
        self.text = ""
        self.timestamp = 0
        self.localthreadID = 0
        self.guildID = 0
        self.ownerID = 0
        self.icon = 0
        self.replies = {}
        self.replyid = 0
        self.ownerID = 0
        self.timestamp = 0
        self.content = ""


    def getReplyCount(self) -> int:
        """方法 getReplyCount"""
        return getattr(self, 'reply_count', 0)

    def isNotice(self) -> bool:
        """方法 isNotice"""
        return bool(getattr(self, 'notice', False))

    def compare(self, o1: Any, o2: Any) -> int:
        """方法 compare"""
        return 0


class ThreadComparator(Comparator):
    """
    类 ThreadComparator - 从Java类转换
    实现接口: Comparator<MapleBBSThread>, Serializable
    """

    def __init__(self):
        """初始化 ThreadComparator"""
        self.name = ""
        self.text = ""
        self.timestamp = 0
        self.localthreadID = 0
        self.guildID = 0
        self.ownerID = 0
        self.icon = 0
        self.replies = {}
        self.replyid = 0
        self.ownerID = 0
        self.timestamp = 0
        self.content = ""


    def getReplyCount(self) -> int:
        """方法 getReplyCount"""
        return getattr(self, 'reply_count', 0)

    def isNotice(self) -> bool:
        """方法 isNotice"""
        return bool(getattr(self, 'notice', False))

    def compare(self, o1: Any, o2: Any) -> int:
        """方法 compare"""
        return 0

