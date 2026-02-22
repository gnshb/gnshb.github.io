# Personal Website

Jekyll-based personal site for projects and blog posts.
Styling uses [LaTeX.css](https://latex.vercel.app/) by Vincent Doerig.

## Customize Your Identity

Edit `_config.yml`:

- `title`
- `author.name`
- `author.role`
- `author.location`
- `author.email`
- `author.github`

## Add A Blog Post

1. Create a markdown file in `_posts/` using this naming format:
   `YYYY-MM-DD-title.md`
2. Add front matter:

```md
---
title: My Post Title
date: 2026-02-22
summary: One-line summary shown on the blog page.
---
```

3. Write content below the front matter.

Posts appear automatically on `blog.md`.

## Add A Project

Edit `projects.md` and copy the project block template already included there.

## Styling Notes

- Base styles are loaded from `https://latex.vercel.app/style.css`
- Small local overrides live in `assets/css/custom.css`

## Run Locally (if Jekyll is installed)

```bash
jekyll serve
```
