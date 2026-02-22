---
title: Blog
---

Posts in reverse chronological order.

{% assign published_posts = site.posts | sort: "date" | reverse %}
{% if published_posts.size > 0 %}
{% for post in published_posts %}
- [{{ post.title }}]({{ post.url | relative_url }})  
  {{ post.date | date: "%B %-d, %Y" }}. {{ post.summary | default: post.excerpt | strip_html | truncate: 160 }}

{% endfor %}
{% else %}
No posts yet. Add one in `_posts/` and it will appear here automatically.
{% endif %}

[Home]({{ '/' | relative_url }}) | [Projects]({{ '/projects/' | relative_url }})
