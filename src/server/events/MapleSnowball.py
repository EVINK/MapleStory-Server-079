"""
MapleSnowball - Converted from Java source
Original: server/events/MapleSnowball.java
Package: server.events
"""

from concurrent.futures import Future
from typing import Optional, Any
import math
import sched
import threading

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MobSkillFactory import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleSnowball(MapleEvent):
    """
    Class MapleSnowball
    Extends: MapleEvent
    """

    def __init__(self, channel: int, mapid: list):
        self.position = 0
        self.team = None
        self.startPoint = 0
        self.invis = False
        self.hittable = False
        self.snowmanhp = 0
        super(channel, mapid)
        self.balls = new MapleSnowballs[2]


    def unreset(self) -> None:
        super.unreset()
        for i in range(2):
            self.getSnowBall(i).resetSchedule()
            self.resetSnowBall(i)

    def reset(self) -> None:
        super.reset()
        self.makeSnowBall(0)
        self.makeSnowBall(1)

    def startEvent(self) -> None:
        for i in range(2):
            ball = self.getSnowBall(i)
            ball.broadcast(self.getMap(0), 0)
            ball.setInvis(False)
            ball.broadcast(self.getMap(0), 5)
            self.getMap(0).broadcastMessage(MaplePacketCreator.enterSnowBall())

    def resetSnowBall(self, teamz: int) -> None:
        self.balls[teamz] = None

    def makeSnowBall(self, teamz: int) -> None:
        self.resetSnowBall(teamz)
        self.balls[teamz] = MapleSnowballs(teamz)

    def getSnowBall(self, teamz: int) -> Any:
        return self.balls[teamz]

    def hitSnowball(self, chr: Any) -> None:
        team = (chr.getPosition().y <= -80) ? 1 : 0
        sb = chr.getClient().getChannelServer().getEvent(MapleEventType.雪球赛)
        ball = sb.getSnowBall(team)
        if ball is not None && !ball.isInvis():
            snowman = chr.getPosition().x < -360 && chr.getPosition().x > -560
            if !snowman:
                damage = ((random.random() < 0.01 || (chr.getPosition().x > ball.getLeftX() && chr.getPosition().x < ball.getRightX())) && ball.isHittable()) ? 10 : 0
                chr.getMap().broadcastMessage(MaplePacketCreator.hitSnowBall(team, damage, 0, 1))
                if damage == 0:
                    if random.random() < 0.2:
                        chr.getClient().getSession().write(MaplePacketCreator.leftKnockBack())
                        chr.getClient().getSession().write(MaplePacketCreator.enableActions())
                else:
                    ball.setPositionX(ball.getPosition() + 1)
                    if ball.getPosition() == 255 || ball.getPosition() == 511 || ball.getPosition() == 767:
                        ball.setStartPoint(chr.getMap())
                        chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(4, sb.getSnowBall(0), sb.getSnowBall(1)))
                    elif ball.getPosition() == 899:
                        map = chr.getMap()
                        for i in range(2):
                            sb.getSnowBall(i).setInvis(True)
                            map.broadcastMessage(MaplePacketCreator.rollSnowball(i + 2, sb.getSnowBall(0), sb.getSnowBall(1)))
                        chr.getMap().broadcastMessage(MaplePacketCreator.serverNotice(6, "[恭喜] " + ((team == 0) ? "蓝队" : "红队") + " 赢得胜利!"))
                        for chrz in chr.getMap().getCharactersThreadsafe():
                            if (team == 0 && chrz.getPosition().y > -80) || (team == 1 && chrz.getPosition().y <= -80):
                                sb.givePrize(chrz)
                            sb.warpBack(chrz)
                        sb.unreset()
                    elif ball.getPosition() < 899:
                        chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(4, sb.getSnowBall(0), sb.getSnowBall(1)))
                        ball.setInvis(False)
            elif ball.getPosition() < 899:
                damage = 15
                if random.random() < 0.3:
                    damage = 0
                if random.random() < 0.05:
                    damage = 45
                chr.getMap().broadcastMessage(MaplePacketCreator.hitSnowBall(team + 2, damage, 0, 0))
                ball.setSnowmanHP(ball.getSnowmanHP() - damage)
                if damage > 0:
                    chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(0, sb.getSnowBall(0), sb.getSnowBall(1)))
                    if ball.getSnowmanHP() <= 0:
                        ball.setSnowmanHP(7500)
                        oBall = sb.getSnowBall((team == 0) ? 1 : 0)
                        oBall.setHittable(False)
                        map2 = chr.getMap()
                        oBall.broadcast(map2, 4)
                        oBall.snowmanSchedule = Timer.EventTimer.getInstance().schedule(Runnable()
                            public void run()
                                oBall.setHittable(True)
                                oBall.broadcast(map2, 5)
                        for chrz2 in chr.getMap().getCharactersThreadsafe():
                            if (ball.getTeam() == 0 && chr.getPosition().y < -80) || (ball.getTeam() == 1 && chr.getPosition().y > -80):
                                chrz2.giveDebuff(MapleDisease.诱惑, MobSkillFactory.getMobSkill(128, 1))

    def run(self) -> None:
        oBall.setHittable(True)
        oBall.broadcast(map2, 5)

    def resetSchedule(self) -> None:
        if self.snowmanSchedule is not None:
            self.snowmanSchedule.cancel(False)
            self.snowmanSchedule = None

    def getTeam(self) -> int:
        return self.team

    def getPosition(self) -> int:
        return self.position

    def setPositionX(self, pos: int) -> None:
        self.position = pos

    def setStartPoint(self, map: Any) -> None:
        self.broadcast(map, ++self.startPoint)

    def isInvis(self) -> bool:
        return self.invis

    def setInvis(self, i: bool) -> None:
        self.invis = i

    def isHittable(self) -> bool:
        return self.hittable && !self.invis

    def setHittable(self, b: bool) -> None:
        self.hittable = b

    def getSnowmanHP(self) -> int:
        return self.snowmanhp

    def setSnowmanHP(self, shp: int) -> None:
        self.snowmanhp = shp

    def broadcast(self, map: Any, message: int) -> None:
        for chr in map.getCharactersThreadsafe():
            if (self.team == 0 && chr.getPosition().y > -80) || (self.team == 1 && chr.getPosition().y <= -80):
                chr.getClient().getSession().write(MaplePacketCreator.snowballMessage(self.team, message))

    def getLeftX(self) -> int:
        return self.position * 3 + 175

    def getRightX(self) -> int:
        return self.getLeftX() + 275


# Inner class from Java (originally nested)
class MapleSnowballs:
    """
    Class MapleSnowballs
    """

    def __init__(self, team_: int):
        self.position = 0
        self.team = None
        self.startPoint = 0
        self.invis = False
        self.hittable = False
        self.snowmanhp = 0
        self.position = 0
        self.startPoint = 0
        self.invis = True
        self.hittable = True
        self.snowmanhp = 7500
        self.snowmanSchedule = None
        self.team = team_


    def hitSnowball(self, chr: Any) -> None:
        team = (chr.getPosition().y <= -80) ? 1 : 0
        sb = chr.getClient().getChannelServer().getEvent(MapleEventType.雪球赛)
        ball = sb.getSnowBall(team)
        if ball is not None && !ball.isInvis():
            snowman = chr.getPosition().x < -360 && chr.getPosition().x > -560
            if !snowman:
                damage = ((random.random() < 0.01 || (chr.getPosition().x > ball.getLeftX() && chr.getPosition().x < ball.getRightX())) && ball.isHittable()) ? 10 : 0
                chr.getMap().broadcastMessage(MaplePacketCreator.hitSnowBall(team, damage, 0, 1))
                if damage == 0:
                    if random.random() < 0.2:
                        chr.getClient().getSession().write(MaplePacketCreator.leftKnockBack())
                        chr.getClient().getSession().write(MaplePacketCreator.enableActions())
                else:
                    ball.setPositionX(ball.getPosition() + 1)
                    if ball.getPosition() == 255 || ball.getPosition() == 511 || ball.getPosition() == 767:
                        ball.setStartPoint(chr.getMap())
                        chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(4, sb.getSnowBall(0), sb.getSnowBall(1)))
                    elif ball.getPosition() == 899:
                        map = chr.getMap()
                        for i in range(2):
                            sb.getSnowBall(i).setInvis(True)
                            map.broadcastMessage(MaplePacketCreator.rollSnowball(i + 2, sb.getSnowBall(0), sb.getSnowBall(1)))
                        chr.getMap().broadcastMessage(MaplePacketCreator.serverNotice(6, "[恭喜] " + ((team == 0) ? "蓝队" : "红队") + " 赢得胜利!"))
                        for chrz in chr.getMap().getCharactersThreadsafe():
                            if (team == 0 && chrz.getPosition().y > -80) || (team == 1 && chrz.getPosition().y <= -80):
                                sb.givePrize(chrz)
                            sb.warpBack(chrz)
                        sb.unreset()
                    elif ball.getPosition() < 899:
                        chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(4, sb.getSnowBall(0), sb.getSnowBall(1)))
                        ball.setInvis(False)
            elif ball.getPosition() < 899:
                damage = 15
                if random.random() < 0.3:
                    damage = 0
                if random.random() < 0.05:
                    damage = 45
                chr.getMap().broadcastMessage(MaplePacketCreator.hitSnowBall(team + 2, damage, 0, 0))
                ball.setSnowmanHP(ball.getSnowmanHP() - damage)
                if damage > 0:
                    chr.getMap().broadcastMessage(MaplePacketCreator.rollSnowball(0, sb.getSnowBall(0), sb.getSnowBall(1)))
                    if ball.getSnowmanHP() <= 0:
                        ball.setSnowmanHP(7500)
                        oBall = sb.getSnowBall((team == 0) ? 1 : 0)
                        oBall.setHittable(False)
                        map2 = chr.getMap()
                        oBall.broadcast(map2, 4)
                        oBall.snowmanSchedule = Timer.EventTimer.getInstance().schedule(Runnable()
                            public void run()
                                oBall.setHittable(True)
                                oBall.broadcast(map2, 5)
                        for chrz2 in chr.getMap().getCharactersThreadsafe():
                            if (ball.getTeam() == 0 && chr.getPosition().y < -80) || (ball.getTeam() == 1 && chr.getPosition().y > -80):
                                chrz2.giveDebuff(MapleDisease.诱惑, MobSkillFactory.getMobSkill(128, 1))

    def run(self) -> None:
        oBall.setHittable(True)
        oBall.broadcast(map2, 5)

    def resetSchedule(self) -> None:
        if self.snowmanSchedule is not None:
            self.snowmanSchedule.cancel(False)
            self.snowmanSchedule = None

    def getTeam(self) -> int:
        return self.team

    def getPosition(self) -> int:
        return self.position

    def setPositionX(self, pos: int) -> None:
        self.position = pos

    def setStartPoint(self, map: Any) -> None:
        self.broadcast(map, ++self.startPoint)

    def isInvis(self) -> bool:
        return self.invis

    def setInvis(self, i: bool) -> None:
        self.invis = i

    def isHittable(self) -> bool:
        return self.hittable && !self.invis

    def setHittable(self, b: bool) -> None:
        self.hittable = b

    def getSnowmanHP(self) -> int:
        return self.snowmanhp

    def setSnowmanHP(self, shp: int) -> None:
        self.snowmanhp = shp

    def broadcast(self, map: Any, message: int) -> None:
        for chr in map.getCharactersThreadsafe():
            if (self.team == 0 && chr.getPosition().y > -80) || (self.team == 1 && chr.getPosition().y <= -80):
                chr.getClient().getSession().write(MaplePacketCreator.snowballMessage(self.team, message))

    def getLeftX(self) -> int:
        return self.position * 3 + 175

    def getRightX(self) -> int:
        return self.getLeftX() + 275

