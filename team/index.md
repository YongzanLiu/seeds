---
title: Team
nav:
  order: 2
  tooltip: About our team
---

<div class="team-page">
  <h1>Team</h1>

  <div class="team-introduction">
    <p>We are a team of researchers, young professionals, and graduate students with diverse backgrounds in petroleum engineering, applied mathematics, rock mechanics, and mechanical engineering. We work closely with the Reservoir Stimulation Research Group led by Prof. Tiankui Guo at China University of Petroleum (East China) and collaborate with established researchers worldwide on modeling and monitoring of subsurface reservoirs.</p>
    <p>We welcome motivated students who are passionate about subsurface engineering. Explore our <a href="{{ '/research/' | relative_url }}">ongoing research</a> and feel free to <a href="{{ '/contacts/' | relative_url }}">contact us</a> about joining the team!</p>
  </div>

  {% for group in site.data.team %}
    <section class="team-section team-section-{{ group.layout }}" aria-labelledby="team-{{ group.id }}-title">
      <div class="team-section-heading">
        <h2 id="team-{{ group.id }}-title">{{ group.title | escape }}</h2>
      </div>
      <div class="team-grid{% if group.layout == 'pi' %} team-grid-pi{% endif %}">
        {% for member in group.members %}
          {% include team-profile.html member=member placeholder=member.placeholder role=group.role layout=group.layout show_contacts=true %}
        {% endfor %}
        {% assign remaining_placeholders = group.placeholder_count | minus: group.members.size %}
        {% if remaining_placeholders > 0 %}
          {% for slot in (1..remaining_placeholders) %}
            {% include team-profile.html placeholder=true role=group.role layout=group.layout %}
          {% endfor %}
        {% endif %}
      </div>
    </section>
  {% endfor %}
</div>
