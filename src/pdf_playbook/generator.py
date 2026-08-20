from __future__ import annotations

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
DISCLAIMER = "AgentBroko is a platform for generating documents. Users are solely responsible for the content they create, publish, sell, or otherwise use."

PAGES = [
    ("What You’ll Learn", "A practical path from account setup to a reliable coding loop.", [
        ("AgentRouter", "A model-routing layer with an account dashboard, API credentials, and provider/model choices that may change over time."),
        ("Cline", "A VS Code coding agent that can inspect a project, plan changes, edit files, run commands, and review results with your approval."),
        ("The outcome", "You will verify credits, connect a model, send a safe first request, and use a plan-first workflow that keeps context and spend under control."),
    ]),
    ("AI Credits Overview", "Treat promotional credits as a usage allowance, not cash.", [
        ("Verify in the dashboard", "Current balances, eligibility, expiration, supported models, and terms belong in the live AgentRouter account and documentation."),
        ("Usage is variable", "Requests consume credits according to the selected model, context size, output length, provider rules, and any current promotion."),
        ("No invented numbers", "This guide intentionally does not promise a credit amount, price, duration, or model availability."),
    ]),
    ("AgentRouter Overview", "Understand the routing layer before wiring it into an editor.", [
        ("Account dashboard", "Use it to inspect available models, API keys, usage, credit balance, and current account notices."),
        ("Routing concept", "Your client sends a request to an AgentRouter endpoint; AgentRouter authenticates it and routes it to the chosen provider/model."),
        ("Configuration", "The exact provider label, base URL, model identifier, and key format can change. Copy current values from the dashboard or docs."),
    ]),
    ("Create Your AgentRouter Account", "Use the current interface as the authority.", [
        ("1. Open the official entry point", "Navigate to the AgentRouter site or link supplied by the current promotion. Confirm the domain before entering credentials."),
        ("2. Register and verify", "Create the account, verify the email if requested, and complete only the profile fields required for access."),
        ("3. Capture the baseline", "Record the displayed balance, account status, and any expiration or eligibility notice before creating a key."),
        ("Screenshot placeholder", "[Insert screenshot: AgentRouter account dashboard with sensitive values blurred]"),
    ]),
    ("Claim / Verify AI Credits", "A checklist for promotional access.", [
        ("1. Read the offer", "Open the current promotion details. Note eligibility, activation steps, expiration, eligible models, and restrictions."),
        ("2. Activate only in the official flow", "Use the dashboard control or documented redemption path. Do not paste keys into third-party forms."),
        ("3. Confirm activation", "Return to the balance/usage view and confirm that the credit status changed. Save a private screenshot for your records."),
        ("Troubleshooting", "If the offer is missing, check account eligibility, region, email verification, and promotion dates before contacting support."),
    ]),
    ("Check Your Credit Balance", "Make balance checks part of your development loop.", [
        ("Before coding", "Open the dashboard usage/billing view and record the current balance and reset/expiration date if shown."),
        ("After a test", "Refresh the view after the first request. Large context windows and long outputs can consume more allowance than expected."),
        ("Before a large task", "Choose a smaller model for exploration, estimate the work in stages, and keep a buffer for testing and review."),
    ]),
    ("Understanding Models", "Choose by task, not by hype.", [
        ("Claude-family models", "Often useful for long-form reasoning, code review, and working through larger coherent changes. Verify current availability and limits."),
        ("GPT-family models", "Useful for general coding, structured planning, debugging, and tool-oriented workflows. Verify current model names and routing support."),
        ("DeepSeek and other models", "Can be attractive for exploration or cost-sensitive work. Validate output quality, context limits, latency, and current availability."),
        ("Selection rule", "Use a capable model for architecture and review; use a lighter available model for small edits, formatting, and repetitive tasks."),
    ]),
    ("Install Visual Studio Code", "Prepare a clean workspace.", [
        ("1. Install", "Download VS Code from the official Microsoft source for your operating system and complete the standard installer."),
        ("2. Open a project", "Use File > Open Folder and open a repository you trust. Confirm the active folder before allowing tools to run."),
        ("3. Prepare the terminal", "Open the integrated terminal and verify your runtime, package manager, Git identity, and test command."),
        ("4. Safety defaults", "Keep auto-approval conservative until you understand what Cline is proposing and which files/commands it will touch."),
    ]),
    ("Install Cline", "Add the coding agent to VS Code.", [
        ("1. Extensions", "Open Extensions, search for the current official Cline extension, verify publisher details, and install it."),
        ("2. Open the panel", "Launch Cline from the activity bar. Read the current provider configuration labels in the extension UI."),
        ("3. Start with review", "Use plan/read-only behavior first. Let Cline inspect the project before enabling edits or command execution."),
        ("Screenshot placeholder", "[Insert screenshot: Cline settings panel with key values redacted]"),
    ]),
    ("Connect AgentRouter to Cline", "Configuration workflow with change-resistant placeholders.", [
        ("Provider", "Select the provider option that corresponds to AgentRouter, or choose the custom/OpenAI-compatible option if the current Cline UI documents that path."),
        ("API key", "Paste the newly created key into Cline's secure key field. Never put it in a prompt, source file, screenshot, or committed settings file."),
        ("Base URL / endpoint", "Enter the current AgentRouter base URL: [VERIFY CURRENT AGENTROUTER BASE URL]. Do not assume an old endpoint."),
        ("Model", "Copy the exact current model identifier from AgentRouter: [VERIFY CURRENT MODEL ID]. Start with a small test request."),
        ("Authentication", "Save, then confirm the extension reports a configured provider without exposing the key in logs."),
    ]),
    ("First Successful Request", "Prove the connection with a low-risk request.", [
        ("Prompt", "Read the repository structure. Summarize the entry points, test command, and three likely files for adding a small feature. Do not edit files or run commands."),
        ("Expected behavior", "Cline should acknowledge the configured model, inspect the workspace, and return a bounded summary without changing files."),
        ("If it fails", "Check provider, base URL, exact model ID, key validity, balance, rate limits, and whether the workspace is trusted."),
    ]),
    ("Plan First, Code Smarter", "Planning is a spend-control and quality-control tool.", [
        ("Prompt pattern", "Analyze this project, identify the architecture, propose a plan, and wait for approval before making changes."),
        ("Require a plan", "Ask for files to change, assumptions, risks, test strategy, and a rollback path. Reject vague plans before implementation."),
        ("Approve in slices", "Approve one coherent slice at a time. This keeps context focused and makes it easier to catch wrong assumptions early."),
    ]),
    ("Build a Real Feature", "A repeatable requirement-to-release loop.", [
        ("Requirement", "Describe the user problem, acceptance criteria, constraints, and out-of-scope behavior."),
        ("Planning", "Ask Cline to map the existing architecture and propose the smallest safe change."),
        ("Implementation", "Approve the plan, let Cline edit only the named files, and inspect each diff."),
        ("Testing", "Run the focused test first, then the broader suite. Ask Cline to explain failures before changing more code."),
        ("Review", "Request a security, edge-case, and maintainability review. Commit only after the working tree is understood."),
    ]),
    ("Token / Credit Optimization", "Spend on decisions, not repeated context.", [
        ("Plan before coding", "A short plan prevents expensive wrong turns."),
        ("Keep context focused", "Reference the relevant files and symbols instead of attaching the whole repository."),
        ("Break large work apart", "Use architecture, implementation, test, and review passes."),
        ("Match model to task", "Reserve the strongest available model for high-risk reasoning and review."),
        ("Review before expensive operations", "Confirm the diff and command before running builds, migrations, or broad test suites."),
    ]),
    ("Troubleshooting", "Work from the outside in.", [
        ("Invalid key / authentication", "Create a fresh key, verify it is active, and re-enter it in the secure field. Never print it for debugging."),
        ("Incorrect endpoint", "Copy the current documented base URL exactly, including path requirements."),
        ("Model unavailable", "Refresh the model list and select an identifier currently shown by AgentRouter."),
        ("Insufficient credits / rate limit", "Check balance, promotion status, usage spikes, request size, and current provider limits."),
        ("Cline not responding", "Check the extension log, network access, workspace trust, provider selection, and whether the request is still processing."),
    ]),
    ("Security Best Practices", "Treat keys like production credentials.", [
        ("Never expose API keys", "Do not paste keys into prompts, screenshots, issues, chat, or source code."),
        ("Use secret storage", "Prefer Cline's secure settings or environment variables appropriate to your operating system."),
        ("Prevent commits", "Use .gitignore and secret scanning. Check `git diff` before every commit."),
        ("Rotate quickly", "Revoke and replace a key if it may have been exposed. Review usage after rotation."),
    ]),
    ("Advanced Workflow", "Plan -> Implement -> Test -> Review -> Refactor -> Commit", [
        ("Architecture", "Map the current boundaries, dependencies, data flow, and likely failure points."),
        ("Debugging", "Reproduce the issue, identify the smallest failing surface, propose hypotheses, then test one at a time."),
        ("Code review", "Review the diff for correctness, security, performance, edge cases, and test coverage."),
        ("Testing", "Add focused tests for the changed behavior, then run the project's standard validation command."),
    ]),
    ("Quick Reference", "Keep this page beside your terminal.", [
        ("AgentRouter", "Create account -> verify offer -> create key -> check balance -> copy current endpoint/model."),
        ("Cline", "Install official extension -> select provider -> secure key -> current endpoint -> exact model ID."),
        ("Model choice", "Strong model for architecture/review; lighter model for small edits and repetitive tasks."),
        ("Errors", "Recheck key, endpoint, model availability, balance, limits, workspace trust, and logs."),
        ("Security", "No keys in code, prompts, screenshots, commits, or public logs."),
    ]),
]

class PlaybookDoc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=17*mm, bottomMargin=17*mm)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="playbook", frames=frame, onPage=self._chrome)])

    def _chrome(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(colors.HexColor("#080d1b")); canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#263356")); canvas.setLineWidth(.4)
        for x in range(0, int(w), 32): canvas.line(x, h-22*mm, x+10, h-22*mm)
        canvas.setFillColor(colors.HexColor("#8dff5a")); canvas.setFont("Helvetica-Bold", 7.5); canvas.drawString(17*mm, 9*mm, BRAND.upper())
        canvas.setFillColor(colors.HexColor("#93a4c6")); canvas.setFont("Helvetica", 7.5); canvas.drawRightString(w-17*mm, 9*mm, f"{doc.page:02d}  /  20")
        canvas.restoreState()

def _styles():
    base = getSampleStyleSheet()
    return {
        "eyebrow": ParagraphStyle("eyebrow", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.HexColor("#8dff5a"), spaceAfter=9),
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=colors.white, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontSize=11, leading=15, textColor=colors.HexColor("#b9c6df"), spaceAfter=18),
        "h": ParagraphStyle("h", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.white, spaceAfter=5),
        "lead": ParagraphStyle("lead", parent=base["Normal"], fontSize=10, leading=14, textColor=colors.HexColor("#aebbd4"), spaceAfter=11),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=9.4, leading=13, textColor=colors.HexColor("#edf2ff"), spaceAfter=5),
        "label": ParagraphStyle("label", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.HexColor("#6cb8ff"), spaceAfter=2),
        "code": ParagraphStyle("code", parent=base["Code"], fontName="Courier", fontSize=8.2, leading=11, textColor=colors.HexColor("#d6f7c1"), backColor=colors.HexColor("#111a2e"), borderPadding=9, leftIndent=2, rightIndent=2),
        "small": ParagraphStyle("small", parent=base["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#9eacc7")),
    }

def generate_playbook(output: str | Path, answers: dict[str, str] | None = None, *, remove_branding: bool = False) -> Path:
    if remove_branding:
        raise ValueError("Branding removal is reserved for a future premium edition.")
    answers = answers or {}
    guide_title = answers.get("title", "AGENTROUTER + CLINE AI CREDITS DEVELOPER PLAYBOOK")
    core_promise = answers.get("topic", "Step-by-step guide to claim AI credits, connect Cline, and supercharge your coding workflow.")
    audience = answers.get("audience", "Developers new to AgentRouter and Cline")
    out = Path(output); out.parent.mkdir(parents=True, exist_ok=True)
    s = _styles(); story = []
    # Cover
    story += [Spacer(1, 36*mm), Paragraph("AGENTBROKO / DEVELOPER EDITION", s["eyebrow"]), Paragraph(guide_title.upper().replace(" + ", " +<br/>").replace(" AI CREDITS ", "<br/>AI CREDITS<br/>"), s["title"]), Paragraph(core_promise, s["subtitle"]), Spacer(1, 12*mm), Paragraph(f"FOR: {audience.upper()}", s["eyebrow"]), Spacer(1, 8*mm), Paragraph(BRAND, s["label"]), Paragraph("Build with clarity. Keep control of context, credentials, and cost.", s["lead"]), PageBreak()]
    for idx, (title, lead, items) in enumerate(PAGES, start=2):
        story += [Paragraph(f"PLAYBOOK / {idx-1:02d}", s["eyebrow"]), Paragraph(title, s["h"]), Paragraph(lead, s["lead"])]
        rows=[]
        for label, text in items:
            rows.append([Paragraph(label, s["label"]), Paragraph(text, s["body"])])
        tbl=Table(rows, colWidths=[43*mm, 118*mm]); tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#111a2e")),("BOX",(0,0),(-1,-1),.5,colors.HexColor("#344771")),("INNERGRID",(0,0),(-1,-1),.25,colors.HexColor("#263356")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)])); story += [tbl]
        if title == "First Successful Request": story += [Spacer(1,8), Preformatted("Read the repository structure. Summarize the entry points, test command, and three likely files for adding a small feature.\nDo not edit files or run commands.", s["code"])]
        if title == "Advanced Workflow": story += [Spacer(1,8), Preformatted("Plan -> Implement -> Test -> Review -> Refactor -> Commit", s["code"])]
        story += [PageBreak()]
    story += [Paragraph("SHIP WITH CONTROL", s["eyebrow"]), Paragraph("Build More. Spend Less. Ship Faster.", s["title"]), Paragraph("AgentBroko helps developers turn careful prompts into useful, reviewable work. Keep your credentials private, verify live provider terms, and make every generated artifact your responsibility.", s["subtitle"]), Spacer(1, 12*mm), Paragraph(BRAND, s["label"]), Paragraph(URL, s["body"]), Spacer(1, 14*mm), Paragraph(DISCLAIMER, s["small"])]
    PlaybookDoc(str(out)).build(story)
    return out
