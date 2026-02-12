"""
PortalScript - 从Java源文件转换而来
对应Java源文件: scripting/PortalScript.java
包路径: scripting
"""


from abc import ABC, abstractmethod

class PortalScript(ABC):
    """接口 PortalScript - 从Java接口转换"""

    @abstractmethod
    def enter(self, p0: Any) -> Any:
        """抽象方法 enter"""
        pass

