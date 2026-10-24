#!/usr/bin/env python3
"""ArchRender Hub R4: offline diagnostic of structure between two images.

This tool computes reproducible edge diagnostics by image and by manually
specified regions. It CANNOT establish true architectural correctness, verify
editing provenance, or approve a customer's render. Use manual visual QA.

Dependencies: numpy, opencv-python (or opencv-python-headless); no network.
The source is never changed. Reports should stay outside the public repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Optional

try:
    import cv2
    import numpy as np
except ImportError as error:
    raise SystemExit("Instale dependencias: python -m pip install numpy opencv-python") from error

MAX_BYTES = 60 * 1024 * 1024
MAX_PIXELS = 28_000_000
MAX_ROIS = 16
ANCHOR_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,31}$")


def _read_image(path: Path) -> tuple:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise ValueError("Arquivo nao encontrado: " + str(path))
    if not (32 <= path.stat().st_size <= MAX_BYTES):
        raise ValueError("Arquivo vazio ou excessivo (limite 60 MB).")
    raw = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    if img is None or img.ndim != 3:
        raise ValueError("Imagem invalida: use PNG/JPEG/WebP valido.")
    height, width = img.shape[:2]
    if height * width > MAX_PIXELS:
        raise ValueError("Imagem excede 28 megapixels.")
    return img, hashlib.sha256(raw.tobytes()).hexdigest()


def parse_anchor(value: str) -> dict:
    """name:x1,y1,x2,y2, all coordinates normalized to [0,1]."""
    try:
        name, coords = value.split(":", 1)
        points = [float(s) for s in coords.split(",")]
    except (ValueError, TypeError) as exc:
        raise ValueError("Ancora invalida: use nome:x1,y1,x2,y2") from exc
    if not ANCHOR_RE.fullmatch(name) or len(points) != 4:
        raise ValueError("Ancora invalida: use nome:x1,y1,x2,y2")
    x1, y1, x2, y2 = points
    if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
        raise ValueError("Ancora deve ser retangulo normalizado entre 0 e 1.")
    if (x2 - x1) < 0.02 or (y2 - y1) < 0.02:
        raise ValueError("Ancora muito pequena: minimo 2% em cada dimensao.")
    return {"id": name, "box_normalized": [x1, y1, x2, y2]}


def _edges(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    return cv2.Canny(blur, 60, 135) > 0


def _rates(reference: np.ndarray, result: np.ndarray, tolerance: int = 2) -> dict:
    a = _edges(reference)
    b = _edges(result)
    total_a = int(np.count_nonzero(a))
    total_b = int(np.count_nonzero(b))
    if total_a < 20 or total_b < 20:
        return {"status": "poucos_contornos", "original_edges": total_a,
                "result_edges": total_b, "recall": None, "precision": None}
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tolerance * 2 + 1,) * 2)
    a_dilated = cv2.dilate(a.astype(np.uint8), kernel) > 0
    b_dilated = cv2.dilate(b.astype(np.uint8), kernel) > 0
    recall = float(np.count_nonzero(a & b_dilated)) / total_a
    precision = float(np.count_nonzero(b & a_dilated)) / total_b
    return {"status": "calculado", "original_edges": total_a,
            "result_edges": total_b, "recall": round(recall, 5),
            "precision": round(precision, 5)}


def _roi_pixels(box: list, width: int, height: int) -> tuple:
    x1, y1, x2, y2 = box
    p = (max(0, int(round(x1 * width))), max(0, int(round(y1 * height))),
         min(width, int(round(x2 * width))), min(height, int(round(y2 * height))))
    if p[2] - p[0] < 8 or p[3] - p[1] < 8:
        raise ValueError("Ancora tem menos de oito pixels de largura/altura.")
    return p


def diagnose(original: Path, candidate: Path, anchors: list = None,
             allow_resize: bool = False) -> tuple:
    """Return (report, visualization_inputs) without approving any render."""
    anchors = anchors or []
    if len(anchors) > MAX_ROIS:
        raise ValueError("Limite de 16 ancoras por analise.")
    ids = [a["id"] for a in anchors]
    if len(set(ids)) != len(ids):
        raise ValueError("IDs de ancoras repetidos.")
    src, src_hash = _read_image(Path(original))
    dst, dst_hash = _read_image(Path(candidate))
    sh, sw = src.shape[:2]
    dh, dw = dst.shape[:2]
    matching_size = (sw, sh) == (dw, dh)
    if not matching_size and allow_resize:
        prepared = cv2.resize(dst, (sw, sh), interpolation=cv2.INTER_AREA)
    elif matching_size:
        prepared = dst
    else:
        prepared = None
    report = {
        "schema": "archrender-qa-r4-1", "original_sha256": src_hash,
        "candidate_sha256": dst_hash, "original_size": [sw, sh],
        "candidate_size": [dw, dh], "same_size": matching_size,
        "resized_for_diagnostics": not matching_size and bool(allow_resize),
        "diagnostic_only": True, "architectural_approval": False,
        "tool_checks_edit_provenance": False,
        "human_review_required": True,
        "metric_explanation": "Canny edge overlap with 2-pixel dilation, sensitive to texture and lighting; never proof of structural correctness.",
        "anchors": [], "global": None, "decision": "revisao_manual_obrigatoria",
    }
    if src_hash == dst_hash:
        report["decision"] = "identica_sem_alteracao"
    if prepared is None:
        report["decision"] = "resolucoes_incompativeis"
        return report, (src, dst, None)
    report["global"] = _rates(src, prepared)
    for anchor in anchors:
        box = _roi_pixels(anchor["box_normalized"], sw, sh)
        x1, y1, x2, y2 = box
        region = _rates(src[y1:y2, x1:x2], prepared[y1:y2, x1:x2])
        report["anchors"].append({"id": anchor["id"],
                                 "box_normalized": anchor["box_normalized"],
                                 "box_px": list(box), **region})
    if not matching_size:
        report["decision"] = "revisao_por_redimensionamento"
    elif src_hash != dst_hash:
        scores = [r["recall"] for r in [report["global"], *report["anchors"]]
                  if r and r.get("recall") is not None]
        if scores and min(scores) < 0.7:
            report["decision"] = "alerta_de_deriva_visual"
        else:
            report["decision"] = "conferencia_manual_necessaria"
    return report, (src, dst, prepared)


def write_visual(report: dict, inputs: tuple, path: Path) -> Path:
    """Three side-by-side panes. Missing edges = magenta, new edges = cyan."""
    src, dst, prepared = inputs
    output = Path(path).expanduser().resolve()
    if output.exists():
        raise FileExistsError("Nao sobrescrever visualizacao existente.")
    if not output.suffix.lower() == ".png":
        raise ValueError("Visualizacao deve ser PNG.")
    h, w = src.shape[:2]
    if prepared is None:
        display_dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_AREA)
        diff = np.zeros_like(src)
        title = "DIFFERENT SIZES - NOT ALIGNED"
    else:
        display_dst = prepared
        a, b = _edges(src), _edges(prepared)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        a_wide = cv2.dilate(a.astype(np.uint8), kernel) > 0
        b_wide = cv2.dilate(b.astype(np.uint8), kernel) > 0
        diff = (src.astype(np.float32) * 0.35).astype(np.uint8)
        diff[a & ~b_wide] = (200, 0, 255)  # missing = magenta in BGR
        diff[b & ~a_wide] = (255, 255, 0)  # new = cyan in BGR
        diff[a & b_wide] = (50, 210, 50)  # matched = green
        title = "EDGE DIAGNOSTIC - NOT PROOF"
    originals = src.copy()
    candidates = display_dst.copy()
    for item in report["anchors"]:
        x1, y1, x2, y2 = item["box_px"]
        for img in (originals, candidates, diff):
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 210, 255), 2)
            cv2.putText(img, item["id"][:16], (x1 + 2, max(18, y1 - 7)),
                        cv2.FONT_HERSHEY_SIMPLEX, .58, (30, 30, 30), 3)
            cv2.putText(img, item["id"][:16], (x1 + 2, max(18, y1 - 7)),
                        cv2.FONT_HERSHEY_SIMPLEX, .58, (0, 230, 255), 1)
    target_width = min(780, w)
    target_height = round(h * target_width / w)
    panes = [cv2.resize(frame, (target_width, target_height),
                        interpolation=cv2.INTER_AREA) for frame in (originals, candidates, diff)]
    canvas = np.concatenate(panes, axis=1)
    header = np.full((70, canvas.shape[1], 3), 247, np.uint8)
    names = ("ORIGINAL", "CANDIDATE", title)
    for i, name in enumerate(names):
        cv2.putText(header, name, (i * target_width + 12, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, .68, (30, 47, 32), 2)
    cv2.putText(header, "Manual architectural inspection is mandatory", (15, 61),
                cv2.FONT_HERSHEY_SIMPLEX, .48, (80, 80, 80), 1)
    canvas = np.concatenate((header, canvas), axis=0)
    output.parent.mkdir(parents=True, exist_ok=True)
    ok, buf = cv2.imencode(".png", canvas)
    if not ok:
        raise ValueError("Falha ao codificar PNG.")
    with output.open("xb") as fp:
        fp.write(buf.tobytes())
    return output


def cli(argv: Optional[list] = None) -> int:
    p = argparse.ArgumentParser(description="ArchRender QA R4: geometric edge diagnostic, not approval")
    p.add_argument("original", type=Path)
    p.add_argument("candidate", type=Path)
    p.add_argument("--anchor", action="append", default=[],
                   help="name:x1,y1,x2,y2 normalized coordinates")
    p.add_argument("--resize-for-diagnostics", action="store_true")
    p.add_argument("--json", type=Path, dest="report")
    p.add_argument("--visual", type=Path)
    args = p.parse_args(argv)
    anchors = [parse_anchor(value) for value in args.anchor]
    report, inputs = diagnose(args.original, args.candidate, anchors,
                              allow_resize=args.resize_for_diagnostics)
    if args.visual:
        report["visual"] = str(write_visual(report, inputs, args.visual))
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        file = args.report.expanduser().resolve()
        if file.exists():
            raise FileExistsError("Nao sobrescrever relatorio existente.")
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("x", encoding="utf-8") as fp:
            fp.write(serialized + "\n")
        print("Report: " + str(file))
    else:
        print(serialized)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except (ValueError, FileExistsError, OSError) as exc:
        raise SystemExit("ERRO: " + str(exc)) from exc
