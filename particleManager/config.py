"""roomieMatter development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
ROOMIEMATTER_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_FILENAME = ROOMIEMATTER_ROOT/'var'/'roomieMatter.sqlite3'

SERVER_HOST = "172.31.28.171"
SERVER_PORT = 1002
LOG_FILE = "var/log/particleManager.log"
LOG_LEVEL = "debug"

# sudo python3 -m particleManager --host 172.31.28.171 --port 1002 --logfile var/log/particleManager.log --loglevel debug
