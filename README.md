# Personal Website

Minimal Markdown-first site with a tiny Python build step.

## Edit These Files

- `site.yaml` for site title, description, and GitHub link
- `content/home.md` for the homepage
- `content/projects.md` for projects
- `content/blog.md` for the blog page intro
- `content/sidebar.md` for the right sidebar
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

## Deploy

Use the helper script after updating content:

```bash
./deploy.sh "Describe your update"
```

What it does:

- builds locally with `python3 build.py`
- checks that the generated homepage, blog, and projects pages exist
- commits and pushes your source changes
