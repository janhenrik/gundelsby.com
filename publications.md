---
layout: page
title: Publications
schema: publications
---
# Publications

Research on agile teams, large-scale software development, technical debt, and AI-human collaboration.

<a rel="me" href="{{ site.data.publications.identity.orcid_url }}">ORCID: {{ site.data.publications.identity.orcid }}</a> · [Semantic Scholar]({{ site.data.publications.identity.semantic_scholar_url }}) · [Google Scholar](https://scholar.google.com/citations?user=4bw3LsEAAAAJ)

## Articles and preprints

| Year | Publication | Venue | Authors |
|------|-------------|-------|---------|
{% for publication in site.data.publications.works -%}
| {{ publication.year }} | [{{ publication.title }}](https://doi.org/{{ publication.doi }}) | {{ publication.venue }} | {% for author in publication.authors %}{{ author.name }}{% unless forloop.last %}; {% endunless %}{% endfor %}{% if publication.et_al %}; et al.{% endif %} |
{% endfor -%}
