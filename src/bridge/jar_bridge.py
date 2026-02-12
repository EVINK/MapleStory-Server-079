"""
jar_bridge.py - Simple bridge to load and call Java classes from a JAR using JPype.
- Falls back to subprocess execution for `java -jar` if needed.
- Configure the JAR path via env JAR_PATH or default to ./bin/maple.jar
"""
import os
from pathlib import Path
from typing import List, Optional
import subprocess

try:
    import jpype
    import jpype.imports  # noqa: F401
except Exception:
    jpype = None

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JAR = ROOT / 'bin' / 'maple.jar'


def start_jvm(jar_path: Optional[Path] = None):
    """Start JVM with given jar on classpath if JPype is available and not started."""
    if jpype is None:
        return False
    if jpype.isJVMStarted():
        return True
    jar = Path(os.getenv('JAR_PATH', str(jar_path or DEFAULT_JAR)))
    if not jar.exists():
        return False
    cp = str(jar)
    try:
        jpype.startJVM(classpath=[cp])
        return True
    except Exception:
        return False


def call_main_with_subprocess(args: List[str]) -> int:
    jar = os.getenv('JAR_PATH', str(DEFAULT_JAR))
    cmd = ['java', '-jar', jar] + args
    return subprocess.call(cmd)


def call_java_static(class_name: str, method: str, *args):
    """Call a static Java method via JPype if available; else raise RuntimeError."""
    if jpype is None:
        raise RuntimeError('JPype not installed in environment')
    if not jpype.isJVMStarted():
        ok = start_jvm()
        if not ok:
            raise RuntimeError('Failed to start JVM for jar bridge')
    parts = class_name.split('.')
    mod = __import__('.'.join(parts[:-1])) if len(parts) > 1 else None
    cls = getattr(mod, parts[-1]) if mod else jpype.JClass(class_name)
    return getattr(cls, method)(*args)
