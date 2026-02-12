"""
MapleBBSThread - Converted from Java source
Original: handling/world/guild/MapleBBSThread.java
Package: handling.world.guild
"""

from typing import Dict
from typing import List
from typing import Optional, Any
import threading


class MapleBBSThread:
    """
    Class MapleBBSThread
    Implements: Serializable
    """

    def __init__(self, localthreadID: int, name: str, text: str, timestamp: int, guildID: int, ownerID: int, icon: int):
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
        self.replies = {}
        self.localthreadID = localthreadID
        self.name = name
        self.text = text
        self.timestamp = timestamp
        self.guildID = guildID
        self.ownerID = ownerID
        self.icon = icon

    # Static initializer
    # MapleBBSThread.serialVersionUID = 3565477792085301248


    def getReplyCount(self) -> int:
        return self.replies

    def isNotice(self) -> bool:
        return self.localthreadID == 0

    def compare(self, o1: Any, o2: Any) -> int:
        if o1.localthreadID < o2.localthreadID:
            return 1
        if o1.localthreadID == o2.localthreadID:
            return 0
        return -1


# Inner class from Java (originally nested)
class MapleBBSReply:
    """
    Class MapleBBSReply
    Implements: Serializable
    """

    def __init__(self, replyid: int, ownerID: int, content: str, timestamp: int):
        self.replyid = 0
        self.ownerID = 0
        self.timestamp = 0
        self.content = ""
        self.ownerID = ownerID
        self.replyid = replyid
        self.content = content
        self.timestamp = timestamp



# Inner class from Java (originally nested)
class ThreadComparator(Comparator):
    """
    Class ThreadComparator
    Implements: Comparator<MapleBBSThread>, Serializable
    """


    def compare(self, o1: Any, o2: Any) -> int:
        if o1.localthreadID < o2.localthreadID:
            return 1
        if o1.localthreadID == o2.localthreadID:
            return 0
        return -1

