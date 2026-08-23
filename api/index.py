"""
AgentBroko Vercel Serverless API & Web Dashboard Entrypoint
Supports both BaseHTTPRequestHandler (Vercel standard) and WSGI/ASGI application.
"""

import http.server
import json
import os
import sys
import time
import urllib.parse

# Ensure repository root is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

STATIC_HTML_PATH = os.path.join(ROOT_DIR, "static", "control_center.html")

def get_dashboard_html():
    if os.path.exists(STATIC_HTML_PATH):
        try:
            with open(STATIC_HTML_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AgentBroko Control Center</title>
    <style>
        body { background: #0b0f19; color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: #1f2937; padding: 2.5rem; border-radius: 1rem; border: 1px solid #374151; text-align: center; max-width: 500px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
        h1 { color: #60a5fa; margin-bottom: 0.5rem; }
        .badge { background: #065f46; color: #34d399; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: bold; font-size: 0.875rem; display: inline-block; margin-bottom: 1.5rem; }
        p { color: #9ca3af; line-height: 1.6; }
        .btn { display: inline-block; background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; margin-top: 1rem; transition: background 0.2s; }
        .btn:hover { background: #2563eb; }
    </style>
</head>
<body>
    <div class="card">
        <h1>AgentBroko OS</h1>
        <div class="badge">ONLINE v1.1.0</div>
        <p>Autonomous AI Executive & Skills Operating System is active and deployed on Vercel.</p>
        <a href="/api/health" class="btn">View API Health</a>
    </div>
</body>
</html>"""

def handle_api_route(path, query_params=None):
    if query_params is None:
        query_params = {}
        
    if path in ("/", "/index.html"):
        return (200, "text/html; charset=utf-8", get_dashboard_html().encode("utf-8"))
    
    if path in ("/api/health", "/api/agent/health"):
        payload = {
            "service": "agentbroko",
            "status": "ONLINE",
            "version": "1.1.0",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment": "Vercel Serverless",
            "system": "Autonomous Executive OS",
            "capabilities": ["pdf_playbook", "video_forge", "moltbook", "agentcoin", "executive_brain", "self_audit"]
        }
        return (200, "application/json", json.dumps(payload, indent=2).encode("utf-8"))
    
    if path == "/api/agent/status":
        try:
            from agent_supervisor import AgentSupervisor
            sup = AgentSupervisor()
            return (200, "application/json", json.dumps(sup.get_status_payload(), indent=2).encode("utf-8"))
        except Exception as e:
            return (200, "application/json", json.dumps({"status": "active", "engine": "AgentBroko V10", "mode": "autonomous", "uptime": "active"}).encode("utf-8"))
            
    if path == "/api/goals":
        try:
            from goal_manager import GoalManager
            mgr = GoalManager()
            return (200, "application/json", json.dumps({"goals": mgr.list_goals()}, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"goals": []}).encode("utf-8"))

    if path == "/api/tasks":
        try:
            from task_manager import TaskManager
            tm = TaskManager()
            return (200, "application/json", json.dumps({"tasks": tm.list_tasks()}, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"tasks": []}).encode("utf-8"))

    if path in ("/api/events", "/api/activity"):
        try:
            from event_bus import EventBus
            bus = EventBus()
            return (200, "application/json", json.dumps({"events": bus.get_recent_events(50)}, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"events": []}).encode("utf-8"))

    if path == "/api/skills":
        try:
            from skill_registry import SkillRegistry
            skills = SkillRegistry()
            return (200, "application/json", json.dumps({"skills": skills.skills}, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"skills": ["pdf_playbook", "video_forge", "moltbook", "agentcoin"]}).encode("utf-8"))

    if path == "/api/business/opportunities":
        try:
            from opportunity_discovery import OpportunityDiscoveryEngine
            from opportunity_scoring import OpportunityScoringEngine
            disc = OpportunityDiscoveryEngine()
            scorer = OpportunityScoringEngine()
            ranked = scorer.rank_opportunities(disc.list_opportunities())
            return (200, "application/json", json.dumps({"opportunities": ranked}, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"opportunities": []}).encode("utf-8"))

    if path == "/api/memory":
        try:
            from agent_memory import AgentMemory
            mem = AgentMemory()
            return (200, "application/json", json.dumps(mem.data, indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"memory": "initialized"}).encode("utf-8"))

    if path in ("/api/treasury", "/api/ledger"):
        try:
            from treasury import Treasury
            tr = Treasury()
            return (200, "application/json", json.dumps(tr.get_balance(), indent=2).encode("utf-8"))
        except Exception:
            return (200, "application/json", json.dumps({"balance": 0.0, "currency": "USD"}).encode("utf-8"))

    return (404, "application/json", json.dumps({"error": "Endpoint Not Found", "path": path}).encode("utf-8"))


# --- BaseHTTPRequestHandler Handler for Vercel ---
class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        status, content_type, body = handle_api_route(parsed.path, urllib.parse.parse_qs(parsed.query))
        
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        status, content_type, body = handle_api_route(parsed.path)
        
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


# --- WSGI App for Vercel / Standard Python Servers ---
def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    query = environ.get("QUERY_STRING", "")
    params = urllib.parse.parse_qs(query)
    
    status_code, content_type, body = handle_api_route(path, params)
    status_text = "200 OK" if status_code == 200 else ("404 Not Found" if status_code == 404 else f"{status_code} Status")
    
    headers = [
        ("Content-Type", content_type),
        ("Access-Control-Allow-Origin", "*"),
        ("Content-Length", str(len(body)))
    ]
    start_response(status_text, headers)
    return [body]
