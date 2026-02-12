"""
FileoutputUtil - Converted from Java source
Original: tools/FileoutputUtil.java
Package: tools
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Any
import os

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes


class FileoutputUtil:
    """
    Class FileoutputUtil
    """

    # Static initializer
    # sdfT = SimpleDateFormat("yyyy年MM月dd日HH時mm分ss秒")
    # FileoutputUtil.fixdam_mg = "logs/魔法伤害修正.rtf"
    # FileoutputUtil.fixdam_ph = "logs/物理伤害修正.rtf"
    # FileoutputUtil.MobVac_log = "logs/Log_吸怪.txt"
    # FileoutputUtil.hack_log = "logs/Log_怀疑外挂.rtf"
    # FileoutputUtil.ban_log = "logs/Log_封号.rtf"
    # FileoutputUtil.Acc_Stuck = "logs/Log_卡账号.rtf"
    # FileoutputUtil.Login_Error = "logs/Log_登录错误.rtf"
    # FileoutputUtil.Movement_Log = "logs/移动出错.log"
    # FileoutputUtil.IP_Log = "logs/Log_账号IP.rtf"
    # FileoutputUtil.Zakum_Log = "logs/Log_扎昆.rtf"
    # FileoutputUtil.Horntail_Log = "logs/Log_暗黑龙王.rtf"
    # FileoutputUtil.Pinkbean_Log = "logs/Log_品克缤.rtf"
    # FileoutputUtil.ScriptEx_Log = "logs/Log_Script_脚本异常.rtf"
    # FileoutputUtil.PacketEx_Log = "logs/Log_Packet_封包异常.rtf"
    # sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    # sdf_ = SimpleDateFormat("yyyy-MM-dd")


    @staticmethod
    def logToFile_chr(chr: Any, file: str, msg: str) -> None:
        logToFile(file, "\r\n" + CurrentReadable_Time() + " 账号 " + chr.getClient().getAccountName() + " 名称 " + chr.getName() + " (" + chr.getId() + ") 等级 " + chr.getLevel() + " 地图 " + chr.getMapId() + " " + msg, False)

    def logToFile(self, file: str, msg: str) -> None:
        logToFile(file, msg, False)

    def logToFile_file_msg_notExists(self, file: str, msg: str, notExists: bool) -> None:
        out = None
        try:
            outputFile = File(file)
            if outputFile.exists() and outputFile.isFile() and outputFile >= 10240000:
                outputFile.renameTo(File(file[0:file.__len__(] - 4) + "_" + FileoutputUtil.sdfT.format(Calendar.getInstance().getTime()) + file[file.__len__(:] - 4, file)))
                outputFile = File(file)
            if outputFile.getParentFile() is not None:
                outputFile.getParentFile().mkdirs()
            out = FileOutputStream(file, True)
            if not (msg in out) or not notExists:
                osw = OutputStreamWriter(out, "UTF-8")
                osw.write(msg)
                osw.flush()
        except IOException as ex:
            pass
        finally:
            try:
                if out is not None:
                    out.close()
            except IOException as ex2:
                pass

    def packetLog(self, file: str, msg: str) -> None:
        notExists = False
        out = None
        try:
            outputFile = File(file)
            if outputFile.exists() and outputFile.isFile() and outputFile >= 1024000:
                outputFile.renameTo(File(file[0:file.__len__(] - 4) + "_" + FileoutputUtil.sdfT.format(Calendar.getInstance().getTime()) + file[file.__len__(:] - 4, file)))
                outputFile = File(file)
            if outputFile.getParentFile() is not None:
                outputFile.getParentFile().mkdirs()
            out = FileOutputStream(file, True)
            if not (msg in out) or not notExists:
                osw = OutputStreamWriter(out, "UTF-8")
                osw.write(msg)
                osw.flush()
        except IOException as ex:
            pass
        finally:
            try:
                if out is not None:
                    out.close()
            except IOException as ex2:
                pass

    def log(self, file: str, msg: str) -> None:
        out = None
        try:
            out = FileOutputStream(file, True)
            out.write(("\r\n------------------------ " + CurrentReadable_Time() + " ------------------------\r\n").encode("utf-8"))
            out.write(msg.encode("utf-8"))
        except IOException as ex:
            pass
        finally:
            try:
                if out is not None:
                    out.close()
            except IOException as ex2:
                pass

    def outputFileError(self, file: str, t: Any) -> None:
        out = None
        try:
            out = FileOutputStream(file, True)
            out.write(("\r\n------------------------ " + CurrentReadable_Time() + " ------------------------\r\n").encode("utf-8"))
            out.write(getString(t).encode("utf-8"))
        except IOException as ex:
            pass
        finally:
            try:
                if out is not None:
                    out.close()
            except IOException as ex2:
                pass

    def CurrentReadable_Date(self) -> str:
        return FileoutputUtil.sdf_.format(Calendar.getInstance().getTime())

    def CurrentReadable_Time(self) -> str:
        return FileoutputUtil.sdf.format(Calendar.getInstance().getTime())

    def getString(self, e: Any) -> str:
        retValue = None
        sw = None
        pw = None
        try:
            sw = StringWriter()
            pw = PrintWriter(sw)
            e.printStackTrace(pw)
            retValue = sw
        finally:
            try:
                if pw is not None:
                    pw.close()
                if sw is not None:
                    sw.close()
            except IOException as ex:
                pass
        return retValue

    def NowTime(self) -> str:
        now = Date()
        dateFormat = SimpleDateFormat("yyyy/MM/dd HH:mm:ss")
        hehe = dateFormat.format(now)
        return hehe

    def hiredMerchLog(self, file: str, msg: str) -> None:
        newfile = "logs/雇佣商人/" + file + ".txt"
        out = None
        try:
            out = FileOutputStream(newfile, True)
            out.write(("[" + CurrentReadable_Time() + "] ").encode("utf-8"))
            out.write(msg.encode("utf-8"))
            out.write("\r\n".encode("utf-8"))
        except IOException as ex:
            pass
        finally:
            try:
                if out is not None:
                    out.close()
            except IOException as ex2:
                pass

