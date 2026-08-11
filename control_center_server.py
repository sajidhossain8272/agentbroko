import http.server
import socketserver
import json
import urllib.parse
import os
import time
import threading
import logging
from event_bus import EventBus
from goal_manager import GoalManager
from task_manager import TaskManager
from agent_supervisor import AgentSupervisor
from agent_memory import AgentMemory
from skill_registry import SkillRegistry

class ThreadingControlCenterServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Threaded TCP server so SSE streams do not block other API endpoints."""
    allow_reuse_address = True
    daemon_threads = True

class AgentCoinHealthHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path in ('/', '/health', '/api/health'):
            payload = {
                "service": "agentcoin_protocol",
                "status": "ONLINE",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "v0.1",
                "providers": [],
                "last_event": "agentcoin.healthcheck"
            }
            self.send_json(payload)
        else:
            self.send_error(404, "Endpoint Not Found")

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode('utf-8')
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
            self.close_connection = True
            return

    def log_message(self, format, *args):
        return

class AgentCoinHealthServer:
    def __init__(self, port=8010):
        self.port = port
        self.server = None

    def start(self):
        self.server = ThreadingControlCenterServer(("", self.port), AgentCoinHealthHTTPHandler)
        print(f"🌐 [AGENTCOIN HEALTH] Server listening live on http://localhost:{self.port}")
        self.server.serve_forever()

class ControlCenterHTTPHandler(http.server.BaseHTTPRequestHandler):
    bus = EventBus()
    goal_mgr = GoalManager()
    task_mgr = TaskManager()
    supervisor = AgentSupervisor()
    memory = AgentMemory()
    skills = SkillRegistry()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/' or path == '/index.html':
            self.serve_static('static/control_center.html', 'text/html')
        elif path == '/api/agent/status' or path == '/api/agent/health':
            self.send_json(self.supervisor.get_status_payload())
        elif path == '/api/goals':
            self.send_json({"goals": self.goal_mgr.list_goals()})
        elif path == '/api/tasks':
            self.send_json({"tasks": self.task_mgr.list_tasks()})
        elif path == '/api/events' or path == '/api/activity':
            self.send_json({"events": self.bus.get_recent_events(100)})
        elif path == '/api/memory':
            self.send_json(self.memory.data)
        elif path == '/api/skills':
            self.send_json({"skills": self.skills.skills})
        elif path == '/api/business/opportunities':
            from opportunity_discovery import OpportunityDiscoveryEngine
            from opportunity_scoring import OpportunityScoringEngine
            disc = OpportunityDiscoveryEngine()
            scorer = OpportunityScoringEngine()
            ranked = scorer.rank_opportunities(disc.list_opportunities())
            self.send_json({"opportunities": ranked})
        elif path == '/api/business/experiments':
            from business_experiment_engine import BusinessExperimentEngine
            exp = BusinessExperimentEngine()
            self.send_json({"experiments": exp.list_experiments()})
        elif path == '/api/business/intel':
            from business_intelligence_memory import BusinessIntelligenceMemory
            intel = BusinessIntelligenceMemory()
            self.send_json(intel.data)
        elif path == '/api/social/feed':
            from moltbook_client import MoltbookClient
            from moltbook_feed_intelligence import MoltbookFeedIntelligence
            client = MoltbookClient()
            feed = client.get_feed(sort='new', limit=15)
            posts = feed.get('posts', [])
            intel = MoltbookFeedIntelligence()
            analyzed = intel.process_feed(posts)
            self.send_json({"feed": analyzed})
        elif path == '/api/social/threads' or path == '/api/social/memory':
            from social_memory import SocialMemory
            sm = SocialMemory()
            self.send_json(sm.data)
        elif path == '/api/errors':
            from agent_memory import AgentMemory
            am = AgentMemory()
            failures = am.data.get("failure_memory", [])
            self.send_json({"errors": failures})
        elif path == '/api/content/brain':
            from content_brain import ContentBrain
            cb = ContentBrain()
            candidates = cb.generate_candidate_topics()
            decision = cb.evaluate_and_select_action()
            self.send_json({"candidates": candidates, "active_decision": decision})
        elif path == '/api/content/memory':
            from content_memory import ContentMemory
            cm = ContentMemory()
            self.send_json(cm.data)
        elif path == '/api/ai/health':
            from ai_provider_router import AIProviderRouter
            router = AIProviderRouter()
            self.send_json({"providers": router.get_provider_health()})
        elif path == '/api/revenue':
            from revenue_engine import RevenueEngine
            rev = RevenueEngine()
            self.send_json(rev.get_financial_summary())
        elif path == '/api/permissions':
            from permission_manager import PermissionManager
            pm = PermissionManager()
            self.send_json({"current_level": pm.current_level, "level_name": pm.LEVELS.get(pm.current_level), "safe_mode": pm.safe_mode})
        elif path == '/api/reflection':
            from daily_reflection import DailyReflectionEngine
            refl = DailyReflectionEngine()
            self.send_json(refl.generate_daily_report())
        elif path == '/api/v10/audit':
            from self_audit_engine import SelfAuditEngine
            audit = SelfAuditEngine()
            self.send_json(audit.run_self_audit())
        elif path == '/api/v10/strategy':
            from strategy_memory import StrategyMemory
            sm = StrategyMemory()
            self.send_json(sm.data)
        elif path == '/api/v11/skills':
            try:
                from self_teaching_engine import SelfTeachingEngine
                ste = SelfTeachingEngine()
                self.send_json(ste.to_api_skills())
            except Exception as e:
                self.send_json({"skills": [], "total": 0, "error": str(e)})
        elif path == '/api/v11/research':
            try:
                from self_teaching_engine import SelfTeachingEngine
                ste = SelfTeachingEngine()
                self.send_json(ste.to_api_research())
            except Exception as e:
                self.send_json({"research_tasks": [], "knowledge_gaps": [], "error": str(e)})
        elif path == '/api/governor/status':
            try:
                from governor import Governor
                gov = Governor()
                self.send_json(gov.get_status())
            except Exception as e:
                self.send_json({"safe_mode": False, "action_counts_today": {}, "action_limits": {}, "error": str(e)})

        elif path == '/api/stream':
            self.handle_sse_stream()
        else:
            local_file = os.path.join('.', path.lstrip('/'))
            if os.path.exists(local_file) and not os.path.isdir(local_file):
                mime = 'text/html'
                if local_file.endswith('.js'): mime = 'application/javascript'
                elif local_file.endswith('.css'): mime = 'text/css'
                elif local_file.endswith('.json'): mime = 'application/json'
                self.serve_static(local_file, mime)
            else:
                self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(length) if length > 0 else b'{}'
        try:
            payload = json.loads(body_bytes.decode('utf-8'))
        except Exception:
            payload = {}

        if path == '/api/agent/pause':
            self.supervisor.set_status("PAUSED")
            self.send_json({"success": True, "status": "PAUSED"})
        elif path == '/api/agent/resume':
            self.supervisor.set_status("ONLINE")
            self.send_json({"success": True, "status": "ONLINE"})
        elif path == '/api/agent/stop':
            self.supervisor.set_status("IDLE")
            self.send_json({"success": True, "status": "IDLE"})
        elif path == '/api/goals':
            obj = payload.get("objective", "New Goal")
            pri = payload.get("priority", 80.0)
            g = self.goal_mgr.create_goal(obj, pri)
            self.send_json({"success": True, "goal": g})
        elif path == '/api/tasks':
            obj = payload.get("objective", "New Task")
            desc = payload.get("description", "")
            g_id = payload.get("goal_id", "goal_001")
            sk = payload.get("skill", "general")
            pri = payload.get("priority", 75.0)
            t = self.task_mgr.create_task(obj, desc, g_id, sk, pri)
            self.send_json({"success": True, "task": t})
        elif path == '/api/governor/safe-mode':
            try:
                from governor import Governor
                gov = Governor()
                enabled = payload.get('enabled', True)
                gov.set_safe_mode(enabled)
                self.send_json({"success": True, "safe_mode": enabled})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)})
        else:
            self.send_error(404, "Endpoint Not Found")


    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode('utf-8')
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
            self.close_connection = True
            return

    def serve_static(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            try:
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                self.close_connection = True
                return
        except Exception as e:
            try:
                self.send_error(500, f"Error serving file: {e}")
            except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                self.close_connection = True

    def handle_sse_stream(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Queue for subscriber callback
        event_queue = []
        def on_event(evt):
            event_queue.append(evt)

        self.bus.subscribe(on_event)
        try:
            # Replay recent 10 events
            for evt in self.bus.get_recent_events(10):
                try:
                    self.wfile.write(f"data: {json.dumps(evt)}\n\n".encode('utf-8'))
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                    break

            while True:
                if event_queue:
                    evt = event_queue.pop(0)
                    try:
                        self.wfile.write(f"data: {json.dumps(evt)}\n\n".encode('utf-8'))
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                        break
                time.sleep(0.5)
        except Exception:
            pass
        finally:
            self.bus.unsubscribe(on_event)

    def log_message(self, format, *args):
        return # Suppress default HTTP server noise

class ControlCenterServer:
    def __init__(self, port=8000):
        self.port = port
        self.server = None

    def start(self):
        os.makedirs('static', exist_ok=True)
        handler = ControlCenterHTTPHandler
        self.server = ThreadingControlCenterServer(("", self.port), handler)
        print(f"🌐 [CONTROL CENTER UI] Server listening live on http://localhost:{self.port}")
        self.server.serve_forever()

if __name__ == '__main__':
    ControlCenterServer(8000).start()
