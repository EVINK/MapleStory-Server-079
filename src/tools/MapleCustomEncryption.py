"""
MapleCustomEncryption - Converted from Java source
Original: tools/MapleCustomEncryption.java
Package: tools
"""

from typing import Optional, Any


class MapleCustomEncryption:
    """
    Class MapleCustomEncryption
    """


    def encryptData(self, data: bytes) -> bytes:
        for j in range(6):
            remember = 0
            dataLength = (byte)(len(data) & 0xFF)
            if j % 2 == 0:
                for i in range(len(data)):
                    cur = data[i]
                    cur = BitTools.rollLeft(cur, 3)
                    cur += dataLength
                    cur = (remember ^= cur)
                    cur = BitTools.rollRight(cur, dataLength & 0xFF)
                    cur = (byte)(~cur & 0xFF)
                    cur += 72
                    dataLength -= 1
                    data[i] = cur
            else:
                i = len(data) - 1
                while i >= 0:
                    cur = data[i]
                    cur = BitTools.rollLeft(cur, 4)
                    cur += dataLength
                    cur = (remember ^= cur)
                    cur ^= 0x13
                    cur = BitTools.rollRight(cur, 3)
                    dataLength -= 1
                    data[i] = cur
        return data

    def decryptData(self, data: bytes) -> bytes:
        for j in range(1, = 6):
            remember = 0
            dataLength = (byte)(len(data) & 0xFF)
            nextRemember = 0
            if j % 2 == 0:
                for i in range(len(data)):
                    cur = data[i]
                    cur -= 72
                    cur = (byte)(~cur & 0xFF)
                    cur = (nextRemember = BitTools.rollLeft(cur, dataLength & 0xFF))
                    cur ^= remember
                    remember = nextRemember
                    cur -= dataLength
                    cur = BitTools.rollRight(cur, 3)
                    data[i] = cur
                    dataLength -= 1
            else:
                i = len(data) - 1
                while i >= 0:
                    cur = data[i]
                    cur = BitTools.rollLeft(cur, 3)
                    cur = (nextRemember = (byte)(cur ^ 0x13))
                    cur ^= remember
                    remember = nextRemember
                    cur -= dataLength
                    cur = BitTools.rollRight(cur, 4)
                    data[i] = cur
                    dataLength -= 1
        return data

