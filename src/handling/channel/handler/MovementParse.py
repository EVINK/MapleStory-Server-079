"""
MovementParse - Converted from Java source
Original: handling/channel/handler/MovementParse.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from server.maps.AnimatedMapleMapObject import *  # TODO: import specific classes
# from server.movement.AbsoluteLifeMovement import *  # TODO: import specific classes
# from server.movement.AranMovement import *  # TODO: import specific classes
# from server.movement.BounceMovement import *  # TODO: import specific classes
# from server.movement.ChairMovement import *  # TODO: import specific classes
# from server.movement.ChangeEquipSpecialAwesome import *  # TODO: import specific classes
# from server.movement.JumpDownMovement import *  # TODO: import specific classes
# from server.movement.LifeMovement import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from server.movement.RelativeLifeMovement import *  # TODO: import specific classes
# from server.movement.TeleportMovement import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class MovementParse:
    """
    Class MovementParse
    """


    def parseMovement(self, lea: Any, kind: int) -> list:
        res = []
        numCommands = lea.readByte()
        类型 = ""
        # switch (kind):
            # case 1:
                类型 = "角色移动"
                break
            # case 2:
                类型 = "怪物移动"
                break
            # case 3:
                类型 = "宠物移动"
                break
            # case 4:
                类型 = "召唤兽移动"
                break
            # case 5:
                类型 = "龙移动"
                break
        i = 0
        while i < numCommands:
            command = lea.readByte()
            # switch (command):
                # case -1:
                    xpos = lea.readShort()
                    ypos = lea.readShort()
                    unk = lea.readShort()
                    fh = lea.readShort()
                    newstate = lea.readByte()
                    duration = lea.readShort()
                    bm = BounceMovement(command, Point(xpos, ypos), duration, newstate)
                    bm.setFH(fh)
                    bm.setUnk(unk)
                    res.add(bm)
                    break
                # case 0:
                # case 5:
                # case 17:
                    xpos = lea.readShort()
                    ypos = lea.readShort()
                    xwobble = lea.readShort()
                    ywobble = lea.readShort()
                    unk2 = lea.readShort()
                    newstate2 = lea.readByte()
                    duration2 = lea.readShort()
                    alm = AbsoluteLifeMovement(command, Point(xpos, ypos), duration2, newstate2)
                    alm.setUnk(unk2)
                    alm.setPixelsPerSecond(Point(xwobble, ywobble))
                    res.add(alm)
                    break
                # case 1:
                # case 2:
                # case 6:
                # case 12:
                # case 13:
                # case 16:
                # case 18:
                # case 19:
                # case 22:
                # case 23:
                # case 24:
                    xmod = lea.readShort()
                    ymod = lea.readShort()
                    newstate3 = lea.readByte()
                    duration3 = lea.readShort()
                    rlm = RelativeLifeMovement(command, Point(xmod, ymod), duration3, newstate3)
                    res.add(rlm)
                    break
                # case 3:
                # case 4:
                # case 7:
                # case 8:
                # case 9:
                # case 14:
                    xpos = lea.readShort()
                    ypos = lea.readShort()
                    xwobble = lea.readShort()
                    ywobble = lea.readShort()
                    newstate = lea.readByte()
                    tm = TeleportMovement(command, Point(xpos, ypos), newstate)
                    tm.setPixelsPerSecond(Point(xwobble, ywobble))
                    res.add(tm)
                    break
                # case 10:
                    res.add(ChangeEquipSpecialAwesome(lea.readByte()))
                    break
                # case 11:
                    xpos = lea.readShort()
                    ypos = lea.readShort()
                    unk = lea.readShort()
                    newstate4 = lea.readByte()
                    duration4 = lea.readShort()
                    cm = ChairMovement(command, Point(xpos, ypos), duration4, newstate4)
                    cm.setUnk(unk)
                    res.add(cm)
                    break
                # case 15:
                    xpos = lea.readShort()
                    ypos = lea.readShort()
                    xwobble = lea.readShort()
                    ywobble = lea.readShort()
                    unk2 = lea.readShort()
                    fh2 = lea.readShort()
                    newstate5 = lea.readByte()
                    duration5 = lea.readShort()
                    jdm = JumpDownMovement(command, Point(xpos, ypos), duration5, newstate5)
                    jdm.setUnk(unk2)
                    jdm.setPixelsPerSecond(Point(xwobble, ywobble))
                    jdm.setFH(fh2)
                    res.add(jdm)
                    break
                # case 20:
                # case 21:
                    unk3 = lea.readShort()
                    newstate6 = lea.readByte()
                    acm = AranMovement(command, Point(0, 0), unk3, newstate6)
                    res.add(acm)
                    break
                # default:
                    print("Kind movement: " + 类型 + ", Remaining : " + (numCommands - res) + " New type of movement ID : " + command + ", packet : " + lea.toString(True))
                    return None
        if numCommands != res:
            print("error in movement")
            return None
        return res

    def updatePosition(self, movement: list, target: Any, yoffset: int) -> None:
        for move in movement:
            if isinstance(move, LifeMovement):
                if isinstance(move, AbsoluteLifeMovement):
                    position2 = None
                    position = position2 = (move).getPosition()
                    position2.y += yoffset
                    target.setPosition(position)
                target.setStance((move).getNewstate())

