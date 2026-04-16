# Personal Website

Minimal Markdown-first site with a tiny Python build step.

## Edit These Files

- `site.yaml` for site title, description, and GitHub link
- `content/home.md` for the homepage
- `content/projects.md` for projects
- `content/blog.md` for the blog page intro
- `content/posts/*.md` for blog posts

## Styling

- `assets/css/latex.css` is the self-hosted LaTeX.css base
- `style.css` holds the small local overrides
- `template.html` is the shared page wrapper

## Build

```bash
python3 build.py
```

The generated site goes into `site/` and is deployed by GitHub Actions.
