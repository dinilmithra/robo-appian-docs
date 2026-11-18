"""Build the documentation's geometric brand artwork from editable SVG sources.

All geometry, including the ROBO APPIAN letter paths, is defined below. No font
files, external images, downloads or existing artwork are used. PNG export needs
Inkscape on PATH. Output is reproducible with the same Inkscape version.

Examples:
    python tools/build_brand_assets.py
    python tools/build_brand_assets.py --svg-only
    python tools/build_brand_assets.py --output-dir brand-preview
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / 'docs' / 'assets' / 'images'
NAVY = '#14253D'
CYAN = '#21A8C8'
TEAL = '#56CBB7'

# Hand-defined geometric strokes in a 100-unit letter grid. No font is used.
LETTERS = {
    'R': (68, 'M0 100V0H40Q64 0 64 24V26Q64 50 40 50H0M36 50L68 100'),
    'O': (64, 'M18 0H46Q64 0 64 18V82Q64 100 46 100H18Q0 100 0 82V18Q0 0 18 0Z'),
    'B': (64, 'M0 100V0H38Q62 0 62 24Q62 50 38 50H0M38 50Q64 50 64 76Q64 100 38 100H0'),
    'A': (64, 'M0 100L32 0L64 100M12 64H52'),
    'P': (64, 'M0 100V0H40Q64 0 64 25Q64 50 40 50H0'),
    'I': (48, 'M0 0H48M24 0V100M0 100H48'),
    'N': (64, 'M0 100V0L64 100V0'),
}


def mark(x: int, y: int, size: int, *, depth: bool = False) -> str:
    layers = ''
    if depth:
        layers = (
            f'<rect x="{x + 28}" y="{y + 30}" width="{size}" height="{size}" '
            f'rx="{size * .203125:g}" fill="{NAVY}" opacity=".10"/>'
            f'<rect x="{x + 14}" y="{y + 15}" width="{size}" height="{size}" '
            f'rx="{size * .203125:g}" fill="{CYAN}" opacity=".26"/>'
        )
    return layers + (
        f'<g transform="translate({x} {y}) scale({size / 512:g})">'
        f'<rect width="512" height="512" rx="104" fill="{NAVY}"/>'
        f'<g fill="none" stroke="{CYAN}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M128 154H232Q278 154 278 200V304H386"/>'
        '<path d="M128 340H196Q232 340 232 304V246Q232 210 278 210"/>'
        '</g>'
        f'<circle cx="128" cy="154" r="25" fill="{CYAN}"/>'
        f'<circle cx="128" cy="340" r="25" fill="{CYAN}"/>'
        f'<circle cx="278" cy="210" r="25" fill="{CYAN}"/>'
        f'<circle cx="386" cy="304" r="31" fill="{TEAL}"/>'
        '</g>'
    )


def wordmark(x: int, y: int, scale: float) -> str:
    cursor = 0
    paths = []
    for word, color in (('ROBO', NAVY), ('APPIAN', CYAN)):
        for letter in word:
            width, path = LETTERS[letter]
            paths.append(f'<path transform="translate({cursor} 0)" d="{path}" stroke="{color}"/>')
            cursor += width + 22
        cursor += 22
    return (f'<g transform="translate({x} {y}) scale({scale:g})" fill="none" '
            'stroke-width="10" stroke-linecap="round" stroke-linejoin="round">'
            + ''.join(paths) + '</g>')


def svg(width: int, height: int, title: str, content: str) -> str:
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">\n'
            f'<title id="title">{title}</title>\n'
            '<desc id="description">Geometric connected-node mark with custom letter paths. '
            'Transparent background; no embedded fonts or images.</desc>\n'
            + content + '\n</svg>\n')


def build_assets(output: Path, *, svg_only: bool = False) -> list[Path]:
    exporter = None if svg_only else shutil.which('inkscape')
    if not svg_only and exporter is None:
        raise RuntimeError('PNG export requires Inkscape on PATH; --svg-only writes the editable sources.')
    output = Path(output).expanduser()
    output.mkdir(parents=True, exist_ok=True)
    artwork = {
        'robo-appian-icon': svg(512, 512, 'Robo Appian connected-node mark', mark(32, 32, 448)),
        'robo-appian-header-logo': svg(1600, 600, 'Robo Appian documentation wordmark',
                                      mark(80, 128, 344) + wordmark(510, 242, 1.10)),
        'robo-appian-logo-3d': svg(1600, 600, 'Robo Appian layered geometric wordmark',
                                  mark(80, 102, 364, depth=True) + wordmark(530, 204, 1.08)
                                  + f'<path d="M530 388H718M752 388H940M974 388H1162" '
                                    f'fill="none" stroke="{TEAL}" stroke-width="10" stroke-linecap="round"/>'),
    }
    written = []
    for name, source in artwork.items():
        vector = output / f'{name}.svg'
        vector.write_text(source, encoding='utf-8', newline='\n')
        written.append(vector)
        if exporter:
            raster = output / f'{name}.png'
            subprocess.run([exporter, str(vector.resolve()), '--export-type=png',
                            f'--export-filename={raster.resolve()}', '--export-background-opacity=0'],
                           check=True, stdout=subprocess.DEVNULL)
            written.append(raster)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT,
                        help='Destination directory; default: docs/assets/images in this project.')
    parser.add_argument('--svg-only', action='store_true', help='Write editable SVGs without requiring Inkscape.')
    args = parser.parse_args(argv)
    try:
        written = build_assets(args.output_dir, svg_only=args.svg_only)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Brand asset generation failed: {exc}\n')
    for path in written:
        print(path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
