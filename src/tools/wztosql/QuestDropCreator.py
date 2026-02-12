"""
QuestDropCreator - Converted from Java source
Original: tools/wztosql/QuestDropCreator.java
Package: tools.wztosql
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys
import time

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from server.quest.MapleQuestRequirementType import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class QuestDropCreator:
    """
    Class QuestDropCreator
    """

    # Static initializer
    # QuestDropCreator.monsterQueryData = "drop_data"
    # QuestDropCreator.itemNameCache = new ArrayList<Pair<Integer, String>>()
    # QuestDropCreator.bossCache = {}
    # QuestDropCreator.quests = []
    # QuestDropCreator.itemIDs = []


    @staticmethod
    def getItemAmountNeeded(questid: int, itemid: int) -> int:
        data = None
        try:
            data = QuestDropCreator.requirements.getChildByPath(str(questid)).getChildByPath("1")
        except TypeError as ex:
            return 0
        if data is not None:
            for req in data.getChildren():
                type = MapleQuestRequirementType.getByWZName(req.getName())
                if !type == (MapleQuestRequirementType.item):
                    continue
                for d in req.getChildren():
                    if MapleDataTool.getInt(d.getChildByPath("id"), 0) == itemid:
                        return MapleDataTool.getInt(d.getChildByPath("count"), 0)
        return 0

    def isQuestRequirement(self, itemid: int) -> bool:
        for quest in QuestDropCreator.quests:
            if getItemAmountNeeded(quest.getId(), itemid) > 0:
                return True
        return False

    def getQuestID(self, itemid: int) -> int:
        for quest in QuestDropCreator.quests:
            if getItemAmountNeeded(quest.getId(), itemid) > 0:
                return quest.getId()
        return 0

    def initializeMySQL(self) -> None:
        DatabaseConnection.getConnection()
        QuestDropCreator.con = DatabaseConnection.getConnection()

    def loadQuests(self) -> None:
        QuestDropCreator.questData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Quest.wz"))
        QuestDropCreator.requirements = QuestDropCreator.questData.getData("Check.img")
        QuestDropCreator.info = QuestDropCreator.questData.getData("QuestInfo.img")
        for quest in QuestDropCreator.info.getChildren():
            QuestDropCreator.quests.add(MapleQuest.getInstance(int(quest.getName())))

    def loadQuestItems(self) -> None:
        items = MapleItemInformationProvider.getInstance().getAllItems()
        for item in items:
            itemid = item.getLeft()
            if !(itemid in QuestDropCreator.itemIDs) && isQuestRequirement(itemid):
                QuestDropCreator.itemIDs.add(itemid)

    def main(self, args: list) -> None:
        print("任务物品爆率更新")
        print("...")
        System.console().readLine()
        timeStart = int(time.time() * 1000)
        print("加载开始.\r\n")
        print("加载任务信息。。。")
        loadQuests()
        print("加载任务道具信息...")
        loadQuestItems()
        print("初始化到 MySQL...")
        initializeMySQL()
        print("加载信息完成.")
        try:
            ps = QuestDropCreator.con.prepareStatement("UPDATE drop_data SET questid = ? WHERE itemid = ?")
            psr = QuestDropCreator.con.prepareStatement("UPDATE reactordrops SET questid = ? WHERE itemid = ?")
            for itemid in QuestDropCreator.itemIDs:
                if MapleItemInformationProvider.getInstance().isQuestItem(itemid):
                    questId = getQuestID(itemid)
                    ps.setInt(1, questId)
                    ps.setInt(2, itemid)
                    psr.setInt(1, questId)
                    psr.setInt(2, itemid)
                    ps.executeUpdate()
                    psr.executeUpdate()
                    print("任务道具更新: " + itemid + " 任务ID: " + questId)
            ps.close()
            psr.close()
        except Exception as sqle:
            print(sqle.getMessage())
        timeEnd = int(time.time() * 1000) - timeStart
        print("更新任务爆率数据完成 耗时 " + (int)(timeEnd / 1000) + " 秒.")

