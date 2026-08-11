import time
import logging
import os
import sys
import threading
from agent_runtime import AgentRuntime
from control_center_server import ControlCenterServer
from startup_diagnostics import StartupDiagnostics

logging.basicConfig(
    filename='agentbroko.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def main():
    print(StartupDiagnostics.run_diagnostics())

    # 1. Start Real-Time Command Center Web UI Server on port 8000
    try:
        ui_server = ControlCenterServer(8000)
        ui_thread = threading.Thread(target=ui_server.start, daemon=True)
        ui_thread.start()
        print("🌐 [COMMAND CENTER UI] Server started live on http://localhost:8000")
    except Exception as e:
        print(f"⚠️ [COMMAND CENTER UI] Notice: Could not start Web UI server: {e}")

    # 2. Launch Authoritative Master AgentRuntime
    runtime = AgentRuntime()
    runtime.start_loop()

if __name__ == '__main__':
    main()
