"""
MapleDataTool - Converted from Java source
Original: provider/MapleDataTool.java
Package: provider
"""

from typing import Optional, Any

# Internal module imports
# from provider.WzXML.MapleDataType import *  # TODO: import specific classes


class MapleDataTool:
    """
    Class MapleDataTool
    """


    def getString(self, data: Any) -> str:
        return data.getData()

    def getString_data_def(self, data: Any, def: str) -> str:
        if data is None or data.getData() is None:
            return def
        return data.getData()

    def getString_path_data(self, path: str, data: Any) -> str:
        return getString(data.getChildByPath(path))

    def getString_path_data_def(self, path: str, data: Any, def: str) -> str:
        return getString(data.getChildByPath(path), def)

    def getDouble(self, data: Any) -> float:
        return data.getData()

    def getFloat(self, data: Any) -> float:
        return data.getData()

    def getFloat_data_def(self, data: Any, def: float) -> float:
        if data is None or data.getData() is None:
            return def
        return data.getData()

    def getInt(self, data: Any) -> int:
        return data.getData()

    def getInt_data_def(self, data: Any, def: int) -> int:
        if data is None or data.getData() is None:
            return def
        if data.getType() == MapleDataType.STRING:
            return int(getString(data))
        if data.getType() == MapleDataType.SHORT:
            return data.getData()
        return data.getData()

    def getInt_path_data(self, path: str, data: Any) -> int:
        return getInt(data.getChildByPath(path))

    def getIntConvert(self, data: Any) -> int:
        if data.getType() == MapleDataType.STRING:
            return int(getString(data))
        return getInt(data)

    def getIntConvert_path_data(self, path: str, data: Any) -> int:
        d = data.getChildByPath(path)
        if d.getType() == MapleDataType.STRING:
            return int(getString(d))
        return getInt(d)

    def getInt_path_data_def(self, path: str, data: Any, def: int) -> int:
        return getInt(data.getChildByPath(path), def)

    def getIntConvert_path_data_def(self, path: str, data: Any, def: int) -> int:
        if data is None:
            return def
        d = data.getChildByPath(path)
        if d is None:
            return def
        if d.getType() == MapleDataType.STRING:
            try:
                return int(getString(d))
            except ValueError as nfe:
                return def
        return getInt(d, def)

    def getImage(self, data: Any) -> Any:
        return (data.getData()).getImage()

    def getPoint(self, data: Any) -> Any:
        return data.getData()

    def getPoint_path_data(self, path: str, data: Any) -> Any:
        return getPoint(data.getChildByPath(path))

    def getPoint_path_data_def(self, path: str, data: Any, def: Any) -> Any:
        pointData = data.getChildByPath(path)
        if pointData is None:
            return def
        return getPoint(pointData)

    def getFullDataPath(self, data: Any) -> str:
        path = ""
        myData = data
        while myData is not None:
            path = myData.getName() + "/" + path
        return path[0:path.__len__(] - 1)

