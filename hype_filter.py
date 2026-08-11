import re

class HypeFilter:
    HYPE_WORDS = [
        "guaranteed profit", "guaranteed gains", "can't lose", "100x guaranteed",
        "easy money", "risk-free", "buy now", "don't miss out", "guaranteed moon",
        "secret strategy", "get rich quick", "financial advice", "guaranteed returns"
    ]

    @classmethod
    def contains_hype(cls, text):
        lower_text = text.lower()
        for word in cls.HYPE_WORDS:
            if word in lower_text:
                return True
        return False

    @classmethod
    def sanitize_content(cls, text):
        """
        Sanitizes text to remove hype phrases and enforce educational tone.
        """
        cleaned = text
        for word in cls.HYPE_WORDS:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            cleaned = pattern.sub("[educational topic]", cleaned)
        
        # Ensure mandatory disclaimer if financial subjects discussed
        if "invest" in text.lower() or "exchange" in text.lower() or "binance" in text.lower() or "bybit" in text.lower():
            if "not financial advice" not in cleaned.lower():
                cleaned += "\n\n*Educational Note: This content is for educational purposes only and is not financial advice.*"
        
        return cleaned
