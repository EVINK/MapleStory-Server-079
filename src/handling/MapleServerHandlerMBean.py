"""
MapleServerHandlerMBean - 从Java源文件转换而来
对应Java源文件: handling/MapleServerHandlerMBean.java
包路径: handling
"""


from abc import ABC, abstractmethod

class MapleServerHandlerMBean(ABC):
    """接口 MapleServerHandlerMBean - 从Java接口转换"""

    @abstractmethod
    def write_log(self) -> Any:
        """抽象方法 writeLog"""
        pass

