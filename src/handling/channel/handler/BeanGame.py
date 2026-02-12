"""
BeanGame - Converted from Java source
Original: handling/channel/handler/BeanGame.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class BeanGame:
    """
    Class BeanGame
    """

    def __init__(self):
        self.number = None
        self.type = None
        self.pos = None


    def BeanGame1(self, slea: Any, c: Any) -> None:
        chr = c.getPlayer()
        beansInfo = []
        type = slea.readByte()
        力度 = 0
        豆豆序號 = 0
        if type == 1:
            力度 = slea.readShort()
            chr.setBeansRange(力度)
            c.getSession().write(MaplePacketCreator.enableActions())
        elif type == 0:
            力度 = slea.readShort()
            豆豆序號 = slea.readInt() + 1
            chr.setBeansRange(力度)
            chr.setBeansNum(豆豆序號)
            if 豆豆序號 == 1:
                chr.setCanSetBeansNum(False)
        elif type == 2:
            if type == 11 || type == 0:
                力度 = slea.readShort()
                豆豆序號 = slea.readInt() + 1
                chr.setBeansRange(力度)
                chr.setBeansNum(豆豆序號)
                if 豆豆序號 == 1:
                    chr.setCanSetBeansNum(False)
        elif type == 6:
            slea.skip(1)
            循環次數 = slea.readByte()
            if 循環次數 == 0:
                return
            if 循環次數 != 1:
                slea.skip((循環次數 - 1) * 8)
            if chr.isCanSetBeansNum():
                chr.setBeansNum(chr.getBeansNum() + 循環次數)
            chr.gainBeans(-循環次數)
            chr.setCanSetBeansNum(True)
        elif type == 11 || type == 6:
            力度 = slea.readShort()
            chr.setBeansRange(力度)
            size = (byte)(slea.readByte() + 1)
            Pos = slea.readShort()
            Type = (byte)(slea.readByte() + 1)
            c.getSession().write(MaplePacketCreator.showBeans(力度, size, Pos, Type))
        else:
            print("未處理的類型【" + type + "】\n包" + slea)

    def getBeanType(self) -> int:
        random = rand(1, 100)
        beanType = 0
        # switch (random):
            # case 2:
                beanType = 1
                break
            # case 49:
                beanType = 2
                break
            # case 99:
                beanType = 3
                break
        return beanType

    def rand(self, lbound: int, ubound: int) -> int:
        return (int)(random.random() * (ubound - lbound + 1) + lbound)

    def BeanGame2(self, slea: Any, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.updateBeans(c.getPlayer().getId(), c.getPlayer().getBeans()))
        c.getSession().write(MaplePacketCreator.enableActions())

    def getType(self) -> int:
        return self.type

    def getNumber(self) -> int:
        return self.number

    def getPos(self) -> int:
        return self.pos


# Inner class from Java (originally nested)
class Beans:
    """
    Class Beans
    """

    def __init__(self, pos: int, type: int, number: int):
        self.number = None
        self.type = None
        self.pos = None
        self.pos = pos
        self.number = number
        self.type = type


    def getType(self) -> int:
        return self.type

    def getNumber(self) -> int:
        return self.number

    def getPos(self) -> int:
        return self.pos

