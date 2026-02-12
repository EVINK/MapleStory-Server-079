"""
MapleCharacterUtil - Converted from Java source
Original: client/MapleCharacterUtil.java
Package: client
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import pymysql
import time

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleCharacterUtil:
    """
    Class MapleCharacterUtil
    """

    # Static initializer
    # namePattern = Pattern.compile("[a-zA-Z0-9_-]{3,12}")
    # petPattern = Pattern.compile("[a-zA-Z0-9_-]{4,12}")


    @staticmethod
    def canCreateChar(name: str) -> bool:
        return getIdByName(name) == -1 and isEligibleCharName(name)

    def isEligibleCharName(self, name: str) -> bool:
        if name > 15:
            return False
        if name < 2:
            return False
        for z in GameConstants.RESERVED:
            if name.find(z) != -1:
                return False
        return True

    def canChangePetName(self, name: str) -> bool:
        if MapleCharacterUtil.petPattern.matcher(name).matches():
            for z in GameConstants.RESERVED:
                if name.find(z) != -1:
                    return False
            return True
        return False

    def makeMapleReadable(self, in: str) -> str:
        wui = in.replace('I', 'i')
        wui = wui.replace('l', 'L')
        wui = wui.replace("rn", "Rn")
        wui = wui.replace("vv", "Vv")
        wui = wui.replace("VV", "Vv")
        return wui

    def getIdByName(self, name: str) -> int:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT id FROM characters WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            id = rs.getInt("id")
            rs.close()
            ps.close()
            return id
        except Exception as e:
            print("error 'getIdByName' " + e)
            return -1

    def PromptPoll(self, accountid: int) -> bool:
        ps = None
        rs = None
        prompt = False
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT * from game_poll_reply where AccountId = ?")
            ps.setInt(1, accountid)
            rs = ps.executeQuery()
            prompt = not rs.next()
        except SQLException as ex:
            pass
        finally:
            try:
                if ps is not None:
                    ps.close()
                if rs is not None:
                    rs.close()
            except SQLException as ex2:
                pass
        return prompt

    def SetPoll(self, accountid: int, selection: int) -> bool:
        if not PromptPoll(accountid):
            return False
        ps = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO game_poll_reply (AccountId, SelectAns) VALUES (?, ?)")
            ps.setInt(1, accountid)
            ps.setInt(2, selection)
            ps.execute()
        except SQLException as ex:
            pass
        finally:
            try:
                if ps is not None:
                    ps.close()
            except SQLException as ex2:
                pass
        return True

    def Change_SecondPassword(self, accid: int, password: str, newpassword: str) -> int:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * from accounts where id = ?")
            ps.setInt(1, accid)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return -1
            secondPassword = rs.getString("2ndpassword")
            salt2 = rs.getString("salt2")
            if secondPassword is not None and salt2 is not None:
                secondPassword = LoginCrypto.rand_r(secondPassword)
            elif secondPassword is None and salt2 is None:
                rs.close()
                ps.close()
                return 0
            if not check_ifPasswordEquals(secondPassword, password, salt2):
                rs.close()
                ps.close()
                return 1
            rs.close()
            ps.close()
            SHA1hashedsecond = None
            try:
                SHA1hashedsecond = LoginCryptoLegacy.encodeSHA1(newpassword)
            catch (UnsupportedEncodingException | NoSuchAlgorithmException ex2)
                ex2.printStackTrace()
                return -2
            ps = con.prepareStatement("UPDATE accounts set 2ndpassword = ?, salt2 = ? where id = ?")
            ps.setString(1, SHA1hashedsecond)
            ps.setString(2, None)
            ps.setInt(3, accid)
            if not ps.execute():
                ps.close()
                return 2
            ps.close()
            return -2
        except Exception as e2:
            print("error 'getIdByName' " + e2)
            return -2

    def check_ifPasswordEquals(self, passhash: str, pwd: str, salt: str) -> bool:
        return (LoginCryptoLegacy.isLegacyPassword(passhash) and LoginCryptoLegacy.checkPassword(pwd, passhash)) or (salt is None and LoginCrypto.checkSha1Hash(passhash, pwd)) or LoginCrypto.checkSaltedSha512Hash(passhash, pwd, salt)

    def getInfoByName(self, name: str, world: int) -> Any:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM characters WHERE name = ? AND world = ?")
            ps.setString(1, name)
            ps.setInt(2, world)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return None
            id = new Pair<Integer, Pair<Integer, Integer>>(rs.getInt("id"), new Pair<Integer, Integer>(rs.getInt("accountid"), rs.getInt("gender")))
            rs.close()
            ps.close()
            return id
        except Exception as e:
            e.printStackTrace()
            return None

    def setNXCodeUsed(self, name: str, code: str) -> None:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("UPDATE nxcode SET `user` = ?, `valid` = 0 WHERE code = ?")
        ps.setString(1, name)
        ps.setString(2, code)
        ps.execute()
        ps.close()

    def sendNote(self, to: str, name: str, msg: str, fame: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("INSERT INTO notes (`to`, `from`, `message`, `timestamp`, `gift`) VALUES (?, ?, ?, ?, ?)")
            ps.setString(1, to)
            ps.setString(2, name)
            ps.setString(3, msg)
            ps.setLong(4, int(time.time() * 1000))
            ps.setInt(5, fame)
            ps.executeUpdate()
            ps.close()
        except Exception as e:
            print("Unable to send note" + e)

    def getNXCodeValid(self, code: str, validcode: bool) -> bool:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT `valid` FROM nxcode WHERE code = ?")
        ps.setString(1, code)
        rs = ps.executeQuery()
        if rs.next():
            validcode = (rs.getInt("valid") > 0)
        rs.close()
        ps.close()
        return validcode

    def getNXCodeType(self, code: str) -> int:
        type = -1
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT `type` FROM nxcode WHERE code = ?")
        ps.setString(1, code)
        rs = ps.executeQuery()
        if rs.next():
            type = rs.getInt("type")
        rs.close()
        ps.close()
        return type

    def getNXCodeItem(self, code: str) -> int:
        item = -1
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT `item` FROM nxcode WHERE code = ?")
        ps.setString(1, code)
        rs = ps.executeQuery()
        if rs.next():
            item = rs.getInt("item")
        rs.close()
        ps.close()
        return item

