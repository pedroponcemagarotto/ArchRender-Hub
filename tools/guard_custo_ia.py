#!/usr/bin/env python3
"""ArchRender Hub — P0 guard for selecting zero-additional-cost AI pathways.

This is a configuration gate for future engine adapters. It does NOT intercept
arbitrary network calls in other software: any future UI/adapter invoking AI
must use this guard and no paid provider SDK may bypass it.
No dependencies or network calls. Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "catalog" / "motores_ia_custo_zero.json"
ALLOWED_ENGINE_IDS = {"chatgpt_manual", "offline_editing", "comfyui_local"}
ALLOWED_MANUAL = {"chatgpt_manual", "offline_editing"}
LOCAL_GENERATION_ID = "comfyui_local"
_ID = re.compile(r"^[a-z][a-z0-9_]{2,39}$")


def _verify_policy(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Politica de IA deve ser objeto JSON.")
    if data.get("allow_paid_ai") is not False:
        raise ValueError("Politica deve proibir IA paga.")
    budget = data.get("max_extra_ai_cost_brl")
    if type(budget) not in (int, float) or budget != 0:
        raise ValueError("Orcamento adicional de IA deve ser numerico e igual a zero.")
    engines = data.get("allowed_engines")
    if not isinstance(engines, list) or len(engines) != 3:
        raise ValueError("Esperadas apenas as tres rotas de custo zero permitidas.")
    ids = [e.get("id") for e in engines if isinstance(e, dict)]
    if len(ids) != 3 or set(ids) != ALLOWED_ENGINE_IDS:
        raise ValueError("Motor desconhecido, duplicado ou nao autorizado.")
    by_id = {}
    for engine in engines:
        name = engine.get("id")
        if not _ID.fullmatch(name):
            raise ValueError("ID de motor invalido.")
        price = engine.get("additional_paid_ai_cost_brl")
        if type(price) not in (int, float) or price != 0:
            raise ValueError("Motor apresenta custo IA diferente de zero.")
        if type(engine.get("enabled")) is not bool:
            raise ValueError("Ativacao deve ser booleana.")
        if type(engine.get("supports_automated_external_generation")) is not bool:
            raise ValueError("Declaracao de automacao deve ser booleana.")
        by_id[name] = engine
    for name in ALLOWED_MANUAL:
        if by_id[name]["supports_automated_external_generation"]:
            raise ValueError("Caminho manual nao pode ser declarado API automatica.")
    if by_id[LOCAL_GENERATION_ID]["enabled"]:
        raise ValueError("ComfyUI nao esta homologado e permanece desabilitado.")
    forbidden = data.get("prohibited_paid_services", [])
    if not isinstance(forbidden, list) or "openai_api_paid" not in forbidden:
        raise ValueError("Lista de provedores cobrados deve incluir OpenAI API.")
    return by_id


def load_policy(path: Path = POLICY) -> dict:
    path = Path(path).expanduser().resolve()
    if not path.is_file() or path.stat().st_size > 64 * 1024:
        raise ValueError("Politica de IA nao encontrada ou tamanho excessivo.")
    return _verify_policy(json.loads(path.read_text(encoding="utf-8")))


def authorize(engine_id: str, operation: str = "manual", policy_path: Path = POLICY) -> dict:
    """Fail closed. Explicitly distinguish manual ChatGPT from automatic APIs."""
    if operation not in {"manual", "local_processing", "automatic_generation"}:
        raise ValueError("Operacao invalida.")
    catalog = load_policy(policy_path)
    if engine_id not in catalog:
        raise PermissionError("Motor de IA nao listado na allowlist de custo zero.")
    engine = catalog[engine_id]
    if not engine["enabled"]:
        raise PermissionError("Motor ainda nao habilitado/homologado.")
    if engine_id == "chatgpt_manual" and operation != "manual":
        raise PermissionError("Assinatura ChatGPT nao equivale a API gratuita.")
    if engine_id == "offline_editing" and operation == "automatic_generation":
        raise PermissionError("Modulo offline nao produz imagens generativas.")
    if operation == "automatic_generation" and engine_id != LOCAL_GENERATION_ID:
        raise PermissionError("Geracao automatica so e considerada com motor local homologado.")
    if engine_id == LOCAL_GENERATION_ID and operation == "manual":
        raise PermissionError("Motor local nao e uso manual do ChatGPT.")
    return {"engine_id": engine_id, "operation": operation,
            "additional_ai_cost_brl": 0, "enabled": True,
            "verified_policy_only": True,
            "note": "Esta autorizacao de config nao confirma disponibilidade real de motor e nao executa geracao."}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Bloqueia configuracoes de IA com gasto adicional no ArchRender Hub")
    sub = parser.add_subparsers(dest="action", required=True)
    verify = sub.add_parser("verify", help="Validar arquivo de politica de custo zero.")
    verify.add_argument("--policy", type=Path, default=POLICY)
    choice = sub.add_parser("authorize", help="Validar uma selecao de motor; NAO executa o motor.")
    choice.add_argument("--engine", required=True)
    choice.add_argument("--operation", choices=("manual", "local_processing", "automatic_generation"), default="manual")
    choice.add_argument("--policy", type=Path, default=POLICY)
    args = parser.parse_args(argv)
    try:
        if args.action == "verify":
            engines = load_policy(args.policy)
            result = {"status": "zero_paid_ai", "extra_ai_budget_brl": 0,
                      "enabled": [key for key, item in engines.items() if item["enabled"]]}
        else:
            result = authorize(args.engine, args.operation, args.policy)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, PermissionError, json.JSONDecodeError) as exc:
        print("BLOQUEADO: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
