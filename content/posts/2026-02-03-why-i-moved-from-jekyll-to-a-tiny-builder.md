---
title: Why I Moved From Jekyll to a Tiny Builder
date: 2026-02-03
summary: A short note on reducing the maintenance surface of a personal site without giving up Markdown authoring.
---

I like Markdown authoring, but I do not like carrying a lot of framework-shaped structure for a very small site.

The problem with the earlier setup was not that Jekyll was bad. It was that the number of moving parts was out of proportion to the size of the site. For a personal homepage, folders like `_layouts`, `_posts`, and generated output add cognitive overhead quickly.

The replacement is deliberately small:

- Markdown files for content
- one HTML template
- one build script
- static output for deployment

That keeps the writing workflow intact while making the repo easier to understand at a glance.
