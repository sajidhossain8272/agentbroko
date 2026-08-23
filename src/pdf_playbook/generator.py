from __future__ import annotations

import json
import os
import urllib.request
import urllib.parse
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Preformatted
)

BRAND = "AgentBroko by Broke Innovation"
URL = "https://github.com/sajidhossain8272/agentbroko"
DISCLAIMER = "AgentBroko is an open skills platform for generating structured media and documents. Users are responsible for the content they generate."


def _fetch_ai_playbook_pages(title: str, audience: str, topic: str, api_key: str | None = None) -> list[tuple[str, str, list[tuple[str, str]]]] | None:
    """Attempt to generate customized 18-chapter playbook using Gemini or OpenAI API if key is available."""
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        try:
            prompt = f"""You are an expert technical curriculum and playbook author. Generate an 18-page comprehensive guide structure for a publication-ready 20-page document.
Title: {title}
Audience: {audience}
Core Promise / Topic: {topic}

Return ONLY valid JSON (no markdown formatting, no code fences) with an array of exactly 18 objects.
Each object must have:
- "title": Chapter Title (string, max 40 chars)
- "lead": Short one-sentence executive summary (string, max 100 chars)
- "items": Array of 3 to 4 [Label, Description] pairs:
  [["Label 1", "Detailed practical explanation tailored to {audience}"], ...]
"""
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "responseMimeType": "application/json"}
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as response:
                result = json.loads(response.read().decode("utf-8"))
                text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text_content)
                if isinstance(data, list) and len(data) >= 10:
                    pages = []
                    for item in data:
                        pages.append((
                            item.get("title", "Chapter Guide"),
                            item.get("lead", "Practical walkthrough and instructions."),
                            item.get("items", [["Key Point", "Guidance for this section."]])
                        ))
                    return pages
        except Exception:
            pass

    # OpenAI API Fallback if OPENAI_API_KEY is available
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You generate structured 18-chapter book blueprints as JSON arrays of objects with {title, lead, items: [[label, text], ...]}"},
                    {"role": "user", "content": f"Title: {title}\nAudience: {audience}\nTopic: {topic}"}
                ],
                "response_format": {"type": "json_object"}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai_key}"})
            with urllib.request.urlopen(req, timeout=12) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = json.loads(result["choices"][0]["message"]["content"])
                data = content.get("pages") or content.get("chapters") or (content if isinstance(content, list) else [])
                if isinstance(data, list) and len(data) >= 10:
                    pages = []
                    for item in data:
                        pages.append((item.get("title"), item.get("lead"), item.get("items")))
                    return pages
        except Exception:
            pass

    return None


def _synthesize_contextual_pages(title: str, audience: str, topic: str) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """
    Intelligent zero-cloud topic synthesizer.
    Dynamically generates an 18-page comprehensive, structured curriculum tailored to the given topic and audience.
    """
    t_clean = title.strip()
    a_clean = audience.strip()
    p_clean = topic.strip()
    
    # Topic keywords detection
    is_video_streaming = any(k in t_clean.lower() or k in p_clean.lower() for k in ["youtube", "video", "stream", "watch", "channel", "playlist"])
    is_kids = any(k in a_clean.lower() for k in ["kid", "child", "teen", "student", "beginner", "young"])
    is_coding = any(k in t_clean.lower() or k in p_clean.lower() for k in ["code", "agent", "api", "ai", "python", "javascript", "dev", "software"])

    if is_video_streaming and is_kids:
        return [
            ("What You'll Learn", "A fun and safe guide to exploring, watching, and enjoying videos.", [
                ("Getting Started", "How to open the app, search for your favorite cartoons, and play videos safely."),
                ("Finding Great Content", "Discover educational shows, science experiments, gaming tutorials, and music."),
                ("Safety & Smart Habits", "How to protect your privacy, balance screen time, and browse with confidence.")
            ]),
            ("Getting Started & Navigation", "Master the screen layout, buttons, and finding what you want.", [
                ("Home Screen", "Explore recommended videos, channels, and curated playlists created just for you."),
                ("Search Bar", "Type words or names of shows you love to find matching episodes and creators."),
                ("Voice Search (Microphone)", "Tap the mic icon and speak clearly to find videos without typing."),
                ("Subscriptions Tab", "Keep track of your favorite channels and never miss new episode releases.")
            ]),
            ("The Video Player Controls", "Take full control of playback, sound, and screen size.", [
                ("Play & Pause", "Tap the center of the screen or press Spacebar to start or stop any video instantly."),
                ("Fullscreen Mode", "Tap the square icon in the bottom-right corner to make the video fill your entire screen."),
                ("Replay & Skip", "Double-tap the right side of the screen to jump ahead 10 seconds, or the left side to rewind."),
                ("Volume & Mute", "Use your device volume rocker or the speaker slider to keep audio comfortable and clear.")
            ]),
            ("Subtitles & Closed Captions", "Read along while you watch to improve reading and understand every word.", [
                ("Turning on CC", "Tap the 'CC' button on the video player to turn on subtitles in your language."),
                ("Changing Font & Colors", "Open caption settings to make subtitle text larger and easier to read."),
                ("Learning New Words", "Subtitles help you learn spelling, grammar, and pronunciation while watching."),
                ("Multi-Language Support", "Switch subtitle languages to practice second languages and global shows.")
            ]),
            ("Creating & Managing Playlists", "Save your favorite videos so you can watch them anytime.", [
                ("The 'Save' Button", "Tap 'Save' beneath any video to add it to 'Watch Later' or a custom playlist."),
                ("Making Custom Lists", "Create playlists named 'Favorite Cartoons', 'Science Fun', or 'Lego Builds'."),
                ("Looping Playlists", "Turn on repeat mode to listen to your favorite songs and bedtime stories continuously."),
                ("Sharing with Family", "Show your playlists to parents and friends on family movie nights.")
            ]),
            ("YouTube Kids & Safety Tools", "How to browse in a protected, kid-friendly environment.", [
                ("YouTube Kids App", "A dedicated app with content filtered specifically for children and families."),
                ("Restricted Mode", "Hides potentially mature content and comments across all search queries."),
                ("Content Categories", "Browse by Shows, Music, Learning, and Explore categories safely."),
                ("Timer Feature", "Built-in timers that alert you when screen time is over for healthy habits.")
            ]),
            ("Finding the Best Educational Shows", "Learn science, art, history, and crafts from trusted creators.", [
                ("Science & Nature", "Watch high-quality animal documentaries, space exploration, and physics demonstrations."),
                ("Drawing & Arts", "Follow step-by-step art tutorials to draw cartoon characters and craft DIY projects."),
                ("Math & Coding Fun", "Interactive animations that make math puzzles and computer logic exciting."),
                ("Storytelling & Books", "Animated read-aloud book channels that bring classic and modern stories to life.")
            ]),
            ("Understanding Ads & Safe Clicking", "Learn how ads work and how to stay safe from popups.", [
                ("The 'Skip Ad' Button", "Many video ads can be skipped after 5 seconds by tapping the yellow button."),
                ("Sponsored Content", "Recognize when a creator is sharing a product or toy sponsorship."),
                ("Never Click Unknown Links", "Do not tap on pop-up external download links or strange website banners."),
                ("Ask a Parent", "Whenever an unfamiliar screen or prompt appears, ask a parent or guardian.")
            ]),
            ("Healthy Screen Time Habits", "Balance watching videos with play, exercise, and schoolwork.", [
                ("The 20-20-20 Rule", "Every 20 minutes, look at an object 20 feet away for 20 seconds to rest your eyes."),
                ("Daily Limits", "Set a clear goal for how many episodes or minutes you will watch each day."),
                ("Sleep Hygiene", "Turn off screens at least 30 minutes before bedtime for restful sleep."),
                ("Active Watching", "Try drawing or building along with tutorials rather than only watching passively.")
            ]),
            ("Keyboard Shortcuts & Speed Tips", "Watch like a pro on laptops, Chromebooks, and desktops.", [
                ("Spacebar / 'K'", "Press Space or K to Play and Pause without reaching for the mouse."),
                ("'F' for Fullscreen", "Press F on your keyboard to instantly enter and exit fullscreen mode."),
                ("'M' for Mute", "Press M to instantly mute or unmute the audio sound."),
                ("'J' and 'L' Keys", "Press J to rewind 10 seconds; press L to fast-forward 10 seconds.")
            ]),
            ("Offline Downloads for Road Trips", "Watch your favorite episodes on airplanes, cars, and vacations without Wi-Fi.", [
                ("The Download Button", "Tap the Download arrow beneath eligible videos while connected to home Wi-Fi."),
                ("Downloads Library", "Access all downloaded videos under the 'You' tab without using mobile data."),
                ("Managing Storage", "Delete watched videos to free up storage space on your tablet or phone."),
                ("Quality Selection", "Choose Standard or High Definition based on your available storage.")
            ]),
            ("Exploring Channels & Creators", "Subscribe to your favorite creators safely.", [
                ("Channel Homepages", "Visit creator pages to browse their uploads, community posts, and curated series."),
                ("The Subscribe Button", "Subscribe to trusted educational channels so new videos appear in your feed."),
                ("The Notification Bell", "Turn on notifications if your parents allow you to receive new episode alerts."),
                ("Verified Badges", "Look for checkmarks next to channel names showing official, verified creators.")
            ]),
            ("Voice Search & Audio Features", "Use voice commands to find videos fast.", [
                ("Speaking Clearly", "Hold down the mic button and say show titles clearly like 'Peppa Pig' or 'National Geographic'."),
                ("Multilingual Voice", "Voice search understands multiple accents and languages automatically."),
                ("Audio Descriptions", "Some educational shows offer audio description tracks for accessibility."),
                ("Background Audio", "Listen to audiobooks and podcasts with the screen dimmed safely.")
            ]),
            ("Troubleshooting Video Issues", "Quick fixes when a video won't load or plays slowly.", [
                ("Buffering & Loading Wheel", "Check your Wi-Fi connection or lower video resolution to 720p or 480p."),
                ("No Sound Playing", "Make sure your device mute switch is off and Bluetooth headphones are connected."),
                ("Black Screen Error", "Refresh the web page or restart the app to clear cached video memory."),
                ("App Updates", "Ensure the YouTube app is updated to the latest version in the app store.")
            ]),
            ("Privacy & Online Safety Rules", "Essential rules to protect yourself and your family.", [
                ("Never Share Personal Info", "Never type your real name, address, school, or phone number in search bars or comments."),
                ("Do Not Chat with Strangers", "Avoid private messaging or sharing game codes with unknown users."),
                ("Reporting Inappropriate Videos", "Tap the three dots on any bad video and select 'Report' to notify safety teams."),
                ("Talk to Parents Openly", "If you ever see something that makes you uncomfortable, tell a grown-up immediately.")
            ]),
            ("Mastery Checklist for Kids", "Check off each skill as you become a master video explorer.", [
                ("Skill 1: Basic Navigation", "I can search for a video, play it in fullscreen, and adjust the volume."),
                ("Skill 2: Playlists & Captions", "I know how to turn on subtitles and save videos into my personal playlist."),
                ("Skill 3: Smart Balance", "I take eye breaks every 20 minutes and stop when my screen time timer rings."),
                ("Skill 4: Safety Champion", "I never share private info and always ask an adult if something looks strange.")
            ]),
            ("Frequently Asked Questions", "Answers to common questions young viewers have.", [
                ("Why do videos buffer?", "When internet speeds drop, videos pause to download more data before continuing."),
                ("Can I watch without internet?", "Yes, if you downloaded the video beforehand on your device library."),
                ("Why do some videos have ads?", "Ads help support creators so they can continue making free educational videos."),
                ("How do I find funny cartoons?", "Use specific keywords like 'funny animated short stories' in the search bar.")
            ]),
            ("Summary & Happy Watching!", "Congratulations on mastering your complete video viewing guide.", [
                ("Key Takeaway 1", "Use search, subtitles, and playlists to discover the best shows and educational tutorials."),
                ("Key Takeaway 2", "Protect your eyes and balance your day with creative outdoor play and reading."),
                ("Key Takeaway 3", "Stay safe, follow parental guidelines, and enjoy learning new things every day!")
            ])
        ]

    # Universal General Synthesizer for any other topic
    return [
        (f"What You'll Learn: {t_clean[:30]}", f"A comprehensive roadmap to master {p_clean[:60]} for {a_clean}.", [
            ("Core Objective", f"Master the fundamental techniques, best practices, and practical tools to succeed in {t_clean}."),
            ("Target Outcome", f"You will learn step-by-step methodologies to achieve {p_clean} with maximum efficiency."),
            ("Audience Fit", f"Specifically crafted for {a_clean} to bridge theoretical principles with hands-on application.")
        ]),
        ("Core Foundations & Prerequisites", f"Everything you need before diving into {t_clean}.", [
            ("Initial Setup", "Ensure all required software, tools, credentials, and environments are properly configured."),
            ("Fundamental Concepts", f"Understand the foundational building blocks and key terminology of {t_clean}."),
            ("Environment Verification", "Run baseline diagnostics and health checks to ensure reliability from day one."),
            ("Safety & Risk Controls", "Establish guardrails, backup strategies, and risk mitigation protocols before beginning.")
        ]),
        ("Step-by-Step Practical Walkthrough", "A proven blueprint from initial setup to production success.", [
            ("Phase 1: Preparation", "Define scope, constraints, success metrics, and expected deliverables."),
            ("Phase 2: Execution", "Implement the core workflow in focused, incremental stages with regular validation."),
            ("Phase 3: Review & Refine", "Inspect outcomes, eliminate inefficiencies, and optimize for long-term consistency."),
            ("Phase 4: Scaling Up", "Standardize the workflow into repeatable templates and automated routines.")
        ]),
        ("Key Tools & Technology Stack", f"Essential utilities, platforms, and engines for {a_clean}.", [
            ("Primary Tooling", "Identify the most reliable, industry-standard tools suited for your specific use cases."),
            ("Configuration Standards", "Follow best practices for settings, profiles, and workflow parameters."),
            ("Integration Points", "Connect complementary tools into a cohesive, streamlined pipeline."),
            ("Performance Tuning", "Optimize tool responsiveness, resource allocation, and execution speed.")
        ]),
        ("Best Practices & Pro Tips", "Field-tested strategies for superior results and fewer mistakes.", [
            ("Tip 1: Plan Before Executing", "Investing 10 minutes in upfront planning saves hours of rework and debugging."),
            ("Tip 2: Focus on High-Leverage Tasks", "Prioritize core high-impact milestones before polishing secondary details."),
            ("Tip 3: Maintain Clean Organization", "Keep projects, assets, and documentation structured and well-labeled."),
            ("Tip 4: Continuous Verification", "Validate results at each milestone rather than waiting until the final delivery.")
        ]),
        ("Common Pitfalls & How to Avoid Them", "Learn from common mistakes and keep your projects on track.", [
            ("Pitfall 1: Overcomplicating Setup", "Start with the simplest viable workflow before introducing complex layers."),
            ("Pitfall 2: Neglecting Backups", "Always maintain version history and safe rollback points for critical assets."),
            ("Pitfall 3: Ignoring Audience Context", f"Ensure all output aligns directly with the expectations of {a_clean}."),
            ("Pitfall 4: Inconsistent Habits", "Adopt standardized checklists and routines to maintain high quality.")
        ]),
        ("Workflow Optimization & Automation", "Boost productivity and eliminate manual repetitive friction.", [
            ("Standardizing Templates", "Create reusable starter templates for recurring tasks and project types."),
            ("Automating Bottlenecks", "Use scripts, hotkeys, and automated batch jobs for tedious transformations."),
            ("Batch Processing", "Group similar tasks together to maintain deep focus and reduce context switching."),
            ("Measuring Output Quality", "Track key turnaround times, quality scores, and satisfaction metrics.")
        ]),
        ("Quality Assurance & Review Checklist", "Ensure every deliverable meets the highest standards.", [
            ("Check 1: Structural Integrity", "Verify that all components, files, and outputs are complete and error-free."),
            ("Check 2: Clarity & Consistency", "Review visual and functional clarity across all user-facing surfaces."),
            ("Check 3: Cross-Platform Compatibility", "Test across different devices, resolutions, and operating environments."),
            ("Check 4: Final Sign-off", "Confirm that all original project requirements and promises are fulfilled.")
        ]),
        ("Advanced Capabilities & Deep Dives", "Unlock power-user techniques for next-level mastery.", [
            ("Deep Technique 1", "Master specialized parameters and advanced configurations for edge cases."),
            ("Deep Technique 2", "Implement modular architectures that scale effortlessly as volume increases."),
            ("Deep Technique 3", "Integrate analytics, logging, and performance monitoring into daily workflows."),
            ("Deep Technique 4", "Contribute back to the ecosystem, share templates, and mentor peers.")
        ]),
        ("Security, Privacy & Data Protection", "Keep your credentials, assets, and data safe.", [
            ("Credential Security", "Never expose private keys, passwords, or tokens in public repos or screenshots."),
            ("Data Isolation", "Keep local environments isolated and maintain strict permission boundaries."),
            ("Audit & Review", "Regularly inspect dependencies, installed packages, and active connections."),
            ("Incident Response", "Have a predefined protocol for revoking credentials and recovering data quickly.")
        ]),
        ("Troubleshooting Guide", "Quick diagnostic steps for resolving errors and bottlenecks.", [
            ("Issue: Execution Fails", "Check runtime logs, verify dependencies, and ensure file paths are valid."),
            ("Issue: Performance Slowdowns", "Monitor system CPU/RAM usage, clear caches, and optimize asset sizes."),
            ("Issue: Configuration Errors", "Validate config schemas and restore known-working baseline settings."),
            ("Issue: Inconsistent Results", "Ensure deterministic seed values and verify clean environment variables.")
        ]),
        ("Step-by-Step Action Plan", "Your daily and weekly implementation schedule for maximum retention.", [
            ("Day 1: Setup & Exploration", "Install prerequisites, run diagnostics, and complete your first test project."),
            ("Day 2-3: Core Practice", "Build 2-3 real-world projects following the structured walkthrough steps."),
            ("Day 4-5: Optimization", "Identify friction points, create custom presets, and refine your speed."),
            ("Week 2+: Mastery & Scaling", "Incorporate the workflow into production and train team members.")
        ]),
        ("Mastery Checklist", f"Check off each milestone as you master {t_clean}.", [
            ("Milestone 1: Fundamentals", "I understand the core principles, terminology, and tools required."),
            ("Milestone 2: Execution", "I have successfully completed end-to-end projects with high quality."),
            ("Milestone 3: Troubleshooting", "I can independently diagnose and resolve common errors and bottlenecks."),
            ("Milestone 4: Autonomy", f"I can consistently deliver {p_clean} for {a_clean}.")
        ]),
        ("Frequently Asked Questions", f"Answers to top questions asked by {a_clean}.", [
            ("How long does it take to learn?", "Most practitioners achieve baseline proficiency within 1-2 focused sessions."),
            ("What are the system requirements?", "Standard modern computing hardware with Python 3.10+ or Node 18+."),
            ("Can this be automated via scripts?", "Yes, all workflows support headless non-interactive execution."),
            ("Where can I find additional resources?", "Check the official repository documentation and community guides.")
        ]),
        ("Quick Reference Cheat Sheet", "Keep this summary handy during daily execution.", [
            ("Core Command Loop", "Plan -> Configure -> Execute -> Validate -> Deploy"),
            ("Key Philosophy", "Local-first, privacy-preserving, deterministic, and modular."),
            ("Support & Docs", f"Visit {URL} for updates, guides, and skill releases."),
            ("Safety Reminder", "Always verify inputs and outputs before publishing or distributing.")
        ]),
        ("Summary & Core Takeaways", "Key principles to remember for ongoing success.", [
            ("Principle 1", f"Focus on delivering {p_clean} with consistency, clarity, and quality."),
            ("Principle 2", "Leverage local-first tools to maintain complete privacy and control."),
            ("Principle 3", "Continuous improvement through deliberate practice and automated routines.")
        ]),
        ("Community, Updates & Support", "Stay connected with the latest tools and best practices.", [
            ("GitHub Repository", f"Star and fork {URL} for new releases and issues."),
            ("Package Releases", "Check npm and PyPI regularly for skill updates and improvements."),
            ("Extending Skills", "Contribute your own custom skills using the AgentBroko skill framework."),
            ("Open Source License", "Free to use, modify, and distribute under the MIT License.")
        ]),
        ("Final Certificate & Next Steps", "Congratulations on completing this comprehensive guide.", [
            ("Next Action", f"Apply what you learned today to build your first project in {t_clean}."),
            ("Share Your Work", "Showcase your results, share feedback, and help other developers grow."),
            ("Final Thought", "Build with clarity. Keep control of context, credentials, and cost.")
        ])
    ]


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


def generate_playbook(output: str | Path, answers: dict[str, str] | None = None, *, remove_branding: bool = False, api_key: str | None = None) -> Path:
    if remove_branding:
        raise ValueError("Branding removal is reserved for a future premium edition.")
    answers = answers or {}
    guide_title = answers.get("title", "AI DEVELOPER & AGENT SKILLS PLAYBOOK")
    core_promise = answers.get("topic", "Step-by-step practical guide to mastering your workflow.")
    audience = answers.get("audience", "Developers, Creators & AI Engineers")
    api_key = api_key or answers.get("api_key")

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    s = _styles()
    story = []

    # Dynamic or Contextual 18 Pages
    pages = _fetch_ai_playbook_pages(guide_title, audience, core_promise, api_key=api_key)
    if not pages or len(pages) < 18:
        pages = _synthesize_contextual_pages(guide_title, audience, core_promise)

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
        Paragraph("Build with clarity. Keep control of context, credentials, and cost.", s["lead"]),
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
        Paragraph(f"AgentBroko helps {audience} turn careful prompts into useful, high-impact results. Keep your credentials private, verify live provider terms, and make every generated artifact your responsibility.", s["subtitle"]),
        Spacer(1, 12*mm),
        Paragraph(BRAND, s["label"]),
        Paragraph(URL, s["body"]),
        Spacer(1, 14*mm),
        Paragraph(DISCLAIMER, s["small"])
    ]

    PlaybookDoc(str(out)).build(story)
    return out
