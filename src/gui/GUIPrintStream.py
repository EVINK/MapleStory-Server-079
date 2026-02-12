"""
GUIPrintStream - Converted from Java source
Original: gui/GUIPrintStream.java
Package: gui
"""

from io import IOBase
from typing import Optional, Any
import threading
import tkinter


class GUIPrintStream(PrintStream):
    """
    Class GUIPrintStream
    Extends: PrintStream
    """

    OUT = 0
    ERR = 1
    NOTICE = 2
    PACKET = 3

    def __init__(self, out: Any, mainComponent: Any, component: Any, type: int):
        self.mainComponent = None
        self.component = None
        self.type = None
        self.lineLimit = None
        super(out)
        self.mainComponent = mainComponent
        self.component = component
        self.type = type
        self.lineLimit = 100


    def write(self, buf: bytes, off: int, len: int) -> None:
        super.write(buf, off, len)
        message = String(buf, off, len)
        col = None
        # switch (self.type):
            # case 0:
            col = Color.BLACK
            break
            # case 1:
            col = Color.RED
            break
            # case 2:
            col = Color.BLUE
            break
            # case 3:
            col = Color.GRAY
            break
            # default:
            col = Color.BLACK
        SwingUtilities.invokeLater(Runnable()
            public void run()
                attrSet = SimpleAttributeSet()
                StyleConstants.setForeground(attrSet, col)
                doc = GUIPrintStream.self.component.getDocument()
                docMain = GUIPrintStream.self.mainComponent.getDocument()
                try:
                    docMainInfo = docMain.getText(0, docMain.getLength()).split("\r\n")
                    docInfo = doc.getText(0, doc.getLength()).split("\r\n")
                    i = None
                    if len(docMainInfo) >= GUIPrintStream.self.lineLimit + 1:
                        = 0
                        while i <= len(docMainInfo) - GUIPrintStream.self.lineLimit - 1:
                            docMain.remove(0, docMainInfo[i] + 2)
                    if len(docInfo) >= GUIPrintStream.self.lineLimit + 1:
                        = 0
                        while i <= len(docInfo) - GUIPrintStream.self.lineLimit - 1:
                            doc.remove(0, docInfo[i] + 2)
                    docMain.insertString(docMain.getLength(), message, attrSet)
                    doc.insertString(doc.getLength(), message, attrSet)
                except BadLocationException as var7:
                    GUIPrintStream.self.component.setText("輸出出錯:" + var7 + "\r\n內容:" + message + "\r\n類型:" + GUIPrintStream.self.type)

    def run(self) -> None:
        attrSet = SimpleAttributeSet()
        StyleConstants.setForeground(attrSet, col)
        doc = GUIPrintStream.self.component.getDocument()
        docMain = GUIPrintStream.self.mainComponent.getDocument()
        try:
            docMainInfo = docMain.getText(0, docMain.getLength()).split("\r\n")
            docInfo = doc.getText(0, doc.getLength()).split("\r\n")
            i = None
            if len(docMainInfo) >= GUIPrintStream.self.lineLimit + 1:
                = 0
                while i <= len(docMainInfo) - GUIPrintStream.self.lineLimit - 1:
                    docMain.remove(0, docMainInfo[i] + 2)
            if len(docInfo) >= GUIPrintStream.self.lineLimit + 1:
                = 0
                while i <= len(docInfo) - GUIPrintStream.self.lineLimit - 1:
                    doc.remove(0, docInfo[i] + 2)
            docMain.insertString(docMain.getLength(), message, attrSet)
            doc.insertString(doc.getLength(), message, attrSet)
        except BadLocationException as var7:
            GUIPrintStream.self.component.setText("輸出出錯:" + var7 + "\r\n內容:" + message + "\r\n類型:" + GUIPrintStream.self.type)

