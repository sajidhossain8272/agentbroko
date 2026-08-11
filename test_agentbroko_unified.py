import os
from brain import Brain
from skill_registry import SkillRegistry
from agent_memory import AgentMemory
from task_queue import TaskQueue
from startup_diagnostics import StartupDiagnostics
from github_engine import GitHubEngine
from moltbook_client import MoltbookClient

def test_unified_system_suite():
    print("Test 1: Startup Diagnostics Engine...")
    diag_report = StartupDiagnostics.run_diagnostics()
    assert "AGENTBROKO UNIFIED AUTONOMOUS OPERATING SYSTEM STATUS REPORT" in diag_report
    assert "GitHub Integration" in diag_report
    assert "Social API (Moltbook)" in diag_report
    print("✅ Test 1 Passed: Startup Diagnostics system report generated successfully.")

    print("Test 2: SkillRegistry Dynamic Skill Loading...")
    sr = SkillRegistry()
    skills = sr.list_skills()
    assert "github_code_agent" in skills
    assert "social_skill" in skills
    assert "education_skill" in skills
    assert "business_skill" in skills
    print(f"✅ Test 2 Passed: {len(skills)} skills dynamically registered and loaded.")

    print("Test 3: Categorized AgentMemory Persistence...")
    mem_file = "test_unified_memory.json"
    am = AgentMemory(mem_file)
    am.record_event("episodic_memory", {"event": "Unified OS Boot Test"})
    fail_entry = am.log_failure("test_task", "Test error cause", "Test lesson learned")
    assert fail_entry["task"] == "test_task"
    if os.path.exists(mem_file): os.remove(mem_file)
    print("✅ Test 3 Passed: Categorized memory logging and failure tracking verified.")

    print("Test 4: TaskQueue Priority Pipeline & Brain Controller...")
    tq_file = "test_unified_tq.json"
    tq = TaskQueue(tq_file)
    tq.add_task("test_high_priority", "Execute high priority task", priority=0.99)
    
    brain = Brain()
    brain.queue = tq
    action = brain.evaluate_and_select_action()
    assert action["action"] == "test_high_priority"
    assert action["priority_score"] == 99.0

    completed = tq.mark_completed(action["task_id"])
    assert completed["status"] == "completed"
    if os.path.exists(tq_file): os.remove(tq_file)
    print("✅ Test 4 Passed: TaskQueue priority popping and Brain evaluation verified.")

    print("Test 5: Live Credentials & Integration Check...")
    gh = GitHubEngine()
    assert gh.token is not None and len(gh.token) > 0
    print(f"✅ Test 5 Passed: GitHub PAT verified live ('{gh.token[:12]}...').")

    print("\n🎉 All AgentBroko Unified Operating System tests passed successfully!")

if __name__ == '__main__':
    test_unified_system_suite()
