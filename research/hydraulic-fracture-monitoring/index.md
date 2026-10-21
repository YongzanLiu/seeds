---
title: Hydraulic Fracture Monitoring and Characterization
---

<div class="research-project-detail">
  <a class="research-project-back" href="{{ '/research/' | relative_url }}">&larr; Current Research</a>
  <h1>Hydraulic Fracture Monitoring and Characterization</h1>

  <div class="research-project-detail-intro" markdown="1">

We develop forward models and inversion algorithms to interpret **cross-well distributed fiber-optic strain sensing** data for quantitative hydraulic fracture characterization. Forward models link fracture growth and geometry to strain-rate patterns, while inverse models use differences in signal sensitivity before and after fracture hits to estimate different fracture parameters. Together, these approaches support field assessments of stimulation effectiveness and fracturing design.

  </div>

  <section class="research-project-section" id="geomechanical-modeling" aria-labelledby="geomechanical-modeling-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">1.</span>
      <h2 id="geomechanical-modeling-title">Geomechanical Modeling of Cross-Well Distributed Strain Patterns</h2>
    </div>

    <div class="research-project-section-body">
      <h3>Three-dimensional rock strain</h3>
      <p>We have developed a geomechanical model based on the <strong>displacement discontinuity method (DDM)</strong> to calculate the three-dimensional rock strain induced by fractures with arbitrary geometries. The model resolves spatial strain components around fractures, providing a physical basis for linking fracture geometry and growth to the deformation measured by distributed fiber-optic sensing.</p>
    </div>

    <div class="research-project-figure-grid research-project-strain-components">
      <figure>
        <img src="{{ '/images/research-projects/fracture-modeling/rock-strain-x.png' | relative_url }}" width="842" height="934" alt="Three-dimensional view of the x-direction rock strain induced by a single fracture." loading="lazy" decoding="async">
        <figcaption>Rock strain in the x direction, &epsilon;<sub>xx</sub>.</figcaption>
      </figure>
      <figure>
        <img src="{{ '/images/research-projects/fracture-modeling/rock-strain-z.png' | relative_url }}" width="842" height="934" alt="Three-dimensional view of the z-direction rock strain induced by the same fracture, aligned with the x-direction view." loading="lazy" decoding="async">
        <figcaption>Rock strain in the z direction, &epsilon;<sub>zz</sub>.</figcaption>
      </figure>
    </div>

    <div class="research-project-section-body">
      <h3>Cross-well strain-rate modeling and fiber slip</h3>
      <p>Using the modeled strain field, we simulate distributed strain and strain-rate responses along monitoring wells at arbitrary orientations relative to fractures. The resulting waterfall plots help relate signal patterns to fracture geometry and propagation. An extension of the model accounts for <strong>fiber slip</strong>, supporting interpretation of measurements from fiber-optic cables deployed inside casing.</p>
    </div>

    <div class="research-project-figure-grid research-project-waterfalls">
      <figure>
        <img src="{{ '/images/research-projects/fracture-modeling/strain-waterfall-standardized.png' | relative_url }}" width="1108" height="826" alt="Modeled cross-well strain-rate response without fiber slippage." loading="lazy" decoding="async">
        <figcaption>Modeled cross-well strain-rate response without fiber slippage.</figcaption>
      </figure>
      <figure>
        <img src="{{ '/images/research-projects/fracture-modeling/strain-waterfall-fiber-slip.png' | relative_url }}" width="1108" height="826" alt="Modeled cross-well strain-rate response with fiber slippage." loading="lazy" decoding="async">
        <figcaption>Modeled cross-well strain-rate response with fiber slippage.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected Reference</h3>
      <p>Liu, Y., Wu, K., Jin, G., &amp; Moridis, G. J. (2020). <a href="https://doi.org/10.2118/202482-PA">Rock deformation and strain-rate characterization during hydraulic fracturing treatments: Insights for interpretation of low-frequency distributed acoustic-sensing signals.</a> <em>SPE Journal</em>, <strong>25</strong>(05), 2251&ndash;2264.</p>
    </div>
  </section>

  <section class="research-project-section" id="strain-inversion" aria-labelledby="strain-inversion-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">2.</span>
      <h2 id="strain-inversion-title">Inversion of Cross-Well Strain Measurements for Hydraulic Fracture Characterization</h2>
    </div>

    <div class="research-project-section-body">
      <p>We develop deterministic inversion algorithms based on <strong>nonlinear least squares</strong> and stochastic inversion algorithms based on <strong>Markov chain Monte Carlo (MCMC)</strong> to estimate fracture parameters from cross-well distributed strain measurements. The target parameters reflect differences in data sensitivity before and after a fracture hit. We evaluate the algorithms using synthetic cases with prescribed fracture properties.</p>

      <h3>Before Fracture Hit</h3>
      <p>Before the fracture reaches the monitoring well, we use distributed strain measurements to estimate the <strong>fracture half-length and aperture distribution</strong>. Synthetic tests compare modeled strain responses with noisy input data and examine how measurement noise affects the inferred fracture parameters.</p>
    </div>

    <div class="research-project-figure-grid research-project-inversion-figures research-project-before-hit-figures">
      <figure class="research-project-inversion-fit-figure">
        <img src="{{ '/images/research-projects/fracture-inversion/before-hit-strain-fit.png' | relative_url }}" width="2658" height="1654" alt="Modeled and input synthetic strain data with 2 percent noise, and strain profiles at selected times before a fracture hit." loading="lazy" decoding="async">
        <figcaption>Modeled and input strain data for a synthetic case with 2% noise, with strain profiles at selected times.</figcaption>
      </figure>
      <figure class="research-project-inversion-parameter-figure">
        <img src="{{ '/images/research-projects/fracture-inversion/before-hit-fracture-parameters.png' | relative_url }}" width="2198" height="1604" alt="Prescribed curves and inverted estimates of fracture half-length and aperture for synthetic measurements with no noise and with 2, 4, and 6 percent noise." loading="lazy" decoding="async">
        <figcaption>Recovered fracture half-length and aperture for synthetic data with different noise levels.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected Reference</h3>
      <p>Liu, Y., et al. (2024). <a href="https://doi.org/10.1007/s00603-024-03853-2">Inference of Intermittent Hydraulic Fracture Tip Advancement Through Inversion of Low-Frequency Distributed Acoustic Sensing Data.</a> <em>Rock Mechanics and Rock Engineering</em>, <strong>57</strong>(8), 6337&ndash;6353.</p>
    </div>

    <div class="research-project-section-body">
      <h3>After Fracture Hit</h3>
      <p>After the fracture intersects the monitoring well, the inversion focuses on <strong>local equivalent fracture height and aperture</strong> near the intersection. Synthetic cases with different well spacings are used to assess parameter recovery by comparing inverted results with prescribed values.</p>
    </div>

    <div class="research-project-figure-grid research-project-inversion-figures research-project-after-hit-figures">
      <figure>
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/fracture-inversion/after-hit-strain-cases-v2-mobile.svg' | relative_url }}">
          <img src="{{ '/images/research-projects/fracture-inversion/after-hit-strain-cases-v2.svg' | relative_url }}" width="2400" height="700" alt="Synthetic strain responses for monitoring wells at 50, 100, and 150 metre spacings." loading="lazy" decoding="async">
        </picture>
        <figcaption>Strain responses in three synthetic cases used to test post-hit inversion.</figcaption>
      </figure>
      <figure class="research-project-inversion-local-figure">
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/fracture-inversion/after-hit-local-parameters-v2-mobile.svg' | relative_url }}">
          <img src="{{ '/images/research-projects/fracture-inversion/after-hit-local-parameters-v2.svg' | relative_url }}" width="2300" height="900" alt="Prescribed and inverted fracture aperture and local equivalent height for 50, 100, and 150 metre well spacings, including error bars." loading="lazy" decoding="async">
        </picture>
        <figcaption>Prescribed and inverted fracture aperture and local equivalent height for different well spacings.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected Reference</h3>
      <p>Liu, Y., et al. (2024). <a href="https://doi.org/10.1016/j.ijrmms.2023.105610">Stochastic inversion for equivalent hydraulic fracture characterization using low-frequency distributed acoustic sensing data.</a> <em>International Journal of Rock Mechanics and Mining Sciences</em>, <strong>173</strong>, 105610.</p>
    </div>
  </section>

  <section class="research-project-section" id="field-assessment" aria-labelledby="field-assessment-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">3.</span>
      <h2 id="field-assessment-title">Field Assessment of Stimulation Effectiveness and Fracturing Design</h2>
    </div>

    <div class="research-project-section-body">
      <p>We are currently applying our forward and inverse modeling workflow to field measurements from the <strong>HFTS-2 project</strong>. The ongoing analysis uses distributed fiber-optic strain data to characterize fracture growth and geometry before and after fracture hits, with the goal of supporting assessments of stimulation effectiveness and fracturing design.</p>
    </div>

    <div class="research-project-figure-grid research-project-field-layout">
      <figure>
        <img src="{{ '/images/research-projects/fracture-field-application/hfts2-well-layout.png' | relative_url }}" width="854" height="369" alt="HFTS-2 well layout showing the fracturing and fiber-optic monitoring wells, well spacing, and monitoring configuration." loading="lazy" decoding="async">
        <figcaption>HFTS-2 well layout and fiber-optic monitoring configuration.</figcaption>
      </figure>
    </div>

    <div class="research-project-section-body">
      <p>Before a fracture hit, we infer <strong>fracture half-length and maximum aperture</strong> and examine their evolution alongside the pumping history. After a fracture hit, we estimate <strong>local equivalent fracture height and aperture</strong> using data from vertical and horizontal monitoring wells. The examples below show the inferred parameters and comparisons between measured and modeled strain-rate responses.</p>
    </div>

    <div class="research-project-figure-grid research-project-field-composite">
      <figure>
        <div class="research-project-field-panels">
          <div class="research-project-field-panel research-project-field-pre-hit">
            <img src="{{ '/images/research-projects/fracture-field-application/before-hit-field-inversion.png' | relative_url }}" width="508" height="531" alt="Pre-hit HFTS-2 field example showing strain-rate data, bottomhole pressure, slurry rate, inverted fracture half-length and maximum aperture with confidence intervals, and propagation velocity." loading="lazy" decoding="async">
          </div>
          <div class="research-project-field-panel research-project-field-post-hit">
            <img src="{{ '/images/research-projects/fracture-field-application/after-hit-field-parameters.png' | relative_url }}" width="613" height="613" alt="Post-hit HFTS-2 field inversion showing equivalent fracture aperture and height inferred from horizontal and vertical monitoring wells, with uncertainty bands and pumping history." loading="lazy" decoding="async">
          </div>
          <div class="research-project-field-panel research-project-field-response-stack">
            <img src="{{ '/images/research-projects/fracture-field-application/after-hit-field-response-3000-3800m.png' | relative_url }}" width="616" height="574" alt="Vertical monitoring well: measured strain-rate data above the modeled response for the 3000 to 3800 metre trace interval." loading="lazy" decoding="async">
            <img src="{{ '/images/research-projects/fracture-field-application/after-hit-field-response-4000-5000m.png' | relative_url }}" width="646" height="602" alt="Horizontal monitoring well: measured strain-rate data above the modeled response for the 4000 to 5000 metre trace interval." loading="lazy" decoding="async">
          </div>
        </div>
        <figcaption>Field inversion examples. <strong>Left:</strong> pre-hit fracture parameters and pumping history. <strong>Center:</strong> post-hit equivalent fracture aperture and height. <strong>Right:</strong> vertical-well (top) and horizontal-well (bottom) strain-rate comparisons, with measured data above the modeled response in each comparison.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected References</h3>
      <p>Liu, Y., et al. (2023). Stage-level hydraulic fracture width and height quantification through stochastic inversion of distributed fiber-optic strain sensing data. <em>SEG International Exposition and Annual Meeting</em>, SEG.</p>
      <p>Liu, Y., et al. (2022). Quantitative hydraulic-fracture-geometry characterization with low-frequency distributed-acoustic-sensing strain data: Fracture-height sensitivity and field applications. <em>SPE Production &amp; Operations</em>, <strong>37</strong>(02), 159&ndash;168.</p>
    </div>
  </section>
</div>
