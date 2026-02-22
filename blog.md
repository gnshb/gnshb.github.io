---
title: Blog
---

## Writing

Short notes on projects, engineering choices, and what I am learning.

---

{% assign published_posts = site.posts | sort: "date" | reverse %}
{% if published_posts.size > 0 %}
{% for post in published_posts %}
### [{{ post.title }}]({{ post.url | relative_url }})
*{{ post.date | date: "%B %-d, %Y" }}*

{{ post.summary | default: post.excerpt | strip_html | truncate: 180 }}

{% endfor %}
{% else %}
No posts yet. Add one in `_posts/` and it will appear here automatically.
{% endif %}

---

[← Home]({{ '/' | relative_url }})
