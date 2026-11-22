# Studio 3D — Executive GitHub Profile

**Status:** Original, physically rendered 3D artwork built in Blender 4.5 Cycles and published as GitHub-compatible imagery. These are not synthetic SVG isometric drawings and are not stock or copied assets.

## Production

Four scenes: `hero`, `ventures`, `systems`, `skills`. Each uses actual 3D geometry, bevels, physically based glass/chrome/champagne-gold materials, multiple area lights, shadow casting, world environment, and Cycles path tracing / denoising. The Blender program `scripts/render-studio3d.py` is the source of every 3D scene.

The editorial compositor `scripts/build-studio3d-panels.cjs` creates each scene's desktop and mobile layout with bounded typography, plus accessible static WebP and lightweight, gently animated looping GIF. The GIF animation is a subtle graphic light sweep over genuine 3D artwork; it is not claimed to be real-time WebGL, physically rotating 3D video, or a separate interactive engine.

## Contents

- `assets/studio3d/*-render.png`: original Blender source renders.
- `assets/studio3d/*-desktop.webp` and `*-mobile.webp`: stills for reduced-motion users.
- `assets/studio3d/*-desktop.gif` and `*-mobile.gif`: GitHub-compatible moving presentations.
- `assets/cinematic/`: historical vector artwork kept in the repository, not deleted.
- `docs/STUDIO3D-CONTENT-CHECK.txt`: checksum confirming all non-image README text and links were unchanged when these visuals replaced four prior images.

## Rebuild

On a workstation with Blender 4.5, Node.js, Sharp (install with `npm ci --prefix scripts`) and FFmpeg:

```powershell
blender -b --factory-startup --python scripts/render-studio3d.py -- hero 1280 22
blender -b --factory-startup --python scripts/render-studio3d.py -- ventures 1200 18
blender -b --factory-startup --python scripts/render-studio3d.py -- systems 1200 18
blender -b --factory-startup --python scripts/render-studio3d.py -- skills 1280 20
node scripts/build-studio3d-panels.cjs
node scripts/check-studio3d.mjs
```

GitHub README blocks inline JavaScript and real-time 3D. Physically rendered visuals are therefore used here, and any fully interactive 3D experience belongs to the external portfolio.

**Claims and privacy:** The visuals symbolize work categories and operating institutions; they are original artistic abstractions, not official replacements for the organizations' logos, proof of deployments, or demonstrations of confidential production UI. Original public references, evidence and qualifications remain in README.
