import time
import logging
import logging.handlers
import os
import sys
import threading
from agent_runtime import AgentRuntime
from control_center_server import ControlCenterServer, AgentCoinHealthServer
from startup_diagnostics import StartupDiagnostics

# ── Load .env into environment variables ──────────────────────────────────────
def _load_env_file(env_path=".env"):
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

_load_env_file()

# ── Logging Setup ─────────────────────────────────────────────────────────────
# RotatingFileHandler: 5 MB max per file, keep 3 backups
_log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
_log_file_handler = logging.handlers.RotatingFileHandler(
    'agentbroko.log', maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8'
)
_log_file_handler.setFormatter(_log_formatter)

# Also stream to stdout so the terminal shows live output
_log_stream_handler = logging.StreamHandler(sys.stdout)
_log_stream_handler.setFormatter(_log_formatter)

# Flush after every write so the file is always up-to-date in the editor
class FlushingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

_flush_handler = FlushingRotatingFileHandler(
    'agentbroko.log', maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8'
)
_flush_handler.setFormatter(_log_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
# Remove any pre-existing handlers to avoid duplicate output
root_logger.handlers.clear()
root_logger.addHandler(_flush_handler)
root_logger.addHandler(_log_stream_handler)

# ──────────────────────────────────────────────────────────────────────────────

def main():
    logging.info("=" * 60)
    logging.info("AgentBroko Master OS — STARTING UP")
    logging.info(f"PID: {os.getpid()} | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 60)

    try:
        diag = StartupDiagnostics.run_diagnostics()
        print(diag)
        logging.info(f"[DIAGNOSTICS] {diag}")
    except Exception as e:
        logging.warning(f"[DIAGNOSTICS] Startup diagnostics error: {e}")

    # 1. Start Real-Time Command Center Web UI Server on port 8000
    try:
        ui_server = ControlCenterServer(8000)
        ui_thread = threading.Thread(target=ui_server.start, daemon=True)
        ui_thread.start()
        logging.info("[COMMAND CENTER UI] Server started live on http://localhost:8000")
        print("🌐 [COMMAND CENTER UI] Server started live on http://localhost:8000")
    except Exception as e:
        logging.warning(f"[COMMAND CENTER UI] Could not start Web UI server: {e}")
        print(f"⚠️ [COMMAND CENTER UI] Notice: Could not start Web UI server: {e}")

    # 2. Bring up AgentCoin compatibility health endpoint expected by the dashboard on port 8010.
    try:
        coin_server = AgentCoinHealthServer(8010)
        coin_thread = threading.Thread(target=coin_server.start, daemon=True)
        coin_thread.start()
        logging.info("[AGENTCOIN HEALTH] Server started live on http://localhost:8010")
        print("🌐 [AGENTCOIN HEALTH] Server started live on http://localhost:8010")
    except Exception as e:
        logging.warning(f"[AGENTCOIN HEALTH] Could not start AgentCoin health server: {e}")
        print(f"⚠️ [AGENTCOIN HEALTH] Notice: Could not start AgentCoin health server: {e}")

    # 3. Launch Authoritative Master AgentRuntime
    logging.info("[RUNNER] Launching Master AgentRuntime — unified autonomous loop active")
    runtime = AgentRuntime()
    runtime.start_loop()

if __name__ == '__main__':
    main()
