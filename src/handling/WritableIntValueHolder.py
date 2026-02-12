"""
WritableIntValueHolder - 从Java源文件转换而来
对应Java源文件: handling/WritableIntValueHolder.java
包路径: handling
"""


from abc import ABC, abstractmethod

class WritableIntValueHolder(ABC):
    """接口 WritableIntValueHolder - 从Java接口转换"""

    @abstractmethod
    def get_value(self) -> Any:
        """抽象方法 getValue"""
        pass

    @abstractmethod
    def set_value(self, p0: int) -> Any:
        """抽象方法 setValue"""
        pass

