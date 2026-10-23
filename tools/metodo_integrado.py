#!/usr/bin/env python3
"""ArchRender Hub R3: offline deterministic method router and QA recorder.

A helper for *preparing* real ChatGPT image experiments. It DOES NOT generate,
analyse or upload images, does not contact external services or guarantee
architectural fidelity. Inputs/outputs remain local and private in data/.
Supports Python >= 3.9, no third-party packages.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Optional
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "prompts.json"
TASKS = {
    "planta-humanizada": "AR-PLAN-HUM-001",
    "planta-tecnica": "AR-PLAN-TEC-001",
    "fachadas": "AR-EXT-3D-001",
    "interiores": "AR-INT-001",
    "croquis": "AR-WHITEBOX-001",
    "paisagismo": "AR-LAND-001",
    "materiais": "AR-MAT-LUZ-001",
    "video": "AR-VIDEO-001",
    "correcao": "AR-CORR-001",
}
GATE_NAMES = ("geometry", "camera", "materials", "artifacts")
GATE_CHOICES = ("passou", "falhou", "nao_verificavel")
REFERENCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
CODE_FENCE = re.compile(r"~~~(?:text)?\s*\n(.*?)\n~~~", re.DOTALL)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def workflow_dir() -> Path:
    """The only directory to which this tool may save assessments."""
    root = Path(os.environ.get("ARCHRENDER_DATA_DIR", str(ROOT / "data")))
    return root.expanduser().resolve() / "workflows"


def load_catalog() -> dict:
    doc = json.loads(CATALOG.read_text(encoding="utf-8"))
    recipes = doc.get("recipes")
    if not isinstance(recipes, list) or not recipes:
        raise ValueError("O catalogo de receitas esta ausente ou invalido.")
    by_id = {}
    for item in recipes:
        rid = item.get("id")
        if not isinstance(rid, str) or rid in by_id:
            raise ValueError("Catalogo: identificadores invalidos ou repetidos.")
        relpath = item.get("path")
        if not isinstance(relpath, str):
            raise ValueError("Catalogo: caminho invalido.")
        resolved = (ROOT / relpath).resolve()
        allowed = (ROOT / "knowledge" / "prompts").resolve()
        if not resolved.is_relative_to(allowed):
            raise ValueError("Catalogo: receita fora da pasta permitida.")
        if not resolved.is_file() or resolved.suffix != ".md":
            raise ValueError("Catalogo: receita nao encontrada: " + rid)
        by_id[rid] = {**item, "_source_file": resolved}
    return by_id


def text_recipe(entry: dict) -> str:
    """Extract the first documented production prompt, without claiming testing."""
    md = entry["_source_file"].read_text(encoding="utf-8")
    match = CODE_FENCE.search(md)
    if not match:
        raise ValueError("Receita nao possui bloco de prompt: " + entry["id"])
    return match.group(1).strip()


def _clean_list(values: list, field: str) -> list:
    cleaned = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("O campo " + field + " precisa ser texto.")
        value = value.strip()
        if len(value) > 220 or any(ord(ch) < 32 and ch not in "\t" for ch in value):
            raise ValueError("Texto longo ou caractere invalido no campo " + field)
        if value and value not in cleaned:
            cleaned.append(value)
    if len(cleaned) > 20:
        raise ValueError("Limite de 20 itens por lista.")
    return cleaned


def build_contract(recipe_id: str, variant: str, reference_id: str,
                   preserve: list, change: list,
                   lighting: str = "", materials: str = "", camera: str = "") -> dict:
    catalog = load_catalog()
    if recipe_id not in catalog:
        raise ValueError("Receita nao encontrada: " + recipe_id)
    if variant not in ("A", "B", "C"):
        raise ValueError("Variante deve ser A, B ou C.")
    if not REFERENCE_RE.fullmatch(reference_id):
        raise ValueError("O ID de referencia deve ser anonimo, curto e sem espacos.")
    preserve = _clean_list(preserve, "preserve")
    change = _clean_list(change, "change")
    options = _clean_list([lighting, materials, camera], "options")
    del options  # validated above; the named options are retained below.

    recipe = catalog[recipe_id]
    warnings = [
        "Nao foi feita inspeção automatica de pixels; confira a imagem mestre.",
        "Este contrato NAO gera imagens, NAO garante geometria e NAO equivale a benchmark.",
        "Imagem, nome de cliente e endereco real nao devem ser publicados no GitHub.",
    ]
    if not preserve:
        warnings.append("Sem inventario de ancoras fornecido: preencha apos inspecionar a imagem original.")
    if not change:
        warnings.append("Nenhuma alteracao autorizada: nao presumir liberdade para redesenhar.")

    items_to_preserve = "\n".join("- " + x for x in preserve) or "- [INSPECIONAR ANCORAS DA REFERENCIA ORIGINAL]"
    items_to_change = "\n".join("- " + x for x in change) or "- [ESPECIFICAR ALTERACOES PERMITIDAS]"
    core = text_recipe(recipe)
    controls = (
        "IMAGEM MESTRE E PAPEL DAS FONTES\n"
        "Imagem anexada correspondente a " + reference_id
        + " e a unica base geometrica; referencias de estilo nao redefinem a planta.\n\n"
        "ELEMENTOS IMUTAVEIS OBSERVADOS/INFORMADOS\n" + items_to_preserve + "\n\n"
        "ALTERACOES EXPLICITAMENTE AUTORIZADAS\n" + items_to_change + "\n\n"
        "CONDICOES VISUAIS\n"
        "Iluminacao: " + (lighting or "seguir luz original salvo autorizacao") + "\n"
        "Materiais: " + (materials or "nao trocar sem autorizacao") + "\n"
        "Camera: " + (camera or "manter enquadramento e pontos de fuga da origem") + "\n\n"
        "Nao acrescente vãos, paredes, escadas, equipamentos, ambientes, "
        "objetos, dimensoes ou vistas inexistentes. "
        "Ao encontrar dados ilegíveis, tratar como desconhecidos."
    )
    if variant == "A":
        prompt = (
            "Transforme a imagem original anexada em uma apresentacao arquitetonica "
            "realista. Preserve o layout geral e a camera; melhore a iluminacao e as "
            "texturas de forma natural, sem acrescentar elementos nao solicitados. "
            "Nao altere materiais nao autorizados."
        )
    else:
        prompt = (
            "TAREFA E RECEITA ESPECIALIZADA\n" + core + "\n\n"
            + controls
        )
        if variant == "C":
            prompt += (
                "\n\nPROTOCOLO DE PRESERVACAO E CONTROLE\n"
                "Antes de alterar a imagem, identifique na referencia os pontos fixos "
                "listados. Altere somente regioes autorizadas; preserve todo o resto "
                "tanto quanto a ferramenta permitir. NAO aumente o numero de objetos "
                "ou mova aberturas. Depois de gerar, compare original x resultado "
                "em paredes, vãos, camera e mobiliario; em caso de divergencia "
                "geometrica, REPROVE e descreva o erro exato. "
                "Nunca alegue verificacao perfeita sem inspecao real."
            )

    return {
        "schema_version": "R3.0",
        "workflow_id": "AR-WF-" + uuid4().hex[:12],
        "created_at": utc_now(),
        "recipe_id": recipe_id,
        "recipe_status": recipe.get("status", "candidato_nao_testado"),
        "mode": recipe.get("mode", "F"),
        "variant": variant,
        "reference_id_private": reference_id,
        "source_role": "geometria_mestre_original",
        "reviewed_source": False,
        "preserve": preserve,
        "change": change,
        "lighting": lighting,
        "materials": materials,
        "camera": camera,
        "source_recipe": recipe["_source_file"].relative_to(ROOT).as_posix(),
        "prompt": prompt,
        "generation": {
            "status": "nao_executada",
            "tool": None,
            "output_dimensions_px": None,
            "output_reference": None,
            "attempts": 0,
        },
        "qa": {
            "gates": {name: "nao_avaliado" for name in GATE_NAMES},
            "editorial_score": None,
            "decision": "nao_avaliado",
            "client_approved": False,
            "issues": [],
            "human_review_required": True,
        },
        "warnings": warnings,
    }


def _within_private_folder(path: Path) -> Path:
    folder = workflow_dir()
    resolved = path.expanduser().resolve()
    if resolved.suffix.lower() != ".json" or not resolved.is_relative_to(folder):
        raise ValueError("Arquivos de workflow devem ficar em data/workflows/ (privado).")
    return resolved


def save_json_private(doc: dict, destination: Path) -> Path:
    target = _within_private_folder(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Atomic creation prevents accidental overwrites and half-written records.
    # Updates are done to a new version of the record, keeping original evidence.
    payload = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with target.open("xb") as file:
        file.write(payload)
    return target


def assess(doc: dict, gates: dict, score: Optional[int]) -> dict:
    """Record manually reported evidence. Never declare client approval."""
    if not isinstance(doc, dict) or "workflow_id" not in doc or "qa" not in doc:
        raise ValueError("Arquivo nao e um contrato R3.")
    if score is not None and not (0 <= score <= 100):
        raise ValueError("Nota precisa estar entre 0 e 100.")
    if set(gates) != set(GATE_NAMES):
        raise ValueError("Avaliacao exige exatamente os quatro gates.")
    if any(value not in GATE_CHOICES for value in gates.values()):
        raise ValueError("Gates invalidos. Use passou/falhou/nao_verificavel.")
    if any(x == "falhou" for x in gates.values()):
        decision = "reprovado"
    elif any(x == "nao_verificavel" for x in gates.values()):
        decision = "nao_verificavel"
    elif score is None:
        decision = "aguarda_nota_editorial"
    elif score < 85:
        decision = "ajustes_visuais_necessarios"
    else:
        decision = "candidato_a_revisao_humana"
    revised = json.loads(json.dumps(doc, ensure_ascii=False))
    revised["qa"]["gates"] = dict(gates)
    revised["qa"]["editorial_score"] = score
    revised["qa"]["decision"] = decision
    revised["qa"]["client_approved"] = False
    revised["qa"]["human_review_required"] = True
    revised["qa"]["manually_reported_at"] = utc_now()
    # An actual generator output must be confirmed separately; QA is not evidence
    # that the underlying image was generated in this workflow.
    return revised


def list_command(args) -> None:
    items = load_catalog()
    if args.json:
        safe = []
        for item in items.values():
            safe.append({key: val for key, val in item.items() if key != "_source_file"})
        print(json.dumps({"tasks": TASKS, "recipes": safe}, ensure_ascii=False, indent=2))
    else:
        print("Roteador deterministico R3 (nao analisa imagens):")
        for task, rid in TASKS.items():
            print("  {:22s} {:20s} {}".format(task, rid, items[rid]["title"]))


def prepare_command(args) -> None:
    recipe_id = args.recipe_id or TASKS[args.task]
    doc = build_contract(recipe_id, args.variant, args.reference_id,
                         args.preserve or [], args.change or [],
                         args.lighting or "", args.materials or "", args.camera or "")
    destination = workflow_dir() / (doc["workflow_id"] + ".json")
    save_json_private(doc, destination)
    print("Contrato preparado (SEM GERACAO DE IMAGEM): " + str(destination))
    print("Receita: " + recipe_id + " | variante: " + args.variant)
    print("Preservacoes declaradas: " + str(len(doc["preserve"])))
    print("Portoes de QA: todos NAO AVALIADOS")
    if args.show_prompt:
        print("\n--- PROMPT PARA CHATGPT ---\n" + doc["prompt"] + "\n--- FIM ---")


def assess_command(args) -> None:
    source = _within_private_folder(args.file)
    if not source.is_file() or source.stat().st_size > 256 * 1024:
        raise ValueError("Contrato privado inexistente ou grande demais.")
    doc = json.loads(source.read_text(encoding="utf-8"))
    gates = {
        "geometry": args.geometry,
        "camera": args.camera,
        "materials": args.materials,
        "artifacts": args.artifacts,
    }
    result = assess(doc, gates, args.score)
    # Immutable versions preserve the chain of assessments.
    new_path = workflow_dir() / (
        result["workflow_id"] + "-qa-" + uuid4().hex[:8] + ".json"
    )
    save_json_private(result, new_path)
    print("Revisao manual registrada: " + str(new_path))
    print("Decisao: " + result["qa"]["decision"])
    print("Aprovacao do cliente: NAO REGISTRADA automaticamente")


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="ArchRender Hub R3 — roteador local, contrato e QA; sem gerar imagens."
    )
    sub = cli.add_subparsers(dest="action", required=True)
    p_list = sub.add_parser("list", help="Listar nove receitas publicadas.")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(execute=list_command)

    p = sub.add_parser("prepare", help="Preparar contrato para imagem no ChatGPT.")
    task = p.add_mutually_exclusive_group(required=True)
    task.add_argument("--task", choices=tuple(TASKS))
    task.add_argument("--recipe-id")
    p.add_argument("--variant", choices=("A", "B", "C"), default="C")
    p.add_argument("--reference-id", required=True)
    p.add_argument("--preserve", action="append", default=[])
    p.add_argument("--change", action="append", default=[])
    p.add_argument("--lighting", default="")
    p.add_argument("--materials", default="")
    p.add_argument("--camera", default="")
    p.add_argument("--show-prompt", action="store_true")
    p.set_defaults(execute=prepare_command)

    q = sub.add_parser("assess", help="Registrar avaliacao humana de uma geracao.")
    q.add_argument("--file", type=Path, required=True)
    for key in GATE_NAMES:
        q.add_argument("--" + key, choices=GATE_CHOICES, required=True)
    q.add_argument("--score", type=int)
    q.set_defaults(execute=assess_command)
    return cli


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        args.execute(args)
        return 0
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print("ERRO: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
