#!/usr/bin/env python3
"""Build calm, standalone motion variants from the existing approved SVG artwork.

The original SVG files remain untouched. A motion variant is the original SVG
with a small decorative overlay inserted before the closing tag.
No script, remote asset, live data, or additional substantive text is inserted.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FAMILIES = (
    ("assets/hero", "hero-centered-"),
    ("assets/dossier", "profile-card-"),
    ("assets/dossier", "milestones-"),
    ("assets/dossier", "workflow-"),
    ("assets/dossier", "principles-"),
    ("assets/dossier", "github-"),
)

STYLE = """<style>
  .motion-rotor { transform-origin: 0px 0px; animation: motionTurn 32s linear infinite; }
  .motion-dash { animation: motionSweep 14s ease-in-out infinite; }
  .motion-beat { animation: motionBeat 12s ease-in-out infinite; }
  .motion-beat:nth-child(2) { animation-delay: -2s; }
  .motion-beat:nth-child(3) { animation-delay: -4s; }
  .motion-beat:nth-child(4) { animation-delay: -6s; }
  .motion-beat:nth-child(5) { animation-delay: -8s; }
  .motion-beat:nth-child(6) { animation-delay: -10s; }
  .motion-beat:nth-child(7) { animation-delay: -12s; }
  @keyframes motionTurn { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @keyframes motionSweep {
    0%, 8% { stroke-dashoffset: 1600; opacity: 0; }
    15% { opacity: .62; }
    53% { opacity: .5; }
    66%, 100% { stroke-dashoffset: 0; opacity: 0; }
  }
  @keyframes motionBeat {
    0%, 12%, 32%, 100% { opacity: .18; }
    18%, 24% { opacity: .82; }
  }
  @media (prefers-reduced-motion: reduce) {
    .motion-rotor, .motion-dash, .motion-beat { animation: none !important; opacity: .22 !important; }
  }
</style>"""


def rects(svg: str) -> list[tuple[float, float, float, float]]:
    matches = re.finditer(
        r'<rect\b[^>]*?x="([\d.]+)"[^>]*?y="([\d.]+)"[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"[^>]*?rx="([\d.]+)"',
        svg,
    )
    return [(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
            for m in matches if float(m.group(3)) > 100 and float(m.group(4)) > 80]


def fmt(n: float) -> str:
    return f"{n:g}"


def pulse_for_rectangles(svg: str, maximum: int = 7) -> str:
    shapes = []
    for i, (x, y, w, h) in enumerate(rects(svg)[:maximum]):
        # Narrow accents stay inside the original card border; no text is covered.
        shapes.append(
            f'<g class="motion-beat" style="animation-delay:-{i * 1.7:g}s">'
            f'<path d="M{fmt(x+18)} {fmt(y+5)}h{fmt(min(62,w*.18))}" '
            f'stroke="#C89756" stroke-width="3" stroke-linecap="round" opacity=".68"/>'
            f'<circle cx="{fmt(x+w-20)}" cy="{fmt(y+18)}" r="4" fill="#C89756" opacity=".52"/>'
            '</g>'
        )
    return "".join(shapes)


def hero_overlay(svg: str) -> str:
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w, h = (float(vb.group(1)), float(vb.group(2))) if vb else (1600., 760.)
    m = re.search(r'<g transform="translate\(([\d.]+) ([\d.]+)\)"', svg)
    cx, cy = (float(m.group(1)), float(m.group(2))) if m else (w/2, h*.28)
    tail = svg[m.end():] if m else svg
    rad = re.search(r'<circle\b[^>]*\br="([\d.]+)"', tail)
    r = float(rad.group(1)) + 14 if rad else min(w,h)*.16
    # Both the orbit and hairline live in the original decorative regions.
    return (
        f'<g transform="translate({fmt(cx)} {fmt(cy)})" fill="none" aria-hidden="true">'
        f'<g class="motion-rotor"><circle r="{fmt(r)}" stroke="#B58A51" '
        f'stroke-width="1.1" stroke-dasharray="2 23" opacity=".36"/>'
        f'<circle cx="0" cy="-{fmt(r)}" r="4.3" fill="#B58A51" stroke="none" opacity=".65"/></g></g>'
        f'<path class="motion-dash" d="M{fmt(w*.05)} {fmt(h*.138)}H{fmt(w*.95)}" '
        'fill="none" stroke="#B58A51" stroke-width="2.6" '
        'stroke-dasharray="110 1600" stroke-dashoffset="1600" aria-hidden="true"/>'
    )


def principles_overlay(svg: str) -> str:
    marks = re.finditer(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*>(0[1-4])</text>', svg)
    dots = []
    for i, m in enumerate(marks):
        x, y = float(m.group(1)), float(m.group(2))
        dots.append(
            f'<circle class="motion-beat" style="animation-delay:-{i * 2.5:g}s" '
            f'cx="{fmt(x-16)}" cy="{fmt(y-9)}" r="5" fill="#C89756" '
            'opacity=".2" aria-hidden="true"/>'
        )
    return "".join(dots)


def github_overlay(svg: str) -> str:
    return (
        '<g aria-hidden="true" fill="none">'
        '<circle class="motion-beat" cx="188" cy="69" r="7" fill="#C89756" '
        'stroke="#C89756" stroke-width="1" opacity=".24"/>'
        '<path class="motion-dash" d="M264 278H1535" '
        'stroke="#B58A51" stroke-width="2.2" stroke-dasharray="100 1600" '
        'stroke-dashoffset="1600"/></g>'
    )


def overlay_for(path: Path, svg: str) -> str:
    name = path.name
    if name.startswith("hero-centered-"):
        return hero_overlay(svg)
    if name.startswith("principles-"):
        return principles_overlay(svg)
    if name.startswith("profile-card-") and "-mobile" not in name:
        # Keep the original SVG source intact but correct visibly cramped desktop labels.
        return ('<style>g:nth-of-type(2) text:nth-of-type(2){font-size:44px}'
                'g:nth-of-type(3) text:nth-of-type(2){font-size:46px}</style>'
                + pulse_for_rectangles(svg, 3))
    if name.startswith("github-"):
        return github_overlay(svg)
    return pulse_for_rectangles(svg)


def main() -> None:
    md = README.read_text(encoding="utf-8")
    created = []
    for folder, prefix in FAMILIES:
        for tone in ("dark", "light"):
            for suffix in ("-mobile", ""):
                name = f"{prefix}{tone}{suffix}.svg"
                source = ROOT / folder / name
                if not source.exists():
                    raise SystemExit(f"Missing source: {source}")
                raw = source.read_text(encoding="utf-8")
                original = raw.rstrip()
                if not original.endswith("</svg>"):
                    raise SystemExit(f"Unexpected SVG ending: {source}")
                motion_name = name[:-4] + "-motion.svg"
                target = source.with_name(motion_name)
                insert = (
                    "\n<!-- MOTION START: decorative SVG-only enhancement; original source is retained -->\n"
                    + STYLE + "\n" + overlay_for(source, original)
                    + "\n<!-- MOTION END -->\n"
                )
                target.write_text(original[:-6] + insert + "</svg>", encoding="utf-8")
                old_ref = f"{folder}/{name}"
                new_ref = f"{folder}/{motion_name}"
                before = md.count(old_ref)
                if before == 1:
                    md = md.replace(old_ref, new_ref)
                elif before == 0 and md.count(new_ref) == 1:
                    pass  # idempotent regeneration after the first successful build
                else:
                    raise SystemExit(f"Expected one source or motion README reference to {old_ref}")
                created.append(str(target.relative_to(ROOT)))
    README.write_text(md, encoding="utf-8")
    print(f"Generated {len(created)} motion variants; original artwork preserved.")
    for item in created:
        print(item)


if __name__ == "__main__":
    main()
