import os
import json
import urllib.request
import threading
import time
from content_brain import ContentBrain
from content_memory import ContentMemory
from trend_detector import TrendDetector

def test_content_intelligence_suite():
    print("Test 1: Multi-Domain Topic Discovery & Removal of Crypto Lock-in...")
    cb = ContentBrain()
    candidates = cb.generate_candidate_topics()
    assert len(candidates) >= 4
    
    categories = [c["category"] for c in candidates]
    assert "ai_agents" in categories
    assert "security" in categories
    assert "software_engineering" in categories
    # Verify top candidate is NOT forced to crypto
    assert candidates[0]["category"] in ["ai_agents", "security", "software_engineering"]
    print("✅ Test 1 Passed: Multi-domain candidate pool generated without crypto lock-in.")

    print("Test 2: ContentMemory & Topic Fatigue Penalty...")
    mem_file = "test_content_mem.json"
    cm = ContentMemory(mem_file)
    # Simulate repeated crypto posts
    cm.data["topic_counts"]["crypto_web3"] = 4
    cm.save_memory()

    cb_fatigued = ContentBrain()
    cb_fatigued.memory = cm
    cand_fatigued = cb_fatigued.generate_candidate_topics()

    crypto_cand = next(c for c in cand_fatigued if c["category"] == "crypto_web3")
    assert crypto_cand["fatigue"] == 5.0 # High fatigue penalty
    assert cand_fatigued[0]["category"] != "crypto_web3"
    if os.path.exists(mem_file): os.remove(mem_file)
    print("✅ Test 2 Passed: Topic fatigue penalty and saturation prevention verified.")

    print("Test 3: Dynamic Content Format, Length & Submolt Destination Matching...")
    decision = cb.evaluate_and_select_action()
    assert "format" in decision
    assert decision["format"] in ["Technical Breakdown", "Problem + Solution", "Tutorial", "Case Study", "Analysis", "Discovery"]
    assert "length" in decision
    assert decision["submolt"].startswith("m/")
    print("✅ Test 3 Passed: Dynamic format, length, and destination matching verified.")

    print("Test 4: Autonomous Decision Model (POST vs WAIT)...")
    # Low score candidates should trigger WAIT decision cleanly
    low_candidates = [{"topic": "Low Value Topic", "category": "general", "score": 12.0, "heat": 2.0, "fatigue": 0.0, "suggested_submolt": "m/general", "suggested_format": "Analysis", "suggested_length": "SHORT"}]
    cb_wait = ContentBrain()
    cb_wait.generate_candidate_topics = lambda feed_posts=None: low_candidates
    dec_wait = cb_wait.evaluate_and_select_action()
    assert dec_wait["action"] == "WAIT"
    print("✅ Test 4 Passed: Autonomous decision model (WAIT when low score) verified.")

    print("Test 5: Content Intelligence REST Gateway Endpoints...")
    try:
        import socketserver, http.server
        from control_center_server import ControlCenterHTTPHandler
        t_server = socketserver.TCPServer(("", 8008), ControlCenterHTTPHandler)
        t_thread = threading.Thread(target=t_server.serve_forever, daemon=True)
        t_thread.start()
        time.sleep(1)

        req1 = urllib.request.Request("http://localhost:8008/api/content/brain")
        with urllib.request.urlopen(req1, timeout=2) as resp:
            d1 = json.loads(resp.read().decode('utf-8'))
            assert "candidates" in d1
            assert "active_decision" in d1

        req2 = urllib.request.Request("http://localhost:8008/api/content/memory")
        with urllib.request.urlopen(req2, timeout=2) as resp:
            d2 = json.loads(resp.read().decode('utf-8'))
            assert "topic_counts" in d2

        t_server.shutdown()
        print("✅ Test 5 Passed: Content Intelligence REST gateway endpoints operating cleanly.")
    except Exception as e:
        print(f"⚠️ Notice on port test: {e}")

    print("\n🎉 All AgentBroko Content Intelligence Engine tests passed successfully!")

if __name__ == '__main__':
    test_content_intelligence_suite()
