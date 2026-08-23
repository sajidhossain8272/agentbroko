"""
Generate complete, unabridged, publication-grade AgentBroko User Journey & Usage Guide PDF.
"""
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

output_pdf = r"c:\Projects\agentbroko\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 810, "AgentBroko • Complete User Journey & Usage Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.drawString(36, 30, "AgentBroko Skills Hub • MIT Licensed • https://github.com/sajidhossain8272/agentbroko")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 30, page_str)
        self.restoreState()

doc = SimpleDocTemplate(
    output_pdf,
    pagesize=A4,
    rightMargin=36,
    leftMargin=36,
    topMargin=46,
    bottomMargin=48
)

styles = getSampleStyleSheet()

# Typography Tokens
brand_style = ParagraphStyle(
    'BrandHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#7C3AED'),
    spaceAfter=4
)

title_style = ParagraphStyle(
    'MainTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
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
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=13.5,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#334155'),
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'BulletText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#334155'),
    leftIndent=12,
    spaceAfter=3
)

code_snippet_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor('#F8FAFC'),
    spaceAfter=0
)

output_box_style = ParagraphStyle(
    'OutputBox',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor('#10B981'),
    spaceAfter=0
)

tree_style = ParagraphStyle(
    'TreeBox',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor('#E2E8F0'),
    spaceAfter=0
)

def make_code_box(code_text):
    lines = code_text.strip().split('\n')
    flowables = []
    for l in lines:
        if l.strip().startswith('#'):
            flowables.append(Paragraph(f'<font color="#94A3B8">{l}</font>', code_snippet_style))
        else:
            flowables.append(Paragraph(f'<b>$</b> {l}', code_snippet_style))
            
    t = Table([[flowables]], colWidths=[522])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def make_output_box(output_text):
    lines = output_text.strip().split('\n')
    flowables = [Paragraph(l, output_box_style) for l in lines]
    t = Table([[flowables]], colWidths=[522])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#05111D')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def make_tree_box(tree_text):
    lines = tree_text.strip().split('\n')
    flowables = []
    for l in lines:
        if '#' in l:
            parts = l.split('#', 1)
            flowables.append(Paragraph(f'{parts[0]}<font color="#94A3B8">#{parts[1]}</font>', tree_style))
        else:
            flowables.append(Paragraph(l, tree_style))
    t = Table([[flowables]], colWidths=[522])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

story = []

# ============================================================================
# COVER HEADER
# ============================================================================
story.append(Paragraph("AGENTBROKO • LOCAL-FIRST AI SKILLS PLATFORM", brand_style))
story.append(Paragraph("AgentBroko Complete User Journey &amp; Usage Guide", title_style))
story.append(Paragraph("This guide breaks down what users experience, how they use AgentBroko, and the exact deliverables they get at every stage.", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C3AED'), spaceAfter=10))

# ============================================================================
# 1. WHAT USERS GET
# ============================================================================
story.append(Paragraph("🌟 What Users Get from AgentBroko", h1_style))
story.append(Paragraph("• <b>Zero Cloud Dependencies &amp; 100% Privacy:</b> All video rendering, speech generation, and PDF processing run on the user's local machine with <b>0 KB network calls and no API keys required</b>.", bullet_style))
story.append(Paragraph("• <b>Coding-Agent Friendly:</b> Structured CLI designed for humans and autonomous coding assistants (Cursor, Cline, Roo, Antigravity).", bullet_style))
story.append(Paragraph("• <b>Dual Packaging:</b> Can be run globally with <code>npm</code> / <code>npx</code> or installed into Python environments via <code>pip</code>.", bullet_style))
story.append(Spacer(1, 8))

# ============================================================================
# 2. USER JOURNEY 1
# ============================================================================
story.append(Paragraph("🚶‍♂️ User Journey 1: Installation &amp; Discovery", h1_style))
story.append(Paragraph("<b>Workflow:</b> User visits agentbroko.vercel.app &rarr; Copies <code>npm install -g agentbroko</code> &rarr; Runs <code>npx agentbroko skills</code> &rarr; Discovers Video Forge, PDF Playbook &amp; PDF Tools", body_style))

story.append(Paragraph("Step 1: Running without installation (Instant Trial)", h2_style))
story.append(make_code_box("npx agentbroko skills"))
story.append(Spacer(1, 4))

story.append(Paragraph("Step 2: Installing globally", h2_style))
story.append(make_code_box("npm install -g agentbroko"))
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Output the user sees:</b>", body_style))
story.append(make_output_box("""AgentBroko skills
  video-forge    Local video editing, offline narration, and captions
  pdf            Local PDF inspection, text extraction, and page rendering
  pdf-playbook   Premium branded developer handbook PDF generation

Use: agentbroko <skill> <command> [options]"""))
story.append(Spacer(1, 10))

# ============================================================================
# 3. USER JOURNEY 2 (VIDEO FORGE)
# ============================================================================
story.append(Paragraph("🎬 User Journey 2: Creating a Video with Video Forge", h1_style))
story.append(Paragraph("<b>Pipeline:</b> 1. doctor &rarr; 2. init my-video &rarr; 3. Edit script.txt &amp; project.json &rarr; 4. speak (Offline TTS &rarr; .wav) &rarr; 5. captions (Auto SRT &rarr; .srt) &rarr; 6. render (FFmpeg &rarr; final.mp4)", body_style))

story.append(Paragraph("Step 1: Health &amp; Environment Check", h2_style))
story.append(Paragraph("The user checks if their system has the necessary binaries (FFmpeg, TTS engine):", body_style))
story.append(make_code_box("agentbroko video-forge doctor"))
story.append(Paragraph("<b>User Output:</b>", body_style))
story.append(make_output_box("""FFmpeg: found
FFprobe: found
Offline TTS: windows"""))
story.append(Spacer(1, 6))

story.append(Paragraph("Step 2: Scaffold a Video Project", h2_style))
story.append(make_code_box("agentbroko video-forge init my-video"))
story.append(Paragraph("<b>What gets created in the user's filesystem:</b>", body_style))
story.append(make_tree_box("""my-video/
├── project.json      # Structured video timeline & clip coordinates
├── script.txt        # Spoken text narration
├── audio/            # Target folder for generated voiceovers
├── captions/         # Target folder for generated SRT subtitles
├── media/            # Folder for input clips/images
└── outputs/          # Folder for the final rendered MP4"""))
story.append(Spacer(1, 6))

story.append(Paragraph("Step 3: Generate Spoken Narration (Offline TTS)", h2_style))
story.append(Paragraph("The user writes their narration in <code>my-video/script.txt</code> (or passes text directly) and generates a clean .wav audio track:", body_style))
story.append(make_code_box("agentbroko video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav"))
story.append(Paragraph("<b>User Output:</b>", body_style))
story.append(make_output_box("Created my-video/audio/narration.wav with windows (or piper)"))
story.append(Spacer(1, 6))

story.append(Paragraph("Step 4: Generate Synchronized SRT Subtitles", h2_style))
story.append(Paragraph("The user generates timed subtitles from their script:", body_style))
story.append(make_code_box("agentbroko video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt"))
story.append(Paragraph("<b>User Output:</b>", body_style))
story.append(make_output_box("Created my-video/captions/subtitles.srt"))
story.append(Spacer(1, 6))

story.append(Paragraph("Step 5: Validate and Render the Final MP4 Video", h2_style))
story.append(make_code_box("""# Validate project schema
agentbroko video-forge validate my-video/project.json

# Render final video
agentbroko video-forge render my-video/project.json"""))
story.append(Paragraph("<b>User Deliverable:</b> A broadcast-quality <code>outputs/final.mp4</code> video with synchronized speech narration, background music ducking, and styled subtitles.", body_style))
story.append(Spacer(1, 10))

# ============================================================================
# 4. USER JOURNEY 3 (PDF PLAYBOOK)
# ============================================================================
story.append(Paragraph("📄 User Journey 3: Creating a 20-Page Developer Handbook (PDF Playbook)", h1_style))
story.append(Paragraph("<b>Pipeline:</b> agentbroko pdf-playbook &rarr; Interactive Wizard (Title, Audience, Promise) &rarr; ReportLab Document Engine &rarr; Outputs 20-Page Dark-Theme Handbook (.pdf)", body_style))

story.append(Paragraph("Option A: Interactive Wizard Mode", h2_style))
story.append(make_code_box("agentbroko pdf-playbook --output my-playbook.pdf"))
story.append(Paragraph("• The CLI prompts: <i>What is your guide title?</i> (e.g. <code>AI Agent Engineering Guide</code>)", bullet_style))
story.append(Paragraph("• The CLI prompts: <i>Who is the target audience?</i> (e.g. <code>Full-Stack Developers</code>)", bullet_style))
story.append(Paragraph("• The CLI prompts: <i>What is the core promise?</i> (e.g. <code>Master local AI model routing</code>)", bullet_style))
story.append(Spacer(1, 4))

story.append(Paragraph("Option B: Automated / CI/CD Mode", h2_style))
story.append(make_code_box("agentbroko pdf-playbook --non-interactive --output production-playbook.pdf"))
story.append(Paragraph("<b>User Deliverable:</b> A 34 KB, publication-ready, dark-theme 20-page A4 PDF complete with table of contents, structured tables, and checklists.", body_style))
story.append(Spacer(1, 10))

# ============================================================================
# 5. USER JOURNEY 4 (LOCAL PDF UTILITIES)
# ============================================================================
story.append(Paragraph("📑 User Journey 4: Local Offline PDF Utilities", h1_style))
story.append(make_code_box("""# 1. Inspect metadata (page count, encrypted status, author)
agentbroko pdf info document.pdf

# 2. Extract clean text to file (zero cloud upload)
agentbroko pdf text document.pdf --output document.txt

# 3. Render all pages as high-res images (requires Poppler)
agentbroko pdf render document.pdf --output rendered-pages/"""))
story.append(Spacer(1, 10))

# ============================================================================
# 6. USER JOURNEY 5 (CODING AGENTS)
# ============================================================================
story.append(Paragraph("🤖 User Journey 5: How Coding Agents (Cursor, Cline, Roo) Use AgentBroko", h1_style))
story.append(Paragraph("Coding agents invoke AgentBroko as a subprocess tool:", body_style))
story.append(Paragraph("• <b>Determinism:</b> Every command returns explicit POSIX exit codes (0 for success, non-zero for validation/runtime errors).", bullet_style))
story.append(Paragraph("• <b>No Prompts in Headless Mode:</b> Commands like <code>--non-interactive</code> allow autonomous agents to build media without human intervention.", bullet_style))
story.append(Paragraph("• <b>Structured JSON:</b> Agents read and modify <code>project.json</code> directly to adjust video timelines.", bullet_style))
story.append(Spacer(1, 10))

# ============================================================================
# 7. DELIVERABLES SUMMARY TABLE
# ============================================================================
story.append(Paragraph("🌐 Summary of Deliverables by Command", h1_style))
ref_table_data = [
    ["Command", "User Input", "Output Generated", "Engine"],
    ["agentbroko skills", "None", "Skills catalog list", "CLI Hub"],
    ["agentbroko video-forge init <name>", "Project Name", "Project folder scaffold", "Template"],
    ["agentbroko video-forge speak", "Text / Script file", ".wav speech audio", "Windows SAPI / Piper"],
    ["agentbroko video-forge captions", "Text script", ".srt subtitle file", "Subtitle Lexer"],
    ["agentbroko video-forge render", "project.json", "final.mp4 video file", "FFmpeg"],
    ["agentbroko pdf-playbook", "Title & Audience", "20-page .pdf handbook", "ReportLab"],
    ["agentbroko pdf text", "Input .pdf", "Clean text .txt file", "pypdf"]
]
t_ref = Table(ref_table_data, colWidths=[130, 95, 185, 112])
t_ref.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ('TOPPADDING', (0, 0), (-1, 0), 4),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('TOPPADDING', (0, 1), (-1, -1), 3.5),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3.5),
]))
story.append(t_ref)

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Generated Complete PDF: {output_pdf}")
print(f"File size: {os.path.getsize(output_pdf)} bytes")

# Copy to Video Edit workspace and brain artifacts directory
shutil.copy2(output_pdf, r"c:\Projects\Video Edit\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf")
brain_art = r"C:\Users\littl\.gemini\antigravity-ide\brain\a334d797-e486-4873-8e2c-ac00a2cebbbe\AGENTBROKO_COMPLETE_USER_JOURNEY_AND_USAGE_GUIDE.pdf"
shutil.copy2(output_pdf, brain_art)
print("Updated all destination copies successfully!")
