"""
WzStringDumper宠物数据 - Converted from Java source
Original: tools/wztosql/WzStringDumper宠物数据.java
Package: tools.wztosql
"""

from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Any
import os

# Internal module imports
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes


class WzStringDumper宠物数据:
    """
    Class WzStringDumper宠物数据
    """


    def main(self, args: list) -> None:
        stringFile = MapleDataProviderFactory.fileInwzPath("String.wz")
        stringProvider = MapleDataProviderFactory.getDataProvider(stringFile)
        pet = stringProvider.getData("Pet.img")
        output = args[0]
        outputDir = File(output)
        petTxt = File(output + "/Pet.txt")
        outputDir.mkdir()
        petTxt.createNewFile()
        print("开始提取宠物数据....")
        # try-with-resources: final PrintWriter writer = PrintWriter(FileOutputStream(petTxt))
        try:
            for child in pet.getChildren():
                writer.println("INSERT INTO `cashshop_modified_items` VALUES ('600500', '8000', '0', '1', '" + child.getName() + "', '0', '0', '0', '2', '1', '0', '0', '0', '0', '0'")
            writer.flush()
        print("宠物数据提取完成....")

