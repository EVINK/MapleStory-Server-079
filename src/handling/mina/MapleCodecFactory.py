"""
MapleCodecFactory - 从Java源文件转换而来
对应Java源文件: handling/mina/MapleCodecFactory.java
包路径: handling.mina
"""

import asyncio


class MapleCodecFactory(ProtocolCodecFactory):
    """
    类 MapleCodecFactory - 从Java类转换
    实现接口: ProtocolCodecFactory
    """

    def __init__(self):
        """初始化 MapleCodecFactory"""
        self.encoder = None
        self.decoder = None


    def getEncoder(self) -> Any:
        """方法 getEncoder"""
        raise NotImplementedError("方法 getEncoder 尚未实现")

    def getDecoder(self) -> Any:
        """方法 getDecoder"""
        raise NotImplementedError("方法 getDecoder 尚未实现")

    def getEncoder(self, session: Any) -> Any:
        """方法 getEncoder"""
        raise NotImplementedError("方法 getEncoder 尚未实现")

    def getDecoder(self, session: Any) -> Any:
        """方法 getDecoder"""
        raise NotImplementedError("方法 getDecoder 尚未实现")

