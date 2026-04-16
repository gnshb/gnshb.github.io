from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
import shutil

import markdown
import yaml


ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
POSTS_DIR = CONTENT_DIR / "posts"
OUTPUT_DIR = ROOT / "site"
TEMPLATE_PATH = ROOT / "template.html"
CONFIG_PATH = ROOT / "site.yaml"


@dataclass
class Page:
    title: str
    body: str
    summary: str | None = None
    date: str | None = None


def parse_markdown(path: Path) -> Page:
    raw = path.read_text(encoding="utf-8").strip()
    if raw.startswith("---"):
        _, frontmatter, body = raw.split("---", 2)
        meta = yaml.safe_load(frontmatter) or {}
    else:
        meta = {}
        body = raw
    return Page(
        title=meta.get("title", path.stem.replace("-", " ").title()),
        body=body.strip(),
        summary=meta.get("summary"),
        date=meta.get("date"),
    )


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "smarty", "tables", "fenced_code"],
    )


def make_post_slug(path: Path) -> str:
    stem = path.stem
    return stem[11:] if len(stem) > 11 and stem[4] == "-" else stem


def post_list_html(posts: list[dict[str, str]], limit: int | None = None, *, class_name: str = "post-list") -> str:
    items = posts[:limit] if limit else posts
    if not items:
        return "<p>No posts yet.</p>"

    lines = [f'<ul class="{class_name}">']
    for post in items:
        summary_html = f'<br /><span class="meta">{escape(post["summary"])}</span>' if post.get("summary") else ""
        lines.append(
            f'<li><a href="{post["url"]}">{escape(post["title"])}</a> '
            f'({escape(post["display_date"])}){summary_html}</li>'
        )
    lines.append("</ul>")
    return "\n".join(lines)


def sidebar_html(site: dict[str, str], posts: list[dict[str, str]], depth: int) -> str:
    prefix = "./" if depth == 0 else "../" * depth
    recent = post_list_html(posts, limit=4, class_name="sidebar-posts")
    return (
        '<section class="sidebar-card">'
        '<h2>About</h2>'
        f'<p>{escape(site["description"])}</p>'
        "</section>"
        '<section class="sidebar-card">'
        "<h2>Explore</h2>"
        '<ul class="sidebar-links">'
        f'<li><a href="{prefix}">Home</a></li>'
        f'<li><a href="{prefix}projects/">Projects</a></li>'
        f'<li><a href="{prefix}blog/">Blog</a></li>'
        f'<li><a href="{escape(site["github"])}">GitHub</a></li>'
        "</ul>"
        "</section>"
        '<section class="sidebar-card">'
        "<h2>Recent Posts</h2>"
        f"{recent}"
        "</section>"
    )


def page_hero(title: str, meta: str | None = None, summary: str | None = None) -> str:
    meta_html = f'<p class="page-meta">{escape(meta)}</p>' if meta else ""
    summary_html = f'<p class="page-summary">{escape(summary)}</p>' if summary else ""
    return (
        '<section class="page-hero">'
        f"<p class=\"page-label\">{escape(title)}</p>"
        f"<h2>{escape(title)}</h2>"
        f"{meta_html}"
        f"{summary_html}"
        "</section>"
    )


def wrap_page(*, site: dict[str, str], title: str, body_html: str, description: str, depth: int, posts: list[dict[str, str]], hero_html: str = "", body_class: str = "page-default") -> str:
    prefix = "./" if depth == 0 else "../" * depth
    page_title = site["title"] if title == "Home" else f"{title} | {site['title']}"
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return template.format(
        title=escape(page_title),
        description=escape(description),
        prefix=prefix,
        site_title=escape(site["title"]),
        site_description=escape(site["description"]),
        github=escape(site["github"]),
        hero=hero_html,
        sidebar=sidebar_html(site, posts, depth),
        body_class=body_class,
        content=body_html,
    )


def write_page(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def build() -> None:
    site = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    shutil.copy(ROOT / "style.css", OUTPUT_DIR / "style.css")
    shutil.copy(ROOT / "favicon.ico", OUTPUT_DIR / "favicon.ico")
    shutil.copytree(ROOT / "assets", OUTPUT_DIR / "assets", dirs_exist_ok=True)

    posts = []
    for post_path in sorted(POSTS_DIR.glob("*.md")):
        post = parse_markdown(post_path)
        slug = make_post_slug(post_path)
        date_text = datetime.strptime(str(post.date), "%Y-%m-%d").strftime("%B %-d, %Y")
        posts.append(
            {
                "title": post.title,
                "url": f"/blog/{slug}/",
                "summary": post.summary or "",
                "display_date": date_text,
                "date": str(post.date),
                "slug": slug,
            }
        )

    posts.sort(key=lambda item: datetime.strptime(item["date"], "%Y-%m-%d"), reverse=True)

    for post_path in sorted(POSTS_DIR.glob("*.md")):
        post = parse_markdown(post_path)
        slug = make_post_slug(post_path)
        date_text = datetime.strptime(str(post.date), "%Y-%m-%d").strftime("%B %-d, %Y")
        post_body = md_to_html(post.body) + '\n<p><a href="/blog/">Back to Blog</a></p>'
        post_html = wrap_page(
            site=site,
            title=post.title,
            body_html=post_body,
            description=post.summary or site["description"],
            depth=2,
            posts=posts,
            hero_html=page_hero(post.title, meta=f"Posted on {date_text}", summary=post.summary),
            body_class="page-post",
        )
        write_page(OUTPUT_DIR / "blog" / slug / "index.html", post_html)

    home = parse_markdown(CONTENT_DIR / "home.md")
    home_body = md_to_html(home.body) + "\n<h2>Recent Writing</h2>\n" + post_list_html(posts, limit=3)
    write_page(
        OUTPUT_DIR / "index.html",
        wrap_page(
            site=site,
            title=home.title,
            body_html=home_body,
            description=site["description"],
            depth=0,
            posts=posts,
            hero_html="",
            body_class="page-home",
        ),
    )

    blog = parse_markdown(CONTENT_DIR / "blog.md")
    blog_body = md_to_html(blog.body) + "\n" + post_list_html(posts)
    write_page(
        OUTPUT_DIR / "blog" / "index.html",
        wrap_page(
            site=site,
            title=blog.title,
            body_html=blog_body,
            description=site["description"],
            depth=1,
            posts=posts,
            hero_html=page_hero(blog.title, summary=blog.summary),
            body_class="page-blog",
        ),
    )

    projects = parse_markdown(CONTENT_DIR / "projects.md")
    write_page(
        OUTPUT_DIR / "projects" / "index.html",
        wrap_page(
            site=site,
            title=projects.title,
            body_html=md_to_html(projects.body),
            description=site["description"],
            depth=1,
            posts=posts,
            hero_html=page_hero(projects.title),
            body_class="page-projects",
        ),
    )


if __name__ == "__main__":
    build()
