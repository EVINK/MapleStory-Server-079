"""
ShutdownServerMBean - 从Java源文件转换而来
对应Java源文件: server/ShutdownServerMBean.java
包路径: server
"""

import threading


from abc import ABC, abstractmethod

class ShutdownServerMBean(ABC):
    """接口 ShutdownServerMBean - 从Java接口转换"""

    @abstractmethod
    def shutdown(self) -> Any:
        """抽象方法 shutdown"""
        pass

