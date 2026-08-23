"""
Generate publication-quality User Journey & Complete Usage Guide PDF using ReportLab.
"""
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

output_pdf = r"c:\Projects\agentbroko\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf"

doc = SimpleDocTemplate(
    output_pdf,
    pagesize=A4,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom Styles
brand_style = ParagraphStyle(
    'BrandHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=12,
    textColor=colors.HexColor('#7C3AED'),
    spaceAfter=6
)

title_style = ParagraphStyle(
    'MainTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=23,
    leading=27,
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'MainSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#475569'),
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=13.5,
    leading=17,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=10,
    spaceAfter=5
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=7,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#334155'),
    spaceAfter=5
)

code_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor('#F8FAFC'),
    spaceAfter=0
)

def make_code_box(code_text):
    lines = code_text.strip().split('\n')
    flowables = []
    for l in lines:
        if l.strip().startswith('#'):
            flowables.append(Paragraph(f'<font color="#94A3B8">{l}</font>', code_style))
        else:
            flowables.append(Paragraph(f'<b>$</b> {l}', code_style))
            
    t = Table([[flowables]], colWidths=[520])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    return t

story = []

# --- Header ---
story.append(Paragraph("AGENTBROKO • LOCAL-FIRST AI SKILLS PLATFORM", brand_style))
story.append(Paragraph("Complete User Journey &amp; Usage Guide", title_style))
story.append(Paragraph("End-to-End Workflow Manual for Video Forge, PDF Playbooks &amp; Offline AI Tooling", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C3AED'), spaceAfter=10))

# --- Section 1: Overview & Value ---
story.append(Paragraph("1. Executive Overview &amp; What Users Get", h1_style))
story.append(Paragraph("AgentBroko provides developers and autonomous coding agents with local-first, privacy-respecting creative skills. All video editing, speech synthesis, and PDF creation run on the user's computer with <b>0 KB external network calls and zero API keys required</b>.", body_style))

summary_table_data = [
    ["Key Pillar", "Technical Guarantee", "Developer Outcome"],
    ["100% Offline Execution", "Zero external network calls (0 KB)", "Full data privacy & offline autonomy"],
    ["Agent-First Architecture", "Deterministic POSIX exit codes & JSON schema", "Seamless integration with Cursor, Cline, Roo"],
    ["Dual Packaging", "NPM global launcher + Python PyPI package", "Run via npx agentbroko or pip install -e ."],
    ["Open Source & Extensible", "MIT Licensed modular skill registration", "Add custom skills in src/agentbroko/cli.py"]
]
t_summary = Table(summary_table_data, colWidths=[120, 200, 200])
t_summary.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ('TOPPADDING', (0, 0), (-1, 0), 4),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('TOPPADDING', (0, 1), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
]))
story.append(t_summary)
story.append(Spacer(1, 10))

# --- Section 2: Journey 1 Install ---
story.append(Paragraph("2. User Journey 1: Installation &amp; Discovery", h1_style))
story.append(Paragraph("Users can run AgentBroko without installation via <code>npx</code> or install globally via npm or pip.", body_style))
story.append(make_code_box("""# Instant trial without install
npx agentbroko skills

# Global NPM install
npm install -g agentbroko
agentbroko skills

# Python package install
git clone https://github.com/sajidhossain8272/agentbroko.git
cd agentbroko
pip install -e ."""))
story.append(Spacer(1, 10))

# --- Section 3: Journey 2 Video Forge ---
story.append(Paragraph("3. User Journey 2: Video Automation with Video Forge", h1_style))
story.append(Paragraph("Video Forge enables humans and coding agents to assemble video timelines, synthesize offline speech, extract subtitles, and render complete MP4 videos.", body_style))

story.append(Paragraph("Step 1: Environment Health Check", h2_style))
story.append(Paragraph("Verifies local FFmpeg, FFprobe, and offline TTS engines:", body_style))
story.append(make_code_box("agentbroko video-forge doctor"))

story.append(Paragraph("Step 2: Scaffold Video Project", h2_style))
story.append(Paragraph("Creates a structured project directory with schema-validated <code>project.json</code> and script file:", body_style))
story.append(make_code_box("agentbroko video-forge init my-video"))

story.append(Paragraph("Step 3: Generate Offline Speech Narration", h2_style))
story.append(Paragraph("Synthesizes speech audio from text using local TTS engines:", body_style))
story.append(make_code_box("agentbroko video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav"))

story.append(Paragraph("Step 4: Generate Synchronized SRT Subtitles", h2_style))
story.append(Paragraph("Creates evenly timed SRT captions directly from script text:", body_style))
story.append(make_code_box("agentbroko video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt"))

story.append(Paragraph("Step 5: Validate and Render Final MP4", h2_style))
story.append(Paragraph("Validates JSON structure and renders broadcast-grade MP4 output:", body_style))
story.append(make_code_box("""# Validate project.json schema
agentbroko video-forge validate my-video/project.json

# Render final MP4 video
agentbroko video-forge render my-video/project.json"""))
story.append(Spacer(1, 10))

# --- Section 4: Journey 3 PDF Playbook ---
story.append(Paragraph("4. User Journey 3: Developer Handbook Generation (PDF Playbook)", h1_style))
story.append(Paragraph("PDF Playbook synthesizes formatted 20-page developer handbooks with tables, checklists, and code layouts via ReportLab.", body_style))
story.append(make_code_box("""# Interactive wizard mode
agentbroko pdf-playbook --output my-guide.pdf

# Non-interactive mode (for automated scripts & CI/CD)
agentbroko pdf-playbook --non-interactive --output production-playbook.pdf"""))
story.append(Spacer(1, 10))

# --- Section 5: Journey 4 PDF Tools ---
story.append(Paragraph("5. User Journey 4: Local Offline PDF Utilities", h1_style))
story.append(Paragraph("Inspect metadata, extract clean text, and render pages offline without third-party API exposure:", body_style))
story.append(make_code_box("""# Inspect metadata & page count
agentbroko pdf info document.pdf

# Extract clean text from PDF
agentbroko pdf text document.pdf --output document.txt

# Render PDF pages to high-res images (requires Poppler)
agentbroko pdf render document.pdf --output rendered-pages/"""))
story.append(Spacer(1, 10))

# --- Section 6: Reference Table ---
story.append(Paragraph("6. Complete Command &amp; Deliverable Reference Table", h1_style))
ref_table_data = [
    ["Command", "Input Argument", "Deliverable Output", "Engine"],
    ["agentbroko skills", "None", "List of available skills", "CLI Registry"],
    ["video-forge doctor", "None", "FFmpeg / TTS status report", "System Probe"],
    ["video-forge init <name>", "Project name", "Folder scaffold & project.json", "Template Engine"],
    ["video-forge speak", "--file or --text", "Clean .wav speech narration", "Windows SAPI / Piper"],
    ["video-forge captions", "--file or --text", "Synchronized .srt subtitle file", "Subtitle Lexer"],
    ["video-forge render", "project.json", "Broadcast-quality final.mp4 video", "FFmpeg Pipeline"],
    ["pdf-playbook", "--output <path>", "20-page formatted .pdf handbook", "ReportLab Engine"],
    ["pdf text", "<file> -o <out>", "Clean UTF-8 extracted text (.txt)", "pypdf Lexer"],
    ["pdf render", "<file> -o <dir>", "High-res rendered page images (.png)", "Poppler pdftoppm"]
]
t_ref = Table(ref_table_data, colWidths=[115, 95, 200, 110])
t_ref.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 7.5),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 3.5),
    ('TOPPADDING', (0, 0), (-1, 0), 3.5),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
    ('TOPPADDING', (0, 1), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
]))
story.append(t_ref)
story.append(Spacer(1, 14))

# --- Footer ---
story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#E2E8F0'), spaceAfter=6))
story.append(Paragraph("<b>AgentBroko</b> • Open Source Skills Hub by Broke Innovation • MIT Licensed • https://github.com/sajidhossain8272/agentbroko", ParagraphStyle('Foot', fontSize=7.5, textColor=colors.HexColor('#64748B'), alignment=1)))

doc.build(story)
print(f"Generated PDF at: {output_pdf}")
print(f"PDF size: {os.path.getsize(output_pdf)} bytes")

# Copy to Video Edit and Brain artifacts directory
shutil.copy2(output_pdf, r"c:\Projects\Video Edit\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf")
brain_art = r"C:\Users\littl\.gemini\antigravity-ide\brain\a334d797-e486-4873-8e2c-ac00a2cebbbe\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf"
shutil.copy2(output_pdf, brain_art)
print("Copied PDF to workspace and brain artifact directories!")
