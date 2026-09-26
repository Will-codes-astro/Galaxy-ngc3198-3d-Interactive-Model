"""Generate high-resolution PNG and SVG QR codes for the EPQ dashboard."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PNG = BASE_DIR / "epq_qr_code.png"
OUTPUT_SVG = BASE_DIR / "epq_qr_code.svg"
TARGET_URL = "https://will-codes-astro.github.io/Galaxy-ngc3198-3d-Interactive-Model/"


def load_qr_modules():
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_H
        from qrcode.image.svg import SvgPathImage
        from PIL import Image  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "qrcode", "pillow"]
        )
        importlib.invalidate_caches()
        import qrcode
        from qrcode.constants import ERROR_CORRECT_H
        from qrcode.image.svg import SvgPathImage
        from PIL import Image  # noqa: F401
    return qrcode, ERROR_CORRECT_H, SvgPathImage


def main() -> None:
    qrcode, error_correct_h, svg_path_image = load_qr_modules()
    code = qrcode.QRCode(
        version=None,
        error_correction=error_correct_h,
        box_size=24,
        border=5,
    )
    code.add_data(TARGET_URL)
    code.make(fit=True)

    png = code.make_image(fill_color="#07111d", back_color="#ffffff")
    png.save(OUTPUT_PNG)
    svg = code.make_image(
        image_factory=svg_path_image,
        fill_color="#07111d",
        back_color="#ffffff",
    )
    svg.save(OUTPUT_SVG)

    print(f"QR target: {TARGET_URL}")
    print(f"Generated {OUTPUT_PNG.name} ({OUTPUT_PNG.stat().st_size:,} bytes)")
    print(f"Generated {OUTPUT_SVG.name} ({OUTPUT_SVG.stat().st_size:,} bytes)")
    print("QR code ready for the configured GitHub Pages deployment.")


if __name__ == "__main__":
    main()