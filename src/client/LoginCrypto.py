"""
LoginCrypto - Converted from Java source
Original: client/LoginCrypto.java
Package: client
"""

from typing import List
from typing import Optional, Any
import hashlib

# Internal module imports
# from tools import *  # TODO: import specific classes


class LoginCrypto:
    """
    Class LoginCrypto
    """

    # Static initializer
    # LoginCrypto.extralength = 6
    # Alphabet = new String[] { "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" }
    # Number = new String[] { "1", "2", "3", "4", "5", "6", "7", "8", "9" }
    # rand = Random()


    @staticmethod
    def Generate_13DigitAsiasoftPassport() -> str:
        sb = ""
        sb.append(LoginCrypto.Alphabet[LoginCrypto.rand.nextInt(LoginCrypto.len(Alphabet))])
        for i in range(11):
            sb.append(LoginCrypto.Number[LoginCrypto.rand.nextInt(LoginCrypto.len(Number))])
        sb.append(LoginCrypto.Alphabet[LoginCrypto.rand.nextInt(LoginCrypto.len(Alphabet))])
        return sb

    def toSimpleHexString(self, bytes: bytes) -> str:
        return HexTool.toString(bytes).replace(" ", "").lower()

    def hashWithDigest(self, in: str, digest: str) -> str:
        try:
            Digester = MessageDigest.getInstance(digest)
            Digester.update(in.encode("utf-8"), 0, in)
            sha1Hash = Digester.digest()
            return toSimpleHexString(sha1Hash)
        except NoSuchAlgorithmException as ex:
            raise RuntimeError("Hashing the password failed", ex)
        except UnsupportedEncodingException as e:
            raise RuntimeError("Encoding the string failed", e)

    def hexSha1(self, in: str) -> str:
        return hashWithDigest(in, "SHA-1")

    def hexSha512(self, in: str) -> str:
        return hashWithDigest(in, "SHA-512")

    def checkSha1Hash(self, hash: str, password: str) -> bool:
        return hash == (makeSaltedSha1Hash(password))

    def checkSaltedSha512Hash(self, hash: str, password: str, salt: str) -> bool:
        return hash == (makeSaltedSha512Hash(password, salt))

    def makeSaltedSha512Hash(self, password: str, salt: str) -> str:
        return hexSha512(password + salt)

    def makeSaltedSha1Hash(self, password: str) -> str:
        return hexSha1(password)

    def makeSalt(self) -> str:
        salt = new byte[16]
        LoginCrypto.rand.nextBytes(salt)
        return toSimpleHexString(salt)

    def rand_s(self, in: str) -> str:
        sb = ""
        for i in range(LoginCrypto.extralength):
            sb.append(LoginCrypto.rand.nextBoolean() ? LoginCrypto.Alphabet[LoginCrypto.rand.nextInt(LoginCrypto.len(Alphabet))] : LoginCrypto.Number[LoginCrypto.rand.nextInt(LoginCrypto.len(Number))])
        return sb + in

    def rand_r(self, in: str) -> str:
        return in[LoginCrypto.extralength:LoginCrypto.extralength + 128]

