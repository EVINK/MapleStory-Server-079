"""
MapleReactorFactory - Converted from Java source
Original: server/maps/MapleReactorFactory.java
Package: server.maps
"""

from pathlib import Path
from typing import Dict
from typing import Optional, Any
import os
import sys

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class MapleReactorFactory:
    """
    Class MapleReactorFactory
    """

    # Static initializer
    # data = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Reactor.wz"))
    # reactorStats = {}


    @staticmethod
    def getReactor(rid: int) -> Any:
        stats = MapleReactorFactory.reactorStats.get(rid)
        if stats is None:
            infoId = rid
            reactorData = MapleReactorFactory.data.getData(StringUtil.getLeftPaddedStr(Integer.toString(infoId) + ".img", '0', 11))
            link = reactorData.getChildByPath("info/link")
            if link is not None:
                infoId = MapleDataTool.getIntConvert("info/link", reactorData)
                stats = MapleReactorFactory.reactorStats.get(infoId)
            if stats is None:
                stats = MapleReactorStats()
                reactorData = MapleReactorFactory.data.getData(StringUtil.getLeftPaddedStr(Integer.toString(infoId) + ".img", '0', 11))
                if reactorData is None:
                    return stats
                canTouch = MapleDataTool.getInt("info/activateByTouch", reactorData, 0) > 0
                areaSet = False
                foundState = False
                i = 0
                while True:
                    reactorD = reactorData.getChildByPath(str(i))
                    if reactorD is None:
                        break
                    reactorInfoData_ = reactorD.getChildByPath("event")
                    if reactorInfoData_ is not None && reactorInfoData_.getChildByPath("0") is not None:
                        reactorInfoData = reactorInfoData_.getChildByPath("0")
                        reactItem = None
                        type = MapleDataTool.getIntConvert("type", reactorInfoData)
                        if type == 100:
                            reactItem = new Pair<Integer, Integer>(MapleDataTool.getIntConvert("0", reactorInfoData), MapleDataTool.getIntConvert("1", reactorInfoData, 1))
                            if !areaSet:
                                stats.setTL(MapleDataTool.getPoint("lt", reactorInfoData))
                                stats.setBR(MapleDataTool.getPoint("rb", reactorInfoData))
                                areaSet = True
                        foundState = True
                        stats.addState(i, type, reactItem, MapleDataTool.getIntConvert("state", reactorInfoData), MapleDataTool.getIntConvert("timeOut", reactorInfoData_, -1), (byte)((MapleDataTool.getIntConvert("2", reactorInfoData, 0) > 0 || reactorInfoData.getChildByPath("clickArea") is not None || type == 9) ? 1 : (canTouch ? 2 : 0)))
                    else:
                        stats.addState(i, 999, None, (byte)(foundState ? -1 : (i + 1)), 0, 0)
                    i += 1
                MapleReactorFactory.reactorStats.put(infoId, stats)
                if rid != infoId:
                    MapleReactorFactory.reactorStats.put(rid, stats)
            else:
                MapleReactorFactory.reactorStats.put(rid, stats)
        return stats

