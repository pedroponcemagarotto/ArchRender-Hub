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

    def test_07_all_gates_pass_needs_real_source_binding_before_review(self):
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        gates = dict.fromkeys(method.GATE_NAMES, "passou")
        invalid = method.assess(doc, gates, 100)
        self.assertEqual(invalid["qa"]["decision"], "nao_elegivel_sem_referencia")
        # Simulated, explicitly MANUALLY reviewed evidence for the unit gate.
        # This is a unit fixture, not a visual experiment.
        doc["reviewed_source"] = True
        doc["generation"].update(
            status="gerada", mode="image_edit", source_bound=True,
            source_sha256="a"*64, output_sha256="b"*64,
            binding_evidence="fixture: evidence of attached original",
            tool="fixture",
        )
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

    def test_10_source_binding_requires_real_files_and_manual_proof(self):
        # Valid RGB PNG fixtures, generated locally; not photos or AI outputs.
        import struct
        import zlib
        def png(color):
            def chunk(name, payload):
                return (struct.pack(">I", len(payload)) + name + payload +
                        struct.pack(">I", zlib.crc32(name + payload) & 0xffffffff))
            header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
            return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) +
                    chunk(b"IDAT", zlib.compress(b"\x00" + bytes(color))) +
                    chunk(b"IEND", b""))
        original = Path(self.tmp.name) / "original.png"
        output = Path(self.tmp.name) / "result.png"
        original.write_bytes(png((200, 90, 70)))
        output.write_bytes(png((202, 95, 71)))
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        unknown = method.register_generation(
            doc, original, output, "text_to_image", "ChatGPT Images",
            "the prompt described the source", source_inspected=True,
        )
        self.assertFalse(unknown["generation"]["source_bound"])
        self.assertEqual("nao_comprovado", unknown["generation"]["binding_status"])
        self.assertEqual(
            "nao_elegivel_sem_referencia",
            method.assess(unknown, dict.fromkeys(method.GATE_NAMES, "passou"), 100)
            ["qa"]["decision"],
        )
        reported = method.register_generation(
            doc, original, output, "image_edit", "Tool X",
            "Human-inspected tool record confirms original image attachment",
            source_inspected=True,
        )
        self.assertTrue(reported["generation"]["source_bound"])
        self.assertTrue(method.source_bound_for_qa(reported))
        self.assertEqual(original.read_bytes(), png((200, 90, 70)))

    def test_11_identical_files_and_unknown_mode_are_rejected(self):
        import base64
        original = Path(self.tmp.name) / "original.png"
        # A valid PNG for the purposes of the stdlib signature and hashing.
        original.write_bytes(base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+L0x0AAAAASUVORK5CYII="
        ))
        doc = method.build_contract("AR-INT-001", "C", "ref1", [], [])
        with self.assertRaisesRegex(ValueError, "identicas"):
            method.register_generation(doc, original, original, "image_edit", "tool")
        with self.assertRaisesRegex(ValueError, "Modo"):
            method.register_generation(doc, original, original, "magic", "tool")




if __name__ == "__main__":
    unittest.main(verbosity=2)
