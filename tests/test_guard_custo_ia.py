"""Budget P0: fail-closed AI engine selection, without triggering an AI service."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import guard_custo_ia as guard


class TestZeroAdditionalAIBudget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="archrender_ai_budget_")
        self.addCleanup(self.tmp.cleanup)
        self.local = Path(self.tmp.name) / "policy.json"
        self.source = json.loads(guard.POLICY.read_text(encoding="utf-8"))

    def write_policy(self, doc):
        self.local.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        return self.local

    def test_01_only_three_free_engines_permitted(self):
        engines = guard.load_policy()
        self.assertEqual({"chatgpt_manual", "offline_editing", "comfyui_local"}, set(engines))
        self.assertFalse(engines["comfyui_local"]["enabled"])
        self.assertTrue(engines["chatgpt_manual"]["enabled"])
        self.assertEqual(self.source["max_extra_ai_cost_brl"], 0)
        self.assertIs(self.source["allow_paid_ai"], False)

    def test_02_subscription_used_only_manually(self):
        result = guard.authorize("chatgpt_manual", "manual")
        self.assertEqual(result["additional_ai_cost_brl"], 0)
        self.assertTrue(result["enabled"])
        with self.assertRaisesRegex(PermissionError, "nao equivale a API"):
            guard.authorize("chatgpt_manual", "automatic_generation")
        with self.assertRaisesRegex(PermissionError, "nao equivale a API"):
            guard.authorize("chatgpt_manual", "local_processing")

    def test_03_offline_editing_is_not_generative_ai(self):
        self.assertEqual(
            0, guard.authorize("offline_editing", "local_processing")["additional_ai_cost_brl"]
        )
        with self.assertRaisesRegex(PermissionError, "nao produz imagens"):
            guard.authorize("offline_editing", "automatic_generation")

    def test_04_comfyui_cannot_run_until_homologation(self):
        with self.assertRaisesRegex(PermissionError, "nao habilitado"):
            guard.authorize("comfyui_local", "automatic_generation")

    def test_05_paid_and_unknown_providers_fail_closed(self):
        for engine in ("openai_api_paid", "runway_paid", "replicate_paid", "unknown", ""):
            with self.subTest(engine=engine):
                with self.assertRaises(PermissionError):
                    guard.authorize(engine, "automatic_generation")

    def test_06_tampering_with_price_or_policy_is_rejected(self):
        doc = json.loads(json.dumps(self.source))
        doc["allow_paid_ai"] = True
        with self.assertRaisesRegex(ValueError, "proibir"):
            guard.load_policy(self.write_policy(doc))
        doc = json.loads(json.dumps(self.source))
        doc["max_extra_ai_cost_brl"] = 0.01
        with self.assertRaisesRegex(ValueError, "zero"):
            guard.load_policy(self.write_policy(doc))
        doc = json.loads(json.dumps(self.source))
        doc["allowed_engines"][0]["additional_paid_ai_cost_brl"] = 0.001
        with self.assertRaisesRegex(ValueError, "diferente de zero"):
            guard.load_policy(self.write_policy(doc))

    def test_07_forbid_disguised_auto_subscription_and_new_engines(self):
        doc = json.loads(json.dumps(self.source))
        doc["allowed_engines"][0]["supports_automated_external_generation"] = True
        with self.assertRaisesRegex(ValueError, "manual"):
            guard.load_policy(self.write_policy(doc))
        doc = json.loads(json.dumps(self.source))
        doc["allowed_engines"].append({
            "id": "luma_api_paid", "enabled": True,
            "supports_automated_external_generation": True,
            "additional_paid_ai_cost_brl": 0
        })
        with self.assertRaisesRegex(ValueError, "tres rotas"):
            guard.load_policy(self.write_policy(doc))

    def test_08_cli_validates_and_blocks_paid_without_side_effects(self):
        script = ROOT / "tools" / "guard_custo_ia.py"
        success = subprocess.run([sys.executable, str(script), "verify"],
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(0, success.returncode, success.stderr)
        self.assertEqual("zero_paid_ai", json.loads(success.stdout)["status"])
        denied = subprocess.run([sys.executable, str(script), "authorize",
                                 "--engine", "openai_api_paid",
                                 "--operation", "automatic_generation"],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(2, denied.returncode)
        self.assertIn("BLOQUEADO:", denied.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
