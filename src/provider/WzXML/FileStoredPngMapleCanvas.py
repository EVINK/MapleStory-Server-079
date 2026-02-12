"""
FileStoredPngMapleCanvas - Converted from Java source
Original: provider/WzXML/FileStoredPngMapleCanvas.java
Package: provider.WzXML
"""

from pathlib import Path
from typing import Optional, Any
import os
import tkinter

# Internal module imports
# from provider.MapleCanvas import *  # TODO: import specific classes


class FileStoredPngMapleCanvas(MapleCanvas):
    """
    Class FileStoredPngMapleCanvas
    Implements: MapleCanvas
    """

    def __init__(self, width: int, height: int, fileIn: Any):
        self.file = None
        self.width = 0
        self.height = 0
        self.image = None
        self.width = width
        self.height = height
        self.file = fileIn


    def getHeight(self) -> int:
        return self.height

    def getWidth(self) -> int:
        return self.width

    def getImage(self) -> Any:
        self.loadImageIfNecessary()
        return self.image

    def loadImageIfNecessary(self) -> None:
        if self.image is None:
            try:
                self.image = ImageIO.read(self.file)
                self.width = self.image.getWidth()
                self.height = self.image.getHeight()
            except IOError as e:
                raise RuntimeError(e)

