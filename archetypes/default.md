---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ time.Format "2006-01-02" .Date }}
summary: ""
# Optional fields (remove the # to use):
# period: "2025 – now"        # shown instead of the date
# authors: "Ganesh Balaji, Coauthor Name"
# venue: "Conference, journal, lab or course"
# tags: [python, geometry]
# featured: true              # also show on the home page
# links:
#   pdf: /papers/example.pdf  # files in static/ are served from the site root
#   code: https://github.com/gnshb/example
# draft: true                 # hide from the published site
---
