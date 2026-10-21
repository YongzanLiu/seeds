---
title: Yongzan Liu
permalink: /team/yongzan-liu/
---

{% assign pi_group = site.data.team | where: "id", "principal-investigator" | first %}
{% assign pi = pi_group.members | first %}

<div class="team-member-page">
  <a class="team-member-back" href="{{ '/team/' | relative_url }}">&larr; Team</a>

  {% include team-profile.html member=pi role=pi_group.role layout="pi" heading_tag="h1" link_name=false %}

  <div class="team-member-links">
    <a class="team-profile-email" href="mailto:{{ pi.email | escape }}">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true" focusable="false">
        <rect x="3" y="5" width="18" height="14" rx="2" />
        <path d="m3 6 9 7 9-7" />
      </svg>
      <span>{{ pi.email | escape }}</span>
    </a>
    <a href="{{ pi.google_scholar | escape }}">Google Scholar</a>
    <a href="{{ pi.linkedin | escape }}">LinkedIn</a>
    <a href="{{ pi.university_profile | escape }}">University Profile</a>
  </div>

  <div class="team-member-overview">
    <p><strong>Yongzan Liu</strong> is a professor at China University of Petroleum (East China). He previously served as a postdoctoral research fellow at Lawrence Berkeley National Laboratory and as a senior research scientist at Schlumberger-Doll Research. His research focuses on energy geomechanics, particularly coupled thermo-hydro-mechanical modeling of subsurface fractured reservoirs, distributed fiber-optic sensing data interpretation for hydraulic fracture monitoring, the production performance of enhanced geothermal systems, and geological carbon storage. His current work integrates advanced numerical modeling with monitoring techniques to better characterize and understand complex subsurface reservoir processes. He holds a granted U.S. patent, has coauthored one book, and has published over 30 technical papers, including 15 in SPE journals, alongside numerous presentations at SPE conferences. He is a two-time recipient of the SPE Technical Reviewer Outstanding Service Award (2021, 2025) and serves as an associate editor for both <em>SPE Journal</em> and <em>Geoenergy Science and Engineering</em>.</p>
  </div>

  {% for section in site.data.yongzan_liu_cv %}
    <section class="team-member-content" aria-labelledby="pi-{{ section.id }}-title">
      <div class="team-cv-heading">
        <h2 id="pi-{{ section.id }}-title">{{ section.title | escape }}</h2>
      </div>
      <dl class="team-cv-list">
        {% for item in section.items %}
          <div class="team-cv-entry">
            <dt>{{ item.period | escape }}</dt>
            <dd>
              <span class="team-cv-title">{{ item.title | escape }}</span>
              <span class="team-cv-detail">{{ item.detail | escape }}</span>
              {% if item.thesis_key %}
                {% assign thesis = site.data.publications | where: "scholar_key", item.thesis_key | first %}
                {% if thesis %}
                  <span class="team-cv-thesis"><span class="team-cv-thesis-label">{{ item.thesis_label | escape }}:</span> <a href="{{ thesis.link | escape }}">{{ thesis.title | escape }}</a></span>
                {% endif %}
              {% endif %}
            </dd>
          </div>
        {% endfor %}
      </dl>
      {% if section.note %}<p class="team-cv-note">{{ section.note | escape }}</p>{% endif %}
    </section>
  {% endfor %}
</div>
