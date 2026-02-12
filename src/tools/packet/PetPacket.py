"""
PetPacket - Converted from Java source
Original: tools/packet/PetPacket.java
Package: tools.packet
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class PetPacket:
    """
    Class PetPacket
    """

    # Static initializer
    # ITEM_MAGIC = new byte[] { -128, 5 }


    @staticmethod
    def updatePet(pet: Any, item: Any, active: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("updatePet--------------------")
        mplew.writeShort(SendPacketOpcode.MODIFY_INVENTORY_ITEM.getValue())
        mplew.write(pet.getInventoryPosition())
        mplew.write(2)
        mplew.write(3)
        mplew.write(5)
        mplew.writeShort(pet.getInventoryPosition())
        mplew.write(0)
        mplew.write(5)
        mplew.writeShort(pet.getInventoryPosition())
        mplew.write(3)
        mplew.writeInt(pet.getPetItemId())
        mplew.write(1)
        mplew.writeLong(pet.getUniqueId())
        PacketHelper.addPetItemInfo(mplew, item, pet, active)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def removePet(self, chr: Any, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removePet--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_PET.getValue())
        mplew.writeInt(chr.getId())
        mplew.writeShort(slot)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showPet(self, chr: Any, pet: Any, remove: bool, hunger: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showPet--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_PET.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(chr.getPetIndex(pet))
        if remove:
            mplew.write(0)
            mplew.write(hunger ? 1 : 0)
        else:
            mplew.write(1)
            mplew.write(0)
            mplew.writeInt(pet.getPetItemId())
            mplew.writeMapleAsciiString(pet.getName())
            mplew.writeLong(pet.getUniqueId())
            mplew.writeShort(pet.getPos().x)
            mplew.writeShort(pet.getPos().y)
            mplew.write(pet.getStance())
            mplew.writeLong(pet.getFh())
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def addPetInfo(self, mplew: Any, chr: Any, pet: Any, showpet: bool) -> None:
        if showpet:
            mplew.write(1)
            mplew.write(chr.getPetIndex(pet))
        mplew.writeInt(pet.getPetItemId())
        mplew.writeMapleAsciiString(pet.getName())
        mplew.writeLong(pet.getUniqueId())
        mplew.writeShort(pet.getPos().x)
        mplew.writeShort(pet.getPos().y)
        mplew.write(pet.getStance())
        mplew.writeLong(pet.getFh())

    def removePet_cid_index(self, cid: int, index: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("removePet--------------------")
        mplew.writeShort(SendPacketOpcode.SPAWN_PET.getValue())
        mplew.writeInt(cid)
        mplew.write(index)
        mplew.writeShort(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def movePet(self, cid: int, pid: int, slot: int, moves: list) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("movePet--------------------")
        mplew.writeShort(SendPacketOpcode.MOVE_PET.getValue())
        mplew.writeInt(cid)
        mplew.write(slot)
        mplew.writeInt(pid)
        PacketHelper.serializeMovementList(mplew, moves)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def petChat(self, cid: int, un: int, text: str, slot: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("petChat--------------------")
        mplew.writeShort(SendPacketOpcode.PET_CHAT.getValue())
        mplew.writeInt(cid)
        mplew.write(slot)
        mplew.writeShort(un)
        mplew.writeMapleAsciiString(text)
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def commandResponse(self, cid: int, command: int, slot: int, success: bool, food: bool) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("commandResponse--------------------")
        mplew.writeShort(SendPacketOpcode.PET_COMMAND.getValue())
        mplew.writeInt(cid)
        mplew.write(slot)
        mplew.write((command == 1) ? 1 : 0)
        mplew.write(command)
        if command == 1:
            mplew.write(0)
        else:
            mplew.writeShort(success ? 1 : 0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showOwnPetLevelUp(self, index: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showOwnPetLevelUp--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_ITEM_GAIN_INCHAT.getValue())
        mplew.write(4)
        mplew.write(0)
        mplew.write(index)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def showPetLevelUp(self, chr: Any, index: int) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("showPetLevelUp--------------------")
        mplew.writeShort(SendPacketOpcode.SHOW_FOREIGN_EFFECT.getValue())
        mplew.writeInt(chr.getId())
        mplew.write(4)
        mplew.write(0)
        mplew.write(index)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def emptyStatUpdate(self) -> Any:
        if ServerConstants.调试输出封包:
            print("emptyStatUpdate--------------------")
        return MaplePacketCreator.enableActions()

    def petStatUpdate_Empty(self) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("petStatUpdate_Empty--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(0)
        mplew.writeInt(MapleStat.PET.getValue())
        mplew.writeZeroBytes(25)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

    def petStatUpdate(self, chr: Any) -> Any:
        mplew = MaplePacketLittleEndianWriter()
        if ServerConstants.调试输出封包:
            print("petStatUpdate--------------------")
        mplew.writeShort(SendPacketOpcode.UPDATE_STATS.getValue())
        mplew.write(0)
        mplew.writeInt(MapleStat.PET.getValue())
        count = 0
        for pet in chr.getPets():
            if pet.getSummoned():
                mplew.writeLong(pet.getUniqueId())
                count += 1
        while count < 3:
            mplew.writeZeroBytes(8)
            count += 1
        mplew.write(0)
        if ServerConstants.PACKET_ERROR_OFF:
            ERROR = ServerConstants()
            ERROR.setPACKET_ERROR(" 暂未定义 ：\r\n" + mplew.getPacket() + "\r\n\r\n")
        return mplew.getPacket()

