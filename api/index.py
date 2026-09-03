"""
AgentBroko Vercel Serverless API & Web Studio Engine
Serves Video Forge & PDF Playbook Studio UI on /
Exposes endpoints:
- POST /api/generate/video -> Generates structured Video Forge timeline project & SRT
- GET /api/generate/pdf -> Generates and streams formatted binary PDF using ReportLab
- GET /api/skills -> Lists available skills
- GET /api/health -> System health status
"""

import http.server
import io
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

APP_HTML_PATH = os.path.join(ROOT_DIR, "static", "app.html")

CHATGPT_OPENAPI = {
    "openapi": "3.0.3",
    "info": {
        "title": "AgentBroko",
        "version": "1.4.2",
        "description": "Generate local-first video project blueprints and discover AgentBroko skills.",
    },
    "servers": [{"url": "https://agentbroko.vercel.app"}],
    "paths": {
        "/api/generate/video": {
            "post": {
                "operationId": "generateVideoProject",
                "summary": "Generate a structured Video Forge project",
                "description": "Creates a video project blueprint and SRT subtitles from a brief. It does not upload or render user media.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/VideoRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Generated project blueprint",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VideoResponse"}}},
                    }
                },
            }
        },
        "/api/skills": {
            "get": {
                "operationId": "listSkills",
                "summary": "List available AgentBroko skills",
                "responses": {"200": {"description": "Skill registry", "content": {"application/json": {"schema": {"type": "object"}}}}},
            }
        },
        "/api/health": {
            "get": {
                "operationId": "checkHealth",
                "summary": "Check AgentBroko availability",
                "responses": {"200": {"description": "Health status", "content": {"application/json": {"schema": {"type": "object"}}}}},
            }
        },
    },
    "components": {
        "schemas": {
            "VideoRequest": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The video concept or production brief."},
                    "aspect": {"type": "string", "enum": ["9:16", "16:9"]},
                    "style": {"type": "string"},
                    "duration": {"type": "integer", "minimum": 3, "maximum": 300},
                    "voice": {"type": "string"},
                    "captions": {"type": "string"},
                },
                "required": ["prompt"],
            },
            "VideoResponse": {
                "type": "object",
                "required": ["project", "scenes", "srt", "duration"],
                "properties": {
                    "project": {"type": "object"},
                    "scenes": {"type": "array", "items": {"type": "object"}},
                    "srt": {"type": "string"},
                    "duration": {"type": "integer"},
                },
            },
        }
    },
}

CHATGPT_PLUGIN_MANIFEST = {
    "schema_version": "v1",
    "name_for_model": "agentbroko",
    "name_for_human": "AgentBroko",
    "description_for_model": "Generate local-first Video Forge project blueprints and list AgentBroko skills. Use for video concepts, storyboards, captions, and production planning.",
    "description_for_human": "Create video project blueprints and discover local-first creative skills.",
    "auth": {"type": "none"},
    "api": {"type": "openapi", "url": "https://agentbroko.vercel.app/openapi.json", "has_user_authentication": False},
    "logo_url": "https://agentbroko.vercel.app/icon.png",
    "contact_email": "brokeinnovation@gmail.com",
    "legal_info_url": "https://agentbroko.vercel.app/TERMS.md",
}

def get_app_html():
    if os.path.exists(APP_HTML_PATH):
        try:
            with open(APP_HTML_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return "<html><body><h1>AgentBroko Studio</h1><p>Video Forge & PDF Playbook</p></body></html>"

# ----------------------------------------------------------------------------
# In-Memory ReportLab PDF Generator
# ----------------------------------------------------------------------------
def generate_pdf_binary(title="AgentBroko Developer Handbook", audience="Developers & AI Engineers", topics="AI Agent Skills, Video Forge, Automation"):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CoverTitle',
            parent=styles['Heading1'],
            fontSize=26,
            leading=32,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=12
        )
        subtitle_style = ParagraphStyle(
            'CoverSub',
            parent=styles['Normal'],
            fontSize=13,
            leading=18,
            textColor=colors.HexColor('#475569'),
            spaceAfter=20
        )
        h2_style = ParagraphStyle(
            'ChapterH2',
            parent=styles['Heading2'],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=14,
            spaceAfter=8
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )

        story = []
        # Header / Brand
        story.append(Paragraph("<b>AGENTBROKO</b> • Open AI Skills Platform", ParagraphStyle('Brd', fontSize=9, textColor=colors.HexColor('#8B5CF6'), spaceAfter=14)))
        story.append(Paragraph(f"{title}", title_style))
        story.append(Paragraph(f"<b>Target Audience:</b> {audience}<br/><b>Key Focus:</b> {topics}", subtitle_style))
        story.append(Spacer(1, 15))

        # Overview Table
        table_data = [
            ["Chapter", "Core Focus", "Outcome"],
            ["1. Architecture", "Deterministic Agent Loops & Skills Hub", "Reliable Local Execution"],
            ["2. Video Forge", "Procedural 60 FPS Video Generation", "Broadcast-Grade MP4 Output"],
            ["3. PDF Playbook", "ReportLab Document Synthesis", "Zero Cloud Document Creation"],
            ["4. Production", "Spend Control & Error Remediation", "Safe Continuous Deployment"]
        ]
        t = Table(table_data, colWidths=[110, 240, 160])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        story.append(Paragraph("Chapter 1: The Local-First Architecture", h2_style))
        story.append(Paragraph("AgentBroko introduces a modular, zero-telemetry skill execution architecture. Rather than relying on fragile cloud endpoints, all core generators (Video Forge and PDF Playbook) compile and render directly on local runtime infrastructure or serverless execution units.", body_style))
        
        story.append(Paragraph("Chapter 2: Production Video Automation Workflow", h2_style))
        story.append(Paragraph("Using Video Forge, creators and autonomous coding agents can translate high-level natural language prompts into complete, frame-by-frame JSON specifications with kinetic typography, audio ducking, and synchronized multi-layer compositing.", body_style))

        story.append(Spacer(1, 15))
        story.append(Paragraph("<i>Generated by AgentBroko Studio • MIT Licensed • https://github.com/sajidhossain8272/agentbroko</i>", ParagraphStyle('Foot', fontSize=8, textColor=colors.HexColor('#94A3B8'))))

        doc.build(story)
        return buf.getvalue()
    except Exception as e:
        return b"%PDF-1.4 Empty fallback PDF due to generation error"

# ----------------------------------------------------------------------------
# Algorithmic Video Project Synthesizer
# ----------------------------------------------------------------------------
def synthesize_video_project(prompt, aspect="9:16", style="minimal_tech", duration=30, voice="windows", captions="kinetic"):
    is_vertical = (aspect == "9:16")
    width = 1080 if is_vertical else 1920
    height = 1920 if is_vertical else 1080
    num_scenes = max(3, round(duration / 7.5))
    scene_dur = duration / num_scenes

    scenes = []
    p_short = prompt.strip()[:45]

    for i in range(num_scenes):
        start = i * scene_dur
        end = (i + 1) * scene_dur
        if i == 0:
            title = "Scene 1: Hook & Cold Open"
            main_text = f"Stop Doing It Manually ⚡"
            sub_text = f"Transforming {p_short}"
            vo = f"Imagine creating complete broadcast videos with just one prompt."
            trans = "Dream Flare Crossfade"
        elif i == num_scenes - 1:
            title = f"Scene {num_scenes}: Call To Action"
            main_text = "Start Forging Today 🚀"
            sub_text = "npx agentbroko video-forge"
            vo = "Get started now with npx agentbroko. Open source and local first."
            trans = "Heart Bloom / Outro Fade"
        else:
            title = f"Scene {i + 1}: Feature Breakdown"
            main_text = f"Instant Automation #{i}"
            sub_text = "Procedural 60 FPS Engine"
            vo = f"In this step, we automate rendering with zero cloud dependencies."
            trans = "Ken Burns Push"

        scene_data = {
            "index": i + 1,
            "title": title,
            "start": f"{start:.1f}",
            "end": f"{end:.1f}",
            "duration": f"{scene_dur:.1f}",
            "main_text": main_text,
            "sub_text": sub_text,
            "narration": vo,
            "transition": trans,
            "color_accent": "#8b5cf6" if i % 2 == 0 else "#06b6d4"
        }
        scenes.append(scene_data)

    project_json = {
        "title": p_short or "Video Forge Project",
        "video": {
            "width": width,
            "height": height,
            "fps": 60,
            "target_seconds": duration,
            "aspect_ratio": aspect
        },
        "style": style,
        "audio": {
            "narration": "audio/narration.wav",
            "voice_engine": voice,
            "music": "audio/bed.mp3",
            "music_volume": 0.15
        },
        "subtitles": "captions/subtitles.srt",
        "scenes": scenes
    }

    srt_lines = []
    for idx, s in enumerate(scenes):
        s_start = float(s["start"])
        s_end = float(s["end"])
        s_min, s_sec = int(s_start // 60), int(s_start % 60)
        e_min, e_sec = int(s_end // 60), int(s_end % 60)
        srt_lines.append(f"{idx + 1}\n00:{s_min:02d}:{s_sec:02d},000 --> 00:{e_min:02d}:{e_sec:02d},000\n{s['main_text']}\n{s['sub_text']}\n")

    return {
        "project": project_json,
        "scenes": scenes,
        "srt": "\n".join(srt_lines),
        "duration": duration
    }

# ----------------------------------------------------------------------------
# Master HTTP Router
# ----------------------------------------------------------------------------
def handle_api_route(path, query_params=None, post_data=None):
    if query_params is None:
        query_params = {}
        
    # 1. Main Web Studio Page
    if path in ("/", "/index.html", "/app", "/studio"):
        return (200, "text/html; charset=utf-8", get_app_html().encode("utf-8"))

    if path == "/openapi.json":
        return (200, "application/json", json.dumps(CHATGPT_OPENAPI, indent=2).encode("utf-8"))

    if path == "/.well-known/ai-plugin.json":
        return (200, "application/json", json.dumps(CHATGPT_PLUGIN_MANIFEST, indent=2).encode("utf-8"))

    # 2. PDF Direct Download Endpoint
    if path == "/api/generate/pdf":
        title = query_params.get("title", ["AgentBroko Playbook"])[0] if isinstance(query_params.get("title"), list) else query_params.get("title", "AgentBroko Playbook")
        audience = query_params.get("audience", ["Developers & Creators"])[0] if isinstance(query_params.get("audience"), list) else query_params.get("audience", "Developers & Creators")
        topics = query_params.get("topics", ["AI Skills, Video Forge"])[0] if isinstance(query_params.get("topics"), list) else query_params.get("topics", "AI Skills, Video Forge")
        
        pdf_bytes = generate_pdf_binary(title, audience, topics)
        return (200, "application/pdf", pdf_bytes)

    # 3. Video Forge Project Generation Endpoint
    if path == "/api/generate/video":
        prompt = "Viral Tech Video"
        aspect = "9:16"
        style = "minimal_tech"
        duration = 30
        voice = "windows"
        captions = "kinetic"

        if post_data:
            try:
                data = json.loads(post_data.decode("utf-8")) if isinstance(post_data, bytes) else post_data
                prompt = data.get("prompt", prompt)
                aspect = data.get("aspect", aspect)
                style = data.get("style", style)
                duration = int(data.get("duration", duration))
                voice = data.get("voice", voice)
                captions = data.get("captions", captions)
            except Exception:
                pass

        result = synthesize_video_project(prompt, aspect, style, duration, voice, captions)
        return (200, "application/json", json.dumps(result, indent=2).encode("utf-8"))

    # 4. System Health Check
    if path in ("/api/health", "/api/status"):
        payload = {
            "status": "ONLINE",
            "service": "AgentBroko Studio",
            "version": "1.1.0",
            "environment": "Vercel Serverless",
            "skills": ["video_forge", "pdf_playbook", "pdf_tools"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return (200, "application/json", json.dumps(payload, indent=2).encode("utf-8"))

    # 5. Skills Registry
    if path == "/api/skills":
        payload = {
            "skills": [
                {
                    "name": "video-forge",
                    "description": "Local-first video editing & AI storyboard generator for 9:16 vertical and 16:9 videos",
                    "cli": "npx agentbroko video-forge"
                },
                {
                    "name": "pdf-playbook",
                    "description": "Multi-page developer handbook & documentation PDF generator powered by ReportLab",
                    "cli": "npx agentbroko pdf-playbook"
                },
                {
                    "name": "pdf-tools",
                    "description": "Offline PDF text extraction, info inspection, and page rendering",
                    "cli": "npx agentbroko pdf text <file>"
                }
            ]
        }
        return (200, "application/json", json.dumps(payload, indent=2).encode("utf-8"))

    return (404, "application/json", json.dumps({"error": "Endpoint Not Found", "path": path}).encode("utf-8"))


# --- BaseHTTPRequestHandler Handler for Vercel ---
class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        status, content_type, body = handle_api_route(parsed.path, urllib.parse.parse_qs(parsed.query))
        
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        if "pdf" in content_type:
            self.send_header("Content-Disposition", 'attachment; filename="AgentBroko_Playbook.pdf"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b""
        
        status, content_type, body = handle_api_route(parsed.path, post_data=post_body)
        
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
    
    post_data = None
    if environ.get("REQUEST_METHOD") == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            post_data = environ["wsgi.input"].read(content_length)
        except Exception:
            post_data = None
            
    status_code, content_type, body = handle_api_route(path, params, post_data)
    status_text = "200 OK" if status_code == 200 else ("404 Not Found" if status_code == 404 else f"{status_code} Status")
    
    headers = [
        ("Content-Type", content_type),
        ("Access-Control-Allow-Origin", "*"),
        ("Content-Length", str(len(body)))
    ]
    if "pdf" in content_type:
        headers.append(("Content-Disposition", 'attachment; filename="AgentBroko_Playbook.pdf"'))
        
    start_response(status_text, headers)
    return [body]
