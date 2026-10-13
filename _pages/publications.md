---
layout: page
permalink: /publications/
title: publications
description: Research on agile teams, large-scale software development, technical debt, and human-AI collaboration.
nav: true
nav_order: 2
schema: publications
---

<!-- _pages/publications.md -->

<p>
  <a rel="me" href="{{ site.data.publications.identity.orcid_url }}">ORCID: {{ site.data.publications.identity.orcid }}</a> ·
  <a href="{{ site.data.publications.identity.semantic_scholar_url }}">Semantic Scholar</a> ·
  <a href="https://scholar.google.com/citations?user=4bw3LsEAAAAJ">Google Scholar</a>
</p>

{% include bib_search.liquid %}

<div class="publications">

{% bibliography %}

</div>
