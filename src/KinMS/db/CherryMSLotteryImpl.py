"""
CherryMSLotteryImpl - Converted from Java source
Original: KinMS/db/CherryMSLotteryImpl.java
Package: KinMS.db
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from typing import Collection
from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class CherryMSLotteryImpl(CherryMSLottery):
    """
    Class CherryMSLotteryImpl
    Implements: CherryMSLottery
    """

    def __init__(self):
        self.cserv = None
        self.mapFactory = None
        self.jjc = False
        self.zjNum = 0
        self.alltouzhu = 0
        self.allpeichu = 0
        self.characters = []

    # Static initializer
    # CherryMSLotteryImpl.instance = None


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getInstance_cserv_mapFactory(self, cserv: Any, mapFactory: Any) -> Any:
        if CherryMSLotteryImpl.instance is None:
            CherryMSLotteryImpl.instance = CherryMSLotteryImpl(cserv, mapFactory)
        return CherryMSLotteryImpl.instance

    def getChannelServer(self) -> Any:
        return self.cserv

    def getMapleMapFactory(self) -> Any:
        return self.mapFactory

    def getDatetimemm(self) -> int:
        date = Date()
        sdf = SimpleDateFormat("mm")
        datetime = sdf.format(date)
        return int(datetime)

    def warp(self, map: int, c: Any) -> None:
        target = self.getWarpMap(map, c)
        c.changeMap(target, target.getPortal(0))

    def getWarpMap(self, map: int, c: Any) -> Any:
        target = None
        if c.getEventInstance() is None:
            target = ChannelServer.getInstance(c.getClient().getChannel()).getMapFactory().getMap(map)
        else:
            target = c.getEventInstance().getMapInstance(map)
        return target

    def getAllpeichu(self) -> int:
        return self.allpeichu

    def setAllpeichu(self, allpeichu: int) -> None:
        self.allpeichu = allpeichu

    def getAlltouzhu(self) -> int:
        return self.alltouzhu

    def setAlltouzhu(self, alltouzhu: int) -> None:
        self.alltouzhu = alltouzhu

    def getCharacters(self) -> list:
        return self.characters

    def setCharacters(self, characters: list) -> None:
        self.characters = characters

    def addChar(self, chr: Any) -> None:
        self.characters.add(chr)

    def getZjNum(self) -> int:
        return self.zjNum

    def setZjNum(self, zjNum: int) -> None:
        self.zjNum = zjNum

    def doLottery(self) -> None:
        self.drawalottery()

    def getTouNumbyType(self, type: int) -> int:
        count = 0
        for chr in self.characters:
            if chr.getTouzhuType() == type:
                count += 1
        return count

    def drawalottery(self) -> None:
        self.zjNum = (int)(random.random() * 6.0 + 1.0)
        zjNames2 = ""
        zjNames3 = ""
        zjNames6 = ""
        toucount2 = 0
        toucount3 = 0
        toucount6 = 0
        zhongcount2 = 0
        zhongcount3 = 0
        zhongcount6 = 0
        sumNX = 0
        peiNX = 0
        zjpeople = 0
        drawchars = self.characters
        if drawchars is not None:
            for chr in drawchars:
                charType = chr.getTouzhuType()
                charNum = chr.getTouzhuNum()
                charZhuNX = chr.getTouzhuNX()
                chr.setTouzhuType(0)
                chr.setTouzhuNum(0)
                chr.setTouzhuNX(0)
                sumNX += charZhuNX
                if charType == 2:
                    toucount2 += 1
                    if self.zjNum == 1 || self.zjNum == 3 || (self.zjNum == 5 && charNum == 1) || self.zjNum == 2 || self.zjNum == 4 || (self.zjNum == 6 && charNum == 2):
                        charZhuNX *= int(ServerProperties.getProperty("RoyMS.赌博A赔率", "2"))
                        charZhuNX -= charZhuNX * int(ServerProperties.getProperty("RoyMS.赌博手续费", "5")) / 100
                        chr.modifyCSPoints(1, charZhuNX)
                        chr.dropMessage(1, "本期号码：【" + self.zjNum + "】 \r\n恭喜你获奖了。扣除手续费5%。获得奖金额:" + charZhuNX)
                        peiNX += charZhuNX
                        zjNames6 = zjNames6 + chr.getName() + ":赢得" + peiNX + "点卷 "
                        zhongcount2 += 1
                        zjpeople += 1
                        getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(6, "[赌博系统]" + int(ServerProperties.getProperty("RoyMS.赌博A赔率", "2")) + "倍中奖名单:" + zjNames6 + "！恭喜他吧"))
                    else:
                        chr.dropMessage(1, "本期号码：【" + self.zjNum + "】\r\n对不起您没有中奖，请继续努力")
                if charType == 3:
                    toucount3 += 1
                    if (self.zjNum > 4 && charNum > 4) || (self.zjNum < 3 && charNum < 3) || (self.zjNum >= 3 && self.zjNum <= 4 && charNum <= 4 && charNum >= 3):
                        charZhuNX *= int(ServerProperties.getProperty("RoyMS.赌博B赔率", "3"))
                        charZhuNX -= charZhuNX * int(ServerProperties.getProperty("RoyMS.赌博手续费", "5")) / 100
                        chr.modifyCSPoints(1, charZhuNX)
                        chr.dropMessage(1, "本期号码：【" + self.zjNum + "】 \r\n恭喜你获奖了。扣除手续费5%。获得奖金额:" + charZhuNX)
                        peiNX += charZhuNX
                        zjNames6 = zjNames6 + chr.getName() + ":赢得" + peiNX + "点卷 "
                        zhongcount3 += 1
                        zjpeople += 1
                        getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(6, "[赌博系统]" + int(ServerProperties.getProperty("RoyMS.赌博B赔率", "3")) + "倍中奖名单:" + zjNames6 + "！恭喜他吧"))
                    else:
                        chr.dropMessage(1, "本期号码：【" + self.zjNum + "】\r\n对不起您没有中奖，请继续努力")
                if charType == 6:
                    toucount6 += 1
                    if self.zjNum == charNum:
                        charZhuNX *= int(ServerProperties.getProperty("RoyMS.赌博C赔率", "6"))
                        charZhuNX -= charZhuNX * int(ServerProperties.getProperty("RoyMS.赌博手续费", "5")) / 100
                        chr.modifyCSPoints(1, charZhuNX)
                        chr.dropMessage(1, "本期号码：【" + self.zjNum + "】 \r\n恭喜你获奖了。扣除手续费5%。获得奖金额:" + charZhuNX)
                        peiNX += charZhuNX
                        zjNames6 = zjNames6 + chr.getName() + ":赢得" + peiNX + "点卷 "
                        zhongcount6 += 1
                        zjpeople += 1
                        getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(6, "[赌博系统]" + int(ServerProperties.getProperty("RoyMS.赌博C赔率", "6")) + "倍中奖名单:" + zjNames6 + "！恭喜他吧"))
                        continue
                    chr.dropMessage(1, "本期号码：【" + self.zjNum + "】\r\n对不起您没有中奖，请继续努力")
            self.alltouzhu += sumNX
            self.allpeichu += peiNX
            self.characters.removeAll(drawchars)
        peoplecount = 0
        if drawchars is not None:
        peoplecount = drawchars
        getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(6, ServerProperties.getProperty("RoyMS.赌博公告")))
        if "" == (zjNames6):

