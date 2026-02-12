"""
PlayerNPC - Converted from Java source
Original: server/life/PlayerNPC.java
Package: server.life
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class PlayerNPC(MapleNPC):
    """
    Class PlayerNPC
    Extends: MapleNPC
    """

    def __init__(self, rs: Any):
        self.equips = {}
        self.mapid = 0
        self.face = 0
        self.hair = 0
        self.charId = 0
        self.skin = 0
        self.gender = 0
        super(rs.getInt("ScriptId"), rs.getString("name"))
        self.equips = {}
        self.pets = new int[3]
        self.hair = rs.getInt("hair")
        self.face = rs.getInt("face")
        self.mapid = rs.getInt("map")
        self.skin = rs.getByte("skin")
        self.charId = rs.getInt("charid")
        self.gender = rs.getByte("gender")
        self.setCoords(rs.getInt("x"), rs.getInt("y"), rs.getInt("dir"), rs.getInt("Foothold"))
        pet = rs.getString("pets").split(",")
        for i in range(3):
            if pet[i] is not None:
                self.pets[i] = int(pet[i])
            else:
                self.pets[i] = 0
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT * FROM playernpcs_equip WHERE NpcId = ?")
        ps.setInt(1, self.getId())
        rs2 = ps.executeQuery()
        while rs2.next():
            self.equips.put(rs2.getByte("equippos"), rs2.getInt("equipid"))
        rs2.close()
        ps.close()


    def loadAll(self) -> None:
        toAdd = []
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM playernpcs")
            rs = ps.executeQuery()
            while rs.next():
                toAdd.add(PlayerNPC(rs))
            rs.close()
            ps.close()
        except Exception as se:
            se.printStackTrace()
        for npc in toAdd:
            npc.addToServer()

    def updateByCharId(self, chr: Any) -> None:
        if World.Find.findChannel(chr.getId()) > 0:
            for npc in ChannelServer.getInstance(World.Find.findChannel(chr.getId())).getAllPlayerNPC():
                npc.update(chr)

    def setCoords(self, x: int, y: int, f: int, fh: int) -> None:
        self.setPosition(Point(x, y))
        self.setCy(y)
        self.setRx0(x - 50)
        self.setRx1(x + 50)
        self.setF(f)
        self.setFh(fh)

    def addToServer(self) -> None:
        for cserv in ChannelServer.getAllInstances():
            cserv.addPlayerNPC(this)

    def removeFromServer(self) -> None:
        for cserv in ChannelServer.getAllInstances():
            cserv.removePlayerNPC(this)

    def update(self, chr: Any) -> None:
        if chr is None || self.charId != chr.getId():
            return
        self.setName(chr.getName())
        self.setHair(chr.getHair())
        self.setFace(chr.getFace())
        self.setSkin(chr.getSkinColor())
        self.setGender(chr.getGender())
        self.setPets(chr.getPets())
        self.equips = {}
        for item in chr.getInventory(MapleInventoryType.EQUIPPED).list():
            if item.getPosition() < -128:
                continue
            self.equips.put(item.getPosition(), item.getItemId())
        self.saveToDB()

    def destroy(self) -> None:
        self.destroy(False)

    def destroy_remove(self, remove: bool) -> None:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("DELETE FROM playernpcs WHERE scriptid = ?")
            ps.setInt(1, self.getId())
            ps.executeUpdate()
            ps.close()
            ps = con.prepareStatement("DELETE FROM playernpcs_equip WHERE npcid = ?")
            ps.setInt(1, self.getId())
            ps.executeUpdate()
            ps.close()
            if remove:
                self.removeFromServer()
        except Exception as se:
            se.printStackTrace()

    def saveToDB(self) -> None:
        con = DatabaseConnection.getConnection()
        try:
            if self.getNPCFromWZ() is None:
                self.destroy(True)
                return
            self.destroy()
            ps = con.prepareStatement("INSERT INTO playernpcs(name, hair, face, skin, x, y, map, charid, scriptid, foothold, dir, gender, pets) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            ps.setString(1, self.getName())
            ps.setInt(2, self.getHair())
            ps.setInt(3, self.getFace())
            ps.setInt(4, self.getSkin())
            ps.setInt(5, self.getPosition().x)
            ps.setInt(6, self.getPosition().y)
            ps.setInt(7, self.getMapId())
            ps.setInt(8, self.getCharId())
            ps.setInt(9, self.getId())
            ps.setInt(10, self.getFh())
            ps.setInt(11, self.getF())
            ps.setInt(12, self.getGender())
            pet = { "0", "0", "0" }
            for i in range(3):
                if self.pets[i] > 0:
                    pet[i] = str(self.pets[i])
            ps.setString(13, pet[0] + "," + pet[1] + "," + pet[2])
            ps.executeUpdate()
            ps.close()
            ps = con.prepareStatement("INSERT INTO playernpcs_equip(npcid, charid, equipid, equippos) VALUES (?, ?, ?, ?)")
            ps.setInt(1, self.getId())
            ps.setInt(2, self.getCharId())
            for (final Map.Entry<Byte, Integer> equip : self.equips.items())
                ps.setInt(3, equip.getValue())
                ps.setInt(4, equip.getKey())
                ps.executeUpdate()
            ps.close()
        except Exception as se:
            se.printStackTrace()

    def getEquips(self) -> dict:
        return self.equips

    def getSkin(self) -> int:
        return self.skin

    def getGender(self) -> int:
        return self.gender

    def getFace(self) -> int:
        return self.face

    def getHair(self) -> int:
        return self.hair

    def getCharId(self) -> int:
        return self.charId

    def getMapId(self) -> int:
        return self.mapid

    def setSkin(self, s: int) -> None:
        self.skin = s

    def setFace(self, f: int) -> None:
        self.face = f

    def setHair(self, h: int) -> None:
        self.hair = h

    def setGender(self, g: int) -> None:
        self.gender = g

    def getPet(self, i: int) -> int:
        return (self.pets[i] > 0) ? self.pets[i] : 0

    def setPets(self, p: list) -> None:
        for i in range(3):
            if p is not None && p > i && p.get(i) is not None:
                self.pets[i] = p.get(i).getPetItemId()
            else:
                self.pets[i] = 0

    def sendSpawnData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.spawnNPC(this, True))
        client.getSession().write(MaplePacketCreator.spawnPlayerNPC(this))
        client.getSession().write(MaplePacketCreator.spawnNPCRequestController(this, True))

    def getNPCFromWZ(self) -> Any:
        npc = MapleLifeFactory.getNPC(self.getId())
        if npc is not None:
            npc.setName(self.getName())
        return npc

