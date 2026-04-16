---
title: Projects
---

Selected work. Add, remove, or reorder sections directly in this file.

## Personal Website

- **Status**: Live and evolving
- **Stack**: Markdown, Python build script, self-hosted LaTeX.css
- **Summary**: Built a small personal site with a Markdown-first workflow and a minimal build step.

### Problem

I wanted a personal site that stayed fast, text-first, and easy to edit without fighting framework-specific folder names or build conventions.

### Approach

I kept the source in Markdown, used one shared HTML template, and generated a static site with a small Python build script.

### Outcome

The site is easy to maintain, easy to read in the repo, and cheap to deploy on GitHub Pages.

## Mess Menu Scraper

- **Status**: Prototype
- **Stack**: Python, requests, HTML parsing
- **Summary**: Collects daily mess menus from inconsistent source pages and turns them into structured data for a simple website.

### Problem

Mess menus are often scattered across PDFs, images, or badly formatted pages, which makes them annoying to check quickly.

### Approach

I wrote a lightweight scraper plus a cleanup step that normalizes meal names, dates, and menu items before publishing them.

### Outcome

The result is a small pipeline that can feed a readable web page or JSON endpoint instead of forcing people to parse raw notices.

## Research Notebook

- **Status**: Live and evolving
- **Stack**: Markdown, Git, small helper scripts
- **Summary**: A plain-text workflow for storing paper notes, experiment logs, and reproducible commands in one place.

### Problem

Research notes often end up split across notebooks, chats, screenshots, and one-off text files that are hard to search later.

### Approach

I kept everything in Markdown with lightweight conventions for paper summaries, run logs, and open questions, then used Git for versioned history.

### Outcome

The notebook makes it easier to revisit ideas, rerun experiments, and turn rough notes into cleaner writing.

## Dataset Explorer

- **Status**: Prototype
- **Stack**: Python, CSV, small static HTML
- **Summary**: A tiny browser for inspecting tabular datasets without pulling in a full dashboard stack.

### Problem

For many small research tasks, opening a giant notebook or dashboard is slower than the task itself.

### Approach

I generated static summaries, filters, and preview pages from raw CSV files so I could inspect columns and rows quickly in the browser.

### Outcome

It became a useful middle ground between raw spreadsheets and a full application.

## Project Template

Copy this block for a new project:

```md
## Project Name

- **Status**: Prototype / Live / Archived
- **Stack**: Tools here
- **Summary**: One paragraph on what you built.

### Problem
What was broken or missing?

### Approach
What did you build and why this design?

### Outcome
What changed because of it?
```
