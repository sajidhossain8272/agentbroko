# 🤖 AgentBroko V9 — Autonomous Business OS & Multi-Domain AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![System Architecture](https://img.shields.io/badge/Architecture-AgentRuntime_V9-orange.svg)](#architecture)
[![Control Center UI](https://img.shields.io/badge/Control_Center-Live_Port_8000-purple.svg)](#control-center)

> **AgentBroko** is an autonomous multi-domain AI agent and open-source software factory. Built on a single authoritative master runtime (`AgentRuntime`), AgentBroko observes its environment, reasons about value-creation opportunities, participates in community conversations, executes software engineering tasks, and monitors multi-chain treasuries—all while self-healing and learning from actual evidence.

---

## 🌟 Vision & Mission

AgentBroko is designed to be a genuinely autonomous, domain-agnostic software engineer, content intelligence agent, and business operator. Rather than following rigid, hard-coded scripts or spamming promotional links, AgentBroko operates under an **Observe $\rightarrow$ Understand $\rightarrow$ Discover $\rightarrow$ Score $\rightarrow$ Select $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Measure $\rightarrow$ Learn** loop.

### Core Philosophy
1. **Value-First Contribution**: Engage in community discussions and publish technical content only when adding genuine value.
2. **Zero Niche Lock-in**: Dynamically evaluate topics across AI agent reliability, software engineering, developer security, business automation, science, and technology.
3. **Evidence-Based Revenue**: Strictly separate potential opportunity scores from confirmed real revenue ($0.00 until verified payment transactions).
4. **Self-Healing Resilience**: Multi-key AI failover router and 3-strike circuit breakers ensure continuous 24/7 autonomous operation without process crashing.

---

## 🏛️ System Architecture

```text
                               AgentRuntime (Singleton Lock)
                                             |
                                             v
                                      ExecutiveBrain
                                             |
        +------------------+-----------------+------------------+
        |                  |                 |                  |
SituationAnalyzer     GoalManager    OpportunityEngine    ExperimentEngine
        |                  |                 |                  |
        +------------------+-----------------+------------------+
                                             |
                                             v
                                    AIProviderRouter
        (GEMINI_API_KEY -> FALLBACK_1 -> FALLBACK_2 -> FALLBACK_3 -> OPENROUTER_FREE)
                                             |
                                             v
                                     Capability Router
                   (Moltbook, GitHub, Business, Wallet, Engineering)
                                             |
                                             v
                        VERIFY -> LEARN -> MEMORY (9 Categories)
                                             |
                                             v
                             AgentEventBus & RevenueEngine
                                             |
                                             v
                         REAL-TIME COMMAND CENTER WEB UI (Port 8000)
```

---

## ⚡ Core Systems & Capabilities

### 1. Master AgentRuntime (`agent_runtime.py`)
- Single authoritative master loop driving explicit state transitions (`STARTING` $\rightarrow$ `OBSERVING` $\rightarrow$ `PLANNING` $\rightarrow$ `SELECTING` $\rightarrow$ `EXECUTING` $\rightarrow$ `VERIFYING` $\rightarrow$ `LEARNING` $\rightarrow$ `WAITING`).
- Governed by a singleton process lock (`agentbroko.lock`) to prevent duplicate runner instances.

### 2. Executive Brain (`executive_brain.py`)
- Coordinates situation analysis, persistent goal management, business opportunity discovery, controlled hypothesis-driven experiments, content selection, and strategy management.

### 3. AI Provider Router (`ai_provider_router.py`)
- Centralized LLM gateway managing `GEMINI_API_KEY`, `GEMINI_API_KEY_FALLBACK_1..3`, and `OPENROUTER_FREE`.
- Classifies requests by task complexity (`HIGH_REASONING`, `CONTENT_GENERATION`, `RESEARCH`, `CODE`, `ANALYSIS`).
- Automatic failover upon rate limits (429) or timeouts without crashing. Zero API key exposure in logs.

### 4. Content Intelligence Engine (`content_brain.py` & `content_memory.py`)
- Discovers candidate topics across AI Agents, Developer Tools, Security Scanning, Business Automation, Tech Trends, and Crypto.
- Calculates `topic_fatigue` penalties to prevent repetitive subjects and enforce topic diversity.
- Dynamically selects content format (`Technical Breakdown`, `Problem + Solution`, `Tutorial`, `Case Study`), length (`SHORT`, `MEDIUM`, `LONG`), and community destination (`m/technology`, `m/tooling`, `m/agentfinance`, `m/todayilearned`, `m/general`).
- Supports valid decisions: `POST`, `COMMENT`, `REPLY`, `RESEARCH`, or `WAIT`.

### 5. Moltbook Autonomous Social Agent (`moltbook_feed_intelligence.py` & `social_memory.py`)
- Categorizes feed discussions and scores conversation priority.
- Engages in non-spam, value-first technical comments and multi-turn thread replies.
- Automatically extracts developer pain points and tool requests into the Opportunity Discovery Engine.

### 6. Revenue Engine & Monetization Registry (`revenue_engine.py`)
- Tracks `potential_revenue`, `expected_revenue`, `confirmed_revenue`, `received_revenue`, `expenses`, and `net_profit`.
- Strictly separates potential opportunity scores from confirmed real revenue ($0.00 until payment).

### 7. Wallet Engine & 3-Strike Circuit Breaker (`capabilities/wallet_capability.py`)
- Monitors multi-chain balances across Bitcoin, Solana, Base, Polygon, Arbitrum, and Ethereum.
- 3-strike circuit breaker isolates provider timeouts (`DEGRADED`/`OFFLINE` state with 2-minute backoff) so wallet queries never block main agent cycles.

### 8. Real-Time Command Center Web UI (`control_center_server.py` & `static/control_center.html`)
- Glassmorphism Web Dashboard running live on `http://localhost:8000`.
- Features Real-Time Activity Stream, AI Provider Health, Confirmed Revenue Ledger, Content Intelligence Hub, Permissions & Safe Mode controls, and Error Center.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- `git`

### 2. Installation
```bash
git clone https://github.com/agentbroko/agentbroko.git
cd agentbroko

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (standard library + optional requests/urllib)
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
MNEMONIC_PHRASE="your twelve word secret phrase here"
github_token="github_pat_11B..."
GEMINI_API_KEY="AIzaSy..."
GEMINI_API_KEY_FALLBACK="AIzaSy..."
OPENROUTER_FREE="sk-or-v1-..."
```

### 4. Launch AgentBroko Master OS
```bash
python agentbroko_runner.py
```
Then open your browser and navigate to:
**`http://localhost:8000`**

---

## 🧪 Test Suite

Run the full V9 System Acceptance & Regression Test Suite:
```bash
python test_v9_system_acceptance.py
python test_v8_master_orchestrator.py
python test_content_intelligence.py
python test_moltbook_social.py
python test_money_intelligence.py
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  <i>Built with ❤️ by the AgentBroko Core Architecture Team</i>
</p>
