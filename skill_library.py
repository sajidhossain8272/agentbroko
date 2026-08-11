"""
AgentBroko — Persistent Skill Library
Version: v1.0

Every skill is a reusable, versioned, measured capability.
Skills are not static knowledge. They are actionable procedures
with verification status, confidence tracking, and performance metrics.
"""
import json
import os
import time
import uuid
import logging
from typing import Optional

SKILL_FILE = "skill_library.json"

VERIFICATION_STATUSES = ["DISCOVERED", "UNDERSTOOD", "EXPERIMENTAL", "TESTED", "VERIFIED", "DEPRECATED"]

SKILL_CATEGORIES = [
    "Programming", "AI", "Agents", "Research", "Web", "GitHub",
    "Automation", "Business", "Marketing", "Writing", "Data",
    "Security", "DevOps", "Cloud", "Databases", "APIs",
    "AgentCoin", "Moltbook", "Product", "Revenue", "Learning"
]


class Skill:
    def __init__(self, name, category, description, purpose="",
                 procedure=None, examples=None, sources=None,
                 dependencies=None, skill_id=None):
        self.skill_id = skill_id or f"skill_{uuid.uuid4().hex[:10]}"
        self.name = name
        self.category = category
        self.description = description
        self.purpose = purpose
        self.procedure = procedure or []          # List of steps
        self.examples = examples or []           # List of example dicts
        self.sources = sources or []             # URLs / references
        self.dependencies = dependencies or []   # Other skill_ids
        self.verification_status = "DISCOVERED"
        self.confidence = 0.10
        self.usage_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.version = 1
        self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.updated_at = self.created_at
        self.last_used = None
        self.last_verified = None
        self.version_history = []
        self.knowledge = ""
        self.common_failures = []
        self.tags = []

    def advance_status(self, status=None):
        """Advance verification status to the next level, or set explicitly."""
        if status and status in VERIFICATION_STATUSES:
            old = self.verification_status
            self.verification_status = status
            self.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            logging.info(f"[SKILL LIBRARY] Skill '{self.name}' status: {old} → {status}")
            return
        idx = VERIFICATION_STATUSES.index(self.verification_status)
        if idx < len(VERIFICATION_STATUSES) - 2:  # don't auto-advance to DEPRECATED
            self.verification_status = VERIFICATION_STATUSES[idx + 1]
            self.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def record_success(self):
        self.usage_count += 1
        self.success_count += 1
        self.last_used = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.confidence = min(1.0, self.confidence + 0.05)
        self.updated_at = self.last_used

    def record_failure(self, failure_note=""):
        self.usage_count += 1
        self.failure_count += 1
        self.last_used = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.confidence = max(0.05, self.confidence - 0.08)
        self.updated_at = self.last_used
        if failure_note and failure_note not in self.common_failures:
            self.common_failures.append(failure_note)

    def reliability(self):
        if self.usage_count == 0:
            return 0.0
        return round(self.success_count / self.usage_count, 3)

    def snapshot_version(self):
        """Save current state to version history before updating."""
        self.version_history.append({
            "version": self.version,
            "verification_status": self.verification_status,
            "confidence": self.confidence,
            "knowledge": self.knowledge[:200],
            "snapshotted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })
        self.version += 1
        self.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self):
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "purpose": self.purpose,
            "knowledge": self.knowledge,
            "procedure": self.procedure,
            "examples": self.examples,
            "sources": self.sources,
            "dependencies": self.dependencies,
            "common_failures": self.common_failures,
            "tags": self.tags,
            "verification_status": self.verification_status,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "reliability": self.reliability(),
            "version": self.version,
            "version_history": self.version_history[-3:],  # keep last 3 snapshots
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_used": self.last_used,
            "last_verified": self.last_verified
        }

    @classmethod
    def from_dict(cls, d):
        s = cls(
            name=d["name"],
            category=d.get("category", "General"),
            description=d.get("description", ""),
            purpose=d.get("purpose", ""),
            procedure=d.get("procedure", []),
            examples=d.get("examples", []),
            sources=d.get("sources", []),
            dependencies=d.get("dependencies", []),
            skill_id=d.get("skill_id")
        )
        s.verification_status = d.get("verification_status", "DISCOVERED")
        s.confidence = d.get("confidence", 0.10)
        s.usage_count = d.get("usage_count", 0)
        s.success_count = d.get("success_count", 0)
        s.failure_count = d.get("failure_count", 0)
        s.version = d.get("version", 1)
        s.version_history = d.get("version_history", [])
        s.created_at = d.get("created_at", s.created_at)
        s.updated_at = d.get("updated_at", s.updated_at)
        s.last_used = d.get("last_used")
        s.last_verified = d.get("last_verified")
        s.knowledge = d.get("knowledge", "")
        s.common_failures = d.get("common_failures", [])
        s.tags = d.get("tags", [])
        return s


class SkillLibrary:
    """
    Persistent, versioned skill store for AgentBroko.
    Every capability the agent learns lives here.
    """

    def __init__(self, library_file=SKILL_FILE):
        self.library_file = library_file
        self._skills = {}   # skill_id -> Skill
        self._load()
        self._seed_if_empty()

    def _load(self):
        if os.path.exists(self.library_file):
            try:
                with open(self.library_file) as f:
                    data = json.load(f)
                for sd in data.get("skills", []):
                    s = Skill.from_dict(sd)
                    self._skills[s.skill_id] = s
                logging.info(f"[SKILL LIBRARY] Loaded {len(self._skills)} skills from {self.library_file}")
            except Exception as e:
                logging.error(f"[SKILL LIBRARY] Load error: {e}")

    def _save(self):
        try:
            with open(self.library_file, "w") as f:
                json.dump({
                    "version": "1.0",
                    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "skill_count": len(self._skills),
                    "skills": [s.to_dict() for s in self._skills.values()]
                }, f, indent=2)
        except Exception as e:
            logging.error(f"[SKILL LIBRARY] Save error: {e}")

    def _seed_if_empty(self):
        if self._skills:
            return
        # Seed with foundational skills that AgentBroko already demonstrated
        seeds = [
            {
                "name": "moltbook_content_strategy",
                "category": "Moltbook",
                "description": "Publish useful, community-driven content on Moltbook",
                "purpose": "Build reputation and discover opportunities through genuine engagement",
                "knowledge": "Post in relevant communities. Focus on developer communities (/dev, /agents, /ai). Write substantive posts with practical value. Avoid spam. Target 6 posts/day max.",
                "verification_status": "TESTED",
                "confidence": 0.75
            },
            {
                "name": "github_repository_management",
                "category": "GitHub",
                "description": "Create, maintain, and push to GitHub repositories via API",
                "purpose": "Publish code, maintain engineering assets, commit as AgentBroko identity",
                "knowledge": "Use git with author brokeinnovaiton@gmail.com. Always verify push succeeded. Never embed credentials in code.",
                "verification_status": "VERIFIED",
                "confidence": 0.90
            },
            {
                "name": "opportunity_scoring",
                "category": "Business",
                "description": "Score business opportunities using the executive value function",
                "purpose": "Select highest-value actions to maximize long-term revenue and learning",
                "knowledge": "Score = (Revenue × Prob × Speed × Repeatability) / (Cost × Risk × Time). Weight toward first-revenue speed and autonomous execution potential.",
                "verification_status": "TESTED",
                "confidence": 0.70
            },
            {
                "name": "ai_provider_routing",
                "category": "AI",
                "description": "Route AI requests to appropriate providers based on task complexity",
                "purpose": "Minimize cost while maximizing quality for each task type",
                "knowledge": "Use Gemini Primary for HIGH_REASONING/CODE/CONTENT. Use fallback keys for routine tasks. Use OpenRouter Free for classification/summarization. Implement exponential backoff on 429.",
                "verification_status": "VERIFIED",
                "confidence": 0.88
            },
            {
                "name": "agentcoin_contribution_protocol",
                "category": "AgentCoin",
                "description": "Submit verified contributions to AgentCoin Protocol v0.1",
                "purpose": "Build portable reputation and earn rewards for genuine contributions",
                "knowledge": "Use agentcoin.py SDK. Submit contribution_type from CONTRIBUTION_TYPES. Attach evidence for higher confidence. Anti-gaming engine enforces rate limits.",
                "verification_status": "EXPERIMENTAL",
                "confidence": 0.60
            }
        ]
        for seed in seeds:
            s = Skill(
                name=seed["name"],
                category=seed["category"],
                description=seed["description"],
                purpose=seed.get("purpose", "")
            )
            s.knowledge = seed.get("knowledge", "")
            s.verification_status = seed.get("verification_status", "DISCOVERED")
            s.confidence = seed.get("confidence", 0.5)
            self._skills[s.skill_id] = s
        self._save()
        logging.info(f"[SKILL LIBRARY] Seeded {len(seeds)} foundational skills")

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def add_skill(self, skill: Skill) -> bool:
        """Add a new skill. Returns False if duplicate name exists."""
        existing = self.find_by_name(skill.name)
        if existing:
            logging.info(f"[SKILL LIBRARY] Skill '{skill.name}' already exists — updating instead")
            return self.update_skill(existing.skill_id, skill)
        self._skills[skill.skill_id] = skill
        self._save()
        logging.info(f"[SKILL LIBRARY] Added new skill: '{skill.name}' ({skill.verification_status})")
        return True

    def update_skill(self, skill_id: str, updated_skill: Skill) -> bool:
        if skill_id not in self._skills:
            return False
        existing = self._skills[skill_id]
        existing.snapshot_version()
        # Merge updates
        existing.description = updated_skill.description or existing.description
        existing.knowledge = updated_skill.knowledge or existing.knowledge
        existing.procedure = updated_skill.procedure or existing.procedure
        existing.sources += [s for s in updated_skill.sources if s not in existing.sources]
        existing.confidence = max(existing.confidence, updated_skill.confidence)
        if updated_skill.verification_status in VERIFICATION_STATUSES:
            existing.verification_status = updated_skill.verification_status
        self._save()
        return True

    def record_skill_use(self, skill_id: str, success: bool, note=""):
        if skill_id not in self._skills:
            return False
        s = self._skills[skill_id]
        if success:
            s.record_success()
        else:
            s.record_failure(note)
        # Auto-advance verification status after consistent success
        if s.success_count >= 5 and s.verification_status == "EXPERIMENTAL":
            s.advance_status("TESTED")
        if s.success_count >= 15 and s.reliability() >= 0.85 and s.verification_status == "TESTED":
            s.advance_status("VERIFIED")
        # Flag unreliable skills
        if s.usage_count >= 5 and s.reliability() < 0.40 and s.verification_status not in ["DEPRECATED"]:
            logging.warning(f"[SKILL LIBRARY] Skill '{s.name}' reliability {s.reliability():.0%} — flagging for review")
        self._save()
        return True

    def deprecate_skill(self, skill_id: str, reason=""):
        if skill_id in self._skills:
            self._skills[skill_id].advance_status("DEPRECATED")
            self._save()

    # ── Lookup ────────────────────────────────────────────────────────────────

    def find_by_name(self, name: str) -> Optional[Skill]:
        name_lower = name.lower().strip()
        for s in self._skills.values():
            if s.name.lower().strip() == name_lower:
                return s
        return None

    def get_by_id(self, skill_id: str) -> Optional[Skill]:
        return self._skills.get(skill_id)

    def search(self, query: str, category: str = None) -> list:
        q = query.lower()
        results = []
        for s in self._skills.values():
            if s.verification_status == "DEPRECATED":
                continue
            if category and s.category.lower() != category.lower():
                continue
            if q in s.name.lower() or q in s.description.lower() or q in s.knowledge.lower():
                results.append(s)
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results

    def get_all(self, include_deprecated=False) -> list:
        skills = list(self._skills.values())
        if not include_deprecated:
            skills = [s for s in skills if s.verification_status != "DEPRECATED"]
        return sorted(skills, key=lambda s: s.confidence, reverse=True)

    def get_verified(self) -> list:
        return [s for s in self._skills.values() if s.verification_status == "VERIFIED"]

    def get_flagged_for_review(self) -> list:
        """Skills with low reliability that need attention."""
        return [s for s in self._skills.values()
                if s.usage_count >= 3 and s.reliability() < 0.50
                and s.verification_status != "DEPRECATED"]

    def knowledge_gap_check(self, topic: str) -> bool:
        """Returns True if no relevant skill exists for the given topic."""
        return len(self.search(topic)) == 0

    def to_api_response(self):
        skills = self.get_all()
        return {
            "total": len(skills),
            "verified": len(self.get_verified()),
            "flagged": len(self.get_flagged_for_review()),
            "skills": [s.to_dict() for s in skills]
        }
