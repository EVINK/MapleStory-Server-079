"""
LieDetectorScript - Converted from Java source
Original: scripting/LieDetectorScript.java
Package: scripting
"""

from io import BytesIO
from io import IOBase
from pathlib import Path
from socket import socket
from typing import Optional, Any
import os
import struct
import sys

# Internal module imports
# from server.Randomizer import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class LieDetectorScript:
    """
    Class LieDetectorScript
    """

    IMG_DIRECTORY = "scripts/lieDetector"
    CAPTCHA_VERIFIER = "98818D40B83AECCFB7AFD7FD9653E1037519AC61"
    CAPTCHA_SERVER = "http://localhost/captcha.php?verify=98818D40B83AECCFB7AFD7FD9653E1037519AC61"


    def getImageBytes(self) -> Any:
        try:
            url = URL(CAPTCHA_SERVER)
            inputStream = url.openStream()
            output = ByteArrayOutputStream()
            buffer = new byte[1024]
            n = 0
            while -1 != (n = inputStream.read(buffer)):
                output.write(buffer, 0, n)
            imgByte = HexTool.toString(output.toByteArray())
            return new Pair<String, String>(imgByte[39:imgByte.__len__(]), output.split("CAPTCHA")[0])
        except IOException as ex:
            ex.printStackTrace()
            scriptsPath = os.environ.get("scripts_path")
            directory = File(scriptsPath+"scripts"+File.separator+"lieDetector")
            if !directory.exists():
                print("lieDetector folder does not exist!")
                return None
            filename = directory.list()
            answer = filename[Randomizer.nextInt(len(filename))]
            answer = answer[0:answer.__len__(] - 4)
            try:
                return new Pair<String, String>(HexTool.toString(getBytesFromFile(File(scriptsPath+"scripts"+File.separator+"lieDetector"+File.separator + answer + ".jpg"))), answer)
            except IOException as ex2:
                ex2.printStackTrace()
                return None

    def getBytesFromFile(self, file: Any) -> bytes:
        bytes = None
        try:
            is = FileInputStream(file)
            length = file
            if length > 2147483647:
                return None
            bytes = new byte[length]
            offset = 0
            numRead = 0
            while offset < len(bytes) && (numRead = is.read(bytes, offset, len(bytes) - offset)) >= 0:
            if offset < len(bytes):
                print("[Lie Detector Script] Could not completely read file " + file.getName())
                return None
        except IOException as e:
            e.printStackTrace()
            return None
        return bytes

