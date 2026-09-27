# gnshb.github.io

My personal website. Pages are Markdown files, [Hugo](https://gohugo.io) turns them into a static site, and GitHub Pages publishes it whenever `main` changes.

## Everyday use

1. **Install Hugo** (once), version 0.166 or newer:
   - macOS: `brew install hugo`
   - Windows: `winget install Hugo.Hugo.Extended`
   - Anywhere with Python: `pip install hugo`
2. **Preview**: run `hugo server` and open <http://localhost:1313>. The page reloads every time you save.
3. **Publish**: run `./publish.sh "What changed"`. It checks that the site builds, then commits and pushes. On `main`, GitHub rebuilds the live site within a couple of minutes.

You can also edit files directly on github.com; pushing to `main` from anywhere publishes the site.

## Where things live

| To change…                      | Edit                                   |
| ------------------------------- | -------------------------------------- |
| Name, tagline, links, menu      | `hugo.yaml`                            |
| Home page                       | `content/_index.md`                    |
| About page                      | `content/about.md`                     |
| Research                        | `content/research/`, one file per entry |
| Projects                        | `content/projects/`, one file per entry |
| Colours, fonts, spacing         | the top of `assets/css/main.css`       |
| Photo, CV, PDFs, images         | add files to `static/`                 |

Files in `static/` are served from the root of the site, so `static/cv.pdf` becomes `/cv.pdf`. To show a photo in the sidebar, add it (e.g. `static/images/me.jpg`) and set `photo: /images/me.jpg` in `hugo.yaml`.

You shouldn't need to open `layouts/` (the HTML templates) for everyday changes.

## Writing

Each page is a Markdown file with a short header, called front matter, between two `---` lines.

### Research and project entries

Every entry is its own file. Copy an existing one, or run `hugo new content research/my-paper.md` to start from a template:

```yaml
---
title: Title of the paper
date: 2026-05-01            # entries are sorted newest first; the year is shown
period: 2025 – now          # optional: shown instead of the date
authors: Ganesh Balaji, A. Coauthor   # optional; your name is bolded automatically
venue: arXiv preprint       # optional
summary: One or two sentences about it.
tags: [python, geometry]    # optional
featured: true              # optional: also show it on the home page
links:                      # optional, any labels you like (shown alphabetically)
  pdf: /papers/paper.pdf
  code: https://github.com/gnshb/example
---

Optional write-up. If you write anything here, the entry gets a page of its own
and its title becomes a link.
```

- To put an entry first regardless of date, give it `weight: 1` (then `weight: 2`, and so on).
- To hide an entry without deleting it, add `draft: true`.
- The home page shows each section's `featured` entries, or its three newest if none are featured. Which sections appear there is set by `homeSections` in `hugo.yaml`.

### Dates in the margin

The News, Education and Experience lists use Markdown definition lists: the date on one line, then the text on the next line after `: `. The date goes in the margin.

```markdown
Sep 2026
: Started a research project on …
```

### Math

Write LaTeX between `$...$` (inline) or `$$...$$` (display). Math is rendered when the site is built, so pages load no JavaScript for it. For a literal dollar sign, write `\$`. If some LaTeX doesn't parse, it shows up in red on the page; hover over it to see the error.

### Code

Fenced code blocks with a language name get syntax colouring:

````markdown
```python
print("hello")
```
````

## Adding a page

Create a Markdown file such as `content/teaching.md` with a `title`, then add it to the menu in `hugo.yaml`:

```yaml
- { name: teaching, pageRef: /teaching, weight: 5 }
```

## Adding a blog

1. Create `content/blog/_index.md`:

   ```yaml
   ---
   title: Blog
   linkTitle: posts          # the home page link then reads "all posts →"
   dateFormat: Jan 2006      # show month and year next to each post
   ---

   An optional line of introduction.
   ```

2. Add posts as `content/blog/my-first-post.md`, each with a `title`, a `date`, and optionally a `summary`.
3. In `hugo.yaml`, uncomment the `blog` line in the menu, and add `blog` to `homeSections` if you want recent posts on the home page.

The list page, post pages, and an RSS feed at `/blog/index.xml` are generated automatically. Any other folder in `content/` (notes, talks, teaching) works the same way.

## Publishing

`.github/workflows/deploy.yml` builds the site with Hugo on every push to `main` and deploys it to GitHub Pages. Pull requests are built but not deployed, so errors show up before anything goes live.

GitHub Pages must be set to deploy from Actions: in the repository's **Settings → Pages**, under **Build and deployment**, set **Source** to **GitHub Actions**.

## How it's built

- `layouts/`: the HTML templates. `baseof.html` is the frame around every page; `home.html`, `section.html` (lists) and `page.html` (single pages) fill it in; `_partials/` holds the pieces (sidebar, entries, footer).
- `assets/css/main.css`: all the styles, with colour, type and layout settings at the top. `fonts.css` and `katex.css` are vendored and don't need editing.
- `assets/js/theme.js`: the light/dark switch, which remembers the visitor's choice.
- `static/fonts/`: self-hosted [Newsreader](https://github.com/productiontype/Newsreader) and [IBM Plex Mono](https://github.com/IBM/plex) (both SIL Open Font License), plus KaTeX's math fonts.
- `archetypes/default.md`: the template used by `hugo new content`.
