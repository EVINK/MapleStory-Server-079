"""
XMLDomMapleData - Converted from Java source
Original: provider/WzXML/XMLDomMapleData.java
Package: provider.WzXML
"""

from pathlib import Path
from typing import Iterator
from typing import List
from typing import Optional, Any
import logging
import os
import tkinter
import xml.etree.ElementTree as ET

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataEntity import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes


class XMLDomMapleData(MapleData):
    """
    Class XMLDomMapleData
    Implements: MapleData, Serializable
    """

    def __init__(self, node: Any):
        self.node = None
        self.imageDataDir = None
        self.node = node


    def getChildByPath(self, path: str) -> Any:
        segments = path.split("/")
        if segments[0] == (".."):
            return (self.getParent()).getChildByPath(path[path.find("/":] + 1))
        myNode = self.node
        for x in range(len(segments)):
            childNodes = myNode.getChildNodes()
            foundChild = False
            for i in range(childNodes.getLength()):
                try:
                    childNode = childNodes.item(i)
                    if childNode is not None && childNode.getNodeType() == 1 && childNode.getAttributes().getNamedItem("name").getNodeValue() == (segments[x]):
                        myNode = childNode
                        foundChild = True
                        break
                except TypeError as e:
                    FileoutputUtil.outputFileError(FileoutputUtil.PacketEx_Log, e)
            if !foundChild:
                return None
        ret = XMLDomMapleData(myNode)
        ret.imageDataDir = File(self.imageDataDir, self.getName() + "/" + path).getParentFile()
        return ret

    def getChildren(self) -> list:
        ret = []
        childNodes = self.node.getChildNodes()
        for i in range(childNodes.getLength()):
            childNode = childNodes.item(i)
            if childNode is not None && childNode.getNodeType() == 1:
                child = XMLDomMapleData(childNode)
                child.imageDataDir = File(self.imageDataDir, self.getName())
                ret.add(child)
        return ret

    def getData(self) -> Any:
        attributes = self.node.getAttributes()
        type = self.getType()
        # switch (type):
            # case DOUBLE:
                return float(attributes.getNamedItem("value").getNodeValue())
            # case FLOAT:
                return float(attributes.getNamedItem("value").getNodeValue())
            # case INT:
                return int(attributes.getNamedItem("value").getNodeValue())
            # case SHORT:
                return Short.parseShort(attributes.getNamedItem("value").getNodeValue())
            # case STRING:
            # case UOL:
                return attributes.getNamedItem("value").getNodeValue()
            # case VECTOR:
                return Point(int(attributes.getNamedItem("x").getNodeValue()), int(attributes.getNamedItem("y").getNodeValue()))
            # case CANVAS:
                return FileStoredPngMapleCanvas(int(attributes.getNamedItem("width").getNodeValue()), int(attributes.getNamedItem("height").getNodeValue()), File(self.imageDataDir, self.getName() + ".png"))
            # default:
                return None

    def getType(self) -> Any:
        nodeName2 = None
        nodeName = nodeName2 = self.node.getNodeName()
        # switch (nodeName2):
            # case "imgdir":
                return MapleDataType.PROPERTY
            # case "canvas":
                return MapleDataType.CANVAS
            # case "convex":
                return MapleDataType.CONVEX
            # case "sound":
                return MapleDataType.SOUND
            # case "uol":
                return MapleDataType.UOL
            # case "double":
                return MapleDataType.DOUBLE
            # case "float":
                return MapleDataType.FLOAT
            # case "int":
                return MapleDataType.INT
            # case "short":
                return MapleDataType.SHORT
            # case "string":
                return MapleDataType.STRING
            # case "vector":
                return MapleDataType.VECTOR
            # case "None":
                return MapleDataType.IMG_0x00
            # default:
                return None

    def getParent(self) -> Any:
        parentNode = self.node.getParentNode()
        if parentNode.getNodeType() == 9:
            return None
        parentData = XMLDomMapleData(parentNode)
        parentData.imageDataDir = self.imageDataDir.getParentFile()
        return parentData

    def getName(self) -> str:
        return self.node.getAttributes().getNamedItem("name").getNodeValue()

    def iterator(self) -> iter:
        return self.getChildren().iterator()

