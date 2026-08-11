from affiliate_engine import AffiliateEngine
from revenue_ledger import RevenueLedger

def test_affiliate_module():
    print("Testing AffiliateEngine...")
    comp = AffiliateEngine.get_comparison()
    assert "https://accounts.binance.com/en-ZA/register?ref=LZPXAPM5" in comp
    assert "https://www.bybit.com/en/invite/?ref=RX0WA2" in comp
    assert "Disclosure:" in comp
    print("✅ Comparison output verified with URLs and Disclosure.")

    edu = AffiliateEngine.get_educational_post('api_trading')
    assert "Guide:" in edu
    assert "Disclosure:" in edu
    print("✅ Educational content verified with Disclosure.")

    print("Testing RevenueLedger...")
    ledger = RevenueLedger("test_ledger.json")
    ledger.record_impression("Binance")
    ledger.record_click("Bybit")
    ledger.record_revenue("Binance", 50.0, 1, 1)

    data = ledger.data["ledger"]
    binance_data = next(item for item in data if item["partner"] == "Binance")
    bybit_data = next(item for item in data if item["partner"] == "Bybit")

    assert binance_data["impressions"] >= 1
    assert binance_data["revenue"] == 50.0
    assert bybit_data["clicks"] >= 1
    print("✅ Revenue ledger functionality verified.")

    import os
    if os.path.exists("test_ledger.json"):
        os.remove("test_ledger.json")

    print("🎉 All Affiliate Revenue Module tests passed successfully!")

if __name__ == '__main__':
    test_affiliate_module()
