import os
import json
import time
from autonomous_scheduler import AutonomousScheduler
from decision_journal import DecisionJournal
from btc_wallet_client import BTCWalletClient

def test_v4_suite():
    print("Testing AutonomousScheduler Singleton Lock...")
    sched = AutonomousScheduler("test_agentbroko.lock", "test_heartbeat.json", "test_agent_state.json")
    assert sched.pid == os.getpid()
    assert os.path.exists("test_agentbroko.lock")
    print(f"✅ Singleton Process Lock acquired for PID: {sched.pid}")

    print("Testing Multi-Speed Timer Configuration...")
    assert sched.RAPID_MONITOR == 60
    assert sched.BUSINESS_CYCLE == 300
    assert sched.DEEP_RESEARCH == 1800
    assert sched.STRATEGIC_REVIEW == 7200
    print("✅ Multi-speed intervals verified (Rapid: 60s, Business: 300s, Research: 1800s, Strategy: 7200s).")

    print("Testing Heartbeat & State Updates...")
    sched.update_heartbeat(last_cycle_type="business")
    assert os.path.exists("test_heartbeat.json")
    with open("test_heartbeat.json") as f:
        hb = json.load(f)
        assert hb["status"] == "running"
        assert hb["pid"] == os.getpid()
    print("✅ Heartbeat updates verified.")

    sched.set_agent_state("Goal", "Task", "Opp", "Reason", "Expected")
    assert os.path.exists("test_agent_state.json")
    print("✅ Agent State updates verified.")

    print("Testing DecisionJournal...")
    journal = DecisionJournal("test_journal.json")
    entry = journal.log_decision("Test Decision", ["Alt1"], "Alt1", "Good reason", 85.0)
    assert entry["id"].startswith("dec_")
    print("✅ Decision Journal logging verified.")

    print("Testing Fail-Soft BTC Wallet Client...")
    btc = BTCWalletClient()
    bal = btc.check_btc_balance()
    assert "confirmed_btc" in bal
    print(f"✅ Fail-soft BTC check output verified (Address: {btc.primary_address}).")

    sched.release_lock()
    for tf in ["test_agentbroko.lock", "test_heartbeat.json", "test_agent_state.json", "test_journal.json"]:
        if os.path.exists(tf):
            os.remove(tf)

    print("\n🎉 All AgentBroko V4 Intelligent Autonomous Scheduler tests passed successfully!")

if __name__ == '__main__':
    test_v4_suite()
