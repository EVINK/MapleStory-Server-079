"""
Triple - Converted from Java source
Original: tools/Triple.java
Package: tools
"""

from typing import Optional, Any


class Triple:
    """
    Class Triple
    Implements: Serializable
    """

    serialVersionUID = 9179541993413739999

    def __init__(self, left: Any, mid: Any, right: Any):
        self.left = None
        self.mid = None
        self.right = None
        self.left = left
        self.mid = mid
        self.right = right


    def getLeft(self) -> Any:
        return self.left

    def getMid(self) -> Any:
        return self.mid

    def getRight(self) -> Any:
        return self.right

    def toString(self) -> str:
        return self.left + ":" + self.mid + ":" + self.right

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = 31 * result + ((self.left is None) ? 0 : self.left.hashCode())
        result = 31 * result + ((self.mid is None) ? 0 : self.mid.hashCode())
        result = 31 * result + ((self.right is None) ? 0 : self.right.hashCode())
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        if self.left is None:
            if other.left is not None:
                return False
        elif !self.left == (other.left):
            return False
        if self.mid is None:
            if other.mid is not None:
                return False
        elif !self.mid == (other.mid):
            return False
        if self.right is None:
            if other.right is not None:
                return False
        elif !self.right == (other.right):
            return False
        return True

