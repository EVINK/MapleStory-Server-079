"""
Pair - 从Java源文件转换而来
对应Java源文件: tools/Pair.java
包路径: tools
"""

from typing import Optional, Any


class Pair:
    """
    类 Pair - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = 9179541993413738569

    def __init__(self, left: Any, right: Any):
        """初始化 Pair"""
        self.left = None
        self.right = None


    def getLeft(self) -> Any:
        """方法 getLeft"""
        return getattr(self, 'left', None)

    def getRight(self) -> Any:
        """方法 getRight"""
        return getattr(self, 'right', None)

    def toString(self) -> str:
        """方法 toString"""
        return ""

    def hashCode(self) -> int:
        """方法 hashCode"""
        return hash(self)

    def equals(self, obj: Any) -> bool:
        """方法 equals"""
        return self is obj or getattr(self, '__eq__', lambda o: False)(obj)

