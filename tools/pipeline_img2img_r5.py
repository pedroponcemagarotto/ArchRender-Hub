#!/usr/bin/env python3
"""ArchRender R5 integration: source contract -> masked PNG -> visual QA -> private report.

This is an offline coordinator, NOT an image generation engine. A candidate
image must already exist. Even proven source editing does not pass the manual
architectural gates or count as a benchmark automatically.

Requires Pillow, numpy, opencv-python for processing; no cloud/network calls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4

import compor_edicao_mascarada as compositor
import metodo_integrado as metodo
import qa_geometria as qa


def execute(*, original: Path, candidate: Path, mask: Path, output: Path,
            reference_id: str, task: str = "interiores", variant: str = "C",
            preserve: list = None, changes: list = None,
            anchors: list = None, protected_mask: Path = None,
            feather: float = 2.0, mode: str = "unknown",
            generator: str = "unspecified/local", binding_evidence: str = "",
            source_inspected: bool = False, visual: bool = True) -> dict:
    """Perform operations and emit a private document, without approving client."""
    if task not in metodo.TASKS:
        raise ValueError("Tarefa desconhecida; escolha uma das nove receitas.")
    if mode not in ("image_edit", "text_to_image", "local_color", "unknown"):
        raise ValueError("Modo de candidato desconhecido.")
    parsed_anchors = [qa.parse_anchor(item) for item in (anchors or [])]
    if len(parsed_anchors) > qa.MAX_ROIS:
        raise ValueError("Excesso de ancoras: maximo 16.")
    if len({a["id"] for a in parsed_anchors}) != len(parsed_anchors):
        raise ValueError("IDs de ancoras repetidos.")
    if mode != "image_edit" and binding_evidence:
        raise ValueError("Evidencia de edicao de IA so se aplica ao modo image_edit.")
    doc = metodo.build_contract(metodo.TASKS[task], variant, reference_id,
                                preserve or [], changes or [])
    target = Path(output).expanduser().resolve()
    if target.exists():
        raise FileExistsError("Arquivo final ja existe: nao sobrescrever.")
    preview = target.with_name(target.stem + "_qa.png") if visual else None
    if preview is not None and preview.exists():
        raise FileExistsError("Imagem diagnostica ja existe: nao sobrescrever.")
    mask_report = compositor.compose(original, candidate, mask, target,
                                     protected_mask=protected_mask, feather=feather)
    diagnosed, rasters = qa.diagnose(original, target, parsed_anchors)
    # The compositor compares decoded RGBA pixels and the QA compares Canny
    # edges. Neither can verify how the external candidate was generated.
    registered = metodo.register_generation(
        doc, original, target, mode, generator, binding_evidence,
        source_inspected=source_inspected,
    )
    registered["qa_diagnostic"] = diagnosed
    registered["mask_composition"] = mask_report
    registered["qa"]["decision"] = "aguarda_revisao_humana"
    registered["qa"]["human_review_required"] = True
    registered["qa"]["client_approved"] = False
    registered["status"] = "producao_com_mascara_sem_homologacao"

    if preview is not None:
        qa.write_visual(diagnosed, rasters, preview)
        registered["qa_visual_private"] = str(preview)

    private_path = metodo.workflow_dir() / (registered["workflow_id"] + "-R5-" + uuid4().hex[:8] + ".json")
    metodo.save_json_private(registered, private_path)
    return {
        "private_report": str(private_path), "output_private": str(target),
        "workflow_id": registered["workflow_id"],
        "geometry_diagnostic": diagnosed["decision"],
        "edited_fraction": mask_report["editable_fraction_after_protection"],
        "pixels_changed_outside_mask": mask_report["outside_edit_mask_pixel_changes"],
        "generator_attachment_binding": registered["generation"]["binding_status"],
        "client_approved": False,
        "benchmark_completed": False,
    }


def cli(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ArchRender R5 - integrar edicao mascarada + QA + relatorio privado")
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference-id", required=True)
    parser.add_argument("--task", choices=tuple(metodo.TASKS), default="interiores")
    parser.add_argument("--variant", choices=("A", "B", "C"), default="C")
    parser.add_argument("--preserve", action="append", default=[])
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--protected-mask", type=Path)
    parser.add_argument("--feather", type=float, default=2.0)
    parser.add_argument("--candidate-mode", choices=("image_edit", "text_to_image", "local_color", "unknown"), default="unknown")
    parser.add_argument("--tool-name", default="unspecified/local")
    parser.add_argument("--binding-evidence", default="")
    parser.add_argument("--source-inspected", action="store_true")
    parser.add_argument("--no-visual", action="store_true")
    options = parser.parse_args(argv)
    data = execute(
        original=options.original, candidate=options.candidate,
        mask=options.mask, output=options.output,
        reference_id=options.reference_id, task=options.task,
        variant=options.variant, preserve=options.preserve,
        changes=options.change, anchors=options.anchor,
        protected_mask=options.protected_mask, feather=options.feather,
        mode=options.candidate_mode, generator=options.tool_name,
        binding_evidence=options.binding_evidence,
        source_inspected=options.source_inspected,
        visual=not options.no_visual,
    )
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except (ValueError, FileExistsError, OSError, AssertionError) as error:
        print("ERRO: " + str(error), file=sys.stderr)
        raise SystemExit(2) from error
