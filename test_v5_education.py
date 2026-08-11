import os
from education_engine import EducationEngine
from hype_filter import HypeFilter
from community_engine import CommunityEngine
from donation_engine import DonationEngine
from funding_ledger import FundingLedger
from agentbroko_dashboard import generate_v5_education_report

def test_v5_suite():
    # Clean up any leftover test files from previous runs
    for tf in ["test_gaps.json", "test_funding.json"]:
        if os.path.exists(tf):
            os.remove(tf)

    print("Testing EducationEngine 5-Level Curriculum...")
    for lvl in ["level_1", "level_2", "level_3", "level_4", "level_5"]:
        post = EducationEngine.generate_educational_post(lvl)
        assert len(post) > 50
        assert "Learn With AgentBroko" in post
    print("✅ 5-Level Education Curriculum generation verified.")

    print("Testing HypeFilter Detection & Sanitization...")
    hype_input = "Guaranteed profit! 100x guaranteed gains buy now risk-free secret strategy!"
    assert HypeFilter.contains_hype(hype_input) is True
    cleaned = HypeFilter.sanitize_content(hype_input)
    assert "guaranteed profit" not in cleaned.lower()
    print("✅ HypeFilter detection and sanitization verified.")

    print("Testing CommunityEngine Answer-First Principle...")
    comm = CommunityEngine("test_gaps.json")
    resp = comm.format_answer_first_response(
        question="What is gas?",
        answer_text="Gas is the execution fee paid to network validators.",
        educational_details="Gas measures computational effort on EVM chains.",
        include_exchange_rec=True
    )
    assert "Direct Answer" in resp
    assert "Educational Breakdown" in resp
    assert "Disclosure:" in resp
    print("✅ Answer-First Principle formatting verified.")

    print("Testing DonationEngine...")
    donations = DonationEngine.get_donation_info()
    assert "1K4i91pJA9RHFUVVwFumpR8sASh1sAfEYq" in donations["addresses"]["Bitcoin (BTC)"]
    assert "5Q5DTQ9bsitWXtgZXivUZZPYkwz6BsFQWJBKRGsgj5Wb" in donations["addresses"]["Solana (SOL)"]
    print("✅ Donation Engine wallet addresses verified.")

    print("Testing FundingLedger...")
    fl = FundingLedger("test_funding.json")
    fl.record_entry("affiliate_revenue", 25.0, "Binance spot referral reward")
    fl.record_entry("donation", 50.0, "Voluntary BTC donation")
    fl.record_entry("operating_cost", 5.0, "RPC node subscription")
    assert fl.data["summary"]["net_funding_usd"] == 70.0
    print("✅ Transparent Funding Ledger accounting verified.")

    print("Testing V5 Daily Education Report...")
    report = generate_v5_education_report()
    assert "AgentBroko V5 Education & Funding Report" in report
    assert "Net Funding" in report
    print("✅ V5 Daily Education Report verified.")

    # Cleanup
    for tf in ["test_gaps.json", "test_funding.json"]:
        if os.path.exists(tf):
            os.remove(tf)

    print("\n🎉 All AgentBroko V5 Education & Donation Engine tests passed successfully!")

if __name__ == '__main__':
    test_v5_suite()
