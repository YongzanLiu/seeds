---
title: Monitoring and Modeling of Induced Seismicity
permalink: /research/induced-seismicity/
---

{% assign project = site.data.research_projects | where: "url", page.url | first %}

<div class="research-project-detail induced-seismicity-detail">
  <a class="research-project-back" href="{{ '/research/' | relative_url }}">&larr; Current Research</a>
  <h1>{{ project.title | escape }}</h1>

  <div class="research-project-detail-intro">
    {{ project.summary | markdownify }}
  </div>

  <section class="research-project-section" id="das-event-detection-location" aria-labelledby="das-event-detection-location-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">1.</span>
      <h2 id="das-event-detection-location-title">Automated Microseismic Event Detection and Location Using DAS</h2>
    </div>

    <div class="research-project-section-body">
      <p>We develop automated workflows for microseismic event detection and location using distributed acoustic sensing (DAS). Dense spatial sampling captures coherent seismic arrivals across many channels, but noise and large recording volumes make efficient analysis challenging. Our event-detection workflow has been evaluated using field datasets from the Utah FORGE project. Work on event location is ongoing.</p>
      <p>The detection method scans apparent velocities through slant stacking and measures waveform coherence using semblance in the velocity&ndash;time (v&ndash;t) domain. Adaptive thresholds identify coherent signals, and density-based clustering (DBSCAN) groups the detections. Filtering coherent-noise clusters then yields seismic event windows for further analysis.</p>
    </div>

    <div class="research-project-figure-grid induced-seismicity-detection-figure">
      <figure>
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/induced-seismicity/das-event-detection-workflow-mobile.webp' | relative_url }}">
          <img src="{{ '/images/research-projects/induced-seismicity/das-event-detection-workflow.webp' | relative_url }}" width="3578" height="835" alt="Three stages of waveform-coherence analysis: a FORGE DAS waveform with a scan window, the enlarged local waveform, and semblance in the apparent velocity-time domain." loading="lazy" decoding="async">
        </picture>
        <figcaption>Waveform coherence-based event detection: DAS data, a local scan window, and the apparent velocity&ndash;time transform.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected Reference</h3>
      <p>Liu, Y., Liang, L., Podgornova, O., et al. (2023). Automated Microseismic Event Detection for Downhole Distributed Acoustic Sensing Data Processing. <em>57th US Rock Mechanics/Geomechanics Symposium</em>, ARMA 23&ndash;797.</p>
    </div>
  </section>

  <section class="research-project-section" id="quasi-dynamic-seismicity-modeling" aria-labelledby="quasi-dynamic-seismicity-modeling-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">2.</span>
      <h2 id="quasi-dynamic-seismicity-modeling-title">Quasi-Dynamic Modeling of Induced Seismicity</h2>
    </div>

    <div class="research-project-section-body">
      <p>We couple quasi-dynamic fracture and fault slip with reservoir flow and geomechanics to investigate induced seismicity. The models account for pore-pressure changes, stress redistribution, and frictional weakening, with thermal coupling included for geothermal applications. This work is conducted in collaboration with Dr. Lijun Liu at Chengdu University of Technology.</p>
    </div>

    <div class="research-project-figure-grid induced-seismicity-modeling-figures">
      <figure class="induced-seismicity-co2-figure">
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/induced-seismicity/co2-fault-model-cfs-mobile.webp' | relative_url }}">
          <img src="{{ '/images/research-projects/induced-seismicity/co2-fault-model-cfs.webp' | relative_url }}" width="1768" height="744" alt="CO2 injection model containing a main fault and secondary fractures, paired with the evolution of Coulomb failure stress along the fault during injection." loading="lazy" decoding="async">
        </picture>
        <figcaption>CO<sub>2</sub> injection model and Coulomb failure stress (CFS) evolution along the fault.</figcaption>
      </figure>
      <figure>
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/induced-seismicity/egs-circulation-pressure-temperature-slip-mobile.webp' | relative_url }}">
          <img src="{{ '/images/research-projects/induced-seismicity/egs-circulation-pressure-temperature-slip.webp' | relative_url }}" width="1385" height="339" alt="Pressure, temperature and shear displacement fields with modeled seismic events after 1000 days of EGS circulation. Event colors indicate their occurrence times." loading="lazy" decoding="async">
        </picture>
        <figcaption>Pressure, temperature, and shear displacement with modeled seismic events after 1,000 days of EGS circulation.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected References</h3>
      <p>Liu, L., Ma, H., Wang, X., et al. (2026). <a href="https://doi.org/10.2118/234702-PA">Mechanisms of Fault Reactivation During CO<sub>2</sub> Storage: Quantifying the Spatiotemporal Evolution of Dominant Driving Forces.</a> <em>SPE Journal</em>, SPE 234702-PA.</p>
      <p>Liu, Y., Li, P., Chen, T., et al. Hydraulic connectivity controls circulation-induced seismicity in an EGS doublet: insights from coupled thermal-hydraulic-mechanical modeling. <em>(submitted)</em>.</p>
    </div>
  </section>
</div>
