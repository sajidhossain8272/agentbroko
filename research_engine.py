"""
AgentBroko — Research Engine
Version: v1.0

Real web and GitHub research engine. No hallucination.
Every source is fetched, hashed, evaluated, and either
extracted into knowledge or discarded with a reason.

Principle: Research without a reason is waste.
           Research with a reason becomes skill.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import hashlib
import logging
import re
from typing import Optional

SOURCE_REGISTRY_FILE = "source_registry.json"

# Source quality tiers
QUALITY_TIERS = {
    "official_docs": 0.95,
    "primary_source": 0.90,
    "maintainer_docs": 0.85,
    "github_readme": 0.75,
    "github_issue": 0.65,
    "engineering_blog": 0.70,
    "community": 0.50,
    "unknown": 0.40
}

# Research budget (per cycle)
MAX_REQUESTS_PER_CYCLE = 5
REQUEST_TIMEOUT = 8


class ResearchSource:
    def __init__(self, url, title="", source_type="unknown", content_hash="",
                 topics=None, quality_score=0.5, retrieved_at=None):
        self.source_id = f"src_{hashlib.md5(url.encode()).hexdigest()[:12]}"
        self.url = url
        self.title = title
        self.source_type = source_type
        self.quality_score = quality_score
        self.content_hash = content_hash
        self.topics = topics or []
        self.retrieved_at = retrieved_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.reliable = quality_score >= 0.65

    def to_dict(self):
        return {
            "source_id": self.source_id,
            "url": self.url,
            "title": self.title,
            "source_type": self.source_type,
            "quality_score": self.quality_score,
            "content_hash": self.content_hash,
            "topics": self.topics,
            "retrieved_at": self.retrieved_at,
            "reliable": self.reliable
        }


class ResearchTask:
    def __init__(self, topic, reason, priority=0.5, task_id=None):
        self.task_id = task_id or f"res_{hashlib.md5(topic.encode()).hexdigest()[:10]}"
        self.topic = topic
        self.reason = reason
        self.priority = priority
        self.status = "QUEUED"
        self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.completed_at = None
        self.results = []
        self.knowledge_extracted = ""
        self.skill_created = None

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "topic": self.topic,
            "reason": self.reason,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "result_count": len(self.results),
            "knowledge_extracted": self.knowledge_extracted[:200] if self.knowledge_extracted else "",
            "skill_created": self.skill_created
        }


class ResearchEngine:
    """
    Fetches real web content and GitHub data to extract actionable knowledge.
    Budget-aware: limits requests per cycle.
    """

    GITHUB_API = "https://api.github.com"

    def __init__(self, source_registry_file=SOURCE_REGISTRY_FILE):
        self.registry_file = source_registry_file
        self._sources = {}   # source_id -> ResearchSource dict
        self._research_tasks = []
        self._load()

    def _load(self):
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file) as f:
                    data = json.load(f)
                self._sources = {s["source_id"]: s for s in data.get("sources", [])}
                self._research_tasks = [ResearchTask(**t) if not isinstance(t, ResearchTask) else t
                                        for t in []]  # tasks are ephemeral
            except Exception:
                pass

    def _save(self):
        try:
            with open(self.registry_file, "w") as f:
                json.dump({
                    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source_count": len(self._sources),
                    "sources": list(self._sources.values())
                }, f, indent=2)
        except Exception as e:
            logging.error(f"[RESEARCH ENGINE] Save error: {e}")

    def _already_seen(self, url: str, content_hash: str) -> bool:
        sid = f"src_{hashlib.md5(url.encode()).hexdigest()[:12]}"
        if sid in self._sources:
            existing = self._sources[sid]
            if existing.get("content_hash") == content_hash:
                logging.debug(f"[RESEARCH ENGINE] Skipping unchanged source: {url}")
                return True
        return False

    def add_research_task(self, topic: str, reason: str, priority: float = 0.5):
        task = ResearchTask(topic, reason, priority)
        self._research_tasks.append(task)
        logging.info(f"[RESEARCH ENGINE] Research task queued: '{topic}' (priority={priority:.2f})")
        return task

    def get_pending_tasks(self) -> list:
        pending = [t for t in self._research_tasks if t.status == "QUEUED"]
        return sorted(pending, key=lambda t: t.priority, reverse=True)

    def get_all_tasks(self) -> list:
        return self._research_tasks

    def fetch_url(self, url: str, purpose="research") -> Optional[str]:
        """Fetch URL content as plain text. Returns None on failure."""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "AgentBroko/v11 Research-Engine (+https://github.com/agentbroko/agentbroko)",
                "Accept": "text/html,application/json"
            })
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                raw = resp.read()
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    text = raw.decode("latin-1", errors="replace")
                logging.info(f"[RESEARCH ENGINE] Fetched: {url} ({len(text)} chars)")
                return text
        except Exception as e:
            logging.warning(f"[RESEARCH ENGINE] Fetch failed: {url} — {e}")
            return None

    def fetch_github_repo(self, owner: str, repo: str) -> Optional[dict]:
        """Fetch GitHub repo metadata + README using public API."""
        try:
            # Repo metadata
            api_url = f"{self.GITHUB_API}/repos/{owner}/{repo}"
            req = urllib.request.Request(api_url, headers={
                "User-Agent": "AgentBroko/v11",
                "Accept": "application/vnd.github.v3+json"
            })
            gh_token = os.environ.get("GITHUB_TOKEN", "")
            if gh_token:
                req.add_header("Authorization", f"token {gh_token}")

            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                meta = json.loads(resp.read().decode())

            # README
            readme_url = f"{self.GITHUB_API}/repos/{owner}/{repo}/readme"
            req2 = urllib.request.Request(readme_url, headers=req.headers)
            readme_text = ""
            try:
                with urllib.request.urlopen(req2, timeout=REQUEST_TIMEOUT) as resp:
                    readme_data = json.loads(resp.read().decode())
                    import base64
                    readme_text = base64.b64decode(readme_data.get("content", "")).decode("utf-8", errors="replace")[:3000]
            except Exception:
                pass

            return {
                "owner": owner,
                "repo": repo,
                "full_name": meta.get("full_name", ""),
                "description": meta.get("description", ""),
                "stars": meta.get("stargazers_count", 0),
                "language": meta.get("language", ""),
                "topics": meta.get("topics", []),
                "license": (meta.get("license") or {}).get("name", ""),
                "readme": readme_text,
                "url": meta.get("html_url", ""),
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        except Exception as e:
            logging.warning(f"[RESEARCH ENGINE] GitHub fetch failed: {owner}/{repo} — {e}")
            return None

    def classify_source_type(self, url: str) -> str:
        url_lower = url.lower()
        if "docs." in url_lower or "/docs/" in url_lower or "documentation" in url_lower:
            return "official_docs"
        if "github.com" in url_lower and ("/blob/" in url_lower or "/readme" in url_lower.lower()):
            return "github_readme"
        if "github.com" in url_lower and "/issues/" in url_lower:
            return "github_issue"
        if any(x in url_lower for x in ["blog.", "/blog/", "dev.to", "medium.com"]):
            return "engineering_blog"
        if "github.com" in url_lower:
            return "primary_source"
        return "unknown"

    def extract_knowledge_from_text(self, text: str, topic: str, max_chars=2000) -> str:
        """
        Extract relevant content from fetched text using keyword proximity.
        Returns a summary suitable for storing in a skill's knowledge field.
        """
        # Strip HTML tags
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean).strip()

        # Find paragraphs mentioning the topic
        topic_words = topic.lower().split()
        paragraphs = [p.strip() for p in clean.split('\n') if len(p.strip()) > 40]
        scored = []
        for p in paragraphs:
            score = sum(1 for w in topic_words if w in p.lower())
            if score > 0:
                scored.append((score, p))
        scored.sort(reverse=True)

        # Take top paragraphs up to max_chars
        result = []
        total = 0
        for score, p in scored:
            if total + len(p) > max_chars:
                break
            result.append(p)
            total += len(p)

        return ' '.join(result) if result else clean[:max_chars]

    def run_research_cycle(self, skill_library=None) -> list:
        """
        Process pending research tasks (up to budget).
        Returns list of completed task dicts.
        """
        pending = self.get_pending_tasks()
        if not pending:
            return []

        completed = []
        requests_used = 0

        for task in pending[:MAX_REQUESTS_PER_CYCLE]:
            if requests_used >= MAX_REQUESTS_PER_CYCLE:
                break

            logging.info(f"[RESEARCH ENGINE] Processing: '{task.topic}' — {task.reason}")
            task.status = "RUNNING"

            # Build search URLs based on topic type
            search_urls = self._build_search_urls(task.topic)
            extracted = ""

            for url in search_urls[:2]:  # Max 2 URLs per task
                if requests_used >= MAX_REQUESTS_PER_CYCLE:
                    break
                content = self.fetch_url(url)
                requests_used += 1
                if not content:
                    continue

                content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]
                if self._already_seen(url, content_hash):
                    continue

                src_type = self.classify_source_type(url)
                quality = QUALITY_TIERS.get(src_type, 0.4)
                src = ResearchSource(url=url, title=task.topic, source_type=src_type,
                                     content_hash=content_hash, topics=[task.topic],
                                     quality_score=quality)
                self._sources[src.source_id] = src.to_dict()
                task.results.append(src.to_dict())

                snippet = self.extract_knowledge_from_text(content, task.topic)
                if snippet:
                    extracted += f"\n\nSource ({src_type}, quality={quality:.2f}): {url}\n{snippet[:800]}"

            task.knowledge_extracted = extracted.strip()
            task.status = "COMPLETED"
            task.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            # If skill_library provided, create/update a skill from the research
            if skill_library and extracted:
                from skill_library import Skill
                existing = skill_library.find_by_name(task.topic.lower().replace(' ', '_'))
                if not existing:
                    skill = Skill(
                        name=task.topic.lower().replace(' ', '_').replace('-', '_'),
                        category="Research",
                        description=f"Researched: {task.topic}",
                        purpose=task.reason,
                        sources=[r["url"] for r in task.results]
                    )
                    skill.knowledge = extracted[:1500]
                    skill.advance_status("UNDERSTOOD")
                    skill_library.add_skill(skill)
                    task.skill_created = skill.skill_id
                    logging.info(f"[RESEARCH ENGINE] Skill created: '{skill.name}'")
                else:
                    existing.knowledge += f"\n\n[Updated {time.strftime('%Y-%m-%d')}]\n{extracted[:500]}"
                    existing.sources += [r["url"] for r in task.results if r["url"] not in existing.sources]
                    skill_library._save()

            completed.append(task.to_dict())

        self._save()
        logging.info(f"[RESEARCH ENGINE] Cycle complete: {len(completed)} tasks, {requests_used} requests")
        return completed

    def _build_search_urls(self, topic: str) -> list:
        """Build targeted URLs for a research topic."""
        urls = []
        topic_encoded = urllib.parse.quote_plus(topic)
        topic_lower = topic.lower()

        # GitHub repositories
        if any(k in topic_lower for k in ["github", "library", "framework", "tool", "api", "sdk", "python", "agent"]):
            urls.append(f"https://github.com/search?q={topic_encoded}&type=repositories&s=stars")
            urls.append(f"https://api.github.com/search/repositories?q={topic_encoded}&sort=stars&per_page=5")

        # Official docs
        if "python" in topic_lower:
            subtopic = topic_lower.replace("python", "").strip()
            urls.append(f"https://docs.python.org/3/search.html?q={urllib.parse.quote_plus(subtopic)}")

        # README.md pattern for specific repos
        if "/" in topic_lower:
            parts = topic_lower.split("/", 1)
            urls.append(f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/main/README.md")
            urls.append(f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/master/README.md")

        # Fallback: GitHub search
        if not urls:
            urls.append(f"https://api.github.com/search/repositories?q={topic_encoded}&sort=stars&per_page=3")

        return urls

    def get_source_registry(self) -> list:
        return list(self._sources.values())

    def to_api_response(self) -> dict:
        pending = self.get_pending_tasks()
        completed = [t for t in self._research_tasks if t.status == "COMPLETED"]
        return {
            "research_tasks": [t.to_dict() for t in self._research_tasks[-20:]],
            "knowledge_gaps": [t.to_dict() for t in pending[:10]],
            "source_count": len(self._sources),
            "tasks_queued": len(pending),
            "tasks_completed": len(completed)
        }
