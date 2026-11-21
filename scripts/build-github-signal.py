#!/usr/bin/env python3
"""Generate tiny, transparent, looped executive-motion rule for GitHub README.

Only Python's standard library and local ffmpeg are needed.
Creates native animated GIFs for GitHub and a still SVG for reduced-motion users.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "motion"
W, H, FPS, N = 1200, 20, 12, 48


def emit_frame(color: tuple[int, int, int]) -> bytes:
    # This helper is unused for full images; per-frame streaming below saves memory.
    raise NotImplementedError


def frame_at(i: int, base: tuple[int, int, int], light: tuple[int, int, int]) -> bytes:
    data = bytearray(W * H * 4)
    # A persistent hairline prevents the animation from looking like a loading bar.
    for x in range(24, W - 24):
        k = (9 * W + x) * 4
        data[k:k + 4] = bytes((*base, 110))
    for x in (24, W - 25):
        for y in range(6, 13):
            k = (y * W + x) * 4
            data[k:k + 4] = bytes((*base, 128))
    center = -160 + (W + 320) * (i / N)
    x0, x1 = max(24, int(center - 180)), min(W - 24, int(center + 10))
    for x in range(x0, x1):
        rel = center - x
        spread = max(0, 1 - rel / 185)
        # Warm travelling glint with a long, understated tail.
        weight = spread ** 2.5
        for y in range(6, 13):
            vertical = max(0, 1 - abs(y - 9) / 4)
            alpha = int(220 * weight * vertical)
            if alpha < 30:
                continue
            k = (y * W + x) * 4
            data[k:k + 4] = bytes((*light, min(255, alpha)))
    for y in range(5, 14):
        for x in range(max(0,int(center)-4), min(W,int(center)+5)):
            if (x-center)**2 + (y-9)**2 > 18:
                continue
            k = (y * W + x) * 4
            data[k:k+4] = bytes((*light, 235))
    return bytes(data)


def generate_gif(name: str, base: tuple[int,int,int], light: tuple[int,int,int]) -> None:
    stream = b"".join(frame_at(i, base, light) for i in range(N))
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pixel_format", "rgba", "-video_size", f"{W}x{H}",
        "-framerate", str(FPS), "-i", "pipe:0",
        "-filter_complex", "[0:v]split[a][b];[a]palettegen=reserve_transparent=1:stats_mode=full[p];[b][p]paletteuse=alpha_threshold=30:diff_mode=rectangle[d]",
        "-map", "[d]", "-loop", "0", str(DEST / name)
    ]
    result = subprocess.run(cmd, input=stream, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", "replace"))
    print(name, (DEST / name).stat().st_size, "bytes")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    generate_gif("executive-signal-light.gif", (119, 88, 51), (188, 124, 55))
    generate_gif("executive-signal-dark.gif", (137, 110, 74), (239, 194, 119))
    static = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="20" viewBox="0 0 1200 20">'
        '<path d="M24 9H1176" stroke="#98764E" stroke-opacity=".6" stroke-width="1"/>'
        '<path d="M24 6V13 M1176 6V13" stroke="#98764E" stroke-opacity=".65"/>'
        '</svg>\n'
    )
    (DEST / "executive-signal-static.svg").write_text(static, encoding="utf-8")


if __name__ == "__main__":
    main()
