"""
MockIOSession - 从Java源文件转换而来
对应Java源文件: tools/MockIOSession.java
包路径: tools
"""

from socket import socket
import asyncio


class MockIOSession(DummySession):
    """
    类 MockIOSession - 从Java类转换
    继承自: DummySession
    """


    def updateTrafficMask(self) -> None:
        """方法 updateTrafficMask"""
        pass

    def getConfig(self) -> Any:
        """方法 getConfig"""
        raise NotImplementedError("方法 getConfig 尚未实现")

    def getFilterChain(self) -> Any:
        """方法 getFilterChain"""
        raise NotImplementedError("方法 getFilterChain 尚未实现")

    def getHandler(self) -> Any:
        """方法 getHandler"""
        raise NotImplementedError("方法 getHandler 尚未实现")

    def getLocalAddress(self) -> Any:
        """方法 getLocalAddress"""
        raise NotImplementedError("方法 getLocalAddress 尚未实现")

    def getRemoteAddress(self) -> Any:
        """方法 getRemoteAddress"""
        raise NotImplementedError("方法 getRemoteAddress 尚未实现")

    def getService(self) -> Any:
        """方法 getService"""
        raise NotImplementedError("方法 getService 尚未实现")

    def getServiceAddress(self) -> Any:
        """方法 getServiceAddress"""
        raise NotImplementedError("方法 getServiceAddress 尚未实现")

    def close0(self) -> None:
        """方法 close0"""
        pass

    def write(self, message: Any, remoteAddress: Any) -> Any:
        """方法 write"""
        raise NotImplementedError("方法 write 尚未实现")

    def write(self, message: Any) -> Any:
        """方法 write"""
        raise NotImplementedError("方法 write 尚未实现")

    def write0(self, writeRequest: Any) -> None:
        """方法 write0"""
        pass

