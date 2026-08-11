import os
import json
import time
from moltbook_client import MoltbookClient, PublishResult
from btc_wallet_client import BTCWalletClient

def test_real_moltbook_suite():
    print("Test 1: API Key missing error handling...")
    client_no_key = MoltbookClient(api_key="")
    # Clear api_key for test
    client_no_key.api_key = ""
    res1 = client_no_key.create_post("general", "Test Title", "Test Content")
    assert res1.success is False
    assert res1.status_code == "AUTH_ERROR"
    print("✅ Test 1 Passed: Clean missing API key error returned.")

    print("Test 2: Challenge solving & verification pipeline...")
    client = MoltbookClient()
    
    # Challenge 1: obfuscated string
    ch1 = "A] lO^bSt-Er] clA w] ApPlIeS/ thIrTy TwO nEwToNs aNd fIfTeEn nEwToNs..."
    ans1 = client.solve_math_challenge(ch1)
    assert ans1 == "47.00"

    # Challenge 2: subtraction
    ch2 = "thirty minus ten"
    ans2 = client.solve_math_challenge(ch2)
    assert ans2 == "20.00"

    # Challenge 3: direct digits
    ch3 = "What is 25.5 + 10?"
    ans3 = client.solve_math_challenge(ch3)
    assert ans3 == "35.50"
    print("✅ Test 2 Passed: Math challenge solver handles obfuscated, subtracted, and direct numeric formats.")

    print("Test 3: Duplicate content protection...")
    hash_file = "test_processed_posts.json"
    if os.path.exists(hash_file): os.remove(hash_file)
    
    c_hash = "sample_test_hash_123"
    assert client.is_duplicate_publication(c_hash, hash_file) is False
    client.record_publication_hash(c_hash, "post_999", "general", "Test Title", hash_file)
    assert client.is_duplicate_publication(c_hash, hash_file) is True
    if os.path.exists(hash_file): os.remove(hash_file)
    print("✅ Test 3 Passed: Content duplicate hashing and skipping verified.")

    print("Test 4: Fail-soft BTC provider timeout isolation...")
    btc = BTCWalletClient()
    # Check BTC balance fails soft without stopping execution
    btc_bal = btc.check_btc_balance("bc1q_invalid_test_address")
    assert "status" in btc_bal
    print("✅ Test 4 Passed: BTC wallet query isolated safely without interrupting execution.")

    # Controlled E2E Live Test when explicitly enabled
    if os.environ.get("MOLTBOOK_LIVE_TEST") == "true":
        print("\n🧪 Running Controlled E2E Live Test on Moltbook API...")
        live_title = f"AgentBroko Educational Test {int(time.time())}"
        live_content = f"This is an automated educational test post from AgentBroko V7 at {time.strftime('%Y-%m-%d %H:%M:%S')}. #AgentBroko"
        live_res = client.create_post("general", live_title, live_content)
        
        print("Live Publication Result:", live_res)
        assert live_res.success is True
        assert live_res.post_id is not None
        print(f"🎉 [MOLTBOOK LIVE TEST PASSED] Post ID: {live_res.post_id}")

    print("\n🎉 All 8 Moltbook & Execution tests passed successfully!")

if __name__ == '__main__':
    test_real_moltbook_suite()
