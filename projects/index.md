---
title: Software
permalink: /software/
redirect_from:
  - /projects/
nav:
  order: 4
  tooltip: Research software and tools
---

<div class="research-projects-page software-page" aria-labelledby="software-title">
  <div class="overview-heading research-projects-heading">
    <h1 id="software-title">Software</h1>
    <p>One of our goals is to translate <a href="{{ '/research/' | relative_url }}">our research</a> into lightweight software tools that address practical field challenges. Industry partners who sponsor our research may request a licence for the software listed below. Please <a href="{{ '/contacts/' | relative_url }}">contact us</a> to discuss potential collaboration.</p>
  </div>

  {% include research-projects.html projects=site.data.software id_prefix="software" placeholder_label="Image coming soon" %}
</div>
