"""
ArrayMap - 从Java源文件转换而来
对应Java源文件: tools/ArrayMap.java
包路径: tools
"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, List, Dict, Any, Set
from typing import Set


class ArrayMap(AbstractMap):
    """
    类 ArrayMap - 从Java类转换
    继承自: AbstractMap<K, V>
    实现接口: Serializable
    """

    def __init__(self):
        """初始化 ArrayMap"""
        self.list = []
        self.key = None
        self.value = None


    def clear(self) -> None:
        """方法 clear"""
        pass

    def iterator(self) -> iter:
        """方法 iterator"""
        raise NotImplementedError("方法 iterator 尚未实现")

    def size(self) -> int:
        """方法 size"""
        return 0

    def put(self, key: Any, value: Any) -> Any:
        """方法 put"""
        raise NotImplementedError("方法 put 尚未实现")

    def getKey(self) -> Any:
        """方法 getKey"""
        raise NotImplementedError("方法 getKey 尚未实现")

    def getValue(self) -> Any:
        """方法 getValue"""
        raise NotImplementedError("方法 getValue 尚未实现")

    def setValue(self, newValue: Any) -> Any:
        """方法 setValue"""
        raise NotImplementedError("方法 setValue 尚未实现")

    def equals(self, o: Any) -> bool:
        """方法 equals"""
        return False

    def hashCode(self) -> int:
        """方法 hashCode"""
        return 0

    def toString(self) -> str:
        """方法 toString"""
        return ""


class Entry(Map.Entry, V>):
    """
    类 Entry - 从Java类转换
    实现接口: Map.Entry<K, V>, Serializable
    """

    def __init__(self, key: Any, value: Any):
        """初始化 Entry"""
        self.list = []
        self.key = None
        self.value = None


    def clear(self) -> None:
        """方法 clear"""
        pass

    def iterator(self) -> iter:
        """方法 iterator"""
        raise NotImplementedError("方法 iterator 尚未实现")

    def size(self) -> int:
        """方法 size"""
        return 0

    def put(self, key: Any, value: Any) -> Any:
        """方法 put"""
        raise NotImplementedError("方法 put 尚未实现")

    def getKey(self) -> Any:
        """方法 getKey"""
        raise NotImplementedError("方法 getKey 尚未实现")

    def getValue(self) -> Any:
        """方法 getValue"""
        raise NotImplementedError("方法 getValue 尚未实现")

    def setValue(self, newValue: Any) -> Any:
        """方法 setValue"""
        raise NotImplementedError("方法 setValue 尚未实现")

    def equals(self, o: Any) -> bool:
        """方法 equals"""
        return False

    def hashCode(self) -> int:
        """方法 hashCode"""
        return 0

    def toString(self) -> str:
        """方法 toString"""
        return ""

