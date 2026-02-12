"""
LoginCryptoLegacy - Converted from Java source
Original: client/LoginCryptoLegacy.java
Package: client
"""

from typing import List
from typing import Optional, Any
import hashlib
import time


class LoginCryptoLegacy:
    """
    Class LoginCryptoLegacy
    """

    # Static initializer
    # rand = Random()
    # iota64 = new char[64]
    # i = 0
    # LoginCryptoLegacy.iota64[i++] = '.'
    # LoginCryptoLegacy.iota64[i++] = '/'
    # c = 'A'
    # while c <= 'Z':
    # LoginCryptoLegacy.iota64[i++] = c
    # c = 'a'
    # while c <= 'z':
    # LoginCryptoLegacy.iota64[i++] = c
    # c = '0'
    # while c <= '9':
    # LoginCryptoLegacy.iota64[i++] = c


    @staticmethod
    def hashPassword(password: str) -> str:
        randomBytes = new byte[6]
        LoginCryptoLegacy.rand.setSeed(int(time.time() * 1000))
        LoginCryptoLegacy.rand.nextBytes(randomBytes)
        return myCrypt(password, genSalt(randomBytes))

    def checkPassword(self, password: str, hash: str) -> bool:
        return myCrypt(password, hash) == (hash)

    def isLegacyPassword(self, hash: str) -> bool:
        return hash[0:3] == ("$H$")

    def myCrypt(self, password: str, seed: str) -> str:
        out = None
        count = 8
        if not seed[0:3] == ("$H$"):
            randomBytes = new byte[6]
            LoginCryptoLegacy.rand.nextBytes(randomBytes)
            seed = genSalt(randomBytes)
        salt = seed[4:12]
        if salt != 8:
            raise RuntimeError("Error hashing password - Invalid seed.")
        try:
            digester = MessageDigest.getInstance("SHA-1")
            digester.update((salt + password).encode("utf-8"), 0, (salt + password))
            sha1Hash = digester.digest()
            while True:
                CombinedBytes = new byte[len(sha1Hash) + password]
                System.arraycopy(sha1Hash, 0, CombinedBytes, 0, len(sha1Hash))
                System.arraycopy(password.encode("utf-8"), 0, CombinedBytes, len(sha1Hash), password.encode("utf-8").length)
                digester.update(CombinedBytes, 0, len(CombinedBytes))
                sha1Hash = digester.digest()
            out = seed[0:12]
            out += encode64(sha1Hash)
        catch (NoSuchAlgorithmException | UnsupportedEncodingException ex2)
            ex2.printStackTrace()
            print("Error hashing password." + ex2.getMessage())
        if out is None:
            raise RuntimeError("Error hashing password - out = None")
        return out

    def genSalt(self, Random: bytes) -> str:
        Salt = ""
        Salt.append(LoginCryptoLegacy.iota64[30])
        Salt.append(encode64(Random))
        return Salt

    def convertToHex(self, data: bytes) -> str:
        buf = ""
        for i in range(len(data)):
            halfbyte = data[i] >>> 4 & 0xF
            two_halfs = 0
            while True:
                if 0 <= halfbyte and halfbyte <= 9:
                    buf.append((char)(48 + halfbyte))
                else:
                    buf.append((char)(97 + (halfbyte - 10)))
                halfbyte = (data[i] & 0xF)
        return buf

    def encodeSHA1(self, text: str) -> str:
        md = MessageDigest.getInstance("SHA-1")
        md.update(text.encode("utf-8"), 0, text)
        return convertToHex(md.digest())

    def encode64(self, Input: bytes) -> str:
        iLen = len(Input)
        oDataLen = (iLen * 4 + 2) / 3
        oLen = (iLen + 2) / 3 * 4
        out = new char[oLen]
        i0 = None
        i2 = None
        i3 = None
        o0 = None
        o2 = None
        o3 = None
        o4 = None
        for (int ip = 0, op = 0; ip < iLen; i0 = (Input[ip++] & 0xFF), i2 = ((ip < iLen) ? (Input[ip++] & 0xFF) : 0), i3 = ((ip < iLen) ? (Input[ip++] & 0xFF) : 0), o0 = i0 >>> 2, o2 = ((i0 & 0x3) << 4 | i2 >>> 4), o3 = ((i2 & 0xF) << 2 | i3 >>> 6), o4 = (i3 & 0x3), out[op++] = LoginCryptoLegacy.iota64[o0], out[op++] = LoginCryptoLegacy.iota64[o2], out[op] = ((op < oDataLen) ? LoginCryptoLegacy.iota64[o3] : '='), ++op, out[op] = ((op < oDataLen) ? LoginCryptoLegacy.iota64[o4] : '='), ++op) {}
        return String(out)

