"""
UserInterfaceHandler - Converted from Java source
Original: handling/channel/handler/UserInterfaceHandler.java
Package: handling.channel.handler
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from scripting.EventManager import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class UserInterfaceHandler:
    """
    Class UserInterfaceHandler
    """


    def CygnusSummon_NPCRequest(self, c: Any) -> None:
        if c.getPlayer().getJob() == 2000:
            NPCScriptManager.getInstance().start(c, 1202000)
        elif c.getPlayer().getJob() == 1000:
            NPCScriptManager.getInstance().start(c, 1101008)

    def ShipObjectRequest(self, mapid: int, c: Any) -> None:
        effect = 3
        # switch (mapid):
            # case 101000300:
            # case 200000111:
                em = c.getChannelServer().getEventSM().getEventManager("Boats")
                if em is not None && em.getProperty("docked") == ("True"):
                    effect = 1
                    break
                break
            # case 200000121:
            # case 220000110:
                em = c.getChannelServer().getEventSM().getEventManager("Trains")
                if em is not None && em.getProperty("docked") == ("True"):
                    effect = 1
                    break
                break
            # case 200000151:
            # case 260000100:
                em = c.getChannelServer().getEventSM().getEventManager("Geenie")
                if em is not None && em.getProperty("docked") == ("True"):
                    effect = 1
                    break
                break
            # case 200000131:
            # case 240000110:
                em = c.getChannelServer().getEventSM().getEventManager("Flight")
                if em is not None && em.getProperty("docked") == ("True"):
                    effect = 1
                    break
                break
            # case 200090000:
            # case 200090010:
                em = c.getChannelServer().getEventSM().getEventManager("Boats")
                if em is not None && em.getProperty("haveBalrog") == ("True"):
                    effect = 1
                    break
                return
            # default:
                print("Unhandled ship object, MapID : " + mapid)
                break
        c.getSession().write(MaplePacketCreator.boatPacket(effect))

