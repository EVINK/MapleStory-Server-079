"""
NPCScriptManager - Converted from Java source
Original: scripting/NPCScriptManager.java
Package: scripting
"""

from pathlib import Path
from threading import Lock
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import sys
import threading
import tkinter

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class NPCScriptManager(AbstractScriptManager):
    """
    Class NPCScriptManager
    Extends: AbstractScriptManager
    """

    npcScriptManager = NPCScriptManager()

    def __init__(self):
        self.mapleClientNPCConversationManagerMap = new WeakHashMap<>()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start(self, c: Any, npc: int) -> None:
        self.start(c, npc, 0)

    def start_c_npc_wh(self, c: Any, npc: int, wh: int) -> None:
        lock = c.getNPCLock()
        lock.lock()
        try:
            if c.getPlayer().isGM():
                if wh == 0:
                    c.getPlayer().dropMessage("[系统提示]您已经建立与NPC:" + npc + "的对话。")
                else:
                    c.getPlayer().dropMessage("[系统提示]您已经建立与NPC:" + npc + "_" + wh + "的对话。")
            if not (c in self.mapleClientNPCConversationManagerMap):
                iv = None
                if wh == 0:
                    iv = self.getInvocable("npc"+ File.separator + npc + ".js", c, True)
                else:
                    iv = self.getInvocable("npc"+File.separator + npc + "_" + wh + ".js", c, True)
                scriptengine = iv
                cm = None
                if wh == 0:
                    cm = NPCConversationManager(c, npc, -1, (byte) (-1), iv, 0)
                else:
                    cm = NPCConversationManager(c, npc, -1, (byte) (-1), iv, wh)
                self.mapleClientNPCConversationManagerMap.put(c, cm)
                if iv is None or getInstance() is None:
                    if wh == 0:
                        # switch (GameConstants.game):
                            # case 0:
                                cm.sendOk("欢迎来到#b冒险岛#k。你找我有什么事吗？\r\n我的ID是: #r" + npc + "#k.\r\n 有问题联系#bGM#k")
                                break
                            # default:
                                cm.sendOk("欢迎来到#b冒险岛#k。你找我有什么事吗？\r\n我的ID是: #r" + npc + "#k.\r\n 有问题联系#bGM#k")
                                break
                    else:
                        cm.sendOk("欢迎来到#b冒险岛#k。你找我有什么事吗？\r\n我的ID是: #r" + npc + "#k.\r\n 有问题联系#bGM#k")
                    cm.dispose()
                    return
                scriptengine.put("cm", cm)
                scriptengine.put("npcid", npc)
                c.getPlayer().setConversation(1)
                try:
                    iv.invokeFunction("start")
                except NoSuchMethodException as nsme:
                    iv.invokeFunction("action", 1, 0, 0)
            else:
                getInstance().dispose(c)
                c.getSession().write(MaplePacketCreator.enableActions())
        except Exception as e:
            print("NPC 腳本錯誤, 它ID為 : " + npc + "_" + wh + "." + e)
            if c.getPlayer().isGM():
                c.getPlayer().dropMessage("[系統提示] NPC " + npc + "_" + wh + "腳本錯誤 " + e + "")
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing NPC script, NPC ID : " + npc + "_" + wh + "." + e)
            self.dispose(c)
        finally:
            lock.unlock()

    def action(self, c: Any, mode: int, type: int, selection: int) -> None:
        self.action(c, mode, type, selection, 0)

    def action_c_mode_type_selection_wh(self, c: Any, mode: int, type: int, selection: int, wh: int) -> None:
        if mode != -1:
            cm = self.mapleClientNPCConversationManagerMap.get(c)
            if cm is None or cm.getLastMsg() > -1:
                return
            lock = c.getNPCLock()
            lock.lock()
            try:
                if cm.pendingDisposal:
                    self.dispose(c)
                elif wh == 0:
                    cm.getIv().invokeFunction("action", mode, type, selection)
                else:
                    cm.getIv().invokeFunction("action", mode, type, selection, wh)
            except Exception as e:
                if c.getPlayer().isGM():
                    c.getPlayer().dropMessage("[系統提示] NPC " + cm.getNpc() + "_" + wh + "腳本錯誤 " + e + "")
                print("NPC 腳本錯誤. 它ID為 : " + cm.getNpc() + "_" + wh + ":" + e)
                self.dispose(c)
                FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing NPC script, NPC ID : " + cm.getNpc() + "_" + wh + "." + e)
            finally:
                lock.unlock()

    def startQuest(self, c: Any, npc: int, quest: int) -> None:
        if not MapleQuest.getInstance(quest).canStart(c.getPlayer(), None):
            return
        lock = c.getNPCLock()
        lock.lock()
        try:
            if not (c in self.mapleClientNPCConversationManagerMap):
                iv = self.getInvocable("quest"+File.separator + quest + ".js", c, True)
                if iv is None:
                    self.dispose(c)
                    return
                scriptengine = iv
                cm = NPCConversationManager(c, npc, quest, 0, iv, 0)
                self.mapleClientNPCConversationManagerMap.put(c, cm)
                scriptengine.put("qm", cm)
                c.getPlayer().setConversation(1)
                if c.getPlayer().isGM():
                    c.getPlayer().dropMessage("[系統提示]您已經建立與任務腳本:" + quest + "的往來。")
                iv.invokeFunction("start", 1, 0, 0)
            else:
                self.dispose(c)
        except Exception as e:
            print("Error executing Quest script. (" + quest + ")..NPCID: " + npc + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing Quest script. (" + quest + ")..NPCID: " + npc + ":" + e)
            self.dispose(c)
        finally:
            lock.unlock()

    def startQuest_c_mode_type_selection(self, c: Any, mode: int, type: int, selection: int) -> None:
        lock = c.getNPCLock()
        cm = self.mapleClientNPCConversationManagerMap.get(c)
        if cm is None or cm.getLastMsg() > -1:
            return
        lock.lock()
        try:
            if cm.pendingDisposal:
                self.dispose(c)
            else:
                cm.getIv().invokeFunction("start", mode, type, selection)
        except Exception as e:
            if c.getPlayer().isGM():
                c.getPlayer().dropMessage("[系統提示]任務腳本:" + cm.getQuest() + "錯誤...NPC: " + cm.getNpc() + ":" + e)
            print("Error executing Quest script. (" + cm.getQuest() + ")...NPC: " + cm.getNpc() + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing Quest script. (" + cm.getQuest() + ")..NPCID: " + cm.getNpc() + ":" + e)
            self.dispose(c)
        finally:
            lock.unlock()

    def endQuest(self, c: Any, npc: int, quest: int, customEnd: bool) -> None:
        if not customEnd and not MapleQuest.getInstance(quest).canComplete(c.getPlayer(), None):
            return
        lock = c.getNPCLock()
        lock.lock()
        try:
            if not (c in self.mapleClientNPCConversationManagerMap):
                iv = self.getInvocable("quest"+File.separator + quest + ".js", c, True)
                if iv is None:
                    self.dispose(c)
                    return
                scriptengine = iv
                cm = NPCConversationManager(c, npc, quest, 1, iv, 0)
                self.mapleClientNPCConversationManagerMap.put(c, cm)
                scriptengine.put("qm", cm)
                c.getPlayer().setConversation(1)
                iv.invokeFunction("end", 1, 0, 0)
        except Exception as e:
            if c.getPlayer().isGM():
                c.getPlayer().dropMessage("[系統提示]任務腳本:" + quest + "錯誤...NPC: " + quest + ":" + e)
            print("Error executing Quest script. (" + quest + ")..NPCID: " + npc + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing Quest script. (" + quest + ")..NPCID: " + npc + ":" + e)
            self.dispose(c)
        finally:
            lock.unlock()

    def endQuest_c_mode_type_selection(self, c: Any, mode: int, type: int, selection: int) -> None:
        lock = c.getNPCLock()
        cm = self.mapleClientNPCConversationManagerMap.get(c)
        if cm is None or cm.getLastMsg() > -1:
            return
        lock.lock()
        try:
            if cm.pendingDisposal:
                self.dispose(c)
            else:
                cm.getIv().invokeFunction("end", mode, type, selection)
        except Exception as e:
            if c.getPlayer().isGM():
                c.getPlayer().dropMessage("[系統提示]任務腳本:" + cm.getQuest() + "錯誤...NPC: " + cm.getNpc() + ":" + e)
            print("Error executing Quest script. (" + cm.getQuest() + ")...NPC: " + cm.getNpc() + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing Quest script. (" + cm.getQuest() + ")..NPCID: " + cm.getNpc() + ":" + e)
            self.dispose(c)
        finally:
            lock.unlock()

    def dispose(self, c: Any) -> None:
        npccm = self.mapleClientNPCConversationManagerMap.get(c)
        if npccm is not None:
            scriptsPath = os.environ.get("scripts_path")
            self.mapleClientNPCConversationManagerMap.remove(c)
            if npccm.getType() == -1:
                if npccm.getwh() == 0:
                    c.removeScriptEngine(scriptsPath +"scripts"+File.separator+"npc"+File.separator + npccm.getNpc() + ".js")
                else:
                    c.removeScriptEngine(scriptsPath +"scripts"+File.separator+"npc"+File.separator + npccm.getNpc() + "_" + npccm.getwh() + ".js")
                c.removeScriptEngine(scriptsPath +"scripts"+File.separator+"npc"+File.separator+"notcoded.js")
            else:
                c.removeScriptEngine(scriptsPath +"scripts"+File.separator+"quest"+File.separator + npccm.getQuest() + ".js")
        if c.getPlayer() is not None and c.getPlayer().getConversation() == 1:
            c.getPlayer().setConversation(0)

    def getCM(self, c: Any) -> Any:
        return self.mapleClientNPCConversationManagerMap.get(c)

