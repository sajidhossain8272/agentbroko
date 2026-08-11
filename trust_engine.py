import json
import os
import time

class TrustEngine:
    @staticmethod
    def calculate_trust_score(sources_provided=True, disclosure_included=True, facts_verified=True, corrections_made=0):
        score = 80.0
        if sources_provided: score += 5.0
        if disclosure_included: score += 5.0
        if facts_verified: score += 5.0
        score += min(corrections_made * 2.0, 5.0) # Transparent corrections add trust
        return min(score, 100.0)

class CorrectionEngine:
    def __init__(self, corrections_file="corrections.json"):
        self.corrections_file = corrections_file
        self.items = self.load_corrections()

    def load_corrections(self):
        if os.path.exists(self.corrections_file):
            try:
                with open(self.corrections_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_corrections()

    def save_corrections(self):
        with open(self.corrections_file, 'w') as f:
            json.dump(self.items, f, indent=2)

    def get_seed_corrections(self):
        return [
            {
                "content_id": "cnt_001",
                "original_claim": "Bitcoin legacy address format starts with 'bc1'",
                "corrected_claim": "Bitcoin legacy address format starts with '1'. Bech32 Native SegWit starts with 'bc1q'.",
                "source": "Bitcoin Developer Documentation",
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "reason": "Address format clarification for user accuracy"
            }
        ]

    def log_correction(self, content_id, original_claim, corrected_claim, source, reason):
        item = {
            "content_id": content_id,
            "original_claim": original_claim,
            "corrected_claim": corrected_claim,
            "source": source,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason
        }
        self.items.append(item)
        self.save_corrections()
        return item
