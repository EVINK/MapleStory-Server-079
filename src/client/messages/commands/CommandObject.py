"""
CommandObject - 从Java源文件转换而来
对应Java源文件: client/messages/commands/CommandObject.java
包路径: client.messages.commands
"""

# 内部模块导入 (Internal module imports)
# from client.MapleClient import *  # TODO: 根据实际需要导入具体类
# from constants.ServerConstants import *  # TODO: 根据实际需要导入具体类


class CommandObject:
    """
    类 CommandObject - 从Java类转换
    """

    def __init__(self, com: str, c: Any, gmLevel: int):
        """初始化 CommandObject"""
        self.command = None
        self.gmLevelReq = None
        self.exe = None


    def execute(self, c: Any, splitted: list) -> int:
        """方法 execute"""
        return 0

    def getReqGMLevel(self) -> int:
        """方法 getReqGMLevel"""
        return getattr(self, 'req_gm_level', 0)

