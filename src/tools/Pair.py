"""
Pair - Converted from Java source
Original: tools/Pair.java
Package: tools
"""

from typing import Optional, Any


class Pair:
    """
    Class Pair
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, left: Any, right: Any):
        self.left = None
        self.right = None
        self.left = left
        self.right = right


    def getLeft(self) -> Any:
        return self.left

    def getRight(self) -> Any:
        return self.right

    def toString(self) -> str:
        return self.left + ":" + self.right

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + ((self.left is None) ? 0 : self.left.hashCode())
        result = prime * result + ((self.right is None) ? 0 : self.right.hashCode())
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
        elif not self.left == (other.left):
            return False
        if self.right is None:
            if other.right is not None:
                return False
        elif not self.right == (other.right):
            return False
        return True

