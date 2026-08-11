import os
from audience_engine import AudienceEngine
from content_performance import ContentPerformanceEngine
from topic_intelligence import TopicIntelligence
from content_factory import ContentFactory
from cta_engine import CTAEngine
from trust_engine import TrustEngine, CorrectionEngine
from content_experiment_engine import ContentExperimentEngine
from agentbroko_dashboard import generate_v6_growth_report

def test_v6_suite():
    print("Testing AudienceEngine Metrics...")
    aud = AudienceEngine("test_aud.json")
    aud.record_interaction("readers", 10)
    assert aud.data["summary"]["readers"] > 10
    print("✅ Audience Engine tracking verified.")

    print("Testing ContentPerformanceEngine Scoring...")
    c_perf = ContentPerformanceEngine("test_cperf.json")
    item = c_perf.record_content_metrics("Test Topic", "level_1", "Moltbook", 200, 20, 5)
    assert item["content_score"] >= 0 and item["content_score"] <= 100
    print(f"✅ Content Score verified: {item['content_score']}/100")

    print("Testing TopicIntelligence Categories...")
    topics = TopicIntelligence("test_topics.json")
    top_2 = topics.get_highest_demand_topics(2)
    assert len(top_2) == 2
    assert "demand_score" in top_2[0]
    print("✅ Topic Intelligence category scoring verified.")

    print("Testing ContentFactory Asset Repurposing...")
    assets = ContentFactory.repurpose_topic("Test Concept", "Test explanation of concept.")
    assert "beginner_explanation" in assets
    assert "faq_asset" in assets
    assert "dev_tutorial" in assets
    print("✅ Content Factory multi-format repurposing verified.")

    print("Testing CTAEngine Rules...")
    sec_cta = CTAEngine.get_contextual_cta("Wallet Security", "educational")
    assert "Security Reminder:" in sec_cta
    assert "http" not in sec_cta # Zero URLs in security CTAs

    ex_cta = CTAEngine.get_contextual_cta("Exchange Comparison", "educational")
    assert "http" not in ex_cta # Zero referral URLs in Moltbook CTAs
    print("✅ Context-aware CTA generation rules verified (NO affiliate links policy enforced).")

    print("Testing TrustEngine & CorrectionEngine...")
    score = TrustEngine.calculate_trust_score(sources_provided=True, disclosure_included=True)
    assert score >= 85.0
    corr = CorrectionEngine("test_corr.json")
    item_corr = corr.log_correction("cnt_001", "Old claim", "New corrected claim", "Official Docs", "Fixed typo")
    assert item_corr["content_id"] == "cnt_001"
    print("✅ Trust Engine & Correction Logging verified.")

    print("Testing ContentExperimentEngine A/B Testing...")
    exp = ContentExperimentEngine("test_ab.json")
    assert len(exp.experiments) >= 2
    print("✅ A/B Testing framework verified.")

    print("Testing V6 Weekly Growth Report...")
    report = generate_v6_growth_report()
    assert "AgentBroko" in report
    print("✅ V6 Weekly Growth Report verified.")

    # Cleanup
    for tf in ["test_aud.json", "test_cperf.json", "test_topics.json", "test_corr.json", "test_ab.json"]:
        if os.path.exists(tf):
            os.remove(tf)

    print("\n🎉 All AgentBroko V6 Growth & Monetization OS tests passed successfully!")

if __name__ == '__main__':
    test_v6_suite()
