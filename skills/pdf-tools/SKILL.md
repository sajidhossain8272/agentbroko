---
name: pdf-tools
description: Inspect PDFs, extract text, check metadata and page counts, and render pages locally without uploading documents.
version: 1.4.6
author: AgentBroko
license: MIT
tags: [pdf, inspection, extraction, local-first]
---

# PDF Tools

Use when the user wants to inspect, extract, or render a PDF.

- `npx agentbroko pdf info document.pdf`
- `npx agentbroko pdf text document.pdf --output extracted.txt`
- `npx agentbroko pdf render document.pdf --output rendered-pages/`

Keep source documents local. Report missing rendering backends clearly, and never expose extracted private text unnecessarily.
