"""
CommandProcessorUtil - Converted from Java source
Original: client/messages/CommandProcessorUtil.java
Package: client.messages
"""

from typing import Optional, Any

# Internal module imports
# from tools import *  # TODO: import specific classes


class CommandProcessorUtil:
    """
    Class CommandProcessorUtil
    """


    def joinAfterString(self, splitted: list, str: str) -> str:
        for i in range(1, len(splitted)):
            if splitted[i].lower() == str.lower() and i + 1 < len(splitted):
                return StringUtil.joinStringFrom(splitted, i + 1)
        return None

    def getOptionalIntArg(self, splitted: list, position: int, def: int) -> int:
        if len(splitted) > position:
            try:
                return int(splitted[position])
            except ValueError as nfe:
                return def
        return def

    def getNamedArg(self, splitted: list, startpos: int, name: str) -> str:
        i = startpos
        while i < len(splitted):
            if splitted[i].lower() == name.lower() and i + 1 < len(splitted):
                return splitted[i + 1]
        return None

    def getNamedLongArg(self, splitted: list, startpos: int, name: str) -> int:
        arg = getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return int(arg)
            except NumberFormatException as ex:
                pass
        return None

    def getNamedIntArg(self, splitted: list, startpos: int, name: str) -> int:
        arg = getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return int(arg)
            except NumberFormatException as ex:
                pass
        return None

    def getNamedIntArg_splitted_startpos_name_def(self, splitted: list, startpos: int, name: str, def: int) -> int:
        ret = getNamedIntArg(splitted, startpos, name)
        if ret is None:
            return def
        return ret

    def getNamedDoubleArg(self, splitted: list, startpos: int, name: str) -> float:
        arg = getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return float(arg)
            except NumberFormatException as ex:
                pass
        return None

