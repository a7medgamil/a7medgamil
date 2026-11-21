# Executive Cinematic Dossier — Design and Rebuild

This profile is an **original visual identity**, not a fork or reproduction of Het161 or AbdullahBakir97. Their README presentation techniques informed the visual direction; all final artwork in `assets/cinematic/` was generated for this profile.

## What is in the profile

- **Executive hero:** 3D isometric glass-metal monolith with rotating orbital rings, cinematic editorial hierarchy, and an organizational identity line.
- **Leadership matrix:** Four original presentation cards for Saltrixma LLC, SMI, Flunex Institute and Gate of Scholarships.
- **Systems atlas:** Original orbit linking QADHA, MIYTO, SMI Digital Operations and AIU Smart HR, with intentionally qualified project descriptions.
- **Engineering constellation:** Eight visually connected capability groups grounded in the existing capability inventory.

Each scene has four published variants: desktop GIF, mobile GIF, editable original SVG, and reduced-motion still SVG for each viewport. The standalone SVGs include native SMIL movement; the GIFs are frame-rendered for reliable movement in GitHub's README.

The original nine executive sections and source artwork are preserved. Existing system screenshots, public test evidence, limitations and public-safe references are not removed.

## Rebuild

The source is intentionally free from remote build-time assets. Requires Python 3, Node.js and FFmpeg:

```sh
python scripts/build-cinematic-dossier.py
python scripts/build-cinematic-mobile.py
cd scripts
npm ci
node build-cinematic-gifs.cjs
node check-cinematic-dossier.mjs
```

All eight GIFs are assembled from rasterized frames and loop without interaction. Existing project testing remains in the `profile-visual-assets.yml` action.

## Constraints

GitHub strips custom JavaScript from profile READMEs. Genuine interactive 3D is reserved for the separate executive portfolio; this README uses vector illusion, GIF, and static accessible fallback art without pretending to run WebGL.
