#!/usr/bin/env python3
"""ArchRender R5: safe pixel-level compositing for *actual* image-edit outputs.

Original + candidate + editable grayscale mask -> lossless PNG. Pixels
outside the explicitly editable mask and inside the protected mask remain
byte-for-byte identical in decoded RGBA. This is NOT an AI model: the
candidate must come from an actual image-edit service and be reviewed.

The algorithm cannot prove the candidate came from the supplied original.
A separate provenance gate, scene anchor review and manual approval remain
necessary. No network, cloud account, model download or GPU required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageChops, ImageFilter, ImageOps
except ImportError as err:
    raise SystemExit("Instale Pillow: python -m pip install pillow") from err

MAX_BYTES = 80 * 1024 * 1024
MAX_PIXELS = 28_000_000
DEFAULT_MAX_EDITED_FRACTION = 0.50


def _read_image(path: Path) -> Image.Image:
    if not path.is_file() or not (32 <= path.stat().st_size <= MAX_BYTES):
        raise ValueError("Imagem inexistente, vazia ou maior que 80 MB.")
    with Image.open(path) as f:
        if f.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError("Entrada deve ser PNG, JPEG ou WebP.")
        if f.width * f.height > MAX_PIXELS:
            raise ValueError("Imagem excede 28 megapixels.")
        return f.convert("RGBA")


def _read_mask(path: Path, required_size: tuple) -> Image.Image:
    if not path.is_file() or not (32 <= path.stat().st_size <= MAX_BYTES):
        raise ValueError("Mascara inexistente ou maior que 80 MB.")
    with Image.open(path) as f:
        if f.format != "PNG" or f.mode not in {"1", "L"}:
            raise ValueError("A mascara deve ser PNG em tons de cinza (L/1).")
        if f.size != required_size:
            raise ValueError("Mascara nao tem as mesmas dimensoes do original.")
        return f.convert("L")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def compose(original: Path, candidate: Path, edit_mask: Path, destination: Path,
            protected_mask: Optional[Path] = None, feather: float = 2.0,
            max_edited_fraction: float = DEFAULT_MAX_EDITED_FRACTION) -> dict:
    """Losslessly lock pixels outside mask, even when candidate rearranges scene.

    Mask >0 designates a permitted region; mask 0 is strictly locked.
    The optional protected mask locks all >0 pixels (even within edit mask).
    Feathering only occurs *inside* the permission mask: no external bleed.
    """
    original, candidate, edit_mask, destination = (
        Path(p).expanduser().resolve()
        for p in (original, candidate, edit_mask, destination)
    )
    if protected_mask is not None:
        protected_mask = Path(protected_mask).expanduser().resolve()
    inputs = [original, candidate, edit_mask]
    if protected_mask is not None:
        inputs.append(protected_mask)
    if destination in inputs:
        raise ValueError("A saida nao pode sobrescrever arquivos de entrada.")
    if destination.suffix.lower() != ".png":
        raise ValueError("Saida deve ser PNG sem perdas para preservar pixels bloqueados.")
    if destination.exists():
        raise FileExistsError("Arquivo de saida ja existe; nao sobrescrever.")
    if not (0 <= feather <= 30):
        raise ValueError("Feather deve ficar entre 0 e 30 pixels.")
    if not (0 < max_edited_fraction <= 0.95):
        raise ValueError("Limite max_edited_fraction deve ficar em (0, 0.95].")

    src = _read_image(original)
    edited = _read_image(candidate)
    if src.size != edited.size:
        raise ValueError("Imagem original e candidata precisam ter o mesmo tamanho. Sem redimensionamento automatico.")
    mask = _read_mask(edit_mask, src.size)
    mask_pixels = mask.histogram()
    active = sum(mask_pixels[1:])
    total = src.width * src.height
    if active <= 0:
        raise ValueError("Mascara vazia: nenhuma edicao autorizada.")
    if active / total > max_edited_fraction:
        raise ValueError("Area editavel excede o limite; revise a mascara para evitar redesenho amplo.")

    if feather:
        soft = mask.filter(ImageFilter.GaussianBlur(radius=float(feather)))
        # Only soften INSIDE the authorized area; outside remains alpha zero.
        effective = ImageChops.darker(mask, soft)
    else:
        effective = mask.copy()

    if protected_mask is not None:
        protected = _read_mask(protected_mask, src.size)
        # Every nonzero protected pixel is a HARD lock, regardless of feather.
        lock = protected.point(lambda v: 255 if v > 0 else 0)
        effective = ImageChops.multiply(effective, ImageOps.invert(lock))

    active_final = total - effective.histogram()[0]
    if not active_final:
        raise ValueError("Nenhum pixel permanece editavel apos aplicar protecoes.")

    output = Image.composite(edited, src, effective)
    # Verify *all four channels* outside the permission mask are preserved.
    outside = effective.point(lambda v: 255 if v == 0 else 0)
    difference = ImageChops.difference(src, output)
    if any(ImageChops.multiply(channel, outside).getbbox()
           for channel in difference.split()):
        raise AssertionError("Invariante violada: pixel fora da mascara foi alterado.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as fp:
            output.save(fp, format="PNG", optimize=True)
    except Exception:
        # Do not leave a misleading partial result.
        if destination.is_file():
            destination.unlink()
        raise

    result = {
        "schema": "archrender-mask-r5-1",
        "original_sha256": _sha(original),
        "candidate_sha256": _sha(candidate),
        "edit_mask_sha256": _sha(edit_mask),
        "protected_mask_sha256": _sha(protected_mask) if protected_mask else None,
        "output_sha256": _sha(destination),
        "size_px": list(src.size),
        "editable_fraction_before_protection": round(active / total, 6),
        "editable_fraction_after_protection": round(active_final / total, 6),
        "feather_px": feather,
        "locked_pixel_changes": 0,
        "outside_edit_mask_pixel_changes": 0,
        "architectural_approval": False,
        "generation_status": "nao_verificado_por_este_modulo",
        "provenance_of_candidate": "nao_verificada",
        "manual_qa_required": True,
        "notes": "Fora da mascara e nas zonas protegidas os pixels foram preservados sem perdas; a qualidade dentro da mascara requer revisao humana.",
    }
    return result


def cli(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ArchRender R5 - compor edicao mascarada mantendo pixels bloqueados intactos")
    parser.add_argument("original", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("mask", type=Path, help="PNG grayscale; branco pode editar, preto bloqueia")
    parser.add_argument("output", type=Path, help="PNG novo; nao sobrescreve originais")
    parser.add_argument("--protected-mask", type=Path)
    parser.add_argument("--feather", type=float, default=2.0)
    parser.add_argument("--max-edited-fraction", type=float, default=DEFAULT_MAX_EDITED_FRACTION)
    parser.add_argument("--report", type=Path, help="JSON privado, somente arquivo novo")
    args = parser.parse_args(argv)
    report = compose(args.original, args.candidate, args.mask, args.output,
                     args.protected_mask, args.feather, args.max_edited_fraction)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        path = args.report.expanduser().resolve()
        if path.exists():
            raise FileExistsError("Relatorio ja existe; nao sobrescrever.")
        if path.suffix.lower() != ".json":
            raise ValueError("Relatorio deve ser JSON.")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as fp:
            fp.write(payload + "\n")
        print("Relatorio privado: " + str(path))
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except (ValueError, FileExistsError, OSError) as error:
        raise SystemExit("ERRO: " + str(error)) from error
