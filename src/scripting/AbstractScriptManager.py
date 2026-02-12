"""
AbstractScriptManager - Converted from Java source
Original: scripting/AbstractScriptManager.java
Package: scripting
"""

from io import IOBase
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Any
import os
import sys
import tkinter

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class AbstractScriptManager:
    """
    Class AbstractScriptManager
    """

    # Static initializer
    # sem = ScriptEngineManager()


    @staticmethod
    def getInvocable(path: str, c: Any) -> Any:
        return self.getInvocable(path, c, False)

    def getInvocable(self, path: str, c: Any, npc: bool) -> Any:
        fr = None
        try:
            serverPath = os.environ.get("scripts_path")
            path = serverPath +"scripts"+File.separator + path
            engine = None
            if c is not None:
                engine = c.getScriptEngine(path)
            if engine is None:
                scriptFile = File(path)
                if not scriptFile.exists():
                    return None
                engine = AbstractScriptManager.sem.getEngineByName("javascript")
                if c is not None:
                    c.setScriptEngine(path, engine)
                fr = FileInputStream(scriptFile)
                bf = BufferedReader(InputStreamReader(fr, EncodingDetect.getJavaEncode(scriptFile)))
                engine.eval(bf)
            elif c is not None and npc:
                NPCScriptManager.getInstance().dispose(c)
                c.getSession().write(MaplePacketCreator.enableActions())
            return engine
        except Exception as e:
            print("Error executing script. Path: " + path + "\nException " + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing script. Path: " + path + "\nException " + e)
            return None
        finally:
            try:
                if fr is not None:
                    fr.close()
            except IOException as ex3:

