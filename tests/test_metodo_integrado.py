"""Offline regression tests for ArchRender Hub's integrated image method."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import metodo_integrado as method  # noqa: E402


class IntegratedMethodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="archrender_method_")
        self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {"ARCHRENDER_DATA_DIR": self.tmp.name})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_01_catalog_contains_exactly_nine_valid_recipes(self):
        recipes = method.load_catalog()
        self.assertEqual(len(recipes), 9)
        self.assertEqual(set(method.TASKS.values()), set(recipes))
        for item in recipes.values():
            text = method.text_recipe(item)
            self.assertTrue(text)
            self.assertIn("candidato_nao_testado", item["status"])

    def test_02_prepare_c_preserves_anchors_without_claiming_image(self):
        doc = method.build_contract(
            "AR-INT-001", "C", "ref-cozinha-001",
            ["janela preta a direita", "geladeira inox"],
            ["melhorar iluminacao"], "luz difusa", "mesmos materiais",
            "perspectiva original"
        )
        self.assertEqual(doc["variant"], "C")
        self.assertEqual(doc["reference_id_private"], "ref-cozinha-001")
        self.assertIn("janela preta a direita", doc["prompt"])
        self.assertIn("PROTOCOLO DE PRESERVACAO", doc["prompt"])
        self.assertEqual(doc["generation"]["status"], "nao_executada")
        self.assertEqual(doc["qa"]["decision"], "nao_avaliado")
        self.assertFalse(doc["qa"]["client_approved"])
        self.assertFalse(doc["reviewed_source"])

    def test_03_variant_a_b_c_are_distinct(self):
        a = method.build_contract("AR-INT-001", "A", "ref1", [], [])
        b = method.build_contract("AR-INT-001", "B", "ref1", [], [])
        c = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        self.assertNotEqual(a["prompt"], b["prompt"])
        self.assertTrue(c["prompt"].startswith(b["prompt"]))
        self.assertTrue(any("inventario" in x for x in c["warnings"]))

    def test_04_reject_private_identifiers_and_nonexistent_recipe(self):
        for bad in ("/etc/passwd", "C:\\Usuarios\\Meu Projeto", "../cliente", "id com espaco", "a"*65):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "anonimo"):
                    method.build_contract("AR-INT-001", "C", bad, [], [])
        with self.assertRaisesRegex(ValueError, "nao encontrada"):
            method.build_contract("INEXISTENTE", "C", "ref1", [], [])

    def test_05_private_output_atomic_create_and_never_overwrite(self):
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        private = method.workflow_dir() / (doc["workflow_id"] + ".json")
        method.save_json_private(doc, private)
        self.assertTrue(private.is_file())
        with self.assertRaises(FileExistsError):
            method.save_json_private(doc, private)
        self.assertEqual(json.loads(private.read_text())["workflow_id"], doc["workflow_id"])
        with self.assertRaisesRegex(ValueError, "privado"):
            method.save_json_private(doc, ROOT / "bad-public-file.json")

    def test_06_geometry_failure_never_approved_even_with_100(self):
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        revised = method.assess(doc, {
            "geometry": "falhou", "camera": "passou",
            "materials": "passou", "artifacts": "passou",
        }, 100)
        self.assertEqual(revised["qa"]["decision"], "reprovado")
        self.assertFalse(revised["qa"]["client_approved"])
        self.assertEqual(doc["qa"]["decision"], "nao_avaliado")

    def test_07_all_gates_pass_remains_human_candidate(self):
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        gates = dict.fromkeys(method.GATE_NAMES, "passou")
        revised = method.assess(doc, gates, 93)
        self.assertEqual(revised["qa"]["decision"], "candidato_a_revisao_humana")
        self.assertFalse(revised["qa"]["client_approved"])
        self.assertTrue(revised["qa"]["human_review_required"])
        low = method.assess(doc, gates, 75)
        self.assertEqual(low["qa"]["decision"], "ajustes_visuais_necessarios")
        none = method.assess(doc, gates, None)
        self.assertEqual(none["qa"]["decision"], "aguarda_nota_editorial")

    def test_08_unknown_gate_is_not_verifiable(self):
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        revised = method.assess(doc, {
            "geometry": "nao_verificavel", "camera": "passou",
            "materials": "passou", "artifacts": "passou",
        }, 99)
        self.assertEqual(revised["qa"]["decision"], "nao_verificavel")

    def test_09_cli_list_and_prepare_and_assess(self):
        base = [sys.executable, str(ROOT / "tools" / "metodo_integrado.py")]
        listed = subprocess.run(base + ["list"], capture_output=True, text=True, timeout=15)
        self.assertEqual(0, listed.returncode, listed.stderr)
        self.assertIn("interiores", listed.stdout)
        created = subprocess.run(
            base + [
                "prepare", "--task", "interiores", "--reference-id", "ref-privado",
                "--variant", "C", "--preserve", "cozinha original"
            ], capture_output=True, text=True, timeout=15
        )
        self.assertEqual(0, created.returncode, created.stderr)
        files = list(method.workflow_dir().glob("AR-WF-*.json"))
        self.assertEqual(len(files), 1)
        review = subprocess.run(
            base + [
                "assess", "--file", str(files[0]), "--geometry", "falhou",
                "--camera", "passou", "--materials", "passou",
                "--artifacts", "passou", "--score", "98",
            ], capture_output=True, text=True, timeout=15
        )
        self.assertEqual(0, review.returncode, review.stderr)
        self.assertIn("reprovado", review.stdout)
        finals = list(method.workflow_dir().glob("*-qa-*.json"))
        self.assertEqual(len(finals), 1)
        self.assertFalse(json.loads(finals[0].read_text())["qa"]["client_approved"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
