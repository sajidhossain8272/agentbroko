"""
AgentBroko — Self-Teaching Engine
Version: v1.0

Orchestrates the full learning loop:
OBSERVE → IDENTIFY GAP → SEARCH → COLLECT → EVALUATE
→ UNDERSTAND → EXTRACT → PRACTICE → TEST → VERIFY
→ CREATE SKILL → USE → MEASURE → IMPROVE

This is the brain of self-improvement.
It does not just read pages. It creates verified, reusable skills.
"""
import logging
import time
import json
import os
from event_bus import EventBus
from skill_library import SkillLibrary, Skill
from research_engine import ResearchEngine

KNOWLEDGE_GAPS_FILE = "knowledge_gaps.json"
LEARNING_LOG_FILE = "learning_log.json"


class KnowledgeGap:
    def __init__(self, topic, reason, source="execution_failure", urgency=0.5, impact=0.5):
        self.topic = topic
        self.reason = reason
        self.source = source
        self.urgency = urgency
        self.impact = impact
        self.score = urgency * impact
        self.detected_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.resolved = False
        self.resolved_at = None

    def to_dict(self):
        return {
            "topic": self.topic,
            "reason": self.reason,
            "source": self.source,
            "urgency": self.urgency,
            "impact": self.impact,
            "score": self.score,
            "detected_at": self.detected_at,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at
        }


class LearningRecord:
    def __init__(self, topic, source, knowledge, skill_id=None, verified=False):
        self.topic = topic
        self.source = source
        self.knowledge = knowledge
        self.skill_id = skill_id
        self.verified = verified
        self.recorded_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self):
        return {
            "topic": self.topic,
            "source": self.source,
            "knowledge": self.knowledge[:300],
            "skill_id": self.skill_id,
            "verified": self.verified,
            "recorded_at": self.recorded_at
        }


class SelfTeachingEngine:
    """
    The full autonomous learning system.
    Detects what AgentBroko doesn't know, researches it,
    builds skills from the results, and tracks performance.
    """

    # Research priorities — areas that directly improve mission performance
    RESEARCH_PRIORITIES = [
        {"topic": "python asyncio event loop patterns", "reason": "Improve agent concurrency", "urgency": 0.7, "impact": 0.8},
        {"topic": "github actions ci workflows", "reason": "Improve automated testing pipeline", "urgency": 0.6, "impact": 0.7},
        {"topic": "moltbook api developer documentation", "reason": "Improve Moltbook integration reliability", "urgency": 0.8, "impact": 0.9},
        {"topic": "semantic versioning software releases", "reason": "Improve GitHub repository management", "urgency": 0.5, "impact": 0.6},
        {"topic": "server sent events python implementation", "reason": "Improve Command Center real-time streaming", "urgency": 0.7, "impact": 0.7},
        {"topic": "saas micro product monetization strategies", "reason": "Improve revenue discovery capability", "urgency": 0.8, "impact": 0.9},
        {"topic": "developer tools market opportunities 2025", "reason": "Identify high-value product opportunities", "urgency": 0.7, "impact": 0.85},
        {"topic": "ai agent frameworks comparison", "reason": "Understand competitive landscape", "urgency": 0.5, "impact": 0.7},
    ]

    def __init__(self):
        self.skills = SkillLibrary()
        self.research = ResearchEngine()
        self.bus = EventBus()
        self._gaps = []
        self._learning_log = []
        self._load_state()
        self._seed_research_tasks()

    def _load_state(self):
        if os.path.exists(KNOWLEDGE_GAPS_FILE):
            try:
                with open(KNOWLEDGE_GAPS_FILE) as f:
                    data = json.load(f)
                for g in data.get("gaps", []):
                    if not g.get("resolved"):
                        gap = KnowledgeGap(g["topic"], g["reason"], g.get("source", "unknown"),
                                           g.get("urgency", 0.5), g.get("impact", 0.5))
                        gap.detected_at = g.get("detected_at", gap.detected_at)
                        self._gaps.append(gap)
            except Exception:
                pass
        if os.path.exists(LEARNING_LOG_FILE):
            try:
                with open(LEARNING_LOG_FILE) as f:
                    self._learning_log = json.load(f).get("records", [])
            except Exception:
                pass

    def _save_state(self):
        try:
            with open(KNOWLEDGE_GAPS_FILE, "w") as f:
                json.dump({"gaps": [g.to_dict() for g in self._gaps[-50:]]}, f, indent=2)
            with open(LEARNING_LOG_FILE, "w") as f:
                json.dump({"records": self._learning_log[-100:]}, f, indent=2)
        except Exception as e:
            logging.error(f"[SELF-TEACHING] State save error: {e}")

    def _seed_research_tasks(self):
        """Add initial research tasks if the queue is empty."""
        if self.research.get_pending_tasks():
            return
        for rp in self.RESEARCH_PRIORITIES[:3]:  # Only seed top 3 initially
            if self.skills.knowledge_gap_check(rp["topic"].replace(" ", "_")):
                self.research.add_research_task(rp["topic"], rp["reason"],
                                                rp["urgency"] * rp["impact"])

    # ── Gap Detection ──────────────────────────────────────────────────────

    def detect_gap_from_error(self, error_message: str, component: str):
        """
        When an error occurs, detect if it represents a knowledge gap.
        Creates a research task if we don't have a skill for this.
        """
        # Classify the error into a topic
        error_lower = error_message.lower()
        topic = None
        urgency = 0.8
        impact = 0.85

        if "api" in error_lower and "timeout" in error_lower:
            topic = "api timeout retry backoff patterns"
        elif "moltbook" in error_lower and ("verif" in error_lower or "fail" in error_lower):
            topic = "moltbook api verification handling"
        elif "import" in error_lower and "module" in error_lower:
            topic = "python module dependency management"
        elif "json" in error_lower and ("decode" in error_lower or "invalid" in error_lower):
            topic = "robust json parsing error handling"
        elif "connection" in error_lower:
            topic = "network connection resilience patterns"

        if topic and self.skills.knowledge_gap_check(topic.replace(" ", "_")):
            gap = KnowledgeGap(topic, f"Error in {component}: {error_message[:100]}", "error",
                               urgency=urgency, impact=impact)
            self._gaps.append(gap)
            self.research.add_research_task(topic, gap.reason, urgency * impact)
            self.bus.emit("learning.gap_detected",
                          f"Knowledge gap detected: '{topic}'",
                          metadata={"topic": topic, "source": "error", "component": component})
            logging.info(f"[SELF-TEACHING] Gap detected from error: {topic}")

    def detect_gap_from_task(self, task_description: str):
        """Detect knowledge gaps from upcoming task requirements."""
        desc_lower = task_description.lower()
        gaps_to_check = [
            ("github actions", "ci/cd automation"),
            ("docker", "containerization"),
            ("stripe api", "payment processing integration"),
            ("graphql", "graphql api development"),
            ("kubernetes", "container orchestration"),
            ("websocket", "websocket real-time communication"),
            ("redis", "redis caching patterns"),
        ]
        for keyword, topic in gaps_to_check:
            if keyword in desc_lower and self.skills.knowledge_gap_check(topic.replace(" ", "_")):
                gap = KnowledgeGap(topic, f"Task requires: {task_description[:60]}", "task", 0.6, 0.7)
                self._gaps.append(gap)
                self.research.add_research_task(topic, gap.reason, 0.6 * 0.7)
                logging.info(f"[SELF-TEACHING] Gap detected from task: {topic}")

    # ── Learning Loop ──────────────────────────────────────────────────────

    def run_learning_cycle(self) -> dict:
        """
        Execute one full OBSERVE→LEARN→SKILL cycle.
        Safe to call from agent_runtime during WAIT cycles.
        """
        logging.info("[SELF-TEACHING] Learning cycle started")
        self.bus.emit("learning.cycle_start", "Self-teaching cycle beginning — researching knowledge gaps")

        results = {
            "tasks_processed": 0,
            "skills_created": 0,
            "skills_updated": 0,
            "gaps_resolved": 0,
            "sources_added": 0
        }

        # 1. Run research cycle
        completed_tasks = self.research.run_research_cycle(skill_library=self.skills)
        results["tasks_processed"] = len(completed_tasks)

        for task in completed_tasks:
            if task.get("skill_created"):
                results["skills_created"] += 1
                self.bus.emit("learning.skill_created",
                              f"New skill created: '{task.get('topic', 'Unknown')}'",
                              metadata={"skill_id": task["skill_created"], "topic": task["topic"]})
                # Mark related gap as resolved
                for gap in self._gaps:
                    if gap.topic.lower() in task["topic"].lower() and not gap.resolved:
                        gap.resolved = True
                        gap.resolved_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                        results["gaps_resolved"] += 1

            # Record to learning log
            record = LearningRecord(
                topic=task.get("topic", ""),
                source=", ".join([r.get("url", "") for r in task.get("results", [])[:2]]),
                knowledge=task.get("knowledge_extracted", ""),
                skill_id=task.get("skill_created"),
                verified=False
            )
            self._learning_log.append(record.to_dict())
            results["sources_added"] += task.get("result_count", 0)

        # 2. Check for flagged skills that need revalidation
        flagged = self.skills.get_flagged_for_review()
        for skill in flagged[:2]:
            logging.warning(f"[SELF-TEACHING] Skill flagged for review: '{skill.name}' (reliability={skill.reliability():.0%})")
            self.bus.emit("learning.skill_flagged",
                          f"Skill '{skill.name}' needs improvement (reliability: {skill.reliability():.0%})",
                          metadata={"skill_id": skill.skill_id, "reliability": skill.reliability()})
            # Queue research to improve it
            self.research.add_research_task(
                skill.name.replace("_", " "),
                f"Skill reliability is low ({skill.reliability():.0%}) — research improvements",
                priority=0.75
            )

        # 3. Queue new priority research if budget allows
        pending_count = len(self.research.get_pending_tasks())
        if pending_count < 3:
            unlearned = [rp for rp in self.RESEARCH_PRIORITIES
                         if self.skills.knowledge_gap_check(rp["topic"].replace(" ", "_"))]
            for rp in unlearned[:2]:
                self.research.add_research_task(rp["topic"], rp["reason"], rp["urgency"] * rp["impact"])

        self._save_state()
        logging.info(f"[SELF-TEACHING] Cycle complete: {results}")
        self.bus.emit("learning.cycle_complete",
                      f"Learning cycle complete: {results['tasks_processed']} tasks, "
                      f"{results['skills_created']} skills created",
                      metadata=results)
        return results

    # ── API Endpoints ──────────────────────────────────────────────────────

    def to_api_skills(self) -> dict:
        return self.skills.to_api_response()

    def to_api_research(self) -> dict:
        return self.research.to_api_response()

    def to_api_gaps(self) -> dict:
        active = [g.to_dict() for g in self._gaps if not g.resolved]
        return {"knowledge_gaps": active, "total": len(active)}

    def to_api_learning_log(self) -> dict:
        return {"records": self._learning_log[-20:]}

    def get_skill_for_task(self, task_description: str) -> list:
        """Return relevant skills for a given task."""
        words = [w for w in task_description.lower().split() if len(w) > 3]
        results = []
        for word in words[:3]:
            found = self.skills.search(word)
            results.extend([s for s in found if s not in results])
        return results[:5]
