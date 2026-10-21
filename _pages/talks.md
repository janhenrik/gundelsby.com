---
layout: page
permalink: /talks/
title: talks
description: Selected talks and public speaking, mostly in Norwegian.
nav: true
nav_order: 3
---

{% assign talks_by_year = site.data.talks | group_by: 'year' %}

<style>
  .talks-year { display: flex; gap: 1.25rem; padding: 0.6rem 0; border-top: 1px solid var(--global-divider-color); }
  .talks-year:first-child { border-top: none; }
  .talks-year h2 { flex: 0 0 3.5rem; margin: 0; font-size: 1.1rem; line-height: 1.6; color: var(--global-text-color-light); }
  .talks-year ul { flex: 1; min-width: 0; margin: 0; padding: 0; list-style: none; }
  .talks-year li { line-height: 1.6; padding: 0.1rem 0; }
  .talks-year li i { width: 1.1rem; color: var(--global-text-color-light); }
  .talks-year .talk-event { font-weight: 600; }
</style>

<div class="talks">
  {% for group in talks_by_year %}
    <section class="talks-year">
      <h2>{{ group.name }}</h2>
      <ul>
        {% for talk in group.items %}
          {% if talk.url contains 'vimeo.com' or talk.url contains 'youtube.com' %}
            {% assign talk_icon = 'fa-solid fa-video' %}
          {% elsif talk.url contains 'slideshare.net' %}
            {% assign talk_icon = 'fa-solid fa-file-powerpoint' %}
          {% else %}
            {% assign talk_icon = 'fa-solid fa-microphone' %}
          {% endif %}
          <li>
            <i class="{{ talk_icon }}"></i>
            {% if talk.url %}<a class="talk-event" href="{{ talk.url }}">{{ talk.event }}</a>{% else %}<span class="talk-event">{{ talk.event }}</span>{% endif %}
            » {{ talk.title }}
          </li>
        {% endfor %}
      </ul>
    </section>
  {% endfor %}
</div>
