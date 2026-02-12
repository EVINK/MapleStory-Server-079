"""
CharLoginHandler - Converted from Java source
Original: handling/login/handler/CharLoginHandler.java
Package: handling.login.handler
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from typing import List
from typing import Optional, Any
import os

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginInformationProvider import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.login.LoginWorker import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.KoreanDateUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.LoginPacket import *  # TODO: import specific classes


class CharLoginHandler:
    """
    Class CharLoginHandler
    """


    def loginFailCount(self, c: Any) -> bool:
        c.loginAttempt += 1
        return c.loginAttempt > 5

    def login(self, slea: Any, c: Any) -> None:
        login = slea.readMapleAsciiString()
        pwd = slea.readMapleAsciiString()
        c.setAccountName(login)
        bytes = new int[6]
        for i in range(len(bytes)):
            bytes[i] = slea.readByteAsInt()
        sps = ""
        for j in range(len(bytes)):
            sps.append(StringUtil.getLeftPaddedStr(Integer.toHexString(bytes[j]).upper(), '0', 2))
            sps.append("-")
        macData = sps
        macData = macData[0:macData.__len__(] - 1)
        c.setMac(macData)
        ip = c.getSession().getRemoteAddress().split(":")[0]
        ip = ip[1:ip.__len__(])
        s = c.getHandSome2()
        getS = c.getHandSome(login)
        防万能 = False
        if !ip.lower() == "127.0.0.1".lower() && getS == s:
            防万能 = False
        ipBan = c.hasBannedIP()
        macBan = c.isBannedMac(macData)
        banned = ipBan || macBan || 防万能
        loginok = 0
        if !bool(ServerProperties.getProperty("RoyMS.AutoRegister")) || !AutoRegister.autoRegister || AutoRegister.getAccountExists(login) || banned:
            AutoRegister.success = True
            AutoRegister.mac = True
            loginok = c.login(login, pwd, ipBan || macBan || 防万能)
            tempbannedTill = c.getTempBanCalendar()
            if loginok == 0 && (ipBan || macBan || 防万能) && !c.isGm():
                loginok = 3
                if macBan || ipBan:
                    MapleCharacter.ban(c.getSession().getRemoteAddress().split(":")[0], "Enforcing account ban, account " + login, False, 4, False)
                if 防万能:
                    c.getSession().write(MaplePacketCreator.serverNotice(1, "请使用本服专用登录器登录。"))
                    c.getSession().write(LoginPacket.getLoginFailed(1))
                    return
            if loginok != 0:
                if !loginFailCount(c):
                    c.getSession().write(LoginPacket.getLoginFailed(loginok))
            elif tempbannedTill.getTimeInMillis() != 0:
                if !loginFailCount(c):
                    c.getSession().write(LoginPacket.getTempBan(KoreanDateUtil.getTempBanTimestamp(tempbannedTill.getTimeInMillis()), c.getBanReason()))
            else:
                FileoutputUtil.logToFile("logs/ACPW.txt", "ACC: " + login + " PW: " + pwd + " MAC : " + macData + " IP: " + c.getSession().getRemoteAddress() + "\r\n")
                c.updateMacs()
                c.loginAttempt = 0
                LoginWorker.registerClient(c)
            return
        if pwd.lower() == "disconnect".lower() || pwd.lower() == "fixme".lower() || pwd.lower() == "admin".lower() || pwd.lower() == "000000".lower():
            c.getSession().write(MaplePacketCreator.serverNotice(1, "你不可以使用这个作为密码."))
            c.getSession().write(LoginPacket.getLoginFailed(1))
            return
        AutoRegister.createAccount(login, pwd, c.getSession().getRemoteAddress(), macData)
        if AutoRegister.success && AutoRegister.mac:
            c.getSession().write(MaplePacketCreator.serverNotice(1, "友情提示：账号创建成功,请尝试重新登录!\r\n拒绝一切第三方辅助程序\r\n提倡手动从我做起-举报开挂有奖\r\n！"))
        elif !AutoRegister.mac:
            c.getSession().write(MaplePacketCreator.serverNotice(1, "友情提示：账号创建失败，你已经注册过账号，一个机器码只能注册一个账号"))
        AutoRegister.success = True
        AutoRegister.mac = True
        c.getSession().write(LoginPacket.getLoginFailed(1))

    def SetGenderRequest(self, slea: Any, c: Any) -> None:
        gender = slea.readByte()
        username = slea.readMapleAsciiString()
        if c.getAccountName() == (username):
            c.setGender(gender)
            c.updateSecondPassword()
            c.updateGender()
            c.getSession().write(LoginPacket.getGenderChanged(c))
            c.getSession().write(MaplePacketCreator.licenseRequest())
            c.updateLoginState(MapleClient.LOGIN_NOTLOGGEDIN, c.getSessionIPAddress())
        else:
            c.getSession().close(True)

    def ServerListRequest(self, c: Any) -> None:
        c.getSession().write(LoginPacket.getServerList(0, LoginServer.getServerName(), LoginServer.getLoad()))
        c.getSession().write(LoginPacket.getEndOfServerList())

    def ServerStatusRequest(self, c: Any) -> None:
        numPlayer = LoginServer.getUsersOn()
        userLimit = LoginServer.getUserLimit()
        if numPlayer >= userLimit:
            c.getSession().write(LoginPacket.getServerStatus(2))
        elif numPlayer * 2 >= userLimit:
            c.getSession().write(LoginPacket.getServerStatus(1))
        else:
            c.getSession().write(LoginPacket.getServerStatus(0))

    def CharlistRequest(self, slea: Any, c: Any) -> None:
        server = slea.readByte()
        channel = slea.readByte() + 1
        slea.readInt()
        c.setWorld(server)
        c.setChannel(channel)
        chars = c.loadCharacters(server)
        if chars is not None:
            c.getSession().write(LoginPacket.getCharList(c.getSecondPassword() is not None, chars, c.getCharacterSlots()))
        else:
            c.getSession().close(True)

    def CheckCharName(self, name: str, c: Any) -> None:
        c.getSession().write(LoginPacket.charNameResponse(name, !MapleCharacterUtil.canCreateChar(name) || LoginInformationProvider.getInstance().isForbiddenName(name)))

    def CreateChar(self, slea: Any, c: Any) -> None:
        name = slea.readMapleAsciiString()
        JobType = slea.readInt()
        # 冒险家
        mxj = bool(ServerProperties.getProperty("RoyMS.mxj"))
        # 骑士团
        qst = bool(ServerProperties.getProperty("RoyMS.qst"))
        # 战神
        zs = bool(ServerProperties.getProperty("RoyMS.zs"))
        if !qst && JobType == 0:
            c.getSession().write(MaplePacketCreator.serverNotice(1, "暂未开放骑士团职业！,请联系GM开放"))
            c.getSession().write(LoginPacket.getLoginFailed(1))
            return
        if !mxj && JobType == 1:
            c.getSession().write(MaplePacketCreator.serverNotice(1, "暂未开放冒险家职业！,请联系GM开放"))
            c.getSession().write(LoginPacket.getLoginFailed(1))
            return
        if !zs && JobType == 2:
            c.getSession().write(MaplePacketCreator.serverNotice(1, "暂未开放战神职业！,请联系GM开放"))
            c.getSession().write(LoginPacket.getLoginFailed(1))
            return
        db = 0
        face = slea.readInt()
        hair = slea.readInt()
        hairColor = 0
        skinColor = 0
        top = slea.readInt()
        bottom = slea.readInt()
        shoes = slea.readInt()
        weapon = slea.readInt()
        gender = c.getGender()
        # switch (gender):
            # case 0:
                if face != 20100 && face != 20401 && face != 20402:
                    return
                if hair != 30030 && hair != 30027 && hair != 30000:
                    return
                if top != 1040002 && top != 1040006 && top != 1040010 && top != 1042167:
                    return
                if bottom != 1060002 && bottom != 1060006 && bottom != 1062115:
                    return
                break
            # case 1:
                if face != 21002 && face != 21700 && face != 21201:
                    return
                if hair != 31002 && hair != 31047 && hair != 31057:
                    return
                if top != 1041002 && top != 1041006 && top != 1041010 && top != 1041011 && top != 1042167:
                    return
                if bottom != 1061002 && bottom != 1061008 && bottom != 1062115:
                    return
                break
            # default:
                return
        if shoes != 1072001 && shoes != 1072005 && shoes != 1072037 && shoes != 1072038 && shoes != 1072383:
            return
        if weapon != 1302000 && weapon != 1322005 && weapon != 1312004 && weapon != 1442079:
            return
        newchar = MapleCharacter.getDefault(c, JobType)
        newchar.setWorld(c.getWorld())
        newchar.setFace(face)
        newchar.setHair(hair + hairColor)
        newchar.setGender(gender)
        newchar.setName(name)
        newchar.setSkinColor(skinColor)
        equip = newchar.getInventory(MapleInventoryType.EQUIPPED)
        li = MapleItemInformationProvider.getInstance()
        item = li.getEquipById(top)
        item.setPosition((short)(-5))
        equip.addFromDB(item)
        item = li.getEquipById(bottom)
        item.setPosition((short)(-6))
        equip.addFromDB(item)
        item = li.getEquipById(shoes)
        item.setPosition((short)(-7))
        equip.addFromDB(item)
        item = li.getEquipById(weapon)
        item.setPosition((short)(-11))
        equip.addFromDB(item)
        # switch (JobType):
            # case 0:
                newchar.setQuestAdd(MapleQuest.getInstance(20022), 1, "1")
                newchar.setQuestAdd(MapleQuest.getInstance(20010), 1, None)
                newchar.setQuestAdd(MapleQuest.getInstance(20000), 1, None)
                newchar.setQuestAdd(MapleQuest.getInstance(20015), 1, None)
                newchar.setQuestAdd(MapleQuest.getInstance(20020), 1, None)
                newchar.getInventory(MapleInventoryType.ETC).addItem(Item(4161047, 0, 1, 0))
                newchar.getInventory(MapleInventoryType.USE).addItem(Item(2022336, 0, 1, 0))
                break
            # case 1:
                newchar.getInventory(MapleInventoryType.ETC).addItem(Item(4161001, 0, 1, 0))
                newchar.getInventory(MapleInventoryType.USE).addItem(Item(2022336, 0, 1, 0))
                break
            # case 2:
                newchar.getInventory(MapleInventoryType.ETC).addItem(Item(4161048, 0, 1, 0))
                newchar.getInventory(MapleInventoryType.USE).addItem(Item(2022336, 0, 1, 0))
                break
        if JobType == 0:
            newchar.setQuestAdd(MapleQuest.getInstance(20022), 1, "1")
            newchar.setQuestAdd(MapleQuest.getInstance(20010), 1, None)
        if MapleCharacterUtil.canCreateChar(name) && !LoginInformationProvider.getInstance().isForbiddenName(name):
            MapleCharacter.saveNewCharToDB(newchar, JobType, JobType == 1 && db == 0)
            c.getSession().write(LoginPacket.addNewCharEntry(newchar, True))
            c.createdChar(newchar.getId())
        else:
            c.getSession().write(LoginPacket.addNewCharEntry(newchar, False))

    def Character_WithoutSecondPassword(self, slea: Any, c: Any) -> None:
        charId = slea.readInt()
        if !c.isLoggedIn() || loginFailCount(c) || !c.login_Auth(charId):
            c.getSession().write(MaplePacketCreator.enableActions())
            return
        if ChannelServer.getInstance(c.getChannel()) is None || c.getWorld() != 0:
            c.getSession().close(True)
            return
        if c.getIdleTask() is not None:
            c.getIdleTask().cancel(True)
        ip = c.getSessionIPAddress()
        LoginServer.putLoginAuth(charId, ip[ip.find(47:] + 1, ip), c.getTempIP(), c.getChannel())
        c.updateLoginState(MapleClient.LOGIN_SERVER_TRANSITION, ip)
        c.getSession().write(MaplePacketCreator.getServerIP(int(ChannelServer.getInstance(c.getChannel()).getIP().split(":")[1]), charId))

    def Welcome(self, c: Any) -> None:
        pass

