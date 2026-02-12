"""
CharacterNameAndId - Converted from Java source
Original: client/CharacterNameAndId.java
Package: client
"""

from typing import Optional, Any


class CharacterNameAndId:
    """
    Class CharacterNameAndId
    """

    def __init__(self, id: int, name: str, level: int, job: int, group: str):
        self.id = None
        self.level = None
        self.job = None
        self.name = None
        self.group = None
        self.id = id
        self.name = name
        self.level = level
        self.job = job
        self.group = group


    def getId(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def getGroup(self) -> str:
        return self.group

    def getLevel(self) -> int:
        return self.level

    def getJob(self) -> int:
        return self.job

