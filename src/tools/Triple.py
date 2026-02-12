"""
Triple - 从Java源文件转换而来
对应Java源文件: tools/Triple.java
包路径: tools
"""

from typing import Optional, Any


class Triple:
    """
    类 Triple - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = 9179541993413739999

    def __init__(self, left: Any, mid: Any, right: Any):
        """初始化 Triple"""
        self.left = None
        self.mid = None
        self.right = None


    def getLeft(self) -> Any:
        """方法 getLeft"""
        raise NotImplementedError("方法 getLeft 尚未实现")

    def getMid(self) -> Any:
        """方法 getMid"""
        raise NotImplementedError("方法 getMid 尚未实现")

    def getRight(self) -> Any:
        """方法 getRight"""
        raise NotImplementedError("方法 getRight 尚未实现")

    def toString(self) -> str:
        """方法 toString"""
        return ""

    def hashCode(self) -> int:
        """方法 hashCode"""
        return 0

    def equals(self, obj: Any) -> bool:
        """方法 equals"""
        return False

