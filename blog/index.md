---
title: News
permalink: /news/
redirect_from:
  - /blog/
nav:
  order: 5
  tooltip: Latest news and updates
---

<div class="news-page" aria-labelledby="news-title">
  <h1 id="news-title">News</h1>

  {% assign sorted_news = site.data.news | sort: "date" | reverse %}
  {% assign years = sorted_news | group_by: "year" | sort: "name" | reverse %}
  {% for year in years %}
  <section class="news-year" aria-labelledby="news-{{ year.name }}">
    <h2 id="news-{{ year.name }}">{{ year.name }}</h2>
    <ul class="news-list">
      {% for item in year.items %}
      <li>
        <time datetime="{{ item.date | escape }}">{{ item.date | date: "%b %-d, %Y" }}</time>
        <p>{% include news-text.html item=item %}</p>
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
</div>
