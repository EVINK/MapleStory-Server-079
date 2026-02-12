"""
MapleCustomQuest - Converted from Java source
Original: server/quest/MapleCustomQuest.java
Package: server.quest
"""

from io import BytesIO
from pymysql.cursors import Cursor
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class MapleCustomQuest(MapleQuest):
    """
    Class MapleCustomQuest
    Extends: MapleQuest
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, id: int):
        super(id)
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM questrequirements WHERE questid = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            while rs.next():
                blob = rs.getBlob("data")
                ois = ObjectInputStream(ByteArrayInputStream(blob.encode("utf-8")blob)))
                data = ois.readObject()
                req = MapleQuestRequirement(this, MapleQuestRequirementType.getByWZName(data.getName()), data)
                status = rs.getByte("status")
                if status == 0:
                    self.startReqs.add(req)
                else:
                    if status != 1:
                        continue
                    self.completeReqs.add(req)
            rs.close()
            ps.close()
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM questactions WHERE questid = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            while rs.next():
                blob2 = rs.getBlob("data")
                ois2 = ObjectInputStream(ByteArrayInputStream(blob2.encode("utf-8")blob2)))
                data = ois2.readObject()
                act = MapleQuestAction(MapleQuestActionType.getByWZName(data.getName()), data, this)
                status2 = rs.getByte("status")
                if status2 == 0:
                    self.startActs.add(act)
                else:
                    if status2 != 1:
                        continue
                    self.completeActs.add(act)
            rs.close()
            ps.close()
        except Exception as e:
            e.printStackTrace()
            print("Error loading custom quest from SQL." + e)


