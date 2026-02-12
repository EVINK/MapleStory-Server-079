"""
MockIOSession - Converted from Java source
Original: tools/MockIOSession.java
Package: tools
"""

from socket import socket
from typing import Optional, Any
import asyncio


class MockIOSession(DummySession):
    """
    Class MockIOSession
    Extends: DummySession
    """


    def updateTrafficMask(self) -> None:
        pass

    def getConfig(self) -> Any:
        return None

    def getFilterChain(self) -> Any:
        return None

    def getHandler(self) -> Any:
        return None

    def getLocalAddress(self) -> Any:
        return None

    def getRemoteAddress(self) -> Any:
        return None

    def getService(self) -> Any:
        return None

    def getServiceAddress(self) -> Any:
        return None

    def close0(self) -> None:
        pass

    def write(self, message: Any, remoteAddress: Any) -> Any:
        return None

    def write_message(self, message: Any) -> Any:
        return None

    def write0(self, writeRequest: Any) -> None:
        pass

