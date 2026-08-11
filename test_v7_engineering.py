import os
from security_engine import SecurityEngine
from repository_map import RepositoryMap
from engineering_memory import EngineeringMemory
from github_engine import GitHubEngine
from agentbroko_dashboard import generate_v7_engineering_report

def test_v7_suite():
    print("Testing SecurityEngine Secret Leakage & Vulnerability Detection...")
    # Safe code
    safe_code = "def add(a, b):\n    return a + b"
    sec_safe = SecurityEngine.scan_code(safe_code, "test.py")
    assert sec_safe["is_safe"] is True

    # Code containing secret leak
    unsafe_code = "EVM_PRIVATE_KEY = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'"
    sec_leak = SecurityEngine.scan_code(unsafe_code, "config.py")
    assert sec_leak["is_safe"] is False
    assert sec_leak["findings"][0]["type"] == "SECRET_LEAK"
    print("✅ SecurityEngine secret leak detection verified.")

    print("Testing RepositoryMap...")
    rmap = RepositoryMap("test_repo_map.json")
    assert rmap.data["repository"] == "agentbroko/agentbroko"
    updated = rmap.update_map(open_issues=5, ci_status="SUCCESS")
    assert updated["open_issues"] == 5
    print("✅ RepositoryMap architecture mapping verified.")

    print("Testing EngineeringMemory...")
    emem = EngineeringMemory("test_eng_mem.json")
    evt = emem.log_engineering_event("Test Feature", "Added test files", "PASSED", "Unit tests work")
    assert evt["id"].startswith("eng_")
    print("✅ EngineeringMemory event logging verified.")

    print("Testing GitHubEngine Issue & PR Payload Generation...")
    gh = GitHubEngine()
    issue = gh.create_issue("Test Bug", "Test problem", "Test logs", "Test fix", "P2")
    assert issue["state"] == "open"

    # PR payload with safe code
    pr_result = gh.create_pull_request("feature/test", "Add test feature", "Modified test.py", "Improves tests", "100% pass", safe_code)
    assert pr_result["success"] is True

    # PR payload with unsafe code (must fail security scan)
    pr_unsafe = gh.create_pull_request("feature/leak", "Add secret key", "Modified config.py", "Exposes key", "100% pass", unsafe_code)
    assert pr_unsafe["success"] is False
    assert "Security check failed" in pr_unsafe["error"]
    print("✅ GitHubEngine security-scanned PR payload generation verified.")

    print("Testing V7 Daily Engineering Report...")
    report = generate_v7_engineering_report()
    assert "AgentBroko V7 Daily Engineering & Software Factory Report" in report
    assert "Repository Overview" in report
    print("✅ V7 Daily Engineering Report verified.")

    # Cleanup
    for tf in ["test_repo_map.json", "test_eng_mem.json"]:
        if os.path.exists(tf):
            os.remove(tf)

    print("\n🎉 All AgentBroko V7 Autonomous GitHub Engineer tests passed successfully!")

if __name__ == '__main__':
    test_v7_suite()
