# GitHub executive motion — reproducible asset build

The README embeds **real looping GIFs** so the icon movement is visible on GitHub without custom JavaScript or CSS. The original institutional card art, technology marks, facts, copy, and static SVG/WEBP assets remain intact.

- Source assets: `assets/hero/` and `assets/dossier/`.
- Generated animations: `assets/live/`, with desktop/mobile and dark/light variants.
- Legacy decorative SVG motion: unchanged in `assets/*/*-motion.svg`.
- Reduced-motion visitors receive the original still graphics through the first `<picture>` sources in README.
- No user metrics, fake GitHub activity, product claims, or third-party assets are generated.

To regenerate on a machine with **Node.js, Python 3 and FFmpeg** on PATH:

```sh
cd scripts
npm ci
npm run build
python optimize-live-profile.py
npm run check
```

The source-generated GIFs are independent of runtime dependencies: **no installation is necessary to view the profile.** CI checks the published assets and does not install Sharp. All image loops are deliberately short, understated, and designed to preserve legibility. Rebuilding these assets requires ensuring the originals have not changed unexpectedly; inspect the visual output at desktop/mobile widths before publishing.

The first-time change from original README image references to animated GIF references was made by `enable-live-profile.py`. Do not rerun that one-time migration after the new references have already been installed.
