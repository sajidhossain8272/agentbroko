import logging

class SkillRegistry:
    def __init__(self):
        self.skills = {}
        self.register_default_skills()

    def register_skill(self, name, description, capabilities, version="1.0"):
        self.skills[name] = {
            "name": name,
            "description": description,
            "capabilities": capabilities,
            "version": version,
            "enabled": True
        }

    def register_default_skills(self):
        self.register_skill("github_auth", "GitHub Authentication & Token Validation", ["validate_token", "check_permissions"])
        self.register_skill("github_code_agent", "Autonomous GitHub Developer & PR Management", ["create_issue", "create_pr", "inspect_repo"])
        self.register_skill("social_skill", "Moltbook Community & Post Creation", ["discover_posts", "upvote_post", "create_post", "verify_challenge"])
        self.register_skill("business_skill", "Business Opportunity Scoring & Pipeline", ["score_opportunity", "evaluate_pipeline"])
        self.register_skill("education_skill", "5-Level Blockchain & Bitcoin Curriculum", ["generate_post", "get_daily_topic"])
        self.register_skill("growth_skill", "Audience Growth & Topic Intelligence", ["track_audience", "score_topics"])
        self.register_skill("monetization_skill", "Affiliate Analytics & Donation Engine", ["track_affiliate", "track_donations"])
        self.register_skill("coding_skill", "Code Generation, Refactoring & Formatting", ["write_code", "refactor_code"])
        self.register_skill("debugging_skill", "Error Isolation & Automated Patching", ["isolate_error", "patch_error"])
        self.register_skill("wallet_skill", "Fail-Soft Multi-Chain Wallet Monitor", ["check_balances", "sync_treasury"])

    def get_skill(self, name):
        return self.skills.get(name)

    def list_skills(self):
        return [s["name"] for s in self.skills.values() if s["enabled"]]
