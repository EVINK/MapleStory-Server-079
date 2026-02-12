"""
ConvertOpcodes - Converted from Java source
Original: tools/wztosql/ConvertOpcodes.java
Package: tools.wztosql
"""

from typing import List
from typing import Optional, Any
import os

# Internal module imports
# from tools import *  # TODO: import specific classes
# from handling import *  # TODO: import specific classes


class ConvertOpcodes:
    """
    Class ConvertOpcodes
    """


    def main(self, args: list) -> None:
        sb = ""
        input = Scanner(System.in)
        print("欢迎来到操作代码转换器。  \r\n你的操作码将被转换成十六进制和十进制数字（无论你选择），  \r\n它们将被保存在一个新的文本文件中。 .")
        print("你想转换的操作码是什么？十六进制还是十进制？ ")
        decimal = "十进制的" == (input.next().lower())
        sb.append("RecvOps.txt 转换为十六进制数据:").append("\r\n")
        for recv in RecvPacketOpcode.values():
            sb.append("\r\n").append(recv.name()).append(" = ").append(decimal ? Short.valueOf(recv.getValue()) : HexTool.getOpcodeToString(recv.getValue()))
        print("\r\n请输入文本文件名文件将被保存到新的操作码：  \r\n")
        out = FileOutputStream(input.next() + ".txt", False)
        sb.append("SendOps.txt 转换为十六进制数据:").append("\r\n")
        for send in SendPacketOpcode.values():
            sb.append("\r\n").append(send.name()).append(" = ").append(decimal ? Short.valueOf(send.getValue()) : HexTool.getOpcodeToString(send.getValue()))
        print("\r\n\r\n")
        out.write(sb.encode("utf-8"))

