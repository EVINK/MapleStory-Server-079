"""
XMLWZFile - Converted from Java source
Original: provider/WzXML/XMLWZFile.java
Package: provider.WzXML
"""

from pathlib import Path
from typing import Optional, Any
import os

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes


class XMLWZFile(MapleDataProvider):
    """
    Class XMLWZFile
    Implements: MapleDataProvider
    """

    def __init__(self, fileIn: Any):
        self.root = None
        self.rootForNavigation = None
        self.root = fileIn
        self.rootForNavigation = WZDirectoryEntry(fileIn.getName(), 0, 0, None)
        self.fillMapleDataEntitys(self.root, self.rootForNavigation)


    def fillMapleDataEntitys(self, lroot: Any, wzdir: Any) -> None:
        for file in lroot.listFiles():
            fileName = file.getName()
            if file.isDirectory() and not fileName.endswith(".img"):
                newDir = WZDirectoryEntry(fileName, 0, 0, wzdir)
                wzdir.addDirectory(newDir)
                self.fillMapleDataEntitys(file, newDir)
            elif fileName.endswith(".xml"):
                wzdir.addFile(WZFileEntry(fileName[0:fileName.__len__(] - 4), 0, 0, wzdir))

    def getData(self, path: str) -> Any:
        dataFile = File(self.root, path + ".xml")
        imageDataDir = File(self.root, path)
        fis = None
        try:
            fis = FileInputStream(dataFile)
        except FileNotFoundException as e2:
            raise RuntimeError("Datafile " + path + " does not exist in " + self.root.getAbsolutePath())
        domMapleData = None
        try:
            domMapleData = XMLDomMapleData(fis, imageDataDir.getParentFile())
        finally:
            try:
                fis.close()
            except IOError as e:
                raise RuntimeError(e)
        return domMapleData

    def getRoot(self) -> Any:
        return self.rootForNavigation

