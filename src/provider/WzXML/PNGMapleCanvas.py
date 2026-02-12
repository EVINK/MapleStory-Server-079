"""
PNGMapleCanvas - Converted from Java source
Original: provider/WzXML/PNGMapleCanvas.java
Package: provider.WzXML
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from provider.MapleCanvas import *  # TODO: import specific classes


class PNGMapleCanvas(MapleCanvas):
    """
    Class PNGMapleCanvas
    Implements: MapleCanvas
    """

    def __init__(self, width: int, height: int, dataLength: int, format: int, data: bytes):
        self.height = None
        self.width = None
        self.dataLength = None
        self.format = None
        self.height = height
        self.width = width
        self.dataLength = dataLength
        self.format = format
        self.data = data

    # Static initializer
    # ZAHLEN = new int[] { 2, 1, 0, 3 }


    def getHeight(self) -> int:
        return self.height

    def getWidth(self) -> int:
        return self.width

    def getFormat(self) -> int:
        return self.format

    def getData(self) -> bytes:
        return self.data

    def getImage(self) -> Any:
        sizeUncompressed = 0
        size8888 = 0
        maxWriteBuf = 2
        maxHeight = 3
        writeBuf = new byte[maxWriteBuf]
        # switch (self.getFormat()):
            # case 1:
            # case 513:
                sizeUncompressed = self.getHeight() * self.getWidth() * 4
                break
            # case 2:
                sizeUncompressed = self.getHeight() * self.getWidth() * 8
                break
            # case 517:
                sizeUncompressed = self.getHeight() * self.getWidth() / 128
                break
        size8888 = self.getHeight() * self.getWidth() * 8
        if size8888 > maxWriteBuf:
            maxWriteBuf = size8888
            writeBuf = new byte[maxWriteBuf]
        if self.getHeight() > maxHeight:
            maxHeight = self.getHeight()
        dec = Inflater()
        dec.setInput(self.getData(), 0, self.dataLength)
        declen = 0
        uc = new byte[sizeUncompressed]
        try:
            declen = dec.inflate(uc)
        except DataFormatException as ex:
            raise RuntimeError("zlib fucks", ex)
        dec.end()
        # switch (self.getFormat()):
            # case 1:
                for i in range(sizeUncompressed):
                    low = (byte)(uc[i] & 0xF)
                    high = (byte)(uc[i] & 0xF0)
                    writeBuf[i << 1] = (byte)((low << 4 | low) & 0xFF)
                    writeBuf[(i << 1) + 1] = (byte)(high | (high >>> 4 & 0xF))
                break
            # case 2:
                writeBuf = uc
                break
            # case 513:
                i = 0
                while i < declen:
                    bBits = (byte)((uc[i] & 0x1) << 3)
                    gBits = (byte)((uc[i + 1] & 0x7) << 5 | (uc[i] & 0xE0) >> 3)
                    rBits = (byte)(uc[i + 1] & 0xF8)
                    writeBuf[i << 1] = (byte)(bBits | bBits >> 5)
                    writeBuf[(i << 1) + 1] = (byte)(gBits | gBits >> 6)
                    writeBuf[(i << 1) + 2] = (byte)(rBits | rBits >> 5)
                    writeBuf[(i << 1) + 3] = -1
                break
            # case 517:
                b = 0
                pixelIndex = 0
                for j in range(declen):
                    for k in range(8):
                        b = (byte)(((uc[j] & 1 << 7 - k) >> 7 - k) * 255)
                        for l in range(16):
                            pixelIndex = (j << 9) + (k << 6) + l * 2
                            writeBuf[pixelIndex] = b
                            writeBuf[pixelIndex + 2] = (writeBuf[pixelIndex + 1] = b)
                            writeBuf[pixelIndex + 3] = -1
                break
        imgData = DataBufferByte(writeBuf, sizeUncompressed)
        sm = PixelInterleavedSampleModel(0, self.getWidth(), self.getHeight(), 4, self.getWidth() * 4, PNGMapleCanvas.ZAHLEN)
        imgRaster = Raster.createWritableRaster(sm, imgData, Point(0, 0))
        aa = BufferedImage(self.getWidth(), self.getHeight(), 2)
        aa.setData(imgRaster)
        return aa

