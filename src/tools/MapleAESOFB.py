"""
MapleAESOFB - Converted from Java source
Original: tools/MapleAESOFB.java
Package: tools
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import Optional, Any
import tkinter


class MapleAESOFB:
    """
    Class MapleAESOFB
    """

    def __init__(self, iv: bytes, mapleVersion: int):
        self.cipher = None
        self.mapleVersion = None
        try:
            self.cipher = Cipher.getInstance("AES")
            self.cipher.init(1, skey)
        except Exception:
            print("ERROR" + e)
        except InvalidKeyException as e:
            print("Error initalizing the encryption cipher.  Make sure you're using the Unlimited Strength cryptography jar files.")
        setIv(iv)
        self.mapleVersion = (short)(mapleVersion >> 8 & 0xFF | mapleVersion << 8 & 0xFF00)

    # Static initializer
    # skey = SecretKeySpec(new byte[] { 19, 0, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0, -76, 0, 0, 0, 27, 0, 0, 0, 15, 0, 0, 0, 51, 0, 0, 0, 82, 0, 0, 0 }, "AES")
    # MapleAESOFB.MAPLE_AES_KEY = new byte[] { 19, 0, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0, -76, 0, 0, 0, 27, 0, 0, 0, 15, 0, 0, 0, 51, 0, 0, 0, 82, 0, 0, 0 }
    # funnyBytes = new byte[] { -20, 63, 119, -92, 69, -48, 113, -65, -73, -104, 32, -4, 75, -23, -77, -31, 92, 34, -9, 12, 68, 27, -127, -67, 99, -115, -44, -61, -14, 16, 25, -32, -5, -95, 110, 102, -22, -82, -42, -50, 6, 24, 78, -21, 120, -107, -37, -70, -74, 66, 122, 42, -125, 11, 84, 103, 109, -24, 101, -25, 47, 7, -13, -86, 39, 123, -123, -80, 38, -3, -117, -87, -6, -66, -88, -41, -53, -52, -110, -38, -7, -109, 96, 45, -35, -46, -94, -101, 57, 95, -126, 33, 76, 105, -8, 49, -121, -18, -114, -83, -116, 106, -68, -75, 107, 89, 19, -15, 4, 0, -10, 90, 53, 121, 72, -113, 21, -51, -105, 87, 18, 62, 55, -1, -99, 79, 81, -11, -93, 112, -69, 20, 117, -62, -72, 114, -64, -19, 125, 104, -55, 46, 13, 98, 70, 23, 17, 77, 108, -60, 126, 83, -63, 37, -57, -102, 28, -120, 88, 44, -119, -36, 2, 100, 64, 1, 93, 56, -91, -30, -81, 85, -43, -17, 26, 124, -89, 91, -90, 111, -122, -97, 115, -26, 10, -34, 43, -103, 74, 71, -100, -33, 9, 118, -98, 48, 14, -28, -78, -108, -96, 59, 52, 29, 40, 15, 54, -29, 35, -76, 3, -40, -112, -56, 60, -2, 94, 50, 36, 80, 31, 58, 67, -118, -106, 65, 116, -84, 82, 51, -16, -39, 41, -128, -79, 22, -45, -85, -111, -71, -124, 127, 97, 30, -49, -59, -47, 86, 61, -54, -12, 5, -58, -27, 8, 73 }
    # rammyByte = new byte[] { -20, 63, 119, -92, 69, -48, 113, -65, -73, -104, 32, -4, 75, -23, -77, -31, 92, 34, -9, 12, 68, 27, -127, -67, 99, -115, -44, -61, -14, 16, 25, -32, -5, -95, 110, 102, -22, -82, -42, -50, 6, 24, 78, -21, 120, -107, -37, -70, -74, 66, 122, 42, -125, 11, 84, 103, 109, -24, 101, -25, 47, 7, -13, -86, 39, 123, -123, -80, 38, -3, -117, -87, -6, -66, -88, -41, -53, -52, -110, -38, -7, -109, 96, 45, -35, -46, -94, -101, 57, 95, -126, 33, 76, 105, -8, 49, -121, -18, -114, -83, -116, 106, -68, -75, 107, 89, 19, -15, 4, 0, -10, 90, 53, 121, 72, -113, 21, -51, -105, 87, 18, 62, 55, -1, -99, 79, 81, -11, -93, 112, -69, 20, 117, -62, -72, 114, -64, -19, 125, 104, -55, 46, 13, 98, 70, 23, 17, 77, 108, -60, 126, 83, -63, 37, -57, -102, 28, -120, 88, 44, -119, -36, 2, 100, 64, 1, 93, 56, -91, -30, -81, 85, -43, -17, 26, 124, -89, 91, -90, 111, -122, -97, 115, -26, 10, -34, 43, -103, 74, 71, -100, -33, 9, 118, -98, 48, 14, -28, -78, -108, -96, 59, 52, 29, 40, 15, 54, -29, 35, -76, 3, -40, -112, -56, 60, -2, 94, 50, 36, 80, 31, 58, 67, -118, -106, 65, 116, -84, 82, 51, -16, -39, 41, -128, -79, 22, -45, -85, -111, -71, -124, 127, 97, 30, -49, -59, -47, 86, 61, -54, -12, 5, -58, -27, 8, 73 }


    def getPacketLength(self, packetHeader: int) -> int:
        packetLength = packetHeader >>> 16 ^ (packetHeader & 0xFFFF)
        packetLength = ((packetLength << 8 & 0xFF00) | (packetLength >>> 8 & 0xFF))
        return packetLength

    def getNewIv(self, oldIv: bytes) -> bytes:
        in = { -14, 83, 80, -58 }
        for x in range(4):
            funnyShit(oldIv[x], in)
        return in

    def funnyShit(self, inputByte: int, in: bytes) -> None:
        elina = in[1]
        anna = inputByte
        moritz = MapleAESOFB.funnyBytes[elina & 0xFF]
        moritz -= inputByte
        n = 0
        in[n] += moritz
        moritz = in[2]
        moritz ^= MapleAESOFB.funnyBytes[anna & 0xFF]
        elina -= (byte)(moritz & 0xFF)
        in[1] = elina
        elina = (moritz = in[3])
        elina -= (byte)(in[0] & 0xFF)
        moritz = MapleAESOFB.funnyBytes[moritz & 0xFF]
        moritz += inputByte
        moritz ^= in[2]
        in[2] = moritz
        elina += (byte)(MapleAESOFB.funnyBytes[anna & 0xFF] & 0xFF)
        in[3] = elina
        merry = in[0] & 0xFF
        merry |= (in[1] << 8 & 0xFF00)
        merry |= (in[2] << 16 & 0xFF0000)
        merry |= (in[3] << 24 & 0xFF000000)
        ret_value = merry >>> 29
        merry <<= 3
        ret_value |= merry
        in[0] = (byte)(ret_value & 0xFF)
        in[1] = (byte)(ret_value >> 8 & 0xFF)
        in[2] = (byte)(ret_value >> 16 & 0xFF)
        in[3] = (byte)(ret_value >> 24 & 0xFF)

    def setIv(self, iv: bytes) -> None:
        self.iv = iv

    def getIv(self) -> bytes:
        return self.iv

    def crypt(self, data: bytes) -> bytes:
        remaining = len(data)
        llength = 1456
        start = 0
        try:
            while remaining > 0:
                myIv = BitTools.multiplyBytes(self.iv, 4, 4)
                if remaining < llength:
                llength = remaining
                x = start
                while x < start + llength:
                    if (x - start) % len(myIv) == 0:
                        newIv = self.cipher.doFinal(myIv)
                        for j in range(len(myIv)):
                        myIv[j] = newIv[j]
                    data[x] = (byte)(data[x] ^ myIv[(x - start) % len(myIv)])
                start += llength
                remaining -= llength
                llength = 1460
            updateIv()
        except Exception:
            e.printStackTrace()
        return data

    def updateIv(self) -> None:
        self.iv = getNewIv(self.iv)

    def getPacketHeader(self, length: int) -> bytes:
        iiv = ((self.iv[3] & 0xFF) | (self.iv[2] << 8 & 0xFF00)) ^ self.mapleVersion
        mlength = ((length << 8 & 0xFF00) | length >>> 8) ^ iiv
        return new byte[] { (byte)(iiv >>> 8 & 0xFF), (byte)(iiv & 0xFF), (byte)(mlength >>> 8 & 0xFF), (byte)(mlength & 0xFF) }

    def checkPacket(self, packet: bytes) -> bool:
        return ((packet[0] ^ self.iv[2]) & 0xFF) == (self.mapleVersion >> 8 & 0xFF) && ((packet[1] ^ self.iv[3]) & 0xFF) == (self.mapleVersion & 0xFF)

    def checkPacket_packetHeader(self, packetHeader: int) -> bool:
        return self.checkPacket(new byte[] { (byte)(packetHeader >> 24 & 0xFF), (byte)(packetHeader >> 16 & 0xFF) })

    def toString(self) -> str:
        return "IV: " + HexTool.toString(self.iv)

