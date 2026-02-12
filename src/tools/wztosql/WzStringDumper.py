"""
WzStringDumper - Converted from Java source
Original: tools/wztosql/WzStringDumper.java
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


class WzStringDumper:
    """
    Class WzStringDumper
    """


    def main(self, args: list) -> None:
        stringFile = MapleDataProviderFactory.fileInwzPath("string.wz")
        stringProvider = MapleDataProviderFactory.getDataProvider(stringFile)
        cash = stringProvider.getData("Cash.img")
        consume = stringProvider.getData("Consume.img")
        eqp = stringProvider.getData("Eqp.img").getChildByPath("Eqp")
        etc = stringProvider.getData("Etc.img").getChildByPath("Etc")
        ins = stringProvider.getData("Ins.img")
        pet = stringProvider.getData("Pet.img")
        map = stringProvider.getData("Map.img")
        mob = stringProvider.getData("Mob.img")
        skill = stringProvider.getData("Skill.img")
        npc = stringProvider.getData("Npc.img")
        output = args[0]
        outputDir = File(output)
        cashTxt = File(output + "/Cash.txt")
        useTxt = File(output + "/Use.txt")
        eqpDir = File(output + "/Equip")
        etcTxt = File(output + "/Etc.txt")
        insTxt = File(output + "/Setup.txt")
        petTxt = File(output + "/Pet.txt")
        mapTxt = File(output + "/Map.txt")
        mobTxt = File(output + "/Mob.txt")
        skillTxt = File(output + "/Skill.txt")
        npcTxt = File(output + "/NPC.txt")
        outputDir.mkdir()
        cashTxt.createNewFile()
        useTxt.createNewFile()
        eqpDir.mkdir()
        etcTxt.createNewFile()
        insTxt.createNewFile()
        petTxt.createNewFile()
        mapTxt.createNewFile()
        mobTxt.createNewFile()
        skillTxt.createNewFile()
        npcTxt.createNewFile()
        print("提取 Cash.img 數據...")
        writer = PrintWriter(FileOutputStream(cashTxt))
        for child in cash.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            name = ""
            desc = "(無描述)"
            if nameData is not None:
                name = nameData.getData()
            if descData is not None:
                desc = descData.getData()
            writer.println(child.getName() + " - " + name + " - " + desc)
        writer.flush()
        writer.close()
        print("Cash.img 提取完成.")
        print("提取 Consume.img 數據...")
        writer = PrintWriter(FileOutputStream(useTxt))
        for child in consume.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            name = ""
            desc = "(無描述)"
            if nameData is not None:
                name = nameData.getData()
            if descData is not None:
                desc = descData.getData()
            writer.println(child.getName() + " - " + name + " - " + desc)
        writer.flush()
        writer.close()
        print("Consume.img 提取完成.")
        print("提取 Eqp.img 數據...")
        for child in eqp.getChildren():
            print("提取 " + child.getName() + " 數據...")
            eqpFile = File(output + "/Equip/" + child.getName() + ".txt")
            eqpFile.createNewFile()
            eqpWriter = PrintWriter(FileOutputStream(eqpFile))
            for child2 in child.getChildren():
                nameData2 = child2.getChildByPath("name")
                descData2 = child2.getChildByPath("desc")
                name2 = ""
                desc2 = "(無描述)"
                if nameData2 is not None:
                    name2 = nameData2.getData()
                if descData2 is not None:
                    desc2 = descData2.getData()
                eqpWriter.println(child2.getName() + " - " + name2 + " - " + desc2)
            eqpWriter.flush()
            eqpWriter.close()
            print(child.getName() + " 提取完成.")
        print("Eqp.img 提取完成.")
        print("提取 Etc.img 數據...")
        writer = PrintWriter(FileOutputStream(etcTxt))
        for child in etc.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            name = ""
            desc = "(無描述)"
            if nameData is not None:
                name = nameData.getData()
            if descData is not None:
                desc = descData.getData()
            writer.println(child.getName() + " - " + name + " - " + desc)
        writer.flush()
        writer.close()
        print("Etc.img 提取完成.")
        print("提取 Ins.img 數據...")
        writer = PrintWriter(FileOutputStream(insTxt))
        for child in ins.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            name = ""
            desc = "(無描述)"
            if nameData is not None:
                name = nameData.getData()
            if descData is not None:
                desc = descData.getData()
            writer.println(child.getName() + " - " + name + " - " + desc)
        writer.flush()
        writer.close()
        print("Ins.img 提取完成.")
        print("提取 Pet.img 數據...")
        writer = PrintWriter(FileOutputStream(petTxt))
        for child in pet.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            name = ""
            desc = "(無描述)"
            if nameData is not None:
                name = nameData.getData()
            if descData is not None:
                desc = descData.getData()
            writer.println(child.getName() + " - " + name + " - " + desc)
        writer.flush()
        writer.close()
        print("Pet.img 提取完成.")
        print("提取 Map.img 數據...")
        writer = PrintWriter(FileOutputStream(mapTxt))
        for child in map.getChildren():
            writer.println(child.getName())
            writer.println()
            for child3 in child.getChildren():
                streetData = child3.getChildByPath("streetName")
                mapData = child3.getChildByPath("mapName")
                streetName = "(無數據名)"
                mapName = "(无地图名)"
                if streetData is not None:
                    streetName = streetData.getData()
                if mapData is not None:
                    mapName = mapData.getData()
                writer.println(child3.getName() + " - " + streetName + " - " + mapName)
            writer.println()
        writer.flush()
        writer.close()
        print("Map.img 提取完成.")
        print("提取 Mob.img 數據...")
        writer = PrintWriter(FileOutputStream(mobTxt))
        for child in mob.getChildren():
            nameData = child.getChildByPath("name")
            name3 = ""
            if nameData is not None:
                name3 = nameData.getData()
            writer.println(child.getName() + " - " + name3)
        writer.flush()
        writer.close()
        print("Mob.img 提取完成.")
        print("提取 Skill.img 數據...")
        writer = PrintWriter(FileOutputStream(skillTxt))
        for child in skill.getChildren():
            nameData = child.getChildByPath("name")
            descData = child.getChildByPath("desc")
            bookData = child.getChildByPath("bookName")
            name4 = ""
            desc3 = ""
            if nameData is not None:
                name4 = nameData.getData()
            if descData is not None:
                desc3 = descData.getData()
            if bookData is None:
                writer.println(child.getName() + " - " + name4 + " - " + desc3)
        writer.flush()
        writer.close()
        print("Skill.img 提取完成.")
        print("提取 Npc.img 數據...")
        writer = PrintWriter(FileOutputStream(npcTxt))
        for child in npc.getChildren():
            nameData = child.getChildByPath("name")
            name3 = ""
            if nameData is not None:
                name3 = nameData.getData()
            writer.println(child.getName() + " - " + name3)
        writer.flush()
        writer.close()
        print("Npc.img 提取完成.")

