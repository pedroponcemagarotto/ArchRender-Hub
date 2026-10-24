#!/usr/bin/env python3
"""ArchRender Hub R3 — photometric retouch without generative AI.

Pure exposure/contrast/saturation/tone curve + bounded sharpening; never moves
windows, doors, furniture or walls because it does not generate image content.

Optional dependency: Pillow (pip install pillow).
Input: PNG, JPEG, WebP. Output: PNG or JPEG.
No network, no paid API, no model download, no source overwrite.
"""
from __future__ import annotations

import argparse
from pathlib import Path
try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError as exc:
    raise SystemExit("Pillow ausente. Instale com: python -m pip install pillow") from exc


PRESETS = {
    # brightness, contrast, saturation, tone gamma, capture sharpening multiplier
    "equilibrado": (1.060, 1.045, 1.045, 0.965, 1.05),
    "interior": (1.065, 1.035, 1.050, 0.960, 1.10),
    "lavanderia": (0.995, 1.070, 1.045, 1.025, 1.10),
}


def render(source: Path, target: Path, preset: str = "equilibrado") -> dict:
    source = source.expanduser().resolve()
    target = target.expanduser().resolve()
    if source == target:
        raise ValueError("Nao sobrescreva a imagem original.")
    if not source.is_file():
        raise ValueError("Imagem de entrada nao encontrada.")
    if target.exists():
        raise FileExistsError("Imagem de saida ja existe; escolha um nome novo.")
    if preset not in PRESETS:
        raise ValueError("Preset desconhecido.")
    if target.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("Saida deve ser PNG ou JPEG.")
    brightness, contrast, saturation, gamma, sharpness = PRESETS[preset]
    with Image.open(source) as img:
        if img.format not in ("PNG", "JPEG", "WEBP"):
            raise ValueError("Entrada deve ser PNG, JPEG ou WebP.")
        original = img.convert("RGB")
        resolution = original.size
        result = ImageEnhance.Brightness(original).enhance(brightness)
        result = ImageEnhance.Contrast(result).enhance(contrast)
        result = ImageEnhance.Color(result).enhance(saturation)
        # Scalar, monotonic, per-pixel curve: no geometric transformation.
        lut = [
            max(0, min(255, round(255 * (i / 255) ** gamma)))
            for i in range(256)
        ]
        result = result.point(lut * 3)
        if sharpness > 1:
            # Mild anti-halo sharpening affects only a ~1 px neighborhood.
            result = result.filter(
                ImageFilter.UnsharpMask(radius=0.8, percent=55, threshold=3)
            )
        if result.size != resolution:
            raise AssertionError("Dimensoes alteradas inesperadamente.")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.suffix.lower() == ".png":
            with target.open("xb") as out:
                result.save(out, format="PNG", optimize=True)
        else:
            with target.open("xb") as out:
                result.save(out, format="JPEG", quality=94, subsampling=0,
                            optimize=True)
        return {
            "source": str(source),
            "result": str(target),
            "preset": preset,
            "width": resolution[0],
            "height": resolution[1],
            "geometry_edited": False,
            "new_objects_generated": False,
            "ai_model": None,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--preset", choices=tuple(PRESETS), default="equilibrado")
    args = parser.parse_args()
    print(render(args.source, args.output, args.preset))


if __name__ == "__main__":
    main()
