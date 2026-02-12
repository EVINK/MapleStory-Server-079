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
        return getattr(self, 'config', None)

    def getFilterChain(self) -> Any:
        """方法 getFilterChain"""
        return getattr(self, 'filter_chain', None)

    def getHandler(self) -> Any:
        """方法 getHandler"""
        return getattr(self, 'handler', None)

    def getLocalAddress(self) -> Any:
        """方法 getLocalAddress"""
        return getattr(self, 'local_address', None)

    def getRemoteAddress(self) -> Any:
        """方法 getRemoteAddress"""
        return getattr(self, 'remote_address', None)

    def getService(self) -> Any:
        """方法 getService"""
        return getattr(self, 'service', None)

    def getServiceAddress(self) -> Any:
        """方法 getServiceAddress"""
        return getattr(self, 'service_address', None)

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

