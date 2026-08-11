from decision_engine import DecisionEngine
from opportunity_queue import OpportunityQueue
from experiment_lab import ExperimentLab
from business_memory import BusinessMemory
from health_monitor import HealthMonitor
from service_factory import ServiceFactory
from payment_verifier import PaymentVerifier
from agentbroko_dashboard import generate_v3_ceo_report

def test_v3_suite():
    print("Testing DecisionEngine 0-100 Scoring...")
    dec = DecisionEngine()
    decision = dec.evaluate_and_decide()
    assert decision["top_score"] >= 0 and decision["top_score"] <= 100
    print(f"✅ Decision Engine Top Score: {decision['top_score']}/100")

    print("Testing OpportunityQueue...")
    oq = OpportunityQueue("test_oq.json")
    item = oq.add_opportunity("Test Source", "Test Problem", "Test Customer", "Test Solution", 100.0)
    assert item["status"] == "new"
    updated = oq.update_status(item["id"], "validated")
    assert updated["status"] == "validated"
    print(f"✅ Opportunity Queue state transitions verified.")

    print("Testing ExperimentLab & Abandonment Logic...")
    lab = ExperimentLab("test_lab.json")
    lab.experiments[0]["consecutive_failures"] = 3
    cleaned = lab.evaluate_and_clean_experiments()
    assert cleaned >= 1
    assert lab.experiments[0]["status"] == "abandoned"
    print("✅ Experiment Lab auto-abandonment verified.")

    print("Testing HealthMonitor Anti-Loop Protection...")
    hm = HealthMonitor(max_consecutive_repeats=3)
    for _ in range(3):
        hm.record_action("test_action")
    assert hm.is_looping("test_action") is True
    print("✅ Health Monitor Anti-Loop detection verified.")

    print("Testing ServiceFactory & PaymentVerifier...")
    offer = ServiceFactory.get_service_offer("website_audit", "standard")
    assert offer["price_usd"] == 75.0
    invoice = PaymentVerifier.generate_invoice("Test Client", offer["service_name"], offer["price_usd"], "0xe74d...")
    assert invoice["status"] == "ISSUED"
    print("✅ Service Factory & Invoice Generation verified.")

    print("Testing V3 Daily CEO Report...")
    report = generate_v3_ceo_report()
    assert "AgentBroko V3 Daily CEO Report" in report
    assert "Net Profit" in report
    print("✅ V3 Daily CEO Report verified.")

    # Cleanup test files
    import os
    for f in ["test_oq.json", "test_lab.json"]:
        if os.path.exists(f):
            os.remove(f)

    print("\n🎉 All AgentBroko V3 Business Operating System tests passed successfully!")

if __name__ == '__main__':
    test_v3_suite()
