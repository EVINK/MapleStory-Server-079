"""
ByteOutputStream - 从Java源文件转换而来
对应Java源文件: tools/data/output/ByteOutputStream.java
包路径: tools.data.output
"""


from abc import ABC, abstractmethod

class ByteOutputStream(ABC):
    """接口 ByteOutputStream - 从Java接口转换"""

    @abstractmethod
    def write_byte(self, p0: int) -> Any:
        """抽象方法 writeByte"""
        pass

