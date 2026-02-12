"""
PortalFactory - Converted from Java source
Original: server/PortalFactory.java
Package: server
"""

from typing import Optional, Any

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.maps.MapleGenericPortal import *  # TODO: import specific classes
# from server.maps.MapleMapPortal import *  # TODO: import specific classes


class PortalFactory:
    """
    Class PortalFactory
    """

    def __init__(self):
        self.nextDoorPortal = 0
        self.nextDoorPortal = 128


    def makePortal(self, type: int, portal: Any) -> Any:
        ret = None
        if type == 2:
            ret = MapleMapPortal()
        else:
            ret = MapleGenericPortal(type)
        self.loadPortal(ret, portal)
        return ret

    def loadPortal(self, myPortal: Any, portal: Any) -> None:
        myPortal.setName(MapleDataTool.getString(portal.getChildByPath("pn")))
        myPortal.setTarget(MapleDataTool.getString(portal.getChildByPath("tn")))
        myPortal.setTargetMapId(MapleDataTool.getInt(portal.getChildByPath("tm")))
        myPortal.setPosition(Point(MapleDataTool.getInt(portal.getChildByPath("x")), MapleDataTool.getInt(portal.getChildByPath("y"))))
        script = MapleDataTool.getString("script", portal, None)
        if script is not None and script == (""):
            script = None
        myPortal.setScriptName(script)
        if myPortal.getType() == 6:
            myPortal.setId(self.nextDoorPortal)
            self.nextDoorPortal += 1
        else:
            myPortal.setId(int(portal.getName()))

