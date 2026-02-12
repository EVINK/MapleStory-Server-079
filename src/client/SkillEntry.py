"""
SkillEntry - Converted from Java source
Original: client/SkillEntry.java
Package: client
"""

from typing import Optional, Any


class SkillEntry:
    """
    Class SkillEntry
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, skillevel: int, masterlevel: int, expiration: int):
        self.skillevel = 0
        self.masterlevel = 0
        self.expiration = 0
        self.skillevel = skillevel
        self.masterlevel = masterlevel
        self.expiration = expiration


