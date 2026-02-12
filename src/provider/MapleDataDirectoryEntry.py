"""
MapleDataDirectoryEntry - 从Java源文件转换而来
对应Java源文件: provider/MapleDataDirectoryEntry.java
包路径: provider
"""

from typing import List
from typing import Optional, List, Dict, Any, Set


from abc import ABC, abstractmethod

class MapleDataDirectoryEntry(ABC):
    """接口 MapleDataDirectoryEntry - 从Java接口转换"""

    @abstractmethod
    def get_subdirectories(self) -> Any:
        """抽象方法 getSubdirectories"""
        pass

    @abstractmethod
    def get_files(self) -> Any:
        """抽象方法 getFiles"""
        pass

    @abstractmethod
    def get_entry(self, p0: str) -> Any:
        """抽象方法 getEntry"""
        pass

