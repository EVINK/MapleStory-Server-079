"""
EncodingDetect - Converted from Java source
Original: scripting/EncodingDetect.java
Package: scripting
"""

from pathlib import Path
from typing import Optional, Any
import os


class EncodingDetect:
    """
    Class EncodingDetect
    """


    def getJavaEncode(self, filePath: str) -> str:
        return getJavaEncode(File(filePath))

    def getJavaEncode_file(self, file: Any) -> str:
        s = BytesEncodingDetect()
        fileCode = BytesEncodingDetect.javaname[s.detectEncoding(file)]
        return fileCode

