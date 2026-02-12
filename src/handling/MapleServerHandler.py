"""
MapleServerHandler - Converted from Java source
Original: handling/MapleServerHandler.java
Package: handling
"""

from io import open
from pathlib import Path
from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import asyncio
import os
import sys
import threading
import time
import tkinter

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.cashshop.handler.CashShopOperation import *  # TODO: import specific classes
# from handling.cashshop.handler.MTSOperation import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.channel.handler.AllianceHandler import *  # TODO: import specific classes
# from handling.channel.handler.BBSHandler import *  # TODO: import specific classes
# from handling.channel.handler.BeanGame import *  # TODO: import specific classes
# from handling.channel.handler.BuddyListHandler import *  # TODO: import specific classes
# from handling.channel.handler.ChatHandler import *  # TODO: import specific classes
# from handling.channel.handler.DueyHandler import *  # TODO: import specific classes
# from handling.channel.handler.FamilyHandler import *  # TODO: import specific classes
# from handling.channel.handler.GuildHandler import *  # TODO: import specific classes
# from handling.channel.handler.HiredMerchantHandler import *  # TODO: import specific classes
# from handling.channel.handler.InterServerHandler import *  # TODO: import specific classes
# from handling.channel.handler.InventoryHandler import *  # TODO: import specific classes
# from handling.channel.handler.ItemMakerHandler import *  # TODO: import specific classes
# from handling.channel.handler.MobHandler import *  # TODO: import specific classes
# from handling.channel.handler.MonsterCarnivalHandler import *  # TODO: import specific classes
# from handling.channel.handler.NPCHandler import *  # TODO: import specific classes
# from handling.channel.handler.PartyHandler import *  # TODO: import specific classes
# from handling.channel.handler.PetHandler import *  # TODO: import specific classes
# from handling.channel.handler.PlayerHandler import *  # TODO: import specific classes
# from handling.channel.handler.PlayerInteractionHandler import *  # TODO: import specific classes
# from handling.channel.handler.PlayersHandler import *  # TODO: import specific classes
# from handling.channel.handler.StatsHandling import *  # TODO: import specific classes
# from handling.channel.handler.SummonHandler import *  # TODO: import specific classes
# from handling.channel.handler.UserInterfaceHandler import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.login.handler.CharLoginHandler import *  # TODO: import specific classes
# from handling.login.handler.PacketErrorHandler import *  # TODO: import specific classes
# from handling.mina.MaplePacketDecoder import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.MTSStorage import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.MapleAESOFB import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.ByteArrayByteStream import *  # TODO: import specific classes
# from tools.data.input.GenericSeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.LoginPacket import *  # TODO: import specific classes


class MapleServerHandler(IoHandlerAdapter, MapleServerHandlerMBean):
    """
    Class MapleServerHandler
    Extends: IoHandlerAdapter
    Implements: MapleServerHandlerMBean
    """

    def __init__(self):
        self.channel = 0
        self.cs = False
        self.BlockedIP = []
        self.tracker = {}
        self.ip = ""
        self.accName = ""
        self.accId = ""
        self.chrName = ""
        self.packet = None
        self.timestamp = 0
        self.op = None
        self.channel = -1
        self.BlockedIP = []
        self.tracker = new ConcurrentHashMap<String, Pair<Long, Byte>>()

    # Static initializer
    # MapleServerHandler.Log_Packets = True
    # MapleServerHandler.nl = os.environ.get("line.separator")
    # MapleServerHandler.loggedIPs = File("logs/LogIPs.txt")
    # MapleServerHandler.logIPMap = {}
    # MapleServerHandler.debugMode = bool(ServerProperties.getProperty("RoyMS.Debug", "False"))
    # MapleServerHandler.blocked = EnumSet.noneOf(RecvPacketOpcode.class)
    # MapleServerHandler.Log_Size = 10000
    # MapleServerHandler.Packet_Log = []
    # MapleServerHandler.Packet_Log_Lock = ReentrantReadWriteLock()
    # MapleServerHandler.Packet_Log_Output = File("logs/PacketLog.txt")
    # reloadLoggedIPs()
    # block = { RecvPacketOpcode.NPC_ACTION, RecvPacketOpcode.MOVE_PLAYER, RecvPacketOpcode.MOVE_PET, RecvPacketOpcode.MOVE_SUMMON, RecvPacketOpcode.MOVE_LIFE, RecvPacketOpcode.HEAL_OVER_TIME, RecvPacketOpcode.STRANGE_DATA }
    # MapleServerHandler.blocked.addAll(Arrays.asList(block))


    def reloadLoggedIPs(self) -> None:
        for fw in MapleServerHandler.logIPMap.values():
            if fw is not None:
                try:
                    fw.write("=== Closing Log ===")
                    fw.write(MapleServerHandler.nl)
                    fw.flush()
                    fw.close()
                except IOError as ex:
                    print("Error closing Packet Log.")
                    print(ex)
        MapleServerHandler.logIPMap.clear()
        try:
            sc = Scanner(MapleServerHandler.loggedIPs)
            while sc.hasNextLine():
                line = sc.nextLine().strip()
                if line > 0:
                    fw2 = FileWriter(File("PacketLog_" + line + ".txt"), True)
                    fw2.write("=== Creating Log ===")
                    fw2.write(MapleServerHandler.nl)
                    fw2.flush()
                    MapleServerHandler.logIPMap.put(line, fw2)
        except IOError as e:
            print("无法加载登录IP数据包。")
            print(e)

    def isLoggedIP(self, sess: Any) -> Any:
        a = sess.getRemoteAddress()
        realIP = a[a.find(47:] + 1, a.find(58))
        return MapleServerHandler.logIPMap.get(realIP)

    def log(self, packet: Any, op: Any, c: Any, io: Any) -> None:
        if (op in MapleServerHandler.blocked):
            return
        try:
            MapleServerHandler.Packet_Log_Lock.writeLock().lock()
            logged = None
            if MapleServerHandler.Packet_Log == MapleServerHandler.Log_Size:
                logged = MapleServerHandler.Packet_Log.remove(0)
            if logged is None:
                logged = LoggedPacket(packet, op, io.getRemoteAddress(), (c is None) ? -1 : c.getAccID(), (c is None || c.getAccountName() is None) ? "[Null]" : c.getAccountName(), (c is None || c.getPlayer() is None || c.getPlayer().getName() is None) ? "[Null]" : c.getPlayer().getName())
            else:
                logged.setInfo(packet, op, io.getRemoteAddress(), (c is None) ? -1 : c.getAccID(), (c is None || c.getAccountName() is None) ? "[Null]" : c.getAccountName(), (c is None || c.getPlayer() is None || c.getPlayer().getName() is None) ? "[Null]" : c.getPlayer().getName())
            MapleServerHandler.Packet_Log.add(logged)
        finally:
            MapleServerHandler.Packet_Log_Lock.writeLock().unlock()

    def registerMBean(self) -> None:
        mBeanServer = ManagementFactory.getPlatformMBeanServer()
        try:
            mbean = MapleServerHandler()
            mBeanServer.registerMBean(mbean, ObjectName("handling:type=MapleServerHandler"))
        catch (InstanceAlreadyExistsException | MBeanRegistrationException | MalformedObjectNameException | NotCompliantMBeanException e)
            print("Error registering PacketLog MBean")
            e.printStackTrace()

    def writeLog(self) -> None:
        try:
            fw = FileWriter(MapleServerHandler.Packet_Log_Output, True)
            try:
                MapleServerHandler.Packet_Log_Lock.readLock().lock()
                nl = os.environ.get("line.separator")
                for loggedPacket in MapleServerHandler.Packet_Log:
                    fw.write(loggedPacket)
                    fw.write(nl)
                fw.flush()
                fw.close()
            finally:
                MapleServerHandler.Packet_Log_Lock.readLock().unlock()
        except IOError as ex:
            print("Error writing log to file.")

    def messageSent(self, session: Any, message: Any) -> None:
        r = (message).getOnSend()
        if r is not None:
            r.run()
        super.messageSent(session, message)

    def exceptionCaught(self, session: Any, cause: Any) -> None:
        pass

    def sessionOpened(self, session: Any) -> None:
        address = session.getRemoteAddress().split(":")[0]
        track = self.tracker.get(address)
        count = None
        if track is None:
            count = 1
        else:
            count = track.right
            difference = int(time.time() * 1000) - track.left
            if difference < 2000:
                count += 1
            elif difference > 20000:
                count = 1
            if count >= 10:
                print("自动断开连接A2")
                self.BlockedIP.add(address)
                self.tracker.remove(address)
                session.close(True)
                return
        self.tracker.put(address, new Pair<Long, Byte>(int(time.time() * 1000), count))
        if self.channel > -1:
            if ChannelServer.getInstance(self.channel).isShutdown():
                print("频道服务器尚未开启,发现连接进入，该连接被断开")
                session.close(True)
                return
        elif self.cs:
            if CashShopServer.isShutdown():
                print("商城服务器尚未开启,发现连接进入，该连接被断开")
                session.close(True)
                return
        elif LoginServer.isShutdown():
            print("登录服务器尚未开启,发现连接进入，该连接被断开")
            session.close(True)
            return
        serverRecv = { 70, 114, 122, Randomizer.nextInt(255) }
        serverSend = { 82, 48, 120, Randomizer.nextInt(255) }
        ivRecv = ServerConstants.Use_Fixed_IV ? new byte[] { 9, 0, 5, 95 } : serverRecv
        ivSend = ServerConstants.Use_Fixed_IV ? new byte[] { 1, 95, 4, 63 } : serverSend
        client = MapleClient(MapleAESOFB(ivSend, (short)(65535 - ServerConstants.MAPLE_VERSION)), MapleAESOFB(ivRecv, ServerConstants.MAPLE_VERSION), session)
        client.setChannel(self.channel)
        final MaplePacketDecoder.DecoderState decoderState = new MaplePacketDecoder.DecoderState()
        session.setAttribute(MaplePacketDecoder.DECODER_STATE_KEY, decoderState)
        session.write(LoginPacket.getHello(ServerConstants.MAPLE_VERSION, ServerConstants.Use_Fixed_IV ? serverSend : ivSend, ServerConstants.Use_Fixed_IV ? serverRecv : ivRecv))
        session.setAttribute(MapleClient.CLIENT_KEY, client)
        session.setAttribute(IdleStatus.READER_IDLE, 60)
        session.setAttribute(IdleStatus.WRITER_IDLE, 60)
        sb = ""
        if self.channel > -1:
            sb.append("[频道服务器] 频道 ").append(self.channel).append(" : ")
        elif self.cs:
            sb.append("[商城服务器]")
        else:
            sb.append("[登录服务器]")
        sb.append("IoSession opened ").append(address)
        print(sb)
        World.Client.addClient(client)
        fw = isLoggedIP(session)
        if fw is not None:
            if self.channel > -1:
                fw.write("=== Logged Into Channel " + self.channel + " ===")
                fw.write(MapleServerHandler.nl)
            elif self.cs:
                fw.write("=== Logged Into CashShop Server ===")
                fw.write(MapleServerHandler.nl)
            else:
                fw.write("=== Logged Into Login Server ===")
                fw.write(MapleServerHandler.nl)
            fw.flush()

    def sessionClosed(self, session: Any) -> None:
        client = session.getAttribute(MapleClient.CLIENT_KEY)
        if client is not None:
            try:
                fw = isLoggedIP(session)
                if fw is not None:
                    fw.write("=== Session Closed ===")
                    fw.write(MapleServerHandler.nl)
                    fw.flush()
                client.disconnect(True, self.cs)
            finally:
                World.Client.removeClient(client)
                session.close(True)
                session.removeAttribute(MapleClient.CLIENT_KEY)
        super.sessionClosed(session)

    def messageReceived(self, session: Any, message: Any) -> None:
        try:
            slea = GenericSeekableLittleEndianAccessor(ByteArrayByteStream((byte[])message))
            if slea.available() < 2:
                return
            header_num = slea.readShort()
            values = RecvPacketOpcode.values()
            length = len(values)
            i = 0
            while i < length:
                recv = values[i]
                if recv.getValue() == header_num:
                    if MapleServerHandler.debugMode && !RecvPacketOpcode.isSpamHeader(recv):
                        sb = "" + "\n")
                        sb.append(HexTool.toString((byte[])message)).append("\n").append(HexTool.toStringFromAscii((byte[])message))
                        print(sb)
                    c = session.getAttribute(MapleClient.CLIENT_KEY)
                    if !c.isReceiving():
                        return
                    if recv.NeedsChecking() && !c.isLoggedIn():
                        return
                    if (c.getPlayer() is None || !c.isMonitored() || !(recv in MapleServerHandler.blocked)) {}
                    if MapleServerHandler.Log_Packets:
                        log(slea, recv, c, session)
                    handlePacket(recv, slea, c, self.cs)
                    fw = isLoggedIP(session)
                    if fw is not None && !(recv in MapleServerHandler.blocked):
                        if recv == RecvPacketOpcode.PLAYER_LOGGEDIN && c is not None:
                            fw.write(">> [AccountName: " + ((c.getAccountName() is None) ? "None" : c.getAccountName()) + "] | [IGN: " + ((c.getPlayer() is None || c.getPlayer().getName() is None) ? "None" : c.getPlayer().getName()) + "] | [Time: " + FileoutputUtil.CurrentReadable_Time() + "]")
                            fw.write(MapleServerHandler.nl)
                        fw.write("[" + recv + "]" + slea.toString(True))
                        fw.write(MapleServerHandler.nl)
                        fw.flush()
                    return
                else:
                    i += 1
            if MapleServerHandler.debugMode:
                sb2 = ""
                sb2.append(HexTool.toString((byte[])message)).append("\n").append(HexTool.toStringFromAscii((byte[])message))
                print(sb2)
        except RejectedExecutionException as ex:
            ex.printStackTrace()
        except Exception as e:
            FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e)
            e.printStackTrace()

    def sessionIdle(self, session: Any, status: Any) -> None:
        client = session.getAttribute(MapleClient.CLIENT_KEY)
        if client is not None:
            client.sendPing()
            super.sessionIdle(session, status)
            return
        session.close(True)

    def isSpamHeader(self, header: Any) -> bool:
        # switch (header):
            # case PONG:
            # case NPC_ACTION:
            # case MOVE_SUMMON:
            # case MOVE_LIFE:
            # case MOVE_PLAYER:
            # case MOVE_PET:
            # case SPECIAL_MOVE:
            # case QUEST_ACTION:
            # case HEAL_OVER_TIME:
            # case STRANGE_DATA:
            # case CHANGE_KEYMAP:
            # case USE_INNER_PORTAL:
                return True
            # default:
                return False

    def handlePacket(self, header: Any, slea: Any, c: Any, cs: bool) -> None:
        # switch (header):
            # case PONG:
                c.pongReceived()
            # case PACKET_ERROR:
                PacketErrorHandler.handlePacket(slea, c)
            # case LOGIN_PASSWORD:
                CharLoginHandler.login(slea, c)
                break
            # case SERVERLIST_REQUEST:
                CharLoginHandler.ServerListRequest(c)
                break
            # case LICENSE_REQUEST:
                CharLoginHandler.ServerListRequest(c)
                break
            # case CHARLIST_REQUEST:
                CharLoginHandler.CharlistRequest(slea, c)
                break
            # case SERVERSTATUS_REQUEST:
                CharLoginHandler.ServerStatusRequest(c)
                break
            # case CHECK_CHAR_NAME:
                CharLoginHandler.CheckCharName(slea.readMapleAsciiString(), c)
                break
            # case CREATE_CHAR:
                CharLoginHandler.CreateChar(slea, c)
                break
            # case CHAR_SELECT:
                CharLoginHandler.Character_WithoutSecondPassword(slea, c)
                break
            # case SET_GENDER:
                CharLoginHandler.SetGenderRequest(slea, c)
                break
            # case RSA_KEY:
                c.getSession().write(LoginPacket.StrangeDATA())
                break
            # case CHANGE_CHANNEL:
                InterServerHandler.ChangeChannel(slea, c, c.getPlayer())
                break
            # case PLAYER_LOGGEDIN:
                playerid = slea.readInt()
                if cs:
                    CashShopOperation.EnterCS(playerid, c)
                    break
                InterServerHandler.Loggedin(playerid, c)
                break
            # case ENTER_CASH_SHOP:
                slea.readInt()
                InterServerHandler.EnterCS(c, c.getPlayer())
                break
            # case ENTER_MTS:
                InterServerHandler.EnterMTS(c, c.getPlayer())
                break
            # case PLAYER_UPDATE:
                PlayerHandler.UpdateHandler(slea, c, c.getPlayer())
                break
            # case MOVE_PLAYER:
                PlayerHandler.MovePlayer(slea, c, c.getPlayer())
                break
            # case CHAR_INFO_REQUEST:
                c.getPlayer().updateTick(slea.readInt())
                PlayerHandler.CharInfoRequest(slea.readInt(), c, c.getPlayer())
                break
            # case CLOSE_RANGE_ATTACK:
                PlayerHandler.closeRangeAttack(slea, c, c.getPlayer(), False)
                break
            # case RANGED_ATTACK:
                PlayerHandler.rangedAttack(slea, c, c.getPlayer())
                break
            # case MAGIC_ATTACK:
                PlayerHandler.MagicDamage(slea, c, c.getPlayer())
                break
            # case SPECIAL_MOVE:
                PlayerHandler.SpecialMove(slea, c, c.getPlayer())
                break
            # case PASSIVE_ENERGY:
                PlayerHandler.closeRangeAttack(slea, c, c.getPlayer(), True)
                break
            # case FACE_EXPRESSION:
                PlayerHandler.ChangeEmotion(slea.readInt(), c.getPlayer())
                break
            # case TAKE_DAMAGE:
                PlayerHandler.TakeDamage(slea, c, c.getPlayer())
                break
            # case HEAL_OVER_TIME:
                PlayerHandler.Heal(slea, c.getPlayer())
                break
            # case CANCEL_BUFF:
                PlayerHandler.CancelBuffHandler(slea.readInt(), c.getPlayer())
                break
            # case CANCEL_ITEM_EFFECT:
                PlayerHandler.CancelItemEffect(slea.readInt(), c.getPlayer())
                break
            # case USE_CHAIR:
                PlayerHandler.UseChair(slea.readInt(), c, c.getPlayer())
                break
            # case CANCEL_CHAIR:
                PlayerHandler.CancelChair(slea.readShort(), c, c.getPlayer())
                break
            # case USE_ITEMEFFECT:
                PlayerHandler.UseItemEffect(slea.readInt(), c, c.getPlayer())
                break
            # case SKILL_EFFECT:
                PlayerHandler.SkillEffect(slea, c.getPlayer())
                break
            # case MESO_DROP:
                c.getPlayer().updateTick(slea.readInt())
                PlayerHandler.DropMeso(slea.readInt(), c.getPlayer())
                break
            # case MONSTER_BOOK_COVER:
                PlayerHandler.ChangeMonsterBookCover(slea.readInt(), c, c.getPlayer())
                break
            # case CHANGE_KEYMAP:
                PlayerHandler.ChangeKeymap(slea, c.getPlayer())
                break
            # case CHANGE_MAP:
                if cs:
                    if ServerConstants.调试输出封包:
                        print("退出商城")
                    CashShopOperation.LeaveCS(slea, c, c.getPlayer())
                    break
                PlayerHandler.ChangeMap(slea, c, c.getPlayer())
                break
            # case CHANGE_MAP_SPECIAL:
                PlayerHandler.ChangeMapSpecial(slea, c, c.getPlayer())
                break
            # case USE_INNER_PORTAL:
                slea.skip(1)
                PlayerHandler.InnerPortal(slea, c, c.getPlayer())
                break
            # case TROCK_ADD_MAP:
                PlayerHandler.TrockAddMap(slea, c, c.getPlayer())
                break
            # case LIE_DETECTOR:
                PlayersHandler.LieDetector(slea, c, c.getPlayer(), False)
                break
            # case LIE_DETECTOR_RESPONSE:
                PlayersHandler.LieDetectorResponse(slea, c)
                break
            # case LIE_DETECTOR_REFRESH:
                PlayersHandler.LieDetectorRefresh(slea, c)
                break
            # case ARAN_COMBO:
                PlayerHandler.AranCombo(c, c.getPlayer())
                break
            # case SKILL_MACRO:
                PlayerHandler.ChangeSkillMacro(slea, c.getPlayer())
                break
            # case ITEM_BAOWU:
                InventoryHandler.UsePenguinBox(slea, c)
                break
            # case ITEM_SUNZI:
                InventoryHandler.SunziBF(slea, c)
                break
            # case GIVE_FAME:
                PlayersHandler.GiveFame(slea, c, c.getPlayer())
                break
            # case TRANSFORM_PLAYER:
                PlayersHandler.TransformPlayer(slea, c, c.getPlayer())
                break
            # case NOTE_ACTION:
                PlayersHandler.Note(slea, c.getPlayer())
                break
            # case USE_DOOR:
                PlayersHandler.UseDoor(slea, c.getPlayer())
                break
            # case DAMAGE_REACTOR:
                PlayersHandler.HitReactor(slea, c)
                break
            # case TOUCH_REACTOR:
                PlayersHandler.TouchReactor(slea, c)
                break
            # case CLOSE_CHALKBOARD:
                c.getPlayer().setChalkboard(None)
                break
            # case ITEM_MAKER:
                ItemMakerHandler.ItemMaker(slea, c)
                break
            # case ITEM_SORT:
                InventoryHandler.ItemSort(slea, c)
                break
            # case ITEM_GATHER:
                InventoryHandler.ItemGather(slea, c)
                break
            # case ITEM_MOVE:
                InventoryHandler.ItemMove(slea, c)
                break
            # case ITEM_PICKUP:
                InventoryHandler.Pickup_Player(slea, c, c.getPlayer())
                break
            # case USE_CASH_ITEM:
                InventoryHandler.UseCashItem(slea, c)
                break
            # case QUEST_KJ:
                InventoryHandler.QuestKJ(slea, c, c.getPlayer())
                break
            # case USE_ITEM:
                InventoryHandler.UseItem(slea, c, c.getPlayer())
                break
            # case USE_RETURN_SCROLL:
                InventoryHandler.UseReturnScroll(slea, c, c.getPlayer())
                break
            # case USE_UPGRADE_SCROLL:
                c.getPlayer().updateTick(slea.readInt())
                InventoryHandler.UseUpgradeScroll(slea.readShort(), slea.readShort(), slea.readShort(), c, c.getPlayer())
                break
            # case USE_SUMMON_BAG:
                InventoryHandler.UseSummonBag(slea, c, c.getPlayer())
                break
            # case ITEM_MZD:
                InventoryHandler.UseTreasureChest(slea, c, c.getPlayer())
                break
            # case USE_SKILL_BOOK:
                InventoryHandler.UseSkillBook(slea, c, c.getPlayer())
                break
            # case USE_CATCH_ITEM:
                InventoryHandler.UseCatchItem(slea, c, c.getPlayer())
                break
            # case USE_MOUNT_FOOD:
                InventoryHandler.UseMountFood(slea, c, c.getPlayer())
                break
            # case MOVE_LIFE:
                MobHandler.MoveMonster(slea, c, c.getPlayer())
                break
            # case AUTO_AGGRO:
                MobHandler.AutoAggro(slea.readInt(), c.getPlayer())
                break
            # case FRIENDLY_DAMAGE:
                MobHandler.FriendlyDamage(slea, c.getPlayer())
                break
            # case MONSTER_BOMB:
                MobHandler.MonsterBomb(slea.readInt(), c.getPlayer())
                break
            # case NPC_SHOP:
                NPCHandler.NPCShop(slea, c, c.getPlayer())
                break
            # case NPC_TALK:
                NPCHandler.NPCTalk(slea, c, c.getPlayer())
                break
            # case NPC_TALK_MORE:
                NPCHandler.NPCMoreTalk(slea, c)
                break
            # case NPC_ACTION:
                NPCHandler.NPCAnimation(slea, c)
                break
            # case QUEST_ACTION:
                NPCHandler.QuestAction(slea, c, c.getPlayer())
                break
            # case STORAGE:
                NPCHandler.Storage(slea, c, c.getPlayer())
                break
            # case GENERAL_CHAT:
                ChatHandler.GeneralChat(slea.readMapleAsciiString(), slea.readByte(), c, c.getPlayer())
                break
            # case PARTYCHAT:
                ChatHandler.Others(slea, c, c.getPlayer())
                break
            # case WHISPER:
                ChatHandler.Whisper_Find(slea, c)
                break
            # case MESSENGER:
                ChatHandler.Messenger(slea, c)
                break
            # case AUTO_ASSIGN_AP:
                StatsHandling.AutoAssignAP(slea, c, c.getPlayer())
                break
            # case DISTRIBUTE_AP:
                StatsHandling.DistributeAP(slea, c, c.getPlayer())
                break
            # case DISTRIBUTE_SP:
                c.getPlayer().updateTick(slea.readInt())
                StatsHandling.DistributeSP(slea.readInt(), c, c.getPlayer())
                break
            # case PLAYER_INTERACTION:
                PlayerInteractionHandler.PlayerInteraction(slea, c, c.getPlayer())
                break
            # case GUILD_OPERATION:
                GuildHandler.Guild(slea, c)
                break
            # case DENY_GUILD_REQUEST:
                slea.skip(1)
                GuildHandler.DenyGuildRequest(slea.readMapleAsciiString(), c)
                break
            # case ALLIANCE_OPERATION:
                AllianceHandler.HandleAlliance(slea, c, False)
                break
            # case DENY_ALLIANCE_REQUEST:
                AllianceHandler.HandleAlliance(slea, c, True)
                break
            # case BBS_OPERATION:
                BBSHandler.BBSOperatopn(slea, c)
                break
            # case PARTY_OPERATION:
                PartyHandler.PartyOperatopn(slea, c)
                break
            # case DENY_PARTY_REQUEST:
                PartyHandler.DenyPartyRequest(slea, c)
                break
            # case BUDDYLIST_MODIFY:
                BuddyListHandler.BuddyOperation(slea, c)
                break
            # case CYGNUS_SUMMON:
                UserInterfaceHandler.CygnusSummon_NPCRequest(c)
                break
            # case SHIP_OBJECT:
                UserInterfaceHandler.ShipObjectRequest(slea.readInt(), c)
                break
            # case BUY_CS_ITEM:
                CashShopOperation.BuyCashItem(slea, c, c.getPlayer())
                break
            # case TOUCHING_CS:
                CashShopOperation.TouchingCashShop(c)
                break
            # case COUPON_CODE:
                FileoutputUtil.log(FileoutputUtil.PacketEx_Log, "Coupon : \n" + slea.toString(True))
                print(slea)
                slea.skip(2)
                CashShopOperation.CouponCode(slea.readMapleAsciiString(), c)
                break
            # case CS_UPDATE:
                CashShopOperation.CSUpdate(c)
                break
            # case TOUCHING_MTS:
                MTSOperation.MTSUpdate(MTSStorage.getInstance().getCart(c.getPlayer().getId()), c)
                break
            # case MTS_TAB:
                MTSOperation.MTSOperation(slea, c)
                break
            # case DAMAGE_SUMMON:
                SummonHandler.DamageSummon(slea, c.getPlayer())
                break
            # case MOVE_SUMMON:
                SummonHandler.MoveSummon(slea, c.getPlayer())
                break
            # case SUMMON_ATTACK:
                SummonHandler.SummonAttack(slea, c, c.getPlayer())
                break
            # case PET_EXCEPTIONLIST:
                PetHandler.PickExceptionList(slea, c, c.getPlayer())
                break
            # case SPAWN_PET:
                PetHandler.SpawnPet(slea, c, c.getPlayer())
                break
            # case MOVE_PET:
                PetHandler.MovePet(slea, c.getPlayer())
                break
            # case PET_CHAT:
                if slea.available() < 12:
                    break
                PetHandler.PetChat(slea.readLong(), slea.readShort(), slea.readMapleAsciiString(), c.getPlayer())
                break
            # case PET_COMMAND:
                PetHandler.PetCommand(slea, c, c.getPlayer())
                break
            # case PET_FOOD:
                PetHandler.PetFood(slea, c, c.getPlayer())
                break
            # case PET_LOOT:
                InventoryHandler.Pickup_Pet(slea, c, c.getPlayer())
                break
            # case PET_AUTO_POT:
                PetHandler.Pet_AutoPotion(slea, c, c.getPlayer())
                break
            # case MONSTER_CARNIVAL:
                MonsterCarnivalHandler.MonsterCarnival(slea, c)
                break
            # case DUEY_ACTION:
                DueyHandler.DueyOperation(slea, c)
                break
            # case USE_HIRED_MERCHANT:
                HiredMerchantHandler.UseHiredMerchant(slea, c)
                break
            # case MERCH_ITEM_STORE:
                HiredMerchantHandler.MerchantItemStore(slea, c)
            # case LEFT_KNOCK_BACK:
                PlayerHandler.leftKnockBack(slea, c)
                break
            # case SNOWBALL:
                PlayerHandler.snowBall(slea, c)
                break
            # case ChatRoom_SYSTEM:
                PlayersHandler.ChatRoomHandler(slea, c)
                break
            # case COCONUT:
                PlayersHandler.hitCoconut(slea, c)
                break
            # case OWL:
                InventoryHandler.Owl(slea, c)
                break
            # case OWL_WARP:
                InventoryHandler.OwlWarp(slea, c)
                break
            # case USE_OWL_MINERVA:
                InventoryHandler.OwlMinerva(slea, c)
                break
            # case RPS_GAME:
                NPCHandler.RPSGame(slea, c)
                break
            # case UPDATE_QUEST:
                NPCHandler.UpdateQuest(slea, c)
                break
            # case RING_ACTION:
                PlayersHandler.RingAction(slea, c)
                break
            # case REQUEST_FAMILY:
                FamilyHandler.RequestFamily(slea, c)
                break
            # case OPEN_FAMILY:
                FamilyHandler.OpenFamily(slea, c)
                break
            # case FAMILY_OPERATION:
                FamilyHandler.FamilyOperation(slea, c)
                break
            # case DELETE_JUNIOR:
                FamilyHandler.DeleteJunior(slea, c)
                break
            # case DELETE_SENIOR:
                FamilyHandler.DeleteSenior(slea, c)
                break
            # case USE_FAMILY:
                FamilyHandler.UseFamily(slea, c)
                break
            # case FAMILY_PRECEPT:
                FamilyHandler.FamilyPrecept(slea, c)
                break
            # case FAMILY_SUMMON:
                FamilyHandler.FamilySummon(slea, c)
                break
            # case ACCEPT_FAMILY:
                FamilyHandler.AcceptFamily(slea, c)
                break
            # case BEANS_GAME1:
                BeanGame.BeanGame1(slea, c)
                break
            # case BEANS_GAME2:
                BeanGame.BeanGame2(slea, c)
                break
            # case MOONRABBIT_HP:
                PlayerHandler.Rabbit(slea, c)
                break

    def setInfo(self, p: Any, op: Any, ip: str, id: int, accName: str, chrName: str) -> None:
        self.ip = ip
        self.op = op
        self.packet = p
        self.accName = accName
        self.chrName = chrName
        self.timestamp = int(time.time() * 1000)

    def toString(self) -> str:
        sb = ""
        sb.append("[IP: ").append(self.ip).append("] [").append(self.accId).append('|').append(self.accName).append('|').append(self.chrName).append("] [Time: ").append(self.timestamp).append(']')
        sb.append(LoggedPacket.nl)
        sb.append("[Op: ").append(self.op).append(']')
        sb.append(" [Data: ").append(self.packet).append(']')
        return sb


# Inner class from Java (originally nested)
class LoggedPacket:
    """
    Class LoggedPacket
    """

    def __init__(self, p: Any, op: Any, ip: str, id: int, accName: str, chrName: str):
        self.ip = ""
        self.accName = ""
        self.accId = ""
        self.chrName = ""
        self.packet = None
        self.timestamp = 0
        self.op = None
        self.setInfo(p, op, ip, id, accName, chrName)

    # Static initializer
    # nl = os.environ.get("line.separator")


    def setInfo(self, p: Any, op: Any, ip: str, id: int, accName: str, chrName: str) -> None:
        self.ip = ip
        self.op = op
        self.packet = p
        self.accName = accName
        self.chrName = chrName
        self.timestamp = int(time.time() * 1000)

    def toString(self) -> str:
        sb = ""
        sb.append("[IP: ").append(self.ip).append("] [").append(self.accId).append('|').append(self.accName).append('|').append(self.chrName).append("] [Time: ").append(self.timestamp).append(']')
        sb.append(LoggedPacket.nl)
        sb.append("[Op: ").append(self.op).append(']')
        sb.append(" [Data: ").append(self.packet).append(']')
        return sb

