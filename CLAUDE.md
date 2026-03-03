# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static webapp serving as a clinical staff handbook/guide for the Hutt Hospital Special Care Baby Unit (SCBU). Content is derived from "Hutt SCBU Handbook Jan 2026.docx".

## Architecture

- **Single-file `index.html`** — embedded CSS + vanilla JS, no build step, no framework
- Fixed sidebar navigation with collapsible subsections and search filter
- Mobile responsive (hamburger menu), print-friendly CSS
- Static site suitable for deployment on GitHub Pages, Netlify, or similar
- Target audience: SCBU clinical staff (junior doctors)

## Key Files

- `index.html` — the webapp (all content, styles, and JS in one file)
- `generate_html.py` — Python script that reads the .docx and generates `index.html`
- `Hutt SCBU Handbook Jan 2026.docx` — source document
- `Hutt SCBU Handbook Jan 2026.pages` / `.pdf` — original formats
- `.venv/` — Python venv with `python-docx` (used by generate_html.py only)

## Development

Open `index.html` in a browser. No build or install commands needed.

## Regenerating the HTML

If the source .docx is updated, regenerate `index.html`:

```sh
.venv/bin/python3 generate_html.py
```

This reads the .docx (paragraphs, headings, tables) and outputs a fresh `index.html`.

## Deployment

Static hosting — serve `index.html` as-is. No server-side processing required.

## Content Source

The source document is `Hutt SCBU Handbook Jan 2026.docx`. Content should closely follow this document's structure and clinical information. Do not invent or embellish clinical content beyond what the source provides.
