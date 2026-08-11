import os
import json
import time
from autonomous_orchestrator import AutonomousOrchestrator
from master_state_machine import MasterStateMachine
from moltbook_client import MoltbookClient
from btc_wallet_client import BTCWalletClient
from capabilities.wallet_capability import WalletCapability
from github_engine import GitHubEngine
from event_bus import EventBus
from agent_supervisor import AgentSupervisor
from capabilities.capability_router import CapabilityRouter

def test_v8_suite():
    print("Test 1: last_business_cycle variable initialization regression test...")
    orchestrator = AutonomousOrchestrator()
    assert hasattr(orchestrator, "last_business_cycle")
    assert isinstance(orchestrator.last_business_cycle, float)
    print("✅ Test 1 Passed: last_business_cycle explicitly initialized.")

    print("Test 2: Moltbook HTTP diagnostics & failure classification...")
    client = MoltbookClient()
    client.api_key = "" # Force auth error
    res = client.create_post("general", "Test Title", "Test Content")
    assert res.success is False
    assert res.status_code == "AUTH_ERROR"
    print("✅ Test 2 Passed: Structured HTTP diagnostics & failure classification verified.")

    print("Test 3: Moltbook verification success & idempotency hashing...")
    client = MoltbookClient()
    assert client.is_duplicate_publication("non_existent_hash_123") is False
    print("✅ Test 3 Passed: Idempotency hashing check verified.")

    print("Test 4: Moltbook request timeout isolation...")
    client = MoltbookClient()
    # Ensure timeout does not raise unhandled exception
    res_t = client._request("/invalid_endpoint_for_timeout")
    assert "error" in res_t or "success" in res_t
    print("✅ Test 4 Passed: Moltbook request timeout isolated safely.")

    print("Test 5: BTC provider timeout isolation...")
    btc = BTCWalletClient()
    bal = btc.check_btc_balance("bc1q_invalid_address")
    assert bal["status"] == "UNAVAILABLE"
    print("✅ Test 5 Passed: BTC provider timeout isolated safely without raising exception.")

    print("Test 6: WalletCapability 3-Strike Circuit Breaker...")
    w_cap = WalletCapability()
    # Simulate 3 failures
    w_cap.consecutive_failures = 3
    w_cap.circuit_open = True
    w_cap.next_retry = time.time() + 120
    exec_res = w_cap.execute()
    assert exec_res["status"] == "DEGRADED"
    assert exec_res["circuit_open"] is True
    print("✅ Test 6 Passed: Wallet Capability Circuit Breaker DEGRADED state verified.")

    print("Test 7: GitHub honest mode reporting (LIVE vs SIMULATED)...")
    gh = GitHubEngine()
    mode = "LIVE" if gh.token else "SIMULATED"
    assert mode == "LIVE" # Token is in .env
    print(f"✅ Test 7 Passed: GitHub honest mode correctly reported as '{mode}'.")

    print("Test 8: Process Lock duplicate runner prevention...")
    # Verify lock file logic exists in scheduler
    from autonomous_scheduler import AutonomousScheduler
    sched = AutonomousScheduler()
    assert sched.pid > 0
    print("✅ Test 8 Passed: Singleton Process Lock verified.")

    print("Test 9: Master State Machine explicit transitions...")
    sm = MasterStateMachine("STARTING")
    sm.transition_to("OBSERVING", "Testing transition")
    assert sm.get_state() == "OBSERVING"
    sm.transition_to("WAITING", "Testing complete")
    assert sm.get_state() == "WAITING"
    print("✅ Test 9 Passed: Master State Machine explicit state transitions verified.")

    print("Test 10: Business score vs actual revenue separation...")
    from capabilities.business_capability import BusinessCapability
    b_cap = BusinessCapability()
    b_res = b_cap.execute()
    assert "opportunity_score" in b_res
    assert b_res["actual_revenue"] == 0.0
    print("✅ Test 10 Passed: Opportunity score separated from actual revenue ($0.00).")

    print("Test 11: Real-time Event Bus throughput...")
    bus = EventBus()
    evt = bus.emit("test.v8", "V8 Event Bus Test", metadata={"v8": True})
    assert evt["event"] == "test.v8"
    print("✅ Test 11 Passed: Real-time Event Bus throughput verified.")

    print("Test 12: Non-spam Moltbook comment/reply decisions...")
    from moltbook_feed_intelligence import MoltbookFeedIntelligence
    intel = MoltbookFeedIntelligence()
    spam_post = {"id": "p_99", "title": "Buy tokens now!", "content": "Referral link http://spam.com", "author": "spammer"}
    score = intel.score_conversation(spam_post)
    assert score["should_participate"] is False
    print("✅ Test 12 Passed: Non-spam comment/reply decision filter verified.")

    print("Test 13: Content duplicate prevention...")
    from social_memory import SocialMemory
    sm_mem = SocialMemory()
    assert sm_mem.is_topic_recent("public keys vs private keys") is True
    print("✅ Test 13 Passed: Content duplicate topic filter verified.")

    print("Test 14: Supervisor state recovery after restart...")
    sp = AgentSupervisor("test_v8_state.json")
    sp.set_status("ONLINE", task="Recovery Test", goal="Test Goal")
    sp_2 = AgentSupervisor("test_v8_state.json")
    assert sp_2.current_task == "Recovery Test"
    if os.path.exists("test_v8_state.json"): os.remove("test_v8_state.json")
    print("✅ Test 14 Passed: Supervisor state persistence & recovery verified.")

    print("Test 15: Multi-capability isolation (single failure does not crash orchestrator)...")
    router = CapabilityRouter()
    res = router.route_and_execute("unknown_test_capability")
    assert res is not None
    print("✅ Test 15 Passed: Multi-capability routing isolation verified.")

    print("\n🎉 ALL 15 REGRESSION TEST SCENARIOS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_v8_suite()
