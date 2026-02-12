"""
WZDirectoryEntry - Converted from Java source
Original: provider/WzXML/WZDirectoryEntry.java
Package: provider.WzXML
"""

from typing import Dict
from typing import List
from typing import Optional, Any
import os

# Internal module imports
# from provider.MapleDataDirectoryEntry import *  # TODO: import specific classes
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from provider.MapleDataEntry import *  # TODO: import specific classes
# from provider.MapleDataFileEntry import *  # TODO: import specific classes


class WZDirectoryEntry(WZEntry, MapleDataDirectoryEntry):
    """
    Class WZDirectoryEntry
    Extends: WZEntry
    Implements: MapleDataDirectoryEntry
    """

    def __init__(self, name: str, size: int, checksum: int, parent: Any):
        self.subdirs = []
        self.files = []
        self.entries = {}
        super(name, size, checksum, parent)
        self.subdirs = []
        self.files = []
        self.entries = {}


    def addDirectory(self, dir: Any) -> None:
        self.subdirs.add(dir)
        self.entries.put(dir.getName(), dir)

    def addFile(self, fileEntry: Any) -> None:
        self.files.add(fileEntry)
        self.entries.put(fileEntry.getName(), fileEntry)

    def getSubdirectories(self) -> list:
        return Collections.unmodifiableList((List<? extends MapleDataDirectoryEntry>)self.subdirs)

    def getFiles(self) -> list:
        return Collections.unmodifiableList((List<? extends MapleDataFileEntry>)self.files)

    def getEntry(self, name: str) -> Any:
        return self.entries.get(name)

