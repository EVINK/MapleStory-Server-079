"""
ExternalCodeTableGetter - Converted from Java source
Original: handling/ExternalCodeTableGetter.java
Package: handling
"""

from configparser import ConfigParser
from typing import Collection
from typing import List
from typing import Optional, Any
import json

# Internal module imports
# from tools.HexTool import *  # TODO: import specific classes


class ExternalCodeTableGetter:
    """
    Class ExternalCodeTableGetter
    """

    def __init__(self, properties: Any):
        self.props = properties


    def valueOf(self, name: str, values: list) -> str:
        for val in values:
            if val == (name):
                return val
        return None

    def valueOf_name_values(self, name: str, values: list) -> Any:
        for val in values:
            if val.name() == (name):
                return val
        return None

    def compare(self, o1: Any, o2: Any) -> int:
        return Short.valueOf(o1.getValue()).compareTo(Short.valueOf(o2.getValue()))

    def populateValues(self, properties: Any, values: list) -> Any:
        exc = ExternalCodeTableGetter(properties)
        for code in values:
            if isinstance(code, SendPacketOpcode):
                new_values = (SendPacketOpcode[]) values
                (code).setValue( exc.getValue(code.name(),new_values,(short)-2))
            if isinstance(code, RecvPacketOpcode):
                new_values = (RecvPacketOpcode[]) values
                (code).setValue(exc.getValue(code.name(), new_values, (short) (-2)))
            # ((WritableIntValueHolder) code).setValue(exc.getValue(code.name(), values, (short) (-2)));

