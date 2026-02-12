"""
MapleData - 从Java源文件转换而来
对应Java源文件: provider/MapleData.java
包路径: provider
"""

from typing import List
from typing import Optional, List, Dict, Any, Set

# 内部模块导入 (Internal module imports)
# from provider.WzXML.MapleDataType import *  # TODO: 根据实际需要导入具体类


from abc import ABC, abstractmethod

class MapleData(ABC):
    """接口 MapleData - 从Java接口转换"""

    @abstractmethod
    def get_name(self) -> Any:
        """抽象方法 getName"""
        pass

    @abstractmethod
    def get_type(self) -> Any:
        """抽象方法 getType"""
        pass

    @abstractmethod
    def get_children(self) -> Any:
        """抽象方法 getChildren"""
        pass

    @abstractmethod
    def get_child_by_path(self, p0: str) -> Any:
        """抽象方法 getChildByPath"""
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """抽象方法 getData"""
        pass

