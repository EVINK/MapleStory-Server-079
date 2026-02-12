"""
main.py - Python 3.12 entrypoint
- Loads configuration from Java-style .properties files under ./config or env vars
- Prepares DB connection settings (PyMySQL) via environment
- Placeholder to start the converted MapleStory server logic
"""
import os
import sys
from pathlib import Path
from typing import Dict

# Ensure src/ is importable
CUR_DIR = Path(__file__).resolve().parent
SRC_DIR = CUR_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def load_properties(path: Path) -> Dict[str, str]:
    """
    Minimal .properties parser (key=value), ignores # and // comments.
    """
    props: Dict[str, str] = {}
    if not path.exists():
        return props
    for raw in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            props[k.strip()] = v.strip()
    return props


def build_db_config() -> Dict[str, str]:
    # Prefer env vars, fallback to ./config/db.properties if present
    cfg = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': os.getenv('DB_NAME', 'maple'),
        'user': os.getenv('DB_USER', 'maple'),
        'password': os.getenv('DB_PASSWORD', 'maple'),
    }
    props = load_properties(CUR_DIR / 'config' / 'db.properties')
    cfg['host'] = os.getenv('DB_HOST', props.get('host', cfg['host']))
    if 'port' in props and not os.getenv('DB_PORT'):
        try:
            cfg['port'] = int(props['port'])
        except ValueError:
            pass
    cfg['database'] = os.getenv('DB_NAME', props.get('database', cfg['database']))
    cfg['user'] = os.getenv('DB_USER', props.get('username', cfg['user']))
    cfg['password'] = os.getenv('DB_PASSWORD', props.get('password', cfg['password']))
    return cfg


def main():
    logger.info('Starting MapleStory Python server (placeholder)')
    logger.info('Python version: %s', sys.version)

    db_cfg = build_db_config()
    logger.info('DB config: host=%s port=%s db=%s user=%s', db_cfg['host'], db_cfg['port'], db_cfg['database'], db_cfg['user'])

    # TODO: Wire up converted server startup sequence here.
    # For now, just print a notice and exit cleanly.
    logger.info('Converted code present under ./src (placeholders with comments).')
    logger.info('Dockerized with docker-compose (service: app + db).')


if __name__ == '__main__':
    main()
