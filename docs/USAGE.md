# AgentBroko Usage Guide & Agent-First Workflows

AgentBroko is designed for both human developers and autonomous AI coding agents (**Google Antigravity**, **Cursor**, **VS Code Cline**, **Roo Code**, **Windsurf**, **Claude Code**, **GitHub Copilot**).

---

## 🤖 The IDE Coding Agent Workflow

### 1. Provision Workspace Skills

```bash
# Provision all skills
npx agentbroko init

# Or install one specific skill
npx agentbroko add video-forge
npx agentbroko add pdf-playbook
npx agentbroko add pdf
```

---

### 2. Prompting Your IDE Agent

#### 🎬 Video Creation Example Prompt:
> *"Agent, create a 30-second vertical TikTok short for my SaaS product launch. Use Video Forge to write the narration script in `script.txt`, synthesize offline speech audio, create synchronized SRT subtitles, and render the final MP4 video."*

**What your agent does:**
1. Creates project scaffold with `npx agentbroko video-forge init my-video`.
2. Synthesizes voiceover with `npx agentbroko video-forge speak --file my-video/script.txt --output my-video/audio/narration.wav`.
3. Creates subtitles with `npx agentbroko video-forge captions --file my-video/script.txt --output my-video/captions/subtitles.srt`.
4. Validates schema with `npx agentbroko video-forge validate my-video/project.json`.
5. Renders the video with `npx agentbroko video-forge render my-video/project.json`.

---

#### 📄 PDF Handbook Example Prompt:
> *"Agent, generate a 20-page developer handbook on 'Kubernetes Production Best Practices' for DevOps Engineers. Use the PDF Playbook skill to structure the 18 chapters and compile the final PDF."*

**What your agent does:**
1. Writes an 18-chapter structured blueprint `playbook_spec.json`.
2. Compiles the publication-ready PDF:
   ```bash
   npx agentbroko pdf-playbook --spec playbook_spec.json --output playbook.pdf
   ```

---

## 🛠️ Complete CLI Command Reference

### Workspace & Skill Management:
```bash
# Initialize all skills
agentbroko init

# Add a single skill
agentbroko add video-forge
agentbroko add pdf-playbook
agentbroko add pdf

# Clone entire starter repository
agentbroko clone my-workspace

# Run system diagnostic checks
agentbroko doctor

# View AI agent execution and emergency recovery guide
agentbroko guide
```

### Video Forge:
```bash
agentbroko video-forge doctor
agentbroko video-forge init <name>
agentbroko video-forge validate <project.json>
agentbroko video-forge speak --file <script.txt> --output <narration.wav>
agentbroko video-forge captions --file <script.txt> --output <subtitles.srt>
agentbroko video-forge render <project.json>
```

### PDF Playbook:
```bash
# Spec mode (agent generated):
agentbroko pdf-playbook --spec <spec.json> --output <guide.pdf>

# Gemini API mode:
agentbroko pdf-playbook --api-key <KEY> --title <TITLE> --output <guide.pdf>

# Offline Ollama mode:
agentbroko pdf-playbook --provider ollama --output <guide.pdf>
```

### Local PDF Tools:
```bash
agentbroko pdf info <document.pdf>
agentbroko pdf text <document.pdf> --output <extracted.txt>
agentbroko pdf render <document.pdf> --output <pages_dir>
```

---

## 🆘 Agent Emergency & Recovery Protocol

If your agent runs into tool errors:
1. Run `npx agentbroko doctor` to verify local binary dependencies.
2. If FFmpeg is missing:
   - Windows: `winget install Gyan.FFmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
3. If ReportLab is missing: `python -m pip install reportlab`
4. Inspect audio or video streams locally with `ffprobe <file>`.
