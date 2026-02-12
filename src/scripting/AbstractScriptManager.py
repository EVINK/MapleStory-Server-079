"""
AbstractScriptManager - 从Java源文件转换而来
对应Java源文件: scripting/AbstractScriptManager.java
包路径: scripting
"""

from io import IOBase
from io import TextIOWrapper
from pathlib import Path
import os
import tkinter

# 内部模块导入 (Internal module imports)
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类
# from tools.FileoutputUtil import *  # TODO: 根据实际需要导入具体类
# from tools.MaplePacketCreator import *  # TODO: 根据实际需要导入具体类


class AbstractScriptManager(ABC):
    """
    类 AbstractScriptManager - 从Java类转换
    """


    @staticmethod
    def getInvocable(path: str, c: Any) -> Any:
        """方法 getInvocable"""
        raise NotImplementedError("方法 getInvocable 尚未实现")

    def getInvocable(self, path: str, c: Any, npc: bool) -> Any:
        """方法 getInvocable"""
        raise NotImplementedError("方法 getInvocable 尚未实现")

