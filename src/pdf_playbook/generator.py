from __future__ import annotations

import json
import os
import urllib.request
import urllib.parse
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle
)

BRAND = "AgentBroko by Broke Innovation"
URL = "https://github.com/sajidhossain8272/agentbroko"
DISCLAIMER = "AgentBroko is an open skills platform for generating structured media and documents. Users are responsible for the content they generate."


def get_available_ai_engines() -> dict[str, str]:
    """Detect available local or cloud AI engines."""
    engines = {}
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        engines["gemini"] = "Google Gemini API (Environment Variable)"
    if os.environ.get("OPENAI_API_KEY"):
        engines["openai"] = "OpenAI API (Environment Variable)"
    if os.environ.get("ANTHROPIC_API_KEY"):
        engines["anthropic"] = "Anthropic Claude API (Environment Variable)"
        
    # Check if local Ollama is running
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", headers={"User-Agent": "AgentBroko/1.2.0"})
        with urllib.request.urlopen(req, timeout=1.5) as res:
            data = json.loads(res.read().decode("utf-8"))
            models = [m.get("name") for m in data.get("models", [])]
            if models:
                engines["ollama"] = f"Local Ollama (Models found: {', '.join(models[:3])})"
            else:
                engines["ollama"] = "Local Ollama (Running, no models pulled yet)"
    except Exception:
        pass

    return engines


def fetch_ai_playbook_pages(
    title: str,
    audience: str,
    topic: str,
    *,
    api_key: str | None = None,
    provider: str | None = None,
    model: str | None = None
) -> tuple[list[tuple[str, str, list[tuple[str, str]]]], str]:
    """
    Generate 18 meaningful, custom chapters specifically for the topic using AI.
    Never uses hardcoded sample text.
    """
    # 1. Check Gemini API
    gemini_key = api_key if (api_key and not api_key.startswith("sk-") and api_key != "ollama") else (
        os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    )
    if (provider == "gemini" or not provider) and gemini_key:
        try:
            prompt = f"""You are an expert handbook and curriculum author. Generate an 18-chapter comprehensive guide specifically about:
Title: {title}
Audience: {audience}
Core Promise: {topic}

Return ONLY valid JSON (no markdown formatting, no code fences) with an array of exactly 18 objects.
Each object must have:
- "title": Chapter Title (string, max 40 chars)
- "lead": Short one-sentence executive summary (string, max 100 chars)
- "items": Array of 3 to 4 [Label, Description] pairs specifically tailored to {audience} and {title}:
  [["Step 1 / Key Point", "Detailed actionable explanation..."], ...]
"""
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "responseMimeType": "application/json"}
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode("utf-8"))
                text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text_content)
                if isinstance(data, list) and len(data) >= 10:
                    pages = [(item.get("title", f"Chapter {i+1}"), item.get("lead", ""), item.get("items", [])) for i, item in enumerate(data)]
                    return pages, "Google Gemini 1.5 Flash"
        except Exception as e:
            if provider == "gemini":
                raise RuntimeError(f"Gemini API generation failed: {e}")

    # 2. Check OpenAI API
    openai_key = api_key if (api_key and api_key.startswith("sk-")) else os.environ.get("OPENAI_API_KEY")
    if (provider == "openai" or not provider) and openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            payload = json.dumps({
                "model": model or "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You generate structured 18-chapter book blueprints as JSON arrays of objects with {title, lead, items: [[label, text], ...]}"},
                    {"role": "user", "content": f"Title: {title}\nAudience: {audience}\nTopic: {topic}"}
                ],
                "response_format": {"type": "json_object"}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai_key}"})
            with urllib.request.urlopen(req, timeout=25) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = json.loads(result["choices"][0]["message"]["content"])
                data = content.get("pages") or content.get("chapters") or (content if isinstance(content, list) else [])
                if isinstance(data, list) and len(data) >= 10:
                    pages = [(item.get("title", f"Chapter {i+1}"), item.get("lead", ""), item.get("items", [])) for i, item in enumerate(data)]
                    return pages, "OpenAI GPT-4o-mini"
        except Exception as e:
            if provider == "openai":
                raise RuntimeError(f"OpenAI API generation failed: {e}")

    # 3. Check Local Ollama (if requested or if provider is ollama or api_key is ollama)
    if provider == "ollama" or api_key == "ollama":
        try:
            req_tags = urllib.request.Request("http://localhost:11434/api/tags")
            with urllib.request.urlopen(req_tags, timeout=2) as res_tags:
                models_data = json.loads(res_tags.read().decode("utf-8"))
                installed_models = [m.get("name") for m in models_data.get("models", [])]
                chosen_model = model or (installed_models[0] if installed_models else "llama3.2:1b")
                
            prompt = f"""You are an expert handbook author. Generate 18 chapters for a guide on '{title}' for '{audience}' with core promise '{topic}'.
Return JSON with an array named "chapters" containing 18 objects:
- "title": Chapter title
- "lead": Executive summary
- "items": Array of 3 [label, text] pairs tailored specifically to {title}.
Return raw JSON only."""
            
            payload = json.dumps({
                "model": chosen_model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }).encode("utf-8")
            
            req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read().decode("utf-8"))
                response_text = data.get("response", "")
                parsed = json.loads(response_text)
                items_list = parsed.get("chapters") or parsed.get("pages") or (parsed if isinstance(parsed, list) else [])
                if isinstance(items_list, list) and len(items_list) >= 5:
                    pages = [(item.get("title", f"Chapter {i+1}"), item.get("lead", ""), item.get("items", [])) for i, item in enumerate(items_list)]
                    return pages, f"Local Ollama ({chosen_model})"
        except Exception as e:
            raise RuntimeError(f"Local Ollama generation failed ({chosen_model if 'chosen_model' in locals() else 'localhost:11434'}): {e}")

    # No AI engine connected
    raise ValueError(
        "No AI Engine or API Key configured.\n\n"
        "To generate a 100% custom, meaningful handbook for your prompt, AgentBroko requires an AI model:\n"
        "  1. Google Gemini API Key (Free tier at https://aistudio.google.com)\n"
        "     Set in terminal: export GEMINI_API_KEY='your-key' (or $env:GEMINI_API_KEY='your-key')\n"
        "  2. OpenAI API Key\n"
        "     Set in terminal: export OPENAI_API_KEY='sk-...'\n"
        "  3. Local Offline AI with Ollama (100% Free & Local)\n"
        "     Install from https://ollama.com and run: ollama run llama3\n"
        "  4. Or pass a custom JSON spec from your AI coding agent (Cursor, Antigravity, Cline):\n"
        "     agentbroko pdf-playbook --spec playbook_spec.json --output playbook.pdf\n"
    )


class PlaybookDoc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=17*mm, bottomMargin=17*mm)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="playbook", frames=frame, onPage=self._chrome)])

    def _chrome(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(colors.HexColor("#080d1b"))
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#263356"))
        canvas.setLineWidth(.4)
        for x in range(0, int(w), 32):
            canvas.line(x, h-22*mm, x+10, h-22*mm)
        canvas.setFillColor(colors.HexColor("#8dff5a"))
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(17*mm, 9*mm, BRAND.upper())
        canvas.setFillColor(colors.HexColor("#93a4c6"))
        canvas.setFont("Helvetica", 7.5)
        canvas.drawRightString(w-17*mm, 9*mm, f"{doc.page:02d}  /  20")
        canvas.restoreState()


def _styles():
    base = getSampleStyleSheet()
    return {
        "eyebrow": ParagraphStyle("eyebrow", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.HexColor("#8dff5a"), spaceAfter=9),
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=colors.white, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontSize=11, leading=15, textColor=colors.HexColor("#b9c6df"), spaceAfter=18),
        "h": ParagraphStyle("h", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=colors.white, spaceAfter=5),
        "lead": ParagraphStyle("lead", parent=base["Normal"], fontSize=10, leading=14, textColor=colors.HexColor("#aebbd4"), spaceAfter=11),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=9.4, leading=13.5, textColor=colors.HexColor("#edf2ff"), spaceAfter=4),
        "label": ParagraphStyle("label", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.HexColor("#6cb8ff"), spaceAfter=2),
        "code": ParagraphStyle("code", parent=base["Code"], fontName="Courier", fontSize=8.2, leading=11, textColor=colors.HexColor("#d6f7c1"), backColor=colors.HexColor("#111a2e"), borderPadding=9, leftIndent=2, rightIndent=2),
        "small": ParagraphStyle("small", parent=base["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#9eacc7")),
    }


def generate_playbook(
    output: str | Path,
    answers: dict[str, str] | None = None,
    *,
    spec_file: str | Path | None = None,
    remove_branding: bool = False,
    api_key: str | None = None,
    provider: str | None = None,
    model: str | None = None
) -> Path:
    if remove_branding:
        raise ValueError("Branding removal is reserved for a future premium edition.")
        
    answers = answers or {}
    guide_title = answers.get("title", "AI PLAYBOOK")
    core_promise = answers.get("topic", "Step-by-step practical guide to mastering your workflow.")
    audience = answers.get("audience", "Learners & Developers")
    api_key = api_key or answers.get("api_key")

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    s = _styles()
    story = []

    # 1. Spec File Mode (From AI Coding Agent or JSON)
    if spec_file and Path(spec_file).exists():
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_data = json.load(f)
            guide_title = spec_data.get("title", guide_title)
            audience = spec_data.get("audience", audience)
            core_promise = spec_data.get("topic", core_promise)
            raw_pages = spec_data.get("pages") or spec_data.get("chapters", [])
            pages = [(p.get("title", f"Chapter {i+1}"), p.get("lead", ""), p.get("items", [])) for i, p in enumerate(raw_pages)]
            engine_label = "Structured Specification (AI Coding Agent)"
    else:
        # 2. AI Generation Mode (Gemini / OpenAI / Ollama)
        pages, engine_label = fetch_ai_playbook_pages(
            guide_title,
            audience,
            core_promise,
            api_key=api_key,
            provider=provider,
            model=model
        )

    # 1. Cover Page
    story += [
        Spacer(1, 36*mm),
        Paragraph("AGENTBROKO / EDITION", s["eyebrow"]),
        Paragraph(guide_title.upper().replace(" + ", " +<br/>"), s["title"]),
        Paragraph(core_promise, s["subtitle"]),
        Spacer(1, 12*mm),
        Paragraph(f"FOR: {audience.upper()}", s["eyebrow"]),
        Spacer(1, 8*mm),
        Paragraph(BRAND, s["label"]),
        Paragraph(f"Generated via {engine_label}. Build with clarity, control, and precision.", s["lead"]),
        PageBreak()
    ]

    # 2. Pages 2 through 19 (18 Chapters)
    for idx, (title, lead, items) in enumerate(pages[:18], start=2):
        story += [
            Paragraph(f"PLAYBOOK / {idx-1:02d}", s["eyebrow"]),
            Paragraph(title, s["h"]),
            Paragraph(lead or "Practical instructions and guidance.", s["lead"])
        ]
        rows = []
        for item in items:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                label, text = item[0], item[1]
            else:
                label, text = "Key Point", str(item)
            rows.append([Paragraph(str(label), s["label"]), Paragraph(str(text), s["body"])])
            
        tbl = Table(rows, colWidths=[43*mm, 118*mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#111a2e")),
            ("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#344771")),
            ("INNERGRID", (0, 0), (-1, -1), .25, colors.HexColor("#263356")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ]))
        story += [tbl, PageBreak()]

    # 3. Page 20: Conclusion & Sign-off
    story += [
        Spacer(1, 24*mm),
        Paragraph("SHIP WITH CONTROL", s["eyebrow"]),
        Paragraph("Build More. Spend Less. Ship Faster.", s["title"]),
        Paragraph(f"AgentBroko helps {audience} turn careful prompts into useful, high-impact deliverables. Keep your credentials private, verify live provider terms, and make every generated artifact your responsibility.", s["subtitle"]),
        Spacer(1, 12*mm),
        Paragraph(BRAND, s["label"]),
        Paragraph(URL, s["body"]),
        Spacer(1, 14*mm),
        Paragraph(DISCLAIMER, s["small"])
    ]

    PlaybookDoc(str(out)).build(story)
    return out
