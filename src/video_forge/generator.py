"""
Prompt-to-video generator module for Video Forge.
Transforms natural language briefs into structured spec.json specifications
and renders broadcast-quality procedural ad / short videos.

Operates with LLMs (Claude, OpenAI, Local OpenAI-compatible) or offline
deterministic template synthesizer when no API key is provided.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema", "spec.schema.json")

SCENE_CATALOG = """\
Scene types (each object needs "type", an optional "act" (light|dark, auto-alternates
if omitted), and "vo" (one or two spoken sentences of narration):

- cold_open   : {glyph:"pause"|"play"|"dot", label?}                 opener, one mark
- statement   : {lines:[1-3 short strings], kicker?, weight?}        the workhorse
- pill_list   : {items:[3-5 short labels]}                           outlined chips
- message     : {message, label?, toggle?, call?}                    chat-bubble beat
- node_stack  : {columns:[{title, rows:[str | [str,str]]}]}          system diagram
- orbit       : {items:[2-4 labels], center:"sphere"}                sphere + features
- waveform    : {text:"one short line"}                              audio/voice beat
- feature_grid: {items:[{title,desc} x2-6], columns?}                "what you get"
- stat        : {value:"99.9%"|"$0"|"10x", caption, sub?}            one big number
- split_compare:{left:{label,value}, right:{label,value,color:"accent"}}  before/after
- cta         : {lines:[1-2], button, url}                           closing call to action
- logo_reveal : {wordmark?, url?, mark:"pause"}                      closing lockup
- screenshot  : {image:"path", caption?}                            only if user supplies an image
"""

STYLE_RULES = """\
STYLE: minimalist premium tech (think a high-end SaaS launch film). Huge negative
space, mostly monochrome with ONE accent colour, short punchy copy (3-6 words per
line), calm confident narration. Alternate light and dark acts for rhythm.

STRUCTURE for a ~{seconds}s ad (~{nscenes} scenes): open with cold_open or a
statement hook; name/introduce the product; show 3-6 capability/benefit beats using
a VARIETY of scene types (don't repeat one type back-to-back); optionally a stat or
split_compare for proof; close with a cta then logo_reveal.

Return ONLY a single JSON object matching the schema. No markdown, no commentary.
Every scene must have a "vo" field. Keep copy specific to the product in the brief.
"""


def build_system_prompt(seconds: int = 60, nscenes: int = 13) -> str:
    return (
        "You are an expert ad creative director and motion designer. You write "
        "specs for a procedural video engine that renders them exactly.\n\n"
        + SCENE_CATALOG + "\n"
        + STYLE_RULES.format(seconds=seconds, nscenes=nscenes)
    )


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        text = re.sub(r"\n```$", "", text.strip())
    if not text.lstrip().startswith("{"):
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            text = m.group(0)
    return json.loads(text)


def generate_offline_spec(brief: str, name: str, accent: str = "#3B5BFF", seconds: int = 60) -> dict:
    """Deterministic offline spec generator that requires zero API keys."""
    title = name if name else "AgentBroko"

    return {
        "brand": {
            "name": title,
            "accent": accent or "#3B5BFF",
            "url": f"https://{name.lower()}.app" if name else "https://agentbroko.vercel.app"
        },
        "video": {
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "target_seconds": seconds,
            "supersample": 1.5
        },
        "voice": {
            "backend": "edge",
            "voice": "en-US-ChristopherNeural",
            "rate": 0
        },
        "music": {
            "file": None,
            "gain_db": -19.0,
            "duck_db": -11.0
        },
        "scenes": [
            {
                "type": "cold_open",
                "act": "light",
                "glyph": "play",
                "label": "INTRODUCING",
                "vo": f"This is {title}. A revolution in speed, clarity, and autonomous execution."
            },
            {
                "type": "statement",
                "act": "dark",
                "kicker": "THE PROBLEM",
                "lines": [
                    {"text": "Most workflows are too slow.", "color": "ink"},
                    {"text": "Complexity kills execution.", "color": "muted"}
                ],
                "vo": "Modern production is fragmented. You spend more time configuring than building."
            },
            {
                "type": "statement",
                "act": "light",
                "kicker": "THE SOLUTION",
                "lines": [
                    {"text": f"Meet {title}.", "color": "ink"},
                    {"text": "Built for high performance.", "color": "accent"}
                ],
                "vo": f"{title} streamlines your entire pipeline into a single, unified local-first workflow."
            },
            {
                "type": "pill_list",
                "act": "dark",
                "items": ["100% Local-First", "High Performance", "Zero Cloud Lock-in", "Instant Output"],
                "vo": "Engineered with four core principles: local execution, raw performance, open architecture, and instant delivery."
            },
            {
                "type": "node_stack",
                "act": "light",
                "columns": [
                    {"title": "Core Ingestion", "rows": ["Data Sources", "Asset Resolver"]},
                    {"title": "Engine Core", "rows": ["Procedural Compositor", "Audio Mixer"]},
                    {"title": "Master Export", "rows": ["60 FPS Video", "AAC Audio Mux"]}
                ],
                "vo": "Our multi-layer procedural pipeline connects your inputs directly to broadcast-ready masters."
            },
            {
                "type": "split_compare",
                "act": "dark",
                "left": {"label": "Traditional Workflow", "value": "Hours", "color": "muted"},
                "right": {"label": f"With {title}", "value": "Seconds", "color": "accent"},
                "arrow": True,
                "vo": "What used to take hours of manual editing now renders in seconds."
            },
            {
                "type": "stat",
                "act": "light",
                "value": "10x",
                "caption": "Faster Production Turnaround",
                "sub": "Zero compromises on quality",
                "vo": "Experience up to ten times faster turnaround with zero compromise on visual quality."
            },
            {
                "type": "cta",
                "act": "dark",
                "lines": [
                    {"text": "Start Building Today", "color": "ink"},
                    {"text": "Free and Open Source", "color": "accent"}
                ],
                "button": "Get Started",
                "url": f"{name.lower()}.app" if name else "agentbroko.vercel.app",
                "vo": f"Get started with {title} today and elevate your production quality."
            },
            {
                "type": "logo_reveal",
                "act": "light",
                "wordmark": title,
                "url": f"https://{name.lower()}.app" if name else "https://agentbroko.vercel.app",
                "mark": "play",
                "vo": f"{title}. Built for creators and autonomous agents."
            }
        ]
    }


def generate_spec_from_brief(
    brief: str,
    name: str = "project",
    accent: Optional[str] = None,
    url: Optional[str] = None,
    seconds: int = 60,
    scenes: int = 9,
) -> dict:
    """Generate a valid spec dict from a prompt using LLM if available, else offline fallback."""
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    llm_base = os.environ.get("LLM_BASE_URL")
    llm_key = os.environ.get("LLM_API_KEY")

    if anthropic_key or (llm_base and llm_key) or openai_key:
        try:
            import requests
            system = build_system_prompt(seconds=seconds, nscenes=scenes)
            user = (f"Brief: {brief}\n\nBrand name: {name}\n"
                    f"Target length: about {seconds} seconds ({scenes} scenes).\n"
                    "Write the spec.json now.")

            if anthropic_key:
                model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
                r = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": anthropic_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                    json={"model": model, "max_tokens": 4096, "system": system, "messages": [{"role": "user", "content": user}]},
                    timeout=60
                )
                r.raise_for_status()
                raw = "".join(b.get("text", "") for b in r.json().get("content", []))
                spec = extract_json(raw)
            else:
                base_url = (llm_base or "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
                auth_key = llm_key or openai_key
                model = os.environ.get("LLM_MODEL") or os.environ.get("OPENAI_MODEL", "gpt-4o")
                r = requests.post(
                    base_url,
                    headers={"Authorization": f"Bearer {auth_key}", "Content-Type": "application/json"},
                    json={"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
                    timeout=60
                )
                r.raise_for_status()
                spec = extract_json(r.json()["choices"][0]["message"]["content"])

            spec.setdefault("brand", {})
            spec["brand"].setdefault("name", name.capitalize())
            if accent:
                spec["brand"]["accent"] = accent
            if url:
                spec["brand"]["url"] = url
            spec.setdefault("video", {})["target_seconds"] = seconds
            return spec
        except Exception as e:
            print(f"[generator] LLM generation failed or unavailable ({e}), using offline template synthesizer.", file=sys.stderr)

    return generate_offline_spec(brief, name, accent=accent or "#3B5BFF", seconds=seconds)
