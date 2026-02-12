"""
MapleClient - Converted from Java source
Original: client/MapleClient.java
Package: client
"""

from concurrent.futures import Future
from datetime import datetime
from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from threading import RLock
from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set
import asyncio
import pymysql
import sched
import threading
import time
import tkinter

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from database.DatabaseException import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleMessengerCharacter import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.PartyOperation import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.family.MapleFamilyCharacter import *  # TODO: import specific classes
# from handling.world.guild.MapleGuildCharacter import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from server.shops.IMaplePlayerShop import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MapleAESOFB import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.LoginPacket import *  # TODO: import specific classes


class MapleClient:
    """
    Class MapleClient
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, send: Any, receive: Any, session: Any):
        self.send = None
        self.receive = None
        self.session = None
        self.player = None
        self.channel = 0
        self.accId = 0
        self.world = 0
        self.birthday = 0
        self.charslots = 0
        self.loggedIn = False
        self.serverTransition = False
        self.tempban = None
        self.accountName = ""
        self.lastPong = None
        self.lastPing = None
        self.monitored = False
        self.receiving = False
        self.lastNpcClick = 0
        self.handsome2 = 0
        self.gm = False
        self.greason = 0
        self.gender = 0
        self.loginAttempt = None
        self.allowedChar = None
        self.macs = None
        self.engines = None
        self.secondPassword = None
        self.salt2 = None
        self.mutex = None
        self.npc_mutex = None
        self.tempIP = None
        self.mac = None
        self.name = ""
        self.id = 0
        self.channel = 1
        self.accId = 1
        self.charslots = 3
        self.loggedIn = False
        self.serverTransition = False
        self.tempban = None
        self.lastPong = 0
        self.lastPing = 0
        self.monitored = False
        self.receiving = True
        self.lastNpcClick = 0
        self.handsome2 = 1
        self.greason = 1
        self.gender = -1
        self.loginAttempt = 0
        self.allowedChar = []
        self.macs = set()
        self.engines = {}
        self.idleTask = None
        self.mutex = ReentrantLock(True)
        self.npc_mutex = ReentrantLock()
        self.tempIP = ""
        self.mac = "00-00-00-00-00-00"
        self.send = send
        self.receive = receive
        self.session = session

    # Static initializer
    # MapleClient.LOGIN_NOTLOGGEDIN = 0
    # MapleClient.LOGIN_SERVER_TRANSITION = 1
    # MapleClient.LOGIN_LOGGEDIN = 2
    # MapleClient.LOGIN_WAITING = 3
    # MapleClient.CASH_SHOP_TRANSITION = 4
    # MapleClient.LOGIN_CS_LOGGEDIN = 5
    # MapleClient.CHANGE_CHANNEL = 6
    # MapleClient.CLIENT_KEY = "CLIENT"
    # login_mutex = ReentrantLock(True)


    def banMacs(self, macs: str) -> None:
        con = DatabaseConnection.getConnection()
        try:
            filtered = []
            ps = con.prepareStatement("SELECT filter FROM macfilters")
            rs = ps.executeQuery()
            while rs.next():
                filtered.add(rs.getString("filter"))
            rs.close()
            ps.close()
            ps = con.prepareStatement("INSERT INTO macbans VALUES (?)")
            matched = False
            for filter in filtered:
                if macs.matches(filter):
                    matched = True
                    break
            if not matched:
                ps.setString(1, macs)
                try:
                    ps.executeUpdate()
                except SQLException as ex:
                    pass
            ps.close()
        except Exception as e:
            print("Error banning MACs" + e)

    def banMacs_macs(self, macs: list) -> None:
        con = DatabaseConnection.getConnection()
        try:
            filtered = []
            ps = con.prepareStatement("SELECT filter FROM macfilters")
            rs = ps.executeQuery()
            while rs.next():
                filtered.add(rs.getString("filter"))
            rs.close()
            ps.close()
            ps = con.prepareStatement("INSERT INTO macbans VALUES (?)")
            for mac in macs:
                matched = False
                for filter in filtered:
                    if mac.matches(filter):
                        matched = True
                        break
                if not matched:
                    ps.setString(1, mac)
                    try:
                        ps.executeUpdate()
                    except SQLException as ex:
                        pass
            ps.close()
        except Exception as e:
            print("Error banning MACs" + e)

    def unban(self, charname: str) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT accountid from characters where name = ?")
            ps.setString(1, charname)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            accid = rs.getInt(1)
            rs.close()
            ps.close()
            ps = con.prepareStatement("UPDATE accounts SET banned = 0 and banreason = '' WHERE id = ?")
            ps.setInt(1, accid)
            ps.executeUpdate()
            ps.close()
        except Exception as e:
            print("Error while unbanning" + e)
            return -2
        return 0

    def getLogMessage(self, cfor: Any, message: str) -> str:
        return getLogMessage(cfor, message, new Object[0])

    def getLogMessage_cfor_message(self, cfor: Any, message: str) -> str:
        return getLogMessage((cfor is None) ? None : cfor.getClient(), message)

    def getLogMessage_cfor_message_parms(self, cfor: Any, message: str, parms: Any) -> str:
        return getLogMessage((cfor is None) ? None : cfor.getClient(), message, parms)

    def findAccIdForCharacterName(self, charName: str) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT accountid FROM characters WHERE name = ?")
            ps.setString(1, charName)
            rs = ps.executeQuery()
            ret = -1
            if rs.next():
                ret = rs.getInt("accountid")
            rs.close()
            ps.close()
            return ret
        except Exception as e:
            print("findAccIdForCharacterName SQL error")
            return -1

    def unbanIPMacs(self, charname: str) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT accountid from characters where name = ?")
            ps.setString(1, charname)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            accid = rs.getInt(1)
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
            ps.setInt(1, accid)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            sessionIP = rs.getString("sessionIP")
            macs = rs.getString("macs")
            rs.close()
            ps.close()
            ret = 0
            if sessionIP is not None:
                psa = con.prepareStatement("DELETE FROM ipbans WHERE ip = ?")
                psa.setString(1, sessionIP)
                psa.execute()
                psa.close()
                ret += 1
            if macs is not None:
                split = None
                macz = split = macs.split(", ")
                for mac in split:
                    if not mac == (""):
                        psa2 = con.prepareStatement("DELETE FROM macbans WHERE mac = ?")
                        psa2.setString(1, mac)
                        psa2.execute()
                        psa2.close()
                ret += 1
            return ret
        except Exception as e:
            print("Error while unbanning" + e)
            return -2

    def unHellban(self, charname: str) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT accountid from characters where name = ?")
            ps.setString(1, charname)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            accid = rs.getInt(1)
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM accounts WHERE id = ?")
            ps.setInt(1, accid)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            sessionIP = rs.getString("sessionIP")
            email = rs.getString("email")
            rs.close()
            ps.close()
            ps = con.prepareStatement("UPDATE accounts SET banned = 0, banreason = '' WHERE email = ?" + ((sessionIP is None) ? "" : " OR sessionIP = ?"))
            ps.setString(1, email)
            if sessionIP is not None:
                ps.setString(2, sessionIP)
            ps.execute()
            ps.close()
            return 0
        except Exception as e:
            print("Error while unbanning" + e)
            return -2

    def getReceiveCrypto(self) -> Any:
        return self.receive

    def getSendCrypto(self) -> Any:
        return self.send

    def getSession(self) -> Any:
        return self.session

    def getTempIP(self) -> str:
        return self.tempIP

    def setTempIP(self, s: str) -> None:
        self.tempIP = s

    def getLock(self) -> Any:
        return self.mutex

    def getNPCLock(self) -> Any:
        return self.npc_mutex

    def sendPacket(self, o: Any) -> None:
        self.session.write(o)

    def getPlayer(self) -> Any:
        return self.player

    def setPlayer(self, player: Any) -> None:
        self.player = player

    def createdChar(self, id: int) -> None:
        self.allowedChar.add(id)

    def login_Auth(self, id: int) -> bool:
        return (id in self.allowedChar)

    def loadCharacters(self, serverId: int) -> list:
        chars = []
        for cni in self.loadCharactersInternal(serverId):
            chr = MapleCharacter.loadCharFromDB(cni.id, this, False)
            chars.add(chr)
            self.allowedChar.add(chr.getId())
        return chars

    def loadCharacterNames(self, serverId: int) -> list:
        chars = []
        for cni in self.loadCharactersInternal(serverId):
            chars.add(cni.name)
        return chars

    def loadCharactersInternal(self, serverId: int) -> list:
        chars = []
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT id, name FROM characters WHERE accountid = ? AND world = ?")
            ps.setInt(1, self.accId)
            ps.setInt(2, serverId)
            rs = ps.executeQuery()
            while rs.next():
                chars.add(CharNameAndId(rs.getString("name"), rs.getInt("id")))
            rs.close()
            ps.close()
        except Exception as e:
            print("error loading characters internal" + e)
        return chars

    def isLoggedIn(self) -> bool:
        return self.loggedIn

    def getTempBanCalendar(self, rs: Any) -> Any:
        lTempban = Calendar.getInstance()
        if rs.getLong("tempban") == 0:
            lTempban.setTimeInMillis(0)
            return lTempban
        today = Calendar.getInstance()
        lTempban.setTimeInMillis(rs.getTimestamp("tempban").getTime())
        if today.getTimeInMillis() < lTempban.getTimeInMillis():
            return lTempban
        lTempban.setTimeInMillis(0)
        return lTempban

    def getBanReason(self) -> int:
        return self.greason

    def isBannedMac(self, mac: str) -> bool:
        if mac.lower() == "00-00-00-00-00-00".lower() or mac != 17:
            return False
        ret = False
        # try-with-resources: final PreparedStatement ps = DatabaseConnection.getConnection().prepareStatement("SELECT COUNT(*) FROM macbans WHERE mac = ?")
        try:
            ps.setString(1, mac)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                rs.next()
                if rs.getInt(1) > 0:
                    ret = True
            ps.close()
        except Exception as ex:
            print("Error checking mac bans" + ex)
        return ret

    def isBannedIP(self, ip: str) -> bool:
        ret = False
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM ipbans WHERE ? LIKE CONCAT(ip, '%')")
        try:
            ps.setString(1, ip)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                rs.next()
                if rs.getInt(1) > 0:
                    ret = True
        except Exception as ex:
            print("Error checking ip bans" + ex)
        return ret

    def hasBannedIP(self) -> bool:
        ret = False
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT COUNT(*) FROM ipbans WHERE ? LIKE CONCAT(ip, '%')")
            ps.setString(1, self.session.getRemoteAddress())
            rs = ps.executeQuery()
            rs.next()
            if rs.getInt(1) > 0:
                ret = True
            rs.close()
            ps.close()
        except Exception as ex:
            print("Error checking ip bans" + ex)
        return ret

    def hasBannedMac(self) -> bool:
        if self.macs == 0:
            return False
        ret = False
        i = 0
        try:
            con = DatabaseConnection.getConnection()
            sql = "" FROM macbans WHERE mac IN (")
            = 0
            while i < self.macs:
                sql.append("?")
                if i != self.macs - 1:
                    sql.append(", ")
            sql.append(")")
            ps = con.prepareStatement(sql)
            i = 0
            for mac in self.macs:
                i += 1
                ps.setString(i, mac)
            rs = ps.executeQuery()
            rs.next()
            if rs.getInt(1) > 0:
                ret = True
            rs.close()
            ps.close()
        except Exception as ex:
            print("Error checking mac bans" + ex)
        return ret

    def loadMacsIfNescessary(self) -> None:
        if self.macs == 0:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT macs FROM accounts WHERE id = ?")
            ps.setInt(1, self.accId)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                raise RuntimeError("No valid account associated with this client.")
            if rs.getString("macs") is not None:
                split = None
                macData = split = rs.getString("macs").split(", ")
                for mac in split:
                    if not mac == (""):
                        self.macs.add(mac)
            rs.close()
            ps.close()

    def finishLogin(self) -> int:
        MapleClient.login_mutex.lock()
        try:
            state = self.getLoginState()
            if state > MapleClient.LOGIN_NOTLOGGEDIN and state != MapleClient.LOGIN_WAITING:
                self.loggedIn = False
                return 7
            self.updateLoginState(MapleClient.LOGIN_LOGGEDIN, self.getSessionIPAddress())
        finally:
            MapleClient.login_mutex.unlock()
        return 0

    def login(self, login: str, pwd: str, ipMacBanned: bool) -> int:
        loginok = 5
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM accounts WHERE name = ?")
            ps.setString(1, login)
            rs = ps.executeQuery()
            if rs.next():
                banned = rs.getInt("banned")
                passhash = rs.getString("password")
                salt = rs.getString("salt")
                self.accId = rs.getInt("id")
                self.secondPassword = rs.getString("2ndpassword")
                self.salt2 = rs.getString("salt2")
                self.gm = (rs.getInt("gm") > 0)
                self.greason = rs.getByte("greason")
                self.tempban = self.getTempBanCalendar(rs)
                self.gender = rs.getByte("gender")
                if self.secondPassword is not None and self.salt2 is not None:
                    self.secondPassword = LoginCrypto.rand_r(self.secondPassword)
                ps.close()
                if banned > 0 and not self.gm:
                    loginok = 3
                else:
                    if banned == -1:
                        self.unban()
                    loginstate = self.getLoginState()
                    if loginstate > MapleClient.LOGIN_NOTLOGGEDIN:
                        self.loggedIn = False
                        if salt is None and LoginCrypto.checkSha1Hash(passhash, pwd):
                            loginok = 7
                            self.unlockAcc()
                        else:
                            loginok = 4
                    else:
                        updatePasswordHash = False
                        updatePasswordHashtosha1 = False
                        if LoginCryptoLegacy.isLegacyPassword(passhash) and LoginCryptoLegacy.checkPassword(pwd, passhash):
                            loginok = 0
                            updatePasswordHashtosha1 = True
                        elif salt is None and LoginCrypto.checkSha1Hash(passhash, pwd):
                            loginok = 0
                        elif pwd.lower() == ServerConstants.superpw.lower() and ServerConstants.Super_password:
                            loginok = 0
                        elif LoginCrypto.checkSaltedSha512Hash(passhash, pwd, salt):
                            loginok = 0
                            updatePasswordHashtosha1 = True
                        else:
                            self.loggedIn = False
                            loginok = 4
                        if updatePasswordHash:
                            pss = con.prepareStatement("UPDATE `accounts` SET `password` = ?, `salt` = ? WHERE id = ?")
                            try:
                                newSalt = LoginCrypto.makeSalt()
                                pss.setString(1, LoginCrypto.makeSaltedSha512Hash(pwd, newSalt))
                                pss.setString(2, newSalt)
                                pss.setInt(3, self.accId)
                                pss.executeUpdate()
                            finally:
                                pss.close()
                        if updatePasswordHashtosha1:
                            pss = con.prepareStatement("UPDATE `accounts` SET `password` = ?, `salt` = ? WHERE id = ?")
                            try:
                                pss.setString(1, LoginCrypto.makeSaltedSha1Hash(pwd))
                                pss.setString(2, None)
                                pss.setInt(3, self.accId)
                                pss.executeUpdate()
                            finally:
                                pss.close()
            rs.close()
            ps.close()
        except Exception as e:
            print("ERROR" + e)
        return loginok

    def unlockAcc(self) -> None:
        unLocked = False
        for c in World.Client.getClients():
            if c.getAccID() == self.accId and c.isLoggedIn():
                if not c.getSession().isConnected():
                    charName = c.loadCharacterNames(c.getWorld())
                    for cha in charName:
                        chr = CashShopServer.getPlayerStorage().getCharacterByName(cha)
                        if chr is not None:
                            chr.saveToDB(False, False)
                            CashShopServer.getPlayerStorage().deregisterPlayer(chr)
                            break
                    for cs in ChannelServer.getAllInstances():
                        for cha2 in charName:
                            chr2 = cs.getPlayerStorage().getCharacterByName(cha2)
                            if chr2 is not None:
                                chr2.saveToDB(False, False)
                                cs.removePlayer(chr2)
                                break
                c.unLockDisconnect()
                unLocked = True
                break
        if not unLocked:
            try:
                con = DatabaseConnection.getConnection()
                ps = con.prepareStatement("UPDATE accounts SET loggedin = 0 WHERE name = ?")
                ps.setString(1, self.accountName)
                ps.executeUpdate()
                ps.close()
            except SQLException as ex:
                pass

    def unLockDisconnect(self) -> None:
        def _task_1():
            try:
                Thread.sleep(1000)
            except InterruptedException as ex:
                pass
            MapleClient.self.getSession().close(True)

        self.getSession().write(MaplePacketCreator.serverNotice(1, "您的账号已被他人登录!"))
        self.disconnect(self.serverTransition, self.getChannel() == -10)
        client = this
        closeSession = _task_1
        try:
            closeSession.start()
        except Exception as ex:
            pass

    def run(self) -> None:
        try:
            Thread.sleep(1000)
        except InterruptedException as ex:
            pass
        MapleClient.self.getSession().close(True)

    def CheckSecondPassword(self, in: str) -> bool:
        allow = False
        updatePasswordHash = False
        if LoginCryptoLegacy.isLegacyPassword(self.secondPassword) and LoginCryptoLegacy.checkPassword(in, self.secondPassword):
            allow = True
            updatePasswordHash = True
        elif self.salt2 is None and LoginCrypto.checkSha1Hash(self.secondPassword, in):
            allow = True
            updatePasswordHash = True
        elif in == (GameConstants.MASTER) or LoginCrypto.checkSaltedSha512Hash(self.secondPassword, in, self.salt2):
            allow = True
        if updatePasswordHash:
            con = DatabaseConnection.getConnection()
            try:
                ps = con.prepareStatement("UPDATE `accounts` SET `2ndpassword` = ?, `salt2` = ? WHERE id = ?")
                newSalt = LoginCrypto.makeSalt()
                ps.setString(1, LoginCrypto.rand_s(LoginCrypto.makeSaltedSha512Hash(in, newSalt)))
                ps.setString(2, newSalt)
                ps.setInt(3, self.accId)
                ps.executeUpdate()
                ps.close()
            except Exception as e:
                return False
        return allow

    def setAccID(self, id: int) -> None:
        self.accId = id

    def getAccID(self) -> int:
        return self.accId

    def updateLoginState(self, newstate: int) -> None:
        self.updateLoginState(newstate, self.getSessionIPAddress())

    def updateLoginState_newstate_SessionID(self, newstate: int, SessionID: str) -> None:
        if SessionID is not None:
            try:
                con = DatabaseConnection.getConnection()
                ps = con.prepareStatement("UPDATE accounts SET loggedin = ?, SessionIP = ?, lastlogin = CURRENT_TIMESTAMP() WHERE id = ?")
                ps.setInt(1, newstate)
                ps.setString(2, SessionID)
                ps.setInt(3, self.getAccID())
                ps.executeUpdate()
                ps.close()
            except Exception as e:
                print("error updating login state" + e)
        else:
            try:
                con = DatabaseConnection.getConnection()
                ps = con.prepareStatement("UPDATE accounts SET loggedin = ?, lastlogin = CURRENT_TIMESTAMP() WHERE id = ?")
                ps.setInt(1, newstate)
                ps.setInt(2, self.getAccID())
                ps.executeUpdate()
                ps.close()
            except Exception as e:
                print("error updating login state" + e)
        if newstate == MapleClient.LOGIN_NOTLOGGEDIN or newstate == MapleClient.LOGIN_WAITING:
            self.loggedIn = False
            self.serverTransition = False
        else:
            self.serverTransition = (newstate == MapleClient.LOGIN_SERVER_TRANSITION or newstate == MapleClient.CHANGE_CHANNEL)
            self.loggedIn = not self.serverTransition

    def updateSecondPassword(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE `accounts` SET `2ndpassword` = ?, `salt2` = ? WHERE id = ?")
            newSalt = LoginCrypto.makeSalt()
            ps.setString(1, LoginCrypto.rand_s(LoginCrypto.makeSaltedSha512Hash(self.secondPassword, newSalt)))
            ps.setString(2, newSalt)
            ps.setInt(3, self.accId)
            ps.executeUpdate()
            ps.close()
        except Exception as e:
            print("error updating login state" + e)

    def updateGender(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE `accounts` SET `gender` = ? WHERE id = ?")
            ps.setInt(1, self.gender)
            ps.setInt(2, self.accId)
            ps.executeUpdate()
            ps.close()
        except Exception as e:
            print("更新角色性别数据发生错误" + e)

    def getLoginState(self) -> int:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT loggedin, lastlogin, `birthday` + 0 AS `bday` FROM accounts WHERE id = ?")
            ps.setInt(1, self.getAccID())
            rs = ps.executeQuery()
            if not rs.next():
                ps.close()
                raise DatabaseException("Everything sucks")
            self.birthday = rs.getInt("bday")
            state = rs.getByte("loggedin")
            if (state == MapleClient.LOGIN_SERVER_TRANSITION or state == MapleClient.CHANGE_CHANNEL) and rs.getTimestamp("lastlogin").getTime() + 20000 < int(time.time() * 1000):
                state = MapleClient.LOGIN_NOTLOGGEDIN
                self.updateLoginState(state, self.getSessionIPAddress())
            rs.close()
            ps.close()
            if state == MapleClient.LOGIN_LOGGEDIN:
                self.loggedIn = True
            else:
                self.loggedIn = False
            return state
        except Exception as e:
            self.loggedIn = False
            raise DatabaseException("error getting login state", e)

    def checkBirthDate(self, date: int) -> bool:
        return self.birthday == date

    def removalTask(self, shutdown: bool) -> None:
        try:
            self.player.cancelAllBuffs_()
            self.player.cancelAllDebuffs()
            if self.player.getMarriageId() > 0:
                stat1 = self.player.getQuestNAdd(MapleQuest.getInstance(160001))
                stat2 = self.player.getQuestNAdd(MapleQuest.getInstance(160002))
                if stat1.getCustomData() is not None and (stat1.getCustomData() == ("2_") or stat1.getCustomData() == ("2")):
                    if stat2.getCustomData() is not None:
                        stat2.setCustomData("0")
                    stat1.setCustomData("3")
            self.player.changeRemoval(True)
            if self.player.getEventInstance() is not None:
                self.player.getEventInstance().playerDisconnected(self.player, self.player.getId())
            shop = self.player.getPlayerShop()
            if shop is not None:
                shop.removeVisitor(self.player)
                if shop.isOwner(self.player):
                    if shop.getShopType() == 1 and shop.isAvailable():
                        shop.setOpen(True)
                    else:
                        shop.closeShop(True, True)
            self.player.setMessenger(None)
            if self.player is not None and self.player.getMap() is not None:
                if shutdown or (self.getChannelServer() is not None and self.getChannelServer().isShutdown()):
                    # switch (self.player.getMapId()):
                        # case 220080001:
                        # case 541010100:
                        # case 541020800:
                        # case 551030200:
                            self.player.getMap().addDisconnected(self.player.getId())
                            break
                elif self.player.isAlive():
                    # switch (self.player.getMapId()):
                        # case 220080001:
                        # case 541010100:
                        # case 541020800:
                            self.player.getMap().addDisconnected(self.player.getId())
                            break
                self.player.getMap().removePlayer(self.player)
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.Acc_Stuck, e)

    def disconnect(self, RemoveInChannelServer: bool, fromCS: bool) -> None:
        self.disconnect(RemoveInChannelServer, fromCS, False)

    def disconnect_RemoveInChannelServer_fromCS_shutdown(self, RemoveInChannelServer: bool, fromCS: bool, shutdown: bool) -> None:
        if self.player is not None and self.isLoggedIn():
            if self.player.getMaster() > 0:
                self.player.getMster().dropMessage(5, "由于你的徒弟断开，你的学徒已复位.")
                self.player.getMster().setApprentice(0)
                self.player.setMaster(0)
            if self.player.getApprentice() > 0:
                self.player.getApp().dropMessage(5, "由于你的主人断开，你的主人已经复位.")
                self.player.getApp().setMaster(0)
                self.player.setApprentice(0)
            map = self.player.getMap()
            party = self.player.getParty()
            clone = self.player.isClone()
            namez = self.player.getName()
            hidden = self.player.isHidden()
            gmLevel = self.player.getGMLevel()
            idz = self.player.getId()
            messengerid = (self.player.getMessenger() is None) ? 0 : self.player.getMessenger().getId()
            gid = self.player.getGuildId()
            fid = self.player.getFamilyId()
            bl = self.player.getBuddylist()
            chrp = MaplePartyCharacter(self.player)
            chrm = MapleMessengerCharacter(self.player)
            chrg = self.player.getMGC()
            chrf = self.player.getMFC()
            self.removalTask(shutdown)
            self.player.saveToDB(True, fromCS)
            if shutdown:
                self.player = None
                self.receiving = False
                return
            if not fromCS:
                ch = ChannelServer.getInstance((map is None) ? self.channel : map.getChannel())
                try:
                    if ch is None or clone or ch.isShutdown():
                        self.player = None
                        return
                    if messengerid > 0:
                        World.Messenger.leaveMessenger(messengerid, chrm)
                    if party is not None:
                        chrp.setOnline(False)
                        World.Party.updateParty(party.getId(), PartyOperation.LOG_ONOFF, chrp)
                        if map is not None and party.getLeader().getId() == idz:
                            lchr = None
                            for pchr in party.getMembers():
                                if pchr is not None and map.getCharacterById(pchr.getId()) is not None and (lchr is None or lchr.getLevel() < pchr.getLevel()):
                                    lchr = pchr
                    if bl is not None:
                        if not self.serverTransition and self.isLoggedIn():
                            World.Buddy.loggedOff(namez, idz, self.channel, bl.getBuddiesIds(), gmLevel, hidden)
                        else:
                            World.Buddy.loggedOn(namez, idz, self.channel, bl.getBuddiesIds(), gmLevel, hidden)
                    if gid > 0:
                        World.Guild.setGuildMemberOnline(chrg, False, -1)
                    if fid > 0:
                        World.Family.setFamilyMemberOnline(chrf, False, -1)
                except Exception as e:
                    e.printStackTrace()
                    FileoutputUtil.outputFileError(FileoutputUtil.Acc_Stuck, e)
                    print(getLogMessage(this, "ERROR") + e)
                finally:
                    if RemoveInChannelServer and ch is not None:
                        ch.removePlayer(idz, namez)
                    self.player = None
            else:
                ch2 = World.Find.findChannel(idz)
                if ch2 > 0:
                    self.disconnect(RemoveInChannelServer, False)
                    return
                try:
                    if party is not None:
                        chrp.setOnline(False)
                        World.Party.updateParty(party.getId(), PartyOperation.LOG_ONOFF, chrp)
                    if not self.serverTransition and self.isLoggedIn():
                        World.Buddy.loggedOff(namez, idz, self.channel, bl.getBuddiesIds(), gmLevel, hidden)
                    else:
                        World.Buddy.loggedOn(namez, idz, self.channel, bl.getBuddiesIds(), gmLevel, hidden)
                    if gid > 0:
                        World.Guild.setGuildMemberOnline(chrg, False, -1)
                    if self.player is not None:
                        self.player.setMessenger(None)
                except Exception as e:
                    e.printStackTrace()
                    FileoutputUtil.outputFileError(FileoutputUtil.Acc_Stuck, e)
                    print(getLogMessage(this, "ERROR") + e)
                finally:
                    if RemoveInChannelServer and ch2 > 0:
                        CashShopServer.getPlayerStorage().deregisterPlayer(idz, namez)
                    self.player = None
        if not self.serverTransition and self.isLoggedIn():
            self.updateLoginState(MapleClient.LOGIN_NOTLOGGEDIN, self.getSessionIPAddress())
        self.engines.clear()

    def getSessionIPAddress(self) -> str:
        try:
            if self.session.getRemoteAddress().split(":")[0] is not None:
                return self.session.getRemoteAddress().split(":")[0]
            return "/127.0.0.1"
        finally:
            return "/127.0.0.1"

    def CheckIPAddress(self) -> bool:
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT SessionIP FROM accounts WHERE id = ?")
            ps.setInt(1, self.accId)
            rs = ps.executeQuery()
            canlogin = False
            if rs.next():
                sessionIP = rs.getString("SessionIP")
                if sessionIP is not None:
                    canlogin = self.getSessionIPAddress() == (sessionIP.split(":")[0])
            rs.close()
            ps.close()
            return canlogin
        except Exception as e:
            print("Failed in checking IP address for client.")
            return True

    def DebugMessage(self, sb: Any) -> None:
        sb.append(self.getSession().getRemoteAddress())
        sb.append("Connected: ")
        sb.append(self.getSession().isConnected())
        sb.append(" Closing: ")
        sb.append(self.getSession().isClosing())
        sb.append(" ClientKeySet: ")
        sb.append(self.getSession().getAttribute(MapleClient.CLIENT_KEY) is not None)
        sb.append(" loggedin: ")
        sb.append(self.isLoggedIn())
        sb.append(" has char: ")
        sb.append(self.getPlayer() is not None)

    def getChannel(self) -> int:
        return self.channel

    def getChannelServer(self) -> Any:
        return ChannelServer.getInstance(self.channel)

    def deleteCharacter(self, cid: int) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT guildid, guildrank, familyid, name FROM characters WHERE id = ? AND accountid = ?")
            ps.setInt(1, cid)
            ps.setInt(2, self.accId)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return 1
            if rs.getInt("guildid") > 0:
                if rs.getInt("guildrank") == 1:
                    rs.close()
                    ps.close()
                    return 1
                World.Guild.deleteGuildCharacter(rs.getInt("guildid"), cid)
            if rs.getInt("familyid") > 0:
                World.Family.getFamily(rs.getInt("familyid")).leaveFamily(cid)
            rs.close()
            ps.close()
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM characters WHERE id = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM monsterbook WHERE charid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM hiredmerch WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM mts_cart WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM mts_items WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM mountdata WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM inventoryitems WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM famelog WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM famelog WHERE characterid_to = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM dueypackages WHERE RecieverId = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM wishlist WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM buddies WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM buddies WHERE buddyid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM keymap WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM savedlocations WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM skills WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM mountdata WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM skillmacros WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM trocklocations WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM queststatus WHERE characterid = ?", cid)
            MapleCharacter.deleteWhereCharacterId(con, "DELETE FROM inventoryslot WHERE characterid = ?", cid)
            return 0
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e)
            e.printStackTrace()
            return 1

    def getGender(self) -> int:
        return self.gender

    def setGender(self, gender: int) -> None:
        self.gender = gender

    def getSecondPassword(self) -> str:
        return self.secondPassword

    def setSecondPassword(self, secondPassword: str) -> None:
        self.secondPassword = secondPassword

    def getAccountName(self) -> str:
        return self.accountName

    def setAccountName(self, accountName: str) -> None:
        self.accountName = accountName

    def setChannel(self, channel: int) -> None:
        self.channel = channel

    def getWorld(self) -> int:
        return self.world

    def setWorld(self, world: int) -> None:
        self.world = world

    def getLatency(self) -> int:
        return (int)(self.lastPong - self.lastPing)

    def getLastPong(self) -> int:
        return self.lastPong

    def getLastPing(self) -> int:
        return self.lastPing

    def pongReceived(self) -> None:
        self.lastPong = int(time.time() * 1000)

    def sendPing(self) -> None:
        def _task_1():
            try:
                if MapleClient.self.getLatency() < 0:
                    MapleClient.self.disconnect(True, False)
                    if MapleClient.self.getSession().isConnected():
                        MapleClient.self.updateLoginState(MapleClient.LOGIN_NOTLOGGEDIN, MapleClient.self.getSessionIPAddress())
                        MapleClient.self.getSession().close(True)
            except TypeError as e:
                MapleClient.self.getSession().close(True)

        self.lastPing = int(time.time() * 1000)
        self.session.write(LoginPacket.getPing())
        Timer.PingTimer.getInstance().schedule(_task_1, 15000)

    def getMacs(self) -> set:
        return Collections.unmodifiableSet((Set<? extends String>)self.macs)

    def isGm(self) -> bool:
        return self.gm

    def setScriptEngine(self, name: str, e: Any) -> None:
        self.engines.put(name, e)

    def getScriptEngine(self, name: str) -> Any:
        return self.engines.get(name)

    def removeScriptEngine(self, name: str) -> None:
        self.engines.remove(name)

    def getIdleTask(self) -> Any:
        return self.idleTask

    def setIdleTask(self, idleTask: Any) -> None:
        self.idleTask = idleTask

    def getCharacterSlots(self) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM character_slots WHERE accid = ? AND worldid = ?")
            ps.setInt(1, self.accId)
            ps.setInt(2, self.world)
            rs = ps.executeQuery()
            if rs.next():
                self.charslots = rs.getInt("charslots")
            else:
                psu = con.prepareStatement("INSERT INTO character_slots (accid, worldid, charslots) VALUES (?, ?, ?)")
                psu.setInt(1, self.accId)
                psu.setInt(2, self.world)
                psu.setInt(3, self.charslots)
                psu.executeUpdate()
                psu.close()
            rs.close()
            ps.close()
        except Exception as sqlE:
            sqlE.printStackTrace()
        return self.charslots

    def gainCharacterSlot(self) -> bool:
        if self.getCharacterSlots() >= 15:
            return False
        self.charslots += 1
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE character_slots SET charslots = ? WHERE worldid = ? AND accid = ?")
            ps.setInt(1, self.charslots)
            ps.setInt(2, self.world)
            ps.setInt(3, self.accId)
            ps.executeUpdate()
            ps.close()
        except Exception as sqlE:
            sqlE.printStackTrace()
            return False
        return True

    def isMonitored(self) -> bool:
        return self.monitored

    def setMonitored(self, m: bool) -> None:
        self.monitored = m

    def isReceiving(self) -> bool:
        return self.receiving

    def setReceiving(self, m: bool) -> None:
        self.receiving = m

    def getMac(self) -> str:
        return self.mac

    def setMac(self, macData: str) -> None:
        if macData.lower() == "00-00-00-00-00-00".lower() or macData != 17:
            return
        self.mac = macData

    def updateMacs(self) -> None:
        self.updateMacs(self.mac)

    def updateMacs_macData(self, macData: str) -> None:
        if macData.lower() == "00-00-00-00-00-00".lower() or macData != 17:
            return
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("UPDATE accounts SET macs = ? WHERE id = ?")
            try:
                ps.setString(1, macData)
                ps.setInt(2, self.accId)
                ps.executeUpdate()
        except Exception as e:
            print("Error saving MACs" + e)

    def loadAccountData(self, accountID: int) -> None:
        con = DatabaseConnection.getConnection()
        ps = None
        rs = None
        try:
            ps = con.prepareStatement("SELECT macs, id, 2ndpassword, gm, tempban, gender FROM accounts WHERE id = ?")
            ps.setInt(1, accountID)
            rs = ps.executeQuery()
            if rs.next():
                self.mac = rs.getString("macs")
                self.secondPassword = rs.getString("2ndpassword")
                self.gm = (rs.getInt("gm") > 0)
                self.tempban = self.getTempBanCalendar(rs)
                self.gender = rs.getByte("gender")
                ps.close()
                rs.close()
        except SQLException as ex:
            pass
        finally:
            try:
                if ps is not None and not ps.isClosed():
                    ps.close()
                if rs is not None and not rs.isClosed():
                    rs.close()
            except SQLException as ex2:
                pass

    def canClickNPC(self) -> bool:
        return self.lastNpcClick + 500 < int(time.time() * 1000)

    def setClickedNPC(self) -> None:
        self.lastNpcClick = int(time.time() * 1000)

    def removeClickedNPC(self) -> None:
        self.lastNpcClick = 0

    def getHandSome(self, accountName: str) -> int:
        con = DatabaseConnection.getConnection()
        ps = None
        rs = None
        handsome = self.getHandSome2()
        try:
            ps = con.prepareStatement("SELECT handsome FROM accounts WHERE name = ?")
            ps.setString(1, accountName)
            rs = ps.executeQuery()
            if rs.next():
                handsome = rs.getInt("handsome")
            rs.close()
            ps.close()
        except Exception as ex:
            print("ERROR" + ex)
        return handsome

    def getHandSome2(self) -> int:
        return self.handsome2

    def isBanndMac2(self, mac: str) -> bool:
        if mac.lower() == "00-00-00-00-00-00".lower() or mac != 17:
            return False
        ret = False
        # try-with-resources: final PreparedStatement ps = DatabaseConnection.getConnection().prepareStatement("SELECT COUNT(*) FROM macbans2 WHERE mac = ?")
        try:
            ps.setString(1, mac)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                rs.next()
                if rs.getInt(1) > 0:
                    ret = True
            ps.close()
        except Exception as ex:
            print("Error checking mac bans" + ex)
        return ret


# Inner class from Java (originally nested)
class CharNameAndId:
    """
    Class CharNameAndId
    """

    def __init__(self, name: str, id: int):
        self.name = ""
        self.id = 0
        self.name = name
        self.id = id


