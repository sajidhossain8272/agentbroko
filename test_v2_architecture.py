from btc_wallet_client import BTCWalletClient
from treasury import Treasury
from financial_ledger import FinancialLedger
from opportunity_engine import OpportunityEngine
from crm_engine import CRMEngine
from experiment_engine import ExperimentEngine
from agentbroko_dashboard import generate_economic_status_report

def test_v2_suite():
    print("Testing BTCWalletClient...")
    btc = BTCWalletClient()
    assert btc.primary_address.startswith("bc1") or btc.primary_address.startswith("3") or btc.primary_address.startswith("1")
    print(f"✅ Derived BTC Primary Address: {btc.primary_address}")

    print("Testing Treasury...")
    t = Treasury("test_treasury.json")
    t_data = t.sync_balances()
    assert "wallets" in t_data
    assert "bitcoin" in t_data["wallets"]
    assert "evm" in t_data["wallets"]
    print("✅ Unified Treasury sync verified.")

    print("Testing FinancialLedger...")
    f = FinancialLedger("test_revenue.json")
    f.record_revenue("SERVICE", "Test SME", "Technical Audit", 50.0)
    f.record_expense("API", "RPC Node Query Fee", 2.50)
    assert f.data["summary"]["total_revenue_usd"] == 50.0
    assert f.data["summary"]["net_profit_usd"] == 47.50
    print(f"✅ Net Profit calculated: ${f.data['summary']['net_profit_usd']}")

    print("Testing OpportunityEngine...")
    opp_eng = OpportunityEngine("test_opp.json")
    top_opp = opp_eng.get_top_opportunity()
    assert top_opp["score"] > 0
    print(f"✅ Top Opportunity: '{top_opp['title']}' (Score: {top_opp['score']})")

    print("Testing CRMEngine...")
    crm = CRMEngine("test_crm.json")
    summary = crm.get_pipeline_summary()
    assert summary["total_leads"] >= 2
    print(f"✅ Pipeline Value: ${summary['pipeline_value_usd']}")

    print("Testing Owner Economic Status Dashboard...")
    report = generate_economic_status_report()
    assert "AGENTBROKO ECONOMIC STATUS" in report
    assert "BTC:" in report
    assert "EVM:" in report
    assert "Profit:" in report
    print("✅ Owner Status Report output verified.")

    # Cleanup test files
    import os
    for test_f in ["test_treasury.json", "test_revenue.json", "test_opp.json", "test_crm.json"]:
        if os.path.exists(test_f):
            os.remove(test_f)

    print("\n🎉 All AgentBroko V2 Master Architecture tests passed successfully!")

if __name__ == '__main__':
    test_v2_suite()
