import json
import os
import time

class ContentExperimentEngine:
    def __init__(self, exp_file="content_experiments.json"):
        self.exp_file = exp_file
        self.experiments = self.load_experiments()

    def load_experiments(self):
        if os.path.exists(self.exp_file):
            try:
                with open(self.exp_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_experiments()

    def save_experiments(self):
        with open(self.exp_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)

    def get_seed_experiments(self):
        return [
            {
                "id": "exp_ab_001",
                "variable_tested": "Headline Curiosity Hook",
                "variant_a": "What is Bitcoin?",
                "variant_b": "Bitcoin doesn't actually store coins inside your wallet. Here's what it stores instead.",
                "winner": "variant_b",
                "lift_percentage": 42.0,
                "status": "completed",
                "lesson": "Curiosity hooks framing factual mechanics generate 42% higher reader retention without clickbait."
            },
            {
                "id": "exp_ab_002",
                "variable_tested": "CTA Placement",
                "variant_a": "Top of article affiliate CTA",
                "variant_b": "Contextual bottom-of-article exchange comparison CTA with disclosure",
                "winner": "variant_b",
                "lift_percentage": 65.0,
                "status": "completed",
                "lesson": "Placing transparent affiliate disclosures at the end of educational breakdowns increases qualified clicks by 65%."
            }
        ]
