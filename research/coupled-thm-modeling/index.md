---
title: Coupled THM Modeling and Applications
permalink: /research/coupled-thm-modeling/
---

{% assign project = site.data.research_projects | where: "url", page.url | first %}

<div class="research-project-detail">
  <a class="research-project-back" href="{{ '/research/' | relative_url }}">&larr; Current Research</a>
  <h1>{{ project.title | escape }}</h1>

  <div class="research-project-detail-intro">
    {{ project.summary | markdownify }}
  </div>

  <section class="research-project-section" id="geoftsim-development" aria-labelledby="geoftsim-development-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">1.</span>
      <h2 id="geoftsim-development-title">Development and Verification of GeoFTSim+</h2>
    </div>

    <div class="research-project-section-body">
      <p>Our ongoing development of <strong>GeoFTSim+</strong> focuses on the coupling formulation, its numerical implementation, and model verification. GeoFTSim+ serves as the computational foundation for most of our numerical research. We continually expand its capabilities to address modeling challenges involving coupled processes in fractured reservoirs.</p>

      <h3>Iterative coupling scheme</h3>
      <p>We use a sequential implicit (fixed-stress) scheme, with finite volume discretization for fluid flow and heat transport and finite element discretization for geomechanics. Within each time step, the non-isothermal flow problem is solved through Newton iterations. Updated pressure and temperature then drive the geomechanical solution, followed by an update of medium properties. The outer coupling loop repeats until convergence.</p>
    </div>

    <div class="research-project-figure-grid geoftsim-coupling-figure">
      <figure>
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-development/geoftsim-iterative-coupling-mobile.svg' | relative_url }}">
          <img src="{{ '/images/research-projects/geoftsim-development/geoftsim-iterative-coupling.svg' | relative_url }}" width="1280" height="595" alt="Sequential iterative THM coupling: solve non-isothermal flow with an inner Newton convergence loop, solve geomechanics with updated pressure and temperature, update medium properties, and repeat the outer coupling loop until convergence before advancing time." loading="lazy" decoding="async">
        </picture>
        <figcaption>Sequential iterative coupling of non-isothermal flow and geomechanics.</figcaption>
      </figure>
    </div>

    <div class="research-project-section-body">
      <h3>Model verification</h3>
      <p>The hydromechanical implementation is checked against analytical pore-pressure and displacement responses for the <strong>McNamee&ndash;Gibson problem</strong>. A sand-column consolidation problem provides a further check of <strong>thermal&ndash;hydraulic&ndash;mechanical coupling</strong>, using top-surface settlement under isothermal and non-isothermal conditions.</p>
    </div>

    <div class="research-project-figure-grid geoftsim-verification-figures">
      <figure class="geoftsim-benchmark-model">
        <img src="{{ '/images/research-projects/geoftsim-development/hydromechanical-benchmark-model.png' | relative_url }}" width="1376" height="664" alt="Physical model with a constant strip load on a poroelastic half-space and its graded numerical discretization for the McNamee and Gibson benchmark." loading="lazy" decoding="async">
        <figcaption>McNamee&ndash;Gibson (1960) benchmark: physical model and numerical discretization.</figcaption>
      </figure>
      <figure>
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-development/hydromechanical-benchmark-response-mobile.png' | relative_url }}">
          <img src="{{ '/images/research-projects/geoftsim-development/hydromechanical-benchmark-response.png' | relative_url }}" width="1696" height="616" alt="Comparison of analytical solutions and numerical results for dimensionless pore pressure and displacement at observation points in the McNamee and Gibson problem." loading="lazy" decoding="async">
        </picture>
        <figcaption>Hydromechanical verification: analytical solutions (lines) and numerical results (symbols) for pore pressure and displacement.</figcaption>
      </figure>
      <figure class="geoftsim-thm-verification">
        <picture>
          <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-development/thm-consolidation-verification-mobile.png' | relative_url }}">
          <img src="{{ '/images/research-projects/geoftsim-development/thm-consolidation-verification.png' | relative_url }}" width="1588" height="800" alt="Sand-column consolidation model and comparison of top-surface settlement with reference solutions under isothermal and non-isothermal conditions. Solid lines show model results; dots show reference solutions." loading="lazy" decoding="async">
        </picture>
        <figcaption>THM verification: sand-column model and top-surface settlement under isothermal and non-isothermal conditions. Lines show model results; dots show reference solutions.</figcaption>
      </figure>
    </div>

    <div class="research-project-reference">
      <h3>Selected References</h3>
      <p>Liu, Y., Liu, L., Leung, J. Y., et al. (2020). <a href="https://doi.org/10.1016/j.petrol.2020.107042">Sequentially coupled flow and geomechanical simulation with a discrete fracture model for analyzing fracturing fluid recovery and distribution in fractured ultra-low permeability gas reservoirs.</a> <em>Journal of Petroleum Science and Engineering</em>, <strong>189</strong>, 107042.</p>
      <p>Liu, L., Liu, Y., Yao, J., et al. (2020). <a href="https://doi.org/10.2118/200496-PA">Efficient Coupled Multiphase-Flow and Geomechanics Modeling of Well Performance and Stress Evolution in Shale-Gas Reservoirs Considering Dynamic Fracture Properties.</a> <em>SPE Journal</em>, <strong>25</strong>(03), 1523&ndash;1542.</p>
      <p>Liu, Y., Liu, L., Jin, G., et al. (2023). <a href="https://doi.org/10.1016/j.geoen.2022.211378">Simulation-based evaluation of the effectiveness of fiber-optic sensing in monitoring and optimizing water circulation in next-generation enhanced geothermal systems.</a> <em>Geoenergy Science and Engineering</em>, <strong>221</strong>, 211378.</p>
    </div>
  </section>

  <section class="research-project-section" id="geoftsim-applications" aria-labelledby="geoftsim-applications-title">
    <div class="research-project-section-heading">
      <span class="research-project-section-number" aria-hidden="true">2.</span>
      <h2 id="geoftsim-applications-title">Applications of GeoFTSim+</h2>
    </div>

    <article class="geoftsim-application" id="in-well-strain" aria-labelledby="in-well-strain-title">
      <div class="research-project-section-body">
        <h3 id="in-well-strain-title">Interpreting In-Well Fiber-Optic Strain During Production</h3>
        <p>We use coupled flow and geomechanics simulations to interpret <strong>distributed fiber-optic strain measured along the producing well</strong>. Forward modeling links fracture properties to pressure depletion, rock deformation, and the spatial and temporal patterns of the strain response. These relationships help clarify what in-well strain measurements can reveal about the <strong>near-wellbore fractured zone</strong>.</p>
      </div>

      <div class="research-project-figure-grid in-well-strain-figures">
        <figure>
          <div class="in-well-strain-media">
            <img src="{{ '/images/research-projects/in-well-strain/production-pressure.png' | relative_url }}" width="265" height="245" alt="Simulated pressure distribution showing a localized pressure-depletion region around a fracture during production." loading="lazy" decoding="async">
          </div>
          <figcaption>Simulated reservoir pressure.</figcaption>
        </figure>
        <figure>
          <div class="in-well-strain-media">
            <img src="{{ '/images/research-projects/in-well-strain/production-strain-x.png' | relative_url }}" width="261" height="240" alt="Simulated x-direction rock strain around the producing fracture." loading="lazy" decoding="async">
          </div>
          <figcaption>Simulated x-direction strain, &epsilon;<sub>xx</sub>.</figcaption>
        </figure>
        <figure>
          <div class="in-well-strain-media">
            <img src="{{ '/images/research-projects/in-well-strain/production-strain-waterfall.svg' | relative_url }}" width="500" height="332" alt="Modeled in-well strain-change waterfall showing the variation of fiber-optic strain with location and time." loading="lazy" decoding="async">
          </div>
          <figcaption>Modeled in-well strain-change response.</figcaption>
        </figure>
      </div>

      <div class="research-project-reference">
        <h3>Selected Reference</h3>
        <p>Liu, Y., Jin, G., &amp; Wu, K. (2022). <a href="https://doi.org/10.2118/208587-PA">New Insights on Characteristics of the Near-Wellbore Fractured Zone from Simulated High-Resolution Distributed Strain Sensing Data.</a> <em>SPE Reservoir Evaluation &amp; Engineering</em>, <strong>25</strong>(01), 99&ndash;112.</p>
      </div>
    </article>

    <article class="geoftsim-application" id="stress-redistribution" aria-labelledby="stress-redistribution-title">
      <div class="research-project-section-body">
        <h3 id="stress-redistribution-title">Stress Redistribution Induced by Production and Injection</h3>
        <p>We use coupled flow and geomechanics simulations to examine how pressure changes during production and injection redistribute reservoir stresses. The example below compares <strong>pressure depletion and horizontal stress evolution</strong> in a fractured shale-gas reservoir. Accounting for natural-fracture activation and stress-dependent fracture properties helps assess well performance and the implications for infill drilling and refracturing.</p>
      </div>
      <div class="research-project-figure-grid geoftsim-stress-figures">
        <figure>
          <picture>
            <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-applications/production-pressure-stress-fields-mobile.svg' | relative_url }}">
            <img src="{{ '/images/research-projects/geoftsim-applications/production-pressure-stress-fields.svg' | relative_url }}" width="1000" height="408" alt="Pressure and horizontal normal stresses after 1,500 days of production. Columns show pressure, sigma xx and sigma yy in MPa. The upper row includes all natural fractures; the lower row includes activated natural fractures only." loading="lazy" decoding="async">
          </picture>
          <figcaption>Pressure and horizontal stresses after 1,500 days of production (MPa). Upper row: all natural fractures. Lower row: activated natural fractures only.</figcaption>
        </figure>
      </div>
      <div class="research-project-reference">
        <h3>Selected Reference</h3>
        <p>Liu, L., Liu, Y., Yao, J., et al. (2020). <a href="https://doi.org/10.2118/200496-PA">Efficient Coupled Multiphase-Flow and Geomechanics Modeling of Well Performance and Stress Evolution in Shale-Gas Reservoirs Considering Dynamic Fracture Properties.</a> <em>SPE Journal</em>, <strong>25</strong>(03), 1523&ndash;1542.</p>
      </div>
    </article>

    <article class="geoftsim-application" id="fracturing-fluid-flowback" aria-labelledby="fracturing-fluid-flowback-title">
      <div class="research-project-section-body">
        <h3 id="fracturing-fluid-flowback-title">Fracturing Fluid Flowback and In-Situ Distribution</h3>
        <p>Low fracturing-fluid recovery raises questions about where injected water remains and how it affects subsequent gas production. We use coupled flow and geomechanics simulations to investigate <strong>fracture closure, gravity segregation, and fluid imbibition into the matrix</strong>, together with the effects of proppant distribution and shut-in duration. The simulations link evolving fracture geometry and conductivity to fluid redistribution, flowback, and well performance. The examples below show fluid distribution around a fracture network and the sensitivity of water recovery to natural-fracture permeability.</p>
      </div>
      <div class="research-project-figure-grid geoftsim-flowback-figures">
        <figure>
          <div class="geoftsim-flowback-media">
            <img src="{{ '/images/research-projects/geoftsim-applications/fracturing-fluid-distribution.png' | relative_url }}" width="573" height="291" alt="Simulated fracturing-fluid distribution in a reservoir, with a magnified view of fluid concentrated along intersecting fractures." loading="lazy" decoding="async">
          </div>
          <figcaption>Simulated fluid distribution around a fracture network, with a local enlarged view.</figcaption>
        </figure>
        <figure>
          <div class="geoftsim-flowback-media">
            <img src="{{ '/images/research-projects/geoftsim-applications/fracturing-fluid-water-recovery.png' | relative_url }}" width="1000" height="844" alt="Water recovery versus production time for no natural fractures, lower-permeability natural fractures and higher-permeability natural fractures." loading="lazy" decoding="async">
          </div>
          <figcaption>Effects of natural-fracture permeability on water recovery after three days of shut-in.</figcaption>
        </figure>
      </div>
      <div class="research-project-reference">
        <h3>Selected References</h3>
        <p>Liu, Y., Liu, L., Leung, J. Y., et al. (2020). <a href="https://doi.org/10.1016/j.petrol.2020.107042">Sequentially coupled flow and geomechanical simulation with a discrete fracture model for analyzing fracturing fluid recovery and distribution in fractured ultra-low permeability gas reservoirs.</a> <em>Journal of Petroleum Science and Engineering</em>, <strong>189</strong>, 107042.</p>
        <p>Liu, Y., Leung, J. Y., Chalaturnyk, R. J., et al. (2019). <a href="https://doi.org/10.2118/185043-PA">New Insights on Mechanisms Controlling Fracturing-Fluid Distribution and Their Effects on Well Performance in Shale-Gas Reservoirs.</a> <em>SPE Production &amp; Operations</em>, <strong>34</strong>(03), 564&ndash;585.</p>
      </div>
    </article>

    <article class="geoftsim-application" id="egs-water-circulation" aria-labelledby="egs-water-circulation-title">
      <div class="research-project-section-body">
        <h3 id="egs-water-circulation-title">Water Circulation in Horizontal EGS Doublets</h3>
        <p>We apply coupled THM modeling to investigate water circulation between horizontal wells in enhanced geothermal systems (EGS). Fractures with high conductivity can concentrate flow, accelerate local cooling, and cause early thermal breakthrough. By simulating <strong>distributed temperature sensing (DTS) and distributed strain sensing (DSS)</strong> responses, we examine how their complementary signatures reveal dominant flow paths and help guide circulation strategies to improve heat recovery.</p>
        <p class="geoftsim-egs-case-note">Each figure compares two fracture configurations. The dominant fracture is the rightmost fracture in Case 1 and the leftmost fracture in Case 2.</p>
      </div>
      <div class="research-project-figure-grid geoftsim-egs-figures">
        <figure>
          <div class="geoftsim-egs-media geoftsim-egs-field-media">
            <picture>
            <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-applications/egs-temperature-fields-mobile.svg' | relative_url }}">
            <img src="{{ '/images/research-projects/geoftsim-applications/egs-temperature-fields.svg' | relative_url }}" width="1000" height="422" alt="Modeled temperature fields after two years of water circulation, comparing Case 1 with a dominant rightmost fracture and Case 2 with a dominant leftmost fracture." loading="lazy" decoding="async">
          </picture>
          </div>
          <figcaption>Temperature after two years of water circulation (&deg;C).</figcaption>
        </figure>
        <figure>
          <div class="geoftsim-egs-media geoftsim-egs-field-media">
            <picture>
            <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-applications/egs-strain-fields-mobile.svg' | relative_url }}">
            <img src="{{ '/images/research-projects/geoftsim-applications/egs-strain-fields.svg' | relative_url }}" width="1000" height="400" alt="Modeled strain-change fields after two years, showing stronger thermal contraction around the dominant fracture in each case." loading="lazy" decoding="async">
          </picture>
          </div>
          <figcaption>Strain change after two years of water circulation (m/m).</figcaption>
        </figure>
        <figure>
          <div class="geoftsim-egs-media geoftsim-egs-waterfall-media">
            <picture>
            <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-applications/egs-dts-waterfalls-mobile.svg' | relative_url }}">
            <img src="{{ '/images/research-projects/geoftsim-applications/egs-dts-waterfalls.svg' | relative_url }}" width="1000" height="316" alt="Synthetic distributed temperature sensing waterfalls along production well 2 for Cases 1 and 2. Axes show time in days and location in meters." loading="lazy" decoding="async">
          </picture>
          </div>
          <figcaption>Modeled DTS responses along the horizontal production well (&deg;C).</figcaption>
        </figure>
        <figure>
          <div class="geoftsim-egs-media geoftsim-egs-waterfall-media">
            <picture>
            <source media="(max-width: 700px)" srcset="{{ '/images/research-projects/geoftsim-applications/egs-dss-waterfalls-mobile.svg' | relative_url }}">
            <img src="{{ '/images/research-projects/geoftsim-applications/egs-dss-waterfalls.svg' | relative_url }}" width="1000" height="306" alt="Synthetic distributed strain sensing waterfalls along production well 2 for Cases 1 and 2, with localized strain changes near the dominant fractures." loading="lazy" decoding="async">
          </picture>
          </div>
          <figcaption>Modeled DSS responses along the horizontal production well (m/m).</figcaption>
        </figure>
      </div>
      <div class="research-project-reference">
        <h3>Selected Reference</h3>
        <p>Liu, Y., Liu, L., Jin, G., et al. (2023). <a href="https://doi.org/10.1016/j.geoen.2022.211378">Simulation-based evaluation of the effectiveness of fiber-optic sensing in monitoring and optimizing water circulation in next-generation enhanced geothermal systems.</a> <em>Geoenergy Science and Engineering</em>, <strong>221</strong>, 211378.</p>
      </div>
    </article>
  </section>
</div>
