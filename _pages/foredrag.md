---
layout: page
permalink: /foredrag/
title: foredrag
description: Talks and public speaking, mostly in Norwegian.
nav: true
nav_order: 3
---

{% assign talks_by_year = site.data.talks | group_by: 'year' %}

<div class="publications talks">
  {% for group in talks_by_year %}
    <h2 class="bibliography">{{ group.name }}</h2>
    <div class="table-responsive">
      <table class="table table-sm table-borderless">
        {% for talk in group.items %}
          {% if talk.url contains 'vimeo.com' or talk.url contains 'youtube.com' %}
            {% assign talk_icon = 'fa-solid fa-video' %}
          {% elsif talk.url contains 'slideshare.net' %}
            {% assign talk_icon = 'fa-solid fa-file-powerpoint' %}
          {% else %}
            {% assign talk_icon = 'fa-solid fa-microphone' %}
          {% endif %}
          <tr>
            <th scope="row" style="width: 30%">
              <i class="{{ talk_icon }}"></i>
              {% if talk.url %}
                <a href="{{ talk.url }}">{{ talk.event }}</a>
              {% else %}
                {{ talk.event }}
              {% endif %}
            </th>
            <td>{{ talk.title }}</td>
          </tr>
        {% endfor %}
      </table>
    </div>
  {% endfor %}
</div>
