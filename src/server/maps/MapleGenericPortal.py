"""
MapleGenericPortal - Converted from Java source
Original: server/maps/MapleGenericPortal.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from scripting.PortalScriptManager import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleGenericPortal(MaplePortal):
    """
    Class MapleGenericPortal
    Implements: MaplePortal
    """

    def __init__(self, type: int):
        self.name = ""
        self.target = ""
        self.scriptName = ""
        self.position = None
        self.targetmap = 0
        self.type = None
        self.id = 0
        self.portalState = False
        self.portalState = True
        self.type = type


    def getId(self) -> int:
        return self.id

    def setId(self, id: int) -> None:
        self.id = id

    def getName(self) -> str:
        return self.name

    def getPosition(self) -> Any:
        return self.position

    def getTarget(self) -> str:
        return self.target

    def getTargetMapId(self) -> int:
        return self.targetmap

    def getType(self) -> int:
        return self.type

    def getScriptName(self) -> str:
        return self.scriptName

    def setName(self, name: str) -> None:
        self.name = name

    def setPosition(self, position: Any) -> None:
        self.position = position

    def setTarget(self, target: str) -> None:
        self.target = target

    def setTargetMapId(self, targetmapid: int) -> None:
        self.targetmap = targetmapid

    def setScriptName(self, scriptName: str) -> None:
        self.scriptName = scriptName

    def enterPortal(self, c: Any) -> None:
        if self.getPosition().distanceSq(c.getPlayer().getPosition()) > 22500.0:
            c.getPlayer().getCheatTracker().registerOffense(CheatingOffense.使用过远传送点)
        currentmap = c.getPlayer().getMap()
        if self.portalState || c.getPlayer().isGM():
            if self.getScriptName() is not None:
                c.getPlayer().checkFollow()
                try:
                    PortalScriptManager.getInstance().executePortalScript(this, c)
                except Exception as e:
                    e.printStackTrace()
            elif self.getTargetMapId() != 999999999:
                to = ChannelServer.getInstance(c.getChannel()).getMapFactory().getMap(self.getTargetMapId())
                if !c.getPlayer().isGM():
                    if to is None:
                        c.getPlayer().dropMessage(5, "本地图目前尚未开放.")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                    if to.getLevelLimit() > 0 && to.getLevelLimit() > c.getPlayer().getLevel():
                        c.getPlayer().dropMessage(5, "You are too low of a level to enter this place.")
                        c.getSession().write(MaplePacketCreator.enableActions())
                        return
                elif to is None:
                    c.getPlayer().dropMessage(5, "本地图目前尚未开放.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                c.getPlayer().changeMapPortal(to, (to.getPortal(self.getTarget()) is None) ? to.getPortal(0) : to.getPortal(self.getTarget()))
        if c is not None && c.getPlayer() is not None && c.getPlayer().getMap() == currentmap:
            c.getSession().write(MaplePacketCreator.enableActions())

    def getPortalState(self) -> bool:
        return self.portalState

    def setPortalState(self, ps: bool) -> None:
        self.portalState = ps

