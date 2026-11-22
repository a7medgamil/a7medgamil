# Geometric Intelligence — Chromatic Executive GitHub Design

A new visual language for the public executive README: **computational geometry rather than decorative trophies or generic metallic sculptures.** This is an original physical 3D art direction, not a copy of a public GitHub profile or a replacement for any organization's official branding.

## Visual language and meaning

The four finished compositions are physically rendered in Blender 4.5 using Cycles and procedural 3D meshes:
- **Hero:** nested Platonic polyhedral forms, geodesic wireframes, helical DNA-like mathematical constructions, and prismatic ribbons. Represents complex problem solving, computational thinking and technical strategy rather than a literal award or badge.
- **Organizations:** four distinct constructions. Saltrixma uses asymmetric computational polyhedra (amber). SMI uses layered mathematical knowledge architecture (blue/amethyst). Flunex uses parametric ribbon surfaces and optimization trajectories (cyan). Gate of Scholarships uses nested, high-precision opportunity portals (emerald).
- **Systems:** QADHA is a blue modular social product topology (not a court system). MIYTO is a pink audio-wave resonance geometry (not an institutional management system). SMI Operations is an emerald process/data lattice. AIU Smart HR is a violet decision-network representation (an academic design, not an invented deployed system).
- **Capabilities:** a central geodesic intelligence network joins eight color-coded satellite polyhedra, signifying linked engineering disciplines.

Materials are faceted, transmissive, metallic, emissive and physically illuminated. The palette balances a deep navy base with spectral blue, cyan, violet, pink, emerald, orange, and restrained champagne-metal accents. The composition contains large readable editorial type and no invented business logos.

## Source files and publishing

- `scripts/render-geometric-intelligence.py` — original true Blender 3D geometry, stage construction, lights, and Cycles rendering.
- `scripts/build-geometric-intelligence-panels.cjs` — precisely measured desktop/mobile layout, color grading, WebP stills, and GitHub compatible looping GIF outputs.
- `assets/geometric-intelligence/*-render.png` — four source physical Blender render passes.
- `assets/geometric-intelligence/*-desktop.webp` and `*-mobile.webp` — still images used for reduced-motion visitors.
- `assets/geometric-intelligence/*-desktop.gif` and `*-mobile.gif` — lightweight animated presentations for GitHub. Their loop adds a subtle moving light pass over **real rendered** 3D artwork; it is not interactive real-time WebGL.
- `docs/GEOMETRIC-INTELLIGENCE-CONTENT-SHA256.txt` — proof that no non-picture README content changed in this redesign.

## Safe rebuild

Requires Blender 4.5, Node.js 24 or compatible, `npm ci --prefix scripts` (Sharp), and FFmpeg on PATH.

```powershell
blender -b --factory-startup --python scripts/render-geometric-intelligence.py -- hero 1200 16
blender -b --factory-startup --python scripts/render-geometric-intelligence.py -- ventures 1200 16
blender -b --factory-startup --python scripts/render-geometric-intelligence.py -- systems 1200 16
blender -b --factory-startup --python scripts/render-geometric-intelligence.py -- skills 1200 16
node scripts/build-geometric-intelligence-panels.cjs
node scripts/check-geometric-intelligence.mjs
```

Original narratives, names, systems, engineering evidence, links, and qualifications are intentionally retained. Previous visual revisions remain versioned in `assets/studio3d/` and `assets/cinematic/` for rollback; none of their source files are deleted.
