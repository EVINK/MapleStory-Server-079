"""
PortalScriptManager - Converted from Java source
Original: scripting/PortalScriptManager.java
Package: scripting
"""

from io import IOBase
from io import TextIOWrapper
from pathlib import Path
from typing import Dict
from typing import Optional, Any
import os
import sys
import tkinter

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes


class PortalScriptManager:
    """
    Class PortalScriptManager
    """

    def __init__(self):
        self.scripts = None
        self.scripts = {}

    # Static initializer
    # instance = PortalScriptManager()
    # sef = ScriptEngineManager().getEngineByName("javascript").getFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getPortalScript(self, c: Any, scriptName: str) -> Any:
        if (scriptName in self.scripts):
            self.scripts.clear()
            return self.scripts.get(scriptName)
        scriptsPath = os.environ.get("scripts_path")
        scriptFile = File(scriptsPath+"scripts"+File.separator+"portal"+File.separator + scriptName + ".js")
        if not scriptFile.exists():
            return None
        fr = None
        portal = PortalScriptManager.sef.getScriptEngine()
        try:
            fr = FileInputStream(scriptFile)
            bf = BufferedReader(InputStreamReader(fr, EncodingDetect.getJavaEncode(scriptFile)))
            compiled = (portal).compile(bf)
            compiled.eval()
        except Exception as e:
            print("Error executing Portalscript: " + scriptName + ":" + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Error executing Portal script. (" + scriptName + ") " + e)
            if fr is not None:
                try:
                    fr.close()
                except IOError as e2:
                    print("ERROR CLOSING" + e2)
        finally:
            if fr is not None:
                try:
                    fr.close()
                except IOError as e3:
                    print("ERROR CLOSING" + e3)
        script = (portal).getInterface(PortalScript.class)
        self.scripts.put(scriptName, script)
        return script

    def executePortalScript(self, portal: Any, c: Any) -> None:
        script = self.getPortalScript(c, portal.getScriptName())
        if c.getPlayer().isGM():
            c.getPlayer().dropMessage("[系统提示]您已经建立与PortalScript:[" + portal.getScriptName() + ".js]的对话。")
        if script is not None:
            try:
                script.enter(PortalPlayerInteraction(c, portal))
            except Exception as e:
                print("Error entering Portalscript: " + portal.getScriptName() + ":" + e)

    def clearScripts(self) -> None:
        self.scripts.clear()

